#!/usr/bin/env python3
"""Independent necessary screen on every producer closed interval."""
from pathlib import Path
from fractions import Fraction as F
import json,time,sys,resource
P=Path(__file__).resolve().parent;mode=int(sys.argv[1]) if len(sys.argv)>1 else 48;assert mode in [48,70]
core=P.parent/'independent_scalar.py';ns={'__file__':str(core)};exec(core.read_text().split("p=values('independent_contractions.out')")[0],ns)
exp,up,G,test=[ns[k] for k in ['exp_interval','ceil','G','test']];start=time.process_time()
data=json.loads((P/'independent_fourier.json').read_text());producer=json.loads((P/('inputs/scalar_results.json' if mode==48 else 'inputs70/scalar_results.json')).read_text());delta=F(data['delta']);R=F(data['numerator_Rayleigh']);groups=[(x['multiplicity'],F(x['gap_upper'])) for x in data[f'groups{mode}']]
assert sum(m for m,g in groups)==mode-1 and all(g>0 for m,g in groups)
assert F(producer['delta_lower'])<=delta
hot=up(exp(-R)[1]/3**96);cold=exp(-160*delta)[1];assert max(hot,cold)<F(2,5) and G(F(2,5))<0
boxes=[];end=F(1,2);unresolved=[]
for box in producer['warm_boxes']:
 lo,hi=F(box['beta_lower']),F(box['beta_upper']);assert lo==end and 0<hi-lo<=F(1,4);end=hi
 num=exp(-2*lo*delta)[1]
 j=up(num/(1+sum(m*exp(-hi*g)[0] for m,g in groups))**4)
 c=up(num/(1+sum(m*exp(-2*hi*g)[0] for m,g in groups))**2)
 assert j<=F(box['J_upper']) and c<=F(box['C_upper'])
 outcome=test(j,c)
 if box['replay']['outcome']=='excluded':assert outcome['excluded']
 if not outcome['excluded']:
  if unresolved and unresolved[-1][1]==str(lo):unresolved[-1][1]=str(hi)
  else:unresolved.append([str(lo),str(hi)])
 boxes.append({'lo':str(lo),'hi':str(hi),'J_upper':str(j),'C_upper':str(c),**outcome})
assert end==80
claimed=[[r['beta_lower'],r['beta_upper']] for r in producer['inconclusive_closed_box_unions']];assert unresolved==claimed
out={'status':'PASS independent necessary-condition replay','retained_states':mode,'hot_upper':str(hot),'cold_upper':str(cold),'all_beta_exclusion':not bool(unresolved),'inconclusive_closed_unions':unresolved,'boxes':boxes,'CPU_seconds':time.process_time()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/f'independent_scalar{mode}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='boxes'}))
