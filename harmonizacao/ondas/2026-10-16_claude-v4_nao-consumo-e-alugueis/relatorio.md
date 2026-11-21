# Relatório — 2026-10-16_claude-v4_nao-consumo-e-alugueis

Tipo `familia` · autor claude-v4 · fechada em 2026-10-16

Outras despesas, ativo, passivo e rendimentos: pares do detector, compra de outros imóveis, aluguéis de aparelhos e de outros imóveis, vazios de 44004/47001 e 34006.

## Decisões (18: aceita 18)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 44001 → 45005 | As outras edições põem os mesmos produtos em 45005, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p02 | MOVER | **aceita** | 1 | 47004 → 44001 | As outras edições põem os mesmos produtos em 44001, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p03 | MOVER | **aceita** | 1 | 47004 → 45005 | As outras edições põem os mesmos produtos em 45005, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p04 | MOVER | **aceita** | 28 | 32001 → 41002 | As outras edições põem os mesmos produtos em 41002, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p05 | MOVER | **aceita** | 2 | 40005 → 42002 | As outras edições põem os mesmos produtos em 42002, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p06 | MOVER | **aceita** | 3 | 41001 → 46001 | As outras edições põem os mesmos produtos em 46001, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p07 | MOVER | **aceita** | 6 | 41001 → 47003 | As outras edições põem os mesmos produtos em 47003, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p08 | MOVER | **aceita** | 1 | 41006 → 41004 | As outras edições põem os mesmos produtos em 41004, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p09 | MOVER | **aceita** | 7 | 47004 → 44001 | As outras edições põem os mesmos produtos em 44001, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p10 | MANTER | **aceita** | 1 | 34005 →  | 1987:5101 AUTOMOVEL está no quadro 51 (compra de veículos): 34005 correto; o par 88888 é do inventário. |  | claude-ia (ADR 0007) |
| p11 | MOVER | **aceita** | 10 | 40005;41006 → 42001 | Comprar imóvel é aumento do ativo; o repositório já trata assim o domicílio principal (42001 nas cinco edições) e o IBGE também. Para outros imóveis o valor de  |  | claude-ia (ADR 0007) |
| p12 | MOVER | **aceita** | 2 | 42001 → 40005 | Aluguel não é aquisição; 2008 e o IBGE 2017 põem em 40005 (Imóveis de uso ocasional). IPTU, ITR e INCRA de outros imóveis e título/joia de clube ficam em 40005, |  | claude-ia (ADR 0007) |
| p13 | MOVER | **aceita** | 11 | 32005 → 40006 | O aluguel de aparelhos está em 40006 em 1987, 1995, 2002 e 2008 (quadro 13) e o IBGE 2017 também o põe em Despesas diversas. A revisão manual propunha o contrár |  | claude-ia (ADR 0007) |
| p14 | MOVER | **aceita** | 1 | 40006 → 31007 | Assinatura de TV, não aluguel de aparelho; 31007 desde 2008 (Cynthia folha 40006 #21). |  | claude-ia (ADR 0007) |
| p15 | MOVER | **aceita** | 3 | 40006 → 39005 | 2017 em 39005 (Cynthia folha 40006 #30). |  | claude-ia (ADR 0007) |
| p16 | MOVER | **aceita** | 2 | 47004 → 47001 | As vendas de 1995-2017 estão em 47001; 1987 estava em 47004 Outros. Preenche o vazio de 47001 em 1987. |  | claude-ia (ADR 0007) |
| p17 | REGRA | **aceita** | 0 |  →  | R5: nenhum item parecido nas duas edições (busca na v3). |  | claude-ia (ADR 0007) |
| p18 | REGRA | **aceita** | 0 |  →  | Mover as viagens para Transporte, como o IBGE, mudaria um grupo inteiro sem ganho de comparabilidade entre as edições (R8). Extinguir não muda nenhuma célula. |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 94
- Regras novas: 2 · pendências resolvidas: 21 · pendências criadas: 0
- Decisões estruturais aplicadas: 2026-10-16_claude-v4_nao-consumo-e-alugueis#p17, 2026-10-16_claude-v4_nao-consumo-e-alugueis#p18 ⇒ PR com label `estrutural` e aprovação de outro membro

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 31007 | Outros servicos etc | 13 28 32 36 39 | 13 29 32 36 39 |
| 32001 | Manutencao do lar | 37 106 142 121 99 | 37 106 114 121 99 |
| 32005 | Consertos de artigos do lar | 17 70 78 157 227 | 17 70 78 157 216 |
| 34005 | Aquisicao de veiculos | 14 21 21 24 26 | 14 21 21 24 26 |
| 39005 | Outras servicos pessoais | 11 19 25 25 28 | 12 19 26 26 28 |
| 40005 | Imoveis de uso ocasional | 16 18 15 19 26 | 13 16 13 17 27 |
| 40006 | Outras despesas diversas | 56 55 56 74 61 | 55 54 55 73 72 |
| 41001 | Impostos | 2 42 17 75 17 | 2 33 17 75 17 |
| 41002 | Contribuicoes trabalhistas | 3 51 4 44 3 | 3 51 32 44 3 |
| 41004 | Pensoes mesadas e doacoes | 7 11 10 11 10 | 7 11 10 11 11 |
| 41006 | Outras despesas | 9 13 21 82 19 | 9 13 19 82 18 |
| 42001 | Imovel aquisicao | 3 8 7 11 6 | 4 10 11 13 5 |
| 42002 | Imovel reforma | 70 12 78 87 103 | 72 12 78 87 103 |
| 44001 | Empregado | 1 5 14 26 8 | 1 6 14 25 15 |
| 45005 | Transferencias transitorias | 10 14 21 25 9 | 10 15 21 26 9 |
| 46001 | Aluguel de bens imoveis | 1 1 1 1 1 | 1 4 1 1 1 |
| 47001 | Vendas esporadicas | 0 10 10 10 7 | 2 10 10 10 7 |
| 47003 | Aplicacoes de capital | 10 3 11 10 11 | 10 9 11 10 11 |
| 47004 | Outros renda | 30 23 15 19 65 | 28 21 15 19 58 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 2 | INFO: 1

- **ALERTA A01** 2 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03202[2002], 16105[2002,2008]
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 5 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v4_nao-consumo-e-alugueis: 18 decisões (aceita 18)`
