"""Decisões da v4 (ADR 0007): a IA decide as pendências que a v3 deixou abertas.

Gera `ondas_v4.json` para `hp_v4_onda.py`. Cada pendência da v3 vira MOVER, MANTER, UNIR, CRIAR ou REGRA,
com a evidência relida (quadro, itens, outras edições, tradutor do IBGE, revisão da Cynthia).

Uso (na raiz do repositório):  python harmonizacao/fonte/v4/decisoes_v4.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / ".claude/skills/harmoniza-pof/scripts"))
import hp_comum  # noqa: E402

V3 = "2026-10-16_claude-v3_"
EST = hp_comum.carrega_estado()
DEP = EST["depara"]
CEL = hp_comum.celulas_df(DEP).set_index("cel")
GRUPO = CEL["grupos"].to_dict()
PEN = EST["pendencias"]

# propostas REVISAR da v3 -> (titulo, celulas, pendencia)
REV: dict[str, dict] = {}
for f in sorted((RAIZ / "harmonizacao/ondas").glob(V3 + "*/propostas.json")):
    w = f.parent.name
    revs = [p for p in json.loads(f.read_text(encoding="utf-8"))["propostas"] if p["tipo"] == "REVISAR"]
    for i, p in enumerate(revs, 1):
        REV[f"{w.replace(V3, '')}#{p['id']}"] = {"titulo": p["titulo"], "cels": p.get("celulas_analisadas", []),
                                                  "pend": f"{w}#q{i}", "ev": p.get("evidencia", "")}

USADAS: dict[str, str] = {}   # célula -> destino já decidido nesta v4
AVISOS: list[str] = []


def pend(*keys: str) -> list[str]:
    out = []
    for k in keys:
        if k in REV:
            out.append(REV[k]["pend"])
        elif "#" in k and (PEN["id"] == k).any():
            out.append(k)
        else:
            sys.exit(f"pendência desconhecida: {k}")
    return out


def cels(key: str, so=None, excl=()) -> list[str]:
    cs = REV[key]["cels"]
    if so is not None:
        cs = [c for c in cs if c in so]
    return [c for c in cs if c not in excl]


def para_de(key: str) -> str:
    return re.search(r"→ (\d{5})", REV[key]["titulo"]).group(1)


def mover(titulo, movs, keys=(), motivo="", ev="", conf="MEDIA", regras=("R6",), tipo="MOVER", **extra):
    movs_ok = []
    for celulas, para in movs:
        cs = []
        for c in celulas:
            if c not in GRUPO:
                AVISOS.append(f"{titulo}: célula inexistente {c}")
                continue
            if c in USADAS:
                if USADAS[c] != para:
                    sys.exit(f"CONFLITO {c}: {USADAS[c]} x {para} ({titulo})")
                if tipo == "UNIR":  # UNIR precisa listar as células do grupo absorvido
                    cs.append(c)
                continue
            USADAS[c] = para
            if GRUPO[c] != para or tipo == "UNIR":
                cs.append(c)
        if cs:
            movs_ok.append({"celulas": cs, "para": para})
    evid = ev or " || ".join(REV[k]["ev"][:600] for k in keys if k in REV)
    if not movs_ok and tipo == "MOVER":
        return manter(titulo + " (células já no destino ou tratadas noutra proposta da v4)", keys,
                      motivo, ev=evid, cels_=[c for cs, _ in movs for c in cs])
    return {"tipo": tipo, "titulo": titulo, "movimentos": movs_ok, "confianca": conf, "regras_ref": list(regras),
            "evidencia": evid or titulo, "motivo_ia": motivo, "pendencias_v3": pend(*keys),
            "impacto": f"{sum(len(m['celulas']) for m in movs_ok)} célula(s) mudam de grupo.", **extra}


def manter(titulo, keys=(), motivo="", ev="", cels_=None):
    cs = cels_ if cels_ is not None else [c for k in keys if k in REV for c in REV[k]["cels"]]
    for c in cs:
        USADAS.setdefault(c, GRUPO.get(c, ""))
    return {"tipo": "MANTER", "titulo": titulo, "movimentos": [], "celulas_analisadas": [c for c in cs if c in GRUPO],
            "confianca": "MEDIA", "regras_ref": ["R6", "R8"],
            "evidencia": ev or " || ".join(REV[k]["ev"][:600] for k in keys if k in REV) or titulo,
            "motivo_ia": motivo, "pendencias_v3": pend(*keys), "impacto": "Nenhuma célula muda."}


def regra(titulo, tipo_r, enunciado, keys=(), grupos=(), anos=(), celulas=(), motivo="", ev="", **extra):
    return {"tipo": "REGRA", "titulo": titulo, "movimentos": [], "confianca": "MEDIA", "regras_ref": ["R4", "R5"],
            "regra_nova": {"tipo": tipo_r, "enunciado": enunciado, "grupos": list(grupos), "anos": list(anos),
                           "celulas": list(celulas), "evidencia": ev or enunciado},
            "evidencia": ev or enunciado, "motivo_ia": motivo, "pendencias_v3": pend(*keys),
            "impacto": "Registra regra; nenhuma célula muda.", **extra}


def segue(key, motivo=None, excl=(), conf="MEDIA"):
    """MOVER para o grupo em que as outras edições põem os mesmos produtos (proposta do detector da v3)."""
    p = para_de(key)
    return mover(REV[key]["titulo"], [(cels(key, excl=excl), p)], [key],
                 motivo or f"As outras edições põem os mesmos produtos em {p}, no quadro de mesmo conceito. "
                               "Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque faltava "
                               "segunda fonte.", conf=conf, regras=("R6",))


def cel_quadro(ano_quadros: dict[str, list[str]]) -> list[str]:
    out = []
    for ano, qs in ano_quadros.items():
        out += sorted(CEL[(CEL["Ano"] == ano) & (CEL["Quadro_H"].isin(qs))].index)
    return out


ONDAS = []
FORA = set(cel_quadro({"1987": ["22"], "1995": ["24"], "2002": ["24"], "2008": ["24"], "2017": ["24"]}))

# ===================================================================== 1. alimentos: detector da v3
alim = [k for k in REV if k.startswith(("alimentos-",))]
ONDAS.append({"escopo": "alimentos-series", "tipo": "familia",
              "plano": "Pares de 2 edições de alimentos que a v3 deixou sem segunda fonte. Conferido célula a "
                       "célula: os quadros mudam de número entre edições (2002 q69 = 2008/2017 q71 Carnes; q92 = q80 "
                       "Panificados), mas o conceito é o mesmo; em todos os casos a célula isolada está num grupo "
                       "genérico ou trocado e as duas outras edições concordam.",
              "propostas": [segue(k, conf="MEDIA") for k in alim]})

# ===================================================================== 2. alimentos: vazios e grupos
P = []
P.append(mover("Laranja-baía 1987 e 1995 em 03117 Tangerina: para 03107 Laranja-baía",
               [(["1987:6615", "1995:6615"], "03107")], ["vazios-por-grupo#p05"],
               "LARANJA BAHIA é o mesmo código e o mesmo produto em 1987, 1995, 2002, 2008 e 2017; nas três edições "
               "recentes está em 03107, nas duas antigas em 03117 Tangerina. Preenche o vazio de 03107 (R4).",
               ev="1987:6615 e 1995:6615 LARANJA BAHIA em 03117; 2002:66015, 2008:68015, 2017:68015 em 03107.",
               conf="ALTA"))
P.append(mover("Laranjas de 1995 com variedade diferente da de 1987 (cópia de código): para 03118 Outras laranjas",
               [(["1995:6612", "1995:6613", "1995:6614"], "03118")], [],
               "Em 1995 os códigos 6612-6614 são LARANJA LIMA, SELETA e PÊRA, mas herdaram os grupos de 1987 "
               "(Açúcar, Campista, Abril) pelo número do código (pendência q3, cópia 1995←1987). Variedade "
               "diferente não pode ficar no grupo de outra variedade; vão para Outras laranjas e os três grupos "
               "ganham regra de ausência em 1995.",
               ev="1987:6612 LARANJA AÇUCAR, 6613 CAMPISTA, 6614 ABRIL; 1995:6612 LARANJA LIMA, 6613 SELETA, 6614 PÊRA."))
P.append(regra("Variedades de laranja açúcar, campista e abril não investigadas em 1995", "ausencia_estrutural",
               "Em 1995 o questionário lista laranja lima, seleta e pêra no lugar de açúcar, campista e abril; os grupos "
               "03108, 03109 e 03110 não têm correspondente em 1995.", grupos=["03108", "03109", "03110"],
               anos=["1995"], motivo="R5: o produto não era observado separadamente naquele ano."))
P.append(mover("Caqui 2002, 2008 e 2017 em 03118 Outras: para 03201 Caqui",
               [(["2002:66028", "2008:68028", "2017:68028"], "03201")], ["vazios-por-grupo#p05"],
               "CAQUI tem código próprio nas cinco edições; 1987/1995 em 03201, 2002-2017 em 03118. A distinção é "
               "observável em todos os anos (R2): preenche o vazio de 03201.", conf="ALTA", regras=("R2", "R4")))
P.append(mover("Fubá/farinha de milho 2008 e 2017 no grupo Pamonha: para 05202 Fubá de milho",
               [(["2008:65006", "2017:65006"], "05202")], ["pendencias-validacao-e-criar#p34"],
               "2008:65006 e 2017:65006 (FARINHA DE MILHO, FUBA, MASSA DE PUBA...) estão em 12205 Pamonha, erro claro; "
               "1987-2002 têm o mesmo produto em 05202. Preenche o vazio de 05202 em 2008/2017.", conf="ALTA",
               regras=("R4", "R6")))
P.append(mover("Fécula de mandioca 2008 e 2017 em 05101 Farinha de mandioca: para 05203",
               [(["2008:65015", "2017:65015"], "05203")], ["vazios-por-grupo#p05"],
               "FECULA DE MANDIOCA / CARIMA tem código próprio nas edições; 1987-2002 em 05203. Preenche o vazio (R2/R4).",
               regras=("R2", "R4")))
P.append(mover("Lagarto paulista (redondo) 2002, 2008 e 2017 fora de 07108",
               [(["2002:69006", "2008:71006", "2017:71006"], "07108")], ["vazios-por-grupo#p05"],
               "LAGARTO PAULISTA (REDONDO) está em 07108 em 1987/1995; em 2002 em 07109 Patinho e em 2008/2017 em 07103 "
               "Carne não especificada, enquanto a versão orgânica de 2008/2017 já está em 07108.", conf="ALTA",
               regras=("R2", "R4")))
P.append(mover("Bola do patinho 2008 e 2017 em 07103: para 07109 Patinho",
               [(["2008:71005", "2017:71005"], "07109")], [],
               "BOLA DO PATINHO está em 07109 em 1987, 1995 e 2002 (e a orgânica de 2008/2017 também); só a comum de "
               "2008/2017 caiu em 07103.", conf="ALTA"))
P.append(mover("Café de cevada 2002, 2008 e 2017 em 15209 Outras bebidas: para 15303 Outros cafés",
               [(["2002:93036", "2008:82036", "2017:82036"], "15303")], ["vazios-por-grupo#p05"],
               "CAFE DE CEVADA tem código próprio nas cinco edições; 1987/1995 em 15303. Preenche o vazio de 15303.",
               regras=("R2", "R4")))
P.append(mover("Frango assado para viagem 1995-2017 em 16104: para 16101 Frango assado ou defumado",
               [(["1995:9460", "2002:94060", "2008:85010", "2017:85010"], "16101")], ["vazios-por-grupo#p03"],
               "FRANGO ASSADO OU DEFUMADO (PARA VIAGEM) tem código próprio nas cinco edições, no quadro de alimentos "
               "preparados. A v3 sugeria unir 16101 em 16104; com a distinção observável em todos os anos, a R2 manda "
               "manter o grupo e trazer as outras edições para ele.", regras=("R2", "R4")))
P.append(mover("Massas prontas para viagem 2002-2017 em 16104: para 16102 Massa preparada",
               [(["2002:94059", "2008:85009", "2008:85080", "2017:85009", "2017:85080"], "16102")],
               ["vazios-por-grupo#p05"],
               "MASSAS PRONTAS (PREPARADAS PARA CONSUMO) tem código próprio nas cinco edições; 1987/1995 em 16102. "
               "Preenche o vazio de 16102 em 2017 (R2).", regras=("R2", "R4")))
P.append(mover("Massa de arroz 2008 e 2017 (quadro de farinhas e massas) em 16104: para 05206",
               [(["2008:65001", "2017:65001"], "05206")], [],
               "MASSA DE ARROZ crua, no quadro de farinhas e massas, está em 05206 em 1987 e 2002; em 2008/2017 caiu em "
               "16104 (alimento preparado).", conf="ALTA"))
P.append(mover("Semente de linhaça 2002 no grupo sem nível 16016: unir 16016 em 01199",
               [(["2002:63034"], "01199")],
               ["alimentos-cereais-hortalicas-frutas#p11", "vazios-por-grupo#p04", "pendencias-validacao-e-criar#p28",
                "base#q2"],
               "SEMENTE DE LINHACA está em 01199 em 2008 e 2017; 16016 só existe por causa dela, sem nível e num ano só "
               "(R3). Une e extingue 16016.", tipo="UNIR", regras=("R3", "R6"), extinguir=["16016"]))
for k, mot in [("pendencias-validacao-e-criar#p01", "Colírio, soro, material de curativo: 36009 é o grupo das outras edições."),
               ("pendencias-validacao-e-criar#p02", "Centeio, amendoim, gergelim, arroz japonês: 01199 é consistente nas edições."),
               ("pendencias-validacao-e-criar#p03", "Sementes, sorgo, quinoa: 01299 consistente; feijão branco em 01203 é coerente."),
               ("pendencias-validacao-e-criar#p24", "Feijão semipronto e azuki em Outros feijões é coerente.")]:
    P.append(manter(REV[k]["titulo"], [k], "Estado atual confirmado: " + mot +
                    " A planilha antiga não traz evidência melhor (R8)."))
for k in ["pendencias-validacao-e-criar#p30", "pendencias-validacao-e-criar#p31", "pendencias-validacao-e-criar#p32",
          "pendencias-validacao-e-criar#p33", "pendencias-validacao-e-criar#p35", "pendencias-validacao-e-criar#p36",
          "pendencias-validacao-e-criar#p37"]:
    P.append(manter(REV[k]["titulo"].replace("CRIAR grupo", "Grupo"), [k], cels_=[c for c in REV[k]["cels"] if c not in FORA],
                    motivo="O grupo sugerido no formulário já existe na base, com células nas cinco edições (R2 atendida). "
                    "Nada a criar; os membros de comida fora de casa saem na onda própria."))
ONDAS.append({"escopo": "alimentos-vazios-e-grupos", "tipo": "familia",
              "plano": "Grupos de alimentos com ano vazio (A01) e grupos sugeridos no formulário. Busca pelo nome do "
                       "produto em todas as edições: na maioria dos vazios o produto existe, com código próprio, em outro "
                       "grupo (R4); a distinção é observável, então a v4 preenche o grupo em vez de uni-lo (R2).",
              "propostas": P})

# ===================================================================== 3. comida fora de casa
fora = cel_quadro({"1987": ["22"], "1995": ["24"], "2002": ["24"], "2008": ["24"], "2017": ["24"]})
ONDAS.append({"escopo": "comida-fora-de-casa", "tipo": "taxonomia",
              "plano": "Questão estrutural da v3: o quadro de alimentação fora do domicílio é classificado por produto em "
                       "2008, quase todo em 16104 em 2017 e de forma mista em 1987-2002.",
              "propostas": [
                  mover("Alimentação fora do domicílio: grupo próprio com todo o quadro (1987 q22; 1995-2017 q24)",
                        [(fora, "NOVO:fora")],
                        ["comida-fora-de-casa#p01", "pendencias-formulario#p14"],
                        "Opção (A) da v3. O questionário separa a alimentação fora do domicílio em todas as edições e o "
                        "IBGE a publica à parte; classificar por produto mistura comer fora com comer em casa e hoje a "
                        "mesma despesa muda de grupo conforme a edição. Um grupo novo, em vez de 16104, porque 16104 "
                        "reúne alimentos preparados comprados para levar (quadros 94/85), outro conceito. A divisão "
                        "refeição × lanche/bebida fica possível depois, por item, se alguém quiser.",
                        tipo="CRIAR", regras=("R2", "R6"), conf="MEDIA",
                        novos_grupos={"fora": {"nome": "Alimentação fora do domicílio", "nivel1": "16. Outros produtos",
                                               "nivel2": "16.2 Alimentação fora do domicílio",
                                               "codigo_sugerido": "16201"}})]})

# ===================================================================== 4. habitação e reforma
P = []
P.append(regra("Reforma × manutenção do lar: convenção pelo quadro", "convencao",
               "Conservação, manutenção e pequenos reparos ficam em 32001 Manutenção do lar; construção e reforma, em 42002 "
               "Imóvel reforma. Em 2008 e 2017 o questionário separa os dois (quadro 8 × quadro 11) e o quadro decide. Em "
               "1987-2002, onde a célula mistura os dois conceitos, ela fica no dominante (32001); itens explícitos de "
               "construção, obra por empreitada ou material de obra vão para 42002.",
               ["2026-09-11_arthurwelle#q1", "2026-09-11_arthurwelle#q2"], grupos=["32001", "42002"],
               motivo="Unir 32001 e 42002 (sugestão das NOTAS) juntaria consumo e aumento do ativo nas cinco edições "
                      "para resolver um problema de 1987-1995; a separação existe no questionário de 2008 e 2017. A R1 "
                      "continua valendo célula a célula (hp_validar sem erro)."))
P.append(mover("1995: reforma ou obra por empreitada e fossa séptica em 32001: para 42002",
               [(["1995:816", "1995:866"], "42002")], ["pendencias-formulario#p13", "nao-consumo#p19"],
               "Itens explícitos de construção (convenção acima). 1995:800 é o cabeçalho que mistura construção, reforma e "
               "pequenos reparos: fica em 32001 (dominante).", regras=("R6",)))
P.append(mover("Material hidráulico e elétrico de 1995 (quadro 8) em 40006: para 42002",
               [(["1995:810", "1995:812"], "42002")], ["cynthia-folha-400006#p05"],
               "Revisão da Cynthia (folha 40006 #10): material de obra, mesmo destino de 1987. Coerente com a convenção."))
P += [segue(k) for k in ["habitacao-servicos#p19", "habitacao-servicos#p20", "habitacao-servicos#p21",
                         "habitacao-servicos#p22", "habitacao-servicos#p24", "habitacao-servicos#p25",
                         "habitacao-servicos#p26"]]
P.append(mover("Acendedor eletrônico 1995 em 32003: para 32004", [(["1995:1631"], "32004")],
               ["habitacao-servicos#p23"], "2002 e 2008 em 32004 (aparelho elétrico); 1995 herdou o grupo de 1987:1631 "
               "(ferramentas) pelo número do código."))
P.append(mover("Conserto e manutenção de móveis 1995 em 42001 Imóvel aquisição: para 32005",
               [(["1995:901", "1995:902"], "32005")],
               ["habitacao-servicos#p27", "pendencias-formulario#p10", "cynthia-folha-32#p09"],
               "1987, 2002 e 2008 em 32005, revisão da Cynthia (folha 32 #9) também; 1995 herdou 'aquisição do imóvel' "
               "de 1987:901/902 pelo número. O formulário sugeria 42002, mas conserto de móvel não é reforma do imóvel.",
               conf="ALTA"))
P.append(mover("Manutenção de utensílios domésticos 1995 em 31007: para 32005", [(["1995:909"], "32005")],
               ["pendencias-formulario#p15"],
               "Conserto/manutenção (quadro 9 de 1995, consertos). Os agregados do quadro 7 (1987:798, 1995:798) ficam em "
               "31007: misturam serviços públicos e combustíveis, e 31007 é o resíduo desses serviços."))
for k, mot in [("habitacao-servicos#p28", "1987:5311 EMPREGADO está no quadro 53, de rendimentos: é renda do trabalho (44001), "
                                          "não pagamento a empregado doméstico; o par das outras edições é do quadro 19."),
               ("habitacao-servicos#p29", "2017:14028 está no quadro 14, inventário de bens duráveis; o par das outras "
                                          "edições é do quadro 17, aquisição. Inventário não é despesa."),
               ("habitacao-servicos#p30", "2008:14008 está no quadro 14, inventário; o par é do quadro 15, aquisição."),
               ("habitacao-servicos#p31", "2008 (e 2017) separam carpete e papel de parede em pequenos reparos (quadro 8, "
                                          "32001) e construção/reforma (quadro 11, 42002); 1987-2002 só têm a compra "
                                          "como decoração (quadro 18). Conceitos diferentes; vale a convenção acima."),
               ("habitacao-servicos#p33", "Idem: quadro 11 de 2008 é construção e reforma (42002), como 2017.")]:
    P.append(manter(REV[k]["titulo"], [k], mot))
P.append(mover("Aparelho para massa e para fondue 2017 (quadro 39) em 32003: para 32004",
               [(["2017:39030", "2017:39033"], "32004")], ["habitacao-servicos#p32", "cynthia-folha-32#p20"],
               "1995, 2002 e 2008 em 32004; a revisão da Cynthia (folha 32 #20) reverteu o outlier de 2017. O IBGE de 2017 "
               "põe em Mobiliário, mas a série prevalece (ADR 0007)."))
P.append(mover("Jazigo: condomínio, placa e lápide para 40003 Cerimônias; reforma de jazigo para 42002",
               [(["1987:1107", "1995:1107", "1995:1106", "1987:1105", "1995:1105", "2002:11082", "2008:11082"], "40003"),
                (["2002:11081", "2008:11081"], "42002")],
               ["habitacao-servicos#p37", "educacao-despesas-diversas#p27", "cynthia-folha-400006#p03",
                "cynthia-folha-400006#p04"],
               "Condomínio (taxa) de jazigo, placa e lápide estão em 40003 em 2002-2017 e vão para lá em 1987/1995 "
               "(Cynthia folha 40006 #8). Construção e reforma de jazigo seguem a reforma do imóvel (42002), como 1987, "
               "1995 e o IBGE 2017 (Cynthia #9).", regras=("R6", "R7")))
ONDAS.append({"escopo": "habitacao-e-reforma", "tipo": "familia",
              "plano": "Pendências de habitação: reforma × manutenção (NOTAS, R1 em 1987), pares de 2 edições, "
                       "mudanças de conceito e jazigo.", "propostas": P})

# ===================================================================== 5. revisão da Cynthia, folhas 32 e 40006
P = []
for k, para in [("cynthia-folha-32#p01", "32001"), ("cynthia-folha-32#p02", "32002"), ("cynthia-folha-32#p03", "32002"),
                ("cynthia-folha-32#p04", "32001"), ("cynthia-folha-32#p11", "32002"), ("cynthia-folha-32#p18", "32002"),
                ("cynthia-folha-32#p15", "32003"), ("cynthia-folha-32#p21", "32003")]:
    P.append(mover(REV[k]["titulo"], [(cels(k), para)], [k],
                   "Revisão manual da Cynthia (evidência humana) confirmada: as outras edições põem o produto no destino "
                   "indicado, ou a revisão adota o destino coerente de 2017 (maturação de taxonomia).", conf="ALTA"))
P.append(mover("Máquina de costura manual 1995 em 32003: para 32004", [(["1995:1632"], "32004")],
               ["cynthia-folha-32#p05"], "Cynthia folha 32 #5; 4 edições contra 1 em 32004.", conf="ALTA"))
P.append(mover("Cofre: 2002, 2008 e 2017 para 32003 Mobiliário e artigos do lar",
               [(["2017:16011", "2002:40075", "2008:40023"], "32003")],
               ["cynthia-folha-32#p14", "cynthia-folha-400006#p19"],
               "1995 em 32003; 2002/2008 em 40006 e 2017 em 38005 (quadro 16 deslocado). Cynthia (folha 32 #14 e 40006 "
               "#31): cofre é artigo do lar. Aluguel de caixa-forte e cofre (serviço) continua em 40006."))
for k, para, cs, mot in [
        ("cynthia-folha-400006#p02", "32004", None, "Tosadeira em 32004 em 1987 e 2002; só 2008 diverge."),
        ("cynthia-folha-400006#p16", "32003", None, "Cesta (objeto) em 32003 desde 2002; 1987/1995 por analogia."),
        ("cynthia-folha-400006#p17", "32003", None, "Bateria de relógio/brinquedo em 32003 em 2017; resíduo nas antigas."),
        ("cynthia-folha-400006#p20", "32002", None, "Pedra para polir fogão: 2017 em 32002, mesmo produto."),
        ("cynthia-folha-400006#p22", "32004", None, "Máquina de moer carne por analogia à elétrica."),
        ("cynthia-folha-400006#p15", "16103", None, "Varejão, sacolão, feirinha, sacola Cobal (caderneta coletiva de "
                                                     "alimentos) já classificados em 16103 nas outras edições.")]:
    P.append(mover(REV[k]["titulo"], [(cs or cels(k), para)], [k], "Revisão da Cynthia. " + mot))
P.append(mover("2017 quadro 16: utensílios domésticos fora do lugar (recreação e despesas diversas)",
               [(["2017:16005", "2017:16014", "2017:16019", "2017:16021", "2017:16024", "2017:16028", "2017:16031",
                  "2017:16036", "2017:16037", "2017:16038", "2017:16999"], "32003"),
                (["2017:16029", "2017:16039"], "32004")],
               ["2017-quadros-deslocados#p05", "cynthia-folha-38#p01", "cynthia-folha-38#p02", "cynthia-folha-38#p03",
                "cynthia-folha-400006#p21"],
               "Quadro 16 de 2017 (aparelhos e utilidades não elétricas de uso doméstico) deslocado por PROCV para "
               "recreação/despesas diversas. Destino pela linha fina do IBGE 2017 (1102.06 Mobiliário e artigos do lar; "
               "1102.07 para o ferro a gás) e pela revisão da Cynthia (folha 38 #1-#3, ferramentas; folha 40006 #33-#34). "
               "Os homônimos que a extração da revisão achou (METRO = metrô, LIMA = fruta) ficam fora.",
               regras=("R4", "R6")))
P.append(mover("2017 quadro 37: tecidos e couro para 33006; artesanato para 38005",
               [(["2017:37003", "2017:37006", "2017:37007", "2017:37023", "2017:37999"], "33006"),
                (["2017:37018", "2017:37019", "2017:37020", "2017:37021", "2017:37022", "2017:37024"], "38005")],
               ["2017-quadros-deslocados#p06"],
               "Tecido para artigos do lar, couro, entretela e o agregado do quadro de armarinho seguem 33006 Tecidos e "
               "armarinhos, como o IBGE e as outras edições (napa e lona já movidas pela v3). Os itens de artesanato, novos "
               "em 2017, vão para 38005, como o IBGE (Recreação > Outras)."))
for k, mot in [("cynthia-folha-400006#p01", "Transporte de animais (2002/2008) fica em 40006; a célula de 2002 sai junto com "
                                            "transporte de mercadorias para 39005 (folha 40006 #30)."),
               ("cynthia-folha-400006#p14", "A própria revisão mantém presentes em geral em 40006."),
               ("cynthia-folha-400006#p09", "A ação não identifica células no estado atual (texto truncado no PDF); nada a fazer.")]:
    P.append(manter(REV[k]["titulo"], [k], mot, cels_=["2008:40002"] if k.endswith("p01") else None))
ONDAS.append({"escopo": "cynthia-habitacao", "tipo": "pendencia",
              "plano": "Ações das revisões manuais (folhas 32 e 40006) que a v3 deixou como REVISAR e os quadros 16 e 37 "
                       "de 2017. A v4 aceita a revisão humana quando ela não contraria a série; homônimos da extração e "
                       "células com itens misturados ficam fora (R1).", "propostas": P})

# ===================================================================== 6. educação
P = [segue(k) for k in ["educacao-despesas-diversas#p19", "educacao-despesas-diversas#p20", "educacao-despesas-diversas#p21",
                        "educacao-despesas-diversas#p23", "educacao-despesas-diversas#p24",
                        "educacao-despesas-diversas#p25", "educacao-despesas-diversas#p26",
                        "educacao-despesas-diversas#p29", "educacao-despesas-diversas#p30"]]
P.append(mover("1987: livros didáticos, técnicos e assinatura de periódico técnico em cursos: para 37004",
               [(["1987:4308", "1987:4306"], "37004")],
               ["educacao-despesas-diversas#p22", "cynthia-folha-37#p05", "cynthia-folha-37#p07"],
               "2002/2008 em 37004 e revisão da Cynthia (folha 37 #18, #20): material didático não é curso.", conf="ALTA"))
P.append(mover("1987: cursos livres (auto-escola, balé, datilografia...), aula particular e curso em disco em Curso superior: "
               "para 37003", [(["1987:4302", "1987:4303", "1987:4304"], "37003")],
               ["pendencias-validacao-e-criar#p11", "cynthia-folha-37#p03"],
               "Código catch-all de cursos livres de 1987 (Cynthia folha 37 #3); nas outras edições esses cursos estão em "
               "37003. Não são curso superior.", conf="ALTA"))
tec = [c for c in CEL[(CEL["Ano"] == "2017") & (CEL["grupos"] == "37001")].index
       if re.search(r"TECNICO|PROFISSIONALIZANTE|EMPREENDEDORISMO|ASSISTENTE ADMINISTRATIVO", CEL.loc[c, "itens"])]
P.append(mover("2017: cursos técnicos e profissionalizantes em Cursos regulares: para 37003",
               [(tec, "37003")], ["cynthia-folha-37#p01"],
               "Revisão da Cynthia (folha 37 #1): curso técnico/profissionalizante é 'outros cursos', como nas edições "
               "anteriores; 37001 é a educação regular."))
for k, para in [("cynthia-folha-37#p02", "37001"), ("cynthia-folha-37#p04", "37002"), ("cynthia-folha-37#p06", "37005"),
                ("cynthia-folha-37#p08", "37003"), ("cynthia-folha-37#p10", "41004")]:
    P.append(mover(REV[k]["titulo"], [(cels(k), para)], [k], "Revisão da Cynthia (folha 37), destino coerente com a "
                                                                "descrição do grupo e com as outras edições."))
for k, mot in [("educacao-despesas-diversas#p28", "2008:8071 (aluguel de lixadeira em pequenos reparos) e 2017:8046 ficam em "
                                                  "32001 pelo quadro 8; o par 40006 é do quadro 13 de aluguel de aparelhos."),
               ("educacao-despesas-diversas#p33", "Idem no quadro 11 (construção e reforma): 42002, como 2017:11069."),
               ("educacao-despesas-diversas#p31", "Batistério em 2008 está no quadro 45 (cerimônias religiosas); o par é do "
                                                  "quadro 44 (cartório). Conceitos distintos; mantém (R8)."),
               ("educacao-despesas-diversas#p32", "Tradutor em 2017 está no quadro 40 (cartório, advogado e similares), "
                                                  "serviço profissional; o par de educação é outro conceito."),
               ("pendencias-validacao-e-criar#p25", "Alimentação escolar em Cursos regulares (1987) é coerente: gasto "
                                                    "com a escola."),
               ("pendencias-validacao-e-criar#p27", "Creche em 37001, como a revisão da Cynthia (folha 37 #2) faz para as "
                                                    "outras edições.")]:
    P.append(manter(REV[k]["titulo"], [k], mot))
ONDAS.append({"escopo": "educacao", "tipo": "familia",
              "plano": "Educação e despesas diversas: pares do detector, revisão da Cynthia (folha 37) e validação.",
              "propostas": P})

# ===================================================================== 7. recreação e telefonia
P = [segue(k) for k in ["recreacao-cultura#p12", "recreacao-cultura#p13", "recreacao-cultura#p15",
                        "recreacao-cultura#p17"]]
P[1]["pendencias_v3"] += pend("cynthia-folha-38#p15")  # academia 2017: mesma célula da revisão manual
P.append(mover("2017 quadro 43: instrumentos musicais, ginástica, praia e camping em Brinquedos: para 38005",
               [(cels("recreacao-cultura#p14") + ["2017:43008", "2017:43044"], "38005")],
               ["recreacao-cultura#p14", "cynthia-folha-38#p04", "cynthia-folha-38#p06"],
               "1987-2008 em 38005 (3 ou 4 edições) e revisão da Cynthia (folha 38 #4 e #6). O IBGE 2017 (Recreação > "
               "Outras) é compatível; a linha fina não muda o grupo. 2017:41017 (hospedagem) ficou fora: homônimo de "
               "'acampamento'.", conf="ALTA"))
P.append(mover("2008: mídia (vinil, fitas, CD, disquete), material esportivo, de pesca e carnaval em 38005: para 38004",
               [(sorted(set(cels("recreacao-cultura#p16")) | set(cels("cynthia-folha-38#p11"))), "38004")],
               ["recreacao-cultura#p16", "cynthia-folha-38#p11"],
               "1995, 2002 e 2017 em 38004 e revisão da Cynthia (folha 38 #11).", conf="ALTA"))
P.append(mover("Patins, skate e porta-patins 2008 em 38005: para 38001 Brinquedos",
               [(["2008:33003", "2008:33010"], "38001")], ["recreacao-cultura#p15", "cynthia-folha-38#p05"],
               "Cynthia folha 38 #5. 2002:33002 (baldinho de praia junto com bolas, boia, pingue-pongue) não sai de 38004: "
               "a célula mistura brinquedo e material esportivo (R1)."))
for k, para in [("cynthia-folha-38#p08", "37005"), ("cynthia-folha-38#p09", "38003"), ("cynthia-folha-38#p20", "32004"),
                ("cynthia-folha-400006#p07", "38005"), ("cynthia-folha-400006#p08", "38004")]:
    P.append(mover(REV[k]["titulo"], [(cels(k), para)], [k], "Revisão da Cynthia confirmada pelas outras edições."))
P.append(manter("Ingressos de exposição, feira, show, piquenique, piscina e festa junina: ficam em 38004",
                ["cynthia-folha-38#p10", "cynthia-folha-38#p12", "cynthia-folha-38#p17"],
                "A revisão manual propunha adotar 2017 (38005, 38006 ou 40003); a v4 não segue porque 1987-2008 (4 "
                "edições) concordam em 38004 Diversões e esportes e o outlier é 2017, que volta para 38004 (proposta "
                "do detector acima). Festa junina e quermesse estão em 38004 em 2002-2017. Alimentação de viagem de 2002 "
                "já está em 38006 (R8).",
                cels_=REV["cynthia-folha-38#p10"]["cels"] + REV["cynthia-folha-38#p12"]["cels"]))
P.append(manter("Bolas e raquetes de 1987 (sapatilha de ginástica na mesma célula)", ["cynthia-folha-38#p14"],
                "1987:3302 reúne bolas, raquetes e outros equipamentos com a sapatilha; mover a célula para calçados "
                "levaria todo o material esportivo junto (R1). Fica em 38004."))
servico = ["1995:715", "2008:28023", "2008:28024", "2017:44001", "2017:44002", "2017:44003", "2017:44007",
           "2017:6010", "2017:6011", "2017:6016"]
P.append(mover("Telefonia celular: serviço em 31003 Telefonia; aparelho e acessórios em 38002",
               [(servico, "31003")], ["recreacao-cultura#p18", "pendencias-formulario#p09"],
               "O serviço de telefonia móvel estava em quatro grupos (38002, 31003, 38005, 38002). Serviço × aparelho é "
               "observável nas cinco edições e é a divisão do IBGE (Habitação 2.3.3 × Recreação 8.2). Conta, cartão, "
               "recarga e pacotes com celular vão para 31003; aparelho, acessórios, aplicativos e seguro ficam em 38002.",
               regras=("R2", "R6")))
P.append(regra("Celular e acessórios: ausência estrutural em 1987", "ausencia_estrutural",
               "A telefonia celular começa no Brasil em 1990; a POF 1987-1988 não tem o produto.",
               ["vazios-por-grupo#p01"], grupos=["38002"], anos=["1987"], motivo="R5 (exemplo da própria CONSTITUICAO)."))
P.append(mover("Linha telefônica (direito de uso) em 42003 Outros investimentos nas cinco edições",
               [(["1995:1673", "1995:1697"], "42003")], ["pendencias-formulario#p11", "pendencias-formulario#p12"],
               "Linha, ramal e central telefônica estão em 42003 em 2002 e 2008, como o IBGE (Aumento do ativo). A compra "
               "do direito de linha era ativo; 1995 (ramal comunitário e linha móvel) vem para o mesmo grupo. A sugestão "
               "do formulário (32004) e a taxa de transferência em 31007 não seguem: série e IBGE concordam com o estado "
               "atual, que fica."))
ONDAS.append({"escopo": "recreacao-e-telefonia", "tipo": "familia",
              "plano": "Recreação (pares do detector, revisão da Cynthia folha 38 e 40006) e reorganização da telefonia.",
              "propostas": P})

# ===================================================================== 8. vestuário, transporte, saúde
P = [segue(k) for k in ["vestuario-transporte-higiene-saude#p22", "vestuario-transporte-higiene-saude#p25",
                        "vestuario-transporte-higiene-saude#p26", "vestuario-transporte-higiene-saude#p27",
                        "vestuario-transporte-higiene-saude#p28", "vestuario-transporte-higiene-saude#p29",
                        "vestuario-transporte-higiene-saude#p30", "vestuario-transporte-higiene-saude#p33",
                        "vestuario-transporte-higiene-saude#p35", "vestuario-transporte-higiene-saude#p36"]]
P.append(mover("Seguro de veículo e gás veicular: 34007 Outros transporte nas cinco edições",
               [(["1987:5003", "1995:5003", "1995:5006", "2002:23018"], "34007")],
               ["vestuario-transporte-higiene-saude#p23", "vestuario-transporte-higiene-saude#p38"],
               "Seguro obrigatório e voluntário estão em 34007 em 2002-2017 e no IBGE (Transporte > Outras); seguro não é "
               "manutenção. Gás veicular em 34007 em 2008/2017.", conf="ALTA"))
P.append(mover("Agregado do quadro de documentação e seguro de veículos (2008, 2017) em Impostos: para 34007",
               [(["2008:50999", "2017:50999"], "34007")], ["vestuario-transporte-higiene-saude#p39"],
               "O IBGE põe o agregado em Transporte > Outras nas duas edições; o agregado reúne seguro e taxas, não só "
               "imposto."))
P.append(mover("Multas de veículo 1987 e 1995 em Manutenção: para 41001", [(["1987:5002", "1995:5002"], "41001")], [],
               "MULTAS (quadro 50) estão em 41001 em 2002, 2008 e 2017; 1987/1995 em 34004.", conf="ALTA"))
P.append(mover("Canoa (transporte, quadro 23) 2017 em 34007: para 34001", [(["2017:23009"], "34001")], [],
               "CANOA no quadro de transporte coletivo está em 34001 em 2002 e 2008."))
for k, mot in [("vestuario-transporte-higiene-saude#p24", "2002:43015 SHAMPU está no quadro 43 (acessórios e manutenção de "
                                                          "veículos): é shampoo automotivo, 34004 correto."),
               ("vestuario-transporte-higiene-saude#p31", "2017:15111 ALARME está no quadro 15 (aparelhos elétricos de uso "
                                                          "doméstico): alarme residencial; o alarme de carro de 2017 (33029) "
                                                          "já está em 34004."),
               ("vestuario-transporte-higiene-saude#p32", "2008:36010 CUECA está no quadro 36 (roupa de criança): 33003 "
                                                          "correto; o par era a cueca do quadro de homem."),
               ("vestuario-transporte-higiene-saude#p34", "2017:51021 CANOA está no quadro 51 (aquisição de veículos): "
                                                          "34005, como 2002:51025 e 2008:51020.")]:
    P.append(manter(REV[k]["titulo"], [k], mot))
P.append(mover("Amplificador, videogame e karaokê 2002/2008 (quadro 15) em Gastos com viagens: para 32004",
               [(cels("pendencias-validacao-e-criar#p04"), "32004")], ["pendencias-validacao-e-criar#p04"],
               "Aparelhos do quadro 15 (aquisição de aparelhos) não podem estar em viagens; 1987/1995 têm videogame em "
               "32004 e a planilha v2026 também.", conf="ALTA"))
P.append(mover("Vidraceiro 2002 em 32005: para 39005", [(["2002:31025"], "39005")], ["pendencias-validacao-e-criar#p26"],
               "Quadro 31 (serviços pessoais); as outras edições põem em 39005."))
for k, mot in [("pendencias-validacao-e-criar#p08", "Anticoncepcionais em 36010 e teste de gravidez em 36009: coerente."),
               ("pendencias-validacao-e-criar#p09", "Bateria musical, revelação fotográfica e luneta em 38005: coerente."),
               ("pendencias-validacao-e-criar#p12", "Corega/fixador de dentadura em 35004: coerente nas três edições."),
               ("pendencias-validacao-e-criar#p29", "Cotonete em 36009, como 1987:2912.")]:
    P.append(manter(REV[k]["titulo"], [k], "Estado atual confirmado. " + mot))
ONDAS.append({"escopo": "vestuario-transporte-saude", "tipo": "familia",
              "plano": "Vestuário, transporte, higiene e saúde: pares do detector conferidos pelo quadro, seguro de veículo "
                       "e validação.", "propostas": P})

# ===================================================================== 9. não consumo, aluguéis, outros imóveis
P = [segue(k) for k in ["nao-consumo#p15", "nao-consumo#p16", "nao-consumo#p17", "nao-consumo#p18", "nao-consumo#p21",
                        "nao-consumo#p22", "nao-consumo#p23", "nao-consumo#p24", "nao-consumo#p25"]]
P.append(manter(REV["nao-consumo#p20"]["titulo"], ["nao-consumo#p20"],
                "1987:5101 AUTOMOVEL está no quadro 51 (compra de veículos): 34005 correto; o par 88888 é do inventário."))
P.append(mover("Compra de outros imóveis (valor do imóvel adquirido, consórcio) em consumo: para 42001",
               [(REV["nao-consumo#p26"]["cels"], "42001")], ["nao-consumo#p26"],
               "Comprar imóvel é aumento do ativo; o repositório já trata assim o domicílio principal (42001 nas cinco "
               "edições) e o IBGE também. Para outros imóveis o valor de compra estava em 40005 Imóveis de uso ocasional "
               "(consumo) em todas as edições.", regras=("R6", "R7")))
P.append(mover("2017 quadro 47: aluguel de outros imóveis e de garagem em Imóvel aquisição: para 40005",
               [(["2017:47003", "2017:47004"], "40005")], ["2017-quadros-deslocados#p08"],
               "Aluguel não é aquisição; 2008 e o IBGE 2017 põem em 40005 (Imóveis de uso ocasional). IPTU, ITR e INCRA de "
               "outros imóveis e título/joia de clube ficam em 40005, como em 2008 (R8)."))
P.append(mover("2017 quadro 9: aluguel de aparelhos em Consertos: para 40006, como 1987-2008",
               [(cels("2017-quadros-deslocados#p07"), "40006")],
               ["2017-quadros-deslocados#p07", "cynthia-folha-400006#p10", "cynthia-folha-400006#p11",
                "cynthia-folha-400006#p06", "cynthia-folha-400006#p12"],
               "O aluguel de aparelhos está em 40006 em 1987, 1995, 2002 e 2008 (quadro 13) e o IBGE 2017 também o põe em "
               "Despesas diversas. A revisão manual propunha o contrário (todas as edições em 32005, como 2017; lixadeira "
               "em 42002; BIP e celular em 31003); a v4 fica com a série de 4 edições e com o IBGE: aluguel não é conserto "
               "nem telefonia."))
P.append(mover("TV a cabo (mensalidade) 1995 no quadro de aluguel: para 31007", [(["1995:1313"], "31007")],
               ["cynthia-folha-400006#p13"],
               "Assinatura de TV, não aluguel de aparelho; 31007 desde 2008 (Cynthia folha 40006 #21)."))
P.append(mover("Transporte de mercadorias (1987, 2002, 2008) em 40006: para 39005",
               [(["1987:4007", "2002:40007", "2008:40005"], "39005")], ["cynthia-folha-400006#p18"],
               "2017 em 39005 (Cynthia folha 40006 #30)."))
P.append(mover("Vendas de automóveis e vendas esporádicas de imóveis 1987: para 47001 Vendas esporádicas",
               [(["1987:5508", "1987:5509"], "47001")], ["vazios-por-grupo#p06"],
               "As vendas de 1995-2017 estão em 47001; 1987 estava em 47004 Outros. Preenche o vazio de 47001 em 1987.",
               conf="ALTA"))
P.append(regra("Trabalho não remunerado: ausência estrutural em 1987 e 1995", "ausencia_estrutural",
               "O questionário de rendimentos de 1987 e 1995 não registra trabalho não remunerado; 44004 começa em 2002.",
               ["vazios-por-grupo#p06"], grupos=["44004"], anos=["1987", "1995"],
               motivo="R5: nenhum item parecido nas duas edições (busca na v3)."))
P.append(regra("Viagens: convenção em 38006; 34006 extinto", "convencao",
               "Os gastos com viagens ficam em 38006 Gastos com viagens em todas as edições; 34006 Viagens (Transporte) "
               "nunca teve célula e é extinto.", ["vazios-por-grupo#p02"], grupos=["38006", "34006"],
               motivo="Mover as viagens para Transporte, como o IBGE, mudaria um grupo inteiro sem ganho de "
                      "comparabilidade entre as edições (R8). Extinguir não muda nenhuma célula.",
               extinguir=["34006"]))
ONDAS.append({"escopo": "nao-consumo-e-alugueis", "tipo": "familia",
              "plano": "Outras despesas, ativo, passivo e rendimentos: pares do detector, compra de outros imóveis, "
                       "aluguéis de aparelhos e de outros imóveis, vazios de 44004/47001 e 34006.", "propostas": P})

# ===================================================================== 10. 1995 copiado de 1987 e pendências antigas
k = "1995-copia-de-1987#p02"
cop = REV[k]["cels"]
mov95 = {"1995:1659": "32004", "1995:1661": "32004", "1995:1675": "32004", "1995:4310": "34004", "1995:4311": "34004",
         "1995:9542": "32002"}
P = [mover("1995 copiado de 1987: células com grupo de outro produto corrigidas",
           [([c for c, g in mov95.items() if g == x], x) for x in sorted(set(mov95.values()))], [k],
           "Conferido produto a produto (ver fonte/v3_extras/1995_copia_1987.csv): antena de rádio, aparelho para massa e "
           "lava a jato são aparelhos (32004; 1987:1581 antena em 32004); toca-fitas e ar-condicionado de veículo são "
           "acessórios de veículo (34004, quadro 43); sulfato de alumínio é produto de limpeza (32002). As demais "
           "suspeitas já foram tratadas noutras propostas da v4 (1995:901, 902, 1631, 1632, 1673, 5002, 5405) ou o grupo "
           "atual está certo para o produto de 1995 (gás de butijão, pipoqueira elétrica, conjunto de baldes, "
           "espreguiçadeira, mordomo, antibiótico, fósforos, carnê de mercadorias, os agregados e cabeçalhos).",
           regras=("R6",))]
P.append(manter("Linhas duplicadas exatas do de-para (A03)", ["base#q1"],
                "As 5 duplicatas estão no mesmo grupo (não afetam a harmonização) e o de-para só muda por `fechar`, que não "
                "remove linhas. Remover é limpeza de dados, fora do escopo de decisão.", cels_=[]))
P.append(manter("2026-09-11 cirurgia q1: auditoria de 2017 inteira", ["2026-09-11_arthurwelle_cirurgia#q1"],
                "Feita na v3 (detector entre edições + tradutor do IBGE) e concluída na v4 (quadros 9, 16, 37, 43 e 47 "
                "de 2017).", cels_=[]))
P.append(manter("base#q6: 29001 Para dor e febre (planilha de melhorias)", ["base#q6"],
                "A linha da planilha de melhorias não traz grupo sugerido nem célula; os analgésicos estão em 36001 "
                "Remédios em todas as edições.", cels_=[]))
ONDAS.append({"escopo": "1995-copia-e-antigas", "tipo": "pendencia",
              "plano": "Fecha a auditoria da cópia 1995←1987 (pendência q3) e as pendências antigas que ainda tinham "
                       "resposta possível.", "propostas": P})

# ===================================================================== 11. vazios que sobraram após as ondas 1-10
ONDAS.append({"escopo": "vazios-finais", "tipo": "familia",
              "plano": "hp_validar depois das ondas 1-10: A01 em 03202 Maçã (2002) e 16105 Salgadinho (2002, 2008). "
                       "Mesmo padrão dos outros vazios: o produto tem código próprio e está num grupo genérico.",
              "propostas": [
                  mover("Maçã 2002, 2008 e 2017 em 03118 Outras frutas: para 03202 Maçã",
                        [(["2002:66030", "2008:68030", "2017:68030"], "03202")], [],
                        "MAÇÃ está em 03202 em 1987 e 1995, e a maçã orgânica de 2008/2017 também; a maçã comum de "
                        "2002-2017 caiu em Outras frutas. Preenche o vazio de 2002 (R2/R4).", conf="ALTA",
                        regras=("R2", "R4")),
                  mover("Salgados para viagem 2002, 2008 e 2017 em 16104: para 16105 Salgadinho",
                        [(["2002:94052", "2008:85002", "2017:85002"], "16105")], [],
                        "SALGADINHOS PARA VIAGEM (coxinha, pastel, esfirra, quibe...) tem código próprio nas cinco "
                        "edições; 1987/1995 em 16105. Preenche o vazio de 2002 e 2008 (R2/R4).", regras=("R2", "R4"))]})

# ===================================================================== saída
todas_rev = {v["pend"] for v in REV.values()}
resolvidas = {x for o in ONDAS for p in o["propostas"] for x in p["pendencias_v3"]}
faltam = sorted(todas_rev - resolvidas)
for a in AVISOS:
    print("AVISO", a)
print(f"{len(ONDAS)} ondas · {sum(len(o['propostas']) for o in ONDAS)} propostas · "
      f"{sum(len(m['celulas']) for o in ONDAS for p in o['propostas'] for m in p['movimentos'])} células movidas")
print(f"pendências da v3 sem decisão: {len(faltam)}", faltam[:20])
(Path(__file__).parent / "ondas_v4.json").write_text(json.dumps({"ondas": ONDAS}, ensure_ascii=False, indent=1),
                                                       encoding="utf-8")
