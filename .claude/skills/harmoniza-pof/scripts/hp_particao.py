"""Partição mínima compatível com a R1 (ADR 0003): componentes conexos entre conceitos que dividem célula.

Uso:
  python hp_particao.py --regras ondas/ONDA/conceitos_regras.csv [--quadros 42] [--grupos 36005,36006]
                        [--simular "2002:42015#implante_cabelo;2002:42008"] [--onda ONDA | --saida arq.md]

`conceitos_regras.csv` (escrito pela IA, versionado na onda): colunas `padrao,conceito,nota`. `padrao` é regex
aplicada ao texto normalizado do item (minúsculo, sem acento, pontuação vira espaço); a primeira que casa vence.
Item sem regra vira conceito `?<texto>` e aparece listado para completar as regras.

Lógica: cada célula liga todos os conceitos dos seus itens (R1). Componentes conexos = menores grupos
harmonizáveis. Componente com células em mais de um grupo atual = violação da R1: ou a célula está fora do grupo
majoritário (MOVER) ou há ligações entre conceitos que exigem UNIR ou exceção.
Exceções (`excecao_r1` ativas em estado/regras.csv, mais `--simular`):
  `ANO:COD`          a célula inteira não liga conceitos (fica no componente do conceito dominante);
  `ANO:COD#conceito` só aquele conceito não propaga dentro da célula (item estranho = contaminação).
"""
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import pandas as pd

from hp_comum import (ANOS, carrega_estado, cod5, dir_ondas, grava_csv, grava_texto, le_csv, nome_grupo,
                      norm_texto, separa)


class UniaoBusca:
    def __init__(self):
        self.pai: dict[str, str] = {}

    def raiz(self, x: str) -> str:
        self.pai.setdefault(x, x)
        while self.pai[x] != x:
            self.pai[x] = self.pai[self.pai[x]]
            x = self.pai[x]
        return x

    def une(self, a: str, b: str) -> None:
        ra, rb = self.raiz(a), self.raiz(b)
        if ra != rb:
            self.pai[rb] = ra


def carrega_regras(path: Path) -> list[tuple[re.Pattern, str]]:
    r = le_csv(path, ["padrao", "conceito", "nota"])
    return [(re.compile(x.padrao), x.conceito) for x in r.itertuples() if x.padrao.strip()]


def conceito_de(desc: str, regras) -> str:
    t = norm_texto(desc)
    for rx, c in regras:
        if rx.search(t):
            return c
    return "?" + t[:50]


def ligantes(cel: str, cs: list[str], exc_cel: set[str], exc_item: set[tuple[str, str]]) -> list[str]:
    """Conceitos que propagam a R1 nesta célula."""
    if cel in exc_cel:
        return []
    return [c for c in dict.fromkeys(cs) if (cel, c) not in exc_item]


def dominante(cel: str, cs: list[str], exc_item: set[tuple[str, str]]) -> str:
    validos = [c for c in cs if (cel, c) not in exc_item] or cs
    return Counter(validos).most_common(1)[0][0]


def liga(cels: dict[str, list[str]], exc_cel, exc_item) -> UniaoBusca:
    uf = UniaoBusca()
    for c, cs in cels.items():
        for x in cs:
            uf.raiz(x)
        lig = ligantes(c, cs, exc_cel, exc_item)
        for x in lig[1:]:
            uf.une(lig[0], x)
    return uf


def parse_excecoes(textos: list[str]) -> tuple[set[str], set[tuple[str, str]]]:
    exc_cel, exc_item = set(), set()
    for t in textos:
        for e in separa(t):
            cel, _, conc = e.partition("#")
            (exc_item.add((cel.strip(), conc.strip())) if conc else exc_cel.add(cel.strip()))
    return exc_cel, exc_item


def md_tab(cols, rows) -> str:
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(str(x).replace("|", "/") for x in r) + " |" for r in rows]
    return "\n".join(out)


def calcula(est: dict, regras, quadros: list[str], grupos: list[str], simular: str = "") -> tuple[str, pd.DataFrame]:
    dep = est["depara"]
    m = pd.Series(True, index=dep.index)
    if quadros:
        m &= dep["Quadro_H"].str.lstrip("0").isin([q.lstrip("0") for q in quadros])
    if grupos:
        m &= dep["Cod_harmo"].isin(grupos)
    sub = dep[m].copy()
    sub["cel"] = sub["Ano"] + ":" + sub["Codigo"]
    sub["conceito"] = sub["Descri_Item"].map(lambda d: conceito_de(d, regras))
    reg = est["regras"]
    registradas = list(reg[(reg["tipo"] == "excecao_r1") & (reg["status"] == "ativa")]["celulas"])
    exc_cel, exc_item = parse_excecoes(registradas + [simular])
    nomes = nome_grupo(est["grupos"])

    cels = sub.groupby("cel")["conceito"].apply(list).to_dict()
    grupo = sub.groupby("cel")["Cod_harmo"].first().to_dict()
    itens_txt = sub.groupby("cel")["Descri_Item"].apply(lambda s: " / ".join(dict.fromkeys(s))).to_dict()
    uf = liga(cels, exc_cel, exc_item)
    comp_de = {c: uf.raiz(dominante(c, cs, exc_item)) for c, cs in cels.items()}
    comps: dict[str, list[str]] = defaultdict(list)
    for c, r in comp_de.items():
        comps[r].append(c)
    ordem = sorted(comps, key=lambda r: (-len(comps[r]), r))
    rotulo = {r: f"C{i + 1:02d}" for i, r in enumerate(ordem)}
    sub["componente"] = sub["cel"].map(lambda c: rotulo[comp_de[c]])

    def conceitos_txt(cs, n=6):
        return ", ".join(f"{k} ({v})" for k, v in Counter(cs).most_common(n))

    n_exc = len(exc_cel & set(cels)) + len({c for c, _ in exc_item} & set(cels))
    out = [f"# Partição R1 — quadros {quadros or 'todos'} · grupos {grupos or 'todos'}",
           f"{len(cels)} células · {sub['conceito'].nunique()} conceitos · {len(comps)} componentes · "
           f"{n_exc} células com exceção" + (f" (simuladas: `{simular}`)" if simular else "")]

    sem = sorted({c for c in sub["conceito"] if c.startswith("?")})
    if sem:
        out += [f"## Itens sem regra de conceito ({len(sem)}) — completar `conceitos_regras.csv`",
                "\n".join(f"- `{c[1:]}`" for c in sem[:200])]

    viol = [r for r in ordem if len({grupo[c] for c in comps[r]}) > 1]
    rows = []
    for r in ordem:
        cs_ = comps[r]
        anos = Counter(c.split(":")[0] for c in cs_)
        gs = Counter(grupo[c] for c in cs_)
        rows.append([rotulo[r], len(cs_), " ".join(str(anos.get(a, 0)) for a in ANOS),
                     ", ".join(f"{g} {nomes.get(g, '?')[:18]} ({n})" for g, n in gs.most_common()),
                     conceitos_txt([x for c in cs_ for x in cels[c]], 4), "**VIOLA R1**" if r in viol else ""])
    out += ["## Componentes (menores grupos compatíveis com a R1)",
            md_tab(["comp", "células", " ".join(ANOS), "grupos atuais", "conceitos (itens)", ""], rows)]

    for r in viol:
        cs_ = sorted(comps[r], key=lambda c: (c.split(":")[0], c))
        gs = Counter(grupo[c] for c in cs_)
        maior = gs.most_common(1)[0][0]
        out.append(f"\n## {rotulo[r]}: células em {len(gs)} grupos (majoritário {maior} {nomes.get(maior, '?')})")

        arestas: dict[tuple[str, str], list[str]] = defaultdict(list)
        for c in cs_:
            for a_, b_ in combinations(sorted(ligantes(c, cels[c], exc_cel, exc_item)), 2):
                arestas[(a_, b_)].append(c)
        if arestas:
            grupos_conc: dict[str, Counter] = defaultdict(Counter)
            for c in cs_:
                grupos_conc[dominante(c, cels[c], exc_item)][grupo[c]] += 1
            arow = [[f"{a_} — {b_}", ", ".join(v), ", ".join(sorted(grupos_conc[a_])) or "—",
                     ", ".join(sorted(grupos_conc[b_])) or "—"] for (a_, b_), v in sorted(arestas.items())]
            out += ["Ligações entre conceitos (quem cria cada ligação):",
                    md_tab(["conceitos ligados", "células", "grupos onde o 1º domina", "grupos onde o 2º domina"], arow)]

        fora = [[c, grupo[c], nomes.get(grupo[c], '?')[:25], conceitos_txt(cels[c], 3), itens_txt[c][:110]]
                for c in cs_ if grupo[c] != maior]
        out += [f"Células fora do grupo majoritário ({len(fora)}):",
                md_tab(["célula", "grupo", "nome", "conceitos", "itens"], fora)]

        pontes = []
        sub_cels = {c: cels[c] for c in cs_}
        for c in cs_:
            lig = ligantes(c, cels[c], exc_cel, exc_item)
            if len(lig) < 2:
                continue
            uf2 = liga(sub_cels, exc_cel | {c}, exc_item)
            partes: dict[str, set] = defaultdict(set)
            for k in cs_:
                partes[uf2.raiz(dominante(k, cels[k], exc_item))].add(grupo[k])
            if len(partes) > 1:
                pontes.append((max(len(v) for v in partes.values()), c, partes))
        if pontes:
            prow = [[c, grupo[c], len(p), " ⟂ ".join("{" + ",".join(sorted(v)) + "}" for v in p.values())]
                    for _, c, p in sorted(pontes, key=lambda x: x[0])]
            out += ["Células-ponte (excetuar a célula inteira divide o componente):",
                    md_tab(["célula", "grupo", "partes", "grupos por parte"], prow)]

    split = []
    for g, cs_g in pd.Series(grupo).groupby(pd.Series(grupo)):
        rs = Counter(rotulo[comp_de[c]] for c in cs_g.index)
        if len(rs) > 1:
            split.append([g, nomes.get(g, "?")[:30], ", ".join(f"{k} ({v})" for k, v in rs.most_common())])
    out += ["## Grupos atuais com mais de um componente (divisão possível se R3 permitir)",
            md_tab(["grupo", "nome", "componentes (células)"], split) if split else "_nenhum_"]
    return "\n\n".join(out) + "\n", sub[["Ano", "Codigo", "Descri_Item", "Cod_harmo", "conceito", "componente"]]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--regras", required=True)
    p.add_argument("--quadros", default="")
    p.add_argument("--grupos", default="")
    p.add_argument("--simular", default="", help="exceções hipotéticas: 'ANO:COD' ou 'ANO:COD#conceito', separadas por ;")
    p.add_argument("--onda")
    p.add_argument("--saida")
    a = p.parse_args()
    quadros = [q.strip() for q in a.quadros.split(",") if q.strip()]
    grupos = [cod5(g) for g in a.grupos.split(",") if g.strip()]
    txt, tab = calcula(carrega_estado(), carrega_regras(Path(a.regras)), quadros, grupos, a.simular)
    if a.onda:
        od = dir_ondas() / a.onda
        nome = "particao_simulada.md" if a.simular else "particao.md"
        grava_texto(txt, od / nome)
        if not a.simular:
            grava_csv(tab, od / "conceitos.csv")
        print(f"gravado {od / nome}")
    elif a.saida:
        grava_texto(txt, Path(a.saida))
        print(f"gravado {a.saida}")
    else:
        print(txt)


if __name__ == "__main__":
    main()
