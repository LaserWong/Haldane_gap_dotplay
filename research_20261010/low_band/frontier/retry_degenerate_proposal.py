import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import lobpcg
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import low_band_certificate as L
L.OUT=HERE

def block_solver(H,k,**kwargs):
    # The first k q=1 configurations span the complete unperturbed band.
    X=np.zeros((H.shape[0],k));X[:k]=np.eye(k)
    return lobpcg(H,X,largest=False,tol=2e-12,maxiter=200)

if __name__=='__main__':
    tag='bilayer_4x4_g1d20_p1_M1_q3'
    for suffix in ['_gram.json','_trial.npz']:
        old=HERE/(tag+suffix);new=HERE/(tag+'_rejected_arpack_missing_modes'+suffix)
        if old.exists() and not new.exists():old.rename(new)
    L.eigsh=block_solver
    r=L.certify_block(4,4,F(1,20),1,1,3,16,bits=34)
    assert max(F(x) for x in r['ritz_upper'])<F(11,10)
    print('RETRY PASSED',r['ritz_upper'],flush=True)
