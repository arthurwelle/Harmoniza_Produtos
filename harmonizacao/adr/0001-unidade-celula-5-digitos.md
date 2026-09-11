# 0001 — Unidade de decisão: célula de 5 dígitos

Onda: 2026-09-11_arthurwelle_base · Status: aceita · Data: 2026-09-11

## Contexto

- Nos microdados de 2002, 2008 e 2017 o produto vem com 7 dígitos (V9001; em 2002, quadro + 5 dígitos).
  O cadastro do IBGE descreve o código como "3 dígitos + 2 dígitos referente ao sequencial".
- O de-para (TodosJuntos) e o pacote harmonizaPOF juntam por 5 dígitos: `pof_budget.R` faz
  `floor(CodProd / 100)` e comenta "tira os 2 últimos dígitos (sinônimos)".
- Os 2 últimos dígitos nem sempre são sinônimos. Em 2008, o código 42005 reúne:
  4200501–06 cirurgia/anestesia/obstetrícia, 4200507–08 implante de cabelo, 4200509 instrumentador cirúrgico,
  4200510–11 raio laser, 4200512 fotografia relativa a cirurgia. Em 2002 esses itens tinham códigos de 5 dígitos
  próprios (42015, 42016, 42020, 42023). Em 2017, 42026 repete o padrão (cirurgia + raio laser).
- A aba `2008` da planilha v2026 já tinha uma coluna com classificação por item (implante e laser em 36005,
  instrumentador em 36010, fotografia em 36009), depois sobrescrita pela classificação de 5 dígitos (36006).
- Em 1987 e 1995 o código tem 4 dígitos e não há subdivisão nos microdados.

## Opções consideradas

1. **7 dígitos em 2002+**: mais granular (R2), menos junções forçadas pela R1. Exige reconstruir o de-para a
   partir das abas por ano e mudar o join do pacote.
2. **5 dígitos definitivo**: compatível com o pacote e com o de-para existente. A R1 passa a forçar junções em
   cadeia onde o IBGE agrupou serviços distintos.
3. **Piloto em 5 dígitos, decidir depois**: adiar para uma onda global específica.

## Decisão

Opção 2. Célula = `Ano:Codigo` com 5 dígitos em 2002/2008/2017 e 4 dígitos em 1987/1995. Itens de 7 dígitos
na mesma célula são inseparáveis para a harmonização.

## Motivos (IA)

A IA recomendou a opção 3 para não travar a primeira onda, e apresentou como argumentos da opção 2 a
compatibilidade com o pacote harmonizaPOF e com todo o trabalho já feito sobre o de-para de 5 dígitos.

## Motivos (humanos)

arthur escolheu "5 dígitos definitivo" depois de ver a lista de 7 dígitos em torno de 2008:42005, e registrou:

> "Às vezes é absurdo o que eles juntam (não parecem sinônimos), mas para todos os efeitos são indissociáveis a
> sete dígitos; só o que vale são os 5 dígitos."

Ou seja: o agrupamento do IBGE pode ser semanticamente estranho, mas o código de 7 dígitos não é uma unidade
utilizável; a unidade real do dado é o código de 5 dígitos.

## Consequências

- A R1 atua sobre células de 5 dígitos. No quadro 42 (saúde) isso cria cadeias a decidir na primeira onda:
  raio laser e fotografia relativa a cirurgia (código próprio em 1987–2002, dentro de cirurgia em 2008/2017);
  implante de cabelo (em 2002 junto de "outros tratamentos", em 2008 dentro de cirurgia); instrumentador
  cirúrgico (em 2002 junto de enfermeira, em 2008/2017 dentro de cirurgia).
- O pacote harmonizaPOF não muda.
- Reabrir esta decisão exige nova ADR que revogue esta.
