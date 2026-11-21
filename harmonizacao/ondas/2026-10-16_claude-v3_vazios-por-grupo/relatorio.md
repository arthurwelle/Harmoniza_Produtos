# Relatório — 2026-10-16_claude-v3_vazios-por-grupo

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 0 MOVER óbvios (0 células), 6 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (6: aceita 6)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | REVISAR | **aceita** | 0 |  →  | Vazio legítimo (exemplo da própria CONSTITUICAO, R5). Regra proposta: {tipo: ausencia_estrutural, grupos: 38002, anos: 1987, enunciado: 'Telefonia celular não e |  | claude-ia (ADR 0005) |
| p02 | REVISAR | **aceita** | 0 |  →  | Grupo ativo e vazio: ou se extingue (sem efeito em dados), ou se decide mover os gastos de viagem de 38006 para 34006, como o IBGE (decisão de convenção, afeta  |  | claude-ia (ADR 0005) |
| p03 | REVISAR | **aceita** | 0 |  →  | Distinção observável num ano só (R3): o grupo não pode existir sozinho. Recomendação da IA: UNIR 16101 em 16104 (estrutural). |  | claude-ia (ADR 0005) |
| p04 | REVISAR | **aceita** | 0 |  →  | Grupo sem nível e de um ano só. Recomendação da IA: mover 2002:63034 para 01199 e extinguir 16016. |  | claude-ia (ADR 0005) |
| p05 | REVISAR | **aceita** | 0 |  →  | Cada vazio pede uma de três respostas (R4): o produto foi para outro grupo naquele ano (mover), a distinção não existe naquele ano (R3: unir) ou o produto não e |  | claude-ia (ADR 0005) |
| p06 | REVISAR | **aceita** | 0 |  →  | Recomendação da IA: 44004 como ausência estrutural (o questionário de rendimentos de 1987/1995 não separa trabalho não remunerado); 47001 receber 1987:5508/5509 |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 0
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 6
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| — | | | |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 14 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 207 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_vazios-por-grupo: 6 decisões (aceita 6)`
