# Relatório — 2026-10-16_claude-v4_alimentos-vazios-e-grupos

Tipo `familia` · autor claude-v4 · fechada em 2026-10-16

Grupos de alimentos com ano vazio (A01) e grupos sugeridos no formulário. Busca pelo nome do produto em todas as edições: na maioria dos vazios o produto existe, com código próprio, em outro grupo (R4); a distinção é observável, então a v4 preenche o grupo em vez de uni-lo (R2).

## Decisões (24: aceita 24)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 2 | 03117 → 03107 | LARANJA BAHIA é o mesmo código e o mesmo produto em 1987, 1995, 2002, 2008 e 2017; nas três edições recentes está em 03107, nas duas antigas em 03117 Tangerina. |  | claude-ia (ADR 0007) |
| p02 | MOVER | **aceita** | 3 | 03108;03109;03110 → 03118 | Em 1995 os códigos 6612-6614 são LARANJA LIMA, SELETA e PÊRA, mas herdaram os grupos de 1987 (Açúcar, Campista, Abril) pelo número do código (pendência q3, cópi |  | claude-ia (ADR 0007) |
| p03 | REGRA | **aceita** | 0 |  →  | R5: o produto não era observado separadamente naquele ano. |  | claude-ia (ADR 0007) |
| p04 | MOVER | **aceita** | 3 | 03118 → 03201 | CAQUI tem código próprio nas cinco edições; 1987/1995 em 03201, 2002-2017 em 03118. A distinção é observável em todos os anos (R2): preenche o vazio de 03201. |  | claude-ia (ADR 0007) |
| p05 | MOVER | **aceita** | 2 | 12205 → 05202 | 2008:65006 e 2017:65006 (FARINHA DE MILHO, FUBA, MASSA DE PUBA...) estão em 12205 Pamonha, erro claro; 1987-2002 têm o mesmo produto em 05202. Preenche o vazio  |  | claude-ia (ADR 0007) |
| p06 | MOVER | **aceita** | 2 | 05101 → 05203 | FECULA DE MANDIOCA / CARIMA tem código próprio nas edições; 1987-2002 em 05203. Preenche o vazio (R2/R4). |  | claude-ia (ADR 0007) |
| p07 | MOVER | **aceita** | 3 | 07103;07109 → 07108 | LAGARTO PAULISTA (REDONDO) está em 07108 em 1987/1995; em 2002 em 07109 Patinho e em 2008/2017 em 07103 Carne não especificada, enquanto a versão orgânica de 20 |  | claude-ia (ADR 0007) |
| p08 | MOVER | **aceita** | 2 | 07103 → 07109 | BOLA DO PATINHO está em 07109 em 1987, 1995 e 2002 (e a orgânica de 2008/2017 também); só a comum de 2008/2017 caiu em 07103. |  | claude-ia (ADR 0007) |
| p09 | MOVER | **aceita** | 3 | 15209 → 15303 | CAFE DE CEVADA tem código próprio nas cinco edições; 1987/1995 em 15303. Preenche o vazio de 15303. |  | claude-ia (ADR 0007) |
| p10 | MOVER | **aceita** | 4 | 16104 → 16101 | FRANGO ASSADO OU DEFUMADO (PARA VIAGEM) tem código próprio nas cinco edições, no quadro de alimentos preparados. A v3 sugeria unir 16101 em 16104; com a distinç |  | claude-ia (ADR 0007) |
| p11 | MOVER | **aceita** | 5 | 16104 → 16102 | MASSAS PRONTAS (PREPARADAS PARA CONSUMO) tem código próprio nas cinco edições; 1987/1995 em 16102. Preenche o vazio de 16102 em 2017 (R2). |  | claude-ia (ADR 0007) |
| p12 | MOVER | **aceita** | 2 | 16104 → 05206 | MASSA DE ARROZ crua, no quadro de farinhas e massas, está em 05206 em 1987 e 2002; em 2008/2017 caiu em 16104 (alimento preparado). |  | claude-ia (ADR 0007) |
| p13 | UNIR | **aceita** | 1 | 01199 → 01199 | SEMENTE DE LINHACA está em 01199 em 2008 e 2017; 16016 só existe por causa dela, sem nível e num ano só (R3). Une e extingue 16016. |  | claude-ia (ADR 0007) |
| p14 | MANTER | **aceita** | 19 | 36009;36010 →  | Estado atual confirmado: Colírio, soro, material de curativo: 36009 é o grupo das outras edições. A planilha antiga não traz evidência melhor (R8). |  | claude-ia (ADR 0007) |
| p15 | MANTER | **aceita** | 17 | 01199;01299 →  | Estado atual confirmado: Centeio, amendoim, gergelim, arroz japonês: 01199 é consistente nas edições. A planilha antiga não traz evidência melhor (R8). |  | claude-ia (ADR 0007) |
| p16 | MANTER | **aceita** | 14 | 01203;01299 →  | Estado atual confirmado: Sementes, sorgo, quinoa: 01299 consistente; feijão branco em 01203 é coerente. A planilha antiga não traz evidência melhor (R8). |  | claude-ia (ADR 0007) |
| p17 | MANTER | **aceita** | 2 | 01208 →  | Estado atual confirmado: Feijão semipronto e azuki em Outros feijões é coerente. A planilha antiga não traz evidência melhor (R8). |  | claude-ia (ADR 0007) |
| p18 | MANTER | **aceita** | 5 | 15210 →  | O grupo sugerido no formulário já existe na base, com células nas cinco edições (R2 atendida). Nada a criar; os membros de comida fora de casa saem na onda próp |  | claude-ia (ADR 0007) |
| p19 | MANTER | **aceita** | 5 | 15211 →  | O grupo sugerido no formulário já existe na base, com células nas cinco edições (R2 atendida). Nada a criar; os membros de comida fora de casa saem na onda próp |  | claude-ia (ADR 0007) |
| p20 | MANTER | **aceita** | 9 | 15212 →  | O grupo sugerido no formulário já existe na base, com células nas cinco edições (R2 atendida). Nada a criar; os membros de comida fora de casa saem na onda próp |  | claude-ia (ADR 0007) |
| p21 | MANTER | **aceita** | 5 | 15304 →  | O grupo sugerido no formulário já existe na base, com células nas cinco edições (R2 atendida). Nada a criar; os membros de comida fora de casa saem na onda próp |  | claude-ia (ADR 0007) |
| p22 | MANTER | **aceita** | 7 | 12303 →  | O grupo sugerido no formulário já existe na base, com células nas cinco edições (R2 atendida). Nada a criar; os membros de comida fora de casa saem na onda próp |  | claude-ia (ADR 0007) |
| p23 | MANTER | **aceita** | 5 | 12304 →  | O grupo sugerido no formulário já existe na base, com células nas cinco edições (R2 atendida). Nada a criar; os membros de comida fora de casa saem na onda próp |  | claude-ia (ADR 0007) |
| p24 | MANTER | **aceita** | 9 | 12305 →  | O grupo sugerido no formulário já existe na base, com células nas cinco edições (R2 atendida). Nada a criar; os membros de comida fora de casa saem na onda próp |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 289
- Regras novas: 1 · pendências resolvidas: 18 · pendências criadas: 0
- Decisões estruturais aplicadas: 2026-10-16_claude-v4_alimentos-vazios-e-grupos#p03, 2026-10-16_claude-v4_alimentos-vazios-e-grupos#p13 ⇒ PR com label `estrutural` e aprovação de outro membro

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 01199 | Outros | 5 4 2 3 4 | 5 4 2 3 4 |
| 01203 | Feijão-manteiga | 1 1 1 1 2 | 1 1 1 1 2 |
| 01208 | Outros feijões | 10 10 7 9 11 | 10 10 7 9 11 |
| 01299 | Outras | 1 1 2 6 7 | 1 1 2 6 7 |
| 03107 | Laranja-baía | 0 0 1 1 1 | 1 1 1 1 1 |
| 03108 | Laranja-lima | 1 1 1 1 1 | 1 0 1 1 1 |
| 03109 | Laranja-pêra | 1 1 1 1 1 | 1 0 1 1 1 |
| 03110 | Laranja-seleta | 1 1 1 1 1 | 1 0 1 1 1 |
| 03117 | Tangerina | 2 2 1 1 1 | 1 1 1 1 1 |
| 03118 | Outras; Outras laranjas; Goiaba; Acerola | 9 11 39 50 56 | 9 14 38 49 55 |
| 03201 | Caqui | 1 1 0 0 0 | 1 1 1 1 1 |
| 05101 | Farinha de mandioca | 1 1 1 3 3 | 1 1 1 2 2 |
| 05202 | Fubá de milho; Creme de milho | 1 1 1 0 0 | 1 1 1 1 1 |
| 05203 | Fécula de mandioca | 1 1 1 0 0 | 1 1 1 1 1 |
| 05206 | Flocos de cereal; Flocos de aveia; Flocos de outro | 8 7 5 12 21 | 8 7 5 13 22 |
| 07103 | Carne não especificada | 2 1 9 5 7 | 2 1 9 3 5 |
| 07108 | Lagarto redondo | 1 1 0 1 1 | 1 1 1 2 2 |
| 07109 | Patinho | 1 1 2 1 1 | 1 1 1 2 2 |
| 12205 | Pamonha | 2 2 2 2 2 | 2 2 2 1 1 |
| 12303 | Mel de abelha | 1 1 1 2 2 | 1 1 1 2 2 |
| 12304 | Melado de cana | 1 1 1 1 1 | 1 1 1 1 1 |
| 12305 | Gelatina | 1 1 1 4 5 | 1 1 1 4 5 |
| 15209 | Outras | 1 2 6 8 14 | 1 2 5 7 13 |
| 15210 | Agua de coco | 1 1 1 1 1 | 1 1 1 1 1 |
| 15211 | Caldo de cana | 1 1 1 1 1 | 1 1 1 1 1 |
| 15212 | Chocolate engarrafado ou encartonado | 1 2 1 3 3 | 1 2 1 3 3 |
| 15303 | Outros | 1 2 0 0 2 | 1 2 1 1 3 |
| 15304 | Café em grão | 1 1 1 1 1 | 1 1 1 1 1 |
| 16101 | Frango assado ou defumado | 1 0 0 0 0 | 1 1 1 1 1 |
| 16102 | Massa; Massa preparada | 2 2 2 1 0 | 2 2 3 3 2 |
| 16104 | Refeição; Refeição pronta | 23 44 76 129 242 | 23 43 74 125 238 |
| 36009 | Material de tratamento | 11 32 38 14 22 | 11 32 38 14 22 |
| 36010 | Outras assistencia saude | 15 15 13 13 12 | 15 15 13 13 12 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 5 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03202[2002], 37004[1987], 38002[1987], 44004[1987,1995], 47001[1987]
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 156 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v4_alimentos-vazios-e-grupos: 24 decisões (aceita 24)`
