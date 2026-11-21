# Relatório — 2026-10-16_claude-v4_vestuario-transporte-saude

Tipo `familia` · autor claude-v4 · fechada em 2026-10-16

Vestuário, transporte, higiene e saúde: pares do detector conferidos pelo quadro, seguro de veículo e validação.

## Decisões (24: aceita 24)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | MOVER | **aceita** | 1 | 32003 → 33006 | As outras edições põem os mesmos produtos em 33006, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p02 | MOVER | **aceita** | 1 | 36001 → 35004 | As outras edições põem os mesmos produtos em 35004, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p03 | MOVER | **aceita** | 1 | 36001 → 36009 | As outras edições põem os mesmos produtos em 36009, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p04 | MOVER | **aceita** | 1 | 38006 → 34007 | As outras edições põem os mesmos produtos em 34007, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p05 | MOVER | **aceita** | 1 | 39003 → 39002 | As outras edições põem os mesmos produtos em 39002, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p06 | MOVER | **aceita** | 3 | 40006 → 33004 | As outras edições põem os mesmos produtos em 33004, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p07 | MOVER | **aceita** | 1 | 42003 → 33005 | As outras edições põem os mesmos produtos em 33005, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p08 | MOVER | **aceita** | 1 | 33004 → 39001 | As outras edições põem os mesmos produtos em 39001, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p09 | MOVER | **aceita** | 1 | 34007 → 34004 | As outras edições põem os mesmos produtos em 34004, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p10 | MOVER | **aceita** | 1 | 36001 → 36009 | As outras edições põem os mesmos produtos em 36009, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p11 | MOVER | **aceita** | 4 | 34004 → 34007 | Seguro obrigatório e voluntário estão em 34007 em 2002-2017 e no IBGE (Transporte > Outras); seguro não é manutenção. Gás veicular em 34007 em 2008/2017. |  | claude-ia (ADR 0007) |
| p12 | MOVER | **aceita** | 2 | 41001 → 34007 | O IBGE põe o agregado em Transporte > Outras nas duas edições; o agregado reúne seguro e taxas, não só imposto. |  | claude-ia (ADR 0007) |
| p13 | MOVER | **aceita** | 2 | 34004 → 41001 | MULTAS (quadro 50) estão em 41001 em 2002, 2008 e 2017; 1987/1995 em 34004. |  | claude-ia (ADR 0007) |
| p14 | MOVER | **aceita** | 1 | 34007 → 34001 | CANOA no quadro de transporte coletivo está em 34001 em 2002 e 2008. |  | claude-ia (ADR 0007) |
| p15 | MANTER | **aceita** | 1 | 34004 →  | 2002:43015 SHAMPU está no quadro 43 (acessórios e manutenção de veículos): é shampoo automotivo, 34004 correto. |  | claude-ia (ADR 0007) |
| p16 | MANTER | **aceita** | 1 | 32004 →  | 2017:15111 ALARME está no quadro 15 (aparelhos elétricos de uso doméstico): alarme residencial; o alarme de carro de 2017 (33029) já está em 34004. |  | claude-ia (ADR 0007) |
| p17 | MANTER | **aceita** | 1 | 33003 →  | 2008:36010 CUECA está no quadro 36 (roupa de criança): 33003 correto; o par era a cueca do quadro de homem. |  | claude-ia (ADR 0007) |
| p18 | MANTER | **aceita** | 1 | 34005 →  | 2017:51021 CANOA está no quadro 51 (aquisição de veículos): 34005, como 2002:51025 e 2008:51020. |  | claude-ia (ADR 0007) |
| p19 | MOVER | **aceita** | 7 | 38006 → 32004 | Aparelhos do quadro 15 (aquisição de aparelhos) não podem estar em viagens; 1987/1995 têm videogame em 32004 e a planilha v2026 também. |  | claude-ia (ADR 0007) |
| p20 | MOVER | **aceita** | 1 | 32005 → 39005 | Quadro 31 (serviços pessoais); as outras edições põem em 39005. |  | claude-ia (ADR 0007) |
| p21 | MANTER | **aceita** | 4 | 36009;36010 →  | Estado atual confirmado. Anticoncepcionais em 36010 e teste de gravidez em 36009: coerente. |  | claude-ia (ADR 0007) |
| p22 | MANTER | **aceita** | 3 | 38005 →  | Estado atual confirmado. Bateria musical, revelação fotográfica e luneta em 38005: coerente. |  | claude-ia (ADR 0007) |
| p23 | MANTER | **aceita** | 3 | 35004 →  | Estado atual confirmado. Corega/fixador de dentadura em 35004: coerente nas três edições. |  | claude-ia (ADR 0007) |
| p24 | MANTER | **aceita** | 1 | 36009 →  | Estado atual confirmado. Cotonete em 36009, como 1987:2912. |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 53
- Regras novas: 0 · pendências resolvidas: 23 · pendências criadas: 0
- Decisões estruturais aplicadas: nenhuma

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 32003 | Mobiliarios e artigos do lar | 268 279 336 335 438 | 268 278 336 335 438 |
| 32004 | Eletrodomesticos | 104 124 150 153 137 | 104 124 153 157 137 |
| 32005 | Consertos de artigos do lar | 17 70 79 157 227 | 17 70 78 157 227 |
| 33003 | Roupa de crianca | 38 53 53 49 55 | 38 53 53 49 55 |
| 33004 | Calcados e apetrechos | 41 40 50 70 50 | 44 40 50 69 50 |
| 33005 | Joias e bijuterias | 12 14 12 12 10 | 12 14 13 12 10 |
| 33006 | Tecidos e armarinhos | 14 12 24 24 18 | 14 13 24 24 18 |
| 34001 | Urbano | 12 20 25 17 20 | 12 20 25 17 21 |
| 34004 | Manutencao de veiculo proprio | 42 38 38 21 70 | 40 35 37 22 70 |
| 34005 | Aquisicao de veiculos | 14 21 21 24 26 | 14 21 21 24 26 |
| 34007 | Outros transporte | 2 12 10 11 13 | 3 14 12 11 13 |
| 35004 | Produtos de uso pessoal | 32 35 45 40 30 | 32 35 46 40 30 |
| 36001 | Remedios | 4 37 92 48 74 | 4 37 90 47 74 |
| 36009 | Material de tratamento | 11 32 38 14 22 | 11 32 39 15 22 |
| 36010 | Outras assistencia saude | 15 15 13 13 12 | 15 15 13 13 12 |
| 38005 | Outras recreacao etc | 29 26 40 70 83 | 29 26 40 70 83 |
| 38006 | Gastos com viagens | 21 26 31 41 72 | 21 26 27 37 72 |
| 39001 | Fumo | 20 22 22 22 26 | 20 22 22 23 26 |
| 39002 | Cabeleireiro | 3 3 5 5 2 | 3 3 5 5 3 |
| 39003 | Manicuro e pedicuro | 1 1 1 1 3 | 1 1 1 1 2 |
| 39005 | Outras servicos pessoais | 11 19 24 25 28 | 11 19 25 25 28 |
| 40006 | Outras despesas diversas | 59 55 56 74 61 | 56 55 56 74 61 |
| 41001 | Impostos | 1 41 17 76 18 | 2 42 17 75 17 |
| 42003 | Outros investimentos | 1 4 8 7 3 | 1 4 7 7 3 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 4 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03202[2002], 16105[2002,2008], 44004[1987,1995], 47001[1987]
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 26 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v4_vestuario-transporte-saude: 24 decisões (aceita 24)`
