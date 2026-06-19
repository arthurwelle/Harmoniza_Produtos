# Explorador da Harmonização POF 1987–2017

Site estático para explorar e criticar a harmonização v2 dos produtos das POF
(1987, 1995, 2002, 2008, 2017).

## O que faz
- **Árvore** (esquerda): navega N1 › N2 › folha, com busca e badge de qualidade.
- **5 anos** (centro): produtos da folha selecionada em 5 colunas por ano, coloridos
  por confiança do mapeamento. Filtro "confiança < X" no topo isola os duvidosos.
- **Contexto** (direita): aba *Vizinhos* mostra as outras folhas do mesmo N2 (p/ achar
  itens deslocados); aba *Busca global* varre os 48 mil produtos.
- **⚑ Apontar problema**: em produto ou folha, abre um formulário (tipo + texto livre).

## ⚠️ Como rodar
O HTML lê os CSV via `fetch`, então **não funciona por duplo-clique** (`file://` é
bloqueado por CORS). É preciso **servir** a pasta:

```bash
cd web
python -m http.server 8000
# abrir http://localhost:8000
```

No **GitHub Pages** funciona direto (já é servido por HTTP).

## Regenerar os dados
Os CSV em `data/` são gerados a partir de `HarmonizacaoProdutos_v2.xlsx`:

```bash
cd ..
python export_csv_web.py
```

- `data/folhas.csv` — 307 folhas (taxonomia + qualidade).
- `data/produtos.csv` — 48.220 produtos (de-para com confiança e notas).

## Envio de flags (Google Forms)
Os apontamentos vão para um **Google Form** via POST silencioso (`no-cors`). Config no
topo do `<script>` em `index.html`: `GFORM_ACTION` (URL `.../formResponse`) e
`GFORM_ENTRY` (mapa campo→`entry.ID`). As respostas caem na planilha do Form.

Para trocar de form: pegue o link público (`.../viewform`), extraia os `entry.ID` de
cada campo (estão no `FB_PUBLIC_LOAD_DATA_` do HTML) e atualize `GFORM_ENTRY`.

Cada flag também fica salvo no `localStorage` como rascunho. Por ser `no-cors`, o
navegador não confirma o recebimento — assume-se sucesso após o POST.

## Publicar no GitHub Pages
Coloque o conteúdo de `web/` na raiz publicada (ou em `/docs`). Caminhos são relativos.
