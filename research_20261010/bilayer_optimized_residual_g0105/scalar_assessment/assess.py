import sys,json,copy
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parents[1]
sys.path.insert(0,str(RES/'bilayer_seed_error_budget'))
from targets import *
HERE=Path(__file__).resolve().parent;RES=HERE.parents[1]
D=json.load(open(RES/'bilayer_seed_error_budget/reoptimized_saved.json'))['results'][0]['data'];physical=json.load(open(HERE.parent/'physical_result.json'));assert physical['g']=='21/200'
p=D['denominator_patches'][1];rho=C.poly(list(map(F,p['rayleigh_coefficients'])),F(21,200));old=p['uniform_Temple_width'];p['uniform_Temple_width']=str(rho-F(physical['ground_lower']));p['trace_ground_lower_override']=physical['ground_lower'];p['override_explanation']='Only normalized ground exponential changes, using independently pending complete residual ground lower with original trace pivot. Old variance metadata is not used to assert this new width.'
out=[]
for b in (F(8),F(47,5),F(19,2),F(11),F(13)):
 r,cc=ratios(D,b);rec={'beta':str(b),'ratios':r,'path':float_path(r,b)}
 if rec['path']['status']=='accepted_small_defect':
  er,_=ratios(D,b,exact=True);rec['exact_path_pending_physical_review']=exact_conditional_path(D,b,er)
 out.append(rec);print(b,rec['path'],flush=True)
(HERE/'assessment.json').write_text(json.dumps({'status':'bounded_actual_improved_input_assessment_no_gap_claim_without_complete_review','g':'21/200','old_trace_ground_width':old,'new_trace_ground_width':p['uniform_Temple_width'],'input':D,'results':out},indent=2)+'\n')
