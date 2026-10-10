"""Independent diagnostics around J=.3 exact-dimer reference.
ROOT convention: same-layer straight J+epsilon, opposite-layer cross J.
Equivalently (J+epsilon/2) T_i.T_j + (epsilon/2) D_i.D_j.
This is NOT the different symmetric convention J±epsilon.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time
import numpy as np
from scipy.sparse.linalg import eigsh
from models import *
OUT=Path(__file__).resolve().parent/'results'

def model(nx,ny,J,eps):
    N=nx*ny;base=square(.5,nx,ny,periodic_x=True,periodic_y=True)
    edges=[Edge(2*i,2*i+1,1.,'rung') for i in range(N)]
    for e in base.edges:
        for a in [0,1]:
            for b in [0,1]:edges.append(Edge(2*e.i+a,2*e.j+b,float(J+(eps if a==b else 0)),'straight' if a==b else 'cross'))
    return Model(.5,2*N,tuple(edges),f'frustrated_{nx}x{ny}_J{J}_eps{eps}',dict(family='frustrated_robustness',nx=nx,ny=ny,J=str(J),epsilon=str(eps),straight=str(J+eps),cross=str(J),periodic_both=True,convention='straight J+epsilon; cross J'))

def vacuum_in_sector(N):
    ids,dig=basis(.5,2*N,0);v=np.zeros(len(ids));mask=np.all(dig[:,::2]+dig[:,1::2]==1,axis=1)
    v[mask]=np.prod(2*dig[mask,::2]-1,axis=1)/(2**(N/2))
    assert abs(v@v-1)<1e-12
    return v

def run():
    rows=[]
    for nx,ny in [(2,2),(4,2)]:
      N=nx*ny
      for eps in [F(1,200),F(1,100),F(1,50)]:
        J=F(3,10);m=model(nx,ny,J,eps);t=time.monotonic();H=hamiltonian(m,0)
        rng=np.random.default_rng(876);e,v=eigsh(H,k=12,which='SA',tol=2e-13,ncv=min(H.shape[0],80),v0=rng.normal(size=H.shape[0]));order=np.argsort(e);e=e[order];v=v[:,order]
        shifted=e+3*N/4;res=np.linalg.norm(H@v-v*e[None,:],axis=0);vac=vacuum_in_sector(N)
        vv=H@vac+3*N/4*vac;rho=vac@vv;res0=vv@vv-rho*rho
        pred=(12 if N==4 else 18)*float(eps)**2
        assert abs(rho)<1e-12 and abs(res0-pred)<1e-12
        overlap=float((vac@v[:,0])**2)
        spin1=low_sector(m,2,k=4);eM1=np.array(spin1['eigenvalues'])+3*N/4
        rec=dict(model=m.metadata(),physical_spins=2*N,full_dimension=m.dimension,Sz0_dimension=H.shape[0],ground_shifted=float(shifted[0]),gap=float(min(shifted[1],eM1[0])-shifted[0]),ground_singlet_product_overlap_squared=overlap,exact_product_rayleigh_shifted='0',product_residual_squared_formula=f'{12 if N==4 else 18} * epsilon^2',product_residual_squared=float(res0),max_low_eigenpair_residual=float(max(res)),energies_M0_shifted=shifted.tolist(),energies_M1_shifted=eM1.tolist(),seconds=time.monotonic()-t,certified=False)
        if N==4:
            ef,_=full_spectrum(m);np.testing.assert_allclose(e,np.sort(la.eigvalsh(H.toarray()))[:12],atol=2e-12)
            rec['full_spectrum_ground_degeneracy']=int(sum(abs(ef-ef[0])<1e-10))
        rows.append(rec);print({k:v for k,v in rec.items() if k not in ['model','energies_M0_shifted','energies_M1_shifted']},flush=True)
        (OUT/'frustrated_robustness_diagnostics.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':run()
