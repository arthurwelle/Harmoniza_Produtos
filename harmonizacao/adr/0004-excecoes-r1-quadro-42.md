# 0004 — As quatro exceções da R1 no quadro 42 (saúde)

Onda: 2026-09-11_arthurwelle_cirurgia · Decisões: `#p01`, `#p02`, `#p03`, `#p04` · Status: aceita · Data: 2026-09-11

## Contexto

Com célula de 5 dígitos (ADR 0001) e R1 estrita (ADR 0003), a partição calculada por `hp_particao.py` sobre as
264 células do quadro 42 devolve um componente único de 140 células, reunindo consulta médica (36004), exames
diversos (36008), tratamento ambulatorial (36005), serviços de cirurgia (36006) e ainda células de enfermagem
(36010) e de fotografia de cirurgia (36009). Quatro junções, todas de 2002, produzem essa cadeia.

## Decisão

As quatro viram regra `excecao_r1` (o item não propaga a R1; a célula segue o conceito dominante e o item fica
registrado como contaminação):

| Decisão | Célula | Item que não propaga | Sem a exceção, une |
|---|---|---|---|
| `#p01` | 2002:42015 | implante de cabelo | tratamentos + cirurgia |
| `#p02` | 2002:42016 | instrumentador cirúrgico | enfermagem/tratamentos + cirurgia |
| `#p03` | 2002:42046 | consulta médica nutricionista | consulta médica + tratamentos |
| `#p04` | 2002:42008 | exame ginecológico/pré-natal/preventivo e exame oftalmológico | consulta médica + exames |

Com elas, o quadro 42 fica com consulta médica (59 células), exames (48), tratamentos e enfermagem (22) e
cirurgia (11) como componentes distintos nos cinco anos.

## Motivos (IA)

Critério da ADR 0003: junção que aparece numa única edição e que o próprio IBGE desfez depois. As quatro são de
2002 e estão desfeitas em 2008 e 2017 (implante e instrumentador passam para a célula de cirurgia; exame
ginecológico e pré-natal, para dentro da consulta; nutricionista, para junto dos tratamentos). Já o raio laser e a
fotografia de cirurgia **não** viraram exceção: a junção se repete em 2008 e 2017, é como a POF passou a medir, e
por isso as células de 1987–2002 foram movidas para cirurgia (`#p06`, `#p07`).

## Motivos (humanos)

arthur aceitou as quatro na mesa de revisão, sem comentário adicional, depois de escolher o cenário B entre os
quatro cenários calculados (ver ADR 0003).

## Consequências

- Contaminação registrada e conhecida: o gasto de 2002 com implante de cabelo fica em tratamento ambulatorial; o
  com instrumentador cirúrgico, em enfermagem/tratamentos; a consulta com nutricionista, em consulta médica; os
  exames ginecológico e oftalmológico, em exames diversos.
- Toda análise longitudinal desses quatro grupos em 2002 carrega esse desvio; está documentado em `regras.csv`.
- `hp_particao.py` lê estas regras e não propaga a R1 por essas células nas próximas ondas.
