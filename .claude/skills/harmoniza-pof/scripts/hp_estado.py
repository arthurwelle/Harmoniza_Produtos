"""Onda base e manutenção de pendências.

Uso:
  python hp_estado.py iniciar --xlsx DEPARA.xlsx [--fonte-xlsx EVIDENCIA.xlsx] [--melhorias X.xlsx]
                              [--notas NOTAS.txt] [--ref DIR] [--motivo "texto"] [--forcar]
  python hp_estado.py comparar --xlsx OUTRA.xlsx [--ignorar-origem Form]
  python hp_estado.py pendencia --descricao "..." [--origem humano] [--celulas ...] [--grupos ...]

`iniciar` só roda uma vez (onda base): lê FINAL e TodosJuntos de --xlsx e as abas de evidência de
--fonte-xlsx (default: o mesmo arquivo). Depois disso estado/ só muda via hp_onda.py fechar.
`comparar` lista células cujo grupo difere de outra versão da planilha e abre pendências para as que
não têm motivo registrado (ignorando células já citadas por pendências das origens indicadas).
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import pandas as pd

from hp_comum import (ANOS, COLS_DEPARA, COLS_GRUPOS, COLS_PENDENCIAS, COLS_QUADROS, COLS_REGRAS,
                      autor_git, carrega_estado, cel, cod5, dir_estado, dir_h, dir_ondas, grava_csv,
                      grava_json, grava_texto, hoje, junta, limpa, norm_texto, ordena_depara, separa, slug)

ABAS_FONTE = ["Quadros", "NOTAS", "1988", "1995", "2002", "2008", "2017", "juntando88 com 95",
              "Zoom1995", "zoom2002", "zoom2008", "compara2002-08", "compara2008-17",
              "HieraquiaAlimentos", "HieraquiaAlimentos2", "Nova2017"]
COLS_TJ = {"Ano": ["Ano"], "Quadro_H": ["Quadro_H", "Quadro H"], "Desc_Quadro": ["Desc_Quadro"],
           "Codigo": ["Codigo"], "Descri_Item": ["Descri_Item"], "Cod_harmo": ["Cod_harmo"],
           "Descr_Cod_Harmo": ["Descr_Cod_Harmo"]}


def acha_col(cols, *nomes: str) -> str | None:
    """Coluna por nome tolerante a acento, maiúscula, '.', '_' e espaços."""
    alvo = {norm_texto(n) for n in nomes}
    return next((c for c in cols if norm_texto(c) in alvo), None)


def sem_zeros(s: str) -> str:
    return (s.lstrip("0") or "0") if s.isdigit() else s


def nome_limpo(desc: str) -> str:
    """FINAL de alimentos traz 'x.x.x Arroz integralx.x.x Arroz polido' -> 'Arroz integral; Arroz polido'."""
    d = limpa(desc)
    marca = r"x{1,2}(?:\.x{1,2}){1,2}\s*"
    if re.search(marca, d):
        partes = [p.strip() for p in re.split(marca, d) if p.strip()]
        return "; ".join(dict.fromkeys(partes))
    return d.replace("_", " ").strip()


def aba_com_cabecalho(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.iloc[1:].copy()
    df.columns = [limpa(c) or f"col{i}" for i, c in enumerate(raw.iloc[0])]
    return df.applymap(limpa)


def exporta_bruto(raw: pd.DataFrame, destino: Path) -> int:
    df = raw.applymap(limpa)
    df = df.loc[(df != "").any(axis=1), (df != "").any(axis=0)]
    if df.empty:
        return 0
    grava_csv(df, destino)
    return len(df)


def le_todosjuntos(raw: pd.DataFrame) -> pd.DataFrame:
    tj = aba_com_cabecalho(raw)
    ren, faltam = {}, []
    for alvo, nomes in COLS_TJ.items():
        c = acha_col(tj.columns, *nomes)
        if c is None:
            faltam.append(alvo)
        else:
            ren[c] = alvo
    if faltam:
        sys.exit(f"ERRO: TodosJuntos sem colunas {faltam} (tem: {list(tj.columns)})")
    tj = tj.rename(columns=ren)
    tj = tj[(tj["Ano"] != "") | (tj["Codigo"] != "")].copy()
    n_antes = tj.groupby(["Ano", "Codigo"]).ngroups
    tj["Codigo"] = tj["Codigo"].map(sem_zeros)
    if tj.groupby(["Ano", "Codigo"]).ngroups != n_antes:
        sys.exit("ERRO: remover zeros à esquerda do Codigo juntaria células distintas.")
    tj["Cod_harmo"] = tj["Cod_harmo"].map(cod5)
    return tj


def le_final(raw: pd.DataFrame) -> pd.DataFrame:
    fin = aba_com_cabecalho(raw)
    c_n1 = acha_col(fin.columns, "Nivel 1")
    c_n2 = acha_col(fin.columns, "Nivel 2")
    c_desc = acha_col(fin.columns, "Descricao")
    c_cod = acha_col(fin.columns, "Codigo final")
    if not all([c_n1, c_n2, c_desc, c_cod]):
        sys.exit(f"ERRO: FINAL sem Nivel 1/Nivel 2/Descrição/Codigo final (tem: {list(fin.columns)})")
    fin = fin[fin[c_cod] != ""]
    return pd.DataFrame({
        "Cod_harmo": fin[c_cod].map(cod5), "nome": fin[c_desc].map(nome_limpo),
        "nivel1": fin[c_n1], "nivel2": fin[c_n2], "status": "ativo", "criado_em": "base",
        "extinto_em": "", "substituido_por": "", "nome_original": fin[c_desc]})


def iniciar(a) -> None:
    est = dir_estado()
    if (est / "depara.csv").exists() and not a.forcar:
        sys.exit("ERRO: estado/depara.csv já existe. A base só é importada uma vez (use --forcar).")
    xlsx = Path(a.xlsx)
    print(f"Lendo {xlsx.name} ...")
    abas = pd.read_excel(xlsx, sheet_name=None, header=None, dtype=object)
    fonte_xlsx = Path(a.fonte_xlsx) if a.fonte_xlsx else xlsx
    abas_f = abas if fonte_xlsx == xlsx else pd.read_excel(fonte_xlsx, sheet_name=None, header=None, dtype=object)

    autor = a.autor or autor_git()
    onda = f"{hoje()}_{autor}_base"
    pend: list[dict] = []

    def add_pend(origem, descricao, celulas="", grupos=""):
        pend.append(dict(id=f"base#q{len(pend) + 1}", data=hoje(), origem=origem, descricao=descricao,
                         celulas=celulas, grupos=grupos, onda_alvo="", status="aberta", resolvida_em=""))

    # ---- de-para
    tj = le_todosjuntos(abas["TodosJuntos"])
    depara = ordena_depara(tj[COLS_DEPARA].copy())
    quadros = (tj[COLS_QUADROS].drop_duplicates()
               .sort_values(["Ano", "Quadro_H", "Desc_Quadro"]).reset_index(drop=True))
    dup = depara[depara.duplicated(keep=False)]
    if len(dup):
        add_pend("validacao", f"{depara.duplicated().sum()} linhas duplicadas exatas herdadas do TodosJuntos "
                 "(mantidas; decidir se removem).",
                 celulas=junta(sorted({cel(r.Ano, r.Codigo) for r in dup.itertuples()})))
    fora = sorted(set(depara["Ano"]) - set(ANOS))
    if fora:
        add_pend("validacao", f"Anos fora do esperado no de-para: {fora}")

    # ---- grupos
    grupos = le_final(abas["FINAL"])
    dups_g = grupos[grupos["Cod_harmo"].duplicated(keep=False)]
    if len(dups_g):
        add_pend("validacao", "Códigos repetidos na aba FINAL (mantida 1ª ocorrência).",
                 grupos=junta(sorted(set(dups_g["Cod_harmo"]))))
        grupos = grupos.drop_duplicates("Cod_harmo")
    sem_final = sorted(set(depara["Cod_harmo"]) - set(grupos["Cod_harmo"]))
    if sem_final:
        extra = tj[tj["Cod_harmo"].isin(sem_final)].drop_duplicates("Cod_harmo")[["Cod_harmo", "Descr_Cod_Harmo"]]
        grupos = pd.concat([grupos, pd.DataFrame({
            "Cod_harmo": extra["Cod_harmo"], "nome": extra["Descr_Cod_Harmo"].map(nome_limpo),
            "nivel1": "", "nivel2": "", "status": "ativo", "criado_em": "base", "extinto_em": "",
            "substituido_por": "", "nome_original": extra["Descr_Cod_Harmo"]})])
        add_pend("validacao", "Cod_harmo usados no TodosJuntos mas ausentes da FINAL "
                 "(incluídos em grupos.csv sem nível).", grupos=junta(sem_final))
    grupos = grupos.sort_values("Cod_harmo").reset_index(drop=True)
    nomes_lista = grupos["nome_original"].str.contains(r"x{1,2}\.x\.x", regex=True).sum()
    if nomes_lista:
        add_pend("validacao", f"{nomes_lista} grupos (alimentos) têm nome = lista de membros concatenada na "
                 "FINAL; precisam de rótulo curto (onda global de nomes).")

    # ---- fonte
    fonte = dir_h() / "fonte"
    n_fonte = {}
    for aba in ABAS_FONTE:
        if aba in abas_f:
            n = exporta_bruto(abas_f[aba], fonte / f"v2026_{slug(aba)}.csv")
            if n:
                n_fonte[f"{fonte_xlsx.name}/{aba}"] = n
    if a.ref:
        for xls in sorted(Path(a.ref).glob("*.xls*")):
            for nome, raw in pd.read_excel(xls, sheet_name=None, header=None, dtype=object).items():
                n = exporta_bruto(raw, fonte / f"ref_{slug(xls.stem)}_{slug(nome)}.csv")
                if n:
                    n_fonte[f"{xls.name}/{nome}"] = n
    if a.notas:
        shutil.copyfile(a.notas, fonte / "NOTAS.txt")
        n_fonte["NOTAS.txt"] = "copiado"

    # ---- melhorias -> pendências
    if a.melhorias:
        raw = pd.read_excel(a.melhorias, sheet_name=None, header=None, dtype=object)
        for nome, r in raw.items():
            n = exporta_bruto(r, fonte / f"melhorias_{slug(nome)}.csv")
            if n:
                n_fonte[f"{Path(a.melhorias).name}/{nome}"] = n
            m = aba_com_cabecalho(r)
            por_celula: dict[str, list[str]] = {}
            for _, row in m.iterrows():
                vals = [v for v in row.values if v]
                if not vals or (len(vals) == 1 and vals[0] in ANOS):
                    continue
                c = cel(row.get("Ano", ""), sem_zeros(row.get("Codigo", ""))) \
                    if row.get("Ano", "") in ANOS and row.get("Codigo", "") else ""
                if c:
                    por_celula.setdefault(c, []).append(" | ".join(vals))
                else:
                    add_pend("Melhorias", " | ".join(vals))
            for c, linhas in por_celula.items():
                add_pend("Melhorias", f"{len(linhas)} linha(s) da planilha de melhorias: " + " || ".join(linhas),
                         celulas=c)

    # ---- grava estado
    grava_csv(depara, est / "depara.csv", COLS_DEPARA)
    grava_csv(quadros, est / "quadros.csv", COLS_QUADROS)
    grava_csv(grupos, est / "grupos.csv", COLS_GRUPOS)
    grava_csv(pd.DataFrame(columns=COLS_REGRAS), est / "regras.csv", COLS_REGRAS)
    grava_csv(pd.DataFrame(pend, columns=COLS_PENDENCIAS), est / "pendencias.csv", COLS_PENDENCIAS)

    # ---- pasta da onda base
    od = dir_ondas() / onda
    grava_json({"onda": onda, "autor": autor, "tipo": "base", "grupos": [], "celulas": [], "pendencias": [],
                "aberta_em": hoje(), "fonte_xlsx": xlsx.name, "evidencia_xlsx": fonte_xlsx.name}, od / "escopo.json")
    n_cel = depara.drop_duplicates(["Ano", "Codigo"]).groupby("Ano").size()
    linhas_ano = depara.groupby("Ano").size()
    tab = "\n".join(f"| {ano} | {linhas_ano.get(ano, 0)} | {n_cel.get(ano, 0)} |" for ano in ANOS)
    fontes_md = "\n".join(f"- `{k}`: {v} linhas" if isinstance(v, int) else f"- `{k}`: {v}"
                          for k, v in n_fonte.items())
    grava_texto(f"""# Onda base — {onda}

## De onde vem
- De-para e taxonomia: `{xlsx.name}` (abas TodosJuntos e FINAL), importados sem alteração de grupo.
- Abas de evidência (zooms, abas por ano, comparações): `{fonte_xlsx.name}`.
- `Codigo` normalizado sem zeros à esquerda (o pacote harmonizaPOF junta por inteiro).

## Por quê (humano)
{a.motivo or '_preencher_'}

Esta é a **única** alteração de `estado/` sem decisão registrada em `decisoes.csv`: é a hipótese inicial a
auditar. Decisões estruturais tomadas ao montar a base: ver `harmonizacao/adr/`.

## Método
`.claude/skills/harmoniza-pof/CONSTITUICAO.md` e `harmonizacao/origem/chatgpt.txt`.
""", od / "plano.md")
    grava_texto(f"""# Relatório — {onda}

## Importado
| Ano | itens | células |
|---|---|---|
{tab}

- Linhas no de-para: {len(depara)}
- Grupos: {len(grupos)} ({len(sem_final)} sem entrada na FINAL)
- Pendências geradas na importação: {len(pend)}

## Fontes de evidência extraídas para `harmonizacao/fonte/`
{fontes_md}

Cobertura e validação: `hp_cobertura.py` e `hp_validar.py`.
""", od / "relatorio.md")
    print(f"OK: onda {onda}\n  depara {len(depara)} linhas | grupos {len(grupos)} | pendências {len(pend)} | "
          f"fonte {len(n_fonte)} arquivos")


def comparar(a) -> None:
    est = carrega_estado()
    dep, grp, pen = est["depara"], est["grupos"], est["pendencias"]
    base = sorted(dir_ondas().glob("*_base"))
    if not base:
        sys.exit("ERRO: onda base não encontrada")
    od = base[-1]
    outra = Path(a.xlsx)
    abas = pd.read_excel(outra, sheet_name=["TodosJuntos", "FINAL"], header=None, dtype=object)
    tj = le_todosjuntos(abas["TodosJuntos"])
    nomes_o = dict(zip(*[le_final(abas["FINAL"])[c] for c in ("Cod_harmo", "nome")]))
    nomes_a = dict(zip(grp["Cod_harmo"], grp["nome"]))
    atual = dep.groupby(["Ano", "Codigo"])["Cod_harmo"].first()
    outro = tj.groupby(["Ano", "Codigo"])["Cod_harmo"].first()
    itens = dep.groupby(["Ano", "Codigo"])["Descri_Item"].apply(lambda s: " | ".join(dict.fromkeys(s)))
    j = pd.concat([atual.rename("base"), outro.rename("outra")], axis=1)
    dif = j[j["base"] != j["outra"]]

    origens = set(a.ignorar_origem.split(",")) if a.ignorar_origem else set()
    citadas: dict[str, list[str]] = {}
    for r in pen[pen["origem"].isin(origens)].itertuples():
        for c in separa(r.celulas):
            ano, _, cod = c.partition(":")
            citadas.setdefault(f"{ano}:{sem_zeros(cod)}", []).append(r.id)

    linhas, sem_motivo = [], {}
    for (ano, cod), r in dif.iterrows():
        c = f"{ano}:{cod}"
        exp = junta(citadas.get(c, []))
        linhas.append({"celula": c, "grupo_base": r["base"], "nome_base": nomes_a.get(r["base"], ""),
                       "grupo_outra": r["outra"], "nome_outra": nomes_o.get(r["outra"], ""),
                       "explicada_por": exp, "itens": itens.get((ano, cod), "")})
        if not exp:
            sem_motivo.setdefault((r["outra"], r["base"]), []).append(c)
    destino = od / f"diferencas_{slug(outra.stem)}.csv"
    grava_csv(pd.DataFrame(linhas), destino)

    novas = []
    for i, ((g_o, g_b), cels) in enumerate(sorted(sem_motivo.items(), key=lambda kv: -len(kv[1])), 1):
        pid = f"base#d{i}"
        if pid in set(pen["id"]):
            continue
        novas.append({"id": pid, "data": hoje(), "origem": "validacao",
                      "descricao": f"{len(cels)} célula(s) mudaram de grupo entre `{outra.name}` e a base sem motivo "
                                   f"registrado: lá {g_o} ({nomes_o.get(g_o, '?')}), na base {g_b} "
                                   f"({nomes_a.get(g_b, '?')}). Auditar: correção legítima ou erro?",
                      "celulas": junta(cels), "grupos": junta(sorted({g for g in (g_o, g_b) if g})),
                      "onda_alvo": "", "status": "aberta", "resolvida_em": ""})
    if novas:
        grava_csv(pd.concat([pen, pd.DataFrame(novas)], ignore_index=True), dir_estado() / "pendencias.csv",
                  COLS_PENDENCIAS)
    n_exp = sum(1 for l in linhas if l["explicada_por"])
    print(f"OK {len(dif)} células diferem de {outra.name}: {n_exp} explicadas por pendências {sorted(origens)}, "
          f"{len(dif) - n_exp} sem motivo → {len(novas)} pendências de auditoria\n  {destino}")


def pendencia(a) -> None:
    """Acrescenta pendência (não altera a harmonização)."""
    est = carrega_estado()
    pen = est["pendencias"]
    prefixo = f"{hoje()}_{a.autor or autor_git()}"
    n = int(pen["id"].str.startswith(prefixo).sum()) + 1
    cels = junta(c.strip() for c in re.split(r"[,;]", a.celulas or "") if c.strip())
    grupos = junta(cod5(g) for g in re.split(r"[,;]", a.grupos or "") if g.strip())
    nova = {"id": f"{prefixo}#q{n}", "data": hoje(), "origem": a.origem, "descricao": a.descricao,
            "celulas": cels, "grupos": grupos, "onda_alvo": "", "status": "aberta", "resolvida_em": ""}
    grava_csv(pd.concat([pen, pd.DataFrame([nova])], ignore_index=True), dir_estado() / "pendencias.csv",
              COLS_PENDENCIAS)
    print(f"OK pendência {nova['id']}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("iniciar")
    i.add_argument("--xlsx", required=True)
    i.add_argument("--fonte-xlsx")
    i.add_argument("--melhorias")
    i.add_argument("--notas")
    i.add_argument("--ref")
    i.add_argument("--motivo")
    i.add_argument("--autor")
    i.add_argument("--forcar", action="store_true")
    c = sub.add_parser("comparar")
    c.add_argument("--xlsx", required=True)
    c.add_argument("--ignorar-origem", default="Form")
    q = sub.add_parser("pendencia")
    q.add_argument("--origem", default="humano", choices=["Form", "Melhorias", "NOTAS", "validacao", "IA", "humano"])
    q.add_argument("--descricao", required=True)
    q.add_argument("--celulas", default="")
    q.add_argument("--grupos", default="")
    q.add_argument("--autor")
    a = p.parse_args()
    {"iniciar": iniciar, "comparar": comparar, "pendencia": pendencia}[a.cmd](a)


if __name__ == "__main__":
    main()
