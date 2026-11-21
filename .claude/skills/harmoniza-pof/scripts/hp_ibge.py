"""Tradutores oficiais do IBGE (POF 2008-2009 e 2017-2018) como evidência.

Uso:
  python hp_ibge.py gerar                 # originais em harmonizacao/fonte/ibge/original -> tradutor_ibge.csv
  python hp_ibge.py auditar [--ano 2017] [--saida arq.md]

O tradutor diz em que linha das tabelas oficiais de despesa (ou de alimentação) o IBGE soma cada código
de 5 dígitos. É a classificação usada nas publicações da POF: evidência de nível 4 da hierarquia
(CONSTITUICAO.md, "outras harmonizações"), útil para achar célula fora do lugar em 2008 e 2017.

Arquivos (harmonizacao/fonte/ibge/):
  original/2017_Tradutor_Despesa_Geral.xls, original/2017_Tradutor_Alimentacao.xls  (IBGE, Tradutores_20210304)
  original/2008_Despesa_total.doc, original/2008_Codigos_de_alimentacao.xls          (IBGE, tradutores 2008-2009)
  tradutor_ibge.csv  Ano|Codigo|tabela|grupo_ibge|linha|descricao   (gerado; Codigo com 5 dígitos)

Auditoria: cada célula de 2008/2017 recebe o grande grupo do IBGE. Dois sinais, só evidência (nunca
decisão automática):
  - G (grupo): o nível 1 do repositório não corresponde ao grande grupo do IBGE.
  - L (linha): a linha fina do IBGE da célula é minoria no grupo do repositório naquele ano e é a linha
    majoritária de outro grupo do repositório (sugere o grupo).
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd

from hp_comum import carrega_estado, celulas_df, dir_h, grava_texto, le_csv

COLS = ["Ano", "Codigo", "tabela", "grupo_ibge", "linha", "descricao"]


def dir_ibge() -> Path:
    return dir_h() / "fonte" / "ibge"


def sem_acento(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def c5(c) -> str:
    c = str(c).strip()
    return c.zfill(5) if c.isdigit() else c


# ------------------------------------------------------------------ gerar

def _2017() -> list[dict]:
    o = dir_ibge() / "original"
    d = pd.read_excel(o / "2017_Tradutor_Despesa_Geral.xls", dtype=str).fillna("")
    out = []
    for r in d.itertuples(index=False):
        if r.Nivel_2 == "11":
            grupo = r.Descricao_3
        elif r.Nivel_1 == "1":
            grupo = "Outras despesas correntes"
        else:
            grupo = r.Descricao_1
        niveis = [(r.Nivel_5, r.Descricao_5), (r.Nivel_4, r.Descricao_4), (r.Nivel_3, r.Descricao_3),
                  (r.Nivel_2, r.Descricao_2)]
        linha, desc = next(((n, t) for n, t in niveis if n and t), ("", ""))
        tab = "despesa"
        if r.Variavel != "V8000_DEFLA":
            desc, tab = f"{desc} ({r.Variavel})", "despesa_outra"
        out.append({"Ano": "2017", "Codigo": c5(r.Codigo), "tabela": tab, "grupo_ibge": grupo,
                    "linha": linha, "descricao": desc})
    a = pd.read_excel(o / "2017_Tradutor_Alimentacao.xls", dtype=str).fillna("")
    for r in a.itertuples(index=False):
        out.append({"Ano": "2017", "Codigo": c5(r.Codigo), "tabela": "alimentacao",
                    "grupo_ibge": "Alimentacao", "linha": r.Nivel_3 or r.Nivel_2,
                    "descricao": f"{r.Descricao_2} > {r.Descricao_3}".strip(" >")})
    return out


def _expande(txt: str) -> list[str]:
    cods = []
    for a, b in re.findall(r"(\d{5})\s*a\s*(\d{5})", txt):
        cods += [f"{i:05d}" for i in range(int(a), int(b) + 1)]
    resto = re.sub(r"\d{5}\s*a\s*\d{5}", " ", txt)
    cods += re.findall(r"\b\d{5}\b", resto)
    return cods


def _texto_doc(path: Path) -> list[str]:
    import olefile
    wd = olefile.OleFileIO(str(path)).openstream("WordDocument").read()
    i = wd.find("C\x00O\x00M\x00P\x00O\x00N".encode("latin-1"))
    t = wd[max(i, 0):].decode("utf-16-le", errors="ignore")
    t = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "\n", t).replace("\r", "\n")
    return [x.strip() for x in t.split("\n") if x.strip()]


def _2008() -> list[dict]:
    o = dir_ibge() / "original"
    linhas = _texto_doc(o / "2008_Despesa_total.doc")
    topo, ultimo_top = {}, ""
    out = []
    pat = re.compile(r"^(\d+(?:\.\d+)*)?\s*[-–]\s*(.+?)\s*[-–]\s*(.*)$")
    for ln in linhas:
        m = pat.match(ln)
        if not m:
            continue
        num, nome, resto = m.group(1) or "", m.group(2).strip(), m.group(3)
        if num and "." not in num:
            topo[num] = nome
        if num:
            ultimo_top = num.split(".")[0]
        cods = _expande(resto)
        if not cods:
            continue
        # linhas sem número no original (ex.: "– Gasolina - veículo próprio") herdam o grupo da anterior
        top = num.split(".")[0] if num else ultimo_top
        grupo = topo.get(top, nome)
        for c in cods:
            out.append({"Ano": "2008", "Codigo": c, "tabela": "despesa", "grupo_ibge": grupo,
                        "linha": num, "descricao": nome})
    a = pd.read_excel(o / "2008_Codigos_de_alimentacao.xls", sheet_name="Componentes", dtype=str, header=2).fillna("")
    a.columns = ["Codigo", "n1", "d1", "n2", "d2", "n3", "d3"]
    for r in a.itertuples(index=False):
        if not str(r.Codigo).strip().isdigit():
            continue
        out.append({"Ano": "2008", "Codigo": c5(r.Codigo), "tabela": "alimentacao", "grupo_ibge": "Alimentacao",
                    "linha": r.n3 or r.n2, "descricao": f"{r.d2} > {r.d3}".strip(" >")})
    return out


def cmd_gerar(_a) -> None:
    df = pd.DataFrame(_2017() + _2008(), columns=COLS).drop_duplicates()
    df = df.sort_values(["Ano", "Codigo", "tabela"]).reset_index(drop=True)
    alvo = dir_ibge() / "tradutor_ibge.csv"
    df.to_csv(alvo, index=False, encoding="utf-8", lineterminator="\n")
    print(f"OK {len(df)} linhas → {alvo}")
    print(df.groupby(["Ano", "tabela"]).size().to_string())


# ------------------------------------------------------------------ uso pelas outras ferramentas

def carrega() -> pd.DataFrame:
    p = dir_ibge() / "tradutor_ibge.csv"
    if not p.exists():
        return pd.DataFrame(columns=COLS)
    t = le_csv(p)
    # alimentação tem linha mais fina que a despesa (que só diz "Alimentação"): prefere a de alimentação
    # despesa_outra = mesmo código usado para INSS/deduções (V1904, V531...), só se não houver outra linha
    t["_o"] = t["tabela"].map({"alimentacao": 0, "despesa": 1}).fillna(2)
    return t.sort_values("_o").drop_duplicates(["Ano", "Codigo"]).drop(columns="_o")


# grande grupo do repositório (nível 1) → grande grupo do IBGE (sem acento, minúsculo)
def grupo_repo_para_ibge(nivel1: str) -> str:
    m = re.match(r"\s*(\d+)", nivel1 or "")
    n = int(m.group(1)) if m else -1
    if 1 <= n <= 16:
        return "alimentacao"
    return {31: "habitacao", 32: "habitacao", 33: "vestuario", 34: "transporte",
            35: "higiene e cuidados pessoais", 36: "assistencia a saude", 37: "educacao",
            38: "recreacao e cultura", 39: "servicos pessoais|fumo", 40: "despesas diversas",
            41: "outras despesas correntes", 42: "aumento do ativo", 43: "diminuicao do passivo"}.get(n, "")


def norm_grupo_ibge(g: str) -> str:
    g = sem_acento(g)
    return {"assistencia a saude": "assistencia a saude", "recreacao e cultura": "recreacao e cultura"}.get(g, g)


def anota(cels: pd.DataFrame, trad: pd.DataFrame | None = None) -> pd.DataFrame:
    """Recebe celulas_df (Ano, Codigo, ...) e devolve com grupo_ibge, linha, descricao_ibge."""
    trad = carrega() if trad is None else trad
    x = cels.copy()
    x["_c5"] = x["Codigo"].map(c5)
    t = trad.rename(columns={"Codigo": "_c5", "descricao": "descricao_ibge"})[["Ano", "_c5", "grupo_ibge", "linha", "descricao_ibge"]]
    return x.merge(t, on=["Ano", "_c5"], how="left").drop(columns="_c5").fillna({"grupo_ibge": "", "linha": "", "descricao_ibge": ""})


# ------------------------------------------------------------------ auditar

def auditoria(est: dict, anos=("2008", "2017")) -> pd.DataFrame:
    cel = celulas_df(est["depara"])
    cel = cel[cel["Ano"].isin(anos)]
    g = est["grupos"].set_index("Cod_harmo")
    x = anota(cel)
    x["nivel1"] = x["grupos"].map(lambda c: g.loc[c, "nivel1"] if c in g.index else "")
    x["esperado"] = x["nivel1"].map(grupo_repo_para_ibge)
    x["ibge_norm"] = x["grupo_ibge"].map(norm_grupo_ibge)
    x["sinal_G"] = [(e != "" and i != "" and i not in e.split("|")) for e, i in zip(x["esperado"], x["ibge_norm"])]
    # linha majoritária por (ano, grupo do repo)
    com = x[x["linha"] != ""]
    maj = (com.groupby(["Ano", "grupos"])["descricao_ibge"].agg(lambda s: Counter(s).most_common(1)[0][0]))
    tam = com.groupby(["Ano", "grupos"]).size()
    dono = {}
    for (ano, grp_), lin in maj.items():
        if tam[(ano, grp_)] >= 3:
            dono.setdefault((ano, lin), []).append(grp_)
    sug, sinal_l = [], []
    for r in x.itertuples():
        m = maj.get((r.Ano, r.grupos), "")
        outros = [d for d in dono.get((r.Ano, r.descricao_ibge), []) if d != r.grupos]
        # alimentos: o IBGE corta por outro eixo (orgânicos, queijos...), a linha fina não serve de sinal
        ok = (r.descricao_ibge != "" and m != "" and r.descricao_ibge != m and len(outros) == 1
              and norm_grupo_ibge(r.grupo_ibge) != "alimentacao")
        sinal_l.append(ok)
        sug.append(outros[0] if ok else "")
    x["sinal_L"], x["sugere"] = sinal_l, sug
    return x


def cmd_auditar(a) -> None:
    est = carrega_estado()
    anos = (a.ano,) if a.ano else ("2008", "2017")
    x = auditoria(est, anos)
    nomes = dict(zip(est["grupos"]["Cod_harmo"], est["grupos"]["nome"]))
    sem = (x["linha"] == "").sum()
    sus = x[x["sinal_G"] | x["sinal_L"]].sort_values(["Ano", "grupos", "Codigo"])
    linhas = [f"# Auditoria contra os tradutores do IBGE ({', '.join(anos)})", "",
              f"Células: {len(x)} · sem linha no tradutor: {sem} · com sinal G (grande grupo diferente): "
              f"{int(x['sinal_G'].sum())} · com sinal L (linha fina de outro grupo): {int(x['sinal_L'].sum())}", "",
              "| célula | grupo repo | sinal | IBGE: grupo > linha | sugere | itens |", "|---|---|---|---|---|---|"]
    for r in sus.itertuples():
        s = ("G" if r.sinal_G else "") + ("L" if r.sinal_L else "")
        linhas.append(f"| {r.cel} | {r.grupos} {nomes.get(r.grupos, '')[:30]} | {s} | {r.grupo_ibge} > {r.descricao_ibge[:50]} | "
                      f"{r.sugere} {nomes.get(r.sugere, '')[:25]} | {r.itens[:90]} |")
    txt = "\n".join(linhas) + "\n"
    if a.saida:
        grava_texto(txt, Path(a.saida))
        print(f"OK {len(sus)} células com sinal → {a.saida}")
    else:
        print(txt)


def main() -> None:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("gerar")
    s = sp.add_parser("auditar")
    s.add_argument("--ano")
    s.add_argument("--saida")
    a = ap.parse_args()
    {"gerar": cmd_gerar, "auditar": cmd_auditar}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
