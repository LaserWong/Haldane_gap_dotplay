"""Exact new g=.10 scalar replay using sealed independent arithmetic."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import math,json,hashlib,copy,ast,types,importlib.util,time,os,resource,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent.parent;OUT=Path(__file__).resolve().parent;SS=OUT/'snapshot_scalar'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
PRIOR=ROOT/'third_moment_review/snapshot/prior_reviews'
# Files are covered by the third-moment independent review's checked manifest.
manifest=load(ROOT/'third_moment_review/MANIFEST_SHA256.json')
for rel in ['snapshot/prior_reviews/combined_ground_review/independent_math.py','snapshot/prior_reviews/bilayer_polynomial_frontier_review/audit.py']:
 assert sha(ROOT/'third_moment_review'/rel)==manifest.get('files',manifest)[rel]
path=PRIOR/'combined_ground_review/independent_math.py';spec=importlib.util.spec_from_file_location('accepted_math',path);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
path=PRIOR/'bilayer_polynomial_frontier_review/audit.py';names=['down','sqrtlo','full','valid','move','advance','canonical_next','one_window','window']
nodes=[n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in nodes}==set(names)
ns={'F':F,'math':math,'M':M};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns);J=types.SimpleNamespace(**ns)
def graph(nx,ny):
 edges=Counter()
 for x in range(nx):
  for y in range(ny):
   for a,b in [((x+1)%nx,y),(x,(y+1)%ny)]:edges[tuple(sorted([x*ny+y,a*ny+b]))]+=1
 return edges,None

def audit_inputs():
 recs=[]
 for shape in ['4x4','8x4','8x8']:
  p=ROOT/f'low_band/combined_ground_bounds/combined/patch_{shape}_g1d10.json';old=load(p)
  accepted=ROOT/f'combined_ground_review/snapshot/research_20261010/low_band/combined_ground_bounds/combined/patch_{shape}_g1d10.json'
  assert sha(p)==sha(accepted)
  expected=copy.deepcopy(old);actual=load(SS/f'scalar/input_{shape}.json')
  if shape=='8x4':
   expected['blocks'][0]['eigen_lower']=[load(OUT/'assembly_result.json')['Temple_lower']]
   expected['complete_residual_source']='physical_result.json';expected['status']='exact_complete_residual_ground_candidate_pending_independent_review'
  elif shape=='8x8':
   num=load(ROOT/'low_band/third_moment_exact/enlarged_8x8_g1d10.json')
   assert F(num['shifted_rayleigh_upper'])==F(load(ROOT/'bilayer_g010_diagnostics_review/exact_result.json')['numerator']['upper'])
   expected['blocks']=expected['blocks'][:1];expected['blocks'][0]['eigen_upper']=[num['shifted_rayleigh_upper']]
  assert actual==expected,shape;recs.append(actual)
 return recs
def labels(n,tau,order):
 base=[n,n,F(tau)];ans=[];monomial=Counter()
 for axis in order:
  before=base[:];base['xyt'.index(axis)]*=2
  ans.append(dict(axis=axis,base=[before[0],before[1],str(before[2])],endpoint=[base[0],base[1],str(base[2])]))
 for i,row in enumerate(ans):
  weight=2**(2-i);a=tuple(row['base']);b=tuple(row['endpoint']);monomial[b]+=weight;monomial[a]-=2*weight
 return ans,{k:v for k,v in monomial.items() if v}

def short_sizes():
 r=load(ROOT/'low_band/frontier_g007_g010/short_sizes/uniform_short_sizes.json');assert r['sides']==list(range(2,8)) and F(r['g_max'])==F(1,10)
 sums=[sum(w*w for w in graph(L,L)[0].values()) for L in range(2,8)];assert sums==r['weighted_edge_square_sums']==[16,18,32,50,72,98]
 alpha,delta,v=map(F,[r['alpha_lower'],r['delta_lower'],r['vacuum_creation_norm_squared_upper']]);assert alpha==F(4,5) and 0<delta*delta<=F(3,5) and v==F(147,200)
 gap=delta-v/(alpha+delta);assert gap==F(r['gap_lower'])>0
 return gap

def replay(short):
 variant="complete_residual"
 candidate=load(SS/'scalar/candidate.json');recs=audit_inputs();upper=F(recs[2]['blocks'][0]['eigen_upper'][0]);assert candidate['accepted_candidate'] is True
 for rel,h in candidate['source_sha256'].items():assert sha(ROOT/rel)==h,rel
 result=[]
 for r in candidate['exact_attempts']:
  assert r['accepted'] and r['order']=='txy';beta=F(r['beta_initial']);num=M.exponential(-2*beta*upper)[0]
  hi0=M.trace(recs[0],beta)[1];hi1=M.trace(recs[0],2*beta)[1];hi2=M.trace(recs[1],2*beta)[1]
  independent=[M.down(num/hi0**8,10**16),M.down(num*num/hi1**8,10**16),M.down(num/hi2**2,10**16)]
  saved=[F(r['initial'][k]) for k in ('J1','J2','C0')];assert all(0<x<=y<=1 for x,y in zip(saved,independent)),(variant,saved,independent)
  raw=M.first_steps(saved);assert raw==list(map(F,r['initial']['permuted_prefix'])) and len(raw)==3
  canonical=J.move(raw);assert canonical==list(map(F,r['initial']['canonical']));joint=J.full(raw);states=[]
  for i,s in enumerate(r['states']):
   if raw is not None:
    converted=J.move(raw);canonical=converted if canonical is None else [max(x,y) for x,y in zip(canonical,converted)];joint=max(joint,J.full(raw))
   assert canonical is not None;joint=max(joint,J.full(canonical));u=max(1-x for x in canonical)
   n=8*2**i;tau=2*beta*2**i
   assert s['cycle']==s['completed_cycles_after_seed']==i and s['n']==n and F(s['beta'])==tau
   assert canonical==list(map(F,s['canonical'])) and joint==F(s['joint']) and u==F(s['u'])
   assert (raw is None and s['raw'] is None) or raw==list(map(F,s['raw']))
   ca,cm=labels(n,tau,'xyt');ra,rm=labels(n,tau,'txy');assert cm==rm
   assert s['canonical_edge_labels']==ca and s['raw_edge_labels']==(ra if raw is not None else None) and s['physical_base']==[n,n,str(tau)]
   w=r['windows'][i];thermal,detail=J.window(canonical,joint)
   assert w['n']==n and w['through']==2*n and F(w['beta'])==tau and F(w['joint_lower'])==joint
   assert F(w['thermal_lower'])==thermal and w['details']==detail and F(1,2)<thermal<1
   gap=F(w['gap_lower']);assert gap>0 and M.exponential(tau*gap)[1]*(1-thermal)<thermal
   required=i<len(r['states'])-1;assert w['included_in_final_minimum']==required
   states.append(dict(cycle=i,n=n,through=2*n,beta=str(tau),u=str(u),window_gap=str(gap),window_gap_display=float(gap),required=required,joint_product_same_physical_base=True))
   if required:
    assert u>F(1,500);nxt,args=J.canonical_next(canonical,joint);assert args==list(map(F,s['canonical_update_arguments']))
    raw=J.advance(raw);canonical=nxt;joint=J.full(nxt) if nxt is not None else F(0)
   else:assert 0<u<=F(1,500)
  assert len(r['windows'])==len(states)
  boot=r['bootstrap'];last=r['states'][-1];n=last['n'];tau=F(last['beta'])
  assert boot['rounds']==0 and boot['updates']==[] and boot['status']=='accepted_analytic_scalar_certificate'
  assert boot['input']==dict(A_lower=last['canonical'][0],B_lower=last['canonical'][1],C_lower=last['canonical'][2],n=n,m=n,beta=str(tau))
  defects=[-J.down(-(1-x),80) for x in canonical];u=max(defects)
  assert defects==list(map(F,boot['defects'])) and u==F(boot['u']) and 0<u<=F(1,500)
  assert boot['n']==boot['m']==n and F(boot['beta'])==tau
  asym=F(boot['uniform_square_gap_lower']);witness=M.exponential(tau*asym)[1]*32*u;assert asym>0 and witness<1
  ub=F(1,500);assert 49/(2*(1-7*ub)**2)<32 and 32*ub<1 and 20/(1-20*ub)<32 and 5*ub<=F(1,100)
  cursor=8;intervals=[]
  for s in states[:-1]:assert s['n']==cursor;cursor=s['through'];intervals.append([s['n'],s['through']])
  assert cursor==n and F(r['short_L2_through_L7_gap'])==short
  c=r['coverage'];assert c==dict(short_integer_sides=[2,7],first_dyadic_window_starts=8,all_early_windows=intervals,asymptotic_all_integer_sides_from=n,terminal_physical_beta=str(tau),no_missing_early_window=True)
  final=min([short,asym]+[F(s['window_gap']) for s in states[:-1]])
  assert final==F(r['all_integer_L_ge2_gap'])==F(candidate['all_integer_L_ge2_gap']) and float(final)==r['all_integer_gap_display']==candidate['gap_display']
  result.append(dict(variant=variant,g='1/10',beta_initial=str(beta),one_retained_numerator_state=True,largest_numerator_upper=str(upper),smaller_denominator_changes_exactly_checked=True,saved_initial_ratios=list(map(str,saved)),independent_initial_ratios=list(map(str,independent)),asymptotic_onset=n,asymptotic_beta=str(tau),asymptotic_gap=str(asym),asymptotic_positive_exponential_witness=str(witness),short_gap=str(short),all_integer_L_ge2_gap=str(final),gap_display=float(final),windows=states,complete_integer_cover=True))
  print('PASS g=.10',variant,'gap',float(final),'onset',n,'required windows',len(states)-1,flush=True)
 return result


if __name__=='__main__':
 start=time.monotonic();out=replay(short_sizes());(OUT/'scalar_result.json').write_text(json.dumps(dict(status='PASS_g010_all_integer_certificate',results=out,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
