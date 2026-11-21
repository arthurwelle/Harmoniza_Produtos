# Relatório — 2026-11-21_arthurwelle_revisao-merge-v4

Tipo `global` · autor arthurwelle · fechada em 2026-11-21

Revisão do PR #1 antes do merge: separa o valor declarado do imóvel adquirido (memória, duplica a aquisição) e alinha o IPTU/ITR de outros imóveis a Impostos.

## Decisões (3: aceita 3)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | CRIAR | **aceita** | 22 | 42001 → 89001 | Somar o valor do bem ao valor pago conta a mesma compra duas vezes e cria a quebra de série de 42001. A v4 (p11) acertou ao tirar a compra de outros imóveis do  | Delegado por Arthur em 2026-11-21: 'fazer o merge mas com modificações que você aprova'. | arthurwelle (delegado a claude-ia) |
| p02 | MOVER | **aceita** | 6 | 40005 → 41001 | Mesmo imposto em dois grupos conforme a edição, e um deles (40005) é consumo. Alinha a série com 2002/2008 e com o IBGE. | Delegado por Arthur em 2026-11-21: 'fazer o merge mas com modificações que você aprova'. | arthurwelle (delegado a claude-ia) |
| p03 | MANTER | **aceita** | 0 |  →  | Nenhuma célula muda. O campo revisor dessas três ondas (ainda não mescladas) passa a 'cynthia (edição no Drive) + claude-ia (ADR 0008)', para que a decisão huma | Delegado por Arthur em 2026-11-21: 'fazer o merge mas com modificações que você aprova'. | arthurwelle (delegado a claude-ia) |

## Efeito
- Itens do de-para que mudaram de grupo: 36
- Regras novas: 0 · pendências resolvidas: 1 · pendências criadas: 0
- Decisões estruturais aplicadas: 2026-11-21_arthurwelle_revisao-merge-v4#p01 ⇒ PR com label `estrutural` e aprovação de outro membro

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 40005 | Imoveis de uso ocasional | 13 16 13 17 27 | 11 14 13 17 25 |
| 41001 | Impostos | 2 33 17 75 17 | 4 35 17 75 19 |
| 42001 | Imovel aquisicao | 4 10 11 13 5 | 2 4 3 7 5 |
| 89001 | Valor do imovel adquirido (memoria, fora da despes | 0 0 0 0 0 | 2 6 8 6 0 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 2 | INFO: 1

- **ALERTA A01** 1 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 89001[2017]
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 8 pendências abertas/em onda

## Commit sugerido
`onda 2026-11-21_arthurwelle_revisao-merge-v4: 3 decisões (aceita 3)`
