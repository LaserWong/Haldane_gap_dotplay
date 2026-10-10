#!/usr/bin/env python3
"""Different exact exponential grid and scalar recurrence; fixed canonical recipes only."""
from pathlib import Path
base=Path(__file__).resolve().parent
exec((base.parent/'mps_excited_seed_review/independent_scalar.py').read_text().split("p=values('independent_contractions.out')")[0])
P=base;resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2))
a=json.loads((P/'independent_assembly.json').read_text());producer=json.loads((P/'inputs/scalar/pi_scalar_results.json').read_text());delta=F(a['delta']);R=F(a['numerator_Rayleigh']);assert delta>0 and R<0
rows=[]
for own,saved in zip(a['cases'],producer['cases']):
 assert own['retained_states']==saved['retained_denominator_states'];groups=[(g['multiplicity'],F(g['gap_upper'])) for g in own['groups']];assert all(g>0 for m,g in groups)
 hot=ceil(exp_interval(-R)[1]/3**96);cold=exp_interval(-160*delta)[1];assert max(hot,cold)<F(2,5) and G(F(2,5))<0
 assert hot<=F(saved['hot_J_upper']) and cold<=F(saved['cold_J_upper'])
 boxes=[];previous=F(1,2)
 for pb in saved['warm_boxes']:
  lo,hi=F(pb['beta_lower']),F(pb['beta_upper']);assert lo==previous and hi-lo==F(1,4);previous=hi
  numerator=exp_interval(-2*lo*delta)[1]
  j=ceil(numerator/(1+sum(m*exp_interval(-hi*g)[0] for m,g in groups))**4)
  c=ceil(numerator/(1+sum(m*exp_interval(-2*hi*g)[0] for m,g in groups))**2)
  assert j<=F(pb['J_upper']) and c<=F(pb['C_upper']);v=test(j,c);assert v['excluded'],(lo,hi,v)
  boxes.append({'lo':str(lo),'hi':str(hi),'J_upper':str(j),'C_upper':str(c),**v})
 assert previous==80 and len(boxes)==318
 rows.append({'retained_states':own['retained_states'],'hot_upper':str(hot),'cold_upper':str(cold),'all_beta_excluded':True,'boxes':boxes,'max_conversion_delays':max(len(b.get('conversions',[])) for b in boxes)})
 print(own['retained_states'],'PASS all beta, 318 closed boxes and both tails',flush=True)
out={'status':'PASS independent scalar arithmetic from independently reviewed physical inputs','scope':'Fixed D26 length48 single-Rayleigh numerator; old whole-cycle time-first delays and accepted joint-aware canonical conversion only. Does not cover new direct finite-window interpolation or imply all-method seed minimum or physical spectral gap.','rows':rows,'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_scalar.json').write_text(json.dumps(out,indent=2)+'\n')
