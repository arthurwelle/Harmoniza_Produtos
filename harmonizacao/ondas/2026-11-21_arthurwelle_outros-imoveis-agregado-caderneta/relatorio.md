# Relatório — 2026-11-21_arthurwelle_outros-imoveis-agregado-caderneta

Tipo `familia` · autor arthurwelle · fechada em 2026-11-21

Aquisição de outros imóveis e sepultura de 1987/1995 fora do consumo; AGREGADO da caderneta de 1987/1995 em 16103 como 2002-2017.

## Decisões (3: aceita 3)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 2 | 40005 → 42001 | Compra de imóvel é aumento do ativo; a v4 (nao-consumo-e-alugueis#p11) tirou do consumo as células de valor declarado mas deixou a aquisição paga de 1987/1995 e | Arthur, 2026-11-21: 'Aplica 2 e 3'. | arthurwelle |
| p02 | MOVER | **aceita** | 2 | 40005 → 42002 | Outlier pontual de 1995; 4 edições concordam. | Arthur, 2026-11-21: 'Aplica 2 e 3'. | arthurwelle |
| p03 | MOVER | **aceita** | 2 | 40006 → 16103 | Mesmo conceito (gasto da caderneta sem produto identificado) em grupos diferentes. 40006 passa a 0,26/0,05/0,05/0,09/0,09%; 16103 a 0,33/1,23/0,67/0,91/1,22%. N | Arthur, 2026-11-21: 'Aplica 2 e 3'. | arthurwelle |

## Efeito
- Itens do de-para que mudaram de grupo: 6
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 0
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 16103 | Outros produtos | 30 21 23 26 33 | 31 22 23 26 33 |
| 40005 | Imoveis de uso ocasional | 11 14 13 17 25 | 10 11 13 17 25 |
| 40006 | Outras despesas diversas | 26 19 19 16 12 | 25 18 19 16 12 |
| 42001 | Imovel aquisicao | 2 4 3 7 5 | 3 5 3 7 5 |
| 42002 | Imovel reforma | 71 11 79 87 103 | 71 13 79 87 103 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 1 | INFO: 1

- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 8 pendências abertas/em onda

## Commit sugerido
`onda 2026-11-21_arthurwelle_outros-imoveis-agregado-caderneta: 3 decisões (aceita 3)`
