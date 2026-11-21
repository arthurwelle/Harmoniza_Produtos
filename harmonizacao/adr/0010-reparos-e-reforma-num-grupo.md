# 0010 — Reparos e reforma de imóvel num grupo só

Onda: `2026-11-21_arthurwelle_reparos-e-reforma` · Decisões: `2026-11-21_arthurwelle_reparos-e-reforma#p01`, `#p02` ·
Status: aceita por Arthur (2026-11-21); **aguarda validação do grupo** · Pendência resolvida: `2026-11-21_arthurwelle#q2`

## Contexto

Na aba Valores (% do consumo sem aluguel, regiões metropolitanas), 32001 Manutenção do lar dava 1,89% em 1987, 8,54% em
1995 e 4,97 / 6,19 / 4,59% em 2002, 2008 e 2017. O grupo tem duas partes: serviço doméstico (estável, 1,8 a 3,2%) e o
quadro de obras e reparos, que causa a quebra.

- 1987 (quadro 10) e 1995 (quadro 8) usam o mesmo quadro misto: "Construção, reforma e pequenos reparos de imóveis, e
  jardinagem", com os mesmos itens (cimento, azulejo, tinta, mão de obra, agregado). O questionário não separa reparo de
  reforma.
- A base mandou 1987 para 42002 Imóvel reforma (62 de 63 células, fora do consumo) e 1995 para 32001 (consumo).
- De 2002 em diante o questionário separa: quadro 8 (pequenos reparos, 32001) e quadro 11 (construção e reforma, 42002).
- A v4 criou a convenção `2026-10-16_claude-v4_habitacao-e-reforma#r1` (célula mista no grupo dominante, 32001), mas não a
  aplicou a 1987; e a Cynthia (folha 40006 #10 e #11) registrou que em 1995 a separação "não dá pra desambiguar".

## Opções consideradas

| Opção | 1987 | 1995 | 2002 | 2008 | 2017 |
|---|---|---|---|---|---|
| A. 1987 como 1995 (quadro misto em 32001) | 7,29 | 8,54 | 4,97 | 6,19 | 4,59 |
| B. 1995 como 1987 (quadro misto em 42002) | 1,89 | 3,24 | 4,97 | 6,19 | 4,59 |
| C. Unir reparos e reforma | 7,35 | 8,81 | 7,22 | 8,23 | 6,12 |

(% do consumo sem aluguel nas RMs; em C, sobre consumo + reforma.)

A e B corrigem a incoerência entre 1987 e 1995, mas deixam uma quebra entre 1995 e 2002. Só C produz uma série
comparável nas cinco edições.

## Decisão

1. `#p01`: as células de construção e reforma de imóvel (330 células, todas as de 42002 que não são jazigo ou sepultura)
   vão para 32001. A convenção da v4 é revogada.
2. `#p02`: 32001 passa a se chamar "Manutenção do lar, reparos e reforma". 42002 fica só com jazigo e sepultura
   (construção, reforma e aquisição; 23 células nos cinco anos, sem célula misturada com imóvel) e passa a se chamar
   "Jazigo e sepultura (construção, reforma e aquisição)", ainda em Aumento do ativo.

## Motivos (IA)

R3: não manter uma distinção que 1987 e 1995 não conseguem alimentar. O quadro misto liga reparo e reforma nas duas
edições, e qualquer separação nelas seria arbitrária (a A e a B são, cada uma, um "default" diferente).

## Motivos (humanos)

Arthur, 2026-11-21: escolheu a opção C depois de ver as três séries; "deixe anotado o motivo, e depois vamos levar para o
grupo geral para validação".

## Consequências

- A reforma de imóvel passa a contar como **consumo** (nível 1 32 Habitação) em todas as edições. O IBGE a classifica em
  Aumento do ativo: a despesa de consumo da harmonização fica acima da do IBGE pelo valor da reforma (cerca de 1 a 2% do
  consumo em 2002-2017). Quem precisar do conceito do IBGE pode separar, de 2002 em diante, pelo quadro 11 no de-para.
- O grupo deve ser validado pelo grupo de trabalho (Tales, Cynthia). Se a validação preferir a A ou a B, a reversão é uma
  onda nova com `revoga` desta decisão.
