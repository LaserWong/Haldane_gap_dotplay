#!/usr/bin/env python3
from pathlib import Path
base=Path(__file__).resolve().parent
exec((base.parent/'mps_excited_seed_review/independent_scalar.py').read_text().split("p=values('independent_contractions.out')")[0]);P=base
source=P.parent/'mps_excited_seed_review'
def raw(f):return {k:int(v) for k,v in (s.split('=') for s in f.read_text().splitlines())}
a=raw(source/'independent_contractions.out');z=raw(source/'longitudinal_extension/independent_contractions.out');g=raw(source/'independent_ground.out');pr=json.loads((P/'inputs/results.json').read_text());rows=[]
for saved in pr['rows']:
 n=saved['n'];states=saved['retained_denominator_states'];assert n in [18,22] and states in [3,4]
 assert all(a[f'{k}_{n}']==z[f'{k}_{n}'] for k in ['N0','H0','N1','H1']);assert a[f'N0_{n}']==g[f'N0_{n}']>0 and a[f'N1_{n}']>0
 alpha=F(a[f'H0_{n}'],a[f'N0_{n}']);excited=F(a[f'H1_{n}'],a[f'N1_{n}']);R=F(g[f'H0_{2*n}'],g[f'N0_{2*n}']);delta=R-2*alpha;gap=excited-alpha
 for key,value in [('alpha0',alpha),('alpha1',excited),('R_2n',R),('delta',delta),('trial_energy_difference',gap)]:assert F(saved[key])==value
 assert delta>0 and gap>0 and R<0
 cold=F(saved['cold_closed_interval'][0]);hot=ceil(exp_interval(-R)[1]/3**(4*n));tail=exp_interval(-2*cold*delta)[1];assert max(hot,tail)<F(2,5) and G(F(2,5))<0
 assert hot<=F(saved['hot_J_upper']) and tail<=F(saved['cold_J_upper']);previous=F(1,2);boxes=[]
 for pb in saved['warm_boxes']:
  lo,hi=F(pb['beta_lower']),F(pb['beta_upper']);assert lo==previous and hi>lo;previous=hi
  num=exp_interval(-2*lo*delta)[1];j=ceil(num/(1+(states-1)*exp_interval(-hi*gap)[0])**4);c=ceil(num/(1+(states-1)*exp_interval(-2*hi*gap)[0])**2)
  assert j<=F(pb['J_upper']) and c<=F(pb['C_upper']);v=test(j,c);assert v['excluded']
  boxes.append({'lo':str(lo),'hi':str(hi),'J_upper':str(j),'C_upper':str(c),**v})
 assert previous==cold
 rows.append({'n':n,'retained_states':states,'alpha0':str(alpha),'alpha1':str(excited),'numerator_Rayleigh':str(R),'delta':str(delta),'gap':str(gap),'hot_upper':str(hot),'cold_start':str(cold),'cold_upper':str(tail),'boxes':boxes,'all_beta_excluded':True});print(n,states,'PASS',len(boxes),flush=True)
assert {(r['n'],r['retained_states']) for r in rows}=={(18,3),(18,4),(22,3),(22,4)}
out={'status':'PASS independent physical-input and exact scalar review','scope':'Fixed archived D26 one-Rayleigh numerator at36/44 and specified old whole-cycle time-first delays plus joint-aware canonical recipes only. No seed-size monotonicity, new direct finite-window interpolation, spectral-gap claim, or all-method minimum.','rows':rows,'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(P/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
