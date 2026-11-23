import sys, numpy as np, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
REPO = sys.argv[1]
c = pd.read_csv('celulas_valor.csv', dtype={'c': str, 'grupo': str, 'ano': str})
grp = pd.read_csv(REPO + '/harmonizacao/estado/grupos.csv', dtype=str).fillna('')
grp = grp[grp.status == 'ativo']
grp['n1n'] = grp.nivel1.str.extract(r'^(\d+)')[0].astype(float)
CONS = set(grp[grp.n1n.between(1, 16) | grp.n1n.between(31, 40)].Cod_harmo)
c = c[c.grupo.isin(CONS)]
G = c.groupby(['rec', 'ano', 'grupo']).vw.sum().reset_index()
G['tot'] = 100 * G.vw / G.groupby(['rec', 'ano']).vw.transform('sum')
v = pd.read_csv(REPO + '/data/valores/valores.csv', sep=';', dtype={'cod': str, 'ano': str}, encoding='utf-8-sig')
v['rec'] = v.recorte.map({'Brasil': 'BR', 'Regiões metropolitanas': 'RM'})
m = G.merge(v[['rec', 'ano', 'cod', 'tot']], left_on=['rec', 'ano', 'grupo'], right_on=['rec', 'ano', 'cod'], suffixes=('', '_arthur'))
print('conferência com valores.csv: maior |diferença| em pontos de % do consumo:', round((m.tot - m.tot_arthur).abs().max(), 4), 'n=', len(m))
G.to_csv('grupos_serie.csv', index=False)
