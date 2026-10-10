#!/usr/bin/env python3
"""Exact n18/n22 screens from already frozen source and ground integers."""
from pathlib import Path
from fractions import Fraction as F
import json,time,os,resource,hashlib
P=Path(__file__).resolve().parent;BASE=P.parent/'mps_excited_seed_witnesses'
source=(BASE/'verify_scalar.py').read_text().split('rows=[]\nfor r in')[0];ns={'__file__':str(BASE/'verify_scalar.py')};exec(source,ns)
exp_i,up,recipe=[ns[k] for k in ['exp_i','up','recipe']];t0=time.process_time();Q=1<<64
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
paths=['contractions_n24.out','../mps_excited_seed_review/independent_ground.out','longitudinal_extension/contractions_n24.out','verify_scalar.py']
inputs={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in paths}
def read(f):return {k:int(v) for k,v in (line.strip().split('=') for line in (BASE/f).read_text().splitlines())}
a,b,z=[read(f) for f in paths[:3]];results=[]
for n in [18,22]:
    assert a[f'N0_{n}']==b[f'N0_{n}']>0 and a[f'N1_{n}']>0
    assert all(z[f'{key}_{n}']==a[f'{key}_{n}'] for key in ['N0','H0','N1','H1'])
    alpha0=F(a[f'H0_{n}'],a[f'N0_{n}']);alpha1=F(a[f'H1_{n}'],a[f'N1_{n}']);R=F(b[f'H0_{2*n}'],b[f'N0_{2*n}']);delta=R-2*alpha0;gap=alpha1-alpha0
    d=F(delta.numerator*Q//delta.denominator,Q);g=F(-(-gap.numerator*Q//gap.denominator),Q);Rlo=F(R.numerator*Q//R.denominator,Q);assert d>0 and g>=gap>0
    hot=up(exp_i(-Rlo)[1]/3**(4*n));cold=10
    while exp_i(-2*cold*d)[1]>=F(2,5):cold*=2
    cold_bound=exp_i(-2*cold*d)[1];assert max(hot,cold_bound)<F(2,5)
    for m in [2,3]:
        def box(lo,hi):
            num=exp_i(-2*lo*d)[1];j=up(num/(1+m*exp_i(-hi*g)[0])**4);c=up(num/(1+m*exp_i(-2*hi*g)[0])**2)
            return {'beta_lower':str(lo),'beta_upper':str(hi),'J_upper':str(j),'C_upper':str(c),'replay':recipe(j,c)}
        boxes=[]
        for i in range(2,4*cold):
            lo,hi=F(i,4),F(i+1,4);entry=box(lo,hi)
            if entry['replay']['outcome']=='excluded':boxes.append(entry)
            else:boxes.extend(box(lo+F(j,64),lo+F(j+1,64)) for j in range(16))
        unresolved=[x for x in boxes if x['replay']['outcome']!='excluded'];merged=[]
        for entry in unresolved:
            if merged and merged[-1]['beta_upper']==entry['beta_lower']:merged[-1]['beta_upper']=entry['beta_upper']
            else:merged.append({'beta_lower':entry['beta_lower'],'beta_upper':entry['beta_upper']})
        row={'n':n,'numerator_length':2*n,'retained_denominator_states':m+1,'retained_numerator_states':1,'single_state_MPS_bond_upper':52,'linear_search_dimension':0,'status':'PASS all-beta recipe-specific exclusion' if not unresolved else 'BOUNDED necessary screen only','alpha0':str(alpha0),'alpha1':str(alpha1),'R_2n':str(R),'delta':str(delta),'trial_energy_difference':str(gap),'delta_lower':str(d),'gap_upper':str(g),'hot_closed_interval':['0','1/2'],'hot_J_upper':str(hot),'cold_closed_interval':[str(cold),'infinity'],'cold_J_upper':str(cold_bound),'inconclusive_closed_box_unions':merged,'warm_boxes':boxes}
        results.append(row);print(n,m+1,row['status'],merged,flush=True)
out={'status':'producer exact results; independent review pending','input_sha256':inputs,'scope':'Separate even sizes n18 and22; no seed-size monotonicity. Fixed archived D26 single-Rayleigh numerator at2n, specified thermal-first and delayed joint-aware canonical recipes.','rows':results,'cpu_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');print('CPU',out['cpu_seconds'],'peakKiB',out['peak_KiB'])
