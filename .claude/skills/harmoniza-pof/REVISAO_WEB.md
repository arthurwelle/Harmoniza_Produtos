# Página de revisão ("Mesa de Revisão POF")

Arquivo único: `revisao/index.html`. Lê `onda.json` (gerado por `hp_onda.py propostas`) e grava vereditos
com motivo. Dois modos, detectados sozinhos:

| | Modo artifact (membro com Claude) | Modo Pages/local (qualquer revisor) |
|---|---|---|
| Dados | `onda.json` publicado junto da página | `?onda=<id>` busca no repo (relativo) ou no raw do GitHub da branch `onda/<id>` |
| Decisões | banco da página (`db`), coleção `ondas/<onda>/decisoes`, doc = id da proposta | navegador (localStorage) + botão **Exportar decisoes.json** |
| Volta ao ledger | Claude: `read_db` → `hp_onda.py importar-db` | revisor manda o arquivo; autor coloca em `ondas/<id>/decisoes.json` |

Documento de decisão (igual nos dois modos):
`{pid, onda, veredito, motivo, revisor, ts, movimentos|null}` — `movimentos` só quando `modificada`.

Regras da página: motivo obrigatório exceto em Aceitar; nome do revisor obrigatório; "aceitar em bloco"
só alcança propostas **não estruturais** ainda pendentes (estrutural sempre uma a uma).

## Publicar (modo artifact)

1. `hp_onda.py propostas ONDA` (gera/atualiza `harmonizacao/ondas/ONDA/onda.json`).
2. Artifact publish:
   - `file_path`: `revisao/index.html`
   - `files`: `{"onda.json": "harmonizacao/ondas/ONDA/onda.json"}`
   - `capabilities`: `{"db": {}}`
   - primeira vez: `favicon` "🧾"; depois omitir (mesma URL é reaproveitada a cada onda; decisões de ondas
     diferentes ficam em coleções diferentes).
   - Sessão nova sem a URL: `Artifact action:list` e procurar "Mesa de Revisão POF".
3. Passar o link ao humano e **esperar** ele dizer que terminou. Não preencher vereditos por ele.

## Trazer decisões de volta

1. `Artifact action:read_db`, `url`, `db_op: list`, `collection: ondas/ONDA/decisoes`, `query: {limit: 1000}`,
   `out_dir: harmonizacao/ondas/ONDA/decisoes_db` (pasta ignorada pelo git).
2. `hp_onda.py importar-db ONDA --dir harmonizacao/ondas/ONDA/decisoes_db` → `decisoes.json`.
3. Conferir contagem de vereditos com o humano; faltando proposta ⇒ pedir que termine.

## Modo Pages/local

- Depois do push da branch: `https://arthurwelle.github.io/Harmoniza_Produtos/revisao/?onda=ONDA`
  (a página publicada na `main` busca `onda.json` no raw do GitHub da branch `onda/ONDA`; outra branch:
  `&branch=nome`; outro arquivo: `&src=URL`).
- Local sem push: `python -m http.server` na raiz do repo e abrir `http://localhost:8000/revisao/?onda=ONDA`.
- Revisor clica **Exportar decisoes.json** e envia (PR, e-mail). Um revisor por onda nesta fase.
