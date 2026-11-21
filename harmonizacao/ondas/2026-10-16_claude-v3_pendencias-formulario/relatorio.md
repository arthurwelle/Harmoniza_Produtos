# Relatório — 2026-10-16_claude-v3_pendencias-formulario

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 6 MOVER óbvios (16 células), 7 REVISAR e 2 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (15: aceita 15)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MANTER | **aceita** | 3 | 01299;15208 →  | As sugestões do formulário já estão aplicadas no estado do repositório. Nada a mudar. |  | claude-ia (ADR 0005) |
| p02 | MANTER | **aceita** | 1 | 36009 →  | Pendência resolvida por decisão anterior desta v3. |  | claude-ia (ADR 0005) |
| p03 | MOVER | **aceita** | 9 | 31007 → 32001 | Combustível doméstico não é serviço: o repositório (2002) e o IBGE (2008) o põem em manutenção do lar, e a sugestão humana do formulário converge. Duas fontes a |  | claude-ia (ADR 0005) |
| p04 | MOVER | **aceita** | 1 | 42001 → 43002 | Outlier pontual de 1995 com descrição diferente (o detector não casou); 1987, 2002, o IBGE e o formulário concordam. |  | claude-ia (ADR 0005) |
| p05 | MOVER | **aceita** | 1 | 43002 → 32001 | Vidro não é prestação de imóvel: o erro de código copiado é inequívoco. O destino 32001 segue a sugestão humana e 2002/2008; a alternativa 42002 faz parte da qu |  | claude-ia (ADR 0005) |
| p06 | MOVER | **aceita** | 3 | 46001 → 46002 | A própria descrição diz bens móveis; 2002, 2017 e a sugestão humana concordam. O grupo 46001 mantém os aluguéis de imóveis. |  | claude-ia (ADR 0005) |
| p07 | MOVER | **aceita** | 1 | 01101 → 01199 | Um agregado de cereais e leguminosas não é arroz; a folha de resíduo do nível é o destino coerente, como pede a sugestão humana. |  | claude-ia (ADR 0005) |
| p08 | MOVER | **aceita** | 1 | 42001 → 31007 | Taxa não é aquisição de imóvel (deslocamento de 2017 no quadro 12). 2008 e a sugestão humana dizem 31007; o IBGE confirma Habitação (linha água e esgoto, que po |  | claude-ia (ADR 0005) |
| p09 | REVISAR | **aceita** | 1 | 31003 →  | Conflita com a reorganização proposta para a telefonia (31003). Decidir junto. |  | claude-ia (ADR 0005) |
| p10 | REVISAR | **aceita** | 2 | 42001 →  | Duas fontes humanas discordam. Recomendação da IA: 32005 (três edições + Cynthia); a v3 não aplicou porque a mudança cruza de 'outras despesas' para consumo sem |  | claude-ia (ADR 0005) |
| p11 | REVISAR | **aceita** | 8 | 42003 →  | A sugestão humana contraria o IBGE; o próprio repositório está dividido entre os anos. Recomendação da IA: manter 42003 (direito de linha é ativo, como o IBGE)  |  | claude-ia (ADR 0005) |
| p12 | REVISAR | **aceita** | 3 | 41006 →  | Série coerente e IBGE concordam com o estado atual. Recomendação da IA: manter (rejeitar a sugestão), salvo razão de conceito. |  | claude-ia (ADR 0005) |
| p13 | REVISAR | **aceita** | 2 | 32001 →  | Faz parte da questão reforma × manutenção do lar (pendência 2026-09-11_arthurwelle#q1, R1 em 1987), que precisa de regra antes de mover células. |  | claude-ia (ADR 0005) |
| p14 | REVISAR | **aceita** | 1 | 15303 →  | Depende da regra da comida fora de casa (onda comida-fora-de-casa da v3). |  | claude-ia (ADR 0005) |
| p15 | REVISAR | **aceita** | 3 | 31007 →  | Agregado mistura os itens do quadro (serviços públicos e combustíveis) e o 909 é conserto: sem par para decidir. Recomendação da IA: agregados acompanham o item |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 20
- Regras novas: 0 · pendências resolvidas: 15 · pendências criadas: 7
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 01101 | Arroz integral; Arroz não especificado; Arroz poli | 5 4 6 10 14 | 4 4 6 10 14 |
| 01199 | Outros | 4 4 1 3 4 | 5 4 1 3 4 |
| 01299 | Outras | 1 1 1 6 7 | 1 1 1 6 7 |
| 15208 | Suco de fruta envasado | 5 5 8 28 28 | 5 5 8 28 28 |
| 15303 | Outros | 1 2 0 0 2 | 1 2 0 0 2 |
| 31003 | Telefonia | 1 3 4 8 9 | 1 3 4 8 9 |
| 31007 | Outros servicos etc | 18 34 32 36 38 | 13 30 32 36 39 |
| 32001 | Manutencao do lar | 29 103 142 121 100 | 34 108 142 121 100 |
| 36009 | Material de tratamento | 11 32 38 14 22 | 11 32 38 14 22 |
| 41006 | Outras despesas | 9 13 22 82 19 | 9 13 22 82 19 |
| 42001 | Imovel aquisicao | 3 11 7 11 7 | 3 10 7 11 6 |
| 42003 | Outros investimentos | 1 2 8 7 3 | 1 2 8 7 3 |
| 43002 | Prestacao de imovel | 1 1 2 2 2 | 1 1 2 2 2 |
| 46001 | Aluguel de bens imoveis | 2 2 1 2 1 | 1 1 1 1 1 |
| 46002 | Aluguel de bens moveis | 0 0 1 0 1 | 1 1 1 1 1 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 14 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 216 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_pendencias-formulario: 15 decisões (aceita 15)`
