"""Onda base: importa a planilha v2026 para harmonizacao/estado e harmonizacao/fonte.

Uso:
  python hp_estado.py iniciar --xlsx CAMINHO/HarmonizacaoProdutos_v2026.xlsx
         [--melhorias CAMINHO.xlsx] [--notas NOTAS.txt] [--ref DIR_COM_XLS] [--forcar]

Só roda uma vez (onda base). Depois disso estado/ só muda via hp_onda.py fechar.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import pandas as pd

from hp_comum import (ANOS, COLS_DEPARA, COLS_GRUPOS, COLS_PENDENCIAS, COLS_QUADROS, COLS_REGRAS,
                      autor_git, cel, cod5, dir_estado, dir_h, dir_ondas, grava_csv, grava_json,
                      grava_texto, hoje, junta, limpa, ordena_depara, slug)

ABAS_FONTE = ["Quadros", "NOTAS", "1988", "1995", "2002", "2008", "2017", "juntando88 com 95",
              "Zoom1995", "zoom2002", "zoom2008", "compara2002-08", "compara2008-17",
              "HieraquiaAlimentos", "HieraquiaAlimentos2", "Nova2017"]


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


def iniciar(a) -> None:
    est = dir_estado()
    if (est / "depara.csv").exists() and not a.forcar:
        sys.exit("ERRO: estado/depara.csv já existe. A base só é importada uma vez (use --forcar).")
    xlsx = Path(a.xlsx)
    print(f"Lendo {xlsx.name} (todas as abas; demora)...")
    abas = pd.read_excel(xlsx, sheet_name=None, header=None, dtype=object)

    autor = a.autor or autor_git()
    onda = f"{hoje()}_{autor}_base"
    pend: list[dict] = []

    def add_pend(origem, descricao, celulas="", grupos=""):
        pend.append(dict(id=f"base#q{len(pend) + 1}", data=hoje(), origem=origem,
                         descricao=descricao, celulas=celulas, grupos=grupos, onda_alvo="",
                         status="aberta", resolvida_em=""))

    # ---- de-para
    tj = aba_com_cabecalho(abas["TodosJuntos"])
    faltam = [c for c in ["Ano", "Quadro_H", "Desc_Quadro", "Codigo", "Descri_Item", "Cod_harmo"]
              if c not in tj.columns]
    if faltam:
        sys.exit(f"ERRO: TodosJuntos sem colunas {faltam}")
    tj = tj[(tj["Ano"] != "") | (tj["Codigo"] != "")]
    tj["Cod_harmo"] = tj["Cod_harmo"].map(cod5)
    depara = ordena_depara(tj[COLS_DEPARA].copy())
    quadros = (tj[COLS_QUADROS].drop_duplicates()
               .sort_values(["Ano", "Quadro_H", "Desc_Quadro"]).reset_index(drop=True))

    dup = depara[depara.duplicated(keep=False)]
    if len(dup):
        add_pend("validacao",
                 f"{depara.duplicated().sum()} linhas duplicadas exatas herdadas do TodosJuntos "
                 f"(mantidas; decidir se removem).",
                 celulas=junta(sorted({cel(r.Ano, r.Codigo) for r in dup.itertuples()})))
    fora = sorted(set(depara["Ano"]) - set(ANOS))
    if fora:
        add_pend("validacao", f"Anos fora do esperado no de-para: {fora}")

    # ---- grupos
    fin = aba_com_cabecalho(abas["FINAL"])
    col_n2 = next(c for c in fin.columns if c.startswith("N") and "2" in c)
    fin = fin[fin["Codigo final"] != ""]
    grupos = pd.DataFrame({
        "Cod_harmo": fin["Codigo final"].map(cod5),
        "nome": fin["Descrição"].map(nome_limpo),
        "nivel1": fin["Nivel 1"],
        "nivel2": fin[col_n2],
        "status": "ativo", "criado_em": "base", "extinto_em": "", "substituido_por": "",
        "nome_original": fin["Descrição"],
    })
    dups_g = grupos[grupos["Cod_harmo"].duplicated(keep=False)]
    if len(dups_g):
        add_pend("validacao", "Códigos repetidos na aba FINAL (mantida 1ª ocorrência).",
                 grupos=junta(sorted(set(dups_g["Cod_harmo"]))))
        grupos = grupos.drop_duplicates("Cod_harmo")
    sem_final = sorted(set(depara["Cod_harmo"]) - set(grupos["Cod_harmo"]))
    if sem_final:
        extra = (tj[tj["Cod_harmo"].isin(sem_final)].drop_duplicates("Cod_harmo")
                 [["Cod_harmo", "Descr_Cod_Harmo"]])
        grupos = pd.concat([grupos, pd.DataFrame({
            "Cod_harmo": extra["Cod_harmo"], "nome": extra["Descr_Cod_Harmo"].map(nome_limpo),
            "nivel1": "", "nivel2": "", "status": "ativo", "criado_em": "base", "extinto_em": "",
            "substituido_por": "", "nome_original": extra["Descr_Cod_Harmo"]})])
        add_pend("validacao", "Cod_harmo usados no TodosJuntos mas ausentes da FINAL "
                 "(incluídos em grupos.csv sem nível).", grupos=junta(sem_final))
    grupos = grupos.sort_values("Cod_harmo").reset_index(drop=True)
    nomes_lista = grupos["nome_original"].str.contains(r"x{1,2}\.x\.x", regex=True).sum()
    if nomes_lista:
        add_pend("validacao", f"{nomes_lista} grupos (alimentos) têm nome = lista de membros "
                 "concatenada na FINAL; precisam de rótulo curto (onda global de nomes).")

    # ---- fonte
    fonte = dir_h() / "fonte"
    n_fonte = {}
    for aba in ABAS_FONTE:
        if aba in abas:
            n_fonte[aba] = exporta_bruto(abas[aba], fonte / f"v2026_{slug(aba)}.csv")
    if a.ref:
        for xls in sorted(Path(a.ref).glob("*.xls*")):
            for nome, raw in pd.read_excel(xls, sheet_name=None, header=None, dtype=object).items():
                dest = fonte / f"ref_{slug(xls.stem)}_{slug(nome)}.csv"
                n_fonte[f"{xls.name}/{nome}"] = exporta_bruto(raw, dest)
    if a.notas:
        shutil.copyfile(a.notas, fonte / "NOTAS.txt")
        n_fonte["NOTAS.txt"] = "copiado"

    # ---- melhorias -> pendências
    if a.melhorias:
        raw = pd.read_excel(a.melhorias, sheet_name=None, header=None, dtype=object)
        for nome, r in raw.items():
            n_fonte[f"{Path(a.melhorias).name}/{nome}"] = exporta_bruto(
                r, fonte / f"melhorias_{slug(nome)}.csv")
            m = aba_com_cabecalho(r)
            por_celula: dict[str, list[str]] = {}
            for _, row in m.iterrows():
                vals = [v for v in row.values if v]
                if not vals or (len(vals) == 1 and vals[0] in ANOS):
                    continue
                c = cel(row.get("Ano", ""), row.get("Codigo", "")) \
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
    grava_json({"onda": onda, "autor": autor, "tipo": "base", "grupos": [], "celulas": [],
                "pendencias": [], "aberta_em": hoje(), "fonte_xlsx": xlsx.name}, od / "escopo.json")
    n_cel = depara.drop_duplicates(["Ano", "Codigo"]).groupby("Ano").size()
    linhas_ano = depara.groupby("Ano").size()
    tab = "\n".join(f"| {ano} | {linhas_ano.get(ano, 0)} | {n_cel.get(ano, 0)} |" for ano in ANOS)
    fontes_md = "\n".join(f"- `{k}`: {v} linhas" if isinstance(v, int) else f"- `{k}`: {v}"
                          for k, v in n_fonte.items())
    grava_texto(f"""# Onda base — {onda}

## Por quê
Ponto de partida da harmonização assistida. Importa sem alterações o de-para da planilha
`{xlsx.name}` (aba TodosJuntos) e a taxonomia (aba FINAL). Decisão do grupo: partir da v2026 local,
ignorar a tentativa Python v2 (pescados/não-alimentos) e absorver sugestões do Google Form como pendências.
Esta é a **única** alteração de `estado/` sem decisão humana registrada: é a hipótese inicial a auditar.

## Método
Ver `.claude/skills/harmoniza-pof/CONSTITUICAO.md` e `harmonizacao/origem/chatgpt.txt`.
""", od / "plano.md")
    grava_texto(f"""# Relatório — {onda}

## Importado
| Ano | itens | células |
|---|---|---|
{tab}

- Linhas no de-para: {len(depara)}
- Grupos: {len(grupos)} ({len(sem_final)} sem entrada na FINAL)
- Pendências abertas geradas: {len(pend)}

## Fontes de evidência extraídas para `harmonizacao/fonte/`
{fontes_md}

Cobertura e validação: rodar `hp_cobertura.py` e `hp_validar.py`.
""", od / "relatorio.md")

    print(f"OK: onda {onda}")
    print(f"  depara {len(depara)} linhas | grupos {len(grupos)} | pendências {len(pend)}")
    print(f"  fonte: {len(n_fonte)} arquivos")


def pendencia(a) -> None:
    """Acrescenta pendência (não altera a harmonização)."""
    from hp_comum import carrega_estado
    est = carrega_estado()
    pen = est["pendencias"]
    prefixo = f"{hoje()}_{a.autor or autor_git()}"
    n = sum(pen["id"].str.startswith(prefixo)) + 1
    cels = junta(c.strip() for c in re.split(r"[,;]", a.celulas or "") if c.strip())
    grupos = junta(cod5(g) for g in re.split(r"[,;]", a.grupos or "") if g.strip())
    nova = {"id": f"{prefixo}#q{n}", "data": hoje(), "origem": a.origem, "descricao": a.descricao,
            "celulas": cels, "grupos": grupos, "onda_alvo": "", "status": "aberta", "resolvida_em": ""}
    pen = pd.concat([pen, pd.DataFrame([nova])], ignore_index=True)
    grava_csv(pen, dir_estado() / "pendencias.csv", COLS_PENDENCIAS)
    print(f"OK pendência {nova['id']}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("pendencia", help="acrescenta pendência")
    q.add_argument("--origem", default="humano", choices=["Form", "Melhorias", "NOTAS", "validacao", "IA", "humano"])
    q.add_argument("--descricao", required=True)
    q.add_argument("--celulas", default="")
    q.add_argument("--grupos", default="")
    q.add_argument("--autor")
    i = sub.add_parser("iniciar")
    i.add_argument("--xlsx", required=True)
    i.add_argument("--melhorias")
    i.add_argument("--notas")
    i.add_argument("--ref")
    i.add_argument("--autor")
    i.add_argument("--forcar", action="store_true")
    a = p.parse_args()
    {"iniciar": iniciar, "pendencia": pendencia}[a.cmd](a)


if __name__ == "__main__":
    main()
