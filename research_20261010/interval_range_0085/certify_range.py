"""Continuous ordinary-bilayer candidates with auxiliary Temple and implicit filtering.
Existing exact G/K/J matrices only; no higher moments or physical vector expansion.
Largest numerator retains one trial contribution and now requires full H2 input.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
import sys;sys.dont_write_bytecode=True
import json,math,hashlib,argparse,time,resource
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;R=HERE.parent;ROOT=R.parent
sys.path[:0]=[str(ROOT/'two_d_theory'),str(R/'root_review'),str(R/'low_band_review')]
from three_purity_certificate import replay,down
from fast_exp import exp_interval
from finite_window_2d import interpolate_2d,gap
try:os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
except AttributeError:pass
resource.setrlimit(resource.RLIMIT_AS,(1024*1024**2,1024*1024**2))
sys.path.insert(0,str(R/'variational_numerator_filter'))
from filter_rayleigh import compressed_upper
sys.path.insert(0,str(R/'low_band'/'joint_trace_bootstrap'))
import joint_scalar as JS
MODELS=[]
AUX=R/'low_band'/'ground_moment_auxiliary'
for nx,ny in ((4,4),(8,4),(8,8)):
 raw=json.loads((AUX/f'matrix_polynomial_{nx}x{ny}.json').read_text())
 rec=dict(geometry=[nx,ny],N=nx*ny,trial_dimension=raw['trial_dimension'],G=np.array([[int(x) for x in row] for row in raw['gram']],dtype=object))
 for new,old in [('first_moment_coefficients','shifted_A_coefficients'),('full_second_moment_coefficients','full_shifted_B_coefficients')]:
  rec[new]=[np.array([[F(x) for x in row] for row in a],dtype=object) for a in raw[old]]
 MODELS.append(rec)
def poly(c,g):return sum(x*g**k for k,x in enumerate(c))
def st(cs):return list(map(str,cs))
def sqrt_down(x,digits=60):
 D=10**digits;k=math.isqrt(x.numerator*D**2//x.denominator)
 lo=F(k,D);assert lo*lo<=x<(lo+F(1,D))**2;return lo
@lru_cache(None)
def reference(g,N,q):
 # All main patches have no parallel edges, S=sum w_e^2=2N.
 C=F(3*N,8);return C*(2*g-1)+(C+q)*sqrt_down(1-4*g)
def optimized_vector(model,g):
 A=sum(float(g)**k*np.array(M,dtype=float) for k,M in enumerate(model['first_moment_coefficients']))
 G=np.array(model['G'],dtype=float);scale=np.sqrt(np.diag(G));sG=G/scale[:,None]/scale[None,:];sA=A/scale[:,None]/scale[None,:]
 vals,U=eigh(sA,sG);v=U[:,0]/scale;v/=max(abs(v));return [int(round(x*2**48)) for x in v]
def trial(model,g,v=None):
 v=optimized_vector(model,g) if v is None else v;c=np.array(v,dtype=object);norm=int(c@model['G']@c);assert norm>0
 rho=[F(c@A@c,norm) for A in model['first_moment_coefficients']]
 out=dict(geometry=model['geometry'],N=model['N'],trial_dimension=model['trial_dimension'],center=str(g),integer_coefficients=v,integer_metric_norm=str(norm),rayleigh_coefficients=st(rho))
 if 'full_second_moment_coefficients' in model:
  h2=[F(c@A@c,norm) for A in model['full_second_moment_coefficients']]
  variance=[h2[0]-rho[0]**2,h2[1]-2*rho[0]*rho[1],h2[2]-rho[1]**2]
  assert variance[0]>=0 and variance[2]>=0 and 4*variance[0]*variance[2]>=variance[1]**2
  out.update(full_second_moment_coefficients=st(h2),full_residual_squared_coefficients=st(variance))
 return out

def quadratic_bounds(cs,lo,hi):
 values=[poly(cs,x) for x in (lo,hi)]
 if cs[2]:
  vertex=-cs[1]/(2*cs[2])
  if lo<=vertex<=hi:values.append(poly(cs,vertex))
 return min(values),max(values)

def auxiliary_vector(model,center):
 nx,ny=model['geometry'];g=min(map(F,('7/100','2/25')),key=lambda x:abs(x-center))
 return json.loads((AUX/f'auxiliary_{nx}x{ny}_g{g}.json'.replace('/','d')).read_text())['coefficients']

def interval_data(lo,hi,vectors=None):
 assert 0<=lo<=hi<F(1,4);center=(lo+hi)/2
 if vectors is None:vectors=[auxiliary_vector(m,center) for m in MODELS[:2]]+[optimized_vector(MODELS[2],center)]
 trials=[trial(m,center,vectors[i]) for i,m in enumerate(MODELS)];patches=[]
 for tr in trials[:2]:
  N=tr['N'];rho=list(map(F,tr['rayleigh_coefficients']));var=list(map(F,tr['full_residual_squared_coefficients']))
  varends=[poly(var,g) for g in (lo,hi)];vmax=max(varends);assert min(varends)>=0
  ends=[[reference(g,N,q)-poly(rho,g) for g in (lo,hi)] for q in range(1,N+1)]
  lower=[min(v) for v in ends];assert lower[0]>0 and lower[1]>0
  width=vmax/lower[1]
  patches.append(dict(**tr,residual_endpoint_values=st(varends),residual_squared_max=str(vmax),reference_minus_rayleigh_endpoint_lowers=[st(v) for v in ends],reference_minus_rayleigh_uniform_lowers=st(lower),ground_identification_margin=str(lower[0]),even_Temple_denominator=str(lower[1]),uniform_Temple_width=str(width)))
 tr=trials[2];rho=list(map(F,tr['rayleigh_coefficients']));var=list(map(F,tr['full_residual_squared_coefficients']))
 vmin,vmax=quadratic_bounds(var,lo,hi);assert vmin>=0
 comp=compressed_upper(8,8,hi);Rmax=F(comp['compressed_H_upper']);Cmax=Rmax-min(poly(rho,g) for g in (lo,hi));assert Cmax>0
 # t fixed over the interval. v/(1+t²v) is increasing for v>=0.
 t=1/Cmax;gain=(2*t-Cmax*t*t)*vmin/(1+t*t*vmin);assert gain>=0
 filt=dict(compressed_upper_at_high=comp,residual_squared_min=str(vmin),residual_squared_max=str(vmax),Cmax=str(Cmax),fixed_t=str(t),uniform_improvement=str(gain),filtered_rayleigh_upper_coefficients=st([rho[0]-gain,rho[1]]),original_space_plus_residual_dimension_upper=tr['trial_dimension']+1,filtered_trial_max_triplet_number=6,retained_ground_contributions=1)
 rr=[list(map(F,x['rayleigh_coefficients'])) for x in trials];rr[2][0]-=gain;joint={}
 for name,w in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
  cs=[sum(w[i]*rr[i][k] for i in range(3)) for k in range(2)];ends=[poly(cs,g) for g in (lo,hi)]
  joint[name]=dict(weights=w,affine_coefficients=st(cs),endpoint_values=st(ends),uniform_lower=str(min(ends)))
 return dict(coupling_interval=st((lo,hi)),fixed_vector_center=str(center),denominator_patches=patches,largest_base_trial=trials[2],largest_interval_filter=filt,correlated_energy_combinations=joint)

def G(x):return 1-(1-x)**2/(2*x*x)
def transport(a,b,c,sqrt):return [a*sqrt(b),a*a*b*sqrt(c),a**4*b*b*c]
def upper_float(p,b):
 N=p['N'];d=float(F(p['uniform_Temple_width']))
 return math.exp(b*d)+sum(math.comb(3*N+q-1,q)*math.exp(-b*float(F(en))) for q,en in enumerate(p['reference_minus_rayleigh_uniform_lowers'],1))
def stages_float(data,b):
 a,m=data['denominator_patches'];u0,u1,u2=upper_float(a,b),upper_float(a,2*b),upper_float(m,2*b)
 e={k:float(F(r['uniform_lower'])) for k,r in data['correlated_energy_combinations'].items()}
 j1=math.exp(b*e['J1'])/u0**8;j2=math.exp(b*e['J2'])/u1**8;c0=math.exp(b*e['C0'])/u2**2
 if min(j1,j2,c0)<=0:return None
 a=G(j1)
 if a<=0:return None
 bb=G(j2*a)
 if bb<=0:return None
 c=G(c0**4*a*a*bb)
 if c<=0:return None
 return [a,bb,c]
def advance_coupled(canonical,permuted,joint,exact):
 nxt,args=JS.canonical_advance(canonical,joint,exact,digits=18)
 per=JS.plain_advance(permuted,exact,digits=18) if permuted is not None else None
 trans=transport(*per,sqrt_down if exact else math.sqrt) if per is not None else None
 if trans is not None and exact:trans=[down(x,18) for x in trans]
 if nxt is None and trans is None:return None,None,None,args
 can=trans if nxt is None else nxt if trans is None else [max(x,y) for x,y in zip(nxt,trans)]
 kk=max(JS.full_product(can),JS.full_product(per) if per is not None else 0)
 return can,per,down(kk,18) if exact else kk,args

def score(data,b):
 per=stages_float(data,b)
 if per is None:return 1.
 can=transport(*per,math.sqrt);joint=JS.full_product(per)
 for j in range(20):
  u=max(1-x for x in can)
  if u<=.002:return -math.log(1/(32*u))/(b*2**(j+1)) if u>0 else -1
  can,per,joint,args=advance_coupled(can,per,joint,False)
  if can is None:return 1.
 return 1.
def proposal(data):return min((score(data,bi/20),F(bi,20)) for bi in range(100,601))
def upper_exact(p,b):
 N=p['N'];ground=exp_interval(b*F(p['uniform_Temple_width']))[1]
 terms=[math.comb(3*N+q-1,q)*exp_interval(-b*F(e))[1] for q,e in enumerate(p['reference_minus_rayleigh_uniform_lowers'],1)]
 return ground+sum(terms),dict(beta=str(b),normalized_ground_upper=str(ground),normalized_tail_upper=str(sum(terms)),normalized_trace_upper=str(ground+sum(terms)),retained_states=1,reference_q_range=[1,N])
def short_gap(hi):
 dl=sqrt_down(1-4*hi);rows=[]
 for L in range(2,8):
  S=16 if L==2 else 2*L*L;C=F(3*S,16);ell=C*(2*hi-1)+(C+1)*dl;assert ell>0
  rows.append(dict(L=L,N=L*L,edge_square_sum=S,lambda2_shifted_lower=str(ell),ground_Rayleigh_upper='0',gap_lower=str(ell)))
 return min(F(r['gap_lower']) for r in rows),rows

def certify(data,b):
 a,m=data['denominator_patches'];u0,t0=upper_exact(a,b);u1,t1=upper_exact(a,2*b);u2,t2=upper_exact(m,2*b)
 e={k:F(r['uniform_lower']) for k,r in data['correlated_energy_combinations'].items()}
 j1=down(exp_interval(b*e['J1'])[0]/u0**8,18);j2=down(exp_interval(b*e['J2'])[0]/u1**8,18);c0=down(exp_interval(b*e['C0'])[0]/u2**2,18)
 assert all(0<x<=1 for x in (j1,j2,c0))
 aa=down(G(j1),18);bb=down(G(j2*aa),18) if aa>0 else F(-1);cc=down(G(c0**4*aa*aa*bb),18) if bb>0 else F(-1)
 result=dict(**data,status='continuous_g_joint_filtered_auxiliary_candidate_pending_independent_review',beta_initial=str(b),trace_upper_certificates=[t0,t1,t2],J1=str(j1),J2=str(j2),C0=str(c0),permuted_first_purities=st((aa,bb,cc)),accepted=False)
 if min(aa,bb,cc)<=0:return result
 per=[aa,bb,cc];abc=[down(x,18) for x in transport(*per,sqrt_down)];joint=down(JS.full_product(per),18)
 result.update(canonical_first_purities=st(abc),initial_joint_product=str(joint));states=[];windows=[]
 for j in range(64):
  n=8*2**j;beta=2*b*2**j
  assert all(0<x<=1 for x in abc) and 0<joint<=1
  thermal,details=JS.interpolate_2d_joint(*abc,joint);gg=gap(thermal,beta)
  if gg is None or gg<=0:return dict(result,failure='joint finite-window bound not positive',failed_level=j)
  windows.append(dict(n=n,through=2*n,beta=str(beta),thermal_lower=str(thermal),gap_lower=str(gg),details=details))
  state=dict(level=j,n=n,beta=str(beta),canonical=st(abc),permuted=st(per) if per is not None else None,joint_product_lower=str(joint));states.append(state)
  if max(1-x for x in abc)<=F(1,500):
   boot=replay(*abc,n=n,m=n,beta=beta,rounds=64,digits=18)
   assert boot['status']=='accepted_analytic_scalar_certificate'
   break
  abc,per,joint,args=advance_coupled(abc,per,joint,True)
  state['canonical_update_arguments']=st(args)
  if abc is None:return dict(result,failure='both coupled updates failed',failed_level=j)
 else:return dict(result,failure='bounded coupled iteration did not reach certified domain')
 result.update(joint_ladder_states=states,bootstrap=boot)
 short,rows=short_gap(F(data['coupling_interval'][1]));target=min([F(boot['uniform_square_gap_lower']),short]+[F(w['gap_lower']) for w in windows if w['n']<boot['n']])
 result.update(accepted=target>0,finite_windows=windows,short_sizes=rows,all_integer_L_ge2_gap=str(target),all_integer_gap_display=float(target))

 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--lo',default='39/500');ap.add_argument('--hi',default='2/25');ap.add_argument('--step',default='1/1000');ap.add_argument('--min-gap',default='1/500');ap.add_argument('--out',default='coverage');ap.add_argument('--scout',action='store_true');args=ap.parse_args()
 lo,hi,step=map(F,(args.lo,args.hi,args.step));queue=[];x=lo
 while x<hi:y=min(x+step,hi);queue.append((x,y));x=y
 records=[];scouts=[];start=time.monotonic()
 while queue:
  left,right=queue.pop(0);data=interval_data(left,right);value,b=proposal(data)
  if value>=0:
   if right-left<F(1,10000000):raise RuntimeError(('no pointwise ground-only certificate',left,right,value))
   mid=(left+right)/2;queue[:0]=[(left,mid),(mid,right)];continue
  scout=dict(interval=st((left,right)),beta=str(b),score=value);scouts.append(scout)
  if args.scout:print(scout,flush=True);continue
  rec=certify(data,b);assert rec['accepted']
  if F(rec['all_integer_L_ge2_gap'])<F(args.min_gap):
   assert right-left>=F(1,10000000),('requested minimum not established',left,right)
   mid=(left+right)/2;queue[:0]=[(left,mid),(mid,right)];exp_interval.cache_clear();continue
  rec['float_proposal_score']=value;records.append(rec)
  target=HERE/args.out;target.mkdir(exist_ok=True);(target/f'interval_{len(records):03d}.json').write_text(json.dumps(rec,indent=2)+'\n')
  print(st((left,right)),str(b),rec['all_integer_gap_display'],flush=True)
  exp_interval.cache_clear()
 if args.scout:output=dict(scout_only_not_certificate=True,scouts=scouts)
 else:
  assert records and F(records[0]['coupling_interval'][0])==lo and F(records[-1]['coupling_interval'][1])==hi
  assert all(a['coupling_interval'][1]==b['coupling_interval'][0] for a,b in zip(records,records[1:]))
  worst=min(F(r['all_integer_L_ge2_gap']) for r in records)
  output=dict(status='continuous_g_joint_filtered_auxiliary_candidate_pending_independent_review',coupling_interval=st((lo,hi)),closed_intervals=len(records),all_integer_L_ge2_uniform_gap=str(worst),uniform_gap_display=float(worst),intervals=[dict(file=f'{args.out}/interval_{i:03d}.json',coupling_interval=r['coupling_interval'],gap_lower=r['all_integer_L_ge2_gap'],gap_display=r['all_integer_gap_display'],beta_initial=r['beta_initial']) for i,r in enumerate(records,1)],zero_coupling_exact_gap='1',largest_trace_rank=1,denominator_retained_states=[1+int('odd_band' in p)*3*p['N'] for p in records[0]['denominator_patches']],odd_trial_inputs='odd_band' in records[0]['denominator_patches'][0],ground_trial_dimensions=[11,29,29],total_augmented_trial_dimensions=([59,125,30] if 'odd_band' in records[0]['denominator_patches'][0] else [11,29,30]),trial_dimensions=[m['trial_dimension'] for m in MODELS],largest_physical_spins=128,largest_full_dimension=4**64,largest_residual_required=True,maximum_full_residual_geometry=[8,8],filtered_augmented_trial_dimensions=[11,29,30],largest_filtered_trial_max_q=6,new_higher_moments=False,minimum_gap_requested=args.min_gap,runtime_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (HERE/f'{args.out}_summary.json').write_text(json.dumps(output,indent=2)+'\n')
 print('SUMMARY',output.get('closed_intervals'),output.get('uniform_gap_display'),time.monotonic()-start,flush=True)
if __name__=='__main__':main()
