# Relatório — 2026-10-16_claude-v4_recreacao-e-telefonia

Tipo `familia` · autor claude-v4 · fechada em 2026-10-16

Recreação (pares do detector, revisão da Cynthia folha 38 e 40006) e reorganização da telefonia.

## Decisões (17: aceita 17)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 2 | 38005 → 38004 | As outras edições põem os mesmos produtos em 38004, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p02 | MOVER | **aceita** | 1 | 37003 → 38004 | As outras edições põem os mesmos produtos em 38004, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p03 | MOVER | **aceita** | 1 | 38005 → 38001 | As outras edições põem os mesmos produtos em 38001, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p04 | MOVER | **aceita** | 2 | 40006 → 38005 | As outras edições põem os mesmos produtos em 38005, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p05 | MOVER | **aceita** | 19 | 38001 → 38005 | 1987-2008 em 38005 (3 ou 4 edições) e revisão da Cynthia (folha 38 #4 e #6). O IBGE 2017 (Recreação > Outras) é compatível; a linha fina não muda o grupo. 2017: |  | claude-ia (ADR 0007) |
| p06 | MOVER | **aceita** | 14 | 38005 → 38004 | 1995, 2002 e 2017 em 38004 e revisão da Cynthia (folha 38 #11). |  | claude-ia (ADR 0007) |
| p07 | MOVER | **aceita** | 1 | 38005 → 38001 | Cynthia folha 38 #5. 2002:33002 (baldinho de praia junto com bolas, boia, pingue-pongue) não sai de 38004: a célula mistura brinquedo e material esportivo (R1). |  | claude-ia (ADR 0007) |
| p08 | MOVER | **aceita** | 1 | 38004 → 37005 | Revisão da Cynthia confirmada pelas outras edições. |  | claude-ia (ADR 0007) |
| p09 | MOVER | **aceita** | 3 | 38005 → 38003 | Revisão da Cynthia confirmada pelas outras edições. |  | claude-ia (ADR 0007) |
| p10 | MOVER | **aceita** | 1 | 38005 → 32004 | Revisão da Cynthia confirmada pelas outras edições. |  | claude-ia (ADR 0007) |
| p11 | MOVER | **aceita** | 1 | 40006 → 38005 | Revisão da Cynthia confirmada pelas outras edições. |  | claude-ia (ADR 0007) |
| p12 | MOVER | **aceita** | 1 | 40006 → 38004 | Revisão da Cynthia confirmada pelas outras edições. |  | claude-ia (ADR 0007) |
| p13 | MANTER | **aceita** | 10 | 38004 →  | A revisão manual propunha adotar 2017 (38005, 38006 ou 40003); a v4 não segue porque 1987-2008 (4 edições) concordam em 38004 Diversões e esportes e o outlier é |  | claude-ia (ADR 0007) |
| p14 | MANTER | **aceita** | 1 | 38004 →  | 1987:3302 reúne bolas, raquetes e outros equipamentos com a sapatilha; mover a célula para calçados levaria todo o material esportivo junto (R1). Fica em 38004. |  | claude-ia (ADR 0007) |
| p15 | MOVER | **aceita** | 10 | 38002;38005 → 31003 | O serviço de telefonia móvel estava em quatro grupos (38002, 31003, 38005, 38002). Serviço × aparelho é observável nas cinco edições e é a divisão do IBGE (Habi |  | claude-ia (ADR 0007) |
| p16 | REGRA | **aceita** | 0 |  →  | R5 (exemplo da própria CONSTITUICAO). |  | claude-ia (ADR 0007) |
| p17 | MOVER | **aceita** | 2 | 32003;32004 → 42003 | Linha, ramal e central telefônica estão em 42003 em 2002 e 2008, como o IBGE (Aumento do ativo). A compra do direito de linha era ativo; 1995 (ramal comunitário |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 165
- Regras novas: 1 · pendências resolvidas: 25 · pendências criadas: 0
- Decisões estruturais aplicadas: 2026-10-16_claude-v4_recreacao-e-telefonia#p16 ⇒ PR com label `estrutural` e aprovação de outro membro

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 31003 | Telefonia | 1 3 4 8 9 | 1 4 4 10 16 |
| 32003 | Mobiliarios e artigos do lar | 268 280 336 335 438 | 268 279 336 335 438 |
| 32004 | Eletrodomesticos | 104 125 149 153 137 | 104 124 150 153 137 |
| 37003 | Outros cursos | 3 17 18 54 88 | 3 17 18 54 87 |
| 37005 | Artigos escolares | 7 20 16 8 72 | 8 20 16 8 72 |
| 38001 | Brinquedos e jogos | 7 8 7 3 55 | 7 8 7 5 36 |
| 38002 | Celular e acessorios | 0 3 4 4 11 | 0 2 4 4 4 |
| 38003 | Periodicos livros e revistas | 6 6 6 22 24 | 6 7 7 23 24 |
| 38004 | Diversoes e esportes | 36 57 63 43 37 | 36 57 63 57 40 |
| 38005 | Outras recreacao etc | 29 27 42 89 63 | 29 26 40 70 83 |
| 40006 | Outras despesas diversas | 60 55 56 74 64 | 59 55 56 74 61 |
| 42003 | Outros investimentos | 1 2 8 7 3 | 1 4 8 7 3 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 4 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03202[2002], 16105[2002,2008], 44004[1987,1995], 47001[1987]
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 49 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v4_recreacao-e-telefonia: 17 decisões (aceita 17)`
