# Relatório — 2026-10-16_claude-v3_2017-quadros-deslocados

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 4 MOVER óbvios (8 células), 4 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (8: aceita 8)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 2 | 38005 → 32004 | Utensílio doméstico em recreação só em 2017, no bloco do quadro 16 que a aba de 2017 deslocou. Outras edições e IBGE concordam no grupo: duas fontes ⇒ ALTA (ADR |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 2 | 38005 → 32003 | Mesmo padrão do quadro 16 de 2017; outras edições e IBGE concordam em 32003. |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 3 | 32003 → 33006 | Em 2017 o quadro 37 tem itens trocados entre 33006 e 32003 (ver também a proposta do enchimento). As outras edições e o IBGE concordam em 33006: duas fontes ⇒ A |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 1 | 33006 → 32003 | O par simétrico da troca de linhas do quadro 37 de 2017. Três edições e o IBGE concordam. |  | claude-ia (ADR 0005) |
| p05 | REVISAR | **aceita** | 14 | 38005;40006 →  | Estão fora do lugar (recreação), mas o destino fino não é unânime nas outras edições. Recomendação da IA: seguir a linha do IBGE 2017 (32003 Mobiliário para qua |  | claude-ia (ADR 0005) |
| p06 | REVISAR | **aceita** | 11 | 32003;33006;40006 →  | Em 2017 o quadro 37 ganhou itens novos e linhas trocadas; sem par nas outras edições, o destino depende de critério (tecido para o lar é armarinho ou artigo do  |  | claude-ia (ADR 0005) |
| p07 | REVISAR | **aceita** | 11 | 32005 →  | Aluguel não é conserto. 2002 e o IBGE (2008 e 2017) põem aluguel de aparelhos em despesas diversas. Recomendação da IA: 40006; só uma edição tem par, por isso n |  | claude-ia (ADR 0005) |
| p08 | REVISAR | **aceita** | 7 | 40005;42001 →  | Aluguel não é aquisição (deslocamento típico de 2017). Recomendação da IA: aluguel e garagem para 40005; impostos de outros imóveis para 41001 (como o IPTU do d |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 10
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 4
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 32003 | Mobiliarios e artigos do lar | 270 281 331 332 434 | 270 281 331 332 434 |
| 32004 | Eletrodomesticos | 104 123 149 152 130 | 104 123 149 152 132 |
| 32005 | Consertos de artigos do lar | 17 67 80 157 227 | 17 67 80 157 227 |
| 33006 | Tecidos e armarinhos | 14 13 25 25 14 | 14 13 25 25 16 |
| 38005 | Outras recreacao etc | 29 27 42 89 75 | 29 27 42 89 71 |
| 40005 | Imoveis de uso ocasional | 16 18 15 19 26 | 16 18 15 19 26 |
| 40006 | Outras despesas diversas | 65 63 61 79 67 | 65 63 61 79 67 |
| 42001 | Imovel aquisicao | 3 11 7 11 7 | 3 11 7 11 7 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 15 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 223 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_2017-quadros-deslocados: 8 decisões (aceita 8)`
