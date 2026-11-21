# Relatório — 2026-10-16_claude-v3_recreacao-cultura

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 11 MOVER óbvios (16 células), 7 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (18: aceita 18)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 37004 → 38003 | Outlier pontual: os mesmos produtos estão em 38003 em todas as outras edições em que aparecem (pelo menos 2); só em 1987 a célula está em 37004, sem nenhum item |  | claude-ia (ADR 0005) |
| p02 | MOVER | **aceita** | 2 | 38005 → 38004 | Outlier pontual: os mesmos produtos estão em 38004 em todas as outras edições em que aparecem (pelo menos 2); só em 1987 a célula está em 38005, sem nenhum item |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 1 | 40006 → 38004 | Outlier pontual: os mesmos produtos estão em 38004 em todas as outras edições em que aparecem (pelo menos 2); só em 1987 a célula está em 40006, sem nenhum item |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 1 | 32004 → 38002 | Outlier pontual: os mesmos produtos estão em 38002 em todas as outras edições em que aparecem (pelo menos 3); só em 1995 a célula está em 32004, sem nenhum item |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 1 | 37004 → 38004 | Outlier pontual: os mesmos produtos estão em 38004 em todas as outras edições em que aparecem (pelo menos 2); só em 1995 a célula está em 37004, sem nenhum item |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 1 | 38003 → 38004 | Outlier pontual: os mesmos produtos estão em 38004 em todas as outras edições em que aparecem (pelo menos 2); só em 1995 a célula está em 38003, sem nenhum item |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 16104 → 38006 | Outlier pontual: os mesmos produtos estão em 38006 em todas as outras edições em que aparecem (pelo menos 4); só em 2002 a célula está em 16104, sem nenhum item |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 32003 → 38005 | Outlier pontual: os mesmos produtos estão em 38005 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 32003, sem nenhum item |  | claude-ia (ADR 0005) |
| p09 | MOVER | **aceita** | 1 | 38003 → 38005 | Outlier pontual: os mesmos produtos estão em 38005 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 38003, sem nenhum item |  | claude-ia (ADR 0005) |
| p10 | MOVER | **aceita** | 4 | 38005 → 38004 | Outlier pontual: os mesmos produtos estão em 38004 em todas as outras edições em que aparecem (pelo menos 3); só em 2017 a célula está em 38005, sem nenhum item |  | claude-ia (ADR 0005) |
| p11 | MOVER | **aceita** | 2 | 40003 → 38004 | Outlier pontual: os mesmos produtos estão em 38004 em todas as outras edições em que aparecem (pelo menos 2); só em 2017 a célula está em 40003, sem nenhum item |  | claude-ia (ADR 0005) |
| p12 | REVISAR | **aceita** | 2 | 38005 →  | Os mesmos produtos estão em 38004 nas duas outras edições em que aparecem; em 2017 estão em 38005. Duas edições contra uma, sem segunda fonte (IBGE neutro ou au |  | claude-ia (ADR 0005) |
| p13 | REVISAR | **aceita** | 1 | 37003 →  | As outras edições põem os mesmos produtos em 38004, mas o tradutor do IBGE confirma o grupo atual (37003) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p14 | REVISAR | **aceita** | 17 | 38001 →  | As outras edições põem os mesmos produtos em 38005, mas o tradutor do IBGE confirma o grupo atual (38001) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p15 | REVISAR | **aceita** | 1 | 38005 →  | As outras edições põem os mesmos produtos em 38001, mas o tradutor do IBGE confirma o grupo atual (38005) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p16 | REVISAR | **aceita** | 11 | 38005 →  | As outras edições põem os mesmos produtos em 38004, mas o tradutor do IBGE confirma o grupo atual (38005) em 2008. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p17 | REVISAR | **aceita** | 2 | 40006 →  | As outras edições põem os mesmos produtos em 38005, mas o tradutor do IBGE confirma o grupo atual (40006) em 2017. Fontes discordantes (CONSTITUICAO, hierarquia |  | claude-ia (ADR 0005) |
| p18 | REVISAR | **aceita** | 19 | 31003;32004;38002;38005;40006 →  | Não há outlier: o serviço muda de grupo em todas as edições (38002, 31003, 38005, 38002). A distinção serviço × aparelho é observável nos cinco anos (R2) e é a  |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 25
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 7
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 16104 | Refeição; Refeição pronta | 23 44 77 129 242 | 23 44 76 129 242 |
| 31003 | Telefonia | 1 3 4 8 9 | 1 3 4 8 9 |
| 32003 | Mobiliarios e artigos do lar | 270 282 332 332 437 | 270 282 332 332 436 |
| 32004 | Eletrodomesticos | 104 124 150 152 131 | 104 123 150 152 131 |
| 37003 | Outros cursos | 1 17 20 55 64 | 1 17 20 55 64 |
| 37004 | Livros e revistas tecnicas | 1 5 4 4 1 | 0 4 4 4 1 |
| 38001 | Brinquedos e jogos | 7 8 7 3 56 | 7 8 7 3 56 |
| 38002 | Celular e acessorios | 0 2 4 4 11 | 0 3 4 4 11 |
| 38003 | Periodicos livros e revistas | 5 7 6 22 25 | 6 6 6 22 24 |
| 38004 | Diversoes e esportes | 33 55 63 43 31 | 36 57 63 43 37 |
| 38005 | Outras recreacao etc | 31 27 42 89 77 | 29 27 42 89 75 |
| 38006 | Gastos com viagens | 21 26 30 41 72 | 21 26 31 41 72 |
| 40003 | Cerimonias e festas | 12 12 17 17 30 | 12 12 17 17 28 |
| 40006 | Outras despesas diversas | 67 63 61 79 68 | 66 63 61 79 68 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 18 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 132 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_recreacao-cultura: 18 decisões (aceita 18)`
