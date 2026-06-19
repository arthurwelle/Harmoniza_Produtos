# Explorador da Harmonização de produtos POF 1987–2017

Site estático para explorar e criticar a harmonização dos produtos das POF
(1987, 1995, 2002, 2008, 2017).

## O que faz
- **Árvore** (esquerda): navega N1 › N2 › folha, com busca e badge de qualidade.
- **5 anos** (centro): produtos da folha selecionada em 5 colunas por ano, coloridos
  por confiança do mapeamento. Filtro "confiança < X" no topo isola os duvidosos.
- **Contexto** (direita): aba *Vizinhos* mostra as outras folhas do mesmo N2 (p/ achar
  itens deslocados); aba *Busca global* varre os 48 mil produtos.
- **⚑ Apontar problema**: em produto ou folha, abre um formulário (tipo + texto livre).


No **GitHub Pages** funciona direto (já é servido por HTTP).

https://arthurwelle.github.io/Harmoniza_Produtos/

## Regenerar os dados
Os CSV em `data/` são gerados a partir de `HarmonizacaoProdutos_v2.xlsx`:

- `data/folhas.csv` — 307 folhas (taxonomia + qualidade).
- `data/produtos.csv` — 48.220 produtos (de-para com confiança e notas).

## Envio de flags (Google Forms)
Os apontamentos vão para um **Google Form** via POST silencioso.


