# 0005 — v3: IA aplica só o óbvio; o resto vira pendência com análise

Ondas: todas as ondas `*_claude-v3_*` · Status: aceita (Arthur, 2026-11-21, com ressalvas da ADR 0009) · Data: 2026-10-16

## Contexto

Arthur pediu para "deixar o claudinho cantando, pedaço a pedaço, até passar por tudo" e criar uma v3 da
harmonização, documentada, juntando a skill, as revisões manuais da Cynthia (folhas 32, 37, 38 e 40006), os
tradutores do IBGE como contexto e as sugestões da auditoria feita com o pacote `pofanalise`. A constituição diz
que nada muda no de-para sem veredito humano. Os dois pedidos se conciliam assim: a IA decide o que é erro óbvio e
deixa registrado que a decisão foi dela; o que exige julgamento vira pendência com a análise pronta.

Arthur, ao mandar o material: "metade é erro óbvio, a outra metade não é nem perto de óbvio e exige compreender o todo
e tomar decisões". Tales escolheu, entre três modos (IA decide tudo marcado; IA só aplica o óbvio; humano revisa cada
onda), **"IA só aplica o óbvio"**, e trabalho só local (branch `v3`, sem push).

## Decisão

1. **Veredito da IA, nunca em nome de humano.** Nas ondas da v3, o campo `revisor` é `claude-ia (ADR 0005)`. Nenhuma
   decisão é atribuída a Arthur, Tales ou Cynthia.
2. **O que a IA aplica (MOVER com veredito `aceita`)** — só célula fora do lugar com evidência que não depende de
   interpretação:
   - **Outlier pontual entre edições** (`hp_outliers.py`): todos os itens da célula que aparecem em outras edições
     estão, em todas elas, num único grupo X; nenhum aparece no grupo atual; pelo menos metade dos itens tem histórico;
     a comparação respeita o conceito do quadro (comida fora de casa só com comida fora de casa; viagem só com viagem);
     a célula não foi tocada por decisão anterior nem citada em regra (R7).
   - E a evidência é forte: **3 ou mais** outras edições concordam (e o tradutor do IBGE não contradiz), **ou** 2
     edições concordam **e** uma segunda fonte independente confirma (tradutor do IBGE ou revisão manual da Cynthia
     para a mesma célula e o mesmo destino). Isso é a confiança ALTA da constituição (convergência de ≥ 2 fontes).
3. **O que vira REVISAR (pendência aberta, nada muda)**: tudo o mais. Em particular: só 2 edições sem segunda fonte;
   tradutor do IBGE contra; célula com itens de conceitos diferentes (R1); mudanças de série inteira, mesmo que
   pareçam erradas (ex.: a compra de "outros imóveis" está em 40005 Imóveis de uso ocasional de forma consistente em quatro edições: é
   decisão, não deslize); ações da Cynthia do tipo "maturação de taxonomia", "resíduo/analogia" e "dúvida em aberto";
   toda proposta estrutural (UNIR, DIVIDIR, CRIAR, REGRA).
4. **Nada estrutural é aplicado pela IA.** Regras novas e grupos novos ficam como propostas REVISAR, com o texto da
   regra pronto.

## Opções consideradas

- IA decide tudo, marcado como provisório: cobriria mais, mas aplicaria escolhas de taxonomia sem humano.
- IA só aplica o óbvio (escolhida).
- Humano revisa cada onda na Mesa de Revisão: segue a skill à risca, mas exige o revisor presente a cada onda.

## Motivos (IA)

O critério de "óbvio" usa a hierarquia de evidência da constituição: estrutura das classificações originais (nível 1),
evidência entre anos (nível 2) e outras harmonizações (nível 4, tradutores do IBGE). Exigir unanimidade item a item e
entre itens impede que a IA mova célula heterogênea (R1) e mantém a R8 (conservadorismo): na dúvida, fica como está.

## Motivos (humanos)

Tales: escolheu "IA só aplica o óbvio" e "só local". Falta a aprovação de um membro (Arthur) para a v3 entrar na `main`.

## Consequências

- Toda decisão da v3 pode ser revertida por uma nova decisão com `revoga`, como qualquer outra (R7).
- As pendências criadas pelas propostas REVISAR carregam a análise da IA; o revisor humano decide a partir delas.
- `hp_ibge.py` e `hp_outliers.py` entram na skill como ferramentas de diagnóstico; `hp_cynthia.py` transforma as
  revisões manuais em células.
