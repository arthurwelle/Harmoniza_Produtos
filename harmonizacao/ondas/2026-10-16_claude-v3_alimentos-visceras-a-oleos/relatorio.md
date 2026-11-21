# Relatório — 2026-10-16_claude-v3_alimentos-visceras-a-oleos

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 15 MOVER óbvios (18 células), 8 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (23: aceita 23)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 09109 → 09104 | Outlier pontual: os mesmos produtos estão em 09104 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 09109, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 1 | 11204 → 11203 | Outlier pontual: os mesmos produtos estão em 11203 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 11204, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 1 | 11204 → 11205 | Outlier pontual: os mesmos produtos estão em 11205 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 11204, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 1 | 07602 → 10107 | Outlier pontual: os mesmos produtos estão em 10107 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 07602, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 1 | 09109 → 09103 | Outlier pontual: os mesmos produtos estão em 09103 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 09109, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 1 | 11106 → 11204 | Outlier pontual: os mesmos produtos estão em 11204 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 11106, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 2 | 12302 → 12204 | Outlier pontual: os mesmos produtos estão em 12204 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 12302, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 14104 → 14202 | Outlier pontual: os mesmos produtos estão em 14202 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 14104, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | MOVER | **aceita** | 1 | 16103 → 08102 | Outlier pontual: os mesmos produtos estão em 08102 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p10 | MOVER | **aceita** | 2 | 16103 → 09109 | Outlier pontual: os mesmos produtos estão em 09109 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p11 | MOVER | **aceita** | 2 | 16103 → 10107 | Outlier pontual: os mesmos produtos estão em 10107 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p12 | MOVER | **aceita** | 1 | 08103 → 08104 | Outlier pontual: os mesmos produtos estão em 08104 em todas as outras edições em que aparecem (pelo menos 4); só em 2002 a célula está em 08103, sem nenhum item |  | claude-ia (ADR 0005) |
| p13 | MOVER | **aceita** | 1 | 10107 → 10102 | Outlier pontual: os mesmos produtos estão em 10102 em todas as outras edições em que aparecem (pelo menos 3); só em 2002 a célula está em 10107, sem nenhum item |  | claude-ia (ADR 0005) |
| p14 | MOVER | **aceita** | 1 | 12204 → 12302 | Outlier pontual: os mesmos produtos estão em 12302 em todas as outras edições em que aparecem (pelo menos 3); só em 2002 a célula está em 12204, sem nenhum item |  | claude-ia (ADR 0005) |
| p15 | MOVER | **aceita** | 1 | 13207 → 13210 | Outlier pontual: os mesmos produtos estão em 13210 em todas as outras edições em que aparecem (pelo menos 4); só em 2002 a célula está em 13207, sem nenhum item |  | claude-ia (ADR 0005) |
| p16 | REVISAR | **aceita** | 1 | 07506 →  | Os mesmos produtos estão em 08103 nas duas outras edições em que aparecem; em 2002 estão em 07506. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p17 | REVISAR | **aceita** | 1 | 07506 →  | Os mesmos produtos estão em 10107 nas duas outras edições em que aparecem; em 2002 estão em 07506. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p18 | REVISAR | **aceita** | 1 | 07602 →  | Os mesmos produtos estão em 08104 nas duas outras edições em que aparecem; em 2002 estão em 07602. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p19 | REVISAR | **aceita** | 1 | 08103 →  | Os mesmos produtos estão em 08104 nas duas outras edições em que aparecem; em 2002 estão em 08103. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p20 | REVISAR | **aceita** | 1 | 08104 →  | Os mesmos produtos estão em 08102 nas duas outras edições em que aparecem; em 2002 estão em 08104. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p21 | REVISAR | **aceita** | 1 | 10107 →  | Os mesmos produtos estão em 10101 nas duas outras edições em que aparecem; em 2002 estão em 10107. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p22 | REVISAR | **aceita** | 3 | 10107 →  | Os mesmos produtos estão em 10102 nas duas outras edições em que aparecem; em 2002 estão em 10107. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p23 | REVISAR | **aceita** | 2 | 10107 →  | Os mesmos produtos estão em 10202 nas duas outras edições em que aparecem; em 2002 estão em 10107. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 31
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 8
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 07506 | Outras; Cane salgada não especificada; Costela de  | 22 23 19 28 37 | 22 23 19 28 37 |
| 07602 | Outras; Carne de cabrito; Carne de carneiro | 21 10 22 16 18 | 21 9 22 16 18 |
| 08102 | Bovina Outras; Bucho; Língua | 14 14 16 16 17 | 14 15 16 16 17 |
| 08103 | Vísceras suínas | 19 21 25 15 15 | 19 21 24 15 15 |
| 08104 | Outras vísceras | 1 1 14 17 18 | 1 1 15 17 18 |
| 09103 | Corvina fresca | 3 3 7 7 7 | 3 4 7 7 7 |
| 09104 | Pescada em filé fresco | 5 5 7 8 8 | 6 5 7 8 8 |
| 09109 | Outros; Anchova fresca; Bagre fresco; Cação fresco | 408 394 356 356 361 | 407 395 356 356 361 |
| 10102 | Carne de frango não especificada; Carne não especi | 1 1 6 12 14 | 1 1 7 12 14 |
| 10107 | Outras; Dorso de frango; Miúdos de frango; Outras  | 32 24 44 48 53 | 32 27 43 48 53 |
| 11106 | Outros | 10 8 9 14 12 | 10 7 9 14 12 |
| 11203 | Queijo prato | 1 1 1 3 3 | 2 1 1 3 3 |
| 11204 | Outros queijos; Queijo não especificado; Queijo pa | 17 11 10 25 35 | 15 12 10 25 35 |
| 11205 | Requeijão | 1 1 1 2 3 | 2 1 1 2 3 |
| 12204 | Outros; Rapadura; Bombom; Chiclete; Chocolate em t | 27 28 45 74 74 | 27 30 44 74 74 |
| 12302 | Outros; Polpa de fruta; Gelatina; Mel de abelha | 3 6 3 13 15 | 3 4 4 13 15 |
| 13207 | Tempero misto | 1 1 5 10 10 | 1 1 4 10 10 |
| 13210 | Outros; Vinagre não especificado; Coco ralado; Out | 46 59 67 100 122 | 46 59 68 100 122 |
| 14104 | Óleo não especificado; Óleo de girassol; Óleo de c | 15 17 23 26 26 | 15 16 23 26 26 |
| 14202 | Outras; Banha de porco | 9 9 11 11 11 | 9 10 11 11 11 |
| 16103 | Outros produtos | 31 28 22 28 34 | 31 23 22 28 34 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 21 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15103[1995], 15303[2002,2008] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 90 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_alimentos-visceras-a-oleos: 23 decisões (aceita 23)`
