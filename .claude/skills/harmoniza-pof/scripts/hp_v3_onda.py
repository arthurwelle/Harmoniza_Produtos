"""Conduz uma onda da v3 de ponta a ponta (ADR 0005), usando as ferramentas da skill.

Uso:
  python hp_v3_onda.py --escopo alimentos-cereais --n1 1,2,3 [--cynthia-folhas 32] [--extras arq.json]
                       [--so-cynthia] [--plano "texto do porquê"] [--pendencias base#q7,...] [--simular]

Passos: 1) propostas a partir de hp_propor (sem gravar) só para saber grupos/células do escopo;
2) hp_onda.py abrir --sem-branch --autor claude-v3 (contexto.md com IBGE); 3) plano.md;
4) propostas.json definitivo + extras; 5) hp_onda.py propostas (valida, gera onda.json);
6) decisoes.json pela ADR 0005 (revisor claude-ia); 7) hp_onda.py fechar (aplica e valida; se a validação
falhar, o estado é restaurado e a onda fica aberta).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import hp_propor
from hp_comum import dir_ondas, grava_json, grava_texto, hoje, le_json, slug

AQUI = Path(__file__).parent


def roda(*args) -> str:
    r = subprocess.run([sys.executable, str(AQUI / args[0]), *args[1:]], capture_output=True, text=True,
                       encoding="utf-8")
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0:
        print(out)
        sys.exit(f"ERRO em {args[0]} {args[1] if len(args) > 1 else ''}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--escopo", required=True)
    ap.add_argument("--n1", default="")
    ap.add_argument("--cynthia-folhas", default="")
    ap.add_argument("--so-cynthia", action="store_true", help="não usa o detector de outliers")
    ap.add_argument("--extras")
    ap.add_argument("--plano", default="")
    ap.add_argument("--pendencias", default="")
    ap.add_argument("--simular", action="store_true")
    a = ap.parse_args()

    n1s = {int(x) for x in a.n1.split(",") if x.strip()} if not a.so_cynthia else {-99}
    folhas = {x.strip() for x in a.cynthia_folhas.split(",") if x.strip()}
    extras = le_json(Path(a.extras))["propostas"] if a.extras else []
    onda = f"{hoje()}_claude-v3_{slug(a.escopo)}"
    P = hp_propor.propor(onda, n1s, extras, folhas, 40)
    if not P["propostas"]:
        print(f"{onda}: nenhuma proposta; onda não aberta.")
        return
    cels = sorted({c for p in P["propostas"] for m in p.get("movimentos", []) or [] for c in m["celulas"]}
                  | {c for p in P["propostas"] for c in p.get("celulas_analisadas", []) or []})
    import hp_comum
    est = hp_comum.carrega_estado()
    chave = est["depara"]["Ano"] + ":" + est["depara"]["Codigo"]
    grupos = sorted(set(est["depara"].loc[chave.isin(cels), "Cod_harmo"])
                    | {m["para"] for p in P["propostas"] for m in p.get("movimentos", []) or []})
    from collections import Counter
    t = Counter(p["tipo"] for p in P["propostas"])
    print(f"{onda}: {len(P['propostas'])} propostas {dict(t)} · {len(cels)} células · {len(grupos)} grupos")
    if a.simular:
        return
    if len(P["propostas"]) > 40:
        sys.exit("ERRO: mais de 40 propostas; divida o escopo (ONDAS.md).")

    roda("hp_onda.py", "abrir", "--escopo", a.escopo, "--tipo", "familia" if not folhas else "pendencia",
         "--grupos", ",".join(grupos), "--autor", "claude-v3", "--sem-branch",
         *(["--pendencias", a.pendencias] if a.pendencias else []))
    od = dir_ondas() / onda
    plano = (od / "plano.md").read_text(encoding="utf-8")
    plano = plano.replace("_preencher: sinal que motivou (alerta, pendência, balde), alternativas consideradas._",
                          a.plano or "Varredura da v3 (ADR 0005): células fora do lugar entre edições na família, "
                          "confirmadas por tradutor do IBGE e revisão manual quando houver.")
    plano = plano.replace("_preencher com o motivo dado pelo autor ao confirmar o escopo._",
                          "Arthur (WhatsApp, 2026-10-16): \"deixar o claudinho cantando, pedaço a pedaço, até passar por "
                          "tudo. Criar uma v3 da harmonização, dessa vez documentada.\" Tales escolheu o modo \"IA só "
                          "aplica o óbvio\" (ADR 0005). Escopo desta onda definido pela IA, por família de nível 1.")
    plano = plano.replace("_preencher antes de ler o contexto; confrontar no diagnóstico._",
                          f"1. Há células de uma edição só fora do grupo em que os mesmos produtos estão nas outras.\n"
                          f"2. Parte delas é erro de digitação/PROCV (sobretudo 2017) e parte é escolha de critério.\n\n"
                          f"## Diagnóstico (resumo da IA)\n\n{P['resumo']}\n")
    grava_texto(plano, od / "plano.md")
    P["onda"] = onda
    grava_json(P, od / "propostas.json")
    print(roda("hp_onda.py", "propostas", onda).strip().splitlines()[-2])
    grava_json(hp_propor.veredito_ia(onda), od / "decisoes.json")
    print(roda("hp_onda.py", "fechar", onda).strip().splitlines()[0])


if __name__ == "__main__":
    sys.exit(main())
