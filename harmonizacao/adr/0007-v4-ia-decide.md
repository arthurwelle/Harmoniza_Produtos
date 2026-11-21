# ADR 0007 — v4: a IA decide as pendências da v3

Data: 2026-10-16 · Status: aceita (Arthur, 2026-11-21, com ressalvas da ADR 0009) · Branch: `v4` (a partir de `v3`)

## Contexto

A v3 (ADR 0005) só aplicou o óbvio e deixou 200 pendências REVISAR, cada uma com análise e recomendação, além de 7
pendências antigas. Pedido do Tales em 2026-10-16: "faz uma v4 deixando a ia decidir. mas nao mexe na v3".

## Decisão

1. A v4 é uma branch separada (`v4`), criada a partir de `v3`; a v3 não muda.
2. Cada pendência vira uma decisão aplicada (MOVER, MANTER, UNIR, CRIAR ou REGRA), inclusive as estruturais, com
   `revisor = claude-ia (ADR 0007)`. Nenhuma decisão da v4 passa por aprovação humana; esta ADR substitui a aprovação
   de outro membro exigida pela CONSTITUICAO para as estruturais, só nesta branch.
3. Critérios, em ordem:
   - **Quadro antes de descrição.** O mesmo nome em quadros de conceito diferente não é o mesmo produto: inventário
     (q14) × aquisição; rendimentos (q53) × despesa; pequenos reparos (q8) × construção e reforma (q11); acessórios de
     veículo (q43) × higiene. Parte dos "pares" do detector da v3 cai aqui e fica como está.
   - **Série antes do IBGE.** Quando as outras edições concordam entre si no mesmo conceito de quadro, a série
     prevalece sobre o tradutor do IBGE (evidência de nível 2/3 × nível 4). Os números de quadro mudam entre edições sem
     mudar o conceito (ex.: carnes 2002 q69 = 2008/2017 q71).
   - **Revisão humana antes da IA**, salvo quando contraria a série: as ações da Cynthia são aceitas quando as outras
     edições não as contradizem. Não seguidas: aluguel de aparelhos em 32005 e ingressos em 38005/40003 (4 edições contra
     1); homônimos da extração (METRO, LIMA, ACAMPAMENTO) e células com itens misturados (R1).
   - **R2 antes de unir.** Grupo com ano vazio é preenchido quando o produto existe com código próprio noutro grupo
     (laranja-baía, caqui, fubá, fécula, lagarto, café de cevada, frango assado, massa pronta); só se une quando a
     distinção não existe (16016).
   - **R8** nos empates.
4. Decisões estruturais desta ADR (ondas `2026-10-16_claude-v4_*`):
   - `2026-10-16_claude-v4_alimentos-vazios-e-grupos`: UNIR 16016 em 01199 (extinto); REGRA de ausência de 03108,
     03109 e 03110 em 1995.
   - `2026-10-16_claude-v4_comida-fora-de-casa`: CRIAR "Alimentação fora do domicílio" (nível 16.2) com todo o quadro de
     alimentação fora (1987 q22; 1995-2017 q24).
   - `2026-10-16_claude-v4_habitacao-e-reforma`: REGRA (convenção) reforma × manutenção pelo quadro.
   - `2026-10-16_claude-v4_recreacao-e-telefonia`: REGRA de ausência de 38002 em 1987.
   - `2026-10-16_claude-v4_nao-consumo-e-alugueis`: REGRA de ausência de 44004 em 1987 e 1995; REGRA (convenção)
     viagens em 38006 e extinção de 34006.
5. Script: `hp_v4_onda.py` aplica as ondas definidas em `harmonizacao/fonte/v4/decisoes_v4.py` (gera `ondas_v4.json`).

## Consequências

- Todas as pendências da v3 ficam resolvidas; continua aberta a base#q3 (nomes-lista dos grupos de alimentos), que é
  rótulo e não classificação.
- A comida fora de casa deixa de alimentar os grupos de produto: séries de refrigerante, doces, salgados etc. passam a
  medir só o consumo no domicílio, e o novo grupo mede o consumo fora. Para análises que querem o produto
  independentemente do local, o quadro continua no de-para.
- Revisar a v4 = ler `V4.md` e os `relatorio.md` das ondas; reverter uma decisão = nova onda com `revoga` (R7).
