import os,sys,resource,json,math,time
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parent
sys.path.insert(0,str(RES/'low_band/frontier_g009'))
import scan_joint as S
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
paths=[RES/'bilayer_complete_residual_8x4/scalar'/f'input_{x}.json' for x in ('4x4','8x4','8x8')]
recs=[json.loads(p.read_text()) for p in paths]
def direct(a,b,c):
 if c<=.5:return 0
 d=b*math.sqrt(c);s=b*b*math.sqrt(2*c-1)
 if min(d,s)<=.5:return 0
 return a**4*(2*d-1)*math.sqrt(2*s-1)
def path(beta):
 st=S.stages(recs,beta,'txy');raw=st.get('permuted_prefix');can=st.get('canonical')
 if can is None:return None
 joint=S.J.full_product(raw);windows=[];best=None
 for cycle in range(7):
  conv=S.transport(*raw,'txy',math.sqrt) if raw else None
  if conv:can=conv if can is None else list(map(max,can,conv))
  if can is None:break
  joint=max(joint,S.J.full_product(can),S.J.full_product(raw) if raw else 0)
  bb=2*beta*2**cycle;u=max(1-x for x in can)
  if 0<u<=.002:
   g=min(windows+[math.log(1/(32*u))/bb]);row=dict(gap=g,beta=beta,terminal_cycle=cycle,windows=windows[:])
   if best is None or g>best['gap']:best=row
  cc=direct(*raw) if raw else 0
  # Existing canonical interpolation provides independently accepted fallback.
  try:old,_=S.J.interpolate_2d_joint(*can,joint);cc=max(cc,float(old))
  except (AssertionError,ValueError):pass
  if cc<=.5:break
  if cc>=1:break
  windows.append(math.log(cc/(1-cc))/bb)
  can,_=S.J.canonical_advance(can,joint,False);raw=S.J.plain_advance(raw,False) if raw else None
  joint=S.J.full_product(can) if can else 0
 return best
if __name__=='__main__':
 start=time.time();rows=[r for i in range(120,401) if (r:=path(i/20))]
 rows.sort(key=lambda x:-x['gap']);out={'status':'bounded_float_proposals_only','grid':'beta6..20 step.05, at most7 states','results':rows[:10],'successful_temperatures':len(rows),'seconds':time.time()-start}
 (HERE/'scan.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
