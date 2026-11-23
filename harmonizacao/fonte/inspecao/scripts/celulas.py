"""Gasto ponderado por célula (Ano:Codigo), mesmo cálculo de valores/gerar_valores.py do repositório."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
REPO, DADOS, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
ANOS = ["1987", "1995", "2002", "2008", "2017"]
def ucs(a):
    m = pd.read_csv(DADOS / f"POF{a}__RDS__MORADORES_H.RDS", low_memory=False,
                    usecols=lambda c: c in ("id_uc", "RGMT", "PESO_FINAL", "Peso"))
    u = m.drop_duplicates("id_uc").set_index("id_uc")
    if a == "1995":
        d = pd.read_csv(DADOS / "POF1995__RDS__DOMICILIOS.RDS", low_memory=False)
        d["id_dom"] = d.V0030 * 10**6 + d.V0050 * 10**3 + d.V0060 * 100 + d.V0065
        u["w"] = (u.index.to_series() // 100).map(d.groupby("id_dom").V0518.first())
    else:
        u["w"] = u["PESO_FINAL"] if "PESO_FINAL" in u else u["Peso"]
    u["rm"] = u["RGMT"].notna()
    return u[["w", "rm"]]
dep = pd.read_csv(REPO / "harmonizacao/estado/depara.csv", dtype=str, keep_default_na=False)
dep["c"] = dep.Codigo.str.lstrip("0")
out, sem = [], []
for a in ANOS:
    u = ucs(a)
    cols = ["Codigo", "id_uc", "Valor_Mensal"] + (["Tipo"] if a != "1987" else [])
    d = pd.read_csv(DADOS / f"POF{a}__GZ__Despesas_POF_{a}.gz", usecols=cols, dtype={"Codigo": str})
    d["c"] = d.Codigo.str.lstrip("0")
    if "Tipo" in d:
        fora = (d.Tipo == "INSS") | d.Tipo.fillna("").str.startswith("Deducao")
        d = d[~fora]
    mapa = dep[dep.Ano == a].drop_duplicates("c").set_index("c").Cod_harmo
    d["g"] = d.c.map(mapa)
    d = d.merge(u, left_on="id_uc", right_index=True, how="inner")
    d["vw"] = d.Valor_Mensal * d.w
    for rec, msk in (("BR", pd.Series(True, index=d.index)), ("RM", d.rm)):
        if rec == "BR" and a in ("1987", "1995"): continue
        x = d[msk]
        wtot = u.w[u.rm].sum() if rec == "RM" else u.w.sum()
        uc = x.groupby(["c", "id_uc"]).agg(v=("Valor_Mensal", "sum"), w=("w", "first"))
        prev = uc[uc.v > 0].groupby("c").w.sum() / wtot * 100
        g = x.groupby("c").agg(vw=("vw", "sum"), n_reg=("vw", "size"), grupo=("g", "first"))
        g["prev"] = prev.reindex(g.index).fillna(0)
        g["ano"] = a; g["rec"] = rec; g["wtot"] = wtot
        out.append(g.reset_index())
    tot = d.vw.abs().sum()
    s = d[d.g.isna()].groupby("c").vw.sum()
    sem.append(pd.DataFrame({"ano": a, "c": s.index, "vw": s.values, "pct_valor": 100 * s.values / tot}))
    print(a, "registros", len(d), "sem grupo %valor", round(100 * d.loc[d.g.isna(), "vw"].abs().sum() / tot, 4))
pd.concat(out).to_csv(OUT / "celulas_valor.csv", index=False)
pd.concat(sem).sort_values("pct_valor", ascending=False).to_csv(OUT / "sem_grupo.csv", index=False)
