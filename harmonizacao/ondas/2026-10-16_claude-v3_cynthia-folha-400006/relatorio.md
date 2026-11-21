# Relatório — 2026-10-16_claude-v3_cynthia-folha-400006

Tipo `pendencia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 0 MOVER óbvios (0 células), 22 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (22: aceita 22)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | REVISAR | **aceita** | 2 | 40006 →  | Ação da revisão manual sem tipo identificado; decisão humana. |  | claude-ia (ADR 0005) |
| p02 | REVISAR | **aceita** | 1 | 40006 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p03 | REVISAR | **aceita** | 4 | 40006;42002 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p04 | REVISAR | **aceita** | 2 | 40006 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p05 | REVISAR | **aceita** | 2 | 40006 →  | A revisão manual move por analogia com itens parecidos, sem o mesmo produto em outras edições. Evidência de nível 5 (descrição): decisão humana. |  | claude-ia (ADR 0005) |
| p06 | REVISAR | **aceita** | 2 | 40006 →  | A revisão manual move por analogia com itens parecidos, sem o mesmo produto em outras edições. Evidência de nível 5 (descrição): decisão humana. |  | claude-ia (ADR 0005) |
| p07 | REVISAR | **aceita** | 3 | 40006 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p08 | REVISAR | **aceita** | 1 | 40006 →  | A revisão manual aponta outlier pontual, mas o detector não o confirmou: a célula tem itens sem histórico ou de outro conceito, ou o histórico não é unânime (R1 |  | claude-ia (ADR 0005) |
| p09 | REVISAR | **aceita** | 0 |  →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p10 | REVISAR | **aceita** | 0 |  →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p11 | REVISAR | **aceita** | 2 | 40006 →  | A revisão manual move por analogia com itens parecidos, sem o mesmo produto em outras edições. Evidência de nível 5 (descrição): decisão humana. |  | claude-ia (ADR 0005) |
| p12 | REVISAR | **aceita** | 3 | 40006 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p13 | REVISAR | **aceita** | 1 | 40006 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p14 | REVISAR | **aceita** | 1 | 40006 →  | Ação da revisão manual sem tipo identificado; decisão humana. |  | claude-ia (ADR 0005) |
| p15 | REVISAR | **aceita** | 8 | 40006 →  | Ação da revisão manual sem tipo identificado; decisão humana. |  | claude-ia (ADR 0005) |
| p16 | REVISAR | **aceita** | 2 | 40006 →  | A revisão manual move por analogia com itens parecidos, sem o mesmo produto em outras edições. Evidência de nível 5 (descrição): decisão humana. |  | claude-ia (ADR 0005) |
| p17 | REVISAR | **aceita** | 1 | 40006 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p18 | REVISAR | **aceita** | 3 | 40006 →  | A revisão manual propõe adotar a classificação mais recente (taxonomia que amadureceu). É escolha de critério para a série, não erro: decisão humana. |  | claude-ia (ADR 0005) |
| p19 | REVISAR | **aceita** | 2 | 40006 →  | Ação da revisão manual sem tipo identificado; decisão humana. |  | claude-ia (ADR 0005) |
| p20 | REVISAR | **aceita** | 1 | 40006 →  | Ação da revisão manual sem tipo identificado; decisão humana. |  | claude-ia (ADR 0005) |
| p21 | REVISAR | **aceita** | 2 | 40006 →  | Ação da revisão manual sem tipo identificado; decisão humana. |  | claude-ia (ADR 0005) |
| p22 | REVISAR | **aceita** | 1 | 40006 →  | Ação da revisão manual sem tipo identificado; decisão humana. |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 0
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 22
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 40006 | Outras despesas diversas | 65 63 61 79 67 | 65 63 61 79 67 |
| 42002 | Imovel reforma | 73 11 77 86 103 | 73 11 77 86 103 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 15 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 219 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_cynthia-folha-400006: 22 decisões (aceita 22)`
