# 0009 — Merge da v4 na main, com ressalvas

Ondas: `2026-11-21_arthurwelle_revisao-merge-v4`, `2026-11-21_arthurwelle_valor-imovel-2017` · Decisões: `2026-11-21_arthurwelle_revisao-merge-v4#p01`, `#p02`, `#p03`, `2026-11-21_arthurwelle_valor-imovel-2017#p01` · Status: aceita · Data: 2026-11-21

## Contexto

O PR #1 (Tales, branch `harmonizacao-v4`) traz a v3 (ADR 0005, a IA aplica só o óbvio), a v4 (ADR 0007, a IA decide
as pendências, inclusive as estruturais) e as edições da Cynthia no Drive (ADR 0008). As três ADRs aguardavam a
aprovação de um membro. A avaliação feita antes do merge, com a despesa ponderada dos microdados, achou:

- um erro de conceito: as células de **valor do imóvel adquirido** (o valor total declarado do bem) foram para
  42001 Imóvel aquisição junto com a aquisição paga. A mesma compra conta duas vezes, e 42001 vai a 7,5% e 7,2% da
  despesa total em 2002 e 2008, contra 2,7% em 2017. O IBGE exclui essas células do total;
- IPTU e ITR de outros imóveis em 40005 (consumo) em 1987, 1995 e 2017, e em 41001 Impostos em 2002 e 2008;
- as decisões que aplicam as edições da Cynthia registradas com revisor `claude-ia`;
- questões de taxonomia que não são erro e pedem decisão humana (comida fora em subgrupos, reforma × manutenção,
  ingressos, deduções de 1987, aluguel estimado de 1995, AGREGADO, taxas de veículos).

## Opções consideradas

1. Recusar o PR até tudo ser resolvido: trava o trabalho do grupo por decisões que não são erro.
2. Aceitar como está: leva o erro dos imóveis para a `main`.
3. Aceitar com as correções do que é erro e registrar o resto como pendência (escolhida).

## Decisão

1. ADRs 0005, 0007 e 0008 aceitas por Arthur, com as ressalvas abaixo.
2. `#p01` CRIAR 89001 "Valor do imovel adquirido (memoria, fora da despesa)", num nível 1 próprio
   (`89. Valores de memoria`, como o 88 Inventário), com as 22 células de valor do imóvel de 1987 a 2008. Revoga em
   parte `2026-10-16_claude-v4_nao-consumo-e-alugueis#p11` (o resto da p11 continua valendo).
3. `#p02` MOVER IPTU/ITR de outros imóveis de 1987, 1995 e 2017 para 41001, como 2002, 2008 e o IBGE.
4. `#p03` O revisor das ondas `2026-11-19_claude-v4_*-drive-cynthia` passa a
   `cynthia (edição no Drive) + claude-ia (ADR 0008)`; nenhuma célula muda.
5. `2026-11-21_arthurwelle_valor-imovel-2017#p01` REGRA de ausência estrutural de 89001 em 2017: o questionário de
   2017 não pergunta o valor total do imóvel, só a aquisição paga.
6. Pendências `2026-11-21_arthurwelle#q1` a `#q7` abertas para as questões de taxonomia.

## Motivos (IA)

R6 e R7: a correção dos imóveis desfaz uma dupla contagem com evidência direta (as células de aquisição paga estão
no mesmo questionário) e com a exclusão pelo IBGE. O IPTU de outros imóveis já estava em Impostos em duas edições.
O nível 1 próprio evita que alguém some o valor do bem ao gasto ao agregar por nível 1.

## Motivos (humanos)

Arthur, 2026-11-21: "eu queria fazer o merge mas com modificações que você aprova". As modificações foram escolhidas
pela IA por delegação e conferidas por Arthur antes do push.

## Consequências

- 42001 passa a 2,0 / 2,6 / 2,6 / 3,9 / 2,7% da despesa total (1987 a 2017).
- O grupo 89001 não é despesa: não entra em consumo, nem em aumento do ativo.
- Ficam para ondas futuras as pendências q1 a q7; a mais urgente é a q1 (subgrupos de 16201, que hoje esconde o
  total de produtos como cerveja e refrigerante).
