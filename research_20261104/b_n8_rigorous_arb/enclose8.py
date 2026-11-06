import numpy as np, json, time
from flint import arb, acb
from common import certify, arbs
t0=time.time()
L=8;N=3**L;p3=3**np.arange(L); s=np.arange(N); d=(s[:,None]//p3)%3; m=1-d
H=np.zeros((N,N)); H[s,s]=(m*np.roll(m,-1,axis=1)).sum(1)
for i in range(L):
    j=(i+1)%L
    for di,dj in [(-1,1),(1,-1)]:
        ok=(d[:,i]+di>=0)&(d[:,i]+di<=2)&(d[:,j]+dj>=0)&(d[:,j]+dj<=2); a=s[ok]
        H[a+di*p3[i]+dj*p3[j],a]+=1.0
assert (H==H.T).all() and (H==np.rint(H)).all()
ent={(int(i),int(j)):acb(int(H[i,j])) for i,j in zip(*np.nonzero(H))}   # exact integers
lt,eta,delta=certify(H,ent,arb(16))
json.dump(dict(lam_t=lt,eta=arbs(eta),delta=arbs(delta),mult=1,trace_exact=int(np.rint(np.trace(H))),frob2_exact=int((H*H).sum())),open('enclosures8.json','w'))
print('L8 eta',eta,'delta',delta,'time',time.time()-t0)
