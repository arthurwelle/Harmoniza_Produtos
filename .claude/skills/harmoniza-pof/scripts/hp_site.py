"""Exporta o estado atual da harmonização para o formato que o site (index.html) lê.

Uso:
  python hp_site.py [--saida data/estado]

Gera:
  <saida>/folhas.csv    cod_final,n1,n2,nome,n_produtos,n_celulas,anos_cobertos,anos_ausentes,regras,dominio
  <saida>/produtos.csv  ano,cod_final,nome_final,descri_item,codigo,quadro,decisao,onda,motivo
  <saida>/meta.json     data, commit, contagens, ondas aplicadas

`decisao`/`onda`/`motivo` vêm do ledger: é a última decisão aceita que moveu aquela célula. Serve para o site
mostrar, no próprio item, por que ele está onde está.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import pandas as pd

from hp_comum import (ANOS, carrega_decisoes_todas, carrega_estado, dir_h, dir_ondas, grava_csv, grava_json,
                      hoje, junta, le_json, raiz_repo, separa, txt_movimentos)


def dominio(cod: str) -> str:
    """Alimentos usam os grupos 01-16 da hierarquia nova; o resto é não alimentar."""
    return "food" if cod[:2].isdigit() and 1 <= int(cod[:2]) <= 16 else "outros"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--saida", default="data/estado")
    a = p.parse_args()
    destino = raiz_repo() / a.saida

    est = carrega_estado()
    dep, grp, reg = est["depara"], est["grupos"], est["regras"]
    dep = dep.copy()
    dep["cel"] = dep["Ano"] + ":" + dep["Codigo"]

    # --- última decisão aceita que moveu cada célula
    dec = carrega_decisoes_todas()
    por_celula: dict[str, dict] = {}
    if not dec.empty:
        aplicadas = dec[dec["veredito"].isin(["aceita", "modificada"])].sort_values(["onda", "_ordem"])
        for r in aplicadas.itertuples():
            for mov in txt_movimentos(r.movimentos):
                for c in mov["celulas"]:
                    por_celula[c] = {"decisao": r.id, "onda": r.onda, "motivo": r.motivo_ia,
                                     "motivo_humano": r.motivo_humano, "revisor": r.revisor}

    nomes = dict(zip(grp["Cod_harmo"], grp["nome"]))
    regras_por_grupo: dict[str, list[str]] = {}
    for r in reg[reg["status"] == "ativa"].itertuples():
        for g in separa(r.grupos):
            regras_por_grupo.setdefault(g, []).append(f"{r.id} ({r.tipo})")

    # --- produtos
    prod = pd.DataFrame({
        "ano": dep["Ano"],
        "cod_final": dep["Cod_harmo"],
        "nome_final": dep["Cod_harmo"].map(lambda c: nomes.get(c, "?")),
        "descri_item": dep["Descri_Item"],
        "codigo": dep["Codigo"],
        "quadro": dep["Quadro_H"],
        "decisao": dep["cel"].map(lambda c: por_celula.get(c, {}).get("decisao", "")),
        "onda": dep["cel"].map(lambda c: por_celula.get(c, {}).get("onda", "")),
        "motivo": dep["cel"].map(lambda c: (por_celula.get(c, {}).get("motivo", "") or "")[:400]),
    })
    grava_csv(prod, destino / "produtos.csv")

    # --- folhas
    cel = dep.drop_duplicates(["Ano", "Codigo", "Cod_harmo"])
    n_cel = cel.groupby(["Cod_harmo", "Ano"]).size().unstack(fill_value=0)
    linhas = []
    for g in grp.itertuples():
        anos_com = [ano for ano in ANOS if g.Cod_harmo in n_cel.index and n_cel.loc[g.Cod_harmo].get(ano, 0) > 0]
        linhas.append({
            "cod_final": g.Cod_harmo, "n1": g.nivel1 or "(sem nível 1)", "n2": g.nivel2 or "(sem nível 2)",
            "nome": g.nome, "status": g.status,
            "n_produtos": int((dep["Cod_harmo"] == g.Cod_harmo).sum()),
            "n_celulas": int(sum(n_cel.loc[g.Cod_harmo]) if g.Cod_harmo in n_cel.index else 0),
            "anos_cobertos": len(anos_com), "anos_ausentes": junta(x for x in ANOS if x not in anos_com),
            "regras": junta(regras_por_grupo.get(g.Cod_harmo, [])), "dominio": dominio(g.Cod_harmo)})
    folhas = pd.DataFrame(linhas).sort_values("cod_final")
    grava_csv(folhas, destino / "folhas.csv")

    # --- meta
    commit = subprocess.run(["git", "log", "-1", "--format=%h %ad %s", "--date=short"], cwd=raiz_repo(),
                            capture_output=True, text=True, encoding="utf-8").stdout.strip()
    ondas = [le_json(x) for x in sorted(dir_ondas().glob("*/escopo.json"))]
    grava_json({"gerado_em": hoje(), "commit": commit, "folhas": len(folhas), "produtos": len(prod),
                "celulas": int(cel.shape[0]), "decisoes_aplicadas": len(por_celula),
                "ondas": [{"onda": o["onda"], "tipo": o.get("tipo"), "autor": o.get("autor")} for o in ondas]},
               destino / "meta.json")
    print(f"OK {len(folhas)} folhas · {len(prod)} produtos · {len(por_celula)} células com decisão → {destino}")


if __name__ == "__main__":
    main()
