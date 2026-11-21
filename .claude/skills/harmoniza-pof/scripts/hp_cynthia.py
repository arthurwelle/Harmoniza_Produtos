"""Revisões manuais (Cynthia, set-out/2026) como pendências com células.

Uso:
  python hp_cynthia.py extrair PASTA_DOS_TXT [--saida harmonizacao/fonte/revisoes_cynthia.csv]

Lê o texto extraído dos PDFs "Revisões manuais da harmonização" (uma folha por arquivo: 32, 37, 38,
40006) e devolve uma linha por ação: folha, n, tipo (Outlier pontual, Maturação de taxonomia,
Resíduo/analogia, Confirmação direta, Dúvida em aberto), de, para, itens (descrição|anos), texto.
Depois casa cada item com o de-para atual: ano + descrição normalizada → célula e grupo atual.
As ações foram feitas sobre a planilha do Drive (aba TodosJuntos), que pode divergir do estado do
repositório: o casamento diz se a célula ainda está no grupo de origem citado.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

from hp_comum import carrega_estado, dir_h, norm_texto

TIPOS = ["Outlier pontual", "Maturação de taxonomia", "Resíduo/analogia", "Confirmação direta",
         "Dúvida em aberto"]
ANO = r"(?:19|20)\d\d"
CONTROLE = re.compile("[\x00-\x08\x0b-\x1f]")
CAB = re.compile(r"^Folha\s+\S+\s*\(.*?\)\s+(\d+)\s*/\s*(\d+)\b")
RODAPE = re.compile(r"^Folha\s+\d+\s+.*\d+\s*/\s*\d+")


def blocos(txt: str, folha: str) -> list[dict]:
    # o travessão dos PDFs sai como caractere de controle (\x16): vira espaço
    txt = CONTROLE.sub(" ", txt)
    linhas = [l.rstrip() for l in txt.splitlines()]
    idx = [i for i, l in enumerate(linhas) if CAB.match(l.strip())]
    out = []
    for j, i in enumerate(idx):
        fim = idx[j + 1] if j + 1 < len(idx) else len(linhas)
        corpo = [l for l in linhas[i + 1:fim] if not RODAPE.match(l.strip())]
        n = CAB.match(linhas[i].strip()).group(1)
        texto = "\n".join(corpo).strip()
        tipo = next((t for t in TIPOS if t.lower() in texto[:80].lower()), "")
        acao = re.search(r"Ação:\s*(.+?)(?:\n\s*Ite(?:m|ns)|$)", texto, re.S)
        acao_txt = re.sub(r"\s+", " ", acao.group(1)) if acao else ""
        m = re.search(r"Mover de (\d{5}).*?para (\d{5})", acao_txt)
        de, para = (m.group(1), m.group(2)) if m else ("", "")
        if "Decidir" in acao_txt or "dúvida" in acao_txt.lower():
            tipo = "Dúvida em aberto"
        itens = []
        pos = re.search(r"Ite(?:m|ns)[^:\n]*:", texto)
        if pos:
            for l in texto[pos.end():].splitlines():
                l = l.strip()
                mm = re.match(rf"^(.+?)\s+({ANO}(?:\s*(?:,|e)\s*{ANO})*)\b(.*)$", l)
                if mm and mm.group(1).upper() == mm.group(1) and len(mm.group(1)) >= 2:
                    anos = re.findall(ANO, mm.group(2))
                    itens.append((mm.group(1).strip(" -–:"), ";".join(anos)))
                elif itens and l and not l.isupper():
                    break
        out.append({"folha": folha, "n": n, "tipo": tipo, "de": de, "para": para,
                    "acao": acao_txt[:300], "itens": " || ".join(f"{d}|{a}" for d, a in itens),
                    "texto": re.sub(r"\s+", " ", texto)[:1500]})
    return out


def casa(acoes: pd.DataFrame, est: dict) -> pd.DataFrame:
    dep = est["depara"].copy()
    dep["k"] = dep["Descri_Item"].map(norm_texto)
    idx = dep.groupby(["Ano", "k"]).agg(cels=("Codigo", lambda s: ";".join(sorted(set(s)))),
                                         grupos=("Cod_harmo", lambda s: ";".join(sorted(set(s)))))
    linhas = []
    for r in acoes.itertuples():
        for par in filter(None, r.itens.split(" || ")):
            desc, anos = par.rsplit("|", 1)
            for ano in filter(None, anos.split(";")):
                k = norm_texto(desc)
                hit = idx.loc[(ano, k)] if (ano, k) in idx.index else None
                linhas.append({"folha": r.folha, "n": r.n, "tipo": r.tipo, "de": r.de, "para": r.para,
                               "item": desc, "ano": ano,
                               "celulas": ";".join(f"{ano}:{c}" for c in hit["cels"].split(";")) if hit is not None else "",
                               "grupo_atual": hit["grupos"] if hit is not None else ""})
    return pd.DataFrame(linhas)


def main() -> None:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("extrair")
    s.add_argument("pasta")
    s.add_argument("--saida", default=str(dir_h() / "fonte" / "revisoes_cynthia.csv"))
    a = ap.parse_args()
    acoes = []
    for p in sorted(Path(a.pasta).glob("*.txt")):
        folha = p.stem.split("-")[0]
        acoes += blocos(p.read_text(encoding="utf-8"), folha)
    ac = pd.DataFrame(acoes)
    ac = ac[ac["acao"] != ""].reset_index(drop=True)
    ac.to_csv(a.saida, index=False, encoding="utf-8", lineterminator="\n")
    m = casa(ac, carrega_estado())
    saida_m = Path(a.saida).with_name(Path(a.saida).stem + "_celulas.csv")
    m.to_csv(saida_m, index=False, encoding="utf-8", lineterminator="\n")
    print(f"OK {len(ac)} ações → {a.saida}\n   {len(m)} itens×ano → {saida_m}")
    print(ac.groupby(["folha", "tipo"]).size().to_string())
    print(f"itens sem célula achada: {(m['celulas'] == '').sum()} · já fora do grupo de origem: "
          f"{((m['celulas'] != '') & (m['grupo_atual'] != m['de'])).sum()}")


if __name__ == "__main__":
    sys.exit(main())
