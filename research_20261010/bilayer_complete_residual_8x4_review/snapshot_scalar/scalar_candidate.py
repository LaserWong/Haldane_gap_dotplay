import os,sys,resource,json,hashlib,copy,math,time
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
cpus=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in cpus else min(cpus)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
HERE=Path(__file__).resolve().parent;RES=HERE.parent;BAND=RES/'low_band';OUT=HERE/'scalar';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(BAND/'frontier_g009'))
import scan_joint as S
paths=[BAND/'combined_ground_bounds/combined/patch_4x4_g1d10.json',HERE/'patch_8x4_g1d10.json',BAND/'combined_ground_bounds/combined/patch_8x8_g1d10.json']
recs=[json.loads(p.read_text()) for p in paths];np=BAND/'third_moment_exact/enlarged_8x8_g1d10.json';nr=json.loads(np.read_text());recs[2]['blocks']=recs[2]['blocks'][:1];recs[2]['blocks'][0]['eigen_upper']=[nr['shifted_rayleigh_upper']]
for shape,r in zip(['4x4','8x4','8x8'],recs):(OUT/f'input_{shape}.json').write_text(json.dumps(r,indent=2)+'\n')
shortpath=BAND/'frontier_g007_g010/short_sizes/uniform_short_sizes.json';short=F(json.loads(shortpath.read_text())['gap_lower'])
proposals=[]
for bi in range(100,401):
 b=F(bi,20);st=S.stages(recs,float(b),'txy');rows,status=S.sequence(st,float(b),'txy',False)
 if status=='accepted_small_defect':proposals.append((math.log(1/(32*rows[-1]['u']))/rows[-1]['beta'],b))
print('Successful floating proposals',len(proposals),flush=True)
out=dict(status='exact_point_scalar_candidate_pending_independent_review',grid='beta5..20 step.05 txy joint at most10 cycles',successful_float_proposals=len(proposals),selected=[])
for score,b in sorted(proposals,reverse=True)[:5]:
 ex=S.exact_record(recs,b,'txy',short);ex['float_score']=score;out['selected'].append(ex);print('EXACT',b,ex.get('accepted'),ex.get('all_integer_gap_display'),flush=True)
 if ex.get('accepted'):out['accepted_candidate']=True;out['all_integer_L_ge2_gap']=ex['all_integer_L_ge2_gap'];out['gap_display']=ex['all_integer_gap_display'];break
def labels(n,beta,order):
 state=[n,n,F(beta)];rows=[]
 for axis in order:
  i={'x':0,'y':1,'t':2}[axis];target=state[:];target[i]*=2
  rows.append(dict(axis=axis,base=[state[0],state[1],str(state[2])],endpoint=[target[0],target[1],str(target[2])]))
  state=target
 return rows
for ex in out['selected']:
 for st in ex['states']:
  n=st['n'];bb=F(st['beta']);st['canonical_edge_labels']=labels(n,bb,'xyt');st['raw_edge_labels']=labels(n,bb,'txy') if st['raw'] else None;st['physical_base']=[n,n,str(bb)];st['completed_cycles_after_seed']=st['cycle']
 for w in ex.get('windows',[]):
  w['scope']='Every integer L,W in [n,through], at the stated physical beta';w['included_in_final_minimum']=w['n']<ex['states'][-1]['n']
 if ex.get('accepted'):
  last=ex['states'][-1];ex['coverage']=dict(short_integer_sides=[2,7],first_dyadic_window_starts=8,all_early_windows=[[w['n'],w['through']] for w in ex['windows'] if w['included_in_final_minimum']],asymptotic_all_integer_sides_from=last['n'],terminal_physical_beta=last['beta'],no_missing_early_window=True)
  expected=8
  for lo,hi in ex['coverage']['all_early_windows']:assert lo==expected;expected=hi
  assert expected==last['n']
out['exact_attempts']=out.pop('selected')
out['source_sha256']={str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[np,shortpath,HERE/'PHYSICAL_MANIFEST.json']}
(OUT/'candidate.json').write_text(json.dumps(out,indent=2)+'\n')
