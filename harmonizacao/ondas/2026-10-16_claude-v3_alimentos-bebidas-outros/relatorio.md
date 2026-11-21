# Relatório — 2026-10-16_claude-v3_alimentos-bebidas-outros

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 15 MOVER óbvios (24 células), 4 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (19: aceita 19)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 15101 → 15104 | Outlier pontual: os mesmos produtos estão em 15104 em todas as outras edições em que aparecem (pelo menos 4); só em 1987 a célula está em 15101, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 2 | 15104 → 15101 | Outlier pontual: os mesmos produtos estão em 15101 em todas as outras edições em que aparecem (pelo menos 4); só em 1987 a célula está em 15104, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 1 | 15104 → 15102 | Outlier pontual: os mesmos produtos estão em 15102 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 15104, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 1 | 16103 → 16104 | Outlier pontual: os mesmos produtos estão em 16104 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 1 | 06104 → 16106 | Outlier pontual: os mesmos produtos estão em 16106 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 06104, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 2 | 15101 → 15206 | Outlier pontual: os mesmos produtos estão em 15206 em todas as outras edições em que aparecem (pelo menos 4); só em 1995 a célula está em 15101, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 15102 → 15206 | Outlier pontual: os mesmos produtos estão em 15206 em todas as outras edições em que aparecem (pelo menos 4); só em 1995 a célula está em 15102, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 15102 → 15402 | Outlier pontual: os mesmos produtos estão em 15402 em todas as outras edições em que aparecem (pelo menos 4); só em 1995 a célula está em 15102, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | MOVER | **aceita** | 1 | 15104 → 15103 | Outlier pontual: os mesmos produtos estão em 15103 em todas as outras edições em que aparecem (pelo menos 4); só em 1995 a célula está em 15104, sem nenhum item |  | claude-ia (ADR 0005) |
| p10 | MOVER | **aceita** | 2 | 15104 → 15206 | Outlier pontual: os mesmos produtos estão em 15206 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 15104, sem nenhum item |  | claude-ia (ADR 0005) |
| p11 | MOVER | **aceita** | 1 | 15104 → 15208 | Outlier pontual: os mesmos produtos estão em 15208 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 15104, sem nenhum item |  | claude-ia (ADR 0005) |
| p12 | MOVER | **aceita** | 2 | 15104 → 15402 | Outlier pontual: os mesmos produtos estão em 15402 em todas as outras edições em que aparecem (pelo menos 4); só em 1995 a célula está em 15104, sem nenhum item |  | claude-ia (ADR 0005) |
| p13 | MOVER | **aceita** | 1 | 16101 → 16104 | Outlier pontual: os mesmos produtos estão em 16104 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 16101, sem nenhum item |  | claude-ia (ADR 0005) |
| p14 | MOVER | **aceita** | 6 | 16103 → 16104 | Outlier pontual: os mesmos produtos estão em 16104 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p15 | MOVER | **aceita** | 1 | 15101 → 15104 | Outlier pontual: os mesmos produtos estão em 15104 em todas as outras edições em que aparecem (pelo menos 3); só em 2002 a célula está em 15101, sem nenhum item |  | claude-ia (ADR 0005) |
| p16 | REVISAR | **aceita** | 3 | 07208 →  | Os mesmos produtos estão em 16103 nas duas outras edições em que aparecem; em 2002 estão em 07208. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p17 | REVISAR | **aceita** | 1 | 10107 →  | Os mesmos produtos estão em 16103 nas duas outras edições em que aparecem; em 2002 estão em 10107. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p18 | REVISAR | **aceita** | 1 | 15101 →  | Os mesmos produtos estão em 15208 nas duas outras edições em que aparecem; em 1995 estão em 15101. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p19 | REVISAR | **aceita** | 2 | 15209 →  | Os mesmos produtos estão em 15208 nas duas outras edições em que aparecem; em 2002 estão em 15209. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 35
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 4
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 06104 | Pão caseiro; Pão de forma de padaria; Pão de milho | 22 19 22 56 58 | 22 18 22 56 58 |
| 07208 | Outros Capa de filé; Carne não especificada; Carne | 18 15 33 26 31 | 18 15 33 26 31 |
| 10107 | Outras; Dorso de frango; Miúdos de frango; Outras  | 32 27 43 48 53 | 32 27 43 48 53 |
| 15101 | Outras aguardentes; Aguardente de cana | 4 9 8 15 15 | 5 7 7 15 15 |
| 15102 | Cerveja | 5 7 6 10 9 | 6 5 6 10 9 |
| 15103 | Vinho | 1 0 1 4 4 | 1 1 1 4 4 |
| 15104 | Outras | 22 36 23 31 33 | 20 30 24 31 33 |
| 15206 | Outros refrigerantes; Refrigerante não especificad | 22 17 28 69 68 | 22 22 28 69 68 |
| 15208 | Suco de fruta envasado | 5 4 8 28 28 | 5 5 8 28 28 |
| 15209 | Outras | 1 2 8 8 14 | 1 2 8 8 14 |
| 15402 | Outros; Chá preto | 43 7 15 29 46 | 43 10 15 29 46 |
| 16101 | Frango assado ou defumado | 1 1 0 0 0 | 1 0 0 0 0 |
| 16103 | Outros produtos | 31 23 22 28 34 | 30 17 22 28 34 |
| 16104 | Refeição; Refeição pronta | 22 37 77 129 242 | 23 44 77 129 242 |
| 16106 | Mistura para bolo; Mistura industrial para bolo | 1 1 2 2 2 | 1 2 2 2 2 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 20 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 94 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_alimentos-bebidas-outros: 19 decisões (aceita 19)`
