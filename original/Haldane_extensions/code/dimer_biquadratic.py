"""Independent ED check for a higher-spin SPT with weak positive biquadratic bonds."""
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy.linalg as la
from threadpoolctl import threadpool_limits
from numerics import local,sectors,block
OUT=Path(__file__).resolve().parents[1]/'results'
s=1.5
g=F(1,450)
x=local(s)
xx=x@x
row=[]
with threadpool_limits(limits=1):
 for L in [4,6]:
    out=[]
    strong=np.array([j%2 for j in range(L)])
    weak=1-strong
    for M,ids,dig,pw in sectors(s,L):
        H=block(s,L,ids,dig,pw,x,strong)+float(g)*block(s,L,ids,dig,pw,xx,weak)
        e=la.eigvalsh(H.toarray(),check_finite=False)
        out.extend([e]*(1 if M==0 else 2))
    es=np.sort(np.concatenate(out))
    np.savez_compressed(OUT/f'spec_biquad_dimer_s1.5_L{L}.npz',energies=es)
    r=dict(s=s,L=L,weak_biquadratic=str(g),E0=float(es[0]),gap=float(es[1]-es[0]),dimension=len(es))
    row.append(r)
    print(r,flush=True)
# Local Casimir values make the spectral-width calculation exact.
S=F(3,2)
vals=[(F(J*(J+1))-2*S*(S+1))/2 for J in range(4)]
width=max(v*v*g for v in vals)-min(v*v*g for v in vals)
assert width==F(3,100)
(OUT/'dimer_biquadratic_diagnostics.json').write_text(json.dumps(dict(rows=row,local_width=str(width),status='width exact, long-chain theorem analytic, listed finite gaps floating'),indent=2))
