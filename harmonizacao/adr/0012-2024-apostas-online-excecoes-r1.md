# 0012 — Apostas on-line como grupo novo, exceções R1 de 2024 e correção de dois agregados

Onda: `2026-11-27_arthurwelle_entrada-2024-estruturais` · Decisões: `#p01` a `#p08` · Status: aceita por Arthur (2026-11-27);
**aguarda validação do grupo**

## Contexto

A entrada de 2024 (ADR 0011) deixou decisões estruturais pendentes (`fonte/2024/saida/pendencias_estruturais.md`).
Duas inconsistências da base também apareceram no caminho:

- `2017:32999` é o AGREGADO do quadro 32 (papelaria em 2017: caneta, régua, borracha → 37005), mas está em **34004
  Manutenção de veículo**. Em 2024, o análogo (412999) foi para 37005.
- `2008:29999` é o AGREGADO do quadro 29 (produtos farmacêuticos), mas está em **35004** (higiene). O IBGE o conta como
  Remédios: documento "Despesa total 2008-2009", item 6.1, códigos 29001 a 29049, 29300 e 29999. Em 2017, o
  AGREGADO do mesmo quadro (2017:29999) já está em 36001. Foi a maior divergência entre a harmonização e o IBGE em
  saúde (0,09 p.p.), achada na análise `POF/Analise_Saude`.

## Opções consideradas

**Apostas on-line**
- (a) Manter em 40001 Jogos e apostas (R3: não criar grupo que 1987-2008 não alimentam).
- (b) Grupo próprio, com ausência estrutural em 1987-2008 (R5).

**Junções que só existem em 2024 (R1)**
- `2024:411005` ALUGUEL DE ROUPA (MASCULINO, FEMININO E INFANTIL): até 2017 eram três células, em 33001, 33002 e
  33003.
- `2024:201005` PACOTE DE SERVIÇOS (fixo, celular, internet, TV e/ou **streaming**): até 2017 o pacote estava em 31003 e
  o streaming avulso em 38004.

A R1 estrita uniria esses grupos em todas as edições. A alternativa é a exceção da ADR 0003: célula no grupo do
conceito dominante, sem propagar a R1.

## Decisão

1. `#p01` MOVER `2017:32999` → 37005 (Artigos escolares).
2. `#p02` MOVER `2008:29999` → 36001 (Remédios).
3. `#p03` CRIAR **40007 Apostas on-line (bets e jogos de azar on-line)**, com:
   - `2017:22029` APOSTA ONLINE, que é uma célula sozinha (sem R1);
   - `2024:404001` BETS;
   - `2024:404002` JOGOS ON-LINE DO TIPO TIGRINHO, FRUTINHA ETC.

   As apostas esportivas fora das bets (404003) e cassino ou jogos presenciais (404022) continuam em 40001.
4. `#p04` REGRA `ausencia_estrutural`: 40007 em 1987, 1995, 2002 e 2008. Não havia aposta on-line nem item no
   questionário.
5. `#p05` e `#p06` REGRA `excecao_r1`:
   - 2024:411005 fica em 33002, como contaminação documentada, de valor ínfimo (R$ 0,55/UC);
   - 2024:201005 fica em 31003 (Telefonia). O conceito dominante é o pacote de telecom; o streaming é um
     componente.
6. `#p07` e `#p08` REGRA `ausencia_estrutural` em 2024:
   - 88888 Inventário: o arquivo de inventário não está na primeira divulgação;
   - 89001 Valor declarado do imóvel: 2024 só tem a aquisição paga, como 2017 (regra
     `2026-11-21_arthurwelle_valor-imovel-2017#r1`).

## Motivos (IA)

- Apostas on-line são um fenômeno novo e grande: R$ 8,64/UC em 2024 entre bets e tigrinho, contra R$ 11,27 de todo o
  restante de 40001 (loterias, jogo do bicho, apostas presenciais etc.). Juntá-las a jogo do bicho e loteria esconderia exatamente o que se quer medir.
- 2017 já tinha uma célula própria (APOSTA ONLINE), então a série começa em 2017 sem violar a R1.
- As exceções R1 seguem a ADR 0003: junção feita só no ano mais recente, com conceito dominante claro, e cujo
  desdobramento quebraria a comparabilidade de 1987-2017 por causa de uma única célula.
- As duas correções de agregado alinham as células ao conteúdo do quadro e à classificação do IBGE.

## Motivos (humanos)

Arthur (2026-11-27): "acato a proposta de tratar como exceção. Transporte por aplicativo já existia em 2017, certo?
Aposta online é criação mesmo, então poderia ser grupo novo. Corrija o erro de 2017 'agregado' e o anterior também
achado."

## Consequências

- **Grupos:** 40007 nasce com células em 2017 e 2024. 40001 perde 2017:22029, 2024:404001 e 2024:404002.
- **Transporte por aplicativo** não ganha grupo: em 2017 já existia `23031` CABIFY | UBER em 34001 (Urbano), e as
  células de 2024 (401007, 401008) estão lá.
- **Regras novas:** duas `excecao_r1` e três `ausencia_estrutural`.
- **2008:** a saúde harmonizada sobe 0,09 p.p. e passa a coincidir com o IBGE; higiene (35004) cai o mesmo tanto.
- **2017:** artigos escolares ganham o agregado de papelaria, e a manutenção de veículo o perde.
