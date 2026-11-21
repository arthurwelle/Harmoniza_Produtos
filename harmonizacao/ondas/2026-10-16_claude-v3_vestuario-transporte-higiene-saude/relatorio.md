# Relatório — 2026-10-16_claude-v3_vestuario-transporte-higiene-saude

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 22 MOVER óbvios (28 células), 17 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (39: aceita 39)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 33004 → 33006 | Outlier pontual: os mesmos produtos estão em 33006 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 33004, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 1 | 36010 → 36009 | Outlier pontual: os mesmos produtos estão em 36009 em todas as outras edições em que aparecem (pelo menos 4); só em 1987 a célula está em 36010, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 1 | 40006 → 33006 | Outlier pontual: os mesmos produtos estão em 33006 em todas as outras edições em que aparecem (pelo menos 3); só em 1987 a célula está em 40006, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 1 | 32002 → 33004 | Outlier pontual: os mesmos produtos estão em 33004 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 32002, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 1 | 32003 → 33006 | Outlier pontual: os mesmos produtos estão em 33006 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 2 | 34007 → 34004 | Outlier pontual: os mesmos produtos estão em 34004 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 34007, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 32003 → 39001 | Outlier pontual: os mesmos produtos estão em 39001 em todas as outras edições em que aparecem (pelo menos 4); só em 2002 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 32004 → 35002 | Outlier pontual: os mesmos produtos estão em 35002 em todas as outras edições em que aparecem (pelo menos 2); só em 2002 a célula está em 32004, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | MOVER | **aceita** | 1 | 35004 → 35003 | Outlier pontual: os mesmos produtos estão em 35003 em todas as outras edições em que aparecem (pelo menos 4); só em 2002 a célula está em 35004, sem nenhum item |  | claude-ia (ADR 0005) |
| p10 | MOVER | **aceita** | 1 | 31007 → 34001 | Outlier pontual: os mesmos produtos estão em 34001 em todas as outras edições em que aparecem (pelo menos 2); só em 2008 a célula está em 31007, sem nenhum item |  | claude-ia (ADR 0005) |
| p11 | MOVER | **aceita** | 1 | 16103 → 35004 | Outlier pontual: os mesmos produtos estão em 35004 em todas as outras edições em que aparecem (pelo menos 4); só em 2017 a célula está em 16103, sem nenhum item |  | claude-ia (ADR 0005) |
| p12 | MOVER | **aceita** | 2 | 32003 → 33006 | Outlier pontual: os mesmos produtos estão em 33006 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p13 | MOVER | **aceita** | 2 | 33004 → 33005 | Outlier pontual: os mesmos produtos estão em 33005 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 33004, sem nenhum item |  | claude-ia (ADR 0005) |
| p14 | MOVER | **aceita** | 1 | 34007 → 34004 | Outlier pontual: os mesmos produtos estão em 34004 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 34007, sem nenhum item |  | claude-ia (ADR 0005) |
| p15 | MOVER | **aceita** | 1 | 35004 → 36009 | Outlier pontual: os mesmos produtos estão em 36009 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 35004, sem nenhum item |  | claude-ia (ADR 0005) |
| p16 | MOVER | **aceita** | 1 | 36001 → 36009 | Outlier pontual: os mesmos produtos estão em 36009 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 36001, sem nenhum item |  | claude-ia (ADR 0005) |
| p17 | MOVER | **aceita** | 1 | 36009 → 36010 | Outlier pontual: os mesmos produtos estão em 36010 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 36009, sem nenhum item |  | claude-ia (ADR 0005) |
| p18 | MOVER | **aceita** | 4 | 39004 → 39005 | Outlier pontual: os mesmos produtos estão em 39005 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 39004, sem nenhum item |  | claude-ia (ADR 0005) |
| p19 | MOVER | **aceita** | 1 | 41001 → 34005 | Outlier pontual: os mesmos produtos estão em 34005 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 41001, sem nenhum item |  | claude-ia (ADR 0005) |
| p20 | MOVER | **aceita** | 1 | 41001 → 34007 | Outlier pontual: os mesmos produtos estão em 34007 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 41001, sem nenhum item |  | claude-ia (ADR 0005) |
| p21 | MOVER | **aceita** | 1 | 41006 → 34001 | Outlier pontual: os mesmos produtos estão em 34001 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 41006, sem nenhum item |  | claude-ia (ADR 0005) |
| p22 | REVISAR | **aceita** | 1 | 32003 →  | Os mesmos produtos estão em 33006 nas duas outras edições em que aparecem; em 1995 estão em 32003. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p23 | REVISAR | **aceita** | 3 | 34004 →  | Os mesmos produtos estão em 34007 nas duas outras edições em que aparecem; em 1995, 2002 estão em 34004. Duas edições contra uma, sem segunda fonte (IBGE neutro |  | claude-ia (ADR 0005) |
| p24 | REVISAR | **aceita** | 1 | 34004 →  | Os mesmos produtos estão em 35002 nas duas outras edições em que aparecem; em 2002 estão em 34004. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p25 | REVISAR | **aceita** | 1 | 36001 →  | Os mesmos produtos estão em 35004 nas duas outras edições em que aparecem; em 2002 estão em 36001. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p26 | REVISAR | **aceita** | 1 | 36001 →  | Os mesmos produtos estão em 36009 nas duas outras edições em que aparecem; em 2002 estão em 36001. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p27 | REVISAR | **aceita** | 1 | 38006 →  | Os mesmos produtos estão em 34007 nas duas outras edições em que aparecem; em 2002 estão em 38006. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p28 | REVISAR | **aceita** | 1 | 39003 →  | Os mesmos produtos estão em 39002 nas duas outras edições em que aparecem; em 2017 estão em 39003. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p29 | REVISAR | **aceita** | 3 | 40006 →  | Os mesmos produtos estão em 33004 nas duas outras edições em que aparecem; em 1987 estão em 40006. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p30 | REVISAR | **aceita** | 1 | 42003 →  | Os mesmos nomes de produto estão em 33005 nas outras edições, mas a célula está em 42003, de outro domínio (consumo, outras despesas, rendimentos ou inventário) |  | claude-ia (ADR 0005) |
| p31 | REVISAR | **aceita** | 1 | 32004 →  | As outras edições põem os mesmos produtos em 34004, mas o tradutor do IBGE confirma o grupo atual (32004) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p32 | REVISAR | **aceita** | 1 | 33003 →  | As outras edições põem os mesmos produtos em 33001, mas o tradutor do IBGE confirma o grupo atual (33003) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p33 | REVISAR | **aceita** | 1 | 33004 →  | As outras edições põem os mesmos produtos em 39001, mas o tradutor do IBGE confirma o grupo atual (33004) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p34 | REVISAR | **aceita** | 1 | 34005 →  | As outras edições põem os mesmos produtos em 34001, mas o tradutor do IBGE confirma o grupo atual (34005) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p35 | REVISAR | **aceita** | 1 | 34007 →  | As outras edições põem os mesmos produtos em 34004, mas o tradutor do IBGE confirma o grupo atual (34007) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p36 | REVISAR | **aceita** | 1 | 36001 →  | As outras edições põem os mesmos produtos em 36009, mas o tradutor do IBGE confirma o grupo atual (36001) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p37 | MOVER | **aceita** | 1 | 41001 → 34007 | Em 2017 o seguro obrigatório sai do consumo sem mudança de conceito na POF; as duas edições anteriores e o IBGE de 2017 concordam em Transporte/Outras. Duas fon |  | claude-ia (ADR 0005) |
| p38 | REVISAR | **aceita** | 5 | 34004;34007 →  | Duas edições antigas contra três recentes, os dois grupos dentro de Transporte. Recomendação da IA: 34007 nos cinco anos (é o que o IBGE faz; seguro não é manut |  | claude-ia (ADR 0005) |
| p39 | REVISAR | **aceita** | 2 | 41001 →  | O agregado reúne itens do quadro sem detalhamento (seguro, documentação, taxas). O IBGE o põe em Transporte nas duas edições. Fontes discordantes (repositório c |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 46
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 17
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 16103 | Outros produtos | 30 17 22 28 34 | 30 17 22 28 33 |
| 31007 | Outros servicos etc | 18 34 32 37 38 | 18 34 32 36 38 |
| 32002 | Artigos de limpeza | 42 44 62 57 62 | 42 43 62 57 62 |
| 32003 | Mobiliarios e artigos do lar | 270 282 332 332 436 | 270 281 331 332 434 |
| 32004 | Eletrodomesticos | 104 123 150 152 131 | 104 123 149 152 131 |
| 33003 | Roupa de crianca | 38 53 53 49 55 | 38 53 53 49 55 |
| 33004 | Calcados e apetrechos | 42 39 50 70 54 | 41 40 50 70 52 |
| 33005 | Joias e bijuterias | 12 14 12 12 8 | 12 14 12 12 10 |
| 33006 | Tecidos e armarinhos | 12 12 25 25 12 | 14 13 25 25 14 |
| 34001 | Urbano | 12 20 25 16 19 | 12 20 25 17 20 |
| 34004 | Manutencao de veiculo proprio | 42 36 38 21 69 | 42 38 38 21 70 |
| 34005 | Aquisicao de veiculos | 14 21 21 24 25 | 14 21 21 24 26 |
| 34007 | Outros transporte | 2 14 10 11 15 | 2 12 10 11 16 |
| 35002 | Produtos para cabelo | 1 1 2 2 1 | 1 1 3 2 1 |
| 35003 | Sabonete | 2 2 2 1 1 | 2 2 3 1 1 |
| 35004 | Produtos de uso pessoal | 32 35 46 40 30 | 32 35 45 40 30 |
| 36001 | Remedios | 4 37 92 48 75 | 4 37 92 48 74 |
| 36009 | Material de tratamento | 10 32 38 14 21 | 11 32 38 14 22 |
| 36010 | Outras assistencia saude | 16 15 13 13 11 | 15 15 13 13 12 |
| 38006 | Gastos com viagens | 21 26 31 41 72 | 21 26 31 41 72 |
| 39001 | Fumo | 20 22 21 23 26 | 20 22 22 23 26 |
| 39003 | Manicuro e pedicuro | 1 1 1 1 3 | 1 1 1 1 3 |
| 39004 | Consertos de artigos pessoais | 13 19 21 22 17 | 13 19 21 22 13 |
| 39005 | Outras servicos pessoais | 11 19 24 25 24 | 11 19 24 25 28 |
| 40006 | Outras despesas diversas | 66 63 61 79 68 | 65 63 61 79 68 |
| 41001 | Impostos | 1 41 17 76 18 | 1 41 17 76 15 |
| 41006 | Outras despesas | 9 13 22 82 28 | 9 13 22 82 27 |
| 42003 | Outros investimentos | 1 2 8 7 0 | 1 2 8 7 0 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 18 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 149 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_vestuario-transporte-higiene-saude: 39 decisões (aceita 39)`
