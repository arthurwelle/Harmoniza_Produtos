"""Auditoria mecânica do estado e do ledger. Roda em todo PR (CI).

Uso:
  python hp_validar.py [--detalhe] [--saida arq.md]

Sai com código 1 se houver ERRO (bloqueante). ALERTA e INFO não bloqueiam.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

from hp_comum import (ANOS, COLS_DECISOES, TIPOS_DECISAO, TIPOS_REGRA, VEREDITOS,
                      ausencias_justificadas, carrega_decisoes_todas, carrega_estado, cod5,
                      dir_h, grava_texto, matriz_cobertura, parse_cel, separa, txt_movimentos)


class Achados:
    def __init__(self):
        self.itens: list[tuple[str, str, str, list[str]]] = []

    def add(self, nivel: str, codigo: str, msg: str, exemplos=None):
        self.itens.append((nivel, codigo, msg, list(exemplos or [])))

    @property
    def erros(self):
        return [i for i in self.itens if i[0] == "ERRO"]

    def md(self, detalhe: bool) -> str:
        if not self.itens:
            return "# Validação\n\nNenhum achado.\n"
        ordem = {"ERRO": 0, "ALERTA": 1, "INFO": 2}
        out = ["# Validação", f"ERRO: {len(self.erros)} | "
               f"ALERTA: {sum(i[0] == 'ALERTA' for i in self.itens)} | "
               f"INFO: {sum(i[0] == 'INFO' for i in self.itens)}", ""]
        for nivel, cod, msg, ex in sorted(self.itens, key=lambda i: (ordem[i[0]], i[1])):
            out.append(f"- **{nivel} {cod}** {msg}")
            if ex:
                mostra = ex if detalhe else ex[:8]
                out.append("  - " + ", ".join(mostra) + (" …" if len(ex) > len(mostra) else ""))
        return "\n".join(out) + "\n"


def valida_estado(est: dict, A: Achados) -> dict[str, str]:
    dep, grp, reg = est["depara"], est["grupos"], est["regras"]

    fora = sorted(set(dep["Ano"]) - set(ANOS))
    if fora:
        A.add("ERRO", "E05", f"Anos fora de {ANOS} no de-para", fora)

    vazios = dep[(dep["Cod_harmo"] == "") | (dep["Codigo"] == "")]
    if len(vazios):
        A.add("ERRO", "E00", f"{len(vazios)} linhas sem Codigo ou Cod_harmo",
              [f"{r.Ano}:{r.Codigo}" for r in vazios.itertuples()])

    multi = dep.groupby(["Ano", "Codigo"])["Cod_harmo"].nunique()
    multi = multi[multi > 1]
    if len(multi):
        A.add("ERRO", "E01", f"{len(multi)} células com mais de um Cod_harmo (itens inseparáveis "
              "separados)", [f"{a}:{c}" for a, c in multi.index])

    if grp["Cod_harmo"].duplicated().any():
        A.add("ERRO", "E04", "Cod_harmo repetido em grupos.csv (código criado em duas ondas?)",
              sorted(set(grp.loc[grp["Cod_harmo"].duplicated(), "Cod_harmo"])))
    ruins = grp.loc[~grp["Cod_harmo"].str.fullmatch(r"\d{5}"), "Cod_harmo"]
    if len(ruins):
        A.add("ERRO", "E04", "Cod_harmo fora do formato 5 dígitos em grupos.csv", list(ruins))

    status = dict(zip(grp["Cod_harmo"], grp["status"]))
    usados = set(dep["Cod_harmo"])
    sem = sorted(usados - set(status))
    if sem:
        A.add("ERRO", "E02", "Cod_harmo usado no de-para mas ausente de grupos.csv", sem)
    ext = sorted(g for g in usados if status.get(g) == "extinto")
    if ext:
        A.add("ERRO", "E03", "Grupo extinto ainda recebe células", ext)

    m = matriz_cobertura(dep, grp)
    ativos = set(grp.loc[grp["status"] == "ativo", "Cod_harmo"])
    m_at = m.loc[m.index.isin(ativos)]
    orfaos = list(m_at.index[m_at.sum(axis=1) == 0])
    if orfaos:
        A.add("ALERTA", "A02", "Grupo ativo sem nenhuma célula (extinguir ou povoar)", orfaos)

    ok = ausencias_justificadas(reg)
    nj = [f"{g}[{','.join(a for a in ANOS if r[a] == 0 and (g, a) not in ok)}]"
          for g, r in m_at.iterrows()
          if any(r[a] == 0 and (g, a) not in ok for a in ANOS) and r.sum() > 0]
    if nj:
        A.add("ALERTA", "A01", f"{len(nj)} grupos com ano vazio sem regra de ausência estrutural (R4)", nj)

    obsoletas = sorted({f"{g}:{a}" for g, a in ok if g in m.index and m.loc[g, a] > 0})
    if obsoletas:
        A.add("ALERTA", "A04", "Regra de ausência estrutural, mas o grupo tem células no ano", obsoletas)

    nd = int(dep.duplicated().sum())
    if nd:
        A.add("ALERTA", "A03", f"{nd} linhas duplicadas exatas no de-para")

    grupo_cel = dict(zip(dep["Ano"] + ":" + dep["Codigo"], dep["Cod_harmo"]))

    for r in reg.itertuples():
        if r.tipo not in TIPOS_REGRA:
            A.add("ERRO", "E11", f"Regra {r.id} com tipo inválido '{r.tipo}'")
        if r.status != "ativa":
            continue
        cels = separa(r.celulas)
        faltam = [c for c in cels if c not in grupo_cel]
        if faltam:
            A.add("ALERTA", "A05", f"Regra {r.id} cita células inexistentes", faltam)
        gs = {grupo_cel[c] for c in cels if c in grupo_cel}
        if r.tipo == "inseparavel" and len(gs) > 1:
            A.add("ERRO", "E07", f"Regra {r.id} (inseparável) violada: células em grupos {sorted(gs)}",
                  cels)
        if r.tipo == "manter_separado" and len(cels) > 1 and len(gs) == 1:
            A.add("ERRO", "E08", f"Regra {r.id} (manter separado) violada: tudo em {gs.pop()}", cels)

    abertas = est["pendencias"]
    n_ab = int((abertas["status"].isin(["aberta", "em_onda"])).sum()) if len(abertas) else 0
    if n_ab:
        A.add("INFO", "I01", f"{n_ab} pendências abertas/em onda")
    return grupo_cel


def valida_ledger(grupo_cel: dict[str, str], A: Achados) -> None:
    dec = carrega_decisoes_todas()
    if dec.empty:
        A.add("INFO", "I02", "Nenhuma decisão registrada ainda")
        return

    if dec["id"].duplicated().any():
        A.add("ERRO", "E10", "Id de decisão repetido", sorted(set(dec.loc[dec["id"].duplicated(), "id"])))
    ruins = dec[~dec["tipo"].isin(TIPOS_DECISAO)]
    if len(ruins):
        A.add("ERRO", "E10", "Tipo de decisão inválido", list(ruins["id"]))
    ruins = dec[~dec["veredito"].isin(VEREDITOS)]
    if len(ruins):
        A.add("ERRO", "E10", "Veredito inválido", list(ruins["id"]))
    sem_motivo = dec[(dec["veredito"].isin(["rejeitada", "modificada", "adiada"]))
                     & (dec["motivo_humano"].str.strip() == "")]
    if len(sem_motivo):
        A.add("ERRO", "E10", "Veredito sem motivo humano (obrigatório exceto 'aceita')",
              list(sem_motivo["id"]))

    # E06: última decisão aplicada sobre cada célula precisa estar refletida no de-para
    esperado: dict[str, tuple[str, str]] = {}
    aplicadas = dec[dec["veredito"].isin(["aceita", "modificada"])].sort_values(["onda", "_ordem"])
    for r in aplicadas.itertuples():
        for mov in txt_movimentos(r.movimentos):
            for c in mov["celulas"]:
                esperado[c] = (mov["para"], r.id)
    div = [f"{c} (esperado {para} por {did}, está {grupo_cel.get(c, 'inexistente')})"
           for c, (para, did) in esperado.items() if grupo_cel.get(c) != para]
    if div:
        A.add("ERRO", "E06", "Decisão aceita não refletida no de-para", div)

    # E09: decisão estrutural aplicada precisa de ADR citando a onda ou o id
    adr_txt = "\n".join(p.read_text(encoding="utf-8") for p in (dir_h() / "adr").glob("*.md"))
    estr = aplicadas[aplicadas["estrutural"].str.lower().isin(["true", "1", "sim"])]
    sem_adr = [r.id for r in estr.itertuples() if r.id not in adr_txt and r.onda not in adr_txt]
    if sem_adr:
        A.add("ERRO", "E09", "Decisão estrutural aplicada sem ADR em harmonizacao/adr/", sem_adr)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--detalhe", action="store_true", help="listar todos os exemplos")
    p.add_argument("--saida")
    a = p.parse_args()
    A = Achados()
    est = carrega_estado()
    grupo_cel = valida_estado(est, A)
    valida_ledger(grupo_cel, A)
    txt = A.md(a.detalhe)
    if a.saida:
        grava_texto(txt, Path(a.saida))
    print(txt)
    sys.exit(1 if A.erros else 0)


if __name__ == "__main__":
    main()
