# Relatório — 2026-09-11_arthurwelle_cirurgia

Tipo `familia` · autor arthurwelle · fechada em 2026-09-11

Família de serviços de saúde (quadro 42) mais as células de farmácia que a base do Drive pôs em cirurgia. A partição R1 (hp_particao.py, conceitos_regras.csv) mostra que quatro junções isoladas de 2002 uniriam consulta médica, exames, tratamento ambulatorial e cirurgia num grupo de 140 células; as quatro viram exceção (cenário B, ADR 0003). Resolvido isso, o que sobra é célula fora do lugar: sete de 2017 (a aba de 2017 foi montada por PROCV com 2008), o raio laser e a fotografia de cirurgia de 1987-2002 (R1, porque em 2008/2017 estão dentro da célula de cirurgia) e as células de enfermagem.

## Decisões (23: aceita 23)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | REGRA | **aceita** | 0 |  →  | Sem esta exceção, implante de cabelo liga o bloco de tratamentos ao de cirurgia e a R1 obriga a unir 36005 e 36006. A junção existe só em 2002 e o próprio IBGE  |  | arthur |
| p02 | REGRA | **aceita** | 0 |  →  | Sem esta exceção, o instrumentador liga enfermagem a cirurgia e, pela cadeia de 1987:4215 (enfermagem junto de outros tratamentos), une também tratamento ambula |  | arthur |
| p03 | REGRA | **aceita** | 0 |  →  | Sem esta exceção, o nutricionista liga consulta médica ao bloco de tratamentos e a R1 obriga a unir 36004 e 36005. Nutricionista não é médico e nos demais anos  |  | arthur |
| p04 | REGRA | **aceita** | 0 |  →  | Sem esta exceção, o exame ginecológico liga consulta médica a exames diversos e a R1 obriga a unir 36004 e 36008. A junção é de 2002 e está desfeita nas edições |  | arthur |
| p05 | MOVER | **aceita** | 1 | 36005 → 36006 | É a única célula de cirurgia de 2017 e está em tratamento ambulatorial, o que deixa 36006 vazio em 2017 e quebra a série (R4). Todos os anos anteriores têm a cé |  | arthur |
| p06 | MOVER | **aceita** | 3 | 36005 → 36006 | A distinção laser x cirurgia não é observável em 2008 nem em 2017, então não pode existir na harmonização (R1). Diferente das quatro exceções, esta junção se re |  | arthur |
| p07 | MOVER | **aceita** | 3 | 36009 → 36006 | Mesma situação do laser: em 2008 não dá para separar fotografia de cirurgia, então a distinção não pode existir na harmonização. Em 2017 o item deixa de aparece |  | arthur |
| p08 | MOVER | **aceita** | 4 | 36010 → 36005 | Enfermeira e tratamento de enfermagem são inseparáveis em 2008, então a harmonização não pode separá-los (R1). O grupo de destino é o dos tratamentos, onde o co |  | arthur |
| p09 | MOVER | **aceita** | 5 | 36004 → 36005 | São profissionais não médicos cujo atendimento a POF trata como tratamento em todos os anos anteriores. Mantê-los em consulta médica quebra a série dos dois gru |  | arthur |
| p10 | MOVER | **aceita** | 4 | 36005;36010 → 36009 | Mesmo produto, mesmo grupo nos quatro anos anteriores; a mudança em 2017 não tem justificativa nas classificações originais. |  | arthur |
| p11 | MOVER | **aceita** | 1 | 36010 → 36009 | Mesma lista de produtos dos anos anteriores, em outro grupo só em 2017. |  | arthur |
| p12 | MOVER | **aceita** | 1 | 36004 → 36003 | Consulta com dentista e tratamento dentário formam o grupo 36003 em todos os anos anteriores. |  | arthur |
| p13 | MOVER | **aceita** | 1 | 36005 → 36010 | Remoção por ambulância está em outras assistências nos quatro anos anteriores. |  | arthur |
| p14 | MOVER | **aceita** | 1 | 36005 → 36010 | Mesmo conjunto de itens, em 36010 nos quatro anos anteriores. |  | arthur |
| p15 | MOVER | **aceita** | 2 | 36005 → 36010 | Três anos contra dois, e a mudança não vem de mudança na POF: o item de 2008 ainda traz SANGUE HUMANO. Mover os dois anos recentes custa menos do que mover três |  | arthur |
| p16 | MOVER | **aceita** | 1 | 36010 → 36002 | Mensalidade de clínica é pagamento recorrente por assistência, classificado com planos nos três anos em que aparece antes de 2017. |  | arthur |
| p17 | MOVER | **aceita** | 1 | 36008 → 36005 | Hemodiálise é tratamento, não exame, e está em 36005 nos dois anos anteriores em que aparece. |  | arthur |
| p18 | MOVER | **aceita** | 3 | 36008 → 36004 | Pela R1 o conceito de exame ginecológico/preventivo pertence ao bloco da consulta, porque em dois anos não dá para separá-lo dela. Consequência: as células com  |  | arthur |
| p19 | MOVER | **aceita** | 1 | 36008 → 36004 | É consulta médica com especialista, como as demais 40 células de consulta de 2017. |  | arthur |
| p20 | MOVER | **aceita** | 6 | 36006 → 36009 | São produtos de farmácia, não serviço de cirurgia. O destino é o grupo em que os mesmos itens estão nos anos intermediários. |  | arthur |
| p21 | MOVER | **aceita** | 4 | 36006 → 36010 | Mesmos produtos, mesmo grupo dos anos intermediários. Observação para uma onda futura: 36010 (outras assistências à saúde) é um destino estranho para produtos d |  | arthur |
| p22 | MANTER | **aceita** | 35 | 36005;36006 →  | Foram examinadas e a classificação atual é a mais granular compatível com os cinco anos. Nada a mudar (R8). |  | arthur |
| p23 | REVISAR | **aceita** | 8 | 36002;36003;36005;36006;36009;36010 →  | O erro não é pontual do quadro 42: se o PROCV deslocou linhas, o mesmo padrão deve aparecer em outros quadros de 2017. Vale uma onda global só para 2017, compar |  | arthur |

## Efeito
- Itens do de-para que mudaram de grupo: 115
- Regras novas: 4 · pendências resolvidas: 2 · pendências criadas: 1
- Decisões estruturais aplicadas: 2026-09-11_arthurwelle_cirurgia#p01, 2026-09-11_arthurwelle_cirurgia#p02, 2026-09-11_arthurwelle_cirurgia#p03, 2026-09-11_arthurwelle_cirurgia#p04 ⇒ PR com label `estrutural` e aprovação de outro membro

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 36002 | Plano Seguro saude | 1 4 3 5 4 | 1 4 3 5 5 |
| 36003 | Consulta e tratamento dentario | 2 2 3 2 1 | 2 2 3 2 2 |
| 36004 | Consulta medica | 1 1 13 4 43 | 1 2 14 4 39 |
| 36005 | Tratamento ambulatorial | 3 3 8 14 13 | 3 3 8 13 15 |
| 36006 | Servicos de cirurgia | 8 1 1 1 3 | 3 3 3 1 1 |
| 36008 | Exames diversos | 4 7 7 9 27 | 4 6 6 9 24 |
| 36009 | Material de tratamento | 7 33 39 14 14 | 10 32 38 14 21 |
| 36010 | Outras assistencia saude | 14 16 14 12 13 | 16 15 13 13 11 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 7 | INFO: 1

- **ALERTA A01** 23 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 01299[2002], 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 07203[2002] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **ALERTA A05** Regra 2026-09-11_arthurwelle_cirurgia#r1 cita células inexistentes
  - 2002:42015#implante_cabelo
- **ALERTA A05** Regra 2026-09-11_arthurwelle_cirurgia#r2 cita células inexistentes
  - 2002:42016#instrumentador
- **ALERTA A05** Regra 2026-09-11_arthurwelle_cirurgia#r3 cita células inexistentes
  - 2002:42046#nutricionista
- **ALERTA A05** Regra 2026-09-11_arthurwelle_cirurgia#r4 cita células inexistentes
  - 2002:42008#exame_ginecologico, 2002:42008#exame_oftalmologico
- **INFO I01** 60 pendências abertas/em onda

## Commit sugerido
`onda 2026-09-11_arthurwelle_cirurgia: 23 decisões (aceita 23)`
