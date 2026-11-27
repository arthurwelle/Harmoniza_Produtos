# Relatório: proposta de harmonização de produtos da POF 2024-2025

Status: **de-para 2024 completo** (`saida/depara_2024_final.csv`, passo 4, decisões da IA a pedido do Arthur). Falta a aprovação humana das pendências estruturais e a mesclagem no repositório. Nada foi aplicado ao de-para vigente de 1987–2017.
Base: commit `ac864e8` (21/11/2026). Método: ver [plano.md](plano.md).

## Resumo

Das 5.538 células de 2024 (4.276 com registro nos microdados):

| Tipo | Confiança | Células | % do valor de 2024 |
|---|---|---:|---:|
| ATRIBUIR, descrição idêntica | ALTA | 4.802 | 82,2 |
| ATRIBUIR, texto quase igual (score ≥ 0,95) | ALTA | 69 | 4,4 |
| ATRIBUIR, texto aproximado | MÉDIA | 192 | 8,0 |
| ATRIBUIR, idêntica mas o IBGE reclassificou o nível 3 | MÉDIA | 59 | 0,7 |
| **REVISAR** | BAIXA | **416** | **4,7** |

O "valor" soma despesa e renda (média mensal por UC, ponderada). No cenário estrito, que só usa
as células ATRIBUIR, **4,0% da despesa total de 2024 fica sem grupo**. Na renda, são 5,4%.
As atribuições usam 319 grupos existentes. Nenhum grupo foi criado, unido ou dividido.

## O que precisa de decisão humana (`saida/revisar_2024.csv`)

| Motivo | Células | Observadas | % do valor |
|---|---:|---:|---:|
| Candidatos ambíguos ou nível IBGE diverge | 104 | 88 | 2,46 |
| Correspondência fraca (score < 0,80) | 213 | 175 | 1,52 |
| Sem correspondente em 2017 (produto novo?) | 77 | 64 | 0,68 |
| Mesma descrição em grupos diferentes em 2017 | 22 | 18 | 0,04 |

A maior parte do valor em REVISAR é de casos em que a sugestão quase certamente está certa, mas o
texto mudou demais para a regra automática:

- **Aplicações financeiras** (510002–510006, 511002–511005: CDB, Tesouro Direto, fundos, ações):
  vão para 47003, Aplicações de capital. Em 2017 a categoria era um item só, "FUNDO DE APLICACAO
  FINANCEIRA (CDB, RDB...)"; em 2024 está desdobrada.
- **Telefonia** (`201005` pacote de serviços, `425001` pré-pago, `425002` pós-pago): sugestão
  31003. **Sem essas três células, Telefonia cai de 2,26% (2017) para 0,29% (2024)**; com elas,
  vai a 1,19%. O pacote de 2017 já estava em 31003 enquanto a TV por assinatura avulsa ia para
  31007. O pacote de 2024 inclui streaming, então a convenção deve ser revista à luz da R1.
- **Outros óbvios:** `401019 ALCOOL/ETANOL` (erro de digitação do IBGE, "COMBUTIVEL") → 34003;
  `402004 QUENTINHA, MARMITA` → 16201; `408007 PARA ESTRESSE/ANSIEDADE` → 36001; cartórios
  `420001`/`420002` → 40004.

**Produtos novos, candidatos a CRIAR ou a R5 (estruturais, exigem ADR):**

| Código | Descrição | Valor/UC |
|---|---|---:|
| 401007 | Carro de aplicativo (urbano) | 36,28 |
| 421009 | Carro de aplicativo (viagem) | 1,96 |
| 404001 | Bets | 4,77 |
| 404002 | Jogos on-line tipo "tigrinho" | 3,87 |
| 505008 | Pé-de-Meia | 1,35 |
| 430010 / 430011 | FIES e crédito educativo | 2,32 |

Em 2017 há "táxi" e "jogos e apostas". A pergunta é se juntar os novos itens com eles (R3:
não criar grupo que 1987–2017 não alimentam) ou criar grupo com ausência estrutural (R5).

**Rendimentos:** `503006 COMISSAO DE VENDA` (R$ 55/UC) não tem correspondente textual. Em 2017 a
comissão provavelmente estava dentro do rendimento do trabalho principal. Decidir entre 44001 e
um grupo de "outros rendimentos do trabalho".

## Alertas em células atribuídas (20)

- **IBGE reclassificou (18):** academia, pilates, natação, artes marciais etc. (quadro 429). Estão
  com descrição idêntica a 2017 e foram mantidas no grupo de 2017 (R8). O IBGE moveu esses itens
  de nível 3 entre 2017 e 2024. Conferir se a harmonização deve acompanhar.
- **Rival próximo (2):** `201001 ENERGIA ELETRICA` (também parece com "juros e multa de energia",
  31007) e `201008 TV POR ASSINATURA` (também parece com "pacote fixo+TV", 31003). As duas
  atribuições parecem certas, mas vale olhar.

## Avaliação: participação dos grupos 2017 × 2024

Fonte: `saida/comparacao_grupos_despesa.csv`. Comparamos participações na despesa total, porque
os anos estão a preços diferentes. 2017 dá R$ 4.649,03/UC (bate com o IBGE); 2024 dá R$ 7.974,44/UC.

**Os grandes saltos refletem os dados, não o de-para.** Os saltos de Educação (3,7% → 7,1%) e de
Saúde (6,5% → 9,4%) aparecem do mesmo tamanho na classificação do próprio IBGE (nível 3 do
tradutor: Educação 3,78% → 7,00%, Saúde 6,50% → 9,60%). Os grupos sinalizados com SALTO (37001
Cursos regulares ×3,3; 36004 Consulta ×3,1; 36007 Hospitalização ×8,8; 41005 Previdência
privada ×2,8) são todos células 1:1 com descrição idêntica nos dois anos. A mudança está nos
valores de 2024, não na correspondência. Vale conferir com o IBGE se houve mudança de método
nesses quadros (2024: quadros 422, 423 e 430).

Uma exceção explicável: **16103 (agregados de alimentos)** cai de 0,85% para 0,18%. Em 2017 o
"AGREGADO" da caderneta era um balde grande; em 2024 as compras vêm mais desagregadas.

**Grupos que dependem do REVISAR** (a participação muda mais de 20% conforme as sugestões entram
ou não): 31003 Telefonia, 32004 Eletrodomésticos, 34001 Urbano, 40004 Serviços profissionais,
34003 Álcool.

**Vazios (R4):** nenhum grupo com peso ≥ 0,01% em 2017 fica vazio em 2024 no cenário com sugestões.

## Próximos passos sugeridos

1. Revisar `saida/revisar_2024.csv`, começando pelos 20 maiores valores (85% do valor em
   REVISAR). Posso montar a página de revisão no formato usual (`revisao/`) a partir de
   `propostas_2024.csv`.
2. Decidir os estruturais: produtos novos, pacote de telefonia × R1, academia/esportes.
3. Mesclar: adendo à ADR 0001 (unidade de 6 dígitos em 2024), registro do tipo ATRIBUIR, ondas no
   repositório com `decisoes.csv` e `Ano=2024` no `depara.csv`. Depois disso, o script 3 de 2024
   preenche `Cod_harmo` sozinho.


## Atualização: de-para final (passo 4, `scripts/04_resolve.py`)

As 416 células REVISAR foram resolvidas por três regras, todas registradas em `saida/decisoes_2024.csv`:

1. **Decisão explícita** (29 células): cada uma traz o motivo e a célula 2017 análoga. Exemplos:
   console de videogame → 38001 (como 2017:43002); FIES → 41006 (como 2017:48016, crédito educativo);
   Pé-de-Meia → 45005; consertos de relógio e de joia → 39004; carne assada para viagem → 16104.
2. **FRETE** (item novo de 2024, um por quadro, valor ~0): grupo dominante do quadro.
3. **Demais:** aceita a sugestão do passo 2. As 60 de maior valor (95% do valor das BAIXA) foram
   conferidas uma a uma.

| Origem | Confiança | Células | % do valor |
|---|---|---:|---:|
| Passo 2 (automático) | ALTA | 4.871 | 86,6 |
| Passo 2 (automático) | MÉDIA | 251 | 8,7 |
| Passo 4 | ALTA | 8 | 0,0 |
| Passo 4 | MÉDIA | 189 | 4,6 |
| Passo 4 | BAIXA | 219 | 0,04 |

Resultado: **100% das células e do valor de 2024 com `Cod_harmo`**, em 320 grupos (2017 usa 321).
O script `3_POF_2024_DespesasRendas.Rmd` já usa esse de-para, até 2024 entrar na aba TodosJuntos.

**Quanto 2024 difere de 2017.** Pouco na estrutura:
- 88% das células de 2024 têm descrição idêntica à de 2017 (82% do valor); 92,5% têm correspondente
  direto.
- 5.119 das 5.122 células com par apontam para **uma única** célula de 2017. Só 3 juntam células de
  2017.
- 134 células de 2017 foram divididas em mais de uma em 2024. Isso não causa problema: todas herdam o
  mesmo grupo.
- 373 células de 2017 ficaram sem par direto (3,9% do valor de 2017). São, em geral, itens que o IBGE
  renomeou ou desdobrou: aplicações financeiras, telefonia, TV.
- Os quadros foram renumerados, mas o mapeamento quadro a quadro é limpo (`mapa_quadros_2024_2017.csv`).

Ou seja, a harmonização de 2024 é **praticamente uma cópia da de 2017**. O trabalho manual se concentra
em ~30 células com produto novo ou mudança de conceito.

**Telefonia (31003) cai de 2,3% para 1,2%.** A queda é real, não perda no de-para: o próprio tradutor do
IBGE mostra telefone fixo 0,17% → 0,01%, celular 1,06% → 0,71% e pacotes 1,08% → 0,74%.

**Pendências estruturais** (exigem ADR e aprovação humana): `saida/pendencias_estruturais.md`.
- Duas junções R1 que aparecem só em 2024: aluguel de roupa M/F/infantil e pacote de telecom com
  streaming.
- Produtos novos ligados a grupos existentes pela R3: aplicativo de transporte, bets, Pé-de-Meia etc.
- Adendo à ADR 0001 (unidade de 6 dígitos).
- Um erro achado na base de 2017: `2017:32999` está em 34004.
