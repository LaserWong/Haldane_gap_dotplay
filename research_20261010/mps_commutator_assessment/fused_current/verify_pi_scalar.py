#!/usr/bin/env python3
"""Exact pi-improved70/73-state necessary screens, with fixed D26 numerator."""
from pathlib import Path
from fractions import Fraction as F
import json,time,os,resource
P=Path(__file__).resolve().parent;BASE=P.parents[1]/'mps_excited_seed_witnesses'
source=(BASE/'verify_scalar.py').read_text().split('rows=[]\nfor r in')[0];ns={'__file__':str(BASE/'verify_scalar.py')};exec(source,ns)
exp_i,up,recipe=[ns[k] for k in ['exp_i','up','recipe']];t0=time.process_time();Q=1<<64
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
data=json.loads((P/'pi_trace_cases.json').read_text());delta=F(data['delta']);d=F(delta.numerator*Q//delta.denominator,Q);R=F(data['numerator_Rayleigh']);Rlo=F(R.numerator*Q//R.denominator,Q)
hot=up(exp_i(-Rlo)[1]/3**96);cold=exp_i(-160*d)[1];assert max(hot,cold)<F(2,5)
results=[]
for case in data['cases']:
    groups=[]
    for r in case['groups']:
        g=F(r['gap_upper']);gu=F(-(-g.numerator*Q//g.denominator),Q);assert gu>=g>0;groups.append((r['multiplicity'],gu))
    assert 1+sum(m for m,g in groups)==case['retained_denominator_states']
    def box(lo,hi):
        num=exp_i(-2*lo*d)[1];j=up(num/(1+sum(m*exp_i(-hi*g)[0] for m,g in groups))**4);c=up(num/(1+sum(m*exp_i(-2*hi*g)[0] for m,g in groups))**2)
        return {'beta_lower':str(lo),'beta_upper':str(hi),'J_upper':str(j),'C_upper':str(c),'J_upper_display':float(j),'C_upper_display':float(c),'replay':recipe(j,c)}
    boxes=[]
    for i in range(2,320):
        lo,hi=F(i,4),F(i+1,4);entry=box(lo,hi)
        if entry['replay']['outcome']=='excluded':boxes.append(entry)
        else:boxes.extend(box(lo+F(j,64),lo+F(j+1,64)) for j in range(16))
    unresolved=[b for b in boxes if b['replay']['outcome']!='excluded'];merged=[]
    for b in unresolved:
        if merged and merged[-1]['beta_upper']==b['beta_lower']:merged[-1]['beta_upper']=b['beta_upper']
        else:merged.append({'beta_lower':b['beta_lower'],'beta_upper':b['beta_upper']})
    row={'status':'PASS all-beta recipe-specific exclusion' if not unresolved else 'BOUNDED necessary screen; unresolved warm boxes remain','retained_denominator_states':case['retained_denominator_states'],'hot_closed_interval':['0','1/2'],'hot_J_upper':str(hot),'cold_closed_interval':['80','infinity'],'cold_J_upper':str(cold),'delta_lower':str(d),'groups':[{'multiplicity':m,'gap_upper':str(g)} for m,g in groups],'inconclusive_closed_box_unions':merged,'warm_boxes':boxes};results.append(row);print(row['retained_denominator_states'],row['status'],merged,flush=True)
out={'n':24,'fixed_numerator':'one exact archived D26 Rayleigh at48','status':'producer exact scalar results; independent review pending','cases':results,'scope':'Specified thermal-first and fixed-delay joint-aware canonical recipes only. No physical gap, exact low eigenvalue, or universal minimum-seed claim.','cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(P/'pi_scalar_results.json').write_text(json.dumps(out,indent=2)+'\n');print('CPU',out['cpu_seconds'],'peakKiB',out['peak_kb'])
