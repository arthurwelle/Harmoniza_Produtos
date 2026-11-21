"""Matriz de cobertura grupo x ano.

Uso:
  python hp_cobertura.py [--grupos 36005,36006] [--medida celulas|itens] [--top 15] [--saida arq.md]

Mostra: células/itens por ano, distribuição de nº de anos presentes, padrões de ausência,
grupos com ausência (marcando se justificada por regra `ausencia_estrutural`) e maiores baldes.
"""
from __future__ import annotations

import argparse

import pandas as pd

from hp_comum import (ANOS, ausencias_justificadas, carrega_estado, cod5, grava_texto,
                      matriz_cobertura, nome_grupo, padrao)


def tabela_md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    linhas = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        linhas.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(linhas)


def ausencias(est: dict) -> pd.DataFrame:
    """Uma linha por grupo ativo com algum ano vazio."""
    m = matriz_cobertura(est["depara"], est["grupos"])
    ok = ausencias_justificadas(est["regras"])
    nomes = nome_grupo(est["grupos"])
    rows = []
    for g, r in m.iterrows():
        vazios = [a for a in ANOS if r[a] == 0]
        if not vazios:
            continue
        nao_just = [a for a in vazios if (g, a) not in ok]
        rows.append({"Cod_harmo": g, "nome": nomes.get(g, "?")[:60], **{a: r[a] for a in ANOS},
                     "padrao": padrao(r), "vazios_nao_justificados": ";".join(nao_just)})
    return pd.DataFrame(rows)


def relatorio(est: dict, grupos: list[str] | None = None, medida: str = "celulas",
              top: int = 15) -> str:
    dep = est["depara"]
    if grupos:
        dep = dep[dep["Cod_harmo"].isin(grupos)]
    m = matriz_cobertura(dep, None if grupos else est["grupos"], medida)
    nomes = nome_grupo(est["grupos"])
    out = []

    if grupos:
        t = m.reset_index()
        t.insert(1, "nome", t["Cod_harmo"].map(lambda g: nomes.get(g, "?")[:60]))
        t["padrao"] = m.apply(padrao, axis=1).values
        out += [f"## Cobertura ({medida}) dos grupos selecionados", tabela_md(t)]
        return "\n\n".join(out) + "\n"

    celulas = dep.drop_duplicates(["Ano", "Codigo"]).groupby("Ano").size()
    itens = dep.groupby("Ano").size()
    presentes = (m > 0).sum()
    resumo = pd.DataFrame({"Ano": ANOS, "celulas": [celulas.get(a, 0) for a in ANOS],
                           "itens": [itens.get(a, 0) for a in ANOS],
                           "grupos_presentes": [presentes.get(a, 0) for a in ANOS]})
    out += ["# Cobertura", f"Grupos ativos: {len(m)}", tabela_md(resumo)]

    n_anos = (m > 0).sum(axis=1).value_counts().sort_index()
    out += ["## Nº de anos em que o grupo aparece",
            tabela_md(pd.DataFrame({"n_anos": n_anos.index, "grupos": n_anos.values}))]

    pad = m.apply(padrao, axis=1).value_counts()
    out += [f"## Padrões de presença ({' '.join(ANOS)})",
            tabela_md(pd.DataFrame({"padrao": pad.index, "grupos": pad.values}))]

    au = ausencias(est)
    nj = au[au["vazios_nao_justificados"] != ""] if len(au) else au
    out += [f"## Grupos com ano vazio: {len(au)} ({len(nj)} com vazio não justificado por regra)",
            tabela_md(au) if len(au) else "_nenhum_"]

    big = matriz_cobertura(est["depara"], None, "itens")
    big["total"] = big.sum(axis=1)
    big = big.sort_values("total", ascending=False).head(top).reset_index()
    big.insert(1, "nome", big["Cod_harmo"].map(lambda g: nomes.get(g, "?")[:50]))
    out += [f"## Maiores baldes (itens) — top {top}", tabela_md(big)]
    return "\n\n".join(out) + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--grupos", help="lista separada por vírgula")
    p.add_argument("--medida", choices=["celulas", "itens"], default="celulas")
    p.add_argument("--top", type=int, default=15)
    p.add_argument("--saida")
    a = p.parse_args()
    est = carrega_estado()
    grupos = [cod5(g) for g in a.grupos.split(",")] if a.grupos else None
    txt = relatorio(est, grupos, a.medida, a.top)
    if a.saida:
        from pathlib import Path
        grava_texto(txt, Path(a.saida))
        print(f"gravado {a.saida}")
    else:
        print(txt)


if __name__ == "__main__":
    main()
