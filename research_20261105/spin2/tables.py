import sys, json, numpy as np; sys.path.insert(0,'.')
from model import *
from scan import max_slack
res = {}
print('== spin-2 seed windows (model) ==')
for n,b in [(200,60),(256,64),(256,80),(280,60),(300,80),(400,80)]:
    s,t,eta = max_slack(2,n,b)
    _,thn,dn = lnZ_shifted(2,n,b); _,th2,d2 = lnZ_shifted(2,2*n,b); _,th22,_ = lnZ_shifted(2,2*n,2*b)
    ok,g,rows = bootstrap(s*np.exp(-eta/2),t*np.exp(-eta/2),n,b)
    print(f'n={n} beta={b}: S={s:.4f} T={t:.4f} max uniform log-slack={eta:.3f}; with half slack gap>={g:.4f}, windows={len(rows)}')
    print(f'   thermal ln(1+eps): L=n:{thn:.4f}  L=2n,beta:{th2:.4f}  L=2n,2beta:{th22:.5f};  delta_n={dn:.2e} delta_2n={d2:.2e}')
    print(f'   per-site free-energy accuracy for eta_up=eta/4: L=n {eta/4/(b*n):.2e}, L=2n {eta/4/(b*2*n):.2e}')
    res[f'{n}_{b}'] = dict(S=s,T=t,eta=eta,gap_half=g,th_n=thn,th_2n=th2,th_2n_2b=th22)
print('== spin-2 prefix: single-L purity p=Z(2b)/Z(b)^2 (model, even L) ==')
for gam in (0.02, 0.04):
    for L in (16,32,64,128,192,254):
        best=None
        for b in np.arange(5,200,1.0):
            lnp = lnZ(2,L,2*b) - 2*lnZ(2,L,b); pmin = np.exp(b*gam)/(1+np.exp(b*gam))
            sl = lnp - np.log(pmin)
            if best is None or sl > best[1]: best=(b,sl)
        print(f'  gamma={gam} L={L}: best beta={best[0]:.0f}, allowed log-slack={best[1]:.3f}, per-site accuracy ~{best[1]/3/(best[0]*L):.1e}')
        res[f'prefix_{gam}_{L}']=best
json.dump(res,open('tables.json','w'),indent=1)
