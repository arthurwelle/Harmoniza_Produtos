# Trabalho em grupo

Repositório: `github.com/arthurwelle/Harmoniza_Produtos`. Cada membro clona e abre o Claude Code na raiz;
a skill é carregada de `.claude/skills/harmoniza-pof/`. Quem não usa Claude revisa pela página
`revisao/` no GitHub Pages e comenta/aprova PRs.

## Fluxo por onda

1. `git switch main && git pull`.
2. `hp_onda.py abrir ...` ⇒ cria branch `onda/<id>` e avisa se o escopo cruza com outra branch `onda/*`
   remota. Sobreposição ⇒ conversar antes (ou escolher outro escopo).
3. **Push cedo** da branch com `escopo.json` + `plano.md`: é assim que o grupo vê o escopo reservado.
4. Diagnóstico, propostas, decisões, `fechar` (ver SKILL.md).
5. Commit; push; PR para `main` com o `relatorio.md` no corpo.
6. PR com decisão estrutural (UNIR/DIVIDIR/CRIAR/REGRA) ⇒ label `estrutural` ⇒ **aprovação de outro membro**.
   Quem aprova confere ADR e motivos; comentário de aprovação é o motivo do segundo humano.
7. Depois do merge: `hp_onda.py consolidar --pr <n>` na main (preenche `pr`, regenera DOCUMENTACAO).

O Claude **sempre pergunta antes de push ou de abrir PR**.

## Por que não dá conflito (e quando dá)

- Decisões ficam em arquivo por onda (`ondas/<id>/decisoes.csv`): duas ondas nunca editam o mesmo arquivo.
- `depara.csv` ordenado por Ano, Codigo, Descri_Item e uma linha por item: ondas em células diferentes
  mesclam linha a linha.
- `DOCUMENTACAO.md` e `decisoes_todas.csv` são gerados: em conflito, aceitar qualquer lado e rodar `consolidar`.
- **Conflito real** = duas ondas mexeram na mesma célula ou criaram o mesmo código novo.
  CI (`hp_validar.py`) acusa E01/E04/E06. Resolver: rebase na main, reabrir propostas afetadas
  (a decisão mais nova deve `revoga`r ou ser refeita), `fechar` de novo.

## Configuração única (dono do repo)

- Settings ⇒ Branches ⇒ proteger `main`: exigir PR, exigir check `validar`, exigir 1 aprovação.
  (Branch protection não distingue label; o combinado é: PR sem label pode ser aprovado pelo próprio fluxo
  de revisão da página, PR `estrutural` só com aprovação de outro membro.)
- Settings ⇒ Pages: servir a partir de `main` (já ativo para o site).
- Colaboradores com permissão de escrita.

## Motivos de quem

| Onde | Quem | O quê |
|---|---|---|
| `plano.md` | IA + autor da onda | por que este escopo agora |
| `propostas.json` → `motivo_ia`, `evidencia` | IA | por que a mudança melhora a comparabilidade |
| `decisoes.csv` → `motivo_humano`, `revisor` | revisor na página | por que aceitou/rejeitou/modificou |
| `adr/*.md` | IA redige, autor completa | decisões estruturais: opções e consequências |
| PR (comentários, aprovação) | segundo membro | validação independente; nº do PR vai para o ledger |
