# Relatório — 2026-11-22_tales-claude_inspecao-geral

Tipo `global` · autor tales-claude · fechada em 2026-11-22

Inspeção geral da main depois do merge da v4 e das ondas de 2026-11-21, voltada aos problemas que ainda existem (pedido do Arthur). Os candidatos vêm do gasto ponderado por célula, calculado dos microdados com o mesmo método da aba Valores: saltos nas séries e células cujo grupo diverge do das outras edições, ordenados pelo valor. Corrige com MOVER o que tem evidência direta (mesmo item, mesmo conceito de quadro, três ou mais edições concordando, ou erro de código) e deixa como REVISAR o que é critério. Lista completa e o que não é classificação em harmonizacao/INSPECAO_2026-11-22.md.

## Decisões (20: aceita 20)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 4 | 11103 → 11104 | Erro de código na caderneta de 2008 (copiado em 2017): a quebra 2002→2008 das duas séries é a mesma célula. 79043 é a versão orgânica do mesmo item. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p02 | MOVER | **aceita** | 4 | 07208;07503 → 07601 | Mesmo item, mesmo conceito de quadro (carnes no varejo); a série de 07601 só fecha com a célula. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p03 | MOVER | **aceita** | 2 | 07103 → 07105 | Os mesmos itens estão em 07105 em três edições e na versão orgânica de 2008/2017. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p04 | MOVER | **aceita** | 2 | 07203 → 07208 | Carne com osso não é carne moída; segue 2002. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p05 | MOVER | **aceita** | 4 | 11106 → 12301 | Mesmo item em 12301 em três edições e na versão light; 12301 fica sem conteúdo em 2008/2017 sem a correção. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p06 | MOVER | **aceita** | 2 | 07506 → 07404 | Carne suína fresca no quadro de carnes, não salgada; segue 1987-2002. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p07 | MOVER | **aceita** | 6 | 06303 → 06201 | Mesmo item, mesmo quadro (92), três edições em 06201. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p08 | MOVER | **aceita** | 2 | 40005 → 41006 | Os nomes de outros imóveis são resíduo da extração do de-para (as despesas de outros imóveis de 2002 estão no quadro 47). O microdado de 48007/48008 é seguro; a |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p09 | MOVER | **aceita** | 1 | 41006 → 41004 | Mesmo item, mesmo quadro (48), quatro edições em 41004. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p10 | MOVER | **aceita** | 4 | 37006 → 37004 | Mesmo item, mesmo quadro (49), quatro edições em 37004. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p11 | MOVER | **aceita** | 1 | 37004 → 38003 | Mesmo item, mesmo quadro (32), quatro edições e o digital de 2017 em 38003. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p12 | MOVER | **aceita** | 7 | 34007;37005;37006 → 37006;37001;37002 | Três edições concordam em cada item; 34007 (transporte) para uniforme e creche é erro evidente. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p13 | MOVER | **aceita** | 3 | 32004 → 42003 | Aplica a regra da ADR 0007 às três células que ficaram de fora; tira 0,68 p.p. de eletrodomésticos em 1995. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p14 | MOVER | **aceita** | 2 | 34004 → 41001 | Mesmo item, mesmo quadro (50), três edições em 41001. Sai do consumo. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p15 | MOVER | **aceita** | 1 | 34004 → 34007 | Aplica a convenção da ADR 0007 à célula de 1987 que ficou de fora. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p16 | REVISAR | **aceita** | 5 | 37001;37005;37006 →  | Sugestão: 37006 Outras educação em todas (paga à escola, não é artigo escolar), ou 16201 se o critério for 'comida fora'. Valores pequenos antes de 2017. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p17 | REVISAR | **aceita** | 6 | 48001;48002 →  | Definir: medicamento é bem (48001) e compra de animal é bem (48001); 1987/2002 juntam compra e tratamento numa célula (R1), que fica no dominante. A divisão é d |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p18 | REVISAR | **aceita** | 7 | 37003;37006 →  | Sugestão: cursos livres (idiomas, informática, música, preparatórios, aula particular) em 37003 Outros cursos; 37006 para despesas que não são curso (transporte |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p19 | REVISAR | **aceita** | 3 | 40005 →  | Decidir se 40005 é consumo de casa de veraneio (fica) ou despesa patrimonial (41006). Hoje a série é coerente; a questão é de conceito. |  | tales (delegou à IA, 2026-11-22) + claude-ia |
| p20 | REVISAR | **aceita** | 1 | 31007 →  | Não é erro de classificação: conferir no questionário de 1987 se o condomínio vinha embutido no aluguel ou só era perguntado a parte dos domicílios. |  | tales (delegou à IA, 2026-11-22) + claude-ia |

## Efeito
- Itens do de-para que mudaram de grupo: 331
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 5
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 06201 | Bolo de trigo; Outros bolos | 8 7 24 36 40 | 11 10 24 36 40 |
| 06303 | Biscoito não especificado; Rosca doce; Rosca não e | 6 6 5 13 28 | 3 3 5 13 28 |
| 07103 | Carne não especificada | 2 1 9 3 5 | 2 1 9 2 4 |
| 07105 | Contrafilé | 1 1 1 1 1 | 1 1 1 2 2 |
| 07203 | Carne moída | 2 2 1 2 2 | 2 2 1 1 1 |
| 07208 | Outros Capa de filé; Carne não especificada; Carne | 18 15 26 26 31 | 18 15 26 26 31 |
| 07404 | Pernil | 1 1 2 1 2 | 1 1 2 2 3 |
| 07503 | Salsicha; Salsicha comum | 2 2 2 4 4 | 2 2 2 3 3 |
| 07506 | Outras; Cane salgada não especificada; Costela de  | 22 23 19 26 37 | 22 23 19 25 36 |
| 07601 | Linguiça | 6 4 3 2 2 | 6 4 3 4 4 |
| 11103 | Leite de vaca fresco | 1 1 1 4 4 | 1 1 1 2 2 |
| 11104 | Leite de vaca pasteurizado | 2 1 1 5 6 | 2 1 1 7 8 |
| 11106 | Outros | 9 7 6 10 12 | 9 7 6 8 10 |
| 12301 | Chocolate em pó | 1 1 1 1 1 | 1 1 1 3 3 |
| 31007 | Outros servicos etc | 13 30 31 36 39 | 13 30 31 36 39 |
| 32004 | Eletrodomesticos | 104 127 155 160 141 | 103 126 155 160 140 |
| 34004 | Manutencao de veiculo proprio | 40 37 37 22 70 | 38 36 37 22 70 |
| 34007 | Outros transporte | 3 12 12 11 13 | 2 12 12 11 13 |
| 37001 | Cursos regulares | 2 4 7 5 8 | 4 6 7 5 8 |
| 37002 | Curso superior | 1 2 4 5 9 | 1 3 4 5 9 |
| 37003 | Outros cursos | 3 15 15 52 87 | 3 15 15 52 87 |
| 37004 | Livros e revistas tecnicas | 3 5 5 5 1 | 3 5 5 5 4 |
| 37005 | Artigos escolares | 12 24 24 12 73 | 12 20 24 12 73 |
| 37006 | Outras educacao | 15 14 23 23 27 | 15 15 23 23 23 |
| 38003 | Periodicos livros e revistas | 7 7 7 23 25 | 7 7 7 23 26 |
| 40005 | Imoveis de uso ocasional | 10 11 13 17 25 | 10 11 11 17 25 |
| 41001 | Impostos | 4 35 17 75 19 | 5 36 17 75 19 |
| 41004 | Pensoes mesadas e doacoes | 7 11 10 11 11 | 7 11 10 11 12 |
| 41006 | Outras despesas | 9 13 16 83 18 | 9 13 18 83 17 |
| 42003 | Outros investimentos | 1 4 7 7 3 | 2 5 7 7 4 |
| 48001 | Bens para animais | 5 4 5 17 21 | 5 4 5 17 21 |
| 48002 | Serviços para animais | 1 1 1 3 5 | 1 1 1 3 5 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 1 | INFO: 1

- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 13 pendências abertas/em onda

## Commit sugerido
`onda 2026-11-22_tales-claude_inspecao-geral: 20 decisões (aceita 20)`
