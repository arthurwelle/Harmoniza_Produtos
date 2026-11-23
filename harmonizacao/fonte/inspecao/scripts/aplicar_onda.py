"""Aplicou a onda 2026-11-22_tales-claude_inspecao-geral (cópia de hp_v4_onda.py com outro autor e revisor).

Uso, da raiz do repositório:
  python harmonizacao/fonte/inspecao/scripts/aplicar_onda.py harmonizacao/fonte/inspecao/inspecao_2026-11-22.json [--simular]

O id da onda usa a data do dia em que roda; a onda já aplicada é a de 2026-11-22 (rodar de novo criaria
outra). Autor "tales-claude"; revisor "tales".

Original (hp_v4_onda.py): conduz as ondas da v4 (ADR 0007: a IA decide), a partir de um arquivo de ondas já decididas.

Uso:
  python hp_v4_onda.py ONDAS.json [--so ESCOPO] [--simular]

ONDAS.json = {"ondas": [{"escopo", "tipo", "plano", "humano"?, "propostas": [...]}]}, cada proposta no schema do
LEDGER mais `pendencias_v3` (ids de pendências que a proposta resolve). Para cada onda: hp_onda.py abrir
--sem-branch --autor claude-v4; plano.md; propostas.json; hp_onda.py propostas; decisoes.json com todas as
propostas aceitas (revisor "claude-ia (ADR 0007)"); hp_onda.py fechar (valida; se falhar, restaura o estado).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / ".claude" / "skills" / "harmoniza-pof" / "scripts"))
import hp_comum
from hp_comum import agora, dir_ondas, grava_json, grava_texto, hoje, le_json, slug

AQUI = Path(__file__).resolve().parents[4] / ".claude" / "skills" / "harmoniza-pof" / "scripts"
sys.path.insert(0, str(AQUI))
REVISOR = "tales"
AUTOR = "tales-claude"


def roda(*args) -> str:
    r = subprocess.run([sys.executable, str(AQUI / args[0]), *args[1:]], capture_output=True, text=True,
                       encoding="utf-8")
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0:
        print(out)
        sys.exit(f"ERRO em {args[0]} {args[1] if len(args) > 1 else ''}")
    return out


def onda_id(escopo: str) -> str:
    return f"{hoje()}_{AUTOR}_{slug(escopo)}"


def roda_onda(o: dict, simular: bool) -> None:
    onda = onda_id(o["escopo"])
    props = []
    for i, p in enumerate(o["propostas"], 1):
        p = {"movimentos": [], "novos_grupos": {}, "regra_nova": None, "revoga": [], "conflito": None,
             "regras_ref": ["R6"], "confianca": "MEDIA", "impacto": "", **p}
        p["id"] = f"p{i:02d}"
        p["pendencias"] = list(dict.fromkeys(p.pop("pendencias_v3", []) + p.get("pendencias", [])))
        props.append(p)
    est = hp_comum.carrega_estado()
    chave = est["depara"]["Ano"] + ":" + est["depara"]["Codigo"]
    cels = {c for p in props for m in p["movimentos"] for c in m["celulas"]} | \
           {c for p in props for c in p.get("celulas_analisadas", []) or []}
    grupos = sorted(set(est["depara"].loc[chave.isin(cels), "Cod_harmo"])
                    | {m["para"] for p in props for m in p["movimentos"] if not m["para"].startswith("NOVO:")})
    t = Counter(p["tipo"] for p in props)
    n_mov = sum(len(m["celulas"]) for p in props for m in p["movimentos"])
    print(f"{onda}: {len(props)} propostas {dict(t)} · {n_mov} células movidas · {len(grupos)} grupos")
    if simular:
        return
    if len(props) > 40:
        sys.exit("ERRO: mais de 40 propostas; divida a onda (ONDAS.md).")
    pend = sorted({x for p in props for x in p["pendencias"]})
    roda("hp_onda.py", "abrir", "--escopo", o["escopo"], "--tipo", o.get("tipo", "pendencia"),
         "--grupos", ",".join(grupos), "--autor", AUTOR, "--sem-branch",
         *(["--pendencias", ",".join(pend)] if pend else []))
    od = dir_ondas() / onda
    plano = (od / "plano.md").read_text(encoding="utf-8")
    plano = plano.replace("_preencher: sinal que motivou (alerta, pendência, balde), alternativas consideradas._",
                          o["plano"])
    plano = plano.replace("_preencher com o motivo dado pelo autor ao confirmar o escopo._", o.get(
        "humano", "Tales (2026-10-16): \"faz uma v4 deixando a ia decidir. mas nao mexe na v3\". A v4 parte da "
                  "branch v3 e decide as pendências que a v3 deixou para humanos (ADR 0007)."))
    plano = plano.replace("_preencher antes de ler o contexto; confrontar no diagnóstico._",
                          "Ver a evidência de cada proposta (o dossiê de cada pendência da v3 foi relido com quadro, "
                          "itens, tradutor do IBGE e revisão manual).")
    grava_texto(plano, od / "plano.md")
    grava_json({"onda": onda, "autor_ia": "claude-opus-5-5", "resumo": o.get("resumo", o["plano"]),
                "propostas": props}, od / "propostas.json")
    print("  " + roda("hp_onda.py", "propostas", onda).strip().splitlines()[-2])
    grava_json({"onda": onda, "modo": "inspecao-delegada", "decisoes": {
        p["id"]: {"veredito": "aceita", "motivo": "", "revisor": REVISOR, "ts": agora(), "movimentos": None}
        for p in props}}, od / "decisoes.json")
    print("  " + roda("hp_onda.py", "fechar", onda).strip().splitlines()[0])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ondas")
    ap.add_argument("--so", default="")
    ap.add_argument("--simular", action="store_true")
    a = ap.parse_args()
    for o in le_json(Path(a.ondas))["ondas"]:
        if a.so and slug(o["escopo"]) != slug(a.so):
            continue
        if (dir_ondas() / onda_id(o["escopo"])).exists():
            print(f"{onda_id(o['escopo'])}: já existe, pulando")
            continue
        roda_onda(o, a.simular)


if __name__ == "__main__":
    sys.exit(main())
