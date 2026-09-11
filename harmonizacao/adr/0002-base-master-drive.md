# 0002 — Onda base a partir do master do Google Drive

Onda: 2026-09-11_arthurwelle_base · Status: aceita · Data: 2026-09-11

## Contexto

Havia duas versões da planilha de harmonização:

| | Local `HarmonizacaoProdutos_v2026.xlsx` (22/06/2026) | Master do Drive (`link.txt`) |
|---|---|---|
| Abas | 19, incluindo as de evidência (zooms, abas por ano com código de 7 dígitos, comparações) | 2 (FINAL, TodosJuntos) |
| Linhas / células | 48.220 / 20.145 | igual |
| Grupos | 297 | 319 (22 novos, 31004 fundido em 31003 "Telefonia") |
| Células com grupo diferente | — | 518 |

Das 518 diferenças, 387 correspondem a sugestões do Google Form aplicadas no Drive entre 10 e 21/07/2026
por `aplicar_sugestoes.Rmd`. As outras 131 foram editadas sem registro de motivo: parte parece correção
(1987: cursos saem de "Manutenção de veículo" para Educação; cinema e teatro saem de "Artigos escolares"),
parte parece erro (1987: material de curativo, termômetro, mamadeira e chupeta vão para 36006 "Serviços de
cirurgia"). Outras 434 células diferem só no formato do código (zero à esquerda).

A primeira versão da onda base (commit afb8e47) foi importada da planilha local.

## Opções consideradas

1. Base no master do Drive; evidência continua vindo da planilha local.
2. Manter a planilha local; as 518 diferenças viram pendências.

## Decisão

Opção 1. A onda base foi refeita com FINAL e TodosJuntos do Drive (cópia em
`harmonizacao/origem/HarmonizacaoProdutos_drive_2026-09-11.xlsx`); as abas de evidência continuam extraídas da
planilha local.

## Motivos (IA)

O Drive contém o trabalho mais recente do grupo (22 grupos novos e 387 decisões vindas do Form). Partir da
versão local obrigaria a redecidir esse trabalho. A IA recomendou a opção 1.

## Motivos (humanos)

arthur tinha escolhido a planilha local no início sem perceber que o `link.txt` apontava para outra versão; ao ver a
comparação, escolheu o Drive.

## Consequências

- Sugestões do Form com data anterior ao último corte de aplicação entram como pendências **resolvidas** na base;
  as posteriores ficam abertas.
- As 131 células sem motivo registrado viram pendências de auditoria (`base#d*`), agrupadas por par de grupos,
  e a lista completa fica em `ondas/2026-09-11_arthurwelle_base/diferencas_harmonizacaoprodutos-v2026.csv`.
- `Codigo` é normalizado sem zeros à esquerda (o pacote harmonizaPOF junta por inteiro).
