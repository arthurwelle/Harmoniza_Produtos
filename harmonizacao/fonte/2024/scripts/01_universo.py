"""Passo 1: universo de células 2024 e de 2017.

Saídas em fonte/:
  celulas_2024.csv  uma linha por célula 2024 (Codigo 6 díg): descrição IBGE, caminho de níveis
                    do tradutor, tipo de registro, linhas e valor médio mensal por UC (ponderado).
  celulas_2017.csv  uma linha por célula 2017 (Codigo 5 díg): itens concatenados, Cod_harmo da base,
                    caminho de níveis do tradutor 2017 e valor médio mensal por UC (ponderado).

Rodar da pasta POF2024/harmonizacao:  python scripts/01_universo.py
"""
import gzip
import pathlib
import pandas as pd

H = pathlib.Path(__file__).resolve().parents[1]
P24 = H.parent
P17 = P24.parent / "POF2017"
FONTE = H / "fonte"
FONTE.mkdir(exist_ok=True)


def txt(s):
    return "" if pd.isna(s) else str(s).strip()


# ---------------------------------------------------------------- 2024
tr = pd.read_excel(P24 / "Tradutores_das_tabelas/Tradutor_Despesa_Geral.xls")
tr = tr.drop_duplicates(["CODIGO", "VARIAVEL"])
tr["Codigo"] = tr["CODIGO"].astype(int)

# caminho IBGE (despesa geral, só a variável principal v8000 quando existir)
def caminho(r, n=5, pref="NIVEL_", dpref="DESCRICAO_"):
    partes = []
    for i in range(0, n + 1):
        c, d = f"{pref}{i}", f"{dpref}{i}"
        if c in r and pd.notna(r[c]):
            partes.append(f"{int(r[c])} {txt(r.get(d))}".strip())
    return " > ".join(partes)

tr["caminho_ibge"] = tr.apply(caminho, axis=1)
tr_main = (tr.sort_values("VARIAVEL", key=lambda s: s.ne("v8000"))
             .groupby("Codigo")
             .agg(Descri_Item=("ITEM", "first"),
                  caminho_ibge=("caminho_ibge", "first"),
                  variaveis=("VARIAVEL", lambda s: ";".join(sorted(set(s)))),
                  nivel3=("NIVEL_3", "first"), nivel4=("NIVEL_4", "first"),
                  nivel5=("NIVEL_5", "first")))

ali = pd.read_excel(P24 / "Tradutores_das_tabelas/Tradutor_Alimentação.xls")
ali["Codigo"] = ali["CODIGO"].astype(int)
ali["caminho_alim"] = ali.apply(lambda r: caminho(r, 3), axis=1)
ali = ali.drop_duplicates("Codigo").set_index("Codigo")[["ITEM", "caminho_alim"]]

ren = pd.read_excel(P24 / "Tradutores_das_tabelas/Tradutor_Rendimento_Monetário.xlsx")
ren["Codigo"] = ren["CODIGO"].astype(int)
ren["caminho_renda"] = ren.apply(lambda r: caminho(r, 3), axis=1)
ren = ren.drop_duplicates("Codigo").set_index("Codigo")[["ITEM", "caminho_renda"]]

serv = pd.read_excel(P24 / "Tradutores_das_tabelas/Tradutor_Serviços.xlsx")
serv.columns = ["quest", "quadro", "Codigo", "desc_serv", "servico"]
serv = serv.drop_duplicates("Codigo").set_index("Codigo")[["desc_serv", "servico"]]

# valores observados nos microdados (saídas do script 3)
n_fam = pd.read_csv(P24 / "RDS/MORADORES_H.RDS", usecols=["V0306", "Peso"])
n_fam = n_fam.loc[n_fam.V0306 == 1, "Peso"].sum()

def resumo(arq, cols, tipo_col="Tipo"):
    d = pd.read_csv(arq, usecols=cols, compression="gzip")
    d["vp"] = d["Valor_Mensal"].fillna(0) * d["PESO_FINAL"]
    if tipo_col not in d:
        d[tipo_col] = "Renda"
    g = d.groupby("Codigo").agg(n_linhas=("vp", "size"), valor_uc=("vp", "sum"),
                                tipos=(tipo_col, lambda s: ";".join(sorted(set(s)))),
                                quadro_pof=("Quadro_POF", "first"))
    g["valor_uc"] /= n_fam
    return g

dsp = resumo(P24 / "GZ/Despesas_POF_2024.gz",
             ["Codigo", "Tipo", "Valor_Mensal", "PESO_FINAL", "Quadro_POF"])
rnd = resumo(P24 / "GZ/Rendas_POF_2024.gz",
             ["Codigo", "Valor_Mensal", "PESO_FINAL", "Quadro_POF"])
rnd["tipos"] = "Renda"
idx = dsp.index.union(rnd.index)
obs = pd.DataFrame(index=idx)
obs["valor_despesa_uc"] = dsp.valor_uc.reindex(idx).fillna(0)
obs["valor_renda_uc"] = rnd.valor_uc.reindex(idx).fillna(0)
obs["valor_uc"] = obs.valor_despesa_uc + obs.valor_renda_uc
obs["n_linhas"] = dsp.n_linhas.reindex(idx).fillna(0) + rnd.n_linhas.reindex(idx).fillna(0)
obs["tipos"] = pd.concat([dsp.tipos, rnd.tipos]).groupby(level=0).agg(lambda s: ";".join(sorted(set(";".join(s).split(";")))))

# universo = tradutores ∪ observados
cod = sorted(set(tr_main.index) | set(ali.index) | set(ren.index) | set(serv.index) | set(obs.index))
c24 = pd.DataFrame(index=pd.Index(cod, name="Codigo"))
c24 = c24.join(tr_main).join(ali, rsuffix="_ali").join(ren, rsuffix="_ren").join(serv).join(obs)
c24["Descri_Item"] = (c24["Descri_Item"].fillna(c24["ITEM"]).fillna(c24["ITEM_ren"])
                      .fillna(c24["desc_serv"]))
c24["Quadro_POF"] = (c24.index // 1000)
c24["observado"] = c24["n_linhas"].fillna(0) > 0
c24["fonte_descricao"] = (pd.Series("tradutor_despesa", index=c24.index)
                          .where(c24.index.isin(tr_main.index),
                                 pd.Series("tradutor_alimentacao", index=c24.index)
                                 .where(c24.index.isin(ali.index),
                                        pd.Series("tradutor_rendimento", index=c24.index)
                                        .where(c24.index.isin(ren.index),
                                               pd.Series("tradutor_servicos", index=c24.index)
                                               .where(c24.index.isin(serv.index), "SEM_DESCRICAO")))))
c24 = c24.drop(columns=["ITEM", "ITEM_ren", "desc_serv"])
for c in ["valor_uc", "valor_despesa_uc", "valor_renda_uc"]: c24[c] = c24[c].fillna(0)
c24["n_linhas"] = c24["n_linhas"].fillna(0).astype(int)
c24.reset_index().to_csv(FONTE / "celulas_2024.csv", index=False)
print("2024: células", len(c24), "| observadas", c24.observado.sum(),
      "| sem descrição", (c24.fonte_descricao == "SEM_DESCRICAO").sum(),
      "| valor sem descrição", round(c24.loc[c24.fonte_descricao == "SEM_DESCRICAO", "valor_uc"].sum(), 2))

# ---------------------------------------------------------------- 2017
dep = pd.read_csv(H / "base/depara.csv", dtype=str)
d17 = dep[dep.Ano == "2017"].copy()
d17["Codigo"] = d17.Codigo.astype(int)
c17 = d17.groupby("Codigo").agg(Quadro_H=("Quadro_H", "first"),
                                itens=("Descri_Item", lambda s: " | ".join(sorted(set(s)))),
                                n_itens=("Descri_Item", "nunique"),
                                Cod_harmo=("Cod_harmo", lambda s: ";".join(sorted(set(s)))))

t17 = pd.read_excel(P17 / "Tradutores/Tradutor_Despesa_Geral.xls")
t17["caminho_ibge17"] = t17.apply(lambda r: caminho(r, 5, "Nivel_", "Descricao_"), axis=1)
t17 = (t17.sort_values("Variavel", key=lambda s: s.ne("V8000_DEFLA"))
          .groupby("Codigo").agg(caminho_ibge17=("caminho_ibge17", "first"),
                                 variavel_17=("Variavel", "first"),
                                 nivel3_17=("Nivel_3", "first"), nivel4_17=("Nivel_4", "first"),
                                 nivel5_17=("Nivel_5", "first")))
c17 = c17.join(t17)

# valor 2017 por célula (GZ canônico do script 3 de 2017; peso dos moradores)
m17 = pd.read_csv(P17 / "RDS/MORADORES_H.RDS", usecols=["id_uc", "V0306", "PESO_FINAL"])
peso17 = m17.drop_duplicates("id_uc").set_index("id_uc")["PESO_FINAL"]
nf17 = m17.loc[m17.V0306 == 1, "PESO_FINAL"].sum()
for arq, col in [("Despesas_POF_2017.gz", "valor_despesa17"), ("Rendas_POF_2017.gz", "valor_renda17")]:
    cols = ["Codigo", "Valor_Mensal"] + (["id_uc"] if arq.startswith("Desp") else ["id_pes"])
    d = pd.read_csv(P17 / "GZ" / arq, usecols=cols, compression="gzip")
    if "id_pes" in d:
        d["id_uc"] = d.pop("id_pes") // 100
    d["vp"] = d.Valor_Mensal.fillna(0) * d.id_uc.map(peso17)
    c17[col] = (d.groupby("Codigo").vp.sum() / nf17).reindex(c17.index).fillna(0)
c17["valor_uc17"] = c17.valor_despesa17 + c17.valor_renda17
c17.reset_index().to_csv(FONTE / "celulas_2017.csv", index=False)
print("2017: células", len(c17), "| multigrupo", (c17.Cod_harmo.str.contains(";")).sum(),
      "| valor total/UC", round(c17.valor_uc17.sum(), 2), "| nf17", round(nf17))
