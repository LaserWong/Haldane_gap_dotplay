"""Exact full-Hilbert inertia checks of quadratic reference counts on 2x2."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,math
import numpy as np
from quadratic_bins import certify
from translated_band import Model
from low_band_certificate import exact_inertia
HERE=Path(__file__).resolve().parent


def verify(g):
    nx=ny=2;model=Model(nx,ny,g);groups=defaultdict(list)
    for state in range(4**model.N):
        mz=sum({0:0,1:-1,2:0,3:1}[(state>>(2*i))&3] for i in range(model.N))
        groups[model.q(state)%2,mz].append(state)
    blocks=[]
    for label,states in groups.items():
        index={s:i for i,s in enumerate(states)};h=np.zeros((len(states),len(states)),dtype=object)
        metric=np.diag([model.weight(s) for s in states]).astype(object)
        for j,state in enumerate(states):
            for out,c in model.apply({state:1}).items():
                assert out in index
                h[index[out],j]+=model.weight(out)*c
        assert np.array_equal(h,h.T)
        blocks.append((label,h,metric))
    record=certify(nx,ny,g);checks=[]
    for row in record['bins'][:4]:
        threshold=F(row['lower']);neg=sum(exact_inertia(h-model.den*threshold*metric)[0] for _,h,metric in blocks)
        allowed=row['first_ordered_index']-1
        assert neg<=allowed
        checks.append(dict(q=row['q'],threshold=str(threshold),full_physical_negative_count=neg,
                           reference_allowed_negative_count=allowed))
    return dict(g=str(g),shape=[nx,ny],full_dimension=4**model.N,
       symmetry_block_dimensions=[dict(parity=p,Sz=z,dimension=len(h)) for (p,z),h,_ in blocks],checks=checks)


if __name__=='__main__':
    out=dict(status='passed_internal_full_Hilbert_exact_inertia_tests_pending_independent_review',
             cases=[verify(F(3,100)),verify(F(3,50))])
    (HERE/'physical_count_validation.json').write_text(json.dumps(out,indent=2))
    print('PASSED',[(x['g'],[(r['q'],r['full_physical_negative_count'],r['reference_allowed_negative_count']) for r in x['checks']]) for x in out['cases']])
