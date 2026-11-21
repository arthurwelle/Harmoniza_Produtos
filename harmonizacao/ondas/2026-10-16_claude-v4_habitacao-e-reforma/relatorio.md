# Relatório — 2026-10-16_claude-v4_habitacao-e-reforma

Tipo `familia` · autor claude-v4 · fechada em 2026-10-16

Pendências de habitação: reforma × manutenção (NOTAS, R1 em 1987), pares de 2 edições, mudanças de conceito e jazigo.

## Decisões (20: aceita 20)
| id | tipo | veredito | células | de → para | motivo IA | motivo humano | revisor |
|---|---|---|---|---|---|---|---|
| p01 | REGRA | **aceita** | 0 |  →  | Unir 32001 e 42002 (sugestão das NOTAS) juntaria consumo e aumento do ativo nas cinco edições para resolver um problema de 1987-1995; a separação existe no ques |  | claude-ia (ADR 0007) |
| p02 | MOVER | **aceita** | 2 | 32001 → 42002 | Itens explícitos de construção (convenção acima). 1995:800 é o cabeçalho que mistura construção, reforma e pequenos reparos: fica em 32001 (dominante). |  | claude-ia (ADR 0007) |
| p03 | MOVER | **aceita** | 2 | 40006 → 42002 | Revisão da Cynthia (folha 40006 #10): material de obra, mesmo destino de 1987. Coerente com a convenção. |  | claude-ia (ADR 0007) |
| p04 | MOVER | **aceita** | 1 | 14104 → 32002 | As outras edições põem os mesmos produtos em 32002, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p05 | MOVER | **aceita** | 1 | 31005 → 32001 | As outras edições põem os mesmos produtos em 32001, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p06 | MOVER | **aceita** | 1 | 31007 → 32001 | As outras edições põem os mesmos produtos em 32001, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p07 | MOVER | **aceita** | 2 | 32003 → 32002 | As outras edições põem os mesmos produtos em 32002, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p08 | MOVER | **aceita** | 1 | 32005 → 32003 | As outras edições põem os mesmos produtos em 32003, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p09 | MOVER | **aceita** | 1 | 38001 → 32004 | As outras edições põem os mesmos produtos em 32004, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p10 | MOVER | **aceita** | 1 | 40006 → 31007 | As outras edições põem os mesmos produtos em 31007, no quadro de mesmo conceito. Pela ADR 0007 a série coerente prevalece (R6); a v3 não aplicou só porque falta |  | claude-ia (ADR 0007) |
| p11 | MOVER | **aceita** | 1 | 32003 → 32004 | 2002 e 2008 em 32004 (aparelho elétrico); 1995 herdou o grupo de 1987:1631 (ferramentas) pelo número do código. |  | claude-ia (ADR 0007) |
| p12 | MOVER | **aceita** | 2 | 42001 → 32005 | 1987, 2002 e 2008 em 32005, revisão da Cynthia (folha 32 #9) também; 1995 herdou 'aquisição do imóvel' de 1987:901/902 pelo número. O formulário sugeria 42002,  |  | claude-ia (ADR 0007) |
| p13 | MOVER | **aceita** | 1 | 31007 → 32005 | Conserto/manutenção (quadro 9 de 1995, consertos). Os agregados do quadro 7 (1987:798, 1995:798) ficam em 31007: misturam serviços públicos e combustíveis, e 31 |  | claude-ia (ADR 0007) |
| p14 | MANTER | **aceita** | 1 | 44001 →  | 1987:5311 EMPREGADO está no quadro 53, de rendimentos: é renda do trabalho (44001), não pagamento a empregado doméstico; o par das outras edições é do quadro 19 |  | claude-ia (ADR 0007) |
| p15 | MANTER | **aceita** | 1 | 88888 →  | 2017:14028 está no quadro 14, inventário de bens duráveis; o par das outras edições é do quadro 17, aquisição. Inventário não é despesa. |  | claude-ia (ADR 0007) |
| p16 | MANTER | **aceita** | 1 | 88888 →  | 2008:14008 está no quadro 14, inventário; o par é do quadro 15, aquisição. |  | claude-ia (ADR 0007) |
| p17 | MANTER | **aceita** | 2 | 32001 →  | 2008 (e 2017) separam carpete e papel de parede em pequenos reparos (quadro 8, 32001) e construção/reforma (quadro 11, 42002); 1987-2002 só têm a compra como de |  | claude-ia (ADR 0007) |
| p18 | MANTER | **aceita** | 2 | 42002 →  | Idem: quadro 11 de 2008 é construção e reforma (42002), como 2017. |  | claude-ia (ADR 0007) |
| p19 | MOVER | **aceita** | 2 | 32003 → 32004 | 1995, 2002 e 2008 em 32004; a revisão da Cynthia (folha 32 #20) reverteu o outlier de 2017. O IBGE de 2017 põe em Mobiliário, mas a série prevalece (ADR 0007). |  | claude-ia (ADR 0007) |
| p20 | MOVER | **aceita** | 9 | 40006;42002 → 40003;42002 | Condomínio (taxa) de jazigo, placa e lápide estão em 40003 em 2002-2017 e vão para lá em 1987/1995 (Cynthia folha 40006 #8). Construção e reforma de jazigo segu |  | claude-ia (ADR 0007) |

## Efeito
- Itens do de-para que mudaram de grupo: 35
- Regras novas: 1 · pendências resolvidas: 28 · pendências criadas: 0
- Decisões estruturais aplicadas: 2026-10-16_claude-v4_habitacao-e-reforma#p01 ⇒ PR com label `estrutural` e aprovação de outro membro

## Cobertura dos grupos tocados (células 1987 1995 2002 2008 2017)
| grupo | nome | antes | depois |
|---|---|---|---|
| 14104 | Óleo não especificado; Óleo de girassol; Óleo de c | 15 16 23 26 26 | 15 16 22 26 26 |
| 31005 | Gas domestico | 3 3 2 2 2 | 2 3 2 2 2 |
| 31007 | Outros servicos etc | 13 30 32 36 39 | 13 29 32 36 39 |
| 32001 | Manutencao do lar | 34 108 142 121 100 | 35 106 143 121 100 |
| 32002 | Artigos de limpeza | 42 43 62 57 62 | 42 45 63 57 62 |
| 32003 | Mobiliarios e artigos do lar | 270 281 331 332 434 | 270 278 332 332 432 |
| 32004 | Eletrodomesticos | 104 123 149 152 132 | 104 124 149 152 135 |
| 32005 | Consertos de artigos do lar | 17 67 80 157 227 | 17 70 79 157 227 |
| 38001 | Brinquedos e jogos | 7 8 7 3 56 | 7 8 7 3 55 |
| 40003 | Cerimonias e festas | 12 12 17 17 28 | 14 15 18 18 28 |
| 40006 | Outras despesas diversas | 65 63 61 79 67 | 65 61 58 77 67 |
| 42001 | Imovel aquisicao | 3 10 7 11 6 | 3 8 7 11 6 |
| 42002 | Imovel reforma | 73 11 77 86 103 | 71 12 78 87 103 |
| 44001 | Empregado | 1 5 14 26 8 | 1 5 14 26 8 |
| 88888 | Inventário | 28 33 33 32 32 | 28 33 33 32 32 |

## Validação após fechar
# Validação
ERRO: 0 | ALERTA: 3 | INFO: 1

- **ALERTA A01** 6 grupos com ano vazio sem regra de ausência estrutural (R4)
  - 03202[2002], 16105[2002,2008], 37004[1987], 38002[1987], 44004[1987,1995], 47001[1987]
- **ALERTA A02** Grupo ativo sem nenhuma célula (extinguir ou povoar)
  - 34006
- **ALERTA A03** 5 linhas duplicadas exatas no de-para
- **INFO I01** 126 pendências abertas/em onda

## Commit sugerido
`onda 2026-10-16_claude-v4_habitacao-e-reforma: 20 decisões (aceita 20)`
