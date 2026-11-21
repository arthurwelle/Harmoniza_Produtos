"""Importa respostas do Google Form (site antigo) como pendências. Idempotente.

Uso:
  python hp_form.py [--sugestoes URL_OU_CSV] [--execucoes URL_OU_CSV] [--incluir-testes]

Nada é aplicado ao de-para: cada sugestão vira pendência origem=Form, a ser analisada numa onda.
Id estável por sugestão (hash de data+ação+itens) ⇒ rodar de novo só acrescenta as novas.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import urllib.request
from datetime import datetime, timedelta, timezone

import pandas as pd

from hp_comum import (COLS_PENDENCIAS, carrega_estado, cod5, dir_estado, grava_csv, hoje, junta, limpa)

URL_SUG = "https://docs.google.com/spreadsheets/d/1JDqb5SYAwx3oB4rfB3hVBRKxrWwNtb1tCkBGYddRE10/export?format=csv"
URL_EXE = "https://docs.google.com/spreadsheets/d/11FhuDDvhE33E7E-c_qsdmAD7AeCGkMo8duxG2My4WnE/export?format=csv"


def le(fonte: str) -> pd.DataFrame:
    if fonte.startswith("http"):
        with urllib.request.urlopen(fonte, timeout=60) as r:
            fonte = io.StringIO(r.read().decode("utf-8"))
    return pd.read_csv(fonte, dtype=str, keep_default_na=False)


def col(df: pd.DataFrame, *nomes: str) -> str:
    alvo = {n.lower().replace("_", " ").replace(".", " ") for n in nomes}
    for c in df.columns:
        if c.lower().replace("_", " ").replace(".", " ").strip() in alvo:
            return c
    return ""


def ts_utc(s: str):
    s = limpa(s)
    for fmt in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone(timedelta(hours=-3))).astimezone(timezone.utc)
        except ValueError:
            pass
    try:
        t = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sugestoes", default=URL_SUG)
    p.add_argument("--execucoes", default=URL_EXE)
    p.add_argument("--incluir-testes", action="store_true")
    p.add_argument("--marcar-aplicadas", action="store_true",
                   help="base importada do master do Drive: sugestões já aplicadas lá entram como resolvidas")
    a = p.parse_args()

    sug = le(a.sugestoes)
    try:
        exe = le(a.execucoes)
        c_corte = col(exe, "Timestamp corte")
        cortes = [t for t in (ts_utc(x) for x in exe[c_corte]) if t] if c_corte else []
        corte = max(cortes) if cortes else None
    except Exception as e:  # execuções são só informativas
        print(f"AVISO: não li execuções ({e})")
        corte = None

    c_ts, c_acao = sug.columns[0], col(sug, "Acao")
    c_alvo, c_nome = col(sug, "Codigo-alvo"), col(sug, "Nome novo")
    c_n1, c_n2 = col(sug, "Nivel 1"), col(sug, "Nivel 2")
    c_itens, c_com = col(sug, "Itens JSON"), col(sug, "Comentario")

    est = carrega_estado()
    pen = est["pendencias"]
    existentes = set(pen["id"])
    cels_ok = set(est["depara"]["Ano"] + ":" + est["depara"]["Codigo"])
    novas, testes, repetidas = [], 0, 0
    for _, r in sug.iterrows():
        com = limpa(r.get(c_com, ""))
        if "TESTE" in com and not a.incluir_testes:
            testes += 1
            continue
        try:
            itens = json.loads(r.get(c_itens, "") or "[]")
        except json.JSONDecodeError:
            itens = []
        cels = list(dict.fromkeys(f"{limpa(x[0])}:{limpa(x[1])}" for x in itens if len(x) >= 2))
        h = hashlib.sha1(f"{r[c_ts]}|{r[c_acao]}|{r.get(c_itens, '')}".encode()).hexdigest()[:8]
        pid = f"form#{h}"
        if pid in existentes:
            repetidas += 1
            continue
        existentes.add(pid)
        t = ts_utc(r[c_ts])
        aplicada = "já aplicada no master do Drive (não na v2026 local)" if (t and corte and t <= corte) \
            else "não aplicada no Drive"
        alvo = cod5(r.get(c_alvo, ""))
        inexist = [c for c in cels if c not in cels_ok]
        partes = [f"Form {r[c_ts]}: {limpa(r[c_acao]).upper()}",
                  f"→ {alvo}" if alvo else "", f"nome '{limpa(r.get(c_nome, ''))}'" if limpa(r.get(c_nome, "")) else "",
                  f"N1 '{limpa(r.get(c_n1, ''))}' N2 '{limpa(r.get(c_n2, ''))}'" if limpa(r.get(c_n1, "")) else "",
                  f"{len(cels)} células", f"comentário do revisor: \"{com}\"" if com else "sem comentário",
                  aplicada, f"células inexistentes no de-para: {inexist}" if inexist else ""]
        ja_na_base = a.marcar_aplicadas and aplicada.startswith("já aplicada")
        novas.append({"id": pid, "data": hoje(), "origem": "Form", "descricao": " | ".join(x for x in partes if x),
                      "celulas": junta(cels), "grupos": alvo, "onda_alvo": "",
                      "status": "resolvida" if ja_na_base else "aberta",
                      "resolvida_em": "base (aplicada no master do Drive antes da importação)" if ja_na_base else ""})
    if novas:
        pen = pd.concat([pen, pd.DataFrame(novas)], ignore_index=True)
        grava_csv(pen, dir_estado() / "pendencias.csv", COLS_PENDENCIAS)
    print(f"OK {len(novas)} pendências novas do Form · {repetidas} já importadas · {testes} testes ignorados")


if __name__ == "__main__":
    main()
