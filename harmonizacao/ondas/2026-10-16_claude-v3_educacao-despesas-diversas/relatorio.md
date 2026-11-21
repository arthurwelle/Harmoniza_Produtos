# Relatório — 2026-10-16_claude-v3_educacao-despesas-diversas

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 18 MOVER óbvios (34 células), 15 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (33: aceita 33)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 34007 → 37006 | Outlier pontual: os mesmos produtos estão em 37006 em todas as outras edições em que aparecem (pelo menos 4); só em 1987 a célula está em 34007, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 1 | 37001 → 37006 | Outlier pontual: os mesmos produtos estão em 37006 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 37001, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 1 | 37002 → 37005 | Outlier pontual: os mesmos produtos estão em 37005 em todas as outras edições em que aparecem (pelo menos 2); só em 1987 a célula está em 37002, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 2 | 37006 → 37005 | Outlier pontual: os mesmos produtos estão em 37005 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 37006, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 3 | 38004 → 37005 | Outlier pontual: os mesmos produtos estão em 37005 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 38004, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 1 | 40006 → 40004 | Outlier pontual: os mesmos produtos estão em 40004 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 40006, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 31007 → 40002 | Outlier pontual: os mesmos produtos estão em 40002 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 31007, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 37003 → 37001 | Outlier pontual: os mesmos produtos estão em 37001 em todas as outras edições em que aparecem (pelo menos 4); só em 1995 a célula está em 37003, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | MOVER | **aceita** | 4 | 37005 → 37006 | Outlier pontual: os mesmos produtos estão em 37006 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 37005, sem nenhum item |  | claude-ia (ADR 0005) |
| p10 | MOVER | **aceita** | 2 | 32003 → 40006 | Outlier pontual: os mesmos produtos estão em 40006 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p11 | MOVER | **aceita** | 3 | 33004 → 40006 | Outlier pontual: os mesmos produtos estão em 40006 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 33004, sem nenhum item |  | claude-ia (ADR 0005) |
| p12 | MOVER | **aceita** | 1 | 35004 → 40006 | Outlier pontual: os mesmos produtos estão em 40006 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 35004, sem nenhum item |  | claude-ia (ADR 0005) |
| p13 | MOVER | **aceita** | 1 | 37005 → 40006 | Outlier pontual: os mesmos produtos estão em 40006 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 37005, sem nenhum item |  | claude-ia (ADR 0005) |
| p14 | MOVER | **aceita** | 2 | 37006 → 37003 | Outlier pontual: os mesmos produtos estão em 37003 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 37006, sem nenhum item |  | claude-ia (ADR 0005) |
| p15 | MOVER | **aceita** | 1 | 38001 → 40006 | Outlier pontual: os mesmos produtos estão em 40006 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 38001, sem nenhum item |  | claude-ia (ADR 0005) |
| p16 | MOVER | **aceita** | 1 | 39005 → 40006 | Outlier pontual: os mesmos produtos estão em 40006 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 39005, sem nenhum item |  | claude-ia (ADR 0005) |
| p17 | MOVER | **aceita** | 7 | 40006 → 40004 | Outlier pontual: os mesmos produtos estão em 40004 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 40006, sem nenhum item |  | claude-ia (ADR 0005) |
| p18 | MOVER | **aceita** | 1 | 42002 → 40006 | Outlier pontual: os mesmos produtos estão em 40006 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 42002, sem nenhum item |  | claude-ia (ADR 0005) |
| p19 | REVISAR | **aceita** | 1 | 31007 →  | Os mesmos produtos estão em 40002 nas duas outras edições em que aparecem; em 1995 estão em 31007. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p20 | REVISAR | **aceita** | 2 | 33004 →  | Os mesmos produtos estão em 40006 nas duas outras edições em que aparecem; em 2017 estão em 33004. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p21 | REVISAR | **aceita** | 1 | 37001 →  | Os mesmos produtos estão em 37003 nas duas outras edições em que aparecem; em 2017 estão em 37001. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p22 | REVISAR | **aceita** | 1 | 37001 →  | Os mesmos produtos estão em 37004 nas duas outras edições em que aparecem; em 1987 estão em 37001. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p23 | REVISAR | **aceita** | 1 | 37001 →  | Os mesmos produtos estão em 37006 nas duas outras edições em que aparecem; em 1995 estão em 37001. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p24 | REVISAR | **aceita** | 1 | 37005 →  | Os mesmos produtos estão em 37006 nas duas outras edições em que aparecem; em 1995 estão em 37005. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p25 | REVISAR | **aceita** | 3 | 38005 →  | Os mesmos produtos estão em 37005 nas duas outras edições em que aparecem; em 2017 estão em 38005. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p26 | REVISAR | **aceita** | 1 | 41006 →  | Os mesmos nomes de produto estão em 40006 nas outras edições, mas a célula está em 41006, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p27 | REVISAR | **aceita** | 1 | 42002 →  | Os mesmos nomes de produto estão em 40003 nas outras edições, mas a célula está em 42002, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p28 | REVISAR | **aceita** | 1 | 32001 →  | As outras edições põem os mesmos produtos em 40006, mas o tradutor do IBGE confirma o grupo atual (32001) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p29 | REVISAR | **aceita** | 1 | 37006 →  | As outras edições põem os mesmos produtos em 37003, mas o tradutor do IBGE confirma o grupo atual (37006) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p30 | REVISAR | **aceita** | 1 | 39001 →  | As outras edições põem os mesmos produtos em 40006, mas o tradutor do IBGE confirma o grupo atual (39001) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p31 | REVISAR | **aceita** | 1 | 40003 →  | As outras edições põem os mesmos produtos em 40004, mas o tradutor do IBGE confirma o grupo atual (40003) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p32 | REVISAR | **aceita** | 1 | 40006 →  | As outras edições põem os mesmos produtos em 37006, mas o tradutor do IBGE confirma o grupo atual (40006) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p33 | REVISAR | **aceita** | 1 | 42002 →  | As outras edições põem os mesmos produtos em 40006, mas o tradutor do IBGE confirma o grupo atual (42002) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 62
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 15
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 31007 | Outros servicos etc | 18 35 32 37 38 | 18 34 32 37 38 |
| 32001 | Manutencao do lar | 29 103 142 121 100 | 29 103 142 121 100 |
| 32003 | Mobiliarios e artigos do lar | 270 282 332 332 439 | 270 282 332 332 437 |
| 33004 | Calcados e apetrechos | 42 39 50 70 57 | 42 39 50 70 54 |
| 34007 | Outros transporte | 3 14 10 11 15 | 2 14 10 11 15 |
| 35004 | Produtos de uso pessoal | 32 35 46 40 31 | 32 35 46 40 30 |
| 37001 | Cursos regulares | 5 3 4 3 36 | 4 4 4 3 36 |
| 37002 | Curso superior | 5 2 3 4 7 | 4 2 3 4 7 |
| 37003 | Outros cursos | 1 18 20 55 62 | 1 17 20 55 64 |
| 37005 | Artigos escolares | 1 25 16 8 69 | 7 21 16 8 68 |
| 37006 | Outras educacao | 15 8 23 24 28 | 15 12 23 24 26 |
| 38001 | Brinquedos e jogos | 7 8 7 3 57 | 7 8 7 3 56 |
| 38004 | Diversoes e esportes | 36 55 63 43 31 | 33 55 63 43 31 |
| 38005 | Outras recreacao etc | 31 27 42 89 77 | 31 27 42 89 77 |
| 39001 | Fumo | 20 22 21 23 26 | 20 22 21 23 26 |
| 39005 | Outras servicos pessoais | 11 19 24 25 25 | 11 19 24 25 24 |
| 40002 | Comunicacao | 4 0 6 6 8 | 4 1 6 6 8 |
| 40003 | Cerimonias e festas | 12 12 17 17 30 | 12 12 17 17 30 |
| 40004 | Servicos profissionais | 14 20 20 20 0 | 15 20 20 20 7 |
| 40006 | Outras despesas diversas | 68 63 61 79 65 | 67 63 61 79 68 |
| 41006 | Outras despesas | 9 13 22 82 28 | 9 13 22 82 28 |
| 42002 | Imovel reforma | 73 11 77 86 104 | 73 11 77 86 103 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 17 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 125 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_educacao-despesas-diversas: 33 decisões (aceita 33)`
