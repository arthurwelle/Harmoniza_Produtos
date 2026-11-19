"""Ondas de 2026-11-19: trazer para a v4 as edições que a Cynthia fez direto na planilha do Drive.

A planilha do Drive (TodosJuntos) foi editada depois da importação da base (commit 2807869): 372 células mudaram de
grupo, inclusive para a categoria nova 48. Animais (48001 Bens, 48002 Serviços). A v3 e a v4 foram feitas sobre a base e
não viam essas edições. `edicoes_drive_cynthia.csv` lista as 372 (item = primeiro item da célula).

Critério (ADR 0008): edição humana no Drive vale sobre decisão da IA. Onda 1 cria Animais com as células da Cynthia e
completa os dois anos que ela deixou vazios; onda 2 aplica as demais edições e desfaz os movimentos da v3/v4 que a
série da Cynthia contradiz.

Uso: python harmonizacao/fonte/v4/drive_cynthia.py  ->  drive_cynthia_2026-11-19.json (para hp_v4_onda.py)
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).parent
EST = AQUI.parent.parent / "estado"
HUMANO = ("Tales (2026-11-19), sobre as edições da Cynthia na planilha do Drive que a v4 não incorporava: \"show, vai\" "
          "(trazer para a v4 e para o pull request, para não perder o trabalho dela). ADR 0008.")

nomes = {r["Cod_harmo"]: r["nome"] for r in csv.DictReader(open(EST / "grupos.csv", encoding="utf-8"))}
ed = list(csv.DictReader(open(AQUI / "edicoes_drive_cynthia.csv", encoding="utf-8")))
aplicar = [r for r in ed if r["grupo_drive"] != r["grupo_v4_antes"]]


def lista(rs):
    return "; ".join(f"{r['celula']} {r['item']}" for r in rs)


# ------------------------------------------------------------------ onda 1: 48. Animais
bens = [r for r in aplicar if r["grupo_drive"] == "48001"]
serv = [r for r in aplicar if r["grupo_drive"] == "48002"]
COMPLETA_BENS = {"2002:95091": "ALIMENTOS DE CAES", "2002:95092": "ALPISTE / ALIMENTOS DE OUTROS ANIMAIS",
                 "2002:95093": "FRONTLINE / PRODUTOS DE LIMPEZA E HIGIENE DE ANIMAIS",
                 "2002:95094": "OBJETOS DE ANIMAIS (CORRENTE, COLEIRA, GAIOLA)",
                 "2002:95100": "RACAO PARA ANIMAIS NAO ESPECIFICADA",
                 "2008:16018": "COMPRA DE ANIMAL DOMESTICO"}
COMPLETA_SERV = {"1995:1640": "COMPRA E TRATAMENTO DE ANIMAIS DOMÉSTICOS"}
onda1 = {
    "escopo": "animais-drive-cynthia", "tipo": "taxonomia", "humano": HUMANO,
    "plano": "A Cynthia criou no Drive o nível 48. Animais (48001 Bens, 48002 Serviços) e passou para ele "
             f"{len(bens) + len(serv)} células, quase todas de 40006 Outras despesas diversas. O grupo não existe no "
             "repositório. Com as células dela, 48001 fica sem 2002 e 48002 sem 1995 (A01): os mesmos itens dessas "
             "edições ficaram fora (2002 quadro 95, igual ao quadro 95 de 1987 e 1995; 1995:1640, igual a 1987:1640 e "
             "2002:16040). A onda cria os dois grupos com o código da planilha e completa os dois anos.",
    "propostas": [{
        "tipo": "CRIAR", "titulo": "48. Animais: 48001 Bens e 48002 Serviços, como na planilha do Drive",
        "movimentos": [{"celulas": [r["celula"] for r in bens] + list(COMPLETA_BENS), "para": "NOVO:bens"},
                       {"celulas": [r["celula"] for r in serv] + list(COMPLETA_SERV), "para": "NOVO:servicos"}],
        "novos_grupos": {
            "bens": {"nome": "Bens para animais", "nivel1": "48. Animais", "nivel2": "Animais",
                     "codigo_sugerido": "48001"},
            "servicos": {"nome": "Serviços para animais", "nivel1": "48. Animais", "nivel2": "Animais",
                         "codigo_sugerido": "48002"}},
        "confianca": "ALTA", "regras_ref": ["R2", "R6"],
        "evidencia": f"Edições da Cynthia no Drive: 48001 = {lista(bens)}. 48002 = {lista(serv)}. "
                     "Completados pela IA (mesmo item, mesmo quadro em outra edição): "
                     + "; ".join(f"{c} {d}" for c, d in {**COMPLETA_BENS, **COMPLETA_SERV}.items()) + ".",
        "motivo_ia": "Decisão humana (Cynthia) registrada na planilha; o repositório só a reproduz, com os mesmos "
                     "códigos. A IA acrescenta só as 7 células que deixariam um ano vazio ou separariam a compra de "
                     "animal de 2008 da de 2017 (48001). Inconsistências internas da classificação dela ficam como "
                     "estão para ela revisar (medicamento: 48001 em 2008, 48002 em 2017; compra: 48002 em "
                     "1987/2002, 48001 em 2017).",
        "pendencias_v3": []}]}

# ------------------------------------------------------------------ onda 2: demais edições + IA × Drive
por_dest = defaultdict(list)
for r in aplicar:
    if not r["grupo_drive"].startswith("48"):
        por_dest[r["grupo_drive"]].append(r)
P = []
for dest, rs in sorted(por_dest.items(), key=lambda kv: -len(kv[1])):
    origens = sorted({r["grupo_base"] for r in rs})
    contra = [r for r in rs if r["grupo_v4_antes"] != r["grupo_base"]]
    P.append({
        "tipo": "MOVER", "titulo": f"Edições da Cynthia no Drive para {dest} {nomes.get(dest, '')} ({len(rs)} células)",
        "movimentos": [{"celulas": [r["celula"] for r in rs], "para": dest}],
        "confianca": "ALTA", "regras_ref": ["R6"],
        "evidencia": f"Planilha do Drive (TodosJuntos), editada depois da base: de {', '.join(origens)} para {dest}. "
                     f"Células: {lista(rs)}."
                     + (f" A v4 tinha movido {lista(contra)} para {contra[0]['grupo_v4_antes']}." if contra else ""),
        "motivo_ia": "Revisão humana (Cynthia) aplicada na planilha e ainda não incorporada ao repositório; pela ADR "
                     "0008 a edição humana prevalece sobre a decisão da IA.",
        "pendencias_v3": []})

REV = [  # (células, para, revoga, título, motivo)
    (["2017:9014", "2017:9015", "2017:9016", "2017:9101", "2017:9102", "2017:9103", "2017:9104", "2017:9105",
      "2017:9106", "2017:9107", "2017:9108"], "32005", ["2026-10-16_claude-v4_nao-consumo-e-alugueis#p13"],
     "Aluguel de aparelhos de 2017 volta a 32005; revoga a decisão da v4",
     "A v4 pôs o aluguel de aparelhos em 40006 porque 1987-2008 estavam lá (4 edições contra 1). No Drive a Cynthia "
     "passou 1987-2008 para 32005; com isso a série inteira fica em 32005 e o motivo da v4 deixa de existir."),
    (["2017:38022"], "33004", [], "Óculos sem grau de 2017 voltam a 33004",
     "A Cynthia passou os óculos sem grau de 1987-2008 para 33004 no Drive; 2017 já estava em 33004 e a v4 o tirou "
     "(educacao#p02). A lente de contato colorida (2017:38034) continua em 40006, como nas outras edições."),
    (["2017:38041", "2017:38042", "2017:38043"], "33004", [], "Máscaras e porta-óculos de 2017 voltam a 33004",
     "Mesma situação: a Cynthia passou máscara de carnaval, máscara protetora e porta-óculos de 1987-2008 para 33004; "
     "a v3 tinha tirado 2017 de 33004 (educacao-despesas-diversas#p11)."),
    (["2017:32015"], "37005", [], "Calendário de 2017 volta a 37005",
     "A Cynthia passou o material de papelaria (inclusive calendário) para 37005; a v3 tinha tirado 2017 de 37005 "
     "(educacao-despesas-diversas#p13)."),
    (["2017:43049"], "38001", [], "Selo e cartão telefônico (hobby) de 2017 voltam a 38001",
     "A Cynthia passou selo (hobby) para 38001 no Drive; a v3 tinha tirado 2017 de 38001 "
     "(educacao-despesas-diversas#p15)."),
    (["2017:43044"], "38001", [], "Monóculo de 2017 volta a 38001",
     "A Cynthia passou o monóculo de 1987-2008 para 38001; a v4 tinha levado 2017 para 38005 "
     "(recreacao-e-telefonia#p05)."),
    (["2008:38069"], "39001", [], "Cigarreira de 2008 volta a 39001",
     "A Cynthia passou cachimbo, cigarreira e parafina de 1987-2008 para 39001 (Fumo); a v4 tinha tirado 2008 de 39001 "
     "(educacao#p09)."),
    (["2017:30023"], "35004", [], "Parafina de 2017 volta a 35004 (quadro de higiene)",
     "A v3 levou a parafina de 2017 para 40006 seguindo as outras edições; a Cynthia mudou as outras para 39001, mas a "
     "de 2017 está no quadro 30 (higiene pessoal, depilação), conceito diferente do quadro 40. Quadro antes de "
     "descrição: volta ao grupo da planilha."),
    (["2017:28004", "2017:28007", "2017:28040", "2017:28041"], "38005", [],
     "Feira de informática, couvert, forró, piscina e piquenique de 2017 voltam a 38005",
     "A Cynthia passou esses ingressos de 2002/2008 para 38005; a v3/v4 tinham levado 2017 para 38004 "
     "(recreacao-cultura#p10, recreacao-e-telefonia#p01). 2017:28044 e 28045 ficam em 38004."),
    (["2017:45020", "2017:45022", "2008:45017", "2008:45018"], "40003", [],
     "Festa junina e quermesse em 40003 (2008 e 2017)",
     "A Cynthia passou festa junina e quermesse de 2002 para 40003; 2017 estava em 40003 na planilha e a v3 o tinha "
     "levado para 38004 (recreacao-cultura#p11). 2008 acompanha a série (2 edições + revisão humana)."),
    (["2008:49048", "1995:4948"], "37004", [], "Software de curso em 37004 (1995 e 2008)",
     "A Cynthia passou o software de curso de 2002 para 37004 (livros e revistas técnicas); a v4 tinha levado 2008 "
     "para 37003 seguindo 1995/2002. 1995 e 2008 acompanham a escolha dela."),
]
for cels, para, rev, tit, mot in REV:
    P.append({"tipo": "MOVER", "titulo": "IA × Drive: " + tit, "movimentos": [{"celulas": cels, "para": para}],
              "revoga": rev, "confianca": "ALTA", "regras_ref": ["R6", "R7"] if rev else ["R6"],
              "evidencia": "Ver edicoes_drive_cynthia.csv (mesmo item nas outras edições).", "motivo_ia": mot,
              "pendencias_v3": []})
onda2 = {
    "escopo": "edicoes-drive-cynthia", "tipo": "familia", "humano": HUMANO,
    "plano": f"Das 372 células editadas pela Cynthia no Drive, {len(ed) - len(aplicar)} já batiam com a v4. Esta onda "
             f"aplica as {sum(len(v) for v in por_dest.values())} restantes fora de Animais (uma delas, 2008:28047, a "
             "v4 tinha movido para outro grupo) e desfaz os movimentos da v3/v4 que a série dela contradiz.",
    "propostas": P}

# ------------------------------------------------------------------ onda 3: aplicação parcial no Drive
onda3 = {
    "escopo": "parciais-drive-cynthia", "tipo": "familia", "humano": HUMANO,
    "plano": "Depois das ondas 1 e 2, a comparação com a revisão em PDF mostrou um caso de aplicação parcial: a folha "
             "38 #12 manda piscina em parque e taxa de piquenique de 38004 para 38005 em todas as edições; no Drive a "
             "Cynthia mudou 2002 piquenique e 2008 piscina, mas não os pares, e a série ficou alternando.",
    "propostas": [{
        "tipo": "MOVER", "titulo": "Piscina em parque e piquenique em 38005 em todas as edições (completa a folha 38 #12)",
        "movimentos": [{"celulas": ["1995:2830", "1995:2834", "2002:28034", "2008:28030"], "para": "38005"}],
        "confianca": "ALTA", "regras_ref": ["R6"],
        "evidencia": "Revisão Cynthia folha 38 #12 (maturação 38004 -> 38005: piquenique 1995/2002/2008, piscina). No "
                     "Drive: 2002:28030 piquenique e 2008:28034 piscina já em 38005; 2017:28040/28041 em 38005.",
        "motivo_ia": "Completa a decisão humana que ficou aplicada pela metade; sem isso o mesmo item alterna de grupo "
                     "entre edições.",
        "pendencias_v3": []}]}

json.dump({"ondas": [onda1, onda2, onda3]}, open(AQUI / "drive_cynthia_2026-11-19.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"onda 1: {sum(len(m['celulas']) for m in onda1['propostas'][0]['movimentos'])} células; "
      f"onda 2: {len(P)} propostas, {sum(len(m['celulas']) for p in P for m in p['movimentos'])} células")
