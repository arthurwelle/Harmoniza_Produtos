import sys, numpy as np, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
REPO = sys.argv[1]
v = pd.read_csv(REPO + '/data/valores/valores.csv', sep=';', dtype={'cod': str, 'ano': str}, encoding='utf-8-sig')
v['rec'] = v.recorte.map({'Brasil': 'BR', 'Regiões metropolitanas': 'RM'})
A = ['1987', '1995', '2002', '2008', '2017']
rows = []
for (cod, rec), g in v.groupby(['cod', 'rec']):
    g = g.set_index('ano')
    anos = [a for a in A if a in g.index]
    s = g.tot.reindex(anos).astype(float); p = g.prev.reindex(anos).astype(float)
    st = g.status.reindex(anos)
    e = 1e-4
    for i, a in enumerate(anos):
        viz = [anos[j] for j in (i - 1, i + 1) if 0 <= j < len(anos)]
        if len(anos) >= 3 and len(viz) == 1:  # ponta: compara com as duas seguintes
            viz = anos[1:3] if i == 0 else anos[-3:-1]
        sv = s[viz]
        if sv.isna().any() or np.isnan(s[a]): continue
        ref = np.exp(np.log(sv + e).mean())
        fat = (s[a] + e) / ref
        coer = (np.log((sv.iloc[0] + e) / (sv.iloc[-1] + e)) if len(sv) == 2 else 0)
        pv = p[viz]; pf = (p[a] + 0.01) / (np.exp(np.log(pv + 0.01).mean()))
        rows.append(dict(cod=cod, rec=rec, ano=a, tot=s[a], ref=ref, fator=fat, dif_pp=s[a] - ref,
                         viz_coerentes=abs(coer) < np.log(2), prev=p[a], prev_ref=np.exp(np.log(pv + 0.01).mean()),
                         fator_prev=pf, status=st[a], nome=g.nome.iloc[0], n1=g.n1.iloc[0]))
r = pd.DataFrame(rows)
r['anom'] = ((r.fator >= 2.5) | (r.fator <= 0.4)) & r.viz_coerentes
r['anom_prev'] = ((r.fator_prev >= 2.5) | (r.fator_prev <= 0.4)) & r.viz_coerentes & (r[['prev', 'prev_ref']].max(axis=1) >= 1)
r['peso'] = r.dif_pp.abs()
f = r[(r.anom | r.anom_prev) & ((r.peso >= 0.02) | r.anom_prev)].sort_values('peso', ascending=False)
f.to_csv('anomalias.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300); pd.set_option('display.max_colwidth', 38)
print(len(f), 'sinais;', f.cod.nunique(), 'grupos')
print(f[['cod', 'nome', 'rec', 'ano', 'tot', 'ref', 'fator', 'prev', 'prev_ref', 'status']].round(3).head(90).to_string(index=False))
