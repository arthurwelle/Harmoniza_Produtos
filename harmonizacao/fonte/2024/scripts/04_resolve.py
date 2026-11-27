"""Passo 4: resolve as células REVISAR e gera o de-para 2024 completo (decisão da IA, a pedido do Arthur).

Ordem das regras para cada célula REVISAR:
  1. DECISOES (abaixo): decisão explícita, com o motivo e a célula 2017 análoga quando existe.
  2. FRETE (item novo de 2024, um por quadro, valor ~0): grupo dominante, em valor, das células
     ATRIBUIR do mesmo quadro 2024.
  3. Demais: aceita Cod_harmo_sugerido do passo 2, que é o grupo da célula 2017 mais parecida no
     quadro mapeado, ou o grupo mais pesado com o mesmo nível IBGE.
Quando o nível 3 do IBGE de 2024 difere do grupo de 2017, prevalece a classificação de 2017 (R7/R8):
o IBGE reclassificou alguns itens entre as edições (ex.: aulas esportivas, de educação para recreação).

Saídas:
  saida/depara_2024_final.csv      formato estado/depara.csv, uma linha por célula 2024 (todas)
  saida/decisoes_2024.csv          ledger: célula, tipo, de (sugestão), para, confiança, motivo, revisor
  saida/pendencias_estruturais.md  o que exige decisão humana com ADR (R1, produtos novos, erros na base)

Rodar da pasta POF2024/harmonizacao:  python scripts/04_resolve.py
"""
import pathlib
import pandas as pd

H = pathlib.Path(__file__).resolve().parents[1]
S = H / "saida"

p = pd.read_csv(S / "propostas_2024.csv", dtype={"Codigo": str, "Cod_harmo": str, "Cod_harmo_sugerido": str})
g = pd.read_csv(H / "base/grupos.csv", dtype=str).set_index("Cod_harmo")

# ---------------------------------------------------------------- decisões explícitas
# codigo: (grupo, confiança, motivo)
DECISOES = {
    # rendimentos e transferências novos
    "503006": ("44001", "MÉDIA", "comissão de venda habitual; o IBGE 2024 classifica como rendimento do trabalho de empregado "
                                 "(tradutor de rendimento, nível 111). Em 2017 só havia a comissão esporádica (55014 → 47001)"),
    "505008": ("45005", "MÉDIA", "Pé-de-Meia: programa governamental de transferência, como os programas de 2017 (54001, 54003 → 45005)"),
    "505007": ("45005", "MÉDIA", "Volta por Cima (RS): auxílio governamental transitório (calamidade), como os programas de 2017 → 45005"),
    "506019": ("45005", "MÉDIA", "MEI RS calamidades: auxílio governamental transitório → 45005"),
    # educação
    "430010": ("41006", "MÉDIA", "FIES (pagamento de financiamento estudantil) = crédito educativo; 2017:48016 CREDITO EDUCATIVO (PAGAMENTO) → 41006"),
    "430011": ("41006", "MÉDIA", "crédito educativo privado (pagamento); 2017:48016 → 41006"),
    "430046": ("37006", "BAIXA", "software (aquisição): mesmo grupo da assinatura (430047); sem análogo direto em 2017"),
    "429003": ("38004", "MÉDIA", "treino funcional ≈ academia; 2017:49024 ACADEMIA → 38004 (e 2024:429001 ACADEMIA → 38004)"),
    # vestuário: R1! a célula 2024 junta aluguel de roupa masculina, feminina e infantil (2017: 33001/33002/33003)
    "411005": ("33002", "BAIXA", "R1: 2024 junta aluguel de roupa M/F/infantil, separados em 2017 (34017→33001, 35020→33002, "
                                 "36020→33003). Atribuída ao maior (feminino) como exceção de valor ínfimo (R$ 0,55/UC); decisão estrutural pendente"),
    "411006": ("33002", "MÉDIA", "aluguel de vestido de noiva; 2017:35033 VESTIDO DE NOIVA → 33002"),
    "411009": ("33004", "BAIXA", "aluguel de calçado, cinto, bolsa: grupo de calçados e apetrechos (33004), não consertos"),
    # recreação, jogos
    "211009": ("38001", "ALTA", "console de videogame; 2017:43002 CONSOLE DE VIDEO GAME → 38001"),
    "211010": ("38001", "ALTA", "acessórios de videogame; 2017:43053 ACESSORIOS DE VIDEO GAME → 38001"),
    "421025": ("38006", "MÉDIA", "ingresso no quadro de viagens; 2017:41022 PARQUE DE DIVERSAO (INGRESSO) em viagem → 38006"),
    "421026": ("38006", "MÉDIA", "ingresso no quadro de viagens; 2017:41023 SHOW (INGRESSO) em viagem → 38006"),
    # consertos de artigos pessoais
    "427008": ("39004", "ALTA", "conserto de joia; 2017:31028 CONSERTO DE JOIAS → 39004"),
    "427009": ("39004", "ALTA", "conserto de relógio; 2017:31018 CONSERTO DE RELOGIO → 39004"),
    "427010": ("39004", "ALTA", "conserto de relógio inteligente; 2017:31018 → 39004"),
    "427011": ("39004", "ALTA", "conserto de relógio de bolso; 2017:31018 → 39004"),
    # transporte e encargos
    "433036": ("43001", "MÉDIA", "outros encargos financeiros e seguros de empréstimo; 2017:48003 SEGURO DE EMPRESTIMO → 43001"),
    "401022": ("34007", "BAIXA", "carga de veículo elétrico: combustível de veículo sem análogo em 2017; vai para outros transportes "
                                 "(onde está o querosene de veículo, 2017:23022) — candidato a grupo próprio no futuro (R5)"),
    # alimentação
    "385011": ("16104", "ALTA", "carne assada ou bife preparado para viagem; 2017:85011 → 16104 (a sugestão apontava carne crua)"),
    # agregados: seguir o agregado do quadro equivalente de 2017
    "412999": ("37005", "MÉDIA", "AGREGADO do quadro de papelaria (2017 Q32 = papelaria → 37005). Na base, 2017:32999 está em 34004 "
                                 "(manutenção de veículo), provável erro da base — ver pendências"),
    "203999": ("40006", "MÉDIA", "AGREGADO do quadro de animais domésticos; 2017:13999 AGREGADO → 40006"),
    "425999": ("31003", "MÉDIA", "AGREGADO do quadro de telefonia celular (serviços); os pacotes do quadro vão para 31003"),
    # animais
    "203001": ("48001", "MÉDIA", "aquisição de animal doméstico = bem, não serviço; grupo 48001 (Bens para animais)"),
    "203004": ("48001", "ALTA", "material higiênico para animal; 2017:87014 SABONETE PARA ANIMAL → 48001"),
}

FRETE_NOME = "FRETE"
# as sugestões BAIXA de maior valor (>= R$ 0,34/UC, 60 células, 95% do valor das BAIXA) foram conferidas
# uma a uma contra a célula 2017 análoga e o quadro; ficam MÉDIA
LIMIAR_CONFERIDAS = 0.34

# ---------------------------------------------------------------- aplica
ok = p[p.tipo == "ATRIBUIR"].copy()
dom_quadro = (ok.groupby(["Quadro_POF", "Cod_harmo"]).valor_uc.sum().reset_index()
                .sort_values("valor_uc", ascending=False).drop_duplicates("Quadro_POF")
                .set_index("Quadro_POF").Cod_harmo)

linhas = []
for x in p.itertuples():
    if x.tipo == "ATRIBUIR":
        linhas.append(dict(Codigo=x.Codigo, tipo="ATRIBUIR", de="", para=x.Cod_harmo, confianca=x.confianca,
                           motivo=x.motivo_ia, revisor="claude-ia (passo 2)"))
        continue
    if x.Codigo in DECISOES:
        para, conf, mot = DECISOES[x.Codigo]
        origem = "decisão explícita"
    elif str(x.Descri_Item).strip() == FRETE_NOME:
        para = dom_quadro.get(x.Quadro_POF)
        conf, mot, origem = "BAIXA", f"FRETE (item novo de 2024): grupo dominante do quadro {x.Quadro_POF}", "regra frete"
    else:
        para = x.Cod_harmo_sugerido
        conf = "MÉDIA" if (pd.notna(x.score) and float(x.score) >= 0.6) else "BAIXA"
        mot = f"aceita a sugestão do passo 2 ({x.motivo_ia})"
        origem = "sugestão aceita"
        if conf == "BAIXA" and x.valor_uc >= LIMIAR_CONFERIDAS:
            conf, origem = "MÉDIA", "sugestão conferida uma a uma pela IA"
    linhas.append(dict(Codigo=x.Codigo, tipo="ATRIBUIR", de=x.Cod_harmo_sugerido if pd.notna(x.Cod_harmo_sugerido) else "",
                       para=para, confianca=conf, motivo=f"[{origem}] {mot}", revisor="claude-ia (passo 4)"))

dec = pd.DataFrame(linhas).merge(p[["Codigo", "Quadro_POF", "Descri_Item", "valor_uc"]], on="Codigo")
assert dec.para.notna().all(), dec[dec.para.isna()]
assert dec.para.isin(g.index).all(), set(dec.para) - set(g.index)
dec["nome_grupo"] = dec.para.map(g.nome)
dec = dec[["Codigo", "Quadro_POF", "Descri_Item", "tipo", "de", "para", "nome_grupo", "confianca",
           "valor_uc", "motivo", "revisor"]]
dec.to_csv(S / "decisoes_2024.csv", index=False, encoding="utf-8")

dp = dec[["Quadro_POF", "Codigo", "Descri_Item", "para"]].rename(columns={"Quadro_POF": "Quadro_H", "para": "Cod_harmo"})
dp.insert(0, "Ano", "2024")
dp.sort_values(["Codigo"]).to_csv(S / "depara_2024_final.csv", index=False, encoding="utf-8")

tot = dec.valor_uc.sum()
r = dec.groupby(["revisor", "confianca"]).agg(celulas=("Codigo", "size"), valor=("valor_uc", "sum"))
r["pct_valor"] = (100 * r.valor / tot).round(2)
print(r)
print("células:", len(dec), "| sem grupo:", dec.para.isna().sum(), "| grupos usados:", dec.para.nunique())
