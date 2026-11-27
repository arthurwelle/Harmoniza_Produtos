# Plano: entrada da POF 2024-2025 na harmonização

Onda candidata: `2026-11-27_arthurwelle_entrada-2024` (provisória, fora do repositório)

## Por que agora

Os microdados da POF 2024-2025 saíram em novembro de 2026, e o pipeline de `POF2024/` (scripts 1–4)
já reproduz os totais do IBGE. Falta o `Cod_harmo` para pôr 2024 na mesma série de 1987–2017.
Hoje o script 3 deixa a coluna vazia.

## Base

Estado vigente em `base/`, commit `ac864e8` (21/11/2026). Inclui o merge do PR #1 (v4 do Tales
com as edições da Cynthia) e as ondas de 21/11 (ADR 0009 e 0010). Esse commit está num clone
local sem push; ver `base/ORIGEM.txt`.

## Unidade de 2024

Célula = `2024:Codigo`, com o **código de 6 dígitos**. O V9001 de 2024 tem 8 dígitos, e os 2
últimos são sinônimos ou regionalismos, como os 7→5 dígitos de 2002–2017. É a extensão direta da
ADR 0001. Ao mesclar, precisa de adendo à ADR 0001.

Como não há Cadastro de Produtos de 2024 na primeira divulgação, a descrição da célula é o `ITEM`
dos tradutores IBGE (Despesa Geral, Alimentação, Rendimento, Serviços). Isso dá uma descrição por
célula, não a lista de sinônimos de 8 dígitos. Todas as 5.538 células têm descrição.

## Método (segue a hierarquia de evidência da CONSTITUICAO)

1. **Estrutura.** O mapa de quadros 2024→2017 é derivado dos dados: são os pares de células com
   descrição idêntica e única (`saida/mapa_quadros_2024_2017.csv`). Usamos também o caminho de
   níveis dos tradutores IBGE. A codificação de níveis é a mesma em 2017 e 2024: o nível 3
   concorda em 99,6% dos pares idênticos. Os níveis só são comparados entre variáveis principais
   (`v8000`). Nos códigos de rendimento, o tradutor de despesa traz o caminho da dedução, que não
   é comparável.
2. **Classificação-base.** O `Cod_harmo` da célula 2017 correspondente.
3. **Texto.** Primeiro o casamento exato, depois o aproximado. O aproximado é o máximo entre três
   medidas: o texto inteiro, o núcleo antes do parêntese e a contenção de tokens. Fica restrito
   aos quadros 2017 mapeados.

## Tipos usados

- **ATRIBUIR** (novo, não estrutural): célula nova de 2024 recebe grupo **existente**. É o
  análogo de MOVER para uma célula sem grupo. Ao mesclar, registrar na ADR.
  - **ALTA**: descrição idêntica no quadro mapeado, um único grupo, nível IBGE compatível. Ou texto
    quase igual, com score ≥ 0,95.
  - **MÉDIA**: texto aproximado com score ≥ 0,80, ou ≥ 0,70 com o nível 4 IBGE igual, sem rival
    de outro grupo. Ou descrição idêntica com o nível 3 reclassificado pelo IBGE (R8: mantém o
    grupo).
- **REVISAR** (confiança BAIXA): nada é aplicado. A célula vai com `Cod_harmo_sugerido` e os
  candidatos.

Nenhuma proposta CRIA, UNE ou DIVIDE grupos. Produtos novos de 2024 (bets, carro de aplicativo,
jogos on-line etc.) e possíveis junções R1 ficam em REVISAR para decisão humana com ADR.

## Riscos e hipóteses

- O mesmo texto nem sempre é o mesmo produto: o IBGE pode ter mudado o escopo de um código
  mantendo o nome. A comparação de participações (passo 3) existe para pegar isso.
- O texto aproximado pode errar entre itens irmãos do mesmo quadro. Por isso, a regra do "rival"
  rebaixa para REVISAR quem tem um candidato próximo em outro grupo.
- R1 com 2024: se uma célula 2024 junta itens que estão em grupos separados até 2017, a R1 obriga
  a unir esses grupos em todos os anos. A candidata mais clara é `201005 PACOTE DE SERVICOS (FIXO
  E/OU CELULAR E/OU INTERNET E/OU TV E/OU STREAMING)`, que está em REVISAR.
