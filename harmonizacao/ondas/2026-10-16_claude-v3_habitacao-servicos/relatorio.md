# Relatório — 2026-10-16_claude-v3_habitacao-servicos

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 21 MOVER óbvios (49 células), 16 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (37: aceita 37)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 2 | 32004 → 32003 | Outlier pontual: os mesmos produtos estão em 32003 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 32004, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 1 | 40006 → 32003 | Outlier pontual: os mesmos produtos estão em 32003 em todas as outras edições em que aparecem (pelo menos 4); só em 1987 a célula está em 40006, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 2 | 32003 → 32002 | Outlier pontual: os mesmos produtos estão em 32002 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 4 | 32003 → 32004 | Outlier pontual: os mesmos produtos estão em 32004 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 2 | 32002 → 32003 | Outlier pontual: os mesmos produtos estão em 32003 em todas as outras edições em que aparecem (pelo menos 3); só em 2002 a célula está em 32002, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 1 | 32005 → 32003 | Outlier pontual: os mesmos produtos estão em 32003 em todas as outras edições em que aparecem (pelo menos 4); só em 2002 a célula está em 32005, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 32003 → 32002 | Outlier pontual: os mesmos produtos estão em 32002 em todas as outras edições em que aparecem (pelo menos 2); só em 2008 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 32001 → 32002 | Outlier pontual: os mesmos produtos estão em 32002 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 32001, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | MOVER | **aceita** | 3 | 32003 → 32002 | Outlier pontual: os mesmos produtos estão em 32002 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p10 | MOVER | **aceita** | 1 | 32003 → 32004 | Outlier pontual: os mesmos produtos estão em 32004 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p11 | MOVER | **aceita** | 1 | 32004 → 32003 | Outlier pontual: os mesmos produtos estão em 32003 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 32004, sem nenhum item |  | claude-ia (ADR 0005) |
| p12 | MOVER | **aceita** | 1 | 37005 → 32003 | Outlier pontual: os mesmos produtos estão em 32003 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 37005, sem nenhum item |  | claude-ia (ADR 0005) |
| p13 | MOVER | **aceita** | 1 | 38001 → 32004 | Outlier pontual: os mesmos produtos estão em 32004 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 38001, sem nenhum item |  | claude-ia (ADR 0005) |
| p14 | MOVER | **aceita** | 11 | 38005 → 32003 | Outlier pontual: os mesmos produtos estão em 32003 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 38005, sem nenhum item |  | claude-ia (ADR 0005) |
| p15 | MOVER | **aceita** | 2 | 38005 → 32004 | Outlier pontual: os mesmos produtos estão em 32004 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 38005, sem nenhum item |  | claude-ia (ADR 0005) |
| p16 | MOVER | **aceita** | 1 | 40006 → 32003 | Outlier pontual: os mesmos produtos estão em 32003 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 40006, sem nenhum item |  | claude-ia (ADR 0005) |
| p17 | MOVER | **aceita** | 3 | 40006 → 32004 | Outlier pontual: os mesmos produtos estão em 32004 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 40006, sem nenhum item |  | claude-ia (ADR 0005) |
| p18 | MOVER | **aceita** | 3 | 42001 → 31007 | Outlier pontual: os mesmos produtos estão em 31007 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 42001, sem nenhum item |  | claude-ia (ADR 0005) |
| p19 | REVISAR | **aceita** | 1 | 14104 →  | Os mesmos produtos estão em 32002 nas duas outras edições em que aparecem; em 2002 estão em 14104. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p20 | REVISAR | **aceita** | 1 | 31005 →  | Os mesmos produtos estão em 32001 nas duas outras edições em que aparecem; em 1987 estão em 31005. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p21 | REVISAR | **aceita** | 1 | 31007 →  | Os mesmos produtos estão em 32001 nas duas outras edições em que aparecem; em 2002 estão em 31007. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p22 | REVISAR | **aceita** | 2 | 32003 →  | Os mesmos produtos estão em 32002 nas duas outras edições em que aparecem; em 1995 estão em 32003. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p23 | REVISAR | **aceita** | 1 | 32003 →  | Os mesmos produtos estão em 32004 nas duas outras edições em que aparecem; em 1995 estão em 32003. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p24 | REVISAR | **aceita** | 1 | 32005 →  | Os mesmos produtos estão em 32003 nas duas outras edições em que aparecem; em 2002 estão em 32005. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p25 | REVISAR | **aceita** | 1 | 38001 →  | Os mesmos produtos estão em 32004 nas duas outras edições em que aparecem; em 2017 estão em 38001. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p26 | REVISAR | **aceita** | 1 | 40006 →  | Os mesmos produtos estão em 31007 nas duas outras edições em que aparecem; em 2002 estão em 40006. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p27 | REVISAR | **aceita** | 2 | 42001 →  | Os mesmos nomes de produto estão em 32005 nas outras edições, mas a célula está em 42001, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p28 | REVISAR | **aceita** | 1 | 44001 →  | Os mesmos nomes de produto estão em 32001 nas outras edições, mas a célula está em 44001, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p29 | REVISAR | **aceita** | 1 | 88888 →  | Os mesmos nomes de produto estão em 32003 nas outras edições, mas a célula está em 88888, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p30 | REVISAR | **aceita** | 1 | 88888 →  | Os mesmos nomes de produto estão em 32004 nas outras edições, mas a célula está em 88888, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p31 | REVISAR | **aceita** | 2 | 32001 →  | As outras edições põem os mesmos produtos em 32003, mas o tradutor do IBGE confirma o grupo atual (32001) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p32 | REVISAR | **aceita** | 2 | 32003 →  | As outras edições põem os mesmos produtos em 32004, mas o tradutor do IBGE confirma o grupo atual (32003) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p33 | REVISAR | **aceita** | 2 | 42002 →  | As outras edições põem os mesmos produtos em 32003, mas o tradutor do IBGE confirma o grupo atual (42002) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p34 | MOVER | **aceita** | 3 | 40006;41006 → 31007 | Quebra de série: o mesmo gasto (condomínio do domicílio principal) está em três grupos diferentes ao longo das edições, e em 2008/2017 cai fora do consumo. Estr |  | claude-ia (ADR 0005) |
| p35 | MOVER | **aceita** | 2 | 31007;32001 → 41001 | Três edições unânimes e o IBGE concordam: imposto é outra despesa corrente, não manutenção do lar nem serviço. Os dois anos antigos estão cada um num grupo dife |  | claude-ia (ADR 0005) |
| p36 | MOVER | **aceita** | 3 | 31007;40006;41006 → 31001 | Mesma despesa espalhada por três grupos; 2002/2008 e o IBGE concordam em Aluguel. Duas fontes ⇒ ALTA. |  | claude-ia (ADR 0005) |
| p37 | REVISAR | **aceita** | 5 | 40003;42002 →  | Série partida em dois critérios. Não é deslize de um ano: é decisão de onde fica gasto com jazigo (investimento em imóvel ou cerimônia/serviço funerário). Recom |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 69
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 16
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 14104 | Óleo não especificado; Óleo de girassol; Óleo de c | 15 16 23 26 26 | 15 16 23 26 26 |
| 31001 | Aluguel | 3 3 5 4 4 | 4 4 5 4 5 |
| 31005 | Gas domestico | 3 3 2 2 2 | 3 3 2 2 2 |
| 31007 | Outros servicos etc | 17 37 32 36 34 | 18 35 32 37 38 |
| 32001 | Manutencao do lar | 30 103 142 121 101 | 29 103 142 121 100 |
| 32002 | Artigos de limpeza | 42 42 64 56 58 | 42 44 62 57 62 |
| 32003 | Mobiliarios e artigos do lar | 267 288 329 333 429 | 270 282 332 332 439 |
| 32004 | Eletrodomesticos | 106 120 150 152 125 | 104 124 150 152 131 |
| 32005 | Consertos de artigos do lar | 17 67 81 157 227 | 17 67 80 157 227 |
| 37005 | Artigos escolares | 1 25 16 8 70 | 1 25 16 8 69 |
| 38001 | Brinquedos e jogos | 7 8 7 3 58 | 7 8 7 3 57 |
| 38005 | Outras recreacao etc | 31 27 42 89 90 | 31 27 42 89 77 |
| 40003 | Cerimonias e festas | 12 12 17 17 30 | 12 12 17 17 30 |
| 40006 | Outras despesas diversas | 71 63 61 79 69 | 68 63 61 79 65 |
| 41001 | Impostos | 0 40 17 76 18 | 1 41 17 76 18 |
| 41006 | Outras despesas | 9 13 22 83 30 | 9 13 22 82 28 |
| 42001 | Imovel aquisicao | 3 11 7 11 10 | 3 11 7 11 7 |
| 42002 | Imovel reforma | 73 11 77 86 104 | 73 11 77 86 104 |
| 44001 | Empregado | 1 5 14 27 8 | 1 5 14 27 8 |
| 88888 | Inventário | 28 33 33 32 32 | 28 33 33 32 32 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 19 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 110 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_habitacao-servicos: 37 decisões (aceita 37)`
