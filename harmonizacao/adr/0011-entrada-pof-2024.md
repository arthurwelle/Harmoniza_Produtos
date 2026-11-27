# 0011 — Entrada da POF 2024-2025 (célula de 6 dígitos e tipo ATRIBUIR)

Onda: `2026-11-27_arthurwelle_entrada-2024` · Decisões: `#a0001` a `#a5538` · Status: aceita por Arthur (2026-11-27);
**aguarda validação do grupo**

## Contexto

O IBGE divulgou em novembro de 2026 a primeira versão dos microdados da POF 2024-2025, com 8 arquivos: morador,
despesas coletiva e individual, caderneta, aluguel estimado, rendimentos e pesos de replicação. O pipeline
`POF2024/1..4_POF_2024_*.Rmd` reproduz os totais oficiais: despesa total R$ 7.974,44/UC; a diferença de R$ 2,99 para os
7.977,43 do IBGE vem de linhas duplicadas no tradutor do IBGE. Rendimento monetário (7.036,08) e não monetário
(1.663,38) batem exatamente.

Três diferenças importam para a harmonização:

- o V9001 tem **8 dígitos** (eram 7). Os 2 últimos são sinônimos ou regionalismos, como em 2002-2017;
- os quadros **recomeçam a numeração em cada questionário**, então o quadro 1 existe na POF 2, 3 e 4;
- não há Cadastro de Produtos na primeira divulgação. A descrição de cada código vem dos tradutores do IBGE
  (Despesa Geral, Alimentação, Rendimento, Serviços).

## Opções consideradas

1. Esperar o Cadastro de Produtos e a divulgação completa.
2. Fazer agora a entrada com a unidade de 6 dígitos, casando com 2017 pela descrição, pelo quadro equivalente e pelo
   nível do tradutor do IBGE.

## Decisão

Opção 2.

- **Unidade:** a célula de 2024 é o código de **6 dígitos** (extensão da ADR 0001). `Quadro_H` de 2024 = 3 primeiros
  dígitos (questionário + quadro, ex.: 209 = POF 2 quadro 9).
- **Tipo de decisão novo `ATRIBUIR`** (não estrutural): uma célula de edição nova, ainda sem grupo, recebe grupo
  existente. É o análogo de MOVER para quem ainda não tem grupo.
- **As 5.538 células de 2024** entram com o grupo de `fonte/2024/saida/decisoes_2024.csv`:
  - 4.802 por descrição idêntica à de 2017 no quadro equivalente;
  - 320 por descrição quase igual;
  - 416 decididas pela IA, uma a uma ou por regra explícita. As 60 de maior valor foram conferidas
    individualmente.
- **Quando o IBGE mudou o nível de um item entre 2017 e 2024**, prevalece o grupo de 2017 (R7/R8). Exemplo: as aulas
  esportivas, que passaram de Educação para Recreação no tradutor.
- A **CONSTITUICAO** passa a citar 2024 e o tipo ATRIBUIR. `ANOS` inclui "2024" nos scripts e no site.

## Motivos (IA)

A estrutura de 2024 é quase uma cópia da de 2017:

- 88% das células têm descrição idêntica (82% do valor);
- das 5.122 células com par, 5.119 apontam para uma única célula de 2017;
- o mapa de quadros 2024 → 2017, derivado dos dados, é limpo;
- o nível 3 do tradutor concorda em 99,6% dos pares idênticos.

Esperar o Cadastro de Produtos não mudaria a unidade nem os grupos: só acrescentaria sinônimos às descrições.

## Motivos (humanos)

Arthur (2026-11-27): "avalie se podemos fazer praticamente uma cópia dos códigos harmonizados de 2017 para 2024 ...
Faça a harmonização de produtos"; depois do relatório: "acato a proposta ... leve para a harmonização, rode, faça upload
na ferramenta".

## Consequências

- 2024 entra em todos os grupos de consumo, menos 88888 (Inventário: arquivo ainda não divulgado) e 89001 (valor
  declarado do imóvel: 2024, como 2017, só tem a aquisição paga). Os dois recebem `ausencia_estrutural` na onda
  `2026-11-27_arthurwelle_entrada-2024-estruturais`.
- As decisões estruturais (grupo novo de apostas on-line, exceções R1 de 2024) estão na ADR 0012.
- Quando o IBGE divulgar o Cadastro de Produtos de 2024, as descrições podem ser enriquecidas, sem mudar as células.
- O **PR #2** (inspeção geral, Tales), ainda aberto, move algumas células de 2017 (ex.: 2017:48009, 49030-33, 32017).
  Se for aceito, as células análogas de 2024 devem seguir o mesmo movimento: reconciliar depois do merge.
- Detalhes do método e dos números: `fonte/2024/` (scripts 01-04, `relatorio_original.md`, `pendencias_estruturais.md`).
