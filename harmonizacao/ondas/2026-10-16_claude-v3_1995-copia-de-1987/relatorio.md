# Relatório — 2026-10-16_claude-v3_1995-copia-de-1987

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 0 MOVER óbvios (0 células), 1 REVISAR e 1 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (2: aceita 2)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MANTER | **aceita** | 34 | 31007;32001;32002;32003;32004;34004;34005;36001;38003;38004;39005;40003;40004;40006;47004 →  | A coincidência de grupo com 1987 não é erro quando as edições seguintes confirmam. Nada a mudar. |  | claude-ia (ADR 0005) |
| p02 | REVISAR | **aceita** | 31 | 31005;32001;32003;32004;34004;34007;36001;38004;39001;40006;42001;43001;47004 →  | O padrão confirma a suspeita da pendência q3. O histórico dessas células vem de palavra-chave (descrições diferem), o que não basta para mover pela ADR 0005. Re |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 0
- Regras novas: 0 · pendências resolvidas: 1 · pendências criadas: 1
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 31005 | Gas domestico | 3 3 2 2 2 | 3 3 2 2 2 |
| 31007 | Outros servicos etc | 13 30 32 36 39 | 13 30 32 36 39 |
| 32001 | Manutencao do lar | 34 108 142 121 100 | 34 108 142 121 100 |
| 32002 | Artigos de limpeza | 42 43 62 57 62 | 42 43 62 57 62 |
| 32003 | Mobiliarios e artigos do lar | 270 281 331 332 434 | 270 281 331 332 434 |
| 32004 | Eletrodomesticos | 104 123 149 152 132 | 104 123 149 152 132 |
| 34004 | Manutencao de veiculo proprio | 42 38 38 21 70 | 42 38 38 21 70 |
| 34005 | Aquisicao de veiculos | 14 21 21 24 26 | 14 21 21 24 26 |
| 34007 | Outros transporte | 2 12 10 11 13 | 2 12 10 11 13 |
| 36001 | Remedios | 4 37 92 48 74 | 4 37 92 48 74 |
| 38003 | Periodicos livros e revistas | 6 6 6 22 24 | 6 6 6 22 24 |
| 38004 | Diversoes e esportes | 36 57 63 43 37 | 36 57 63 43 37 |
| 39001 | Fumo | 20 22 22 23 26 | 20 22 22 23 26 |
| 39005 | Outras servicos pessoais | 11 19 24 25 28 | 11 19 24 25 28 |
| 40003 | Cerimonias e festas | 12 12 17 17 28 | 12 12 17 17 28 |
| 40004 | Servicos profissionais | 15 20 20 20 7 | 15 20 20 20 7 |
| 40006 | Outras despesas diversas | 65 63 61 79 67 | 65 63 61 79 67 |
| 42001 | Imovel aquisicao | 3 10 7 11 6 | 3 10 7 11 6 |
| 43001 | Emprestimo e carne | 4 4 4 5 4 | 4 4 4 5 4 |
| 47004 | Outros renda | 30 23 15 19 65 | 30 23 15 19 65 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 14 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 216 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_1995-copia-de-1987: 2 decisões (aceita 2)`
