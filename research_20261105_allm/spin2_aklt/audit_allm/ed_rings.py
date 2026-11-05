import sys; sys.path.insert(0,'.')
from ff import *
import json,time
P,ms=proj_bond(2,[3,4]); out={}
for L in [int(a) for a in sys.argv[1:]]:
    t0=time.time()
    digs=sector_basis(5,L,ms,0)
    for kind,bonds in (('ring',ring(L)),('open',chain(L))):
        if kind=='open' and L not in (8,): continue
        H=build(P,5,L,bonds,digs=digs)
        g,k0,w=gapnz(H,k=6)
        out[f'{kind}{L}']=dict(dim=len(digs),gap=float(g),kerSz0=k0,low=[float(x) for x in w[:6]])
        print(kind,L,len(digs),'gap %.8f'%g,'ker(Sz=0)',k0,'%.0fs'%(time.time()-t0),flush=True)
json.dump(out,open('ed_rings_%s.json'%'_'.join(sys.argv[1:]),'w'),indent=1)
