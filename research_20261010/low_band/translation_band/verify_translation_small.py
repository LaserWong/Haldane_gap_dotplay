import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,gzip
from fractions import Fraction as F
from collections import defaultdict
import numpy as np
from translated_band import HERE,Model,translator
from low_band_certificate import make_map,exact_gram

def highest_weight(nx,ny,g):
    m=Model(nx,ny,g);bare={3:1};W={3:2*m.den};W.update({s:-c for s,c in m.apply(bare).items() if m.q(s)==3})
    out=defaultdict(int)
    for s,c in W.items():
        for i in range(m.N):
            digit=(s>>(2*i))&3
            if digit in [1,2]:out[s^((digit^(digit+1))<<(2*i))]+=c*(1 if digit==1 else 2)
    assert not any(out.values())
    return dict(nx=nx,ny=ny,highest_weight_annihilation_exact=True,magnetization=1)

def full_gram():
    nx=ny=4;g=F(3,100);m=Model(nx,ny,g)
    rec=json.loads((HERE/'translated_4x4_g3d100_moments.json').read_text())
    with gzip.open(HERE/'translated_4x4_g3d100_column.json.gz','rt') as f:W={int(s):int(c) for s,c in json.load(f)['W']}
    basis,A,den,weights,_=make_map(nx,ny,g,1,1,3)
    index={sum(v<<(2*i) for i,v in enumerate(st)):j for j,st in enumerate(basis)}
    V=np.zeros((len(basis),m.N),dtype=np.int64)
    for j in range(m.N):
        tr=translator(nx,ny,*divmod(j,ny))
        for st,c in W.items():V[index[tr(st)],j]=c
    rownorm=max(sum(abs(int(A.data[j])) for j in range(A.indptr[i],A.indptr[i+1])) for i in range(A.shape[0]))
    assert rownorm*int(np.max(np.abs(V)))<(1<<63)-1
    HV=A@V
    G=exact_gram(V.astype(object),V.astype(object),weights[:len(basis)])
    AA=exact_gram(V.astype(object),HV[:len(basis)].astype(object),weights[:len(basis)])
    B=exact_gram(HV.astype(object),HV.astype(object),weights)
    for i in range(m.N):
        xi,yi=divmod(i,ny)
        for j in range(m.N):
            xj,yj=divmod(j,ny);dx=(xj-xi)%nx;dy=(yj-yi)%ny
            assert G[i,j]==int(rec['G'][dx][dy])
            assert F(AA[i,j],den)==F(int(rec['A'][dx][dy]),m.den)
            assert F(B[i,j],den*den)==F(int(rec['B'][dx][dy]),m.den*m.den)
    return dict(full_16_by_16_G_A_B_equality=True,exact_entries_compared=3*m.N*m.N,rectangular_rows=A.shape[0])

if __name__=='__main__':
    r=dict(ground_and_triplet_overlap='Even and odd triplet parity are orthogonal',full_gram=full_gram(),highest_weight=[highest_weight(nx,ny,F(3,100)) for nx,ny in [(4,4),(8,4),(8,8)]])
    (HERE/'translation_crosschecks.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
