import sys,json,copy,time,hashlib
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parents[1]
sys.path.insert(0,str(RES/'bilayer_seed_error_budget'))
from targets import *
HERE=Path(__file__).resolve().parent;RES=HERE.parents[1]
D=json.load(open(RES/'bilayer_seed_error_budget/reoptimized_saved.json'))['results'][0]['data'];physical_paths=[HERE.parent/'physical_result.json',RES/'bilayer_optimized_residual_g0105/physical_result.json']
for p,source in zip(D['denominator_patches'],physical_paths):
 physical=json.load(open(source));assert physical['g']=='21/200';rho=C.poly(list(map(F,p['rayleigh_coefficients'])),F(21,200));p['uniform_Temple_width']=str(rho-F(physical['ground_lower']));assert F(p['uniform_Temple_width'])>0
 p['trace_ground_lower_override']={'lower':physical['ground_lower'],'source':str(source.relative_to(RES)),'search_dimension':physical['search_dimension'],'explanation':'Original pivot trial and polynomial metadata are retained for trace normalization only; the overridden ground lower comes from the new complete residual.'}
out=[];start=time.time()
for b in (F(47,5),F(19,2),F(10),F(11)):
 r,_=ratios(D,b);diag=float_path(r,b);print(b,diag['status'],flush=True)
 if diag['status']!='accepted_small_defect':continue
 er,comp=ratios(D,b,exact=True);cert=exact_conditional_path(D,b,er)
 row={'status':'actual_new_input_exact_allsize_candidate_pending_independent_review','g':'21/200','physical_input':D,'exact_initial_trace_components':R.S.serial(comp),'exact_initial_ratios':R.S.serial(er),'certificate':cert};out.append(row);print('EXACT',b,cert['gap_display'],flush=True)
 (HERE/'checkpoint.json').write_text(json.dumps(out,indent=2)+'\n');exp.cache_clear()
result={'status':'producer_exact_candidate_pending_independent_physical_and_scalar_review','results':out,'seconds':time.time()-start,'physical_source_sha256':{str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in physical_paths},'best':max(out,key=lambda x:F(x['certificate']['gap'])) if out else None}
(HERE/'candidate_check.json').write_text(json.dumps(result,indent=2)+'\n')
