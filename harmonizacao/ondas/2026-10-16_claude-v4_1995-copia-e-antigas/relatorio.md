# Relatório — 2026-10-16_claude-v4_1995-copia-e-antigas

Tipo `pendencia` · autor claude-v4 · fechada em 2026-10-16

Fecha a auditoria da cópia 1995←1987 (pendência q3) e as pendências antigas que ainda tinham resposta possível.

## Decisões (4: aceita 4)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 6 | 32003;34007 → 32002;32004;34004 | Conferido produto a produto (ver fonte/v3_extras/1995_copia_1987.csv): antena de rádio, aparelho para massa e lava a jato são aparelhos (32004; 1987:1581 antena |  | claude-ia (ADR 0007) |
| p02 | MANTER | **aceita** | 0 |  →  | As 5 duplicatas estão no mesmo grupo (não afetam a harmonização) e o de-para só muda por `fechar`, que não remove linhas. Remover é limpeza de dados, fora do es |  | claude-ia (ADR 0007) |
| p03 | MANTER | **aceita** | 0 |  →  | Feita na v3 (detector entre edições + tradutor do IBGE) e concluída na v4 (quadros 9, 16, 37, 43 e 47 de 2017). |  | claude-ia (ADR 0007) |
| p04 | MANTER | **aceita** | 0 |  →  | A linha da planilha de melhorias não traz grupo sugerido nem célula; os analgésicos estão em 36001 Remédios em todas as edições. |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 6
- Regras novas: 0 · pendências resolvidas: 4 · pendências criadas: 0
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 32002 | Artigos de limpeza | 44 45 64 58 63 | 44 46 64 58 63 |
| 32003 | Mobiliarios e artigos do lar | 268 278 336 335 438 | 268 274 336 335 438 |
| 32004 | Eletrodomesticos | 104 124 153 157 137 | 104 127 153 157 137 |
| 34004 | Manutencao de veiculo proprio | 40 35 37 22 70 | 40 37 37 22 70 |
| 34007 | Outros transporte | 3 14 12 11 13 | 3 12 12 11 13 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 2 | INFO: 1

- **ALERTA A01** 2 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03202[2002], 16105[2002,2008]
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 1 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v4_1995-copia-e-antigas: 4 decisões (aceita 4)`
