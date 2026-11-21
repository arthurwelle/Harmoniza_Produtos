"""Monta propostas.json de uma onda a partir das evidências (ADR 0005 e 0006).

Uso:
  python hp_propor.py ONDA --n1 32,31 [--extras extras.json] [--cynthia-folhas 32] [--max 40]
  python hp_propor.py ONDA --veredito-ia      # escreve decisoes.json segundo a ADR 0005

Fontes:
  - hp_outliers.detecta: células fora do lugar entre edições (destino com nível 1 em --n1).
  - fonte/revisoes_cynthia_celulas.csv: ações da revisão manual (segunda fonte; pendências humanas).
  - hp_ibge: grande grupo/linha do tradutor oficial (2008/2017).
  - --extras: propostas escritas pela IA para a onda (JSON com a lista "propostas", mesmo schema do LEDGER).

Classificação (ADR 0005):
  aplicar  = (≥3 outras edições e IBGE não contra) ou (2 edições e IBGE ou Cynthia confirmam) → MOVER, ALTA
  revisar  = 2 edições sem segunda fonte; IBGE contra; ações da Cynthia que não coincidem → REVISAR
  MANTER   = ações da Cynthia já refletidas no estado atual (célula já no destino)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict

import pandas as pd

import hp_outliers
from hp_comum import carrega_estado, celulas_df, dir_h, dir_ondas, grava_json, le_csv, le_json, agora

REVISOR_IA = "claude-ia (ADR 0005)"


def n1_num(s: str) -> int:
    m = re.match(r"\s*(\d+)", s or "")
    return int(m.group(1)) if m else -1


def carrega_cynthia() -> pd.DataFrame:
    p = dir_h() / "fonte" / "revisoes_cynthia_celulas.csv"
    return le_csv(p) if p.exists() else pd.DataFrame()


def evid_celula(r, cyn_txt: str) -> str:
    s = f"{r['cel']} [{r['itens'][:140]}]: nas outras edições ({r['anos_x'].replace(';', ', ')}) os mesmos itens estão em {r['para']}"
    if r.get("ibge"):
        s += f"; IBGE: {r['ibge']} ({'confirma o destino' if r['ibge_concorda'] == 'sim' else 'contra o destino' if r['ibge_concorda'] == 'nao' else 'neutro'})"
    if cyn_txt:
        s += f"; revisão manual: {cyn_txt}"
    return s


def propor(onda: str, n1s: set[int], extras: list[dict], folhas_cyn: set[str], maxp: int) -> dict:
    est = carrega_estado()
    nomes = dict(zip(est["grupos"]["Cod_harmo"], est["grupos"]["nome"]))
    o = hp_outliers.detecta(est)
    if o.empty:
        o = pd.DataFrame(columns=["cel", "ano", "codigo", "quadro", "de", "para", "n1_de", "n1_para", "conceito",
                                  "n_itens", "n_hist", "n_outros", "anos_x", "itens", "ibge", "ibge_concorda",
                                  "muda_dominio"])
    o = o[o["n1_para"].map(n1_num).isin(n1s) & (o["conceito"] != "fora")].copy()
    cyn = carrega_cynthia()
    cyn_por_cel = defaultdict(list)
    if len(cyn):
        for r in cyn.itertuples():
            for c in filter(None, r.celulas.split(";")):
                cyn_por_cel[c].append(r)
    def cyn_confirma(cel, para):
        return [r for r in cyn_por_cel.get(cel, []) if r.para == para]
    o["cyn"] = [cyn_confirma(c, p) for c, p in zip(o["cel"], o["para"])]
    # ADR 0005; mudar de domínio (consumo/outras/rendimentos/inventário) só com o IBGE confirmando
    o["classe"] = ["ibge_contra" if i == "nao"
                   else ("dominio" if md and i != "sim"
                         else ("aplicar" if (int(n) >= 3) or (int(n) == 2 and (i == "sim" or len(cy) > 0)) else "revisar"))
                   for n, i, cy, md in zip(o["n_outros"], o["ibge_concorda"].fillna(""), o["cyn"], o["muda_dominio"])]
    props, k = [], 0
    def novo_id():
        nonlocal k
        k += 1
        return f"p{k:02d}"
    usados = set()
    # MOVER óbvios
    for (ano, de, para), sub in o[o["classe"] == "aplicar"].groupby(["ano", "de", "para"]):
        cels = list(sub["cel"])
        usados.update(cels)
        evs = [evid_celula(r, "; ".join(f"folha {c.folha} #{c.n} ({c.tipo})" for c in r["cyn"])) for _, r in sub.iterrows()]
        n_out = sub["n_outros"].astype(int).min()
        fontes = []
        if (sub["ibge_concorda"] == "sim").any():
            fontes.append("tradutor do IBGE")
        if sub["cyn"].map(len).sum():
            fontes.append("revisão manual da Cynthia")
        props.append({
            "id": novo_id(), "tipo": "MOVER",
            "titulo": f"{ano}: {de} {nomes.get(de, '')[:30]} → {para} {nomes.get(para, '')[:30]} ({len(cels)} célula{'s' if len(cels) > 1 else ''})",
            "movimentos": [{"celulas": cels, "para": para}], "novos_grupos": {}, "regra_nova": None, "revoga": [],
            "confianca": "ALTA", "regras_ref": ["R4", "R6", "R8"],
            "evidencia": " || ".join(evs) + (f" || Segunda fonte: {', '.join(fontes)}." if fontes else ""),
            "motivo_ia": (f"Outlier pontual: os mesmos produtos estão em {para} em todas as outras edições em que aparecem "
                          f"(pelo menos {n_out}); só em {ano} a célula está em {de}, sem nenhum item desse grupo em outro ano. "
                          f"Mover a célula inteira respeita a R1 (todos os itens com histórico apontam para {para}) e "
                          f"recompõe a série do grupo (R4/R6). Critério de óbvio da ADR 0005."),
            "conflito": None,
            "impacto": f"{len(cels)} célula(s) saem de {de} e entram em {para} em {ano}; nenhum grupo novo, nenhuma distinção criada.",
            "pendencias": []})
    # REVISAR: 2 edições sem segunda fonte / IBGE contra
    for classe, titulo_c, motivo_c in [
        ("revisar", "só 2 edições", "Os mesmos produtos estão em {para} nas duas outras edições em que aparecem; em {ano} estão em {de}. Duas edições contra uma, sem segunda fonte (IBGE neutro ou ausente, sem revisão manual): pela ADR 0005 não é óbvio. Recomendação da IA: mover, salvo razão de conceito."),
        ("dominio", "muda de conceito", "Os mesmos nomes de produto estão em {para} nas outras edições, mas a célula está em {de}, de outro domínio (consumo, outras despesas, rendimentos ou inventário). Mesmo nome não garante mesma despesa (ex.: item de inventário de bens duráveis × compra; 'empregado' como rendimento × serviço doméstico). Sem confirmação do IBGE, a decisão é humana."),
        ("ibge_contra", "IBGE contra", "As outras edições põem os mesmos produtos em {para}, mas o tradutor do IBGE confirma o grupo atual ({de}) em {ano}. Fontes discordantes (CONSTITUICAO, hierarquia de evidência): decidir qual convenção vale para a série.")]:
        for (de, para), sub in o[o["classe"] == classe].groupby(["de", "para"]):
            cels = list(sub["cel"])
            usados.update(cels)
            evs = [evid_celula(r, "") for _, r in sub.iterrows()]
            anos = ", ".join(sorted(sub["ano"].unique()))
            props.append({
                "id": novo_id(), "tipo": "REVISAR",
                "titulo": f"{titulo_c}: {de} {nomes.get(de, '')[:30]} → {para} {nomes.get(para, '')[:30]} ({anos})",
                "movimentos": [], "celulas_analisadas": cels, "confianca": "MEDIA", "regras_ref": ["R4", "R6", "R8"],
                "evidencia": " || ".join(evs),
                "motivo_ia": motivo_c.format(para=para, de=de, ano=anos),
                "conflito": None, "impacto": f"Se aceito como MOVER: {len(cels)} célula(s) de {de} para {para}.", "pendencias": []})
    # Cynthia: ações das folhas da onda que não viraram MOVER
    if len(cyn) and folhas_cyn:
        pa = dir_h() / "fonte" / "revisoes_cynthia.csv"
        acs = le_csv(pa) if pa.exists() else pd.DataFrame(columns=["folha", "n", "texto", "acao"])
        textos = {(r.folha, r.n): r.texto for r in acs.itertuples()}
        acoes_txt = {(r.folha, r.n): r.acao for r in acs.itertuples()}
        sub = cyn[cyn["folha"].isin(folhas_cyn)]
        for (folha, n), a in sub.groupby(["folha", "n"], sort=False):
            r0 = a.iloc[0]
            cels = sorted({c for cs in a["celulas"] for c in cs.split(";") if c})
            if cels and all(c in usados for c in cels):
                continue
            ja = [c for c in cels if est["depara"].loc[(est["depara"]["Ano"] + ":" + est["depara"]["Codigo"]) == c, "Cod_harmo"].iloc[0] == r0["para"]] if cels else []
            itens = "; ".join(f"{x.item} ({x.ano})" for x in a.itertuples())
            if cels and len(ja) == len(cels):
                props.append({
                    "id": novo_id(), "tipo": "MANTER", "titulo": f"Cynthia folha {folha} #{n}: já aplicada no repositório",
                    "movimentos": [], "celulas_analisadas": cels, "confianca": "ALTA", "regras_ref": ["R7"],
                    "evidencia": f"Ação: {r0['tipo']} {r0['de']} → {r0['para']}. Itens: {itens}.",
                    "motivo_ia": "As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar.",
                    "conflito": None, "impacto": "nenhum", "pendencias": []})
                continue
            cels_fora = [c for c in cels if c not in usados and c not in ja]
            motivo = {"Outlier pontual": "A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1). Precisa olhar a célula inteira.",
                      "Maturação de taxonomia": "A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana.",
                      "Resíduo/analogia": "A revisão manual move por analogia com itens parecidos, sem o mesmo produto em outras edições. Evidência de nível 5 (descrição): decisão humana.",
                      "Confirmação direta": "A revisão manual confirma o destino; o detector não pegou a célula por diferença de grafia ou por célula heterogênea.",
                      "Dúvida em aberto": "A própria revisão manual deixou a questão em aberto."}.get(r0["tipo"], "Ação da revisão manual sem tipo identificado; decisão humana.")
            props.append({
                "id": novo_id(), "tipo": "REVISAR",
                "titulo": f"Cynthia folha {folha} #{n} ({r0['tipo'] or 'sem tipo'}): {r0['de']} → {r0['para']}",
                "movimentos": [], "celulas_analisadas": cels_fora, "confianca": "MEDIA", "regras_ref": ["R6", "R7"],
                "evidencia": f"Ação: {acoes_txt.get((folha, n), '')[:200]}. Itens: {itens}. Células achadas no estado atual: {', '.join(cels) or 'nenhuma (grafia diferente)'}; já no destino: {', '.join(ja) or 'nenhuma'}. Texto da revisão: {textos.get((folha, n), '')[:700]}",
                "motivo_ia": motivo, "conflito": None,
                "impacto": f"Se aceito: {len(cels_fora)} célula(s) de {r0['de']} para {r0['para']}.", "pendencias": []})
    for e in extras:
        e = dict(e)
        e["id"] = novo_id()
        props.append(e)
    if len(props) > maxp:
        print(f"AVISO: {len(props)} propostas > {maxp}; dividir a onda (ONDAS.md).")
    resumo = (f"Onda da v3 (ADR 0005): {sum(p['tipo'] == 'MOVER' for p in props)} MOVER óbvios "
              f"({sum(len(m['celulas']) for p in props for m in p.get('movimentos', []))} células), "
              f"{sum(p['tipo'] == 'REVISAR' for p in props)} REVISAR e {sum(p['tipo'] == 'MANTER' for p in props)} MANTER. "
              f"Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.")
    return {"onda": onda, "autor_ia": "claude-opus-5-5", "resumo": resumo, "propostas": props}


def veredito_ia(onda: str) -> dict:
    P = le_json(dir_ondas() / onda / "propostas.json")
    dec = {}
    for p in P["propostas"]:
        estrut = p["tipo"] in {"UNIR", "DIVIDIR", "CRIAR", "REGRA"}
        conf = (p.get("confianca") or "").upper().replace("É", "E")
        if p["tipo"] in {"MOVER", "RENOMEAR"} and conf == "ALTA" and not estrut:
            v, m = "aceita", ""
        elif p["tipo"] in {"REVISAR", "MANTER"}:
            v, m = "aceita", ""
        else:
            v, m = "adiada", "ADR 0005: proposta estrutural ou sem confiança ALTA; fica para decisão humana."
        dec[p["id"]] = {"veredito": v, "motivo": m, "revisor": REVISOR_IA, "ts": agora(), "movimentos": None}
    return {"onda": onda, "modo": "ia-adr-0005", "decisoes": dec}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("onda")
    ap.add_argument("--n1", default="")
    ap.add_argument("--extras")
    ap.add_argument("--cynthia-folhas", default="")
    ap.add_argument("--max", type=int, default=40)
    ap.add_argument("--veredito-ia", action="store_true")
    a = ap.parse_args()
    od = dir_ondas() / a.onda
    if a.veredito_ia:
        D = veredito_ia(a.onda)
        grava_json(D, od / "decisoes.json")
        from collections import Counter
        print("OK decisoes.json", dict(Counter(d["veredito"] for d in D["decisoes"].values())))
        return
    n1s = {int(x) for x in a.n1.split(",") if x.strip()}
    extras = le_json(od / a.extras)["propostas"] if a.extras else []
    folhas = {x.strip() for x in a.cynthia_folhas.split(",") if x.strip()}
    P = propor(a.onda, n1s, extras, folhas, a.max)
    grava_json(P, od / "propostas.json")
    from collections import Counter
    print(f"OK {len(P['propostas'])} propostas {dict(Counter(p['tipo'] for p in P['propostas']))}")


if __name__ == "__main__":
    sys.exit(main())
