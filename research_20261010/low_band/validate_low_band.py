"""Small independent physical-basis benchmark and randomized theorem stress test.
Floating tests are diagnostics, distinct from the exact accepted certificate.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math
from fractions import Fraction as F
import numpy as np
from scipy.linalg import null_space
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from low_band_certificate import OUT,traces

def physical_hamiltonian(nx,ny,g):
    N=nx*ny;D=1<<(2*N);H=np.zeros((D,D))
    site=lambda x,y,a:2*((x%nx)*ny+y%ny)+a
    bonds=[(2*i,2*i+1,1.) for i in range(N)]
    for x in range(nx):
        for y in range(ny):
            for a in range(2):
                bonds.extend([(site(x,y,a),site(x+1,y,a),g),(site(x,y,a),site(x,y+1,a),g)])
    for state in range(D):
        for i,j,c in bonds:
            vi=(state>>i)&1;vj=(state>>j)&1
            H[state,state]+=c*(vi-.5)*(vj-.5)
            if vi!=vj:H[state^((1<<i)|(1<<j)),state]+=c*.5
    return H+3*N/4*np.eye(D)

def check_small():
    rec=json.loads((OUT/'bilayer_2x2_g3d100_low_band.json').read_text())
    H=physical_hamiltonian(2,2,.03);ev=np.linalg.eigvalsh(H);k=rec['retained_full_band_dimension']
    lo=[];hi=[]
    for block in rec['blocks']:
        for l,h in zip(block['eigen_lower'],block['eigen_upper']):
            lo.extend([float(F(l))]*block['multiplicity']);hi.extend([float(F(h))]*block['multiplicity'])
    lo=np.sort(lo);hi=np.sort(hi)
    assert np.all(lo<=ev[:k]+1e-12) and np.all(ev[:k]<=hi+1e-12)
    assert ev[k]>=float(F(rec['global_lambda_kplus1_lower']))-1e-12
    results=[]
    shift=float(F(rec['blocks'][0]['eigen_upper'][0]))
    for beta in [1,4,8,12,20]:
        q=np.exp(-beta*(ev-shift)).sum();ql,qh,tail=traces(rec,beta)
        assert float(ql)<=q+1e-10 and q<=float(qh)+1e-10
        results.append(dict(beta=beta,actual=q,lower=float(ql),upper=float(qh),tail=float(tail)))
    return dict(kind='independent full physical-basis floating benchmark',dimension=len(H),band_size=k,
       eigenvalues_low=ev[:k].tolist(),max_band_width=float(np.max(hi-lo)),trace_checks=results)

def randomized():
    rng=np.random.default_rng(1811);nchecked=0;worst=1e9
    for D in [4,9,15]:
        for k in range(1,D):
            for scale in [.001,.03,.1,.4]:
                eig=np.sort(rng.uniform(-1,4,D));eig[k:]+=2
                H=np.diag(eig)
                W=np.vstack([np.eye(k),scale*rng.normal(size=(D-k,k))]);Q=np.linalg.qr(W)[0]
                T=Q.T@H@Q;R=H@Q-Q@T;r=np.linalg.eigvalsh(T)[-1];a=eig[k]
                if r>=a:continue
                eps=np.linalg.norm(R,2)**2;b=a-(a-eig[0])*min(1,eps/(a-r)**2)
                Qc=null_space(Q.T);actual=np.linalg.eigvalsh(Qc.T@H@Qc)[0]
                assert actual>=b-1e-10
                worst=min(worst,actual-b);nchecked+=1
    return dict(kind='floating stress test, not proof',tests=nchecked,minimum_complement_slack=worst)

if __name__=='__main__':
    out=dict(small_patch=check_small(),randomized_lemma=randomized())
    (OUT/'validation_diagnostics.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
