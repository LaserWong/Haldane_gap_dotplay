import sys, json, numpy as np; sys.path.insert(0,'.')
from model import *
def max_slack(S, n, beta, gtarget=1e-9, **kw):
    s,t = seeds(S,n,beta,**kw)
    if not bootstrap(s,t,n,beta)[0]: return s,t,None
    lo,hi=0.0,2.0
    for _ in range(40):
        m=(lo+hi)/2; ok,g,_=bootstrap(s*np.exp(-m),t*np.exp(-m),n,beta)
        if ok and g>=gtarget: lo=m
        else: hi=m
    return s,t,lo
out={}
for S,ns,betas in [(1,[16,20,24,30,34,40],[6,8,10,12.25,15,20]),
                   (2,[50,100,150,200,250,300,400,500],[20,30,40,50,60,80,100])]:
    print('spin',S)
    for n in ns:
        best=None
        for b in betas:
            s,t,eta=max_slack(S,n,b)
            if eta is not None and (best is None or eta>best[3]): best=(b,s,t,eta)
            print('  n=%4d beta=%6.2f S=%.4f T=%.4f max_slack=%s'%(n,b,s,t,'%.4f'%eta if eta is not None else 'FAIL'))
        out['S%d_n%d'%(S,n)]=best
json.dump(out,open('scan.json','w'),indent=1)
