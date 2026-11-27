"""Passo 3: avalia o de-para 2024 proposto comparando 2017 x 2024 por grupo harmonizado.

Compara PARTICIPAÇÕES (% da despesa total de cada ano), não níveis: 2017 está a preços de
jan/2018 e 2024 a preços da POF 2024-2025.

Dois cenários:
  estrito        só as células ATRIBUIR (ALTA/MÉDIA)
  com_sugestoes  de-para final (saida/decisoes_2024.csv, passo 4) quando existir; senão, sugestões do passo 2

Saídas em saida/:
  comparacao_grupos_despesa.csv   grupo x ano, com sinalizações
  comparacao_grupos_renda.csv     idem para rendas
  comparacao_nivel1.csv           agregado no nível 1 da harmonização

Rodar da pasta POF2024/harmonizacao:  python scripts/03_avalia.py
"""
import pathlib

import numpy as np
import pandas as pd

H = pathlib.Path(__file__).resolve().parents[1]
FONTE, SAIDA = H / "fonte", H / "saida"

p = pd.read_csv(SAIDA / "propostas_2024.csv", dtype={"Cod_harmo": str, "Cod_harmo_sugerido": str, "Codigo": str})
c24 = pd.read_csv(FONTE / "celulas_2024.csv", dtype={"Codigo": str})[["Codigo", "valor_despesa_uc", "valor_renda_uc"]]
p = p.merge(c24, on="Codigo", how="left")
c17 = pd.read_csv(FONTE / "celulas_2017.csv")
c17["Cod_harmo"] = c17.Cod_harmo.astype(str).str.zfill(5)
g = pd.read_csv(H / "base/grupos.csv", dtype=str).set_index("Cod_harmo")[["nome", "nivel1", "nivel2"]]


def tabela(col17, col24):
    t17 = c17.groupby("Cod_harmo").agg(valor17=(col17, "sum"), celulas17=("Codigo", "size"))
    est = p[p.tipo == "ATRIBUIR"].groupby("Cod_harmo").agg(valor24=(col24, "sum"), celulas24=("Codigo", "size"))
    fin = SAIDA / "decisoes_2024.csv"
    base_sug = (pd.read_csv(fin, dtype={"Codigo": str, "para": str})[["Codigo", "para"]]
                  .merge(p[["Codigo", col24]], on="Codigo").rename(columns={"para": "Cod_harmo_sugerido"})
                if fin.exists() else p[p.Cod_harmo_sugerido.notna()])
    sug = base_sug.groupby("Cod_harmo_sugerido").agg(
        valor24_sug=(col24, "sum"), celulas24_sug=("Codigo", "size"))
    t = t17.join(est, how="outer").join(sug, how="outer").fillna(0)
    t = t[(t.valor17 > 0) | (t.valor24_sug > 0)]
    tot17 = c17[col17].sum()
    tot24 = p[col24].sum()  # total do ano, inclusive o que ficou sem grupo
    t["pct17"] = 100 * t.valor17 / tot17
    t["pct24"] = 100 * t.valor24 / tot24
    t["pct24_sug"] = 100 * t.valor24_sug / tot24
    t["razao_sug"] = np.where(t.pct17 > 0, t.pct24_sug / t.pct17, np.nan)
    sinal = []
    for _, r in t.iterrows():
        s = []
        if r.pct17 >= 0.01 and r.valor24_sug == 0:
            s.append("VAZIO_2024 (R4)")
        if r.valor17 == 0 and r.valor24_sug > 0:
            s.append("SO_2024")
        if max(r.pct17, r.pct24_sug) >= 0.10 and r.pct17 > 0 and (r.razao_sug > 2 or r.razao_sug < 0.5):
            s.append("SALTO")
        if r.valor24_sug > r.valor24 * 1.2 and r.valor24_sug - r.valor24 > 0.002 * tot24:
            s.append("DEPENDE_DE_REVISAR")
        sinal.append("; ".join(s))
    t["sinal"] = sinal
    t = t.join(g, how="left")
    cols = ["nome", "nivel1", "nivel2", "celulas17", "celulas24", "celulas24_sug",
            "pct17", "pct24", "pct24_sug", "razao_sug", "sinal"]
    t = t[cols].sort_values("pct17", ascending=False)
    for c in ["pct17", "pct24", "pct24_sug"]:
        t[c] = t[c].round(3)
    t["razao_sug"] = t.razao_sug.round(2)
    return t, tot17, tot24


for nome_arq, c17col, c24col in [("despesa", "valor_despesa17", "valor_despesa_uc"),
                                 ("renda", "valor_renda17", "valor_renda_uc")]:
    t, tot17, tot24 = tabela(c17col, c24col)
    t.index.name = "Cod_harmo"
    t.to_csv(SAIDA / f"comparacao_grupos_{nome_arq}.csv", encoding="utf-8")
    sem = p.loc[p.tipo != "ATRIBUIR", c24col].sum()
    print(f"\n== {nome_arq}: total/UC 2017 {tot17:,.2f} | 2024 {tot24:,.2f} | "
          f"2024 sem grupo (estrito) {100*sem/tot24:.2f}%")
    print(t.sinal.str.split("; ").explode().value_counts().drop("", errors="ignore").to_string())
    if nome_arq == "despesa":
        n1 = t.groupby("nivel1")[["pct17", "pct24", "pct24_sug"]].sum().round(2).sort_values("pct17", ascending=False)
        n1.to_csv(SAIDA / "comparacao_nivel1.csv", encoding="utf-8")
        print(n1.to_string())
