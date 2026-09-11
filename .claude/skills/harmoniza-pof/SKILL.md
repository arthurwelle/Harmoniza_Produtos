---
name: harmoniza-pof
description: Harmonização longitudinal assistida dos produtos das POF 1987–2017 em ondas sucessivas (locais por família, globais de consistência), com propostas da IA, decisão humana numa página de revisão e ledger versionado de motivos (IA e humanos). Use quando o usuário quiser revisar ou corrigir o de-para de produtos POF (Cod_harmo), abrir, continuar ou fechar uma onda de harmonização, tratar pendências (Google Form, planilha de melhorias), grupos vazios em algum ano, mega-baldes, regras de junção/separação, ou gerar a documentação da harmonização.
---

# Harmonização POF em ondas

Rodar da raiz do repo: `python .claude/skills/harmoniza-pof/scripts/<script>` (abaixo só o nome).
Lei do trabalho: [CONSTITUICAO.md](CONSTITUICAO.md) — ler **sempre** antes de propor algo.
Arquivos e schemas: [LEDGER.md](LEDGER.md). Escolha de ondas: [ONDAS.md](ONDAS.md).
Página de revisão: [REVISAO_WEB.md](REVISAO_WEB.md). Grupo/git: [COLABORACAO.md](COLABORACAO.md).

## Ao ser acionada

1. `hp_form.py` (traz sugestões novas do Form como pendências; idempotente).
2. `hp_onda.py status` — branch atual, pendências, validação, candidatas à próxima onda.
3. Na branch `onda/<id>` com pasta já existente: retomar pelo que falta
   (sem propostas.json → passo 2; sem decisoes.json → passo 3; sem decisoes.csv → passo 4).

## Ciclo de uma onda

1. **Escolher.** Apresentar 2–3 candidatas do `status` com o porquê (ONDAS.md). Humano escolhe
   (AskUserQuestion) e diz o que o preocupa. `hp_onda.py abrir --escopo X --tipo T --grupos ... [--celulas ...]
   [--pendencias ...]`. Preencher `plano.md`: motivo IA, motivo humano, hipóteses iniciais.
2. **Diagnosticar.** Ler `contexto.md` inteiro. Ampliar se preciso (`hp_familias.py --grupos ... --saida`,
   pandas em `estado/depara.csv`, `harmonizacao/fonte/`). Havendo célula com itens de conceitos diferentes,
   **calcular a cadeia da R1 com `hp_particao.py`, nunca de cabeça**: escrever `conceitos_regras.csv` na onda
   (regex → conceito, com nota), rodar `--quadros`/`--grupos`, ler componentes, ligações e células-ponte, e usar
   `--simular "ANO:COD#conceito;..."` para medir cada exceção antes de propor (ADR 0003). Examinar a família nos 5 anos:
   células com itens de conceitos distintos (R1), distinções só observáveis em alguns anos (R3), vazios (R4/R5),
   decisões e regras anteriores (R7). Escrever `propostas.json` (schema LEDGER.md), com MANTER explícito
   para o que foi examinado e está bom. `hp_onda.py propostas ONDA` até zerar ERRO.
3. **Decidir.** Poucas questões estruturais de alto impacto → AskUserQuestion; o motivo dado vai para
   `decisoes.json`. Volume → página (REVISAO_WEB.md): publicar, passar link, esperar o humano avisar que
   terminou, `read_db` → `hp_onda.py importar-db`. Revisor sem Claude → Pages + `decisoes.json` exportado.
   Nunca preencher veredito pelo humano.
4. **Aplicar.** Decisão estrutural aceita ⇒ escrever `harmonizacao/adr/NNNN-<slug>.md` (modelo abaixo) antes.
   `hp_onda.py fechar ONDA`. Validação falhou ⇒ estado restaurado; corrigir e repetir. Resumir
   `relatorio.md` para o humano, destacando cobertura antes/depois e o que ficou adiado.
5. **Compartilhar.** `hp_onda.py consolidar`; `git add harmonizacao .claude`; commit
   `onda <id>: <resumo>`. **Perguntar antes de push e de abrir PR.** PR com decisão estrutural ⇒ label
   `estrutural`, aprovação de outro membro. Após merge: `hp_onda.py consolidar --onda ID --pr N`.

Ondas pequenas (≤ 40 propostas). A cada ~3 ondas locais, uma global (`status` avisa; roteiro em ONDAS.md).

## Invariantes

- Nunca editar `estado/*.csv` à mão nem escrever nas planilhas originais.
- Nada muda no de-para sem veredito humano. Rejeitar/modificar/adiar exige motivo.
- Célula `Ano:Codigo` é indivisível. Código de grupo nunca é reusado.
- Conflito com decisão/regra anterior ⇒ campo `conflito` + `revoga`. Nunca silencioso.
- Confiança BAIXA ⇒ REVISAR, nunca mudança.
- Registrar o próprio raciocínio: `plano.md` (por que a onda), `motivo_ia`/`evidencia` (por que a mudança),
  ADR (por que a estrutura). Motivo bom cita célula, ano e regra; não "parece melhor".

## Modelo de ADR

```markdown
# NNNN — <título>
Onda: <id> · Decisões: <id#p01>, ... · Status: aceita
## Contexto
## Opções consideradas
## Decisão
## Motivos (IA)
## Motivos (humanos)   ← revisor na página; aprovador do PR
## Consequências       ← cobertura, regras novas, grupos extintos, o que fica para ondas futuras
```

## Utilitários

- `hp_validar.py [--detalhe]` — mesma auditoria do CI.
- `hp_cobertura.py [--grupos a,b] [--medida itens]` — matriz grupo × ano.
- `hp_estado.py pendencia --origem humano --descricao "..." [--celulas] [--grupos]` — anotar dúvida.
- `hp_estado.py iniciar` só existiu para a onda base; não repetir.
