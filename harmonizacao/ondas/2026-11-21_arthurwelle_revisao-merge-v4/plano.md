# Plano — 2026-11-21_arthurwelle_revisao-merge-v4

Tipo: `global` · grupos: 42001, 40005, 41001 · células extras: 1987:4797, 1987:997, 1995:1292, 1995:1293, 1995:1294, 1995:1295, 1995:4794, 1995:4795, 2002:12092, 2002:12093, 2002:12094, 2002:12095, 2002:47094, 2002:47095, 2002:48094, 2002:48095, 2008:12026, 2008:12027, 2008:12028, 2008:12029, 2008:47094, 2008:47095, 1987:4705, 1987:4711, 1995:4705, 1995:4711, 2017:47006, 2017:47007
· pendências: — · total de células no escopo: 273

## Por que esta onda agora (IA)
Revisão do PR #1 (v4 do Tales, ADRs 0005, 0007 e 0008) antes do merge na `main`. A avaliação de 2026-11-01 e 2026-11-21 (despesa ponderada dos microdados) achou um erro de conceito na v4: as células de **valor do imóvel adquirido** (valor total declarado, que repete o que já está nas células de aquisição/prestação) foram para 42001 Imóvel aquisição, inflando o grupo para 7,5% e 7,2% da despesa total em 2002 e 2008 contra 2,7% em 2017. O IBGE exclui esses códigos do total (o pipeline `3_POF_2008_DespesasRendas_v2.Rmd` os lista em `codigos_fora_total_IBGE`). A varredura das correções do pacote `pofanalise` (Tales) achou ainda o IPTU/ITR de outros imóveis em 40005 (consumo) em 1987, 1995 e 2017, contra 41001 Impostos em 2002 e 2008 e no tradutor do IBGE 2017. O resto da avaliação (comida fora em subgrupos, reforma × manutenção, ingressos, deduções de 1987, aluguel estimado de 1995, AGREGADO, taxas de veículos) vira pendência: são decisões de taxonomia que não devem atrasar o merge.

## Por que esta onda agora (humano)
Arthur (2026-11-21): "eu queria fazer o merge mas com modificações que você aprova". Delegou à IA a escolha das modificações; o push só sai depois da confirmação dele.

## Hipóteses iniciais
1. As 17 células de valor do imóvel (1987:997, 4797; 1995:1292-1295, 4794, 4795; 2002:12092-12095, 47094, 47095, 48094, 48095; 2008:12026-12029, 47094, 47095) duplicam as células de aquisição do mesmo questionário; 2017 não coleta esse valor. Confirmado: em todas as edições com essas células também existem 12001/12002 ou 47001 (ou 901/902, 1201/1202) com o valor pago.
2. IPTU/ITR de outros imóveis: 2002:47005, 47011 e 2008:47008, 47022 já estão em 41001; 1987/1995:4705, 4711 e 2017:47006, 47007 estão em 40005. Confirmado no contexto.
