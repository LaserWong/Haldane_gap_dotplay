"""Independent full spin-basis checks of sparse-support large-D certificates."""
import json,math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import scipy.linalg as la
from models import *
BASE=Path(__file__).resolve().parent;OUT=BASE/'results'

def check(path):
    rec=json.loads(path.read_text());N=rec['N'];assert N<=8
    art=np.load(OUT/rec['trial_artifact']);states=art['basis'];vec=art['vector']
    # Trial tuple coordinates were m=-1,0,+1, while physical digits are m+1.
    ids,digits=basis(1.,N,0);where={int(x):i for i,x in enumerate(ids)};pw=3**np.arange(N,dtype=np.int64)
    v=[0]*len(ids)
    for st,amp in zip(states,vec):v[where[int((st.astype(np.int64)+1)@pw)]]=int(amp)
    model=large_d_square(rec['nx'],rec['ny'],float(F(rec['g'])),float(F(rec['g'])))
    H=hamiltonian(model,0);den=F(rec['g']).denominator;A=H.copy();raw=A.data*den;rounded=np.rint(raw)
    assert np.max(abs(raw-rounded),initial=0)<1e-9;A.data=rounded.astype(np.int64)
    Hv=[sum(int(A.data[j])*v[int(A.indices[j])] for j in range(A.indptr[i],A.indptr[i+1])) for i in range(A.shape[0])]
    norm=sum(x*x for x in v);rho=F(sum(x*y for x,y in zip(v,Hv)),den*norm);r2=F(sum(y*y for y in Hv),den*den*norm)-rho*rho
    assert rho==F(rec['exact_rayleigh']);assert r2==F(rec['exact_residual_squared'])
    eig,_=full_spectrum(model)
    assert float(F(rec['ground_lower']))<=eig[0]+2e-13 and eig[0]-2e-13<=float(F(rec['ground_upper']))
    # Direct 9x9 PSD check supplements the exact analytic conditions in the builder.
    g=F(rec['g']);cp=rec['comparison'];a,b,c,B=[F(cp[k]) for k in ['a','b','c','B']]
    pair=Model(1.,2,(Edge(0,1,float(g),'pair'),),'pair',{},float(a))
    e=la.eigvalsh(independent_dense(pair))+float(b)
    assert e[0]>-1e-13
    return dict(artifact=path.name,physical_sites=N,full_dimension=3**N,full_Sz0_dimension=len(ids),exact_rayleigh_match=True,exact_full_residual_squared_match=True,ground_full_ED=float(eig[0]),certificate_lower=float(F(rec['ground_lower'])),certificate_upper=float(F(rec['ground_upper'])),bond_PSD_min_float=float(e[0]),ground_degeneracy=int(sum(abs(eig-eig[0])<1e-10)))

if __name__=='__main__':
    rows=[]
    for p in sorted(OUT.glob('largeD_*x*_ground.json')):
        rec=json.loads(p.read_text())
        if rec['N']<=8:rows.append(check(p));print(rows[-1],flush=True)
    (OUT/'largeD_independent_checks.json').write_text(json.dumps(rows,indent=2))
