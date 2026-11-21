# Relatório — 2026-11-18_claude-v4_correcoes-series

Tipo `familia` · autor claude-v4 · fechada em 2026-11-18

Revisão de 2026-11-18 (doc 'Harmonização POF: decisões da v3 e da v4'): a v4 criou 43 divergências novas de série; 35 são a comida fora de casa (intencional) e 8 são erros. Sete são inversões: ações da revisão manual escritas sobre a planilha anterior à v3 foram aplicadas depois que a v3 já tinha movido o item de 2017; a v4 levou as outras edições para o grupo antigo de 2017 e 2017 ficou de fora. O oitavo é leitura errada das laranjas de 1995. Tales aceitou todas as correções propostas.

## Decisões (8: aceita 8)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 40006 → 32003 | Inversão entre v3 e v4: a série fica toda em 32003, o destino que a revisão manual escolheu. |  | claude-ia (ADR 0007) |
| p02 | MOVER | **aceita** | 1 | 33006 → 32003 | Mesma inversão; série em 32003. |  | claude-ia (ADR 0007) |
| p03 | MOVER | **aceita** | 2 | 40006 → 32003 | A revisão manual escolheu 32003 para a série; a v4 só aplicou em 2002. Completa a série. |  | claude-ia (ADR 0007) |
| p04 | MOVER | **aceita** | 1 | 40006 → 39005 | Inversão; volta ao destino original de 2017, agora comum às cinco edições. |  | claude-ia (ADR 0007) |
| p05 | MOVER | **aceita** | 1 | 40006 → 40003 | Aplica a 2017 o mesmo critério de jazigo da v4. |  | claude-ia (ADR 0007) |
| p06 | MOVER | **aceita** | 2 | 38005 → 38003 | Completa a série que a revisão manual definiu (periódicos, livros e revistas). |  | claude-ia (ADR 0007) |
| p07 | MOVER | **aceita** | 2 | 38005 → 32004 | A revisão manual define 32004 para a série inteira; alinha 2008 e 2017. |  | claude-ia (ADR 0007) |
| p08 | MOVER | **aceita** | 3 | 03118 → 03108;03110;03109 | Erro de leitura da v4: os grupos de 1995 estavam certos. Desfaz o movimento e revoga a regra de ausência que dependia dele (R7). |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 20
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 0
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 03108 | Laranja-lima | 1 0 1 1 1 | 1 1 1 1 1 |
| 03109 | Laranja-pêra | 1 0 1 1 1 | 1 1 1 1 1 |
| 03110 | Laranja-seleta | 1 0 1 1 1 | 1 1 1 1 1 |
| 03118 | Outras; Outras laranjas; Goiaba; Acerola | 9 14 37 48 54 | 9 11 37 48 54 |
| 32003 | Mobiliarios e artigos do lar | 268 274 336 335 438 | 268 274 336 336 441 |
| 32004 | Eletrodomesticos | 104 127 153 157 137 | 104 127 153 158 138 |
| 33006 | Tecidos e armarinhos | 14 13 24 24 18 | 14 13 24 24 17 |
| 38003 | Periodicos livros e revistas | 6 7 7 23 24 | 7 7 7 23 25 |
| 38005 | Outras recreacao etc | 29 26 40 70 83 | 28 26 40 69 81 |
| 39005 | Outras servicos pessoais | 12 19 26 26 28 | 12 19 26 26 29 |
| 40003 | Cerimonias e festas | 14 15 18 18 28 | 14 15 18 18 29 |
| 40006 | Outras despesas diversas | 55 54 55 73 72 | 55 54 55 72 68 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 1 | INFO: 1

- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 1 pendências abertas/em onda

## Commit sugerido
`onda 2026-11-18_claude-v4_correcoes-series: 8 decisões (aceita 8)`
