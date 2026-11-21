# Plano — 2026-09-11_arthurwelle_cirurgia

Tipo `familia` · grupos 36005 (Tratamento ambulatorial), 36006 (Serviços de cirurgia) · célula extra 2017:42026
· pendências `base#q7` (planilha de melhorias), `base#d4` (farmácia em cirurgia) · 55 células no escopo

## Por que esta onda agora (IA)

- Primeira onda real da skill (piloto ponta a ponta).
- 36006 é o único grupo de saúde com ano vazio (2017). A planilha de melhorias (`base#q7`) aponta a causa:
  2017:42026 "SERVICOS DE CIRURGIA, ANESTESIA E PARTO" caiu em 36005.
- Ao refazer a base pelo master do Drive (ADR 0002), 36006 recebeu 10 células de produtos de farmácia de 1987 e
  2017 sem motivo registrado (`base#d4`).
- A IA tinha recomendado Telefonia como piloto (exercitaria mais regras e sugestões do Form); a escolha foi Cirurgia.

## Por que esta onda agora (humano)

arthur escolheu "Cirurgia" entre Telefonia, Cirurgia, Reforma x manutenção e Educação. A opção foi apresentada
como "menor e mais limpa". Motivo não detalhado.

## Hipóteses iniciais

1. 2017:42026 deve ir para 36006: quebra de série só em 2017.
2. Farmácia em 36006 é erro de digitação no Drive.
3. Outros serviços de 2017 do quadro 42 podem ter caído em grupos errados (a aba 2017 foi montada por PROCV com 2008).
4. A unidade de 5 dígitos (ADR 0001) cria cadeias R1 no quadro 42.

## Diagnóstico (resumo da IA)

- **Hipótese 1 confirmada.** 1987:4205, 1995:4205, 2002:42005 e 2008:42005 estão em 36006. DataZoom (zoom2008),
  tradutores de Contas Nacionais (2003 e 2009: mesmo produto "Saúde mercantil/privada") e a planilha de melhorias
  apontam o mesmo.
- **Hipótese 2 confirmada.** Material de curativo, seringa, termômetro e bolsa de água quente estão em 36009 em
  1995, 2002 e 2008; mamadeira, chupeta e mordedor estão em 36010. Destino: o mesmo grupo dos anos intermediários.
- **Hipótese 3 confirmada.** Em 2017: ambulância (42025) e curandeiro/parteira (42074) caíram em 36005 (36010 nos
  outros anos); hemodiálise (42060) caiu em 36008 (36005 em 2002/2008); psicólogo, fisioterapeuta e fonoaudiólogo
  (42013, 42014, 42016) caíram em 36004 (36005 em 1987–2008); lente de contato (42078) em 36005 e óculos
  (42028–42030) em 36010 (36009 em 1987–2008). Sangue/hemoterapia: 36010 em 1987–2002, 36005 em 2008/2017.
- **Hipótese 4 confirmada.** Com célula de 5 dígitos, a R1 encadeia: raio laser e fotografia relativa a cirurgia
  (código próprio em 1987–2002, dentro de cirurgia em 2008/2017), implante de cabelo (2002 em "outros tratamentos",
  2008 em cirurgia), instrumentador cirúrgico (2002 com enfermeira, 2008/2017 em cirurgia), nutricionista (2002 em
  consulta médica, 2008 com tratamento dietético). Aplicada à risca, junta cirurgia, tratamento ambulatorial,
  enfermagem e consulta médica. Política decidida com o humano antes das propostas (ver decisões da onda).

## Decisão de política durante o diagnóstico (humano)

arthur: "Tendo a ser R1 estrita, mas podem haver exceções onde isso fizer sentido (algum caso muito absurdo)."
Registrado na ADR 0003. Consequência para esta onda: o escopo real da R1 é o quadro 42 inteiro, porque a cadeia
alcança exames (exame ginecológico e pré-natal) e consulta médica (nutricionista). Próximo passo: marcar conceitos
dos itens do quadro 42, calcular a partição com `hp_particao.py` e levar ao humano as células-ponte candidatas a
exceção.
