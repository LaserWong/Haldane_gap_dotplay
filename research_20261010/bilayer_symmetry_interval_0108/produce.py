"""Uniform cached-polynomial scalar certificate; no new matrix contractions."""
import os,resource,json,math,time,hashlib,ast
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_CPU,(115,115));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
HERE=Path(__file__).resolve().parent;RES=HERE.parent;start=time.process_time();D=10**60;GRID=1<<384
load=lambda p:json.loads(p.read_text())
point=RES/'bilayer_symmetry_frontier_0107_0108';assert hashlib.sha256((point/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='9cfcc6ca5332fa4ed2724f16f49554efd5c5de535b736f1dffcbc94d7dde2475'
for p,h in load(point/'MANIFEST_SHA256.json').items():assert hashlib.sha256((point/p).read_bytes()).hexdigest()==h,p
for p,h in load(point/'INPUT_SHA256.json').items():assert hashlib.sha256((RES/p).read_bytes()).hexdigest()==h,p
short_record=load(RES/'bilayer_short_bridge_refinement/result.json')['continuous_endpoints'][0]
assert short_record['continuous_coupling_interval']==['0','3/20'] and F(short_record['decimal_gap_lower'])>=F(50426624396,10**12)
for filename,names in [(RES/'bilayer_symmetry_scalar_pilot/exact_pilot.py',{'down','up','sqrtlo','G','raw','advance','window','canonical','gap_witness'}),(RES/'bilayer_symmetry_intermediate_points/produce.py',{'exp','poly','root60','ref','qload','qadd','qmul','qsign','qbound','qpoly'})]:
 for node in ast.parse(filename.read_text()).body:
  if isinstance(node,ast.FunctionDef) and node.name in names:exec(compile(ast.Module(body=[node],type_ignores=[]),'sealed_scalar_helpers','exec'))
rt2=root60(F(2));fixed=load(point/'result.json')['results'][-1];assert F(fixed['g'])==F(27,250)
moms={}
for row in fixed['matrix_witnesses']:
 selected=row[row['selected']+'_optimized'];moms[row['N']]=dict(rho=selected['rayleigh_coefficients'],variance=selected['full_variance_coefficients'])
num=list(map(F,fixed['numerator_witness']['rayleigh_coefficients']))
base=next(x['data'] for x in load(RES/'bilayer_symmetry_scalar_pilot/snapshot/bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100))

def variance_form(coeff):
 v=list(map(F,coeff));assert v[0]>=0 and v[2]>=0 and 4*v[0]*v[2]>=v[1]*v[1]
 return v

def odd_variance_form(coeff):
 a,b,c=map(qload,coeff);disc=qadd(qmul((F(4),F(0)),qmul(a,c)),qmul((F(-1),F(0)),qmul(b,b)))
 assert qsign(a)>=0 and qsign(c)>=0 and qsign(disc)>=0
 return dict(c0=list(map(str,a)),c2=list(map(str,c)),four_c0_c2_minus_c1sq=list(map(str,disc)))

def physical(lo,hi):
 assert F(213,2000)<=lo<hi<=F(27,250);patches=[]
 for ix,N in enumerate([16,32]):
  m=moms[N];rho=list(map(F,m['rho']));var=variance_form(m['variance']);mean=[poly(rho,g) for g in [lo,hi]];variance=[poly(var,g) for g in [lo,hi]]
  reference=[[ref(N,g,q)-rr for g,rr in zip([lo,hi],mean)] for q in range(1,N+1)]
  lowers=[min(x) for x in reference];assert lowers[0]>0 and lowers[1]>0;vmax=max(variance);width=vmax/lowers[1]
  odd=[];details=[]
  for mode in base['denominator_patches'][ix]['odd_band']['modes']:
   assert qsign(qload(mode['gram_symbol']))>0;form=odd_variance_form(mode['residual_squared_coefficients'])
   means=[qpoly(mode['theta_coefficients'],g) for g in [lo,hi]];vars=[qpoly(mode['residual_squared_coefficients'],g) for g in [lo,hi]]
   encl=[qbound(x) for x in means];vars_up=[qbound(x)[1] for x in vars];delta=[ref(N,g,2)-u for g,(l,u) in zip([lo,hi],encl)];den=min(delta);assert den>0
   rel=min(l-r for (l,u),r in zip(encl,mean));vr=max(vars_up);assert vr>=0;ell=max(lowers[0],rel-vr/den);odd.append(ell)
   details.append(dict(momentum=mode['momentum'],gram_symbol=mode['gram_symbol'],mean_endpoint_enclosures=[[str(x) for x in v] for v in encl],variance_endpoint_upper=list(map(str,vars_up)),variance_form=form,cutoff_margins=list(map(str,delta)),uniform_Temple_denominator=str(den),theta_minus_pivot_lower=str(rel),uniform_odd_lower=str(ell)))
  assert len(odd)==N
  patches.append(dict(N=N,trial_dimension=21 if N==16 else 57,mean_coefficients=list(map(str,rho)),variance_coefficients=list(map(str,var)),mean_endpoint_values=list(map(str,mean)),variance_endpoint_values=list(map(str,variance)),ground_identification_margin=str(lowers[0]),even_Temple_denominator=str(lowers[1]),uniform_ground_width=str(width),odd=list(map(str,odd)),odd_details=details,tail=list(map(str,lowers[1:])),reference_relative_endpoint_lowers=[[str(x) for x in t] for t in reference]))
 rr=[list(map(F,moms[N]['rho'])) for N in [16,32]]+[num];comb={};combdetail={}
 for k,w in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
  coeff=[sum(w[j]*rr[j][i] for j in range(3)) for i in range(2)];ends=[poly(coeff,g) for g in [lo,hi]];comb[k]=min(ends);combdetail[k]=dict(coefficients=list(map(str,coeff)),endpoint_values=list(map(str,ends)),uniform_lower=str(min(ends)))
 return dict(coupling_interval=list(map(str,[lo,hi])),patches=patches,numerator_coefficients=list(map(str,num)),energy_combinations={k:str(x) for k,x in comb.items()},energy_combination_details=combdetail,retained_counts=[49,97,1],trial_dimensions=[21,57,43])

def ratios(phys,beta,exact=True):
 eup=(lambda z:exp(z)[1]) if exact else lambda z:math.exp(float(z));elo=(lambda z:exp(z)[0]) if exact else lambda z:math.exp(float(z));uppers=[];parts=[]
 for ix,mult in [(0,1),(0,2),(1,2)]:
  p=phys['patches'][ix];b=mult*beta;N=p['N'];ground=eup(b*F(p['uniform_ground_width']));odd=3*sum(eup(-b*F(x)) for x in p['odd']);tail=sum(math.comb(3*N+q-1,q)*eup(-b*F(x)) for q,x in enumerate(p['tail'],2));uppers.append(ground+odd+tail);parts.append(dict(beta=str(b),N=N,ground=str(ground),odd=str(odd),tail=str(tail),total=str(ground+odd+tail)))
 rr={k:elo(beta*F(phys['energy_combinations'][k]))/u**power for k,u,power in zip(['J1','J2','C0'],uppers,[8,8,2])}
 return ({k:down(x) for k,x in rr.items()} if exact else rr),parts

def score(rr,beta):
 abc=raw(rr,False)
 if abc is None:return None
 bounds=[]
 for j in range(18):
  u=max(1-x for x in canonical(abc,False));bb=2*float(beta)*2**j
  if 1e-12<u<=.002:return min(bounds+[math.log(1/(32*u))/bb])
  v=window(abc,False)
  if v<=.5:return None
  bounds.append(math.log(v/(1-v))/bb);abc=advance(abc,False)
  if abc is None:return None
 return None

def certificate(phys,beta):
 rr,trace=ratios(phys,beta);assert all(0<x<=1 for x in rr.values());abc=raw(rr);assert abc is not None;states=[]
 for j in range(20):
  can=canonical(abc);u=max(1-x for x in can);bb=2*beta*2**j;row=dict(n=8*2**j,beta=str(bb),raw=list(map(str,abc)),canonical=list(map(str,can)),common_defect=str(u))
  if 0<u<=F(1,500):
   prop=F(math.floor(math.log(float(1/(32*u)))/float(bb)*10**12)-1,10**12)
   while exp(bb*prop)[1]*32*u>=1:prop-=F(1,10**12)
   row['asymptotic_gap']=str(prop);row['exp_witness']=str(exp(bb*prop)[1]*32*u);states.append(row);break
  v=window(abc);assert v>F(1,2);gap=gap_witness(v,bb);row.update(thermal_lower=str(v),finite_window_gap=str(gap),exp_gap_witness=str(exp(bb*gap)[1]*(1-v)/v));states.append(row);abc=advance(abc);assert abc is not None
 assert 'asymptotic_gap' in states[-1]
 short=F(50426624396,10**12);gap=min([short]+[F(x.get('finite_window_gap',x.get('asymptotic_gap'))) for x in states]);assert gap>0
 return dict(status='EXACT_CLOSED_INTERVAL_CANDIDATE_PENDING_REVIEW',coupling_interval=phys['coupling_interval'],beta_initial=str(beta),ratios={k:str(x) for k,x in rr.items()},trace_components=trace,states=states,short_sizes=dict(L_from=2,L_through=7,coupling_interval=['0','3/20'],gap=str(short)),all_integer_L_ge2_gap=str(gap),gap_display=float(gap),physical=phys)

queue=[(F(213,2000),F(27,250))];accepted=[];attempts=[]
while queue:
 lo,hi=queue.pop(0);p=physical(lo,hi);grid=[]
 for i in range(160,251):
  beta=F(i,20);r,_=ratios(p,beta,False);v=score(r,beta)
  if v is not None:grid.append((v,beta))
 row=dict(interval=list(map(str,[lo,hi])),successful_grid_proposals=len(grid))
 if grid:
  value,beta=max(grid);c=certificate(p,beta);row.update(beta=str(beta),gap=c['all_integer_L_ge2_gap'])
  if F(c['all_integer_L_ge2_gap'])>=F(4499695659,10**12):
   accepted.append(c);print(row,flush=True)
  else:
   assert hi-lo>F(1,1000000),'Requested retained gap not reached at minimum tested width'
   mid=(lo+hi)/2;queue[:0]=[(lo,mid),(mid,hi)];row['subdivided_to_preserve_prior_uniform_gap']=True
 else:
  assert hi-lo>F(1,1000000),'No candidate at minimum tested interval width';mid=(lo+hi)/2;queue[:0]=[(lo,mid),(mid,hi)];row['subdivided']=True
 attempts.append(row);(HERE/'checkpoint.json').write_text(json.dumps(dict(accepted=accepted,attempts=attempts,pending=[list(map(str,x)) for x in queue],cpu_seconds=time.process_time()-start),indent=2)+'\n');exp.cache_clear()
assert accepted[0]['coupling_interval'][0]=='213/2000' and accepted[-1]['coupling_interval'][1]=='27/250'
assert all(a['coupling_interval'][1]==b['coupling_interval'][0] for a,b in zip(accepted,accepted[1:]))
gap=min(F(x['all_integer_L_ge2_gap']) for x in accepted)
result=dict(status='EXACT_CLOSED_01065_TO_0108_CANDIDATE_PENDING_INDEPENDENT_REVIEW',coupling_interval=['213/2000','27/250'],all_integer_square_L_ge=2,uniform_gap=str(gap),gap_display=float(gap),certificates=accepted,attempts=attempts,no_gap_monotonicity_assumption=True,no_physical_contractions=True,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('COVERED',len(accepted),float(gap),'CPU',result['cpu_seconds'],flush=True)
