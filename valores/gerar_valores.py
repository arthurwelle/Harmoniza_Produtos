"""Gera data/valores/valores.json, lido pela aba Valores (valores/index.html).

Para cada grupo de consumo da harmonização do repositório (harmonizacao/estado/), em cada edição
da POF e recorte, calcula:
  - prevalência: % das unidades de consumo (UCs) com gasto no grupo;
  - % do gasto da categoria: participação no gasto do nível 1;
  - % do consumo e % do consumo sem aluguel (31001);
  - gasto médio mensal por UC (inclui quem não comprou), em R$ de janeiro de 2018 (IPCA).
Recortes: Brasil (2002 em diante) e regiões metropolitanas (RGMT preenchido; as seis edições).

Entrada: os bancos de despesa harmonizados (GZ) e de moradores (MORADORES_H.RDS, que é CSV) de cada
edição, gerados pelos Rmd 1-3 de cada ano. Uso, da raiz do repositório:

    python valores/gerar_valores.py C:/Users/arthur/Desktop/POF

Sem intervalos de confiança (o desenho amostral fica para depois).
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
POF = Path(sys.argv[1] if len(sys.argv) > 1 else "C:/Users/arthur/Desktop/POF")
ANOS = ["1987", "1995", "2002", "2008", "2017", "2024"]
EDICAO = {"1987": "1987-1988", "1995": "1995-1996", "2002": "2002-2003", "2008": "2008-2009", "2017": "2017-2018", "2024": "2024-2025"}
DESPESAS = {a: POF / f"POF{a}" / "GZ" / f"Despesas_POF_{a}.gz" for a in ANOS}
# IPCA (número-índice, dez/1993 = 100) do mês de referência de cada edição; fonte: IBGE, série 433
# (mesmos meses de referência que pofanalise::pof_deflacionar). 1987 está em cruzados: sem deflator.
# 2024-2025: referência maio de 2025 (mês em que o DEFLATOR dos microdados vale 1; IPCA mai/2025, SIDRA t.1737).
IPCA = {"1995": 1348.48, "2002": 2085.68, "2008": 2906.74, "2017": 4930.72, "2024": 7295.46}
IPCA_REF = 4930.72
# níveis 1 de consumo: alimentos (1-16) e não alimentos (31-40)
N1_CONSUMO = set(range(1, 17)) | set(range(31, 41))
ALUGUEL = "31001"


def n1_num(s):
    try:
        return int(str(s).split(".")[0])
    except ValueError:
        return -1


def ucs(ano):
    m = pd.read_csv(POF / f"POF{ano}" / "RDS" / "MORADORES_H.RDS", low_memory=False,
                    usecols=lambda c: c in ("id_uc", "RGMT", "PESO_FINAL", "Peso"))
    u = m.drop_duplicates("id_uc").set_index("id_uc")
    if ano == "1995":  # peso só no arquivo de domicílios
        d = pd.read_csv(POF / "POF1995" / "RDS" / "DOMICILIOS.RDS", low_memory=False)
        d["id_dom"] = d.V0030 * 10**6 + d.V0050 * 10**3 + d.V0060 * 100 + d.V0065
        u["w"] = (u.index.to_series() // 100).map(d.groupby("id_dom").V0518.first())
    else:
        u["w"] = u["PESO_FINAL"] if "PESO_FINAL" in u else u["Peso"]
    u["rm"] = u["RGMT"].notna()
    return u[["w", "rm"]]


def main():
    dep = pd.read_csv(RAIZ / "harmonizacao/estado/depara.csv", dtype=str, keep_default_na=False)
    grp = pd.read_csv(RAIZ / "harmonizacao/estado/grupos.csv", dtype=str, keep_default_na=False)
    grp = grp[grp.status == "ativo"].copy()
    grp["n1n"] = grp.nivel1.map(n1_num)
    cons = grp[grp.n1n.isin(N1_CONSUMO)].sort_values("Cod_harmo")
    cons_set = set(cons.Cod_harmo)
    dep["c"] = dep.Codigo.str.lstrip("0")
    mapa = {a: dep[dep.Ano == a].drop_duplicates("c").set_index("c").Cod_harmo for a in ANOS}
    no_depara = {a: set(dep[dep.Ano == a].Cod_harmo) for a in ANOS}

    linhas, totais, checagem = [], [], {}
    for a in ANOS:
        u = ucs(a)
        cols = ["Codigo", "id_uc", "Valor_Mensal"] + (["Tipo"] if a != "1987" else [])
        d = pd.read_csv(DESPESAS[a], usecols=cols, dtype={"Codigo": str})
        d["g"] = d.Codigo.str.lstrip("0").map(mapa[a])
        checagem[a] = {"sem_grupo_%valor": round(100 * d.loc[d.g.isna(), "Valor_Mensal"].abs().sum()
                                                  / d.Valor_Mensal.abs().sum(), 4)}
        if "Tipo" in d:  # como pofanalise: INSS de doméstico e deduções não são consumo
            fora = (d.Tipo == "INSS") | d.Tipo.str.startswith("Deducao")
            d.loc[fora, "g"] = None
        d = d[d.g.isin(cons_set)]
        codigos_micro = set(d.Codigo.str.lstrip("0"))
        tem_registro = {g for g in cons_set
                        if set(mapa[a][mapa[a] == g].index) & codigos_micro}
        uc_g = d.groupby(["id_uc", "g"]).Valor_Mensal.sum().unstack(fill_value=0.0)
        uc_g = uc_g.reindex(u.index, fill_value=0.0)
        fator = IPCA_REF / IPCA[a] if a in IPCA else np.nan
        for rec, dom in (("Brasil", pd.Series(True, index=u.index)), ("Regiões metropolitanas", u.rm)):
            if rec == "Brasil" and a in ("1987", "1995"):
                continue
            w = u.w[dom]
            x = uc_g[dom]
            gasto = x.mul(w, axis=0).sum()
            prev = (x > 0).mul(w, axis=0).sum() / w.sum() * 100
            total = gasto.sum()
            total_sa = total - gasto.get(ALUGUEL, 0.0)
            n1 = cons.set_index("Cod_harmo").n1n
            tot_n1 = gasto.groupby(n1.reindex(gasto.index)).sum()
            totais.append({"ano": a, "recorte": rec, "n_uc": int(dom.sum()),
                           "consumo_medio_2018": None if np.isnan(fator) else round(total / w.sum() * fator, 2)})
            for g in cons.Cod_harmo:
                if g not in no_depara[a]:
                    st = "ausente"
                elif g not in tem_registro:
                    st = "sem_registro"
                elif gasto.get(g, 0.0) == 0:
                    st = "sem_compra"
                else:
                    st = "ok"
                v = gasto.get(g, 0.0)
                tn = tot_n1.get(n1[g], 0.0)
                linhas.append({
                    "ano": a, "recorte": rec, "cod": g, "status": st,
                    "prev": None if st == "ausente" else round(float(prev.get(g, 0.0)), 4),
                    "cat": None if st == "ausente" or tn == 0 else round(100 * v / tn, 4),
                    "tot": None if st == "ausente" else round(100 * v / total, 5),
                    "tot_sa": None if st == "ausente" or g == ALUGUEL else round(100 * v / total_sa, 5),
                    "gasto": None if st == "ausente" or np.isnan(fator) else round(v / w.sum() * fator, 4)})
        print(a, "ok", checagem[a])

    regras = pd.read_csv(RAIZ / "harmonizacao/estado/regras.csv", dtype=str, keep_default_na=False)
    aus = {}
    for r in regras[(regras.tipo == "ausencia_estrutural") & (regras.status == "ativa")].itertuples():
        for g in r.grupos.split(";"):
            for an in r.anos.split(";"):
                aus.setdefault(g, {})[an] = r.enunciado
    produtos = [{"cod": r.Cod_harmo, "nome": r.nome, "n1": r.nivel1, "n1n": int(r.n1n), "n2": r.nivel2,
                 "ausencia": aus.get(r.Cod_harmo, {})} for r in cons.itertuples()]
    idx = {p["cod"]: i for i, p in enumerate(produtos)}
    ST = {"ok": 0, "ausente": 1, "sem_registro": 3, "sem_compra": 4}
    REC = {"Brasil": 0, "Regiões metropolitanas": 1}
    valores = [[idx[l["cod"]], ANOS.index(l["ano"]), REC[l["recorte"]], l["prev"], l["cat"], l["tot"],
                l["tot_sa"], l["gasto"], ST[l["status"]]] for l in linhas]
    try:
        commit = subprocess.run(["git", "log", "-1", "--format=%h %ad %s", "--date=short"], cwd=RAIZ,
                                capture_output=True, text=True, encoding="utf-8").stdout.strip()
    except OSError:
        commit = ""
    out = {"gerado": date.today().isoformat(), "commit": commit, "edicoes": [EDICAO[a] for a in ANOS],
           "produtos": produtos, "valores": valores, "totais": totais, "checagem": checagem}
    dest = RAIZ / "data" / "valores"
    dest.mkdir(parents=True, exist_ok=True)
    with open(dest / "valores.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    tab = pd.DataFrame(linhas).merge(pd.DataFrame(produtos)[["cod", "nome", "n1", "n2"]], on="cod")
    with open(dest / "valores.csv", "w", encoding="utf-8-sig", newline="\n") as f:
        tab.to_csv(f, index=False, sep=";")
    print("OK", len(produtos), "grupos,", len(valores), "linhas →", dest)


if __name__ == "__main__":
    main()
