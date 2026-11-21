# Relatório — 2026-10-16_claude-v3_cynthia-folha-32

Tipo `pendencia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 0 MOVER óbvios (0 células), 12 REVISAR e 10 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (22: aceita 22)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | REVISAR | **aceita** | 1 | 32002 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p02 | REVISAR | **aceita** | 2 | 32003 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p03 | REVISAR | **aceita** | 1 | 32003 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p04 | REVISAR | **aceita** | 1 | 42002 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p05 | REVISAR | **aceita** | 1 | 32003 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p06 | MANTER | **aceita** | 2 | 32002 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p07 | MANTER | **aceita** | 1 | 33006 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p08 | MANTER | **aceita** | 1 | 33004 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p09 | REVISAR | **aceita** | 1 | 42001 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p10 | MANTER | **aceita** | 2 | 32003 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p11 | REVISAR | **aceita** | 1 | 32001 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p12 | MANTER | **aceita** | 1 | 32003 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p13 | MANTER | **aceita** | 1 | 38004 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p14 | REVISAR | **aceita** | 1 | 38005 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p15 | REVISAR | **aceita** | 3 | 40006 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p16 | MANTER | **aceita** | 2 | 35002 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p17 | MANTER | **aceita** | 3 | 32002 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p18 | REVISAR | **aceita** | 1 | 32001 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p19 | MANTER | **aceita** | 1 | 32003 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p20 | REVISAR | **aceita** | 1 | 32003 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p21 | REVISAR | **aceita** | 3 | 33006 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p22 | MANTER | **aceita** | 1 | 33006 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 0
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 12
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 32001 | Manutencao do lar | 29 103 142 121 100 | 29 103 142 121 100 |
| 32002 | Artigos de limpeza | 42 43 62 57 62 | 42 43 62 57 62 |
| 32003 | Mobiliarios e artigos do lar | 270 281 331 332 434 | 270 281 331 332 434 |
| 33004 | Calcados e apetrechos | 41 40 50 70 52 | 41 40 50 70 52 |
| 33006 | Tecidos e armarinhos | 14 13 25 25 14 | 14 13 25 25 14 |
| 35002 | Produtos para cabelo | 1 1 3 2 1 | 1 1 3 2 1 |
| 38004 | Diversoes e esportes | 36 57 63 43 37 | 36 57 63 43 37 |
| 38005 | Outras recreacao etc | 29 27 42 89 75 | 29 27 42 89 75 |
| 40006 | Outras despesas diversas | 65 63 61 79 67 | 65 63 61 79 67 |
| 42001 | Imovel aquisicao | 3 11 7 11 7 | 3 11 7 11 7 |
| 42002 | Imovel reforma | 73 11 77 86 103 | 73 11 77 86 103 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 15 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 173 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_cynthia-folha-32: 22 decisões (aceita 22)`
