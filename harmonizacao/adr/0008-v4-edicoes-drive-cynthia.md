# ADR 0008 — v4 incorpora as edições da Cynthia na planilha do Drive

Data: 2026-11-19 · Status: aceita (pedido do Tales; aguarda revisão do Arthur) · Branch: `v4`

## Contexto

A planilha do Drive (abas TodosJuntos e FINAL) foi editada depois da importação da base deste repositório (ADR 0002,
commit `2807869`). Em 372 células o grupo da planilha é diferente do da base: são as revisões da Cynthia aplicadas
direto no Drive, inclusive o nível novo **48. Animais** (48001 Bens, 48002 Serviços). A v3 e a v4 partiram da base e não
viam essas edições; das 372, 154 já coincidiam com a v4, 217 a v4 não tinha tocado e 1 a v4 tinha movido para outro
grupo. Além disso, 13 movimentos da v3/v4 tinham sido justificados por uma série que a Cynthia mudou depois.

## Decisão

1. Edição humana registrada no Drive prevalece sobre decisão da IA (critério 3 da ADR 0007, sem a exceção da série,
   porque aqui a série é a dela). Lista completa em `fonte/v4/edicoes_drive_cynthia.csv`.
2. `2026-11-19_claude-v4_animais-drive-cynthia`: CRIAR 48001 "Bens para animais" e 48002 "Serviços para animais"
   (nível 1 "48. Animais"), com os códigos da planilha. A IA completa só os anos que ficariam vazios (2002 quadro 95 em
   48001; 1995:1640 em 48002) e a compra de animal de 2008 (48001, como 2017).
3. `2026-11-19_claude-v4_edicoes-drive-cynthia`: aplica as demais edições e desfaz os movimentos da v3/v4 contrariados
   pela série da Cynthia, entre eles o aluguel de aparelhos: com 1987-2008 em 32005 no Drive, 2017 volta a 32005 e a
   decisão `2026-10-16_claude-v4_nao-consumo-e-alugueis#p13` é revogada.
4. `2026-11-19_claude-v4_parciais-drive-cynthia`: completa a folha 38 #12 (piscina em parque e piquenique em 38005),
   que o Drive aplicou só em parte.
5. Exceções, por conceito de quadro: o karaokê do quadro 15 (compra de aparelho) fica em 32004 e a parafina de 2017
   (quadro 30, higiene) volta a 35004, não ao grupo das outras edições.
6. A comida fora de casa (16201) não é afetada: nenhuma edição do Drive toca nos quadros 22/24.

## Consequências

- A v4 passa a conter o trabalho da Cynthia; as abas geradas para o Drive deixam de sinalizar essas células.
- Ficam para a Cynthia conferir (não alterados): medicamento para animal em 48001 em 2008 e em 48002 em 2017; compra
  de animal em 48002 em 1987/2002 e em 48001 em 2017; funeral de animal (2017) em 40006.
