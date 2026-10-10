import os,sys,resource,json,copy,math
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
cpus=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in cpus else min(cpus)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
HERE=Path(__file__).resolve().parent;RES=HERE.parent;BAND=RES/'low_band'
sys.path.insert(0,str(BAND/'frontier_g009'))
import scan_joint as S
from correlated_low_band import traces_float
shapes=['4x4','8x4','8x8']
base=[json.loads((BAND/'combined_ground_bounds'/'combined'/f'patch_{s}_g1d10.json').read_text()) for s in shapes]
u=json.loads((BAND/'third_moment_exact'/'enlarged_8x8_g1d10.json').read_text())['shifted_rayleigh_upper']
base[2]['blocks']=base[2]['blocks'][:1];base[2]['blocks'][0]['eigen_upper']=[u]
def scan(recs):
 out=[];parts=[]
 for bi in range(100,401):
  b=bi/20;st=S.stages(recs,b,'txy');rows,status=S.sequence(st,b,'txy',False)
  parts.append(dict(beta=b,status=status,initial=st,min_defect=min([r['u'] for r in rows],default=1),cycles=len(rows)))
  if status=='accepted_small_defect':out.append(dict(beta=b,score=math.log(1/(32*rows[-1]['u']))/rows[-1]['beta']))
 return dict(successes=len(out),best=max(out,key=lambda r:r['score']) if out else None,best_partial=min(parts,key=lambda r:r['min_defect']))
cases={'baseline':base}
for name in ['ground_lower_to_saved_upper','odd_lower_to_saved_upper','tail_deleted','all_denominator_uncertainty_deleted']:
 r=copy.deepcopy(base)
 for p in r[:2]:
  if name in ['ground_lower_to_saved_upper','all_denominator_uncertainty_deleted']:p['blocks'][0]['eigen_lower']=p['blocks'][0]['eigen_upper'][:]
  if name in ['odd_lower_to_saved_upper','all_denominator_uncertainty_deleted']:p['blocks'][1]['eigen_lower']=p['blocks'][1]['eigen_upper'][:]
  if name in ['tail_deleted','all_denominator_uncertainty_deleted']:p['number_sector_bins']['bins']=p['number_sector_bins']['bins'][:2]
 cases[name]=r
for delta in [.0005,.001,.002,.003,.004,.005,.01]:
 r=copy.deepcopy(base);r[2]['blocks'][0]['eigen_upper']=[str(F(u)-F(str(delta)))];cases['numerator_minus_'+str(delta)]=r
out={name:scan(r) for name,r in cases.items()}
for name,r in out.items():print(name,r['successes'],r['best'],r['best_partial']['beta'],r['best_partial']['min_defect'],flush=True)
betas=[8,9,9.25,10,12]
out['trace_decomposition']=[]
for b in betas:
 row={'beta':b,'patches':[]}
 for r,t in [(base[0],b),(base[0],2*b),(base[1],2*b)]:
  shift=float(F(r['blocks'][0]['eigen_upper'][0]));q=traces_float(r,t)
  gr=math.exp(-t*(float(F(r['blocks'][0]['eigen_lower'][0]))-shift))
  od=q[1]-q[2]-gr
  row['patches'].append(dict(N=r['N'],physical_beta=t,ground=gr,ground_excess_over_saved_upper=gr-1,odd=od,tail=q[2],total_upper=q[1]))
 out['trace_decomposition'].append(row)
out['limitations']='All scans conditional floating diagnostics, beta5..20 step .05, at most10 cycles; idealizing a lower endpoint to a trial upper is NOT a valid certificate. Tail deletion invalid. No all-beta exclusion.'
(HERE/'diagnostics.json').write_text(json.dumps(out,indent=2)+'\n')
