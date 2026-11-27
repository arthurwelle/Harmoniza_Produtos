"""Passo 2: propõe Cod_harmo para cada célula 2024 a partir da harmonização vigente (base/).

Unidade: célula 2024 = código de 6 dígitos (os 2 últimos dos 8 dígitos de V9001 são sinônimos,
equivalente ao código de 5 dígitos de 2002-2017; ADR 0001).

Evidência usada, na ordem da hierarquia da CONSTITUICAO:
  1. estrutura das classificações: mapa de quadros 2024 -> 2017 derivado dos próprios dados
     (pares de células com descrição idêntica) e caminho de níveis dos tradutores IBGE
     (a codificação de níveis é a mesma em 2017 e 2024: 99,6% de concordância no nível 3);
  2. classificação-base: Cod_harmo das células 2017 em base/depara.csv;
  5. descrição textual (casamento exato e aproximado).

Tipos de saída (por célula 2024):
  ATRIBUIR  célula nova de 2024 recebe grupo existente (não estrutural). ALTA ou MÉDIA.
  REVISAR   evidência insuficiente ou conflitante. Nada é aplicado; vai com sugestão e candidatos.
Nenhuma proposta cria, une ou divide grupos: isso é estrutural e fica para decisão humana.

Rodar da pasta POF2024/harmonizacao:  python scripts/02_propoe.py
"""
import difflib
import pathlib
import re
import unicodedata
from collections import Counter

import pandas as pd

H = pathlib.Path(__file__).resolve().parents[1]
FONTE, SAIDA = H / "fonte", H / "saida"
SAIDA.mkdir(exist_ok=True)

STOP = {"DE", "DA", "DO", "DAS", "DOS", "E", "OU", "COM", "PARA", "A", "O", "AS", "OS", "EM",
        "ETC", "NA", "NO", "NAS", "NOS", "P", "C", "S", "POR", "SEM", "TIPO", "EXCETO", "INCLUSIVE"}
GENERICOS = {"AGREGADO", "OUTROS", "OUTRAS", "OUTRO", "OUTRA"}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tokens(n):
    out = set()
    for t in n.split():
        if t in STOP:
            continue
        if len(t) > 3 and t.endswith("S"):
            t = t[:-1]
        out.add(t)
    return out


def nucleo(desc):
    """Texto antes do primeiro parêntese (qualificadores do IBGE mudam muito entre edições)."""
    return norm(str(desc).split("(")[0])


def _s(a_n, a_t, b_n, b_t):
    if not a_t or not b_t:
        return 0.0
    jac = len(a_t & b_t) / len(a_t | b_t)
    rat = difflib.SequenceMatcher(None, a_n, b_n).ratio()
    return 0.6 * jac + 0.4 * rat


def score(a, b):
    """a, b = (norm, tokens, nucleo, tokens_nucleo). Máximo entre texto inteiro, núcleo e contenção."""
    full = _s(a[0], a[1], b[0], b[1])
    core = _s(a[2], a[3], b[2], b[3])
    menor = min(len(a[3]), len(b[3]))
    cont = (len(a[3] & b[3]) / menor) if menor >= 2 else 0.0
    return max(full, core, 0.9 * cont)


# ------------------------------------------------------------------ dados
c24 = pd.read_csv(FONTE / "celulas_2024.csv")
c17 = pd.read_csv(FONTE / "celulas_2017.csv").set_index("Codigo")
grupos = pd.read_csv(H / "base/grupos.csv", dtype=str).set_index("Cod_harmo")
dep = pd.read_csv(H / "base/depara.csv", dtype=str)
d17 = dep[dep.Ano == "2017"].copy()
d17["Codigo"] = d17.Codigo.astype(int)
d17["n"] = d17.Descri_Item.map(norm)
d17["t"] = d17.n.map(tokens)
d17["nc"] = d17.Descri_Item.map(nucleo)
d17["tc"] = d17.nc.map(tokens)
d17["Quadro_H"] = d17.Quadro_H.astype(int)
c17["Cod_harmo"] = c17.Cod_harmo.astype(str).str.zfill(5)
grupo_de = c17.Cod_harmo.to_dict()

c24["n"] = c24.Descri_Item.map(norm)
c24["t"] = c24.n.map(tokens)
c24["nc"] = c24.Descri_Item.map(nucleo)
c24["tc"] = c24.nc.map(tokens)
idx_exato = d17.groupby("n").Codigo.apply(lambda s: sorted(set(s))).to_dict()

# mapa de quadros 2024 -> 2017 a partir das descrições idênticas e únicas
pares = []
for _, r in c24.iterrows():
    e = idx_exato.get(r.n)
    if e and len(e) == 1 and r.n not in GENERICOS:
        pares.append((r.Quadro_POF, int(c17.loc[e[0], "Quadro_H"])))
qm = pd.DataFrame(pares, columns=["Q24", "Q17"]).value_counts().rename("n").reset_index()
qm["share"] = qm.n / qm.groupby("Q24").n.transform("sum")
qm = qm[qm.share >= 0.10]
mapa_q = qm.groupby("Q24").Q17.apply(list).to_dict()
qm.sort_values(["Q24", "share"], ascending=[True, False]).to_csv(SAIDA / "mapa_quadros_2024_2017.csv", index=False)

itens_por_q = {q: g for q, g in d17.groupby("Quadro_H")}


def niv_ok(r, cod17, nivel="nivel3"):
    """True/False se os níveis IBGE são comparáveis e iguais/diferentes; None se não dá para comparar."""
    if "v8000" not in str(r.variaveis) or c17.loc[cod17, "variavel_17"] != "V8000_DEFLA":
        return None  # rendimentos/deduções: o caminho do tradutor é o da dedução, não comparável
    a, b = r[nivel], c17.loc[cod17, nivel + "_17"]
    if pd.isna(a) or pd.isna(b):
        return None
    return int(a) == int(b)


def nome(g):
    return grupos.loc[g, "nome"] if g in grupos.index else "?"


def sugestao_por_nivel(r, quadros):
    """Grupo 2017 mais pesado entre células com o mesmo nível IBGE (nivel4, senão nivel3) nos quadros mapeados."""
    if "v8000" not in str(r.variaveis):
        return None, None, ""  # rendimentos/deduções: nível do tradutor de despesa não serve
    base = c17[c17.Quadro_H.isin(quadros)] if quadros else c17
    for nv in ["nivel4", "nivel3"]:
        if pd.notna(r[nv]):
            sub = base[base[nv + "_17"] == r[nv]]
            if len(sub):
                w = sub.groupby("Cod_harmo").valor_uc17.sum().sort_values(ascending=False)
                if w.sum() == 0:
                    w = sub.Cod_harmo.value_counts()
                return w.index[0], nv, ";".join(w.index[:3])
    return None, None, ""


# ------------------------------------------------------------------ propostas
linhas = []
for _, r in c24.iterrows():
    quadros = mapa_q.get(r.Quadro_POF, [])
    out = dict(Codigo=r.Codigo, Quadro_POF=r.Quadro_POF, Descri_Item=r.Descri_Item,
               caminho_ibge=r.caminho_ibge if pd.notna(r.caminho_ibge) else r.caminho_alim,
               valor_uc=round(r.valor_uc, 4), observado=r.observado,
               quadros_2017=";".join(map(str, quadros)))
    e = idx_exato.get(r.n, [])
    e_filtrado = [c for c in e if c17.loc[c, "Quadro_H"] in quadros] if quadros else e
    if e and quadros and e_filtrado:
        e = e_filtrado
    elif e and quadros and not e_filtrado and r.n in GENERICOS:
        e = []  # "AGREGADO"/"OUTROS" de outro quadro não serve de evidência

    if e:
        gs = sorted({grupo_de[c] for c in e})
        out.update(metodo="exato", score=1.0, celulas_2017=";".join(f"2017:{c}" for c in e),
                   grupos_candidatos=";".join(gs))
        niv = [niv_ok(r, c) for c in e]
        if len(gs) == 1:
            g = gs[0]
            if False in niv and True not in niv:
                out.update(tipo="ATRIBUIR", confianca="MÉDIA", Cod_harmo=g, Cod_harmo_sugerido=g,
                           motivo_ia=f"descrição idêntica à de {len(e)} célula(s) 2017 do grupo {g}; "
                                     "o IBGE mudou o nível 3 do tradutor entre 2017 e 2024",
                           alerta="IBGE reclassificou (nível 3 diferente)",
                           regras_ref="R6;R8")
            else:
                conf = "ALTA" if (quadros and set(c17.loc[e, "Quadro_H"]) <= set(quadros)) else "MÉDIA"
                out.update(tipo="ATRIBUIR", confianca=conf, Cod_harmo=g, Cod_harmo_sugerido=g,
                           motivo_ia=f"descrição idêntica à de {len(e)} célula(s) 2017 do grupo {g}"
                                     + ("" if conf == "ALTA" else "; quadro sem correspondência no mapa"),
                           regras_ref="R6;R7")
        else:
            # mesma descrição em células 2017 de grupos diferentes
            w = c17.loc[e].groupby("Cod_harmo").valor_uc17.sum().sort_values(ascending=False)
            out.update(tipo="REVISAR", confianca="BAIXA", Cod_harmo_sugerido=w.index[0],
                       motivo_ia="descrição idêntica em células 2017 de grupos diferentes ("
                                 + ", ".join(gs) + "); escolher pelo contexto do quadro",
                       regras_ref="R1;R6")
    else:
        pool = pd.concat([itens_por_q[q] for q in quadros if q in itens_por_q]) if quadros else d17
        if r.n in GENERICOS or not r.t:
            cand = pd.DataFrame()
        else:
            # pré-filtro por token comum para não rodar difflib em tudo
            pre = pool[pool.t.map(lambda t: bool(t & r.t))]
            if len(pre):
                a = (r.n, r.t, r.nc, r.tc)
                pre = pre.assign(s=[score(a, b) for b in zip(pre.n, pre.t, pre.nc, pre.tc)])
                cand = (pre.sort_values("s", ascending=False)
                           .drop_duplicates("Codigo").head(5))
            else:
                cand = pd.DataFrame()
        if len(cand):
            best = cand.iloc[0]
            g1 = grupo_de[best.Codigo]
            outros = cand[(cand.s >= best.s - 0.05) & (cand.Codigo.map(grupo_de) != g1)]
            ok = niv_ok(r, best.Codigo)
            out.update(metodo="aproximado", score=round(best.s, 3),
                       celulas_2017=";".join(f"2017:{c}" for c in cand.Codigo),
                       grupos_candidatos=";".join(dict.fromkeys(cand.Codigo.map(grupo_de))),
                       item_2017_mais_proximo=best.Descri_Item)
            ok4 = niv_ok(r, best.Codigo, "nivel4")
            rivais = cand[(cand.Codigo.map(grupo_de) != g1) & (cand.s >= 0.70)]
            aceita = len(outros) == 0 and ok is not False and (best.s >= 0.80 or (best.s >= 0.70 and ok4))
            if aceita:
                conf = "ALTA" if best.s >= 0.95 else "MÉDIA"
                out.update(tipo="ATRIBUIR", confianca=conf, Cod_harmo=g1, Cod_harmo_sugerido=g1,
                           motivo_ia=f"descrição quase igual a '{best.Descri_Item}' (2017:{best.Codigo}, "
                                     f"score {best.s:.2f}), mesmo quadro"
                                     + ("" if ok is None else " e mesmo nível 3 IBGE")
                                     + (" e nível 4" if ok4 else ""),
                           regras_ref="R6")
            else:
                motivo = []
                if best.s < 0.80:
                    motivo.append(f"melhor correspondência fraca (score {best.s:.2f})")
                if len(outros):
                    motivo.append("candidatos próximos em grupos diferentes")
                if ok is False:
                    motivo.append("nível 3 IBGE difere do melhor candidato")
                sug, nv, top = (g1, None, "") if best.s >= 0.6 else sugestao_por_nivel(r, quadros)
                out.update(tipo="REVISAR", confianca="BAIXA", Cod_harmo_sugerido=sug or g1,
                           motivo_ia="; ".join(motivo) + (f"; sugestão pelo {nv} IBGE" if nv else ""),
                           regras_ref="R4;R6")
        else:
            sug, nv, top = sugestao_por_nivel(r, quadros)
            out.update(metodo="nivel_ibge" if sug else "nenhum", score=0.0, grupos_candidatos=top,
                       tipo="REVISAR", confianca="BAIXA", Cod_harmo_sugerido=sug,
                       motivo_ia=("sem descrição correspondente em 2017"
                                  + (f"; sugestão = grupo mais pesado com o mesmo {nv} IBGE" if sug else "")
                                  + "; possível produto novo (CRIAR) ou ausência estrutural (R5)"),
                       regras_ref="R4;R5")

        if out.get("tipo") == "ATRIBUIR" and len(rivais):
            rv = rivais.iloc[0]
            out["alerta"] = (f"conferir: '{rv.Descri_Item}' (2017:{rv.Codigo}, grupo {grupo_de[rv.Codigo]}) "
                             f"também é próximo (score {rv.s:.2f})")
    linhas.append(out)

p = pd.DataFrame(linhas)
p["nome_grupo"] = p.Cod_harmo_sugerido.map(lambda g: nome(g) if isinstance(g, str) else "")
p["Codigo"] = p.Codigo.astype(str)
cols = ["Codigo", "Quadro_POF", "Descri_Item", "tipo", "confianca", "Cod_harmo", "Cod_harmo_sugerido",
        "nome_grupo", "metodo", "score", "item_2017_mais_proximo", "celulas_2017", "grupos_candidatos",
        "quadros_2017", "caminho_ibge", "valor_uc", "observado", "motivo_ia", "regras_ref", "alerta"]
p = p.reindex(columns=cols)
p.to_csv(SAIDA / "propostas_2024.csv", index=False, encoding="utf-8")

# de-para no mesmo formato de base/depara.csv (só o que tem ALTA/MÉDIA)
dp = p[p.tipo == "ATRIBUIR"][["Quadro_POF", "Codigo", "Descri_Item", "Cod_harmo"]].copy()
dp.insert(0, "Ano", "2024")
dp = dp.rename(columns={"Quadro_POF": "Quadro_H"}).sort_values(["Codigo", "Descri_Item"])
dp.to_csv(SAIDA / "depara_2024.csv", index=False, encoding="utf-8")

# de-para provisório "com sugestões" (inclui REVISAR pela sugestão) para análise de sensibilidade
ds = p[p.Cod_harmo_sugerido.notna()][["Quadro_POF", "Codigo", "Descri_Item", "Cod_harmo_sugerido", "tipo"]]
ds = ds.rename(columns={"Quadro_POF": "Quadro_H", "Cod_harmo_sugerido": "Cod_harmo"})
ds.insert(0, "Ano", "2024")
ds.to_csv(SAIDA / "depara_2024_com_sugestoes.csv", index=False, encoding="utf-8")

tot = p.valor_uc.sum()
res = p.groupby(["tipo", "confianca"]).agg(celulas=("Codigo", "size"), valor_uc=("valor_uc", "sum"))
res["pct_valor"] = (100 * res.valor_uc / tot).round(2)
print(res)
print("alertas:", p.alerta.notna().sum())
