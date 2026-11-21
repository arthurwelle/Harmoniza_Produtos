# Relatório — 2026-10-16_claude-v3_alimentos-cereais-hortalicas-frutas

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 8 MOVER óbvios (10 células), 4 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (12: aceita 12)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 01208 → 01201 | Outlier pontual: os mesmos produtos estão em 01201 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 01208, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 1 | 13210 → 02212 | Outlier pontual: os mesmos produtos estão em 02212 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 13210, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 2 | 02107 → 02103 | Outlier pontual: os mesmos produtos estão em 02103 em todas as outras edições em que aparecem (pelo menos 4); só em 1995 a célula está em 02107, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 2 | 03205 → 03118 | Outlier pontual: os mesmos produtos estão em 03118 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 03205, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 1 | 13210 → 02212 | Outlier pontual: os mesmos produtos estão em 02212 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 13210, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 1 | 16103 → 02212 | Outlier pontual: os mesmos produtos estão em 02212 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 01199 → 01299 | Outlier pontual: os mesmos produtos estão em 01299 em todas as outras edições em que aparecem (pelo menos 4); só em 2002 a célula está em 01199, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 01299 → 01203 | Outlier pontual: os mesmos produtos estão em 01203 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 01299, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | REVISAR | **aceita** | 1 | 02309 →  | Os mesmos produtos estão em 01101 nas duas outras edições em que aparecem; em 2002 estão em 02309. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p10 | REVISAR | **aceita** | 1 | 03205 →  | Os mesmos produtos estão em 03118 nas duas outras edições em que aparecem; em 2002 estão em 03205. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p11 | REVISAR | **aceita** | 1 | 16016 →  | Os mesmos produtos estão em 01199 nas duas outras edições em que aparecem; em 2002 estão em 16016. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p12 | REVISAR | **aceita** | 1 | 16103 →  | Os mesmos produtos estão em 01299 nas duas outras edições em que aparecem; em 2002 estão em 16103. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 11
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 4
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 01199 | Outros | 4 4 2 3 4 | 4 4 1 3 4 |
| 01201 | Feijão-fradinho | 1 1 1 2 2 | 2 1 1 2 2 |
| 01203 | Feijão-manteiga | 1 1 1 1 1 | 1 1 1 1 2 |
| 01208 | Outros feijões | 11 10 7 9 11 | 10 10 7 9 11 |
| 01299 | Outras | 1 1 0 6 8 | 1 1 1 6 7 |
| 02103 | Cheiro-verde | 3 1 3 3 5 | 3 3 3 3 5 |
| 02107 | Outras; Acelga | 23 24 25 32 56 | 23 22 25 32 56 |
| 02212 | Outras; Maxixe; Azeitona em conserva; Outros feijõ | 17 16 28 37 41 | 18 18 28 37 41 |
| 02309 | Outras; Cará | 7 7 7 11 14 | 7 7 7 11 14 |
| 03118 | Outras; Outras laranjas; Goiaba; Acerola | 9 9 38 50 56 | 9 11 38 50 56 |
| 03205 | Outras; Pêssego; Morango; Ameixa | 47 53 19 23 26 | 47 51 19 23 26 |
| 13210 | Outros; Vinagre não especificado; Coco ralado; Out | 47 60 67 100 122 | 46 59 67 100 122 |
| 16016 | Outros | 0 0 1 0 0 | 0 0 1 0 0 |
| 16103 | Outros produtos | 31 31 22 28 34 | 31 30 22 28 34 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 22 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 07203[2002], 15103[1995] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 64 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_alimentos-cereais-hortalicas-frutas: 12 decisões (aceita 12)`
