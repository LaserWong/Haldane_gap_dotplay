# Shows the operator form "B >= (avg c) eps_n on ker(B)^perp" (CERT_ALLM step 1 as written) is false in general.
import sys; sys.path.insert(0,'.')
from ff import *
P,ms=proj_bond(1,[2])
for n,c in [(6,[0.05,1,1,1,0.05]),(6,[0.3,1,1,1,0.3]),(8,[465,771,944,1000,944,771,465]),(8,[0.1,1,1,1,1,1,0.1])]:
    c=np.array(c,float)
    H=build(P,3,n,chain(n)).toarray(); w=np.linalg.eigvalsh(H); eps=w[w>1e-9].min()
    B=build(P,3,n,chain(n),weights=c).toarray(); wb=np.linalg.eigvalsh(B); lb=wb[wb>1e-9*c.max()].min()
    print('AKLT S=1 n=%d c=%s: lambda+_min(B)=%.5f vs avg(c)*eps_n=%.5f -> %s'%(n,list(c),lb,c.mean()*eps,'HOLDS' if lb>=c.mean()*eps-1e-9 else 'VIOLATED'))
