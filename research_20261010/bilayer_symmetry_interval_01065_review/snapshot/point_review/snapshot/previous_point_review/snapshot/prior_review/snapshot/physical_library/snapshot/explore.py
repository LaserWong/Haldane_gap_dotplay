import os,sys,json,time,resource,math
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;RES=HERE.parent
sys.path.insert(0,str(RES/'interval_range_010'))
import certify as P
C=P.C
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
saved=json.load(open(RES/'interval_range_010/coverage/interval_010.json'))
vectors=[p['integer_coefficients'] for p in saved['denominator_patches']]+[saved['largest_base_trial']['integer_coefficients']]
# Use the same explicitly fixed odd trial family throughout this new frontier.
fixed_modes=P.L.O.fixed_modes
P.L.O.fixed_modes=lambda raw,z:fixed_modes(raw,F(1,10))
def data(lo,hi=None):return P.interval_data(lo,lo if hi is None else hi,vectors)
def margin_record(d):
 return [{'geometry':p['geometry'],'ground_identification_margin':p['ground_identification_margin'],'even_Temple_denominator':p['even_Temple_denominator'],'even_Temple_width':p['uniform_Temple_width'],'odd_cutoff_margin':str(min(F(x['uniform_Temple_denominator']) for x in p['odd_band']['modes']))} for p in d['denominator_patches']]
def raw_float(d,b):
 a,m=d['denominator_patches'];u0,u1,u2=P.L.upper_float(a,b),P.L.upper_float(a,2*b),P.L.upper_float(m,2*b)
 e={k:float(F(r['uniform_lower'])) for k,r in d['correlated_energy_combinations'].items()}
 j1=math.exp(b*e['J1'])/u0**8;j2=math.exp(b*e['J2'])/u1**8;c0=math.exp(b*e['C0'])/u2**2
 a=C.G(j1)
 if a<=0:return None
 bb=C.G(j2*a)
 if bb<=0:return None
 c=C.G(c0**4*a*a*bb)
 if c<=0:return None
 return [a,bb,c]
def path_float(d,b):
 raw=raw_float(d,b)
 if raw is None:return None
 can=C.transport(*raw,math.sqrt);joint=max(C.JS.full_product(raw),C.JS.full_product(can));best=None;windows=[]
 for cycle in range(12):
  if raw:can=list(map(max,can,C.transport(*raw,math.sqrt))) if can else C.transport(*raw,math.sqrt)
  if can is None:break
  joint=max(joint,C.JS.full_product(can),C.JS.full_product(raw) if raw else 0)
  u=max(1-x for x in can);beta=2*b*2**cycle
  if 0<u<=.002:
   score=min(windows+[math.log(1/(32*u))/beta])
   if best is None or score>best:best=score
  if u<1e-12:break
  if raw:
   a,x,y=raw;dd=x*math.sqrt(y);ss=x*x*math.sqrt(2*y-1) if y>.5 else 0
   pp=a**4*(2*dd-1)*math.sqrt(2*ss-1) if min(dd,ss)>.5 else 0
  else:pp=0
  if pp<=.5:break
  windows.append(math.log(pp/(1-pp))/beta)
  can,_=C.JS.canonical_advance(can,joint,False);raw=C.JS.plain_advance(raw,False) if raw else None
  joint=C.JS.full_product(can) if can else 0
 return best
if __name__=='__main__':
 start=time.time();out=[]
 for g in (F(41,400),F(21,200),F(11,100)):
  try:d=data(g);margin=margin_record(d);short,ss=C.short_gap(g)
  except AssertionError as e:out.append({'g':str(g),'legal':False,'error':str(e)});continue
  vals=[(v,F(i,20)) for i in range(100,401) if (v:=path_float(d,i/20)) is not None]
  best=max(vals) if vals else None;rec={'g':str(g),'legal':True,'margins':margin,'short_gap':str(short),'successful_temperatures':len(vals),'best_float':None if best is None else [best[0],str(best[1])],'data':d};out.append(rec)
  print(g,rec['margins'],rec['best_float'],flush=True)
  (HERE/'checkpoint.json').write_text(json.dumps(out,indent=2)+'\n')
 (HERE/'exploration.json').write_text(json.dumps({'results':out,'seconds':time.time()-start,'status':'bounded_float_proposals_with_exact_physical_legality_checks'},indent=2)+'\n')
