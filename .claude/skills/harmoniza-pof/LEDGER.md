# Ledger: arquivos de estado e histórico

Tudo em `harmonizacao/`, CSV UTF-8, separador vírgula, fim de linha LF, tudo texto (códigos com zero à esquerda).

## Identificadores

- **Célula**: `Ano:Codigo` (ex. `2017:42026`). Lista de células separada por `;`.
- **Grupo**: `Cod_harmo` com 5 dígitos texto (`01101`, `36005`, `88888`). Grupo novo ainda sem código: `NOVO:<slug>`.
- **Onda**: `AAAA-MM-DD_<autor>_<escopo>` (ex. `2026-09-12_arthur_cirurgia`). Único entre membros sem coordenação.
- **Proposta/decisão**: `<onda>#<pid>` (ex. `2026-09-12_arthur_cirurgia#p03`).
- **Pendência**: `<onda>#q<n>` (base usa `base#q<n>`).
- **Regra**: `<onda>#r<n>`.

## `estado/` (estado atual — sobrescrito só por `hp_onda.py fechar`)

`depara.csv` — uma linha por item. Ordenado por Ano, Codigo, Descri_Item.
`Ano|Quadro_H|Codigo|Descri_Item|Cod_harmo`

`quadros.csv` — `Ano|Quadro_H|Desc_Quadro` (separado para não repetir texto em 48 mil linhas).

`grupos.csv` — `Cod_harmo|nome|nivel1|nivel2|status|criado_em|extinto_em|substituido_por|nome_original`
- `status`: `ativo` | `extinto`. Extinto nunca volta nem é reusado.
- `nome_original`: texto da aba FINAL (folhas de alimentos lá são listas de membros concatenadas).

`regras.csv` — `id|tipo|enunciado|celulas|grupos|anos|evidencia|autor|onda|status|revogada_por`
- `tipo`: `inseparavel` | `ausencia_estrutural` | `manter_separado` | `equivalencia` | `convencao`.
- `ausencia_estrutural` com `grupos=X` e `anos=1987;1995` justifica vazio de X nesses anos.
- `status`: `ativa` | `revogada`.

`pendencias.csv` — `id|data|origem|descricao|celulas|grupos|onda_alvo|status|resolvida_em`
- `origem`: `Form` | `Melhorias` | `NOTAS` | `validacao` | `IA` | `humano`.
- `status`: `aberta` | `em_onda` | `resolvida` | `descartada`.

## `ondas/<onda>/`

| Arquivo | Quem escreve | Conteúdo |
|---|---|---|
| `escopo.json` | `abrir` | `{onda, autor, tipo, grupos[], celulas[], pendencias[], aberta_em}` |
| `plano.md` | IA + humano | escopo e **por que esta onda agora** |
| `contexto.md` | `hp_familias.py` | pacote de evidência lido pela IA |
| `propostas.json` | IA (validado por `propostas`) | ver schema abaixo |
| `decisoes.json` | página (export) ou IA (a partir do `read_db`) | vereditos humanos |
| `decisoes.csv` | `fechar` | ledger da onda (imutável depois do merge) |
| `relatorio.md` | `fechar` | mudanças aplicadas, motivos, cobertura antes/depois |

### `propostas.json`
```json
{
  "onda": "2026-09-12_arthur_cirurgia",
  "autor_ia": "claude-opus-5",
  "resumo": "texto curto do diagnóstico da onda",
  "propostas": [
    {
      "id": "p01",
      "tipo": "MOVER",
      "titulo": "Cirurgia 2017 para Serviços de cirurgia",
      "movimentos": [{"celulas": ["2017:42026"], "para": "36006"}],
      "novos_grupos": {},
      "regra_nova": null,
      "revoga": [],
      "confianca": "ALTA",
      "regras_ref": ["R2", "R6"],
      "evidencia": "fontes consultadas e o que dizem (divergências explícitas)",
      "motivo_ia": "por que melhora a comparabilidade longitudinal",
      "conflito": null,
      "impacto": "grupos alterados, vazios criados/eliminados, distinções criadas/eliminadas"
    }
  ]
}
```
- `MANTER`/`REVISAR`: `movimentos` vazio; `celulas_analisadas` lista o que foi olhado.
- `CRIAR`/`DIVIDIR`: `para` = `NOVO:<slug>`; `novos_grupos` = `{"<slug>": {"nome","nivel1","nivel2","codigo_sugerido"}}`.
- `UNIR`: movimentos levam todas as células do(s) grupo(s) absorvido(s); `extinguir: ["<cod>"]`.
- `RENOMEAR`: `renomear: {"<cod>": {"nome","nivel1","nivel2"}}`.
- `REGRA`: `regra_nova = {tipo, enunciado, celulas, grupos, anos, evidencia}`.
- `conflito` (R7): `{decisao_anterior, nova_evidencia, solucao}`.
- `hp_onda.py propostas` preenche `contexto_celulas` e `cobertura_antes/depois` para a página.

### `decisoes.json`
```json
{
  "onda": "2026-09-12_arthur_cirurgia",
  "modo": "artifact | local",
  "decisoes": {
    "p01": {"veredito": "aceita", "motivo": "", "revisor": "arthur", "ts": "2026-09-12T10:00:00Z",
            "movimentos": null}
  }
}
```
`veredito`: `aceita` | `rejeitada` | `modificada` | `adiada`. `modificada` traz `movimentos` alterados.
Motivo obrigatório exceto em `aceita`.

### `decisoes.csv`
`id|data|tipo|estrutural|celulas|de|para|movimentos|confianca|regras_ref|evidencia|motivo_ia|veredito|motivo_humano|revisor|revoga|pr`
- `movimentos` compacto: `2017:42026;2017:42027>36006|2008:42001>36006`.
- `pr` preenchido na consolidação pós-merge.

## Regras de escrita

1. `estado/` só muda via `fechar` (exceção: `iniciar` da base). Nunca editar à mão.
2. `decisoes.csv` de onda mesclada é imutável. Corrigir = nova decisão com `revoga`.
3. Planilhas originais (`HarmonizacaoProdutos*.xlsx`) nunca escritas.
4. `DOCUMENTACAO.md` e `decisoes_todas.csv` são gerados (`consolidar`); em conflito de merge, regenerar.
