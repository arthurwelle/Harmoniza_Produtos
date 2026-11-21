# Relatório — 2026-10-16_claude-v4_vazios-finais

Tipo `familia` · autor claude-v4 · fechada em 2026-10-16

hp_validar depois das ondas 1-10: A01 em 03202 Maçã (2002) e 16105 Salgadinho (2002, 2008). Mesmo padrão dos outros vazios: o produto tem código próprio e está num grupo genérico.

## Decisões (2: aceita 2)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 3 | 03118 → 03202 | MAÇÃ está em 03202 em 1987 e 1995, e a maçã orgânica de 2008/2017 também; a maçã comum de 2002-2017 caiu em Outras frutas. Preenche o vazio de 2002 (R2/R4). |  | claude-ia (ADR 0007) |
| p02 | MOVER | **aceita** | 3 | 16104 → 16105 | SALGADINHOS PARA VIAGEM (coxinha, pastel, esfirra, quibe...) tem código próprio nas cinco edições; 1987/1995 em 16105. Preenche o vazio de 2002 e 2008 (R2/R4). |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 118
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 0
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 03118 | Outras; Outras laranjas; Goiaba; Acerola | 9 14 38 49 55 | 9 14 37 48 54 |
| 03202 | Maçã | 1 1 0 1 1 | 1 1 1 2 2 |
| 16104 | Refeição; Refeição pronta | 16 28 58 109 138 | 16 28 57 108 137 |
| 16105 | Salgadinho | 1 1 0 0 4 | 1 1 1 1 5 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 1 | INFO: 1

- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 1 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v4_vazios-finais: 2 decisões (aceita 2)`
