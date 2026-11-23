"""Compara cada célula de ANO_B com as células de ANO_A que têm os mesmos itens (nome exato ou 2 primeiras palavras)."""
import sys, re, unicodedata, pandas as pd
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
REPO, A, B = sys.argv[1:4]
dep = pd.read_csv(REPO + '/harmonizacao/estado/depara.csv', dtype=str, keep_default_na=False)
grp = pd.read_csv(REPO + '/harmonizacao/estado/grupos.csv', dtype=str).fillna(''); nm = dict(zip(grp.Cod_harmo, grp.nome))
def norm(s):
    s = unicodedata.normalize('NFKD', s.upper()); s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r'\((VAREJO|PACOTE|NAO ESPECIFICAD[OA]|QUALQUER MARCA|A GRANEL|KG)\)', ' ', s)
    return re.sub(r'[^A-Z0-9]+', ' ', s).strip()
dep['nd'] = dep.Descri_Item.map(norm); dep['k'] = dep.Ano + ':' + dep.Codigo
GEN = re.compile(r'^(AGREGADO|OUTR[OA]S?|NAO ESPECIFICAD|DESPESAS)')
dep = dep[~dep.nd.str.match(GEN) & (dep.nd != '')]
c = pd.read_csv('celulas_valor.csv', dtype={'c': str, 'grupo': str, 'ano': str})
c = c[c.rec == 'RM']; tot = c.groupby('ano').vw.sum()
pp = {r.ano + ':' + r.c: 100 * r.vw / tot[r.ano] for r in c.itertuples()}
NF = lambda d: d[d.Quadro_H.str.isdigit() & (d.Quadro_H.str.zfill(3) < '063') & (d.Cod_harmo != '16201') & (d.Cod_harmo != '88888')]
da, db = NF(dep[dep.Ano == A]), NF(dep[dep.Ano == B])
da = da.assign(nd=da.Quadro_H.str.zfill(3) + '|' + da.nd); db = db.assign(nd=db.Quadro_H.str.zfill(3) + '|' + db.nd)
ga = da.groupby('nd').Cod_harmo.agg(lambda s: Counter(s).most_common(1)[0][0])
pref = lambda s: s.split('|')[0] + '|' + ' '.join(s.split('|')[1].split()[:2])
gp = da.assign(p=da.nd.map(pref)).groupby('p').Cod_harmo.agg(lambda s: Counter(s).most_common(1)[0][0] if s.nunique() == 1 else None).dropna()
out = []
for k, g in db.groupby('k'):
    gb = g.Cod_harmo.iloc[0]
    v = Counter(ga[n] for n in g.nd if n in ga.index)
    modo = 'nome'
    if not v:
        v = Counter(gp[pref(n)] for n in g.nd if pref(n) in gp.index); modo = 'prefixo'
    if not v: continue
    top, n = v.most_common(1)[0]
    if top != gb and n / sum(v.values()) >= 0.6:
        out.append(dict(k=k, q=g.Quadro_H.iloc[0], grupo=gb, ng=nm.get(gb, '')[:26], sug=top, ns=nm.get(top, '')[:26],
                        modo=modo, n=n, de=sum(v.values()), pp=pp.get(k, 0.0), itens=' / '.join(g.Descri_Item.head(4))[:80]))
o = pd.DataFrame(out).sort_values('pp', ascending=False)
o.to_csv(f'parNF_{A}_{B}.csv', index=False)
print(f'{B} contra {A}: {len(o)} células divergentes, {o.pp.sum():.3f} p.p.')
for r in o.head(int(sys.argv[4]) if len(sys.argv) > 4 else 60).itertuples():
    print(f'{r.k:11} q{r.q:>3} {r.grupo} {r.ng:26} -> {r.sug} {r.ns:26} {r.modo[:4]} {r.n}/{r.de} {r.pp:6.3f} | {r.itens}')
