"""Float cross-check (NONRIGOROUS, sanity only): on periodic rings L=4..10 (even, L>=k+1) compute
min_x (Hv)_x/v_x / L by full enumeration of 3^L configs for the certified Jastrow-k vector,
and compare with mu_cert (must be <=) and exact E0(L)/L from Lanczos ED (must be >=)."""
import json,itertools,numpy as np
SP=np.array([1,0,-1])
ed=json.load(open('../ed_small_S1.json')); E0={4:-6.0}; E0.update({int(L):v['E0'] for L,v in ed.items()})
res={}
for k in range(1,7):
    try: r=json.load(open(f'jastrow_k{k}.json')); c=json.load(open(f'cert_k{k}.json'))
    except FileNotFoundError: continue
    th=np.array(r['theta']); mu=c['mu_cert_float']
    for L in range(4,11,2):
        if L<k+1: continue
        X=np.array(list(itertools.product(range(3),repeat=L)))
        def logv(X):
            s=np.zeros(len(X))
            for i in range(L):
                idx=np.zeros(len(X),int)
                for j in range(k): idx=3*idx+X[:,(i+j)%L]
                s+=th[idx]
            return s
        lv=logv(X); loc=np.zeros(len(X))
        for i in range(L):
            a,b=X[:,i],X[:,(i+1)%L]; loc+=SP[a]*SP[b]
            for d in (1,-1):
                na,nb=SP[a]+d,SP[b]-d; ok=(abs(na)<=1)&(abs(nb)<=1)
                Y=X[ok].copy(); Y[:,i]=1-na[ok]; Y[:,(i+1)%L]=1-nb[ok]   # index = 1-m
                loc[ok]-=np.exp(logv(Y)-lv[ok])
        m=loc.min()/L
        ok_=bool(mu<=m+1e-12 and m<=E0[L]/L+1e-12)
        res[f'k{k}_L{L}']=dict(mu_cert=mu,ring_min_per_site=m,E0_per_site=E0[L]/L,chain_ok=ok_)
        print(k,L,mu,m,E0[L]/L,ok_,flush=True)
json.dump(res,open('bruteforce.json','w'),indent=1)
