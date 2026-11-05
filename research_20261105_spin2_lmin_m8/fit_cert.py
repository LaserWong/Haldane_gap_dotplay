"""CERT refit: targets = exact rational midpoints of the rigorous boxes cert/enclosures.json.\nAdapted even NNLS / integer-cluster Newton from moment_nogo.
No real-valued multiplicity relaxation survives in the exported candidate.
"""
import json,sys,platform
from pathlib import Path
import numpy as np, scipy, mpmath as mp
from scipy.optimize import nnls
mp.mp.dps=180
from fractions import Fraction as Fr
enc=json.loads(Path('cert/enclosures.json').read_text())
def mid(key): lo,hi=Fr(enc[key]['lo']),Fr(enc[key]['hi']); m=(lo+hi)/2; return m
TGT={f'{s}{k}':mid(f'{s}{k}') for s in 'ZP' for k in range(4,9)}
Z={k:mp.mpf(TGT[f'Z{k}'].numerator)/TGT[f'Z{k}'].denominator for k in range(4,9)}
P={k:mp.mpf(TGT[f'P{k}'].numerator)/TGT[f'P{k}'].denominator for k in range(4,9)}
ks=list(range(4,9)); even=[4,6,8]
big={'J':[(mp.mpf('1.00001'),1),(mp.mpf('.999'),1)],'N':[]}
sectors={}
for sec in ['J','N']:
    T={k:(Z[k]+3*P[k])/4 if sec=='J' else (Z[k]-P[k])/4 for k in ks}
    r={k:T[k]-sum(w*x**k for x,w in big[sec]) for k in ks}
    # Positive +/- pairs: variable is pair weight; normalize all columns.
    grid=np.unique(np.r_[np.geomspace(1e-10,.94,1601),np.linspace(.001,.94,401)])
    A=np.array([[float(2*mp.mpf(str(x))**k/r[k]) for x in grid] for k in even])
    scales=np.linalg.norm(A,axis=0); B=A/scales
    u,res=nnls(B,np.ones(3),maxiter=10000)
    active=[(grid[i],u[i]/scales[i]) for i in range(len(grid)) if u[i]>1e-12]
    print(sec,'even NNLS',res,'active',active,flush=True)
    if len(active)!=3 or res>1e-8: raise RuntimeError('Even proposal outside declared class')
    nodes=[]; weights=[]
    for x,w in active:
        assert w>1e4
        for sign in [1,-1]: nodes.append(mp.mpf(str(sign*x)));weights.append(int(round(w)))
    row_scales={k:max(abs(r[k]),mp.sqrt(abs(r[k-1]*r[k+1]))) if k%2 else abs(r[k]) for k in ks}
    fixed=nodes[-1]
    def eq(*free):
        pos=list(free)+[fixed]
        return [(sum(w*x**k for x,w in zip(pos,weights))-r[k])/row_scales[k] for k in ks]
    sol=mp.findroot(eq,nodes[:5],tol=mp.mpf('1e-150'),maxsteps=50,solver='mdnewton')
    pos=list(sol)+[fixed]
    err=max(abs(x) for x in eq(*pos[:5])); assert err<mp.mpf('1e-130')
    atoms=big[sec]+list(zip(pos,weights));sectors[sec]=atoms
    print(sec,'scaled Newton residual',mp.nstr(err,8),'bulk max',mp.nstr(max(map(abs,pos)),8),flush=True)
# Export finite rational decimal positions, integer weights. Input still TESTED.
out={'status':'candidate (verified separately by check_cert.py)','contract':'B-cert-M8','targets':{k:str(v) for k,v in TGT.items()},'dps':mp.mp.dps,'atoms':{sec:[[mp.nstr(x,165),str(w)] for x,w in aa] for sec,aa in sectors.items()},'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mp.__version__}}
Path('candidate_cert.json').write_text(json.dumps(out,indent=2))
print('candidate_cert.json written',flush=True)
