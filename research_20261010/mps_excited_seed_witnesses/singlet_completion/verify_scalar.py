#!/usr/bin/env python3
"""Exact necessary screen using70 fixed compact orthogonal n24 witnesses."""
from pathlib import Path
import json,time,os,resource
from fractions import Fraction as F
P=Path(__file__).resolve().parent
# Reuse the frozen, separately reviewed scalar primitive definitions only.
source=(P.parent/'verify_scalar.py').read_text().split('rows=[]\nfor r in')[0]
ns={'__file__':str(P.parent/'verify_scalar.py')};exec(source,ns)
exp_i,up,G,recipe=[ns[k] for k in ['exp_i','up','G','recipe']]
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));t0=time.process_time()
data=json.loads((P/'fourier_witness_data.json').read_text());Q=1<<64
delta=F(data['delta']);d=F(delta.numerator*Q//delta.denominator,Q);R=F(data['numerator_Rayleigh']);Rlo=F(R.numerator*Q//R.denominator,Q)
groups=[]
for row in data['trace_groups']:
    g=F(row['energy_difference_upper']);gu=F(-(-g.numerator*Q//g.denominator),Q);assert gu>=g>0
    groups.append((row['multiplicity'],gu))
assert sum(m for m,g in groups)==69 and 0<d<=delta
hot=up(exp_i(-Rlo)[1]/3**96);assert hot<F(2,5)
cold=80;cold_bound=exp_i(-2*cold*d)[1];assert cold_bound<F(2,5)
def box(lo,hi):
    num=exp_i(-2*lo*d)[1]
    j=up(num/(1+sum(m*exp_i(-hi*g)[0] for m,g in groups))**4)
    c=up(num/(1+sum(m*exp_i(-2*hi*g)[0] for m,g in groups))**2)
    return {'beta_lower':str(lo),'beta_upper':str(hi),'J_upper':str(j),'C_upper':str(c),'J_upper_display':float(j),'C_upper_display':float(c),'replay':recipe(j,c)}
boxes=[]
for i in range(2,320):
    lo,hi=F(i,4),F(i+1,4);entry=box(lo,hi)
    if entry['replay']['outcome']=='excluded':boxes.append(entry)
    else:
        # Refine only surviving coarse boxes to width1/64, still closed.
        boxes.extend(box(lo+F(j,64),lo+F(j+1,64)) for j in range(16))
unresolved=[b for b in boxes if b['replay']['outcome']!='excluded'];merged=[]
for b in unresolved:
    if merged and merged[-1]['beta_upper']==b['beta_lower']:merged[-1]['beta_upper']=b['beta_upper']
    else:merged.append({'beta_lower':b['beta_lower'],'beta_upper':b['beta_upper']})
out={'status':'PASS all-beta recipe-specific exclusion' if not unresolved else 'BOUNDED necessary screen; unresolved warm boxes remain','n':24,'retained_orthogonal_denominator_states':70,'fixed_numerator':'one archived exact D26 Rayleigh state at48','hot_closed_interval':['0','1/2'],'hot_J_upper':str(hot),'cold_closed_interval':['80','infinity'],'cold_J_upper':str(cold_bound),'delta_lower':str(d),'energy_difference_upper_groups':[{'multiplicity':m,'gap_upper':str(g)} for m,g in groups],'inconclusive_closed_box_unions':merged,'warm_boxes':boxes,'global_J_upper_display':max(float(hot),float(cold_bound),max(b['J_upper_display'] for b in boxes)),'scope':'Only the fixed one-Rayleigh thermal-first recipes and accepted delayed joint-aware conversion; no physical eigenvalue, gap, or universal minimum-seed claim.','cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'scalar_results.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status']);print('inconclusive',merged);print('CPU',out['cpu_seconds'],'peakKiB',out['peak_kb'])
