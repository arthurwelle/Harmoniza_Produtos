# Relatório — 2026-10-16_claude-v3_nao-consumo

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 14 MOVER óbvios (21 células), 12 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (26: aceita 26)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 47004 → 45005 | Outlier pontual: os mesmos produtos estão em 45005 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 47004, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 1 | 47004 → 47002 | Outlier pontual: os mesmos produtos estão em 47002 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 47004, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 1 | 44001 → 47004 | Outlier pontual: os mesmos produtos estão em 47004 em todas as outras edições em que aparecem (pelo menos 3); só em 2008 a célula está em 44001, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 1 | 45005 → 45003 | Outlier pontual: os mesmos produtos estão em 45003 em todas as outras edições em que aparecem (pelo menos 4); só em 2008 a célula está em 45005, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 1 | 47004 → 47001 | Outlier pontual: os mesmos produtos estão em 47001 em todas as outras edições em que aparecem (pelo menos 3); só em 2008 a célula está em 47004, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 1 | 47004 → 47003 | Outlier pontual: os mesmos produtos estão em 47003 em todas as outras edições em que aparecem (pelo menos 3); só em 2008 a célula está em 47004, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 32004 → 42003 | Outlier pontual: os mesmos produtos estão em 42003 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 32004, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 3 | 34007 → 41001 | Outlier pontual: os mesmos produtos estão em 41001 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 34007, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | MOVER | **aceita** | 1 | 40006 → 41006 | Outlier pontual: os mesmos produtos estão em 41006 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 40006, sem nenhum item |  | claude-ia (ADR 0005) |
| p10 | MOVER | **aceita** | 1 | 41006 → 41002 | Outlier pontual: os mesmos produtos estão em 41002 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 41006, sem nenhum item |  | claude-ia (ADR 0005) |
| p11 | MOVER | **aceita** | 5 | 41006 → 41004 | Outlier pontual: os mesmos produtos estão em 41004 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 41006, sem nenhum item |  | claude-ia (ADR 0005) |
| p12 | MOVER | **aceita** | 2 | 41006 → 42003 | Outlier pontual: os mesmos produtos estão em 42003 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 41006, sem nenhum item |  | claude-ia (ADR 0005) |
| p13 | MOVER | **aceita** | 1 | 41006 → 43001 | Outlier pontual: os mesmos produtos estão em 43001 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 41006, sem nenhum item |  | claude-ia (ADR 0005) |
| p14 | MOVER | **aceita** | 1 | 47004 → 45005 | Outlier pontual: os mesmos produtos estão em 45005 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 47004, sem nenhum item |  | claude-ia (ADR 0005) |
| p15 | REVISAR | **aceita** | 1 | 44001 →  | Os mesmos produtos estão em 45005 nas duas outras edições em que aparecem; em 2008 estão em 44001. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p16 | REVISAR | **aceita** | 1 | 47004 →  | Os mesmos produtos estão em 44001 nas duas outras edições em que aparecem; em 1995 estão em 47004. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p17 | REVISAR | **aceita** | 1 | 47004 →  | Os mesmos produtos estão em 45005 nas duas outras edições em que aparecem; em 1995 estão em 47004. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p18 | REVISAR | **aceita** | 28 | 32001 →  | Os mesmos nomes de produto estão em 41002 nas outras edições, mas a célula está em 32001, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p19 | REVISAR | **aceita** | 1 | 32001 →  | Os mesmos nomes de produto estão em 42002 nas outras edições, mas a célula está em 32001, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p20 | REVISAR | **aceita** | 1 | 34005 →  | Os mesmos nomes de produto estão em 88888 nas outras edições, mas a célula está em 34005, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p21 | REVISAR | **aceita** | 2 | 40005 →  | Os mesmos nomes de produto estão em 42002 nas outras edições, mas a célula está em 40005, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p22 | REVISAR | **aceita** | 3 | 41001 →  | Os mesmos nomes de produto estão em 46001 nas outras edições, mas a célula está em 41001, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p23 | REVISAR | **aceita** | 6 | 41001 →  | Os mesmos nomes de produto estão em 47003 nas outras edições, mas a célula está em 41001, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p24 | REVISAR | **aceita** | 1 | 41006 →  | As outras edições põem os mesmos produtos em 41004, mas o tradutor do IBGE confirma o grupo atual (41006) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p25 | REVISAR | **aceita** | 7 | 47004 →  | As outras edições põem os mesmos produtos em 44001, mas o tradutor do IBGE confirma o grupo atual (47004) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p26 | REVISAR | **aceita** | 11 | 40005;41006;42001 →  | Comprar imóvel é investimento (aumento do ativo), não consumo; o próprio repositório trata assim a compra do domicílio principal. Para outros imóveis o critério |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 64
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 12
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 32001 | Manutencao do lar | 29 103 142 121 100 | 29 103 142 121 100 |
| 32004 | Eletrodomesticos | 104 123 149 152 131 | 104 123 149 152 130 |
| 34005 | Aquisicao de veiculos | 14 21 21 24 26 | 14 21 21 24 26 |
| 34007 | Outros transporte | 2 12 10 11 16 | 2 12 10 11 13 |
| 40005 | Imoveis de uso ocasional | 16 18 15 19 26 | 16 18 15 19 26 |
| 40006 | Outras despesas diversas | 65 63 61 79 68 | 65 63 61 79 67 |
| 41001 | Impostos | 1 41 17 76 15 | 1 41 17 76 18 |
| 41002 | Contribuicoes trabalhistas | 3 51 4 44 2 | 3 51 4 44 3 |
| 41004 | Pensoes mesadas e doacoes | 7 11 10 11 4 | 7 11 10 11 9 |
| 41006 | Outras despesas | 9 13 22 82 27 | 9 13 22 82 19 |
| 42001 | Imovel aquisicao | 3 11 7 11 7 | 3 11 7 11 7 |
| 42003 | Outros investimentos | 1 2 8 7 0 | 1 2 8 7 3 |
| 43001 | Emprestimo e carne | 4 4 4 5 3 | 4 4 4 5 4 |
| 44001 | Empregado | 1 5 14 27 8 | 1 5 14 26 8 |
| 45003 | Bolsa de estudo | 1 1 1 0 1 | 1 1 1 1 1 |
| 45005 | Transferencias transitorias | 9 14 21 26 8 | 10 14 21 25 9 |
| 47001 | Vendas esporadicas | 0 10 10 9 7 | 0 10 10 10 7 |
| 47002 | Emprestimos | 0 3 3 1 1 | 1 3 3 1 1 |
| 47003 | Aplicacoes de capital | 10 3 11 9 11 | 10 3 11 10 11 |
| 47004 | Outros renda | 32 23 15 20 66 | 30 23 15 19 65 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 15 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 161 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_nao-consumo: 26 decisões (aceita 26)`
