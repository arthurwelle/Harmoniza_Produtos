# Pendências estruturais do de-para 2024 (exigem decisão humana e ADR)

Gerado com o de-para final (`decisoes_2024.csv`). Cada item já tem uma atribuição provisória, para que
o pipeline funcione. Aqui fica o que, pela CONSTITUICAO, não pode ser decidido só pela IA.

## 1. Unidade de 2024 (adendo à ADR 0001)
A célula de 2024 é o código de **6 dígitos**: o V9001 tem 8 dígitos e os 2 últimos são sinônimos.
É o equivalente dos 5 dígitos de 2002–2017. Formalizar, junto com o tipo **ATRIBUIR** (célula nova
que recebe grupo existente, não estrutural).

## 2. Junções R1 que aparecem só em 2024
| Célula 2024 | O que junta | Grupos separados até 2017 | Atribuição provisória | R$/UC |
|---|---|---|---|---:|
| 411005 Aluguel de roupa (M, F e infantil) | aluguel de roupa de homem, mulher e criança | 33001, 33002, 33003 | 33002 | 0,55 |
| 201005 Pacote de serviços (fixo e/ou celular e/ou internet e/ou TV e/ou **streaming**) | pacotes de telecom + streaming | 31003 (pacotes) e 38004 (streaming avulso, 2024:407001) | 31003 | 37,77 |

Proposta: registrar as duas como `excecao_r1` (ADR 0003): junção feita só no ano mais recente, de valor
pequeno no caso do aluguel, ou com conceito dominante claro no caso do pacote (telecom). Assim a
cadeia não une os grupos em 1987–2017.

## 3. Produtos novos sem análogo em 2017 (R3 × R5)
Pela R3, foram ligados a grupos existentes, sem criar grupo que 1987–2017 não conseguem alimentar:

| Célula | Produto | Grupo | R$/UC |
|---|---|---|---:|
| 401007 / 421009 | Carro de aplicativo (urbano / viagem) | 34001 / 38006 (2017 já tinha CABIFY/UBER em 34001) | 36,28 / 1,96 |
| 401008 | Moto de aplicativo | 34001 | 2,97 |
| 404001 | Bets | 40001 Jogos e apostas | 4,77 |
| 404002 | Jogos on-line tipo "tigrinho" | 40001 | 3,87 |
| 505008 / 505007 / 506019 | Pé-de-Meia; Volta por Cima RS; MEI RS calamidades | 45005 Transferências transitórias | 1,35 / … |
| 503006 | Comissão de venda (habitual) | 44001 Empregado (o IBGE 2024 classifica como rendimento do trabalho) | 55,09 |
| 401022 | Carga de veículo elétrico | 34007 Outros transportes | 0,21 |
| 403002 | Cigarro eletrônico | 39001 Fumo | 1,30 |
| *FRETE* (um código em cada quadro) | frete | grupo dominante do quadro | ~0 |

Decidir se algum merece grupo próprio com `ausencia_estrutural` para 1987–2017 (R5). Candidatos:
apostas on-line (bets + tigrinho) e transporte por aplicativo.

## 4. O IBGE reclassificou itens entre 2017 e 2024 (mantido o grupo de 2017, R8)
- Quadro 429 (academia, pilates, natação, artes marciais, aulas esportivas): no IBGE 2024 o nível 3 é
  Recreação (1108); em 2017 era Educação (1107). Mantidos 38004 (academia) e 37003 (aulas).
- Outros 18 itens com descrição idêntica e nível 3 diferente: estão marcados com alerta em
  `propostas_2024.csv`.

## 5. Erros na base 1987–2017 encontrados no caminho
- `2017:32999` AGREGADO do quadro 32 (papelaria) está em **34004 Manutenção de veículo**. Deveria
  ficar em 37005. Em 2024 o análogo (412999) foi para 37005.
- `2008:29999` AGREGADO de remédios está em 35004 (higiene), mas o IBGE conta como saúde. Ver
  `../pendencias_para_harmonizacao.md`.
