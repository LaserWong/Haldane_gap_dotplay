"""Exact continuous .09-.10 extension; fixed 43D one-state numerator."""
import os,sys
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
from pathlib import Path
HERE=Path(__file__).resolve().parent;R=HERE.parent
sys.path.insert(0,str(R/'interval_range_0085'))
import certify_lowband as L
C=L.C;F=C.F;np=C.np;json=C.json
THIRD=R/'low_band'/'third_moment_exact'
raw=json.loads((THIRD/'enlarged_8x8_g9d100.json').read_text())
geom=json.loads((THIRD/'geometry_8x8_origin.json').read_text())
n=geom['pair_orbits'];d=n+1
G=np.array(raw['gram'],dtype=object);assert raw['selected_basis_indices']==list(range(3*n+1))
K0=np.zeros_like(G);K0[:d,:d]=G[:d,:d]@np.diag([0]+[2]*n)
ff,ss,vv,ww=[np.array(geom[k],dtype=object) for k in ('F','S','V','W')]
K0[d:d+n,d:d+n]=4*ff;K0[d:d+n,d+n:]=4*ss;K0[d+n:,d:d+n]=4*ss.T;K0[d+n:,d+n:]=4*vv+6*ww
K=np.array([[F(x,raw['integer_matrix_denominator']) for x in row] for row in raw['shifted_H_numerator']],dtype=object)
K1=(K-K0)/F(raw['coupling'])
assert np.array_equal(K0,K0.T) and np.array_equal(K1,K1.T)
NUM=dict(geometry=[8,8],N=64,trial_dimension=43,G=G,first_moment_coefficients=[K0,K1])

COMPLETE=R/'bilayer_complete_residual_8x4'
FIXED=json.loads((COMPLETE/'fixed_vector_coupling_polynomials.json').read_text())
WITNESS=json.loads((COMPLETE/'ground_8x4_trial.json').read_text())
allowed=os.sched_getaffinity(0)
# Imported scalar module restricts affinity; recover the requested worker CPU.
try:os.sched_setaffinity(0,{5})
except OSError:pass

def fixed_trial(center,vector):
 assert vector==WITNESS['coefficients']
 rho=list(map(F,FIXED['rayleigh_coefficients_in_g']));h2=list(map(F,FIXED['full_second_moment_coefficients_in_g']));v=list(map(F,FIXED['full_variance_coefficients_in_g']))
 assert F(FIXED['norm'])>0 and v==[h2[0]-rho[0]**2,h2[1]-2*rho[0]*rho[1],h2[2]-rho[1]**2]
 assert v[0]>=0 and v[2]>=0 and 4*v[0]*v[2]>=v[1]**2
 return dict(geometry=[8,4],N=32,trial_dimension=43,center=str(center),integer_coefficients=vector,integer_metric_norm=FIXED['norm'],rayleigh_coefficients=C.st(rho),full_second_moment_coefficients=C.st(h2),full_residual_squared_coefficients=C.st(v),complete_residual_source='bilayer_complete_residual_8x4/fixed_vector_coupling_polynomials.json',max_trial_triplet_number=6,max_full_residual_triplet_number=8)

def base_data(lo,hi,vectors=None):
 assert 0<=lo<=hi<F(1,4);center=(lo+hi)/2
 if vectors is None:vectors=[L.optimized_auxiliary(C.MODELS[0],center),WITNESS['coefficients']]+[C.optimized_vector(NUM,center)]
 trials=[C.trial(C.MODELS[0],center,vectors[0]),fixed_trial(center,vectors[1]),C.trial(NUM,center,vectors[2])];patches=[]
 for tr in trials[:2]:
  N=tr['N'];rho=list(map(F,tr['rayleigh_coefficients']));var=list(map(F,tr['full_residual_squared_coefficients']))
  varends=[C.poly(var,g) for g in (lo,hi)];vmax=max(varends);assert min(varends)>=0
  ends=[[C.reference(g,N,q)-C.poly(rho,g) for g in (lo,hi)] for q in range(1,N+1)]
  lower=[min(v) for v in ends];assert lower[0]>0 and lower[1]>0
  patches.append(dict(**tr,residual_endpoint_values=C.st(varends),residual_squared_max=str(vmax),reference_minus_rayleigh_endpoint_lowers=[C.st(v) for v in ends],reference_minus_rayleigh_uniform_lowers=C.st(lower),ground_identification_margin=str(lower[0]),even_Temple_denominator=str(lower[1]),uniform_Temple_width=str(vmax/lower[1])))
 rr=[list(map(F,t['rayleigh_coefficients'])) for t in trials];joint={}
 for name,w in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
  cs=[sum(w[i]*rr[i][k] for i in range(3)) for k in range(2)];ends=[C.poly(cs,g) for g in (lo,hi)]
  joint[name]=dict(weights=w,affine_coefficients=C.st(cs),endpoint_values=C.st(ends),uniform_lower=str(min(ends)))
 return dict(coupling_interval=C.st((lo,hi)),fixed_vector_center=str(center),denominator_patches=patches,largest_base_trial=trials[2],largest_numerator=dict(retained_states=1,search_dimension=43,max_triplet_number=6,residual_required=False,physical_spins=128,full_dimension=4**64),correlated_energy_combinations=joint)

L.base_interval_data=base_data

def interval_data(lo,hi,vectors=None):
 if vectors is None:
  center=(lo+hi)/2;vectors=[L.optimized_auxiliary(C.MODELS[0],center),WITNESS['coefficients']]+[C.optimized_vector(NUM,center)]
 return L.interval_data(lo,hi,vectors)

C.interval_data=interval_data

original_certify=C.certify
def edges(n,beta,order):
 state=[n,n,F(beta)];result=[]
 for axis in order:
  k={'x':0,'y':1,'t':2}[axis];end=state[:];end[k]*=2
  result.append(dict(axis=axis,base=[state[0],state[1],str(state[2])],endpoint=[end[0],end[1],str(end[2])]))
  state=end
 return result

def certify(data,beta):
 result=original_certify(data,beta)
 for st in result.get('joint_ladder_states',[]):
  n=st['n'];b=F(st['beta']);st['physical_base']=[n,n,str(b)]
  st['canonical_edge_labels']=edges(n,b,'xyt')
  st['permuted_edge_labels']=edges(n,b,'txy') if st['permuted'] is not None else None
  st['joint_product_physical_base']=[n,n,str(b)]
 for w in result.get('finite_windows',[]):w['included_in_final_minimum']=w['n']<result['bootstrap']['n']
 return result
C.certify=certify

def run(lo,hi,step,min_gap,out):
 import time,resource
 start=time.monotonic();queue=[];x=lo
 while x<hi:y=min(x+step,hi);queue.append((x,y));x=y
 records=[];attempts=[];target=HERE/out;target.mkdir(exist_ok=True)
 while queue:
  left,right=queue.pop(0);data=interval_data(left,right);score,b=C.proposal(data)
  row=dict(interval=C.st((left,right)),score=score,beta=str(b));attempts.append(row)
  if score<0:
   rec=C.certify(data,b);row.update(exact_accepted=rec['accepted'],gap=rec.get('all_integer_gap_display'))
  else:rec=None
  if rec is None or not rec['accepted'] or F(rec['all_integer_L_ge2_gap'])<min_gap:
   assert right-left>=F(1,10**7),row
   mid=(left+right)/2;queue[:0]=[(left,mid),(mid,right)];C.exp_interval.cache_clear();continue
  rec['status']='continuous_complete_8x4_residual_candidate_pending_independent_review';rec['float_proposal_score']=score;records.append(rec)
  (target/f'interval_{len(records):03d}.json').write_text(json.dumps(rec,indent=2)+'\n');print(row,flush=True);C.exp_interval.cache_clear()
 assert F(records[0]['coupling_interval'][0])==lo and F(records[-1]['coupling_interval'][1])==hi
 assert all(a['coupling_interval'][1]==b['coupling_interval'][0] for a,b in zip(records,records[1:]))
 summary=dict(status='exact_producer_candidate_pending_independent_review',coupling_interval=C.st((lo,hi)),closed_intervals=len(records),uniform_gap=str(min(F(r['all_integer_L_ge2_gap']) for r in records)),uniform_gap_display=min(r['all_integer_gap_display'] for r in records),intervals=[dict(file=f'{out}/interval_{i:03d}.json',coupling_interval=r['coupling_interval'],gap=r['all_integer_L_ge2_gap']) for i,r in enumerate(records,1)],attempts=attempts,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,largest_retained_states=1,search_dimensions=[11,43,43],denominator_retained_states=[49,97])
 (HERE/f'{out}_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--lo',default='9/100');p.add_argument('--hi',default='1/10');p.add_argument('--step',default='1/1000');p.add_argument('--min-gap',default='1/500');p.add_argument('--out',default='coverage');a=p.parse_args()
 model=dict(geometry=[8,8],basis=raw['basis'],dimension=43,gram=G.tolist(),shifted_A_coefficients=[[[str(x) for x in row] for row in M] for M in (K0,K1)])
 (HERE/'numerator_matrix_polynomial.json').write_text(json.dumps(model,indent=2)+'\n')
 run(F(a.lo),F(a.hi),F(a.step),F(a.min_gap),a.out)
