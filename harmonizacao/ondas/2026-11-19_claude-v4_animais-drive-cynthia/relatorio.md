# Relatório — 2026-11-19_claude-v4_animais-drive-cynthia

Tipo `taxonomia` · autor claude-v4 · fechada em 2026-11-19

A Cynthia criou no Drive o nível 48. Animais (48001 Bens, 48002 Serviços) e passou para ele 56 células, quase todas de 40006 Outras despesas diversas. O grupo não existe no repositório. Com as células dela, 48001 fica sem 2002 e 48002 sem 1995 (A01): os mesmos itens dessas edições ficaram fora (2002 quadro 95, igual ao quadro 95 de 1987 e 1995; 1995:1640, igual a 1987:1640 e 2002:16040). A onda cria os dois grupos com o código da planilha e completa os dois anos.

## Decisões (1: aceita 1)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | CRIAR | **aceita** | 63 | 40006;41006 → 48001;48002 | Decisão humana (Cynthia) registrada na planilha; o repositório só a reproduz, com os mesmos códigos. A IA acrescenta só as 7 células que deixariam um ano vazio  |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 267
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 0
- Decisões estruturais aplicadas: 2026-11-19_claude-v4_animais-drive-cynthia#p01 ⇒ PR com label `estrutural` e aprovação de outro membro

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 40006 | Outras despesas diversas | 55 54 55 72 68 | 49 49 53 52 42 |
| 41006 | Outras despesas | 9 13 19 82 18 | 9 13 15 82 18 |
| 48001 | Bens para animais | 0 0 0 0 0 | 5 4 5 17 21 |
| 48002 | Serviços para animais | 0 0 0 0 0 | 1 1 1 3 5 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 1 | INFO: 1

- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 1 pendências abertas/em onda

## Commit sugerido
`onda 2026-11-19_claude-v4_animais-drive-cynthia: 1 decisões (aceita 1)`
