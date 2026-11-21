# Relatório — 2026-10-16_claude-v3_comida-fora-de-casa

Tipo `familia` · autor claude-v3 · fechada em 2026-10-16

Onda da v3 (ADR 0005): 0 MOVER óbvios (0 células), 1 REVISAR e 0 MANTER. Fontes: detector de outliers entre edições, tradutores do IBGE (2008/2017) e revisões manuais da Cynthia.

## Decisões (1: aceita 1)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | REVISAR | **aceita** | 410 | 01102;02210;02304;02309;03205;04101;04103;05104;06103;06104;06301;06302;06303;07506;11103;11106;11201;11202;11203;11204;11301;11302;11304;12103;12202;12203;12204;12205;12302;12305;15101;15102;15103;15104;15201;15202;15203;15204;15205;15206;15208;15209;15212;15301;15303;15401;15402;16102;16103;16104;16105 →  | Não há como decidir célula a célula sem uma regra: hoje a mesma despesa (refrigerante tomado na rua) muda de grupo conforme a edição. Duas opções coerentes: (A) |  | claude-ia (ADR 0005) |

## Efeito
- Itens do de-para que mudaram de grupo: 0
- Regras novas: 0 · pendências resolvidas: 0 · pendências criadas: 1
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 01102 | Milho seco; Milho em grão; Milho verde em conserva | 5 4 6 7 7 | 5 4 6 7 7 |
| 02210 | Tomate | 2 2 2 2 3 | 2 2 2 2 3 |
| 02304 | Batata não especificada; Batata-baroa; Batata-aipo | 5 4 5 4 5 | 5 4 5 4 5 |
| 02309 | Outras; Cará | 7 7 7 11 14 | 7 7 7 11 14 |
| 03205 | Outras; Pêssego; Morango; Ameixa | 47 51 19 23 26 | 47 51 19 23 26 |
| 04101 | Coco-açaí em pasta; Açaí (emulsão) | 2 2 2 2 1 | 2 2 2 2 1 |
| 04103 | Coco-da-baía | 2 1 3 3 4 | 2 1 3 3 4 |
| 05104 | Farinha vitaminada | 1 1 6 4 4 | 1 1 6 4 4 |
| 06103 | Pão francês | 2 2 1 3 5 | 2 2 1 3 5 |
| 06104 | Pão caseiro; Pão de forma de padaria; Pão de milho | 22 18 22 56 58 | 22 18 22 56 58 |
| 06301 | Biscoito doce | 2 2 4 10 8 | 2 2 4 10 8 |
| 06302 | Biscoito salgado | 1 1 2 5 5 | 1 1 2 5 5 |
| 06303 | Biscoito não especificado; Rosca doce; Rosca não e | 7 7 7 15 28 | 7 7 7 15 28 |
| 07506 | Outras; Cane salgada não especificada; Costela de  | 22 23 19 28 37 | 22 23 19 28 37 |
| 11103 | Leite de vaca fresco | 1 1 1 6 5 | 1 1 1 6 5 |
| 11106 | Outros | 10 7 9 14 12 | 10 7 9 14 12 |
| 11201 | Queijo minas | 2 1 1 5 4 | 2 1 1 5 4 |
| 11202 | Queijo mozarela | 2 2 1 3 3 | 2 2 1 3 3 |
| 11203 | Queijo prato | 2 1 1 3 3 | 2 1 1 3 3 |
| 11204 | Outros queijos; Queijo não especificado; Queijo pa | 15 12 10 25 35 | 15 12 10 25 35 |
| 11301 | Iogurte | 2 2 2 9 9 | 2 2 2 9 9 |
| 11302 | Leite fermentado | 3 3 2 4 3 | 3 3 2 4 3 |
| 11304 | Outros | 1 2 3 6 10 | 1 2 3 6 10 |
| 12103 | Outros | 3 3 11 21 20 | 3 3 11 21 20 |
| 12202 | Doce de fruta | 5 5 7 14 17 | 5 5 7 14 17 |
| 12203 | Sorvete | 3 3 2 8 11 | 3 3 2 8 11 |
| 12204 | Outros; Rapadura; Bombom; Chiclete; Chocolate em t | 27 30 44 74 74 | 27 30 44 74 74 |
| 12205 | Pamonha | 2 2 2 2 2 | 2 2 2 2 2 |
| 12302 | Outros; Polpa de fruta; Gelatina; Mel de abelha | 3 4 4 13 15 | 3 4 4 13 15 |
| 12305 | Gelatina | 1 1 1 4 5 | 1 1 1 4 5 |
| 15101 | Outras aguardentes; Aguardente de cana | 5 7 7 15 15 | 5 7 7 15 15 |
| 15102 | Cerveja | 6 5 6 10 9 | 6 5 6 10 9 |
| 15103 | Vinho | 1 1 1 4 4 | 1 1 1 4 4 |
| 15104 | Outras | 20 30 24 31 33 | 20 30 24 31 33 |
| 15201 | Água mineral | 4 4 6 4 4 | 4 4 6 4 4 |
| 15202 | Refrigerante de cola | 4 3 1 7 4 | 4 3 1 7 4 |
| 15203 | Refrigerante de guaraná | 2 2 2 5 3 | 2 2 2 5 3 |
| 15204 | Refrigerante de laranja | 3 3 1 4 2 | 3 3 1 4 2 |
| 15205 | Refrigerante de limão | 1 1 2 6 4 | 1 1 2 6 4 |
| 15206 | Outros refrigerantes; Refrigerante não especificad | 22 22 28 69 68 | 22 22 28 69 68 |
| 15208 | Suco de fruta envasado | 5 5 8 28 28 | 5 5 8 28 28 |
| 15209 | Outras | 1 2 8 8 14 | 1 2 8 8 14 |
| 15212 | Chocolate engarrafado ou encartonado | 1 2 1 3 3 | 1 2 1 3 3 |
| 15301 | Café moído | 2 1 2 7 3 | 2 1 2 7 3 |
| 15303 | Outros | 1 2 0 0 2 | 1 2 0 0 2 |
| 15401 | Chá-mate | 1 1 1 7 5 | 1 1 1 7 5 |
| 15402 | Outros; Chá preto | 43 10 15 29 46 | 43 10 15 29 46 |
| 16102 | Massa; Massa preparada | 2 2 2 1 0 | 2 2 2 1 0 |
| 16103 | Outros produtos | 30 17 22 28 33 | 30 17 22 28 33 |
| 16104 | Refeição; Refeição pronta | 23 44 76 129 242 | 23 44 76 129 242 |
| 16105 | Salgadinho | 2 2 3 4 5 | 2 2 3 4 5 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 15 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03107[1987,1995], 03201[2002,2008,2017], 03202[2002], 05202[2008,2017], 05203[2008,2017], 07108[2002], 15303[2002,2008], 16016[1987,1995,2008,2017] …
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 224 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v3_comida-fora-de-casa: 1 decisões (aceita 1)`
