"""Detector de célula fora do lugar ("outlier pontual") entre edições.

Uso:
  python hp_outliers.py [--min-outros 2] [--saida arq.csv]

Para cada célula (Ano:Codigo) no grupo Y, olha os mesmos produtos (descrição normalizada idêntica)
nas OUTRAS edições. A célula é candidata a MOVER para X quando:
  1. todo item da célula que aparece em outra edição está, em todas elas, num único grupo X ≠ Y
     (unanimidade item a item e entre itens);
  2. nenhum item da célula aparece em Y em outra edição;
  3. pelo menos metade dos itens da célula tem histórico (célula de 1987 com 40 itens e 1 casado não passa);
  4. a célula não foi tocada por decisão anterior (R7) nem citada em regra (exceções R1 etc.).
A força da evidência é o número de outras edições que concordam (n_outros). Isto é diagnóstico para
a IA: a decisão continua sendo proposta, com motivo, na onda (CONSTITUICAO.md, R6/R8).

Colunas: cel, ano, codigo, quadro, de, para, n_itens, n_hist, n_outros, anos_x, itens, ibge (grupo>linha
do tradutor oficial, 2008/2017), ibge_concorda (destino compatível com o grande grupo do IBGE e origem não).
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

import hp_ibge
from hp_comum import carrega_decisoes_todas, carrega_estado, celulas_df, norm_texto, separa


# quadros de conceito próprio: o mesmo nome de produto ali é outra despesa (comer fora, gasto em viagem)
CONCEITO_QUADRO = {("1987", "22"): "fora", ("1995", "24"): "fora", ("2002", "24"): "fora", ("2008", "24"): "fora",
                   ("2017", "24"): "fora", ("1987", "46"): "viagem", ("1995", "41"): "viagem",
                   ("2002", "41"): "viagem", ("2008", "41"): "viagem", ("2017", "41"): "viagem"}


def conceito(ano: str, quadro: str) -> str:
    return CONCEITO_QUADRO.get((ano, quadro), "outro")


def detecta(est: dict, min_outros: int = 2) -> pd.DataFrame:
    dep, grp = est["depara"], est["grupos"]
    ativos = set(grp.loc[grp["status"] == "ativo", "Cod_harmo"])
    n1 = dict(zip(grp["Cod_harmo"], grp["nivel1"]))
    d = dep.copy()
    d["k"] = d["Descri_Item"].map(norm_texto)
    d["cel"] = d["Ano"] + ":" + d["Codigo"]
    d["conc"] = [conceito(a, q) for a, q in zip(d["Ano"], d["Quadro_H"])]
    # onde cada descrição está em cada ano, por conceito de quadro: (k, conceito) -> ano -> {grupos}
    onde = defaultdict(lambda: defaultdict(set))
    for k, ano, g, cc in zip(d["k"], d["Ano"], d["Cod_harmo"], d["conc"]):
        if k:
            onde[(k, cc)][ano].add(g)
    # células já decididas ou citadas em regra ficam de fora (R7)
    trav = set()
    dec = carrega_decisoes_todas()
    for c in dec.get("celulas", pd.Series(dtype=str)):
        trav.update(separa(c))
    for c in est["regras"].get("celulas", pd.Series(dtype=str)):
        trav.update(x.split("#")[0] for x in separa(c))

    out = []
    for cel, sub in d.groupby("cel", sort=False):
        if cel in trav:
            continue
        ano = sub["Ano"].iloc[0]
        y = sub["Cod_harmo"].iloc[0]
        cc = sub["conc"].iloc[0]
        destinos, n_hist, confirma_y, outros_anos = set(), 0, False, set()
        ok = True
        for k in sub["k"].unique():
            hist = {a: gs for a, gs in onde[(k, cc)].items() if a != ano}
            if not hist:
                continue
            n_hist += 1
            gs = set().union(*hist.values())
            if y in gs:
                confirma_y = True
                break
            if len(gs) != 1:
                ok = False
                break
            destinos |= gs
            outros_anos |= set(hist)
        n_itens = sub["k"].nunique()
        if confirma_y or not ok or len(destinos) != 1 or n_hist * 2 < n_itens:
            continue
        x = next(iter(destinos))
        if x not in ativos or len(outros_anos) < min_outros:
            continue
        out.append({"cel": cel, "ano": ano, "codigo": sub["Codigo"].iloc[0], "quadro": sub["Quadro_H"].iloc[0],
                    "de": y, "para": x, "n1_de": n1.get(y, ""), "n1_para": n1.get(x, ""),
                    "conceito": cc, "n_itens": n_itens, "n_hist": n_hist, "n_outros": len(outros_anos),
                    "anos_x": ";".join(sorted(outros_anos)),
                    "itens": " | ".join(sub["Descri_Item"].unique()[:15])})
    o = pd.DataFrame(out)
    if o.empty:
        return o
    # evidência do IBGE (2008/2017): grande grupo e, fora de alimentos, a linha fina típica de cada grupo
    cel = celulas_df(dep)
    todas = hp_ibge.anota(cel[cel["Ano"].isin(["2008", "2017"])])
    com = todas[(todas["descricao_ibge"] != "") & (todas["grupo_ibge"].map(hp_ibge.norm_grupo_ibge) != "alimentacao")]
    tipica = com.groupby(["Ano", "grupos"])["descricao_ibge"].agg(lambda s: s.value_counts().index[0]).to_dict()
    an = todas.set_index("cel")
    o["ibge"] = o["cel"].map(lambda c: f"{an.loc[c, 'grupo_ibge']} > {an.loc[c, 'descricao_ibge']}"
                             if c in an.index and an.loc[c, "grupo_ibge"] else "")

    def concorda(r):
        if r["cel"] not in an.index or not an.loc[r["cel"], "grupo_ibge"]:
            return ""
        ib = hp_ibge.norm_grupo_ibge(an.loc[r["cel"], "grupo_ibge"])
        ep = hp_ibge.grupo_repo_para_ibge(r["n1_para"]).split("|")
        ed = hp_ibge.grupo_repo_para_ibge(r["n1_de"]).split("|")
        if ib in ep and ib not in ed:
            return "sim"
        if ib in ed and ib not in ep:
            return "nao"
        # mesmo grande grupo: decide pela linha fina típica do grupo de origem e do de destino
        lin = an.loc[r["cel"], "descricao_ibge"]
        if ib != "alimentacao" and lin:
            if lin == tipica.get((r["ano"], r["de"])) and lin != tipica.get((r["ano"], r["para"])):
                return "nao"
            if lin == tipica.get((r["ano"], r["para"])) and lin != tipica.get((r["ano"], r["de"])):
                return "sim"
        return "neutro"
    o["ibge_concorda"] = o.apply(concorda, axis=1)
    # domínio: consumo (1-40), outras despesas (41-43), rendimentos (44-47), inventário (88). Mudar de domínio
    # é mudar de conceito (mesmo nome, outra despesa): só com o IBGE confirmando.
    def dominio(n1):
        m = re.match(r"\s*(\d+)", n1 or "")
        n = int(m.group(1)) if m else -1
        return "consumo" if 1 <= n <= 40 else "outras" if 41 <= n <= 43 else "rend" if 44 <= n <= 47 else "inv" if n == 88 else "?"
    o["muda_dominio"] = [dominio(a) != dominio(b) for a, b in zip(o["n1_de"], o["n1_para"])]
    return o.sort_values(["n1_para", "para", "ano", "codigo"]).reset_index(drop=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-outros", type=int, default=2)
    ap.add_argument("--saida")
    a = ap.parse_args()
    o = detecta(carrega_estado(), a.min_outros)
    if a.saida:
        o.to_csv(a.saida, index=False, encoding="utf-8", lineterminator="\n")
    print(f"{len(o)} células candidatas (min_outros={a.min_outros})")
    if len(o):
        print(o.groupby(["n_outros", "ibge_concorda"]).size().to_string())
        print(o.groupby("ano").size().to_string())


if __name__ == "__main__":
    sys.exit(main())
