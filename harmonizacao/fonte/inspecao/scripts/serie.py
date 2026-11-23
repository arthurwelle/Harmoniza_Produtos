"""uso: serie.py REPO 'regex de item' [...]  |  serie.py REPO @GRUPO ANO  (células do grupo na edição)"""
import sys, re, unicodedata, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
REPO = sys.argv[1]
dep = pd.read_csv(REPO + '/harmonizacao/estado/depara.csv', dtype=str, keep_default_na=False)
grp = pd.read_csv(REPO + '/harmonizacao/estado/grupos.csv', dtype=str).fillna('')
nm = dict(zip(grp.Cod_harmo, grp.nome))
c = pd.read_csv('celulas_valor.csv', dtype={'c': str, 'grupo': str, 'ano': str})
grp['n1n'] = grp.nivel1.str.extract(r'^(\d+)')[0].astype(float)
CONS = set(grp[(grp.status == 'ativo') & (grp.n1n.between(1, 16) | grp.n1n.between(31, 40))].Cod_harmo)
pp = {}
for rec in ('RM', 'BR'):
    x = c[c.rec == rec]; t = x[x.grupo.isin(CONS)].groupby('ano').vw.sum()
    for r in x.itertuples(): pp[(rec, r.ano + ':' + r.c)] = 100 * r.vw / t[r.ano]
dep['k'] = dep.Ano + ':' + dep.Codigo
def norm(s):
    s = unicodedata.normalize('NFKD', s.upper()); return ''.join(ch for ch in s if not unicodedata.combining(ch))
dep['nd'] = dep.Descri_Item.map(norm)
cel = dep.groupby('k').agg(ano=('Ano', 'first'), q=('Quadro_H', 'first'), g=('Cod_harmo', 'first'),
                           itens=('Descri_Item', lambda s: ' / '.join(s.drop_duplicates().head(5))))
def show(ks, titulo):
    print('##', titulo)
    for k in sorted(ks, key=lambda k: (k[:4], int(k[5:]) if k[5:].isdigit() else 0)):
        r = cel.loc[k]
        print(f"  {k:11} q{r.q:>3} {r.g} {nm.get(r.g,'')[:26]:26} RM {pp.get(('RM',k),0):7.3f} BR {pp.get(('BR',k),0) if r.ano>='2002' else float('nan'):7.3f} | {r.itens[:95]}")
args = sys.argv[2:]
i = 0
while i < len(args):
    a = args[i]
    if a.startswith('@'):
        g, ano = a[1:], args[i + 1]; i += 2
        ks = [k for k in cel.index[(cel.g == g) & (cel.ano == ano)]]
        ks = sorted(ks, key=lambda k: -pp.get(('RM', k), 0))[:15]
        print('##', g, nm.get(g, ''), ano, '(top 15 por valor RM)')
        for k in ks:
            r = cel.loc[k]; print(f"  {k:11} q{r.q:>3} RM {pp.get(('RM',k),0):7.3f} BR {pp.get(('BR',k),0):7.3f} | {r.itens[:110]}")
    else:
        i += 1
        ks = set(dep.loc[dep.nd.str.contains(a, regex=True), 'k'])
        show(ks, a)
