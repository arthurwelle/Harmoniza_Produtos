# Relatório — 2026-10-16_claude-v3_alimentos-cocos-farinhas-panif-carnes

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 16 MOVER óbvios (18 células), 18 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (34: aceita 34)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 05105 → 05206 | Outlier pontual: os mesmos produtos estão em 05206 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 05105, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 1 | 07208 → 07205 | Outlier pontual: os mesmos produtos estão em 07205 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 07208, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 1 | 07506 → 07208 | Outlier pontual: os mesmos produtos estão em 07208 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 07506, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 1 | 07506 → 07502 | Outlier pontual: os mesmos produtos estão em 07502 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 07506, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 2 | 07506 → 07601 | Outlier pontual: os mesmos produtos estão em 07601 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 07506, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 1 | 07506 → 07602 | Outlier pontual: os mesmos produtos estão em 07602 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 07506, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 08101 → 07208 | Outlier pontual: os mesmos produtos estão em 07208 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 08101, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 07103 → 07208 | Outlier pontual: os mesmos produtos estão em 07208 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 07103, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | MOVER | **aceita** | 1 | 07208 → 07602 | Outlier pontual: os mesmos produtos estão em 07602 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 07208, sem nenhum item |  | claude-ia (ADR 0005) |
| p10 | MOVER | **aceita** | 1 | 07506 → 07602 | Outlier pontual: os mesmos produtos estão em 07602 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 07506, sem nenhum item |  | claude-ia (ADR 0005) |
| p11 | MOVER | **aceita** | 1 | 16103 → 07501 | Outlier pontual: os mesmos produtos estão em 07501 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p12 | MOVER | **aceita** | 1 | 16103 → 07506 | Outlier pontual: os mesmos produtos estão em 07506 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p13 | MOVER | **aceita** | 1 | 07102 → 07203 | Outlier pontual: os mesmos produtos estão em 07203 em todas as outras edições em que aparecem (pelo menos 4); só em 2002 a célula está em 07102, sem nenhum item |  | claude-ia (ADR 0005) |
| p14 | MOVER | **aceita** | 1 | 16102 → 05303 | Outlier pontual: os mesmos produtos estão em 05303 em todas as outras edições em que aparecem (pelo menos 3); só em 2002 a célula está em 16102, sem nenhum item |  | claude-ia (ADR 0005) |
| p15 | MOVER | **aceita** | 1 | 16104 → 07208 | Outlier pontual: os mesmos produtos estão em 07208 em todas as outras edições em que aparecem (pelo menos 3); só em 2002 a célula está em 16104, sem nenhum item |  | claude-ia (ADR 0005) |
| p16 | MOVER | **aceita** | 2 | 07103 → 07101 | Outlier pontual: os mesmos produtos estão em 07101 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 07103, sem nenhum item |  | claude-ia (ADR 0005) |
| p17 | REVISAR | **aceita** | 1 | 03205 →  | Os mesmos produtos estão em 04104 nas duas outras edições em que aparecem; em 2002 estão em 03205. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p18 | REVISAR | **aceita** | 1 | 05105 →  | Os mesmos produtos estão em 05103 nas duas outras edições em que aparecem; em 1987 estão em 05105. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p19 | REVISAR | **aceita** | 1 | 06101 →  | Os mesmos produtos estão em 06104 nas duas outras edições em que aparecem; em 2002 estão em 06101. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p20 | REVISAR | **aceita** | 1 | 06303 →  | Os mesmos produtos estão em 06302 nas duas outras edições em que aparecem; em 2002 estão em 06303. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p21 | REVISAR | **aceita** | 2 | 07208 →  | Os mesmos produtos estão em 07103 nas duas outras edições em que aparecem; em 2002 estão em 07208. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p22 | REVISAR | **aceita** | 1 | 07208 →  | Os mesmos produtos estão em 07205 nas duas outras edições em que aparecem; em 2002 estão em 07208. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p23 | REVISAR | **aceita** | 1 | 07208 →  | Os mesmos produtos estão em 07403 nas duas outras edições em que aparecem; em 2002 estão em 07208. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p24 | REVISAR | **aceita** | 1 | 07208 →  | Os mesmos produtos estão em 07506 nas duas outras edições em que aparecem; em 2002 estão em 07208. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p25 | REVISAR | **aceita** | 1 | 07506 →  | Os mesmos produtos estão em 07602 nas duas outras edições em que aparecem; em 2002 estão em 07506. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p26 | REVISAR | **aceita** | 1 | 07602 →  | Os mesmos produtos estão em 07402 nas duas outras edições em que aparecem; em 2002 estão em 07602. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p27 | REVISAR | **aceita** | 1 | 07602 →  | Os mesmos produtos estão em 07404 nas duas outras edições em que aparecem; em 2002 estão em 07602. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p28 | REVISAR | **aceita** | 1 | 08102 →  | Os mesmos produtos estão em 07208 nas duas outras edições em que aparecem; em 2002 estão em 08102. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p29 | REVISAR | **aceita** | 1 | 08103 →  | Os mesmos produtos estão em 07103 nas duas outras edições em que aparecem; em 2002 estão em 08103. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p30 | REVISAR | **aceita** | 1 | 08103 →  | Os mesmos produtos estão em 07506 nas duas outras edições em que aparecem; em 2002 estão em 08103. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p31 | REVISAR | **aceita** | 1 | 08104 →  | Os mesmos produtos estão em 07506 nas duas outras edições em que aparecem; em 2002 estão em 08104. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p32 | REVISAR | **aceita** | 3 | 12204 →  | Os mesmos produtos estão em 06201 nas duas outras edições em que aparecem; em 2002 estão em 12204. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p33 | REVISAR | **aceita** | 1 | 12204 →  | Os mesmos produtos estão em 06303 nas duas outras edições em que aparecem; em 2002 estão em 12204. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p34 | REVISAR | **aceita** | 1 | 16103 →  | Os mesmos produtos estão em 05104 nas duas outras edições em que aparecem; em 2008 estão em 16103. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 32
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 18
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 03205 | Outras; Pêssego; Morango; Ameixa | 47 51 19 23 26 | 47 51 19 23 26 |
| 05105 | Outras | 13 10 11 15 23 | 12 10 11 15 23 |
| 05206 | Flocos de cereal; Flocos de aveia; Flocos de outro | 7 7 5 12 21 | 8 7 5 12 21 |
| 05303 | Massa de pizza; Outras; Massa de lasanha | 12 12 9 18 22 | 12 12 10 18 22 |
| 06101 | Pão de forma industrializado | 3 3 2 4 4 | 3 3 2 4 4 |
| 06303 | Biscoito não especificado; Rosca doce; Rosca não e | 7 7 7 15 28 | 7 7 7 15 28 |
| 07101 | Alcatra | 1 1 1 2 2 | 1 1 1 2 4 |
| 07102 | Carne moída | 1 1 2 2 2 | 1 1 1 2 2 |
| 07103 | Carne não especificada | 2 2 6 5 9 | 2 1 6 5 7 |
| 07203 | Carne moída | 2 2 0 2 2 | 2 2 1 2 2 |
| 07205 | Músculo | 1 1 1 3 3 | 2 1 1 3 3 |
| 07208 | Outros Capa de filé; Carne não especificada; Carne | 17 15 32 26 31 | 18 15 33 26 31 |
| 07501 | Mortadela | 1 1 2 3 3 | 1 2 2 3 3 |
| 07502 | Presunto | 1 1 2 7 9 | 2 1 2 7 9 |
| 07506 | Outras; Cane salgada não especificada; Costela de  | 27 23 19 28 37 | 22 23 19 28 37 |
| 07601 | Linguiça | 4 4 3 2 2 | 6 4 3 2 2 |
| 07602 | Outras; Carne de cabrito; Carne de carneiro | 20 8 22 16 18 | 21 10 22 16 18 |
| 08101 | Bovina Fígado | 4 3 3 3 4 | 3 3 3 3 4 |
| 08102 | Bovina Outras; Bucho; Língua | 14 14 16 16 17 | 14 14 16 16 17 |
| 08103 | Vísceras suínas | 19 21 25 15 15 | 19 21 25 15 15 |
| 08104 | Outras vísceras | 1 1 14 17 18 | 1 1 14 17 18 |
| 12204 | Outros; Rapadura; Bombom; Chiclete; Chocolate em t | 27 28 45 74 74 | 27 28 45 74 74 |
| 16102 | Massa; Massa preparada | 2 2 3 1 0 | 2 2 2 1 0 |
| 16103 | Outros produtos | 31 30 22 28 34 | 31 28 22 28 34 |
| 16104 | Refeição; Refeição pronta | 22 37 78 129 242 | 22 37 77 129 242 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 21 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15103[1995], 15303[2002,2008] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 82 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_alimentos-cocos-farinhas-panif-carnes: 34 decisões (aceita 34)`
