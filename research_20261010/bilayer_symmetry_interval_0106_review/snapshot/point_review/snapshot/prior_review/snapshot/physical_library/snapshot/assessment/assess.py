import os,sys,resource,json,time,math
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
# Imported predecessors request larger limits. Clamp those calls to this task's hard caps.
real=resource.setrlimit
def clamp(which,limits):
 old=resource.getrlimit(which);cap=old[1];real(which,tuple(min(v,cap) if cap>=0 else v for v in limits))
resource.setrlimit=clamp
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parent
sys.path.insert(0,str(RES/'bilayer_frontier_above_010'))
import explore as E
import ast,types
B=types.SimpleNamespace(E=E,C=E.C,P=E.P)
ns=dict(F=F,math=math,C=E.C,exp=E.C.exp_interval)
target=json.loads((RES/'bilayer_frontier_above_010/points.json').read_text())['results'][-1]['input']
ns['TARGET']={k:F(target[k]) for k in ('J1','J2','C0')}
for name,functions in [('budget.py',{'components','ratios','raw'}),('targets.py',{'sufficient_numerator'})]:
 nodes=[x for x in ast.parse((RES/'bilayer_seed_error_budget'/name).read_text()).body if isinstance(x,ast.FunctionDef) and x.name in functions]
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'cached_scalar_functions','exec'),ns)
for k in ('ratios','sufficient_numerator','TARGET'):setattr(B,k,ns[k])
B.float_path=lambda r,b:dict(status='initial_cycle_positive_only' if min(r.values())>1e-30 and ns['raw'](r) is not None else 'initial_cycle_nonpositive')
resource.setrlimit=real
C=B.C;P=B.P;start=time.time()
sys.path.insert(0,str(RES/'low_band/joint_trace_bootstrap'));import joint_scalar as J
from finite_window_2d import exp_upper
serial=lambda x:str(x) if isinstance(x,F) else ({k:serial(v) for k,v in x.items()} if isinstance(x,dict) else [serial(v) for v in x] if isinstance(x,list) else x)
transport=lambda a,b,c,order,sqrt:C.transport(a,b,c,sqrt)
S=types.SimpleNamespace(J=J,transport=transport,serial=serial)
rrns=dict(F=F,math=math,D=10**120,S=S,exp_upper=exp_upper)
nodes=[x for x in ast.parse((RES/'bilayer_direct_window_extension/replay.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name in {'sqrtlo','down','direct_exact','labels'}];exec(compile(ast.Module(body=nodes,type_ignores=[]),'cached_direct','exec'),rrns)
R=types.SimpleNamespace(**rrns);ins=dict(F=F,S=S,R=R)
nodes=[x for x in ast.parse((RES/'bilayer_direct_window_continuation/replay_intervals.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='improve'];exec(compile(ast.Module(body=nodes,type_ignores=[]),'cached_windows','exec'),ins)
def diag(r,beta):
 raw=[]
 for key in ('J1','J2','C0'):
  z=r[key] if key=='J1' else r[key]*raw[0] if key=='J2' else r[key]**4*raw[0]**2*raw[1]
  if z<1e-100:return dict(status='initial_'+key+'_underflow',cycle=0)
  val=C.G(z)
  if val<=0:return dict(status='initial_'+key+'_nonpositive',cycle=0,argument=z,computed_lower=val)
  raw.append(val)
 can=C.transport(*raw,math.sqrt);joint=J.full_product(raw);rows=[];best=None
 for cycle in range(16):
  if raw:
   can=list(map(max,can,C.transport(*raw,math.sqrt))) if can else C.transport(*raw,math.sqrt)
  if can is None:return dict(status='continuation_left_domain',cycle=cycle,states=rows)
  joint=max(joint,J.full_product(can),J.full_product(raw) if raw else 0);u=max(1-x for x in can)
  rows.append(dict(cycle=cycle,defect=u,raw=raw,canonical=can))
  if 0<u<=.002:return dict(status='small_defect_candidate',cycle=cycle,states=rows)
  direct=float(rrns['direct_exact'](*map(F,raw))[0]) if raw else 0
  old=float(J.interpolate_2d_joint(*can,joint)[0]);v=max(direct,old)
  if v<=.5:return dict(status='finite_window_purity_le_half',cycle=cycle,purity=v,states=rows)
  can,_=J.canonical_advance(can,joint,False);raw=J.plain_advance(raw,False) if raw else None;joint=J.full_product(can) if can else 0
 return dict(status='round_limit',states=rows)
opts=json.loads((RES/'bilayer_split_basis_plan/reoptimization.json').read_text())['results'];pencils=json.loads((RES/'bilayer_residual_pencil_optimization/result.json').read_text())['results'];out=[]
for g in (F(11,100),F(3,25)):
 d=B.E.data(g);ops=[x for x in opts if F(x['g'])==g];ops.sort(key=lambda x:math.prod(x['shape']));gain=C.poly(list(map(F,d['largest_base_trial']['rayleigh_coefficients'])),g)-F(ops[-1]['split']['rayleigh']);width={};physical=[]
 for patch in d['denominator_patches']:
  N=patch['N'];rho=C.poly(list(map(F,patch['rayleigh_coefficients'])),g);w=next(t for t in pencils if F(t['g'])==g and math.prod(t['shape'])==N);lower=F(w['Temple_lower']);width[f'width{N}']=rho-lower;assert width[f'width{N}']>0;floor=C.reference(g,N,1)-rho;assert min(F(m['uniform_Temple_denominator']) for m in patch['odd_band']['modes'])>0
  for mode in patch['odd_band']['modes']:mode['eigen_lower_minus_ground_rayleigh_uniform_lower']=str(max(floor,F(mode['eigen_lower_minus_ground_rayleigh_uniform_lower'])))
  bestup=F(next(x for x in ops if math.prod(x['shape'])==N)['split']['rayleigh']);physical.append(dict(N=N,ground_lower=str(lower),best_upper=str(bestup),ground_uncertainty=str(bestup-lower),odd_floor=str(floor),trace_pivot=str(rho)))
 tests=[]
 for beta in (F(8),F(47,5),F(10),F(11),F(12),F(13),F(15)):
  rat,comp=B.ratios(d,beta,scenario=width,epsilon=gain);failure=diag(rat,float(beta));row=dict(beta=str(beta),ratios=rat,components=comp,diagnostic=failure)
  if failure['status']=='small_defect_candidate':
   er,ec=B.ratios(d,beta,scenario=width,epsilon=gain,exact=True);er={k:C.down(v,80) for k,v in er.items()};raw=ns['raw'](er);assert raw is not None;can=C.transport(*raw,C.sqrt_down)
   short=F(50426624396,10**12);rec=dict(coupling_interval=[str(g)]*2,beta_initial=str(beta),**{k:str(v) for k,v in er.items()},permuted_first_purities=serial(raw),canonical_first_purities=serial(can),short_sizes=[dict(L=L,gap_lower=str(short)) for L in range(2,8)],all_integer_L_ge2_gap='0')
   try:row['exact_conditional_certificate']=ins['improve'](rec);row['exact_initial']=rec;row['exact_components']=serial(ec)
   except AssertionError:row['exact_conditional_status']='did_not_certify'
  row['components_rebased_best_upper']=[{k:v*math.exp(float((beta if i==0 else 2*beta)*(F(physical[0 if i<2 else 1]['best_upper'])-F(physical[0 if i<2 else 1]['trace_pivot'])))) for k,v in part.items()} for i,part in enumerate(comp)]
  if beta in (F(47,5),F(10)):
   sensitivity=[]
   for label in ('ground16_ideal','ground32_ideal','both_grounds_ideal','odd_remove','odd_ritz','tail_remove'):
    import copy
    dd=copy.deepcopy(d);ww=width.copy()
    for pp,ph in zip(dd['denominator_patches'],physical):
     N=pp['N']
     if label in (f'ground{N}_ideal','both_grounds_ideal'):ww[f'width{N}']=F(ph['trace_pivot'])-F(ph['best_upper'])
     if label=='odd_remove':pp['odd_band']['modes']=[]
     if label=='odd_ritz':
      for mm in pp['odd_band']['modes']:mm['eigen_lower_minus_ground_rayleigh_uniform_lower']=str(min(map(F,mm['theta_minus_ground_rayleigh_endpoint_lowers'])))
     if label=='tail_remove':pp['reference_minus_rayleigh_uniform_lowers']=[]
    sr,sc=B.ratios(dd,beta,scenario=ww,epsilon=gain);sensitivity.append(dict(hypothetical_only=label,diagnostic=diag(sr,float(beta)),ratios=sr))
   row['sensitivity']=sensitivity
  tests.append(row);print(g,beta,failure['status'],row.get('exact_conditional_certificate',{}).get('gap_display'),flush=True);C.exp_interval.cache_clear()
  (HERE/'checkpoint.json').write_text(json.dumps(out+[dict(g=str(g),physical=physical,tests=tests)],indent=2,default=str)+'\n')
 targets=[]
 if g==F(11,100):
  ph=physical[1];basewidth=F(ph['trace_pivot'])-F(ph['best_upper']);actual=F(ph['ground_uncertainty'])
  for beta in (F(47,5),F(10)):
   lo,hi=F(0),actual
   for _ in range(32):
    mid=(lo+hi)/2;ww=width.copy();ww['width32']=basewidth+mid;rat,_=B.ratios(d,beta,scenario=ww,epsilon=gain)
    if diag(rat,float(beta))['status']=='small_defect_candidate':lo=mid
    else:hi=mid
   if lo==0:continue
   wanted=F(math.floor(float(lo)*.99*10**10),10**10);ww=width.copy();ww['width32']=basewidth+wanted;er,ec=B.ratios(d,beta,scenario=ww,epsilon=gain,exact=True);er={k:C.down(v,80) for k,v in er.items()};raw=ns['raw'](er);can=C.transport(*raw,C.sqrt_down);short=F(50426624396,10**12)
   rec=dict(coupling_interval=[str(g)]*2,beta_initial=str(beta),**{k:str(v) for k,v in er.items()},permuted_first_purities=serial(raw),canonical_first_purities=serial(can),short_sizes=[dict(L=L,gap_lower=str(short)) for L in range(2,8)],all_integer_L_ge2_gap='0')
   cert=ins['improve'](rec);L=F(ph['best_upper'])-wanted
   targets.append(dict(beta=str(beta),hypothetical_only=True,target_ground32_width=str(wanted),target_ground32_lower=str(L),current_ground32_lower=ph['ground_lower'],required_lower_improvement=str(L-F(ph['ground_lower'])),conditional_certificate=cert,exact_initial=rec))
 out.append(dict(g=str(g),physical=physical,tests=tests,hypothetical_ground32_targets=targets))
(HERE/'result.json').write_text(json.dumps(dict(status='ACTUAL_INPUT_SCALAR_ASSESSMENT_CONDITIONAL_ON_COMPLETE_MATRIX_AUDIT',results=out,seconds=time.time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2,default=str)+'\n')
