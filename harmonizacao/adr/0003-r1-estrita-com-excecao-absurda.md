# 0003 — R1 estrita, em cadeia, com exceção só para junção absurda

Onda: 2026-09-11_arthurwelle_cirurgia · Status: aceita · Data: 2026-09-11

## Contexto

Com a unidade de 5 dígitos (ADR 0001), o quadro 42 (serviços de saúde) mostra junções que encadeiam grupos:
raio laser e fotografia relativa a cirurgia (código próprio em 1987–2002, dentro de cirurgia em 2008/2017),
implante de cabelo (2002 em "outros tratamentos", 2008 em cirurgia), instrumentador cirúrgico (2002 com enfermeira,
2008/2017 em cirurgia), nutricionista (2002 em consulta médica, 2008 com tratamento dietético), exame ginecológico e
pré-natal (2002 em exames, 2008/2017 em consulta). Aplicada à risca, a R1 junta vários grupos de saúde.

## Opções consideradas

1. R1 sem cascata: mover itens quando não arrasta mais nada; tolerar contaminação onde haveria cascata.
2. R1 estrita: aplicar a cadeia inteira.
3. Tolerância total: nenhuma célula anda por junção feita pelo IBGE.

## Decisão

R1 estrita e em cadeia como padrão. Exceção permitida só quando a junção feita pelo IBGE é absurda (item claramente
de outro conceito); cada exceção é uma regra `excecao_r1` com aprovação estrutural. As cadeias são calculadas por
`hp_particao.py` (componentes conexos entre conceitos que dividem célula), não à mão.

## Motivos (IA)

A IA recomendou a opção 1 para preservar granularidade (R2) e evitar colapsar os serviços de saúde num único
grupo. Registrou que a opção 2 maximiza a comparabilidade, que é o objetivo 1 da constituição.

## Critério de exceção (refinado durante a onda cirurgia)

"Absurdo" era difícil de aplicar: das quatro junções do quadro 42, só uma (implante de cabelo entre acupuntura e
massagem) era claramente estranha, e mesmo assim a R1 estrita uniria consulta médica, exames, tratamento
ambulatorial e cirurgia num grupo de 140 células.

Critério adotado, mais verificável: **é exceção a junção que aparece numa única edição da POF e que o próprio IBGE
desfez nas edições seguintes.** As quatro junções do quadro 42 são de 2002 e estão desfeitas em 2008 e 2017
(implante e instrumentador passam a ficar em cirurgia; exame ginecológico e pré-natal, dentro da consulta;
nutricionista, com os tratamentos). Junção que se repete em mais de um ano não é exceção: é como a POF mede.

## Motivos (humanos)

arthur: "Tendo a ser R1 estrita, mas podem haver exceções onde isso fizer sentido (algum caso muito absurdo)."

Ao ver os quatro cenários calculados, escolheu o cenário B (as quatro junções de 2002 viram exceção), que preserva
consulta médica, exames, tratamentos e cirurgia como grupos distintos nos cinco anos.

## Consequências

- `hp_particao.py` passa a fazer parte do diagnóstico de toda onda com células heterogêneas.
- A primeira aplicação (quadro 42) mostra quais células fazem a ponte entre grupos; o humano julga quais são
  absurdas. O resto da cadeia vira UNIR.
- Constituição (R1) e ledger atualizados com o tipo de regra `excecao_r1`.
