"""Temperature-first 1D producer. All statements await independent review.
Reuses saved integer trials; never calls a many-body eigensolver.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,resource,time,hashlib,importlib.util
from pathlib import Path
from fractions import Fraction as F
resource.setrlimit(resource.RLIMIT_AS,(1500*1024**2,1500*1024**2))
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];BASE=OUT.parent/'chain_frontier'
sys.path[:0]=[str(ROOT/'seed_size/code'),str(ROOT/'low_energy'),str(ROOT/'original/Haldane_extensions/code')]
from certified_core import exp_bounds,G,up
from bootstrap_scalar import replay
from local_relative_bound import optimize_bound
from dimer_subspace import dimer_local
import numpy as np
spec=importlib.util.spec_from_file_location('window',OUT.parent/'root_review/finite_window_2d.py');window=importlib.util.module_from_spec(spec);spec.loader.exec_module(window)

def down(x):return F(x.numerator*10**12//x.denominator,10**12)
def q_upper(r,beta):
 a=F(r['relative_form_bound']['alpha']);B=F(r['relative_form_bound']['B']);N=r['N_dimers']
 z=1+3*exp_bounds(-beta*a)[1]+5*exp_bounds(-3*beta*a)[1]
 tail=up(exp_bounds(-beta*(F(r['E00'])-B-F(r['ground_upper'])))[1]*(z**N-1))
 return up(exp_bounds(beta*(F(r['ground_upper'])-F(r['ground_lower'])))[1]+tail)

def cycle(small,large,beta):
 # This function consumes ONLY one largest-input quantity: its Rayleigh quotient.
 rho8=F(large['exact_rayleigh']);rho4=F(small['ground_upper']);shift=rho8-2*rho4
 q1=q_upper(small,beta);q2=q_upper(small,2*beta)
 L=exp_bounds(-2*beta*shift)[0]
 J=down(L/q1**4);C=down(L/q2**2)
 a=down(G(J)) if J>0 else F(-1)
 b=down(G(C*C*a)) if a>0 else F(-1)
 out=dict(beta=str(beta),small_Q_beta_upper=str(q1),small_Q_2beta_upper=str(q2),Rayleigh_shift=str(shift),J_lower=str(J),C_lower=str(C),time_first=[str(a),str(b)])
 if b<=0:out['status']='nonpositive_first_cycle';return out
 root=window.sqrt_lower(b);S=down(a*root);T=down(a*a*b)
 boot=replay(str(S),str(T),8,str(2*beta))
 out.update(canonical_S=str(S),canonical_T=str(T),sqrt_b_lower=str(root),bootstrap=boot)
 if not boot['status'].startswith('accepted'):out['status']='scalar_rejected';return out
 nn=8;bb=2*beta;wins=[]
 states=[(S,T)]+[(1-F(x['p_upper']),1-F(x['q_upper'])) for x in boot['updates']]
 for SS,TT in states:
  if nn>=boot['final_n']:break
  cc,detail=window.interpolate_1d(SS,TT);gap=window.gap(cc,bb)
  wins.append(dict(cells=[nn,2*nn],beta=str(bb),S=str(SS),T=str(TT),thermal_lower=str(cc),gap_lower=str(gap),detail=detail))
  nn*=2;bb*=2
 gap=min([F(boot['conditional_gap_lower_rational'])]+[F(x['gap_lower']) for x in wins])
 out.update(status='exact_scalar_and_M_ge8_candidate',windows=wins,M_ge8_gap=str(gap),M_ge8_gap_display=float(gap))
 return out

def affine_saved_rayleigh(path):
 z=np.load(path,allow_pickle=False);basis=[tuple(map(int,x)) for x in z['basis']];v=list(map(int,z['vector']));N=len(basis[0]);lookup=dict(zip(basis,v))
 labels,weights,kernels=dimer_local(F(1));metric={s:math.prod(weights[x] for x in s) for s in basis};norm=sum(metric[s]*x*x for s,x in zip(basis,v))
 h0=sum(metric[s]*x*x*(-2*N+sum(labels[d][2] for d in s)) for s,x in zip(basis,v));weak=F(0)
 for s,x in zip(basis,v):
  for j in range(N):
   i=(j-1)%N
   for a,b,c in kernels[1,0][9*s[i]+s[j]]:
    t=list(s);t[i]=a;t[j]=b;t=tuple(t)
    if t in lookup:weak+=metric[t]*lookup[t]*c*x
 return dict(source=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),N=N,dimension=len(v),norm=str(norm),H0_expectation=str(h0/norm),weak_unit_expectation=str(weak/norm))

def short_bridge(g,affine):
 # One N=7 local comparison applies simultaneously to 2<=M<=7.
 b=optimize_bound(F(1),g,'chain',7);alpha=F(b['alpha']);unitb=F(b['local_certificate']['b']);rows=[]
 for M in range(2,8):
  rho=-2*F(M);source='singlet product';source_sha=None
  if M==7:rho=F(affine['H0_expectation'])+g*F(affine['weak_unit_expectation']);source=affine['source'];source_sha=affine['sha256']
  # Reuse the existing M=6 optimized trial at g=.175 if it helps its short bridge.
  if M==6 and g==F(7,40):
   rr=json.loads((BASE/'chain_s1_M6_g7d40_depth3_ground.json').read_text());rho=min(rho,F(rr['exact_rayleigh']));source=str((BASE/'chain_s1_M6_g7d40_depth3_ground.json').relative_to(ROOT));source_sha=hashlib.sha256((BASE/'chain_s1_M6_g7d40_depth3_ground.json').read_bytes()).hexdigest()
  cut=-2*M+alpha-M*unitb;gap=cut-rho
  rows.append(dict(M=M,cutoff_lower=str(cut),trial_rayleigh=str(rho),trial_source=source,trial_source_sha256=source_sha,gap_lower=str(gap)))
 return dict(local_comparison=b,affine_M7_trial=affine,rows=rows,gap_lower=str(min(F(x['gap_lower']) for x in rows)))

def main():
 t=time.monotonic();affine=affine_saved_rayleigh(BASE/'chain_s1_M7_g129d800_depth2_trial.npz')
 orig=json.loads((BASE/'chain_s1_M7_g129d800_depth2_ground.json').read_text())
 assert F(affine['H0_expectation'])+F(129,800)*F(affine['weak_unit_expectation'])==F(orig['exact_rayleigh'])
 outputs=[]
 for tag,beta in [('323d2000','39/2'),('13d80','81/4'),('7d40','23'),('1d5','23')]:
  source=BASE/f'chain_sparse_s1_g{tag}_n4_depth4.json';r=json.loads(source.read_text());small,big=r['ground_certificates'];reduced={'exact_rayleigh':big['exact_rayleigh']}
  # Bounded exact local beta refinement around the float proposal.
  rows=[cycle(small,reduced,F(beta)+F(i,4)) for i in range(-4,5)]
  poison=dict(reduced,ground_lower='POISON',ground_upper='POISON',exact_residual_squared='POISON',second_eigenvalue_lower='POISON',relative_form_bound='POISON',status='REJECTED',N_dimers='POISON')
  assert cycle(small,reduced,F(beta))==cycle(small,poison,F(beta))==cycle(small,big,F(beta))
  accepted=[x for x in rows if x.get('M_ge8_gap')]
  bridge=short_bridge(F(r['g']),affine) if accepted else None
  for x in accepted:x['all_M_ge2_gap']=str(min(F(bridge['gap_lower']),F(x['M_ge8_gap'])))
  best=max(accepted,key=lambda x:F(x['all_M_ge2_gap'])) if accepted else None
  out=dict(status='exact_arithmetic_producer_candidate_REQUIRES_INDEPENDENT_AUDIT',g=r['g'],source=str(source.relative_to(ROOT)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),small_input=small,large_input=reduced,large_trial_path=str((BASE/big['trial_artifact']).relative_to(ROOT)),large_trial_dimension=big['trial_subspace_dimension'],large_full_dimension=big['full_dimension'],largest_dependency_test={'minimal_keys':['exact_rayleigh'],'full_record_equals_minimal':True,'poisoned_other_fields_equal_minimal':True},large_input_contract='Rayleigh-only. No large residual, ground lower, isolation, local comparison, or tail consumed.',rows=rows,short_bridge=bridge,best=best)
  (OUT/f'candidate_g{tag}.json').write_text(json.dumps(out,indent=2)+'\n');outputs.append(dict(g=r['g'],best=None if best is None else {'beta':best['beta'],'all_M_ge2_gap':best['all_M_ge2_gap'],'display':float(F(best['all_M_ge2_gap'])),'asymptotic_from':best['bootstrap']['final_n']},short_gap=None if bridge is None else bridge['gap_lower']))
  print(outputs[-1],flush=True)
 summary=dict(status='CANDIDATES_PENDING_INDEPENDENT_AUDIT',results=outputs,seconds=time.monotonic()-t,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,affinity=sorted(os.sched_getaffinity(0)),BLAS_threads=1,address_space_limit_bytes=1500*1024**2)
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(summary,flush=True)
if __name__=='__main__':main()
