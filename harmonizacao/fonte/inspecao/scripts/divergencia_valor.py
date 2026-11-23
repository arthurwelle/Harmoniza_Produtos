import sys, re, unicodedata, numpy as np, pandas as pd
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
REPO = sys.argv[1]
dep = pd.read_csv(REPO + '/harmonizacao/estado/depara.csv', dtype=str, keep_default_na=False)
grp = pd.read_csv(REPO + '/harmonizacao/estado/grupos.csv', dtype=str).fillna('')
nm = dict(zip(grp.Cod_harmo, grp.nome))
grp['n1n'] = grp.nivel1.str.extract(r'^(\d+)')[0].astype(float)
CONS = set(grp[(grp.status == 'ativo') & (grp.n1n.between(1, 16) | grp.n1n.between(31, 40))].Cod_harmo)
def norm(s):
    s = unicodedata.normalize('NFKD', s.upper()); s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r'[^A-Z0-9]+', ' ', s).strip()
GEN = {'AGREGADO', 'OUTROS', 'OUTRAS', 'OUTRO', 'OUTRA', 'NAO ESPECIFICADO', 'DIVERSOS', 'DESPESAS DIVERSAS', ''}
dep['nd'] = dep.Descri_Item.map(norm)
dep['k'] = dep.Ano + ':' + dep.Codigo
dep = dep[~dep.nd.isin(GEN)]
c = pd.read_csv('celulas_valor.csv', dtype={'c': str, 'grupo': str, 'ano': str})
c = c[c.rec == 'RM'].copy()
tot = c[c.grupo.isin(CONS)].groupby('ano').vw.sum()
c['pp'] = 100 * c.vw / c.ano.map(tot)
c['k'] = c.ano + ':' + c.c
pp = dict(zip(c.k, c.pp))
# grupo de cada nome por edição (célula -> grupo)
cel_g = dep.groupby('k').Cod_harmo.first()
_t = dep.groupby(['nd', 'Ano']).Cod_harmo.agg(lambda s: Counter(s).most_common(1)[0][0])
nome_ano_g = defaultdict(dict)
for (n_, a_), h_ in _t.items(): nome_ano_g[n_][a_] = h_
nomes_por_cel = dep.groupby('k').nd.agg(lambda s: list(dict.fromkeys(s)))
quadro = dep.groupby('k').Quadro_H.first()
out = []
for k, nomes in nomes_por_cel.items():
    ano = k[:4]; g = cel_g[k]
    votos = Counter(); por_ed = defaultdict(set)
    for n in nomes:
        for a, h in nome_ano_g.get(n, {}).items():
            if a != ano: por_ed[a].add(h)
    for a, hs in por_ed.items():
        for h in hs: votos[h] += 1 / len(hs)
    if not votos: continue
    top, n = votos.most_common(1)[0]
    eds = len(por_ed)
    if top != g and eds >= 2 and n >= 2 and n / sum(votos.values()) >= 0.6:
        out.append(dict(k=k, ano=ano, quadro=quadro[k], grupo=g, nome_grupo=nm.get(g, ''), sugere=top,
                        nome_sugere=nm.get(top, ''), apoio=round(n, 1), edicoes=eds, pp=pp.get(k, 0.0),
                        itens=' / '.join(nomes[:5]), cons_grupo=g in CONS, cons_sugere=top in CONS))
o = pd.DataFrame(out)
o['fora'] = (o.grupo == '16201') | (o.sugere == '16201')
o = o.sort_values('pp', ascending=False)
o.to_csv('divergencias_valor.csv', index=False)
x = o[~o.fora]
pd.set_option('display.width', 260); pd.set_option('display.max_rows', 200); pd.set_option('display.max_colwidth', 45)
print('divergentes:', len(o), '| sem comida fora:', len(x), '| pp total (RM):', round(x.pp.sum(), 3))
print(x[['k', 'quadro', 'grupo', 'nome_grupo', 'sugere', 'nome_sugere', 'apoio', 'pp', 'itens']].round(4).head(70).to_string(index=False))
