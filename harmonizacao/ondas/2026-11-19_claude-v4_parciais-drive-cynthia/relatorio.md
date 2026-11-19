# Relatório — 2026-11-19_claude-v4_parciais-drive-cynthia

Tipo `familia` · autor claude-v4 · fechada em 2026-11-19

Depois das ondas 1 e 2, a comparação com a revisão em PDF mostrou um caso de aplicação parcial: a folha 38 #12 manda piscina em parque e taxa de piquenique de 38004 para 38005 em todas as edições; no Drive a Cynthia mudou 2002 piquenique e 2008 piscina, mas não os pares, e a série ficou alternando.

## Decisões (1: aceita 1)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 4 | 38004 → 38005 | Completa a decisão humana que ficou aplicada pela metade; sem isso o mesmo item alterna de grupo entre edições. |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 5
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 0
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 38004 | Diversoes e esportes | 34 56 58 52 34 | 34 54 57 51 34 |
| 38005 | Outras recreacao etc | 29 27 42 70 84 | 29 29 43 71 84 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 1 | INFO: 1

- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 1 pendências abertas/em onda

## Commit sugerido
`onda 2026-11-19_claude-v4_parciais-drive-cynthia: 1 decisões (aceita 1)`
