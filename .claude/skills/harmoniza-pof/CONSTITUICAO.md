# Constituição da harmonização de produtos POF 1987–2017

Texto estável. Não muda entre ondas. Mudança aqui = ADR + PR estrutural.
Origem: `harmonizacao/origem/chatgpt.txt`.

## Objetivo

Construir uma classificação de produtos **comparável entre as edições da POF** (1987, 1995, 2002, 2008, 2017),
com a **maior granularidade compatível** com as classificações originais de cada ano.

A pergunta nunca é "qual categoria combina com esse produto?". É:
**"qual estrutura de grupos maximiza a granularidade sem violar as restrições impostas pelas diferentes POFs?"**

A classificação atual (`estado/depara.csv`) é **hipótese inicial a auditar**, não rascunho a descartar.

## Unidade de decisão: a célula

Célula = `(Ano, Codigo)` original. Todos os `Descri_Item` de uma célula compartilham o mesmo registro de
despesa na POF daquele ano ⇒ são **inseparáveis** ⇒ uma célula tem exatamente um `Cod_harmo`.
Mover um item isolado de uma célula com vários itens **não existe**: move-se a célula inteira.

Tamanhos: 1987 até 49 itens/célula; 1995 sempre 1; 2002 até 53; 2008 e 2017 até 80.

## Regras (aplicar nesta ordem)

**R1 — Junção obrigatória.** Se, em qualquer ano, uma célula contém produtos A e B, então nenhum grupo
harmonizado pode separar A de B em nenhum ano. A distinção observada em outro ano não basta.
Ex.: 1987 `A+B` num código; 2017 `A` e `B` em códigos distintos ⇒ grupo único `A+B`.

**R2 — Máxima granularidade compatível.** Quando a distinção é observável de forma comparável em todos os anos
relevantes, manter grupos separados. Não juntar só porque são parecidos ou da mesma categoria comercial.

**R3 — Sem distinção temporal artificial.** Se 2017 tem "biscoito doce / recheado / wafer" e 1987 só
"biscoitos", o nível harmonizado provável é "biscoitos". Não criar grupos que um ano não consegue alimentar
(salvo R5).

**R4 — Célula vazia é suspeita.** Grupo sem membro num ano exige investigação antes de aceitar:
outro nome? agregado em código mais genérico? junto de outro produto? mudança de questionário/metodologia?
produto inexistente?

**R5 — Ausência estrutural só com evidência.** Vazio legítimo quando o produto não existia ou não era
observado (ex.: celular em 1987). Registrar como regra `ausencia_estrutural` com evidência. Não inventar
correspondência para tapar buraco.

**R6 — Família analisada em conjunto.** Nunca decidir olhando linha isolada. Considerar: códigos vizinhos no
mesmo quadro, descrições similares, células do mesmo grupo, correspondentes nos 5 anos, fontes externas.
Proximidade de código é evidência, não prova de equivalência.

**R7 — Não-contradição.** Decisões e regras anteriores são restrições. Nova decisão que conflite com anterior
deve ser marcada `CONFLITO` com: decisão anterior, nova evidência, solução possível, recomendação.
Nunca alterar decisão anterior em silêncio; revogar é nova decisão com campo `revoga`.

**R8 — Conservadorismo.** Duas alternativas igualmente plausíveis ⇒ manter a atual. Mudança só por ganho de
comparabilidade, coerência ou granularidade. Elegância não é motivo.

Extra — **código nunca reusado.** Código de grupo extinto não volta com outro significado.

## Hierarquia de evidência

1. Estrutura das classificações originais (o que cada ano junta/separa em células).
2. Evidência de agregação/desagregação entre anos (tabelas `compara`, sequência de códigos).
3. Classificação-base manual (`Cod_harmo` da v2026).
4. Outras harmonizações (DataZoom `fonte/zoom*`, tradutores Contas Nacionais, SIDRA tab. 419).
5. Descrição textual dos produtos.
6. Conhecimento econômico/comercial geral.

Fontes discordantes ⇒ registrar divergência explicitamente na `evidencia`.

## Tipos de decisão

| Tipo | Significado | Estrutural? |
|---|---|---|
| MANTER | classificação atual adequada (resposta válida e frequente) | não |
| MOVER | células vão para outro grupo existente | não |
| RENOMEAR | muda nome/nível de grupo, membros iguais | não |
| UNIR | dois ou mais grupos viram um (tipicamente R1/R3) | **sim** |
| DIVIDIR | grupo vira vários (R2, distinção observável em todos os anos) | **sim** |
| CRIAR | grupo novo recebe células | **sim** |
| REGRA | registra regra geral (inseparável, ausência estrutural, equivalência...) | **sim** |
| REVISAR | evidência conflitante; precisa discussão humana, não aplica nada | não |

Estrutural ⇒ ADR + aprovação de outro membro no PR.

## Confiança

- **ALTA** — evidência direta (estrutura dos códigos) ou convergência de ≥2 fontes independentes.
- **MÉDIA** — plausível, depende de interpretação de descrição.
- **BAIXA** — possível, sem evidência suficiente. BAIXA nunca vira MOVER/UNIR/DIVIDIR: usar REVISAR.

## Toda proposta deve responder

1. Diagnóstico: problema, anos, células e grupos afetados.
2. Proposta por célula: atual → proposto, tipo, confiança.
3. Justificativa: por que melhora comparabilidade longitudinal, com regra(s) R citada(s).
4. Impacto: grupos alterados, cobertura antes/depois, vazios criados, distinções criadas/eliminadas.
5. Regra nova candidata, se a análise revelar padrão generalizável.

Não maximizar nem minimizar número de grupos. Maximizar comparabilidade com a maior desagregação possível.
