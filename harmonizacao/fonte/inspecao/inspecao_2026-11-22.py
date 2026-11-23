"""Inspeção geral de 2026-11-22 (Tales + IA): problemas que ainda existem na harmonização da main (ac864e8).

Método (detalhes em harmonizacao/INSPECAO_2026-11-22.md):
  1. Gasto ponderado por célula (Ano:Codigo) a partir dos microdados, mesmo cálculo de valores/gerar_valores.py
     (confere com data/valores/valores.csv em todas as 2.335 combinações grupo × edição × recorte).
  2. Séries por grupo: picos isolados, quebras 2002→2008 e grupos que somem.
  3. Comparação célula a célula entre edições vizinhas, pelo nome dos itens: alimentos só dentro da caderneta
     (quadros 63+), o resto só dentro do mesmo quadro; ordenada pelo valor (p.p. do consumo, regiões metropolitanas).
  4. Cada candidata conferida na série das cinco edições antes de virar proposta.

Gera inspecao_2026-11-22.json (ondas para o runner) com as propostas MOVER (erros com evidência) e REVISAR
(critério para o grupo decidir). Os p.p. citados são da despesa de consumo das regiões metropolitanas.
"""
from __future__ import annotations

import json
from pathlib import Path

AQUI = Path(__file__).parent
HUMANO = ("Arthur (2026-11-21), sobre a inspeção geral pedida pelo Tales: \"pode. o ponto é, inspeção do passado o "
          "ganho é pouco. tem que tentar atacar os problemas ainda existentes, nem que seja listá-los\". Tales: "
          "\"mete marcha\".")


def mover(titulo, movs, evid, motivo, conf="ALTA", regras=("R6",)):
    return {"tipo": "MOVER", "titulo": titulo, "movimentos": [{"celulas": c, "para": p} for c, p in movs],
            "confianca": conf, "regras_ref": list(regras), "evidencia": evid, "motivo_ia": motivo,
            "pendencias_v3": []}


def revisar(titulo, cels, evid, motivo):
    return {"tipo": "REVISAR", "titulo": titulo, "movimentos": [], "celulas_analisadas": cels, "confianca": "MEDIA",
            "regras_ref": ["R6"], "evidencia": evid, "motivo_ia": motivo, "pendencias_v3": []}


P = []
# ---------------------------------------------------------------- caderneta de 2008, herdada por 2017
P.append(mover(
    "Leite de vaca integral/pasteurizado de 2008 e 2017 em 11104 (estava em 11103 Leite fresco)",
    [(["2008:79001", "2008:79043", "2017:79001", "2017:79043"], "11104")],
    "2008:79001 'LEITE DE VACA INTEGRAL / LEITE DE VACA PASTEURIZADO INTEGRAL / LEITE ESTERILIZADO...' vale 0,44 p.p. "
    "em 2008 e 0,24 em 2017 e está em 11103 Leite de vaca fresco, ao lado de 2008:79002 'LEITE DA ROCA / IN NATURA' "
    "(0,008). Em 2002 o leite pasteurizado (2002:91051) está em 11104 e o fresco (91052) em 11103. Série de 11104: "
    "1,31 / 0,96 / 0,66 / 0,075 / 0,052; de 11103: 0,035 / 0,020 / 0,014 / 0,45 / 0,24.",
    "Erro de código na caderneta de 2008 (copiado em 2017): a quebra 2002→2008 das duas séries é a mesma célula. "
    "79043 é a versão orgânica do mesmo item."))
P.append(mover(
    "Linguiça de 2008 e 2017 em 07601 (estava em 07208 carne bovina e 07503 salsicha)",
    [(["2008:81022", "2017:81022", "2008:81053", "2017:81053"], "07601")],
    "2008:81022 'LINGUICA CALABRESA / LINGUICA BOVINA / LINGUICA DE FRANGO...' (0,15 p.p. em 2008, 0,14 em 2017) "
    "está em 07208 Outros (capa de filé); 81053 é a linguiça light, em 07503 Salsicha. 1987-2002 têm a linguiça em "
    "07601 (0,18 / 0,15 / 0,16 p.p.); em 2008 e 2017 07601 cai para 0,014.",
    "Mesmo item, mesmo conceito de quadro (carnes no varejo); a série de 07601 só fecha com a célula."))
P.append(mover(
    "Contrafilé/bisteca/chuleta de 2008 e 2017 em 07105 (estava em 07103 Carne não especificada)",
    [(["2008:71002", "2017:71002"], "07105")],
    "2008:71002 'BISTECA BOVINA / CHULETA COM OSSO (CONTRAFILE) / CONTRAFILE / FILE CURTO' (0,10 p.p.) em 07103; a "
    "versão orgânica 2008:71114 já está em 07105. 1987-2002 (6902/69002) em 07105. Série de 07105: 0,20 / 0,13 / "
    "0,09 / 0,005 / 0,002.",
    "Os mesmos itens estão em 07105 em três edições e na versão orgânica de 2008/2017."))
P.append(mover(
    "Alcatrinha/carne bovina com osso de 2008 e 2017 em 07208 (estava em 07203 Carne moída)",
    [(["2008:71017", "2017:71017"], "07208")],
    "2008:71017 'ALCATRINHA / ALCATRINHA COM OSSO (DIANTEIRO DE SEGUNDA) / CARNE BOVINA COM OSSO NAO-ESPECIFICADA' "
    "(0,08 p.p.) em 07203 Carne moída; em 2002 a mesma célula (69017) está em 07208. Ajuda a explicar o salto de "
    "07203 (0,047 → 0,148 p.p. de 2002 para 2008).",
    "Carne com osso não é carne moída; segue 2002."))
P.append(mover(
    "Chocolate em pó/achocolatado em pó de 2008 e 2017 em 12301 (estava em 11106 laticínios)",
    [(["2008:69008", "2017:69008", "2008:69103", "2017:69103"], "12301")],
    "2008:69008 'ACHOCOLATADO EM PO / CHOCOLATE EM PO...' (0,05 p.p.) em 11106 Outros (laticínios); a versão light "
    "(69102) está em 12301. 1987-2002 em 12301 (0,058 / 0,058 / 0,076); 12301 em 2008/2017: 0,000. 69103 é a diet.",
    "Mesmo item em 12301 em três edições e na versão light; 12301 fica sem conteúdo em 2008/2017 sem a correção."))
P.append(mover(
    "Pernil suíno de 2008 e 2017 em 07404 (estava em 07506 carnes salgadas)",
    [(["2008:71034", "2017:71034"], "07404")],
    "2008:71034 'COXAO SUINO / PERNIL SUINO / QUARTO SUINO' (0,013 p.p.; 0,029 no Brasil) em 07506 Outras (carne "
    "salgada); 1987-2002 'PERNIL DE PORCO / COXAO DE PORCO / QUARTO DE PORCO' em 07404. 07404 em 2008: 0,002.",
    "Carne suína fresca no quadro de carnes, não salgada; segue 1987-2002."))
P.append(mover(
    "Bolo e tortas de 1987 e 1995 em 06201 (estavam em 06303 Biscoito não especificado)",
    [(["1987:9225", "1995:9225", "1987:9235", "1995:9235", "1987:9236", "1995:9236"], "06201")],
    "'BOLO DE QUALQUER MARCA E SABOR' (1987:9225 0,05 p.p.; 1995:9225 0,04) e 'TORTAS DOCES/SALGADAS DE QUALQUER "
    "SABOR' em 06303; 2002 (92025, 92035, 92036), 2008 e 2017 em 06201. Série de 06201: 0,006 / 0,005 / 0,096 / "
    "0,092 / 0,092.",
    "Mesmo item, mesmo quadro (92), três edições em 06201."))
# ---------------------------------------------------------------- não alimentos
P.append(mover(
    "Seguro de vida e de acidentes pessoais de 2002 em 41006 (estavam em 40005 Imóveis de uso ocasional)",
    [(["2002:48007", "2002:48008"], "41006")],
    "No de-para, os códigos 2002:48007 e 48008 (quadro 48, outras despesas) trazem nomes de itens de outros imóveis "
    "(água, luz, coleta de lixo...) junto com 'SEGURO DE ACIDENTES PESSOAIS' e 'SEGURO DE VIDA'. Em 1995 (4807, 4808) "
    "e 2008 (48007, 48008) esses códigos são só os seguros, em 41006. 2002:48008 vale 0,23 p.p.; seguro de vida vale "
    "0,28 / 0,17 / — / 0,17 / 0,13 nas outras edições. 40005 em 2002 tem pico (0,66 contra 0,32 de referência).",
    "Os nomes de outros imóveis são resíduo da extração do de-para (as despesas de outros imóveis de 2002 estão no "
    "quadro 47). O microdado de 48007/48008 é seguro; a célula vai para o grupo dos seguros nas outras edições. "
    "Sai do consumo (40 → 41).", regras=("R6", "R1")))
P.append(mover(
    "Pensão alimentícia de 2017 em 41004 (estava em 41006 Outras despesas)",
    [(["2017:48009"], "41004")],
    "2017:48009 'PENSAO ALIMENTICIA EM DINHEIRO' (0,29 p.p.) em 41006; 1987-2008 em 41004 Pensões, mesadas e doações "
    "(0,41 / 0,45 / 0,69 / 0,36).", "Mesmo item, mesmo quadro (48), quatro edições em 41004."))
P.append(mover(
    "Livro escolar, apostila e dicionário de 2017 em 37004 (estavam em 37006 Outras educação)",
    [(["2017:49030", "2017:49031", "2017:49032", "2017:49033"], "37004")],
    "2017:49030 'LIVRO ESCOLAR DE 1º OU 2º GRAU IMPRESSO' (0,24 p.p.) e 49031-49033 (digital, apostila/dicionário, "
    "livro técnico digital) em 37006; 1987-2008 o livro escolar está em 37004 (0,12 / 0,09 / 0,11 / 0,06) e a apostila "
    "e o dicionário de 1987 (4308) também. Explica o pico de 37006 em 2017 (0,81 contra 0,21) e a queda de 37004 "
    "(0,05 contra 0,17).", "Mesmo item, mesmo quadro (49), quatro edições em 37004."))
P.append(mover(
    "Bíblia e livros não didáticos de 2017 em 38003 (estavam em 37004 Livros técnicos)",
    [(["2017:32017"], "38003")],
    "2017:32017 'BIBLIA IMPRESSA / LIVRO NAO DIDATICO IMPRESSO...' (0,05 p.p.) em 37004; 1987-2008 em 38003 "
    "(0,16 / 0,07 / 0,08 / 0,11) e a versão digital de 2017 (32018) também.",
    "Mesmo item, mesmo quadro (32), quatro edições e o digital de 2017 em 38003."))
P.append(mover(
    "Uniforme escolar, creche e mestrado de 1987 e 1995 nos grupos das outras edições",
    [(["1987:4310", "1995:4910"], "37006"), (["1987:4311", "1987:4323", "1995:4911", "1995:4923"], "37001"),
     (["1995:4922"], "37002")],
    "UNIFORME ESCOLAR: 1987 em 34007 Outros transporte (0,12 p.p.), 1995 em 37005, 2002-2017 em 37006. CRECHE: 1987 "
    "em 34007 e 37006, 1995 em 37005, 2002-2017 em 37001. PÓS-GRADUAÇÃO (MESTRADO): 1995 em 37005 Artigos escolares, "
    "1987 e 2002-2017 em 37002.",
    "Três edições concordam em cada item; 34007 (transporte) para uniforme e creche é erro evidente."))
P.append(mover(
    "Linha telefônica residencial de 1987, 1995 e 2017 em 42003 (estava em 32004 Eletrodomésticos)",
    [(["1987:1639", "1995:1639", "2017:15093"], "42003")],
    "'LINHA TELEFONICA (RESIDENCIAL)': 1987 0,26 p.p. e 1995 0,68 p.p. em 32004; 2002 (16039) e 2008 (15149) em 42003, "
    "assim como a linha móvel de 1995 (1697) e 'APARELHO E LINHA TELEFONICA' de 2002-2017. A linha era um direito "
    "revendável (há 'VENDA DE LINHA TELEFONICA' nas vendas esporádicas). ADR 0007: linha telefônica em 42003.",
    "Aplica a regra da ADR 0007 às três células que ficaram de fora; tira 0,68 p.p. de eletrodomésticos em 1995."))
P.append(mover(
    "IPVA de 1987 e 1995 em 41001 Impostos (estava em 34004 Manutenção de veículo)",
    [(["1987:5004", "1995:5004"], "41001")],
    "IPVA: 1987 0,09 p.p. e 1995 0,60 p.p. em 34004; 2002 (50004), 2008 (50004) e 2017 (50001) em 41001 (0,51 / 0,77 / "
    "1,25). O IBGE 2017 e o pofanalise põem IPVA em impostos. Parte da pendência 2026-11-21_arthurwelle#q7, que "
    "continua aberta para 2017:50017 (IPVA+seguro obrigatório+taxas) e as taxas do Detran.",
    "Mesmo item, mesmo quadro (50), três edições em 41001. Sai do consumo."))
P.append(mover(
    "Seguro voluntário de veículo de 1987 em 34007 (estava em 34004)",
    [(["1987:5006"], "34007")],
    "'SEGURO VOLUNTARIO PARA VEICULO' (0,31 p.p.) em 34004 em 1987; 1995-2017 em 34007 (0,46 / 0,45 / 0,50 / 0,86). "
    "ADR 0007: seguro de veículo em 34007.", "Aplica a convenção da ADR 0007 à célula de 1987 que ficou de fora."))

# ---------------------------------------------------------------- critério: para o grupo decidir
P.append(revisar(
    "Alimentação escolar em quatro grupos",
    ["1987:4326", "1995:4926", "2002:49026", "2008:49026", "2017:49075"],
    "ALIMENTACAO ESCOLAR (quadro de educação): 1987 em 37001, 1995/2002/2008 em 37005 Artigos escolares, 2017 em "
    "37006 (0,08 p.p.; 0,15 no Brasil). A merenda do quadro 24 já está em 16201.",
    "Sugestão: 37006 Outras educação em todas (paga à escola, não é artigo escolar), ou 16201 se o critério for "
    "'comida fora'. Valores pequenos antes de 2017."))
P.append(revisar(
    "Animais: divisão Bens (48001) × Serviços (48002) muda entre edições",
    ["2008:16024", "2017:13002", "1987:1640", "2002:16040", "2017:13001", "2008:16018"],
    "Medicamento/injeção para animal: 2008:16024 em 48001, 2017:13002 em 48002. Compra de animal: 1987:1640 e "
    "2002:16040 em 48002 (junto com tratamento), 2017:13001 e 2008:16018 em 48001. 48002 em 2017 vale 0,27 p.p. "
    "contra 0,07 de referência.",
    "Definir: medicamento é bem (48001) e compra de animal é bem (48001); 1987/2002 juntam compra e tratamento numa "
    "célula (R1), que fica no dominante. A divisão é da Cynthia (ADR 0008)."))
P.append(revisar(
    "Cursos livres e preparatórios espalhados entre 37001, 37003 e 37006",
    ["2008:49051", "2008:49052", "2008:49003", "2017:49013", "2017:49014", "2017:49016", "2002:49003"],
    "Pré-vestibular e pré-técnico de 2008 em 37003 (2002 em 37001); aula particular em 37003 (2008) e 37006 "
    "(2002); curso preparatório para concurso, de informática e de música de 2017 em 37006 (2008 em 37003).",
    "Sugestão: cursos livres (idiomas, informática, música, preparatórios, aula particular) em 37003 Outros cursos; "
    "37006 para despesas que não são curso (transporte, uniforme, formatura, matrícula)."))
P.append(revisar(
    "Despesas de outros imóveis: consumo (40005) ou fora (41006)?",
    ["2002:47004", "1987:4704", "2017:47005"],
    "Água, luz, gás, condomínio e taxas de outros imóveis estão em 40005 Imóveis de uso ocasional (consumo); o IPTU de "
    "outros imóveis foi para 41001 (ADR 0009). O condomínio de outros imóveis vale 0,10 / 0,10 / 0,10 / 0,07 / 0,27 "
    "p.p.",
    "Decidir se 40005 é consumo de casa de veraneio (fica) ou despesa patrimonial (41006). Hoje a série é coerente; "
    "a questão é de conceito."))
P.append(revisar(
    "Condomínio de 1987 vale 0,17 p.p. contra 2,2 em 1995",
    ["1987:812"],
    "1987:812 CONDOMINIO está em 31007, como nas outras edições, mas vale 0,17 p.p. do consumo; 1995: 2,24; 2002: 1,51; "
    "2008: 1,84; 2017: 2,53. 31007 tem o maior salto entre edições de todos os grupos de serviços.",
    "Não é erro de classificação: conferir no questionário de 1987 se o condomínio vinha embutido no aluguel ou só "
    "era perguntado a parte dos domicílios."))

ONDAS = {"ondas": [{
    "escopo": "inspecao-geral", "tipo": "global", "humano": HUMANO,
    "plano": "Inspeção geral da main depois do merge da v4 e das ondas de 2026-11-21, voltada aos problemas que ainda "
             "existem (pedido do Arthur). Os candidatos vêm do gasto ponderado por célula, calculado dos microdados "
             "com o mesmo método da aba Valores: saltos nas séries e células cujo grupo diverge do das outras edições, "
             "ordenados pelo valor. Corrige com MOVER o que tem evidência direta (mesmo item, mesmo conceito de "
             "quadro, três ou mais edições concordando, ou erro de código) e deixa como REVISAR o que é critério. "
             "Lista completa e o que não é classificação em harmonizacao/INSPECAO_2026-11-22.md.",
    "propostas": P}]}
json.dump(ONDAS, open(AQUI / "inspecao_2026-11-22.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(P), "propostas:", sum(p["tipo"] == "MOVER" for p in P), "MOVER,", sum(p["tipo"] == "REVISAR" for p in P),
      "REVISAR;", sum(len(m["celulas"]) for p in P for m in p["movimentos"]), "células")
