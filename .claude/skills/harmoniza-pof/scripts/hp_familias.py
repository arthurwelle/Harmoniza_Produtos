"""Monta o pacote de contexto de uma família para a IA analisar (R6).

Uso:
  python hp_familias.py --grupos 36005,36006 [--celulas 2017:42026] [--vizinhos 3]
                        [--similares 10] [--max-itens 12] [--onda ID | --saida arq.md]

Conteúdo: grupos-alvo (nome, níveis, cobertura), grupos irmãos (mesmo nível 2), células dos 5 anos
com itens, vizinhos de código no mesmo quadro, itens parecidos classificados em OUTROS grupos,
regras/decisões/pendências que tocam o escopo, linhas das fontes externas que citam os códigos.
"""
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

from hp_comum import (ANOS, carrega_decisoes_todas, carrega_estado, celulas_df, cod5, dir_h,
                      dir_ondas, grava_texto, le_csv, matriz_cobertura, norm_texto, padrao,
                      separa, txt_movimentos)

STOP = {"de", "da", "do", "das", "dos", "com", "sem", "para", "em", "e", "ou", "a", "o", "tipo",
        "outros", "outras", "nao", "especificado", "especificada", "etc", "kg", "por", "na", "no"}


def tokens(s: str) -> set[str]:
    return {t for t in norm_texto(s).split() if len(t) >= 3 and t not in STOP and not t.isdigit()}


def corta(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


def md_tab(cols, rows) -> str:
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)


def expande_faixas(txt: str) -> set[str]:
    """'6301:6303, 6333' -> {'6301','6302','6303','6333'}."""
    out = set()
    for a, b in re.findall(r"(\d{3,7})\s*:\s*(\d{3,7})", txt):
        if int(b) - int(a) < 2000:
            out.update(str(i) for i in range(int(a), int(b) + 1))
    out.update(re.findall(r"\b\d{3,7}\b", txt))
    return out


def evidencia_fontes(cods_por_ano: dict[str, set[str]], max_linhas: int = 12) -> list[str]:
    fonte = dir_h() / "fonte"
    todos = set().union(*cods_por_ano.values()) if cods_por_ano else set()
    todos = {c for c in todos if len(c) >= 4}
    out = []
    for p in sorted(fonte.glob("*.csv")):
        m = re.search(r"zoom(\d{4})", p.name)
        ano_zoom = m.group(1) if m else None
        alvo = cods_por_ano.get(ano_zoom, set()) if ano_zoom else todos
        if not alvo:
            continue
        df = le_csv(p)
        achadas = []
        for row in df.itertuples(index=False):
            vals = [v for v in row if v]
            if ano_zoom:
                hit = any(alvo & expande_faixas(v) for v in vals if re.search(r"\d", v))
            else:
                hit = any(v in alvo for v in vals)
            if hit:
                achadas.append(corta(" · ".join(vals), 220))
                if len(achadas) >= max_linhas:
                    break
        if achadas:
            aviso = "" if ano_zoom else " (código casado por valor exato; conferir o ano)"
            out.append(f"**{p.name}**{aviso}\n" + "\n".join(f"- {a}" for a in achadas))
    return out


def contexto(est: dict, grupos: list[str], celulas_extra: list[str], k: int, n_sim: int,
             max_itens: int) -> str:
    dep, grp = est["depara"], est["grupos"]
    cel = celulas_df(dep)
    nomes = dict(zip(grp["Cod_harmo"], grp["nome"]))
    alvo = cel[cel["grupos"].isin(grupos) | cel["cel"].isin(celulas_extra)].copy()
    grupos_all = sorted(set(grupos) | set(alvo["grupos"]))
    out = [f"# Contexto da família: {', '.join(grupos_all)}"]

    # grupos-alvo + irmãos
    m = matriz_cobertura(dep, grp)
    g_info = grp.set_index("Cod_harmo")
    rows = []
    for g in grupos_all:
        r = g_info.loc[g] if g in g_info.index else None
        cov = m.loc[g] if g in m.index else pd.Series({a: 0 for a in ANOS})
        rows.append([g, corta(nomes.get(g, "?"), 70), r["nivel1"] if r is not None else "",
                     r["nivel2"] if r is not None else "", *[cov[a] for a in ANOS], padrao(cov),
                     r["status"] if r is not None else "?"])
    out += ["## Grupos no escopo (células por ano)",
            md_tab(["Cod", "nome", "nível1", "nível2", *ANOS, "padrão", "status"], rows)]

    n2 = set(g_info.loc[[g for g in grupos_all if g in g_info.index], "nivel2"]) - {""}
    irm = grp[grp["nivel2"].isin(n2) & ~grp["Cod_harmo"].isin(grupos_all)]
    if len(irm):
        rows = [[g, corta(nomes.get(g, ""), 70), *[m.loc[g, a] if g in m.index else 0 for a in ANOS]]
                for g in irm["Cod_harmo"]]
        out += ["## Grupos irmãos (mesmo nível 2)", md_tab(["Cod", "nome", *ANOS], rows)]

    # células por ano
    out.append("## Células do escopo, por ano")
    for ano in ANOS:
        sub = alvo[alvo["Ano"] == ano]
        if sub.empty:
            out.append(f"### {ano}\n_nenhuma célula_")
            continue
        rows = []
        for r in sub.itertuples():
            its = r.itens.split(" | ")
            txt = " | ".join(its[:max_itens]) + (f" … (+{len(its) - max_itens})" if len(its) > max_itens else "")
            rows.append([r.Codigo, r.Quadro_H, r.grupos, r.n_itens, txt])
        out.append(f"### {ano} ({len(sub)} células)\n" + md_tab(["Codigo", "Quadro", "grupo", "n", "itens"], rows))

    # vizinhos de código
    viz_rows = []
    alvo_cels = set(alvo["cel"])
    for (ano, quadro), bloco in cel.groupby(["Ano", "Quadro_H"], sort=False):
        if not alvo_cels & set(bloco["cel"]):
            continue
        bloco = bloco.assign(_k=bloco["Codigo"].map(lambda s: int(s) if s.isdigit() else 0)).sort_values("_k")
        idx = [i for i, c in enumerate(bloco["cel"]) if c in alvo_cels]
        pegar = sorted({j for i in idx for j in range(max(0, i - k), min(len(bloco), i + k + 1))} - set(idx))
        for j in pegar:
            r = bloco.iloc[j]
            viz_rows.append([ano, quadro, r["Codigo"], r["grupos"], corta(nomes.get(r["grupos"], ""), 40),
                             corta(r["itens"], 120)])
    if viz_rows:
        out += [f"## Vizinhos de código (±{k} no mesmo quadro) fora do escopo",
                md_tab(["Ano", "Quadro", "Codigo", "grupo", "nome", "itens"], viz_rows)]

    # itens parecidos em outros grupos (índice invertido de tokens)
    fora = dep[~dep["Cod_harmo"].isin(grupos_all)]
    df_tok = Counter(t for s in dep["Descri_Item"].unique() for t in tokens(s))
    idx_inv = defaultdict(set)
    fora_u = fora.drop_duplicates(["Ano", "Codigo", "Descri_Item"])
    for i, s in enumerate(fora_u["Descri_Item"]):
        for t in tokens(s):
            if df_tok[t] <= 400:
                idx_inv[t].add(i)
    alvo_tok = Counter(t for s in dep.loc[dep["Cod_harmo"].isin(grupos_all) | (dep["Ano"] + ":" + dep["Codigo"]).isin(celulas_extra),
                                           "Descri_Item"].unique() for t in tokens(s))
    marcas = [t for t, _ in alvo_tok.most_common(40) if t in idx_inv]
    score = Counter()
    for t in marcas:
        for i in idx_inv[t]:
            score[i] += 1 / (1 + df_tok[t] ** 0.5)
    sim_rows = []
    por_grupo = Counter()
    for i, _ in score.most_common(300):
        r = fora_u.iloc[i]
        por_grupo[r["Cod_harmo"]] += 1
        if len(sim_rows) < n_sim * 3:
            sim_rows.append([r["Ano"], r["Codigo"], corta(r["Descri_Item"], 60), r["Cod_harmo"],
                             corta(nomes.get(r["Cod_harmo"], ""), 40)])
    if sim_rows:
        out += ["## Itens com vocabulário parecido classificados em OUTROS grupos",
                "Grupos mais frequentes: " + ", ".join(f"{g} {corta(nomes.get(g, ''), 30)} ({n})"
                                                       for g, n in por_grupo.most_common(n_sim)),
                md_tab(["Ano", "Codigo", "item", "grupo", "nome"], sim_rows)]

    # regras, decisões, pendências
    reg = est["regras"]
    toca = lambda cels, gs: bool(set(separa(cels)) & alvo_cels or set(map(cod5, separa(gs))) & set(grupos_all))
    r_rows = [[r.id, r.tipo, r.status, corta(r.enunciado, 120)] for r in reg.itertuples() if toca(r.celulas, r.grupos)]
    out += ["## Regras que tocam o escopo", md_tab(["id", "tipo", "status", "enunciado"], r_rows) if r_rows else "_nenhuma_"]

    dec = carrega_decisoes_todas()
    d_rows = []
    for r in dec.itertuples():
        movs = txt_movimentos(r.movimentos)
        cels = {c for mv in movs for c in mv["celulas"]} | set(separa(r.celulas))
        paras = {mv["para"] for mv in movs} | set(separa(r.de))
        if cels & alvo_cels or paras & set(grupos_all):
            d_rows.append([r.id, r.tipo, r.veredito, corta(r.motivo_ia, 90), corta(r.motivo_humano, 90)])
    out += ["## Decisões anteriores que tocam o escopo (R7: são restrições)",
            md_tab(["id", "tipo", "veredito", "motivo IA", "motivo humano"], d_rows) if d_rows else "_nenhuma_"]

    pen = est["pendencias"]
    p_rows = [[r.id, r.origem, r.status, corta(r.descricao, 160)] for r in pen.itertuples()
              if toca(r.celulas, r.grupos)]
    out += ["## Pendências que tocam o escopo", md_tab(["id", "origem", "status", "descrição"], p_rows) if p_rows else "_nenhuma_"]

    cods_ano = {a: set(alvo.loc[alvo["Ano"] == a, "Codigo"]) for a in ANOS}
    ev = evidencia_fontes(cods_ano)
    out += ["## Fontes externas que citam os códigos do escopo", "\n\n".join(ev) if ev else "_nada encontrado_"]
    return "\n\n".join(out) + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--grupos", default="")
    p.add_argument("--celulas", default="")
    p.add_argument("--vizinhos", type=int, default=3)
    p.add_argument("--similares", type=int, default=10)
    p.add_argument("--max-itens", type=int, default=12)
    p.add_argument("--onda")
    p.add_argument("--saida")
    a = p.parse_args()
    grupos = [cod5(g) for g in a.grupos.replace(";", ",").split(",") if g.strip()]
    cels = [c.strip() for c in a.celulas.replace(",", ";").split(";") if c.strip()]
    if not grupos and not cels:
        p.error("informe --grupos e/ou --celulas")
    txt = contexto(carrega_estado(), grupos, cels, a.vizinhos, a.similares, a.max_itens)
    destino = dir_ondas() / a.onda / "contexto.md" if a.onda else (Path(a.saida) if a.saida else None)
    if destino:
        grava_texto(txt, destino)
        print(f"gravado {destino} ({len(txt)} caracteres)")
    else:
        print(txt)


if __name__ == "__main__":
    main()
