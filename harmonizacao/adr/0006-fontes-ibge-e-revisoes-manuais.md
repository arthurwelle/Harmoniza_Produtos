# 0006 — Tradutores do IBGE e revisões manuais como fontes de evidência

Ondas: todas as ondas `*_claude-v3_*` · Status: aceita (Arthur, 2026-11-21, com ressalvas da ADR 0009) · Data: 2026-10-16

## Contexto

Faltava contexto para a IA decidir células de 2008 e 2017: a classificação oficial do IBGE (em que linha das tabelas
de despesa cada código é somado). Também havia quatro revisões manuais da Cynthia (folhas 32 Habitação, 37 Educação,
38 Recreação e cultura, 40006 Outras despesas diversas; set-out/2026), feitas sobre a planilha do Drive.

## Decisão

1. **Tradutores do IBGE** em `harmonizacao/fonte/ibge/`:
   - `original/`: os arquivos do IBGE (2017: `Tradutor_Despesa_Geral.xls` e `Tradutor_Alimentação.xls`, pacote
     Tradutores_20210304; 2008: `Despesa total 2008 - 2009.doc` e `POF_2008-2009_Codigos_de_alimentacao.xls`).
   - `tradutor_ibge.csv`: código de 5 dígitos → grande grupo, linha e descrição do IBGE (gerado por
     `hp_ibge.py gerar`; o documento de 2008 é lido direto do .doc, com as faixas "06008 a 06011" expandidas).
   - Posição na hierarquia de evidência: nível 4 ("outras harmonizações"). Serve para confirmar ou contestar, nunca
     decide sozinho. A comparação é feita no grande grupo (Habitação, Saúde...) e, fora de alimentos, na linha fina.
   - `hp_ibge.py auditar` lista as células de 2008/2017 cujo grande grupo difere do IBGE (sinal G) ou cuja linha fina
     é de outro grupo do repositório (sinal L). Parte das diferenças é convenção da harmonização (ex.: gastos em viagem
     ficam em 38006 Gastos com viagens; o IBGE os distribui), e isso não é erro.
2. **Revisões manuais da Cynthia** em `harmonizacao/fonte/revisoes_cynthia.csv` (uma linha por ação) e
   `revisoes_cynthia_celulas.csv` (item × ano casado com a célula atual), gerados por `hp_cynthia.py extrair` a partir
   do texto dos PDFs. Cada ação é tratada como evidência de nível 3 (classificação manual) e como pendência humana.
   Como foram feitas sobre a planilha do Drive, o casamento informa se a célula ainda está no grupo de origem.

## Consequências

- O contexto das ondas (`hp_familias.py`) passa a mostrar a linha do IBGE de cada célula de 2008 e 2017 do escopo.
- Ações da Cynthia que coincidem com um outlier detectado por `hp_outliers.py` (mesma célula, mesmo destino) contam
  como segunda fonte independente (ADR 0005).
