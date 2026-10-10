from fractions import Fraction as F
from pathlib import Path
import json,math,resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
P=Path(__file__).resolve().parent
rows=json.loads((P/'copied_beta8_lower_trace_intervals.json').read_text());r=next(r for r in rows if r['n']==8 and r['twist']=='I');u=F(r['upper']);out=[]
for L in [128,256,512,1024]:
 ell=F(math.floor(math.exp(-math.log(float(u))/(L-8))*10**6),10**6)
 value=u*ell**(L-8);assert value<1
 out.append({'L':L,'ell':str(ell),'ell_display':float(ell),'exclusion_upper_display':float(value),'exact_comparison_passed':True})
result={'status':'EXACT_SCALAR_CHECK_CONDITIONAL_ON_ALL_LENGTH_TRANSFER_IDENTITIES_AND_ARCHIVED_INPUTS','beta':8,'target_shift':'4.76121','upper_trace_source_shift':'4.7608','U8':str(u),'B_L':'1','rows':out,'uniform_gap_proved':False,'thermal_purity_claim':False}
(P/'atom_location.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
