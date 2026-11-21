# Relatório — 2026-10-16_claude-v3_cynthia-folha-38

Tipo `pendencia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 0 MOVER óbvios (0 células), 15 REVISAR e 5 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (20: aceita 20)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | REVISAR | **aceita** | 1 | 38005 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p02 | REVISAR | **aceita** | 4 | 03118;34001;38005;38006 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p03 | REVISAR | **aceita** | 1 | 38005 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p04 | REVISAR | **aceita** | 11 | 38001 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p05 | REVISAR | **aceita** | 3 | 38004;38005 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p06 | REVISAR | **aceita** | 8 | 38001;38006 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p07 | MANTER | **aceita** | 2 | 32004 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p08 | REVISAR | **aceita** | 1 | 38004 →  | A revisão manual move por analogia com itens parecidos, sem o mesmo produto em outras edições. Evidência de nível 5 (descrição): decisão humana. |  | claude-ia (ADR 0005) |
| p09 | REVISAR | **aceita** | 3 | 38005 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p10 | REVISAR | **aceita** | 3 | 38004 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p11 | REVISAR | **aceita** | 9 | 38005 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p12 | REVISAR | **aceita** | 7 | 38004 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p13 | MANTER | **aceita** | 2 | 38004 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p14 | REVISAR | **aceita** | 1 | 38004 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p15 | REVISAR | **aceita** | 1 | 37003 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p16 | MANTER | **aceita** | 1 | 38004 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p17 | REVISAR | **aceita** | 0 |  →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p18 | MANTER | **aceita** | 1 | 38002 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p19 | MANTER | **aceita** | 1 | 38004 →  | As células da ação já estão no destino proposto pela revisão manual (a planilha do Drive estava defasada). Nada a mudar. |  | claude-ia (ADR 0005) |
| p20 | REVISAR | **aceita** | 1 | 38005 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 0
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 15
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 03118 | Outras; Outras laranjas; Goiaba; Acerola | 9 11 38 50 56 | 9 11 38 50 56 |
| 32004 | Eletrodomesticos | 104 123 149 152 130 | 104 123 149 152 130 |
| 34001 | Urbano | 12 20 25 17 20 | 12 20 25 17 20 |
| 37003 | Outros cursos | 1 17 20 55 64 | 1 17 20 55 64 |
| 38001 | Brinquedos e jogos | 7 8 7 3 56 | 7 8 7 3 56 |
| 38002 | Celular e acessorios | 0 3 4 4 11 | 0 3 4 4 11 |
| 38004 | Diversoes e esportes | 36 57 63 43 37 | 36 57 63 43 37 |
| 38005 | Outras recreacao etc | 29 27 42 89 75 | 29 27 42 89 75 |
| 38006 | Gastos com viagens | 21 26 31 41 72 | 21 26 31 41 72 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 15 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 197 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_cynthia-folha-38: 20 decisões (aceita 20)`
