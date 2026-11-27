# Harmonização de produtos POF 2024-2025 (provisória)

Proposta de `Cod_harmo` para as células da POF 2024-2025, feita sobre a harmonização vigente de
1987–2017 e seguindo a mesma constituição (R1–R8) e o mesmo formato de ledger do repositório
`Harmoniza_Produtos`. **É uma proposta à parte.** Nada aqui foi escrito no repositório nem nas
planilhas. Só depois de revisada entra numa onda e é mesclada com a harmonização já feita.

## Como rodar

Pré-requisito: scripts 1–3 de `POF2024/` já rodados (precisa de `RDS/` e `GZ/`) e os GZ de 2017.

```
cd POF2024/harmonizacao
python scripts/01_universo.py   # fonte/celulas_2024.csv, fonte/celulas_2017.csv
python scripts/02_propoe.py     # saida/propostas_2024.csv, depara_2024*.csv, mapa_quadros
python scripts/04_resolve.py    # resolve REVISAR: saida/depara_2024_final.csv, decisoes_2024.csv
python scripts/03_avalia.py     # saida/comparacao_*.csv (usa o de-para final se existir)
```

Leva cerca de 2 minutos no total (Python 3.10, pandas 1.4).

## Pastas

| Pasta | Conteúdo |
|---|---|
| `base/` | Retrato do estado vigente (`depara`, `grupos`, `regras`, `quadros`, `pendencias`), a `CONSTITUICAO.md` e as ADRs 0001–0010. A origem está em `base/ORIGEM.txt`. |
| `fonte/` | Universo de células: 2024 com descrição IBGE, caminho do tradutor e valor; 2017 com itens, grupo e valor. |
| `scripts/` | Os quatro passos acima. |
| `saida/` | Resultados (ver abaixo). |

## Saídas

| Arquivo | Para que serve |
|---|---|
| `saida/depara_2024_final.csv` | **De-para completo de 2024** (todas as células), formato `estado/depara.csv`. É o que o script 3 de 2024 usa. |
| `saida/decisoes_2024.csv` | Ledger: célula, de, para, confiança, motivo e revisor. |
| `saida/pendencias_estruturais.md` | O que exige ADR e aprovação humana. |
| `saida/propostas_2024.csv` | Uma linha por célula 2024, com tipo, confiança, grupo proposto e sugerido, evidência, motivo e alerta. Este é o arquivo principal. |
| `saida/depara_2024.csv` | De-para no formato de `estado/depara.csv`, só com as células ATRIBUIR (ALTA ou MÉDIA). |
| `saida/depara_2024_com_sugestoes.csv` | O mesmo, acrescido das células REVISAR pela sugestão. Serve só para análise de sensibilidade. |
| `saida/revisar_2024.csv` | As 416 células que precisam de decisão humana, ordenadas por valor. |
| `saida/mapa_quadros_2024_2017.csv` | Correspondência de quadros derivada dos dados. |
| `saida/comparacao_grupos_despesa.csv`, `saida/comparacao_grupos_renda.csv`, `saida/comparacao_nivel1.csv` | Participação de cada grupo em 2017 e em 2024, com sinalizações. |

Ver [plano.md](plano.md) para o método e [relatorio.md](relatorio.md) para os resultados.
