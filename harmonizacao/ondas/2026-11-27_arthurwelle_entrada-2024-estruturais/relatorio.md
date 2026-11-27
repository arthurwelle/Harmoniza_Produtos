# Relatório — 2026-11-27_arthurwelle_entrada-2024-estruturais

Tipo `global` · autor arthurwelle · fechada em 2026-11-27

Decisões estruturais da entrada de 2024 (grupo novo de apostas on-line, exceções R1, ausências) e correção de dois agregados da base.

## Decisões (8: aceita 8)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 34004 → 37005 | O agregado segue o conteúdo do quadro, como os demais AGREGADO de 2017. | Arthur: 'Corrija o erro de 2017 agregado'. | arthurwelle |
| p02 | MOVER | **aceita** | 1 | 35004 → 36001 | Alinha 2008 ao IBGE e a 2017; era a maior divergência harmonização × IBGE em saúde. | Arthur: 'e o anterior também achado' (2008:29999, achado na análise de saúde). | arthurwelle |
| p03 | CRIAR | **aceita** | 3 | 40001 → 40007 | Fenômeno novo e grande; juntar a loterias e jogo do bicho esconderia o que se quer medir. A série começa em 2017 sem violar R1. | Arthur: 'Aposta online é criação mesmo, então poderia ser grupo novo'. | arthurwelle |
| p04 | REGRA | **aceita** | 0 |  →  | Justifica os vazios de 40007 (R4/R5). | Consequência do grupo novo (p03). | arthurwelle |
| p05 | REGRA | **aceita** | 0 |  →  | Junção só no ano mais recente e de valor ínfimo (ADR 0003). | Arthur: 'acato a proposta de tratar como exceção'. | arthurwelle |
| p06 | REGRA | **aceita** | 0 |  →  | Conceito dominante é o pacote de telecom (ADR 0003). | Arthur: 'acato a proposta de tratar como exceção'. | arthurwelle |
| p07 | REGRA | **aceita** | 0 |  →  | Justifica o vazio de 88888 em 2024; rever quando o IBGE divulgar o arquivo. | Consequência da entrada de 2024 (arquivo não divulgado). | arthurwelle |
| p08 | REGRA | **aceita** | 0 |  →  | Justifica o vazio de 89001 em 2024. | Consequência da entrada de 2024 (mesma situação de 2017). | arthurwelle |

## Efeito
- Itens do de-para que mudaram de grupo: 5
- Regras novas: 5 · pendências resolvidas: 0 · pendências criadas: 0
- Decisões estruturais aplicadas: 2026-11-27_arthurwelle_entrada-2024-estruturais#p03, 2026-11-27_arthurwelle_entrada-2024-estruturais#p04, 2026-11-27_arthurwelle_entrada-2024-estruturais#p05, 2026-11-27_arthurwelle_entrada-2024-estruturais#p06, 2026-11-27_arthurwelle_entrada-2024-estruturais#p07, 2026-11-27_arthurwelle_entrada-2024-estruturais#p08 ⇒ PR com label `estrutural` e aprovação de outro membro

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017 2024)
| grupo | nome | antes | depois |
|---|---|---|---|
| 34004 | Manutencao de veiculo proprio | 40 37 37 22 70 70 | 40 37 37 22 69 70 |
| 35004 | Produtos de uso pessoal | 32 35 46 40 31 32 | 32 35 46 39 31 32 |
| 36001 | Remedios | 4 37 90 47 74 74 | 4 37 90 48 74 74 |
| 37005 | Artigos escolares | 12 24 24 12 73 73 | 12 24 24 12 74 73 |
| 40001 | Jogos e apostas | 12 17 22 25 33 24 | 12 17 22 25 32 22 |
| 40007 | Apostas on-line (bets e jogos de azar on-line) | 0 0 0 0 0 0 | 0 0 0 0 1 2 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 1 | INFO: 1

- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 8 pendências abertas/em onda

## Commit sugerido
`onda 2026-11-27_arthurwelle_entrada-2024-estruturais: 8 decisões (aceita 8)`
