# Explorador da Harmonização de produtos POF 1987–2017

Site estático para explorar e criticar a harmonização dos produtos das POF
(1987, 1995, 2002, 2008, 2017). No ar em <https://arthurwelle.github.io/Harmoniza_Produtos/>.

## Duas listas, um botão

O botão no topo troca a classificação do site inteiro (árvore, colunas dos anos, busca, vizinhos):

| Lista | De onde vem | Para que serve |
|---|---|---|
| **Repositório** | `data/estado/`, gerado de `harmonizacao/estado/` pela skill `harmoniza-pof` | a harmonização revisada em ondas, com o motivo de cada decisão no próprio item |
| **Google Drive** | planilha master, lida ao vivo (abas FINAL e TodosJuntos) | o que está na planilha neste momento |

Ao abrir uma folha, a faixa **"Na lista X, estes códigos estão em:"** mostra onde os mesmos códigos caem na
outra lista, e o link leva direto até lá. É assim que se compara uma com a outra.

Link direto para uma folha: `index.html?folha=36006&lista=repo`.

## Painéis
- **Árvore** (esquerda): navega N1 › N2 › folha, com busca. O selo *só aqui* marca folha que não existe na outra
  lista (aparece depois que a outra lista foi carregada uma vez).
- **5 anos** (centro): produtos da folha em cinco colunas. Borda verde e nota curta = célula movida por uma
  decisão registrada (onda, id e motivo; o texto completo fica no tooltip). Borda vermelha = o mesmo
  código original aparece em mais de uma folha, o que é erro.
- **Contexto** (direita): *Vizinhos* mostra as outras folhas do mesmo N2; *Busca global* varre os 48 mil produtos.
- **⚑ Apontar problema**: manda para a planilha de sugestões (Google Forms). A skill importa esses apontamentos
  como pendências com `hp_form.py`.

## Regenerar os dados da lista do repositório

```bash
python .claude/skills/harmoniza-pof/scripts/hp_site.py     # escreve data/estado/{folhas,produtos,meta}
```

Rodar ao fim de cada onda, antes do commit (está no passo 5 da SKILL.md). Servir localmente com
`python -m http.server` na raiz do repositório; abrir por `file://` não funciona.

## Histórico
- `inicial/` é a página do fluxo antigo (Google Form + `aplicar_sugestoes.Rmd`), mantida para consulta.
- `data/folhas.csv` e `data/produtos.csv` na raiz de `data/` são da tentativa de junho de 2026 e não são mais
  usados pelo site.
