import os,sys,resource,json,hashlib
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
cpus=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in cpus else min(cpus)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
import numpy as np
HERE=Path(__file__).resolve().parent;RES=HERE.parent;BAND=RES/'low_band'
sys.path.insert(0,str(BAND/'third_moment_exact'))
from enlarged_numerator import build

gp=BAND/'frontier_g007_g010/g1d10/block1_8x4_g1d10.json';gm=BAND/'third_moment_exact/geometry_8x4_origin.json';pp=BAND/'combined_ground_bounds/combined/patch_8x4_g1d10.json'
gr,geom,patch=[json.loads(p.read_text()) for p in [gp,gm,pp]]
trial=json.loads((HERE/'ground_8x4_trial.json').read_text());raw=json.loads((HERE/'residual_8x4_origin.json').read_text());assert not raw['partial'] and raw['fixed_origin'] and raw['q6_processed']==169911 and raw['q4_processed']==4495
G,K,_=build(gr,geom);ids=trial['selected_basis_indices'];G=G[np.ix_(ids,ids)];K=K[np.ix_(ids,ids)];c=np.array(trial['coefficients'],dtype=object);d=gr['integer_matrix_denominator'];h=F(gr['coupling'])*d/2;assert h==2
norm=F(c@G@c);rho=F(c@K@c)/d/norm;assert rho==F(trial['rayleigh']) and norm==F(trial['norm'])
low=[]
for i in range(15):
 k=F(K[i,:]@c);low.append(k*k/F(G[i,i]))
q0,q2=low[0],sum(low[1:]);q4=F(raw['Tpsi_q4_norm']);q6=F(raw['Tpsi_q6_norm']);q8=h*h*F(raw['q8_creation_norm']);assert F(raw['q8_creation_norm'])==F(raw['CM_norm'])+F(raw['commutator_expectation'])
m2=(q0+q2+q4+q6+q8)/d**2/norm;variance=m2-rho*rho;assert variance>=0
a=F(patch['global_lambda_kplus1_lower']);assert rho<F(patch['all_excited_global_lower'])<a and max(map(F,patch['blocks'][1]['eigen_upper']))<a
ell=rho-variance/(a-rho);assert ell<rho<a and ell>F(patch['blocks'][0]['eigen_lower'][0])
record=dict(status='exact_complete_residual_candidate_pending_independent_review',g='1/10',shape='8x4',normalization='Reduced matching metric; common factor 2**N removed. T_int=40 Hprime.',trial_dimension=43,retained_ground_states=1,full_hilbert_dimension=str(2**64),integer_denominator=d,exact_norm=str(norm),shifted_rayleigh=str(rho),shifted_rayleigh_display=float(rho),Tpsi_sector_norms={str(q):str(v) for q,v in [(0,q0),(2,q2),(4,q4),(6,q6),(8,q8)]},exact_second_moment=str(m2),exact_variance=str(variance),variance_display=float(variance),cutoff=str(a),ground_lower=str(ell),ground_lower_display=float(ell),previous_ground_lower=patch['blocks'][0]['eigen_lower'][0],improvement_display=float(ell-F(patch['blocks'][0]['eigen_lower'][0])),conditional_budget_from_assessment=trial['residual_squared_budget'],conditional_budget_met=variance<F(trial['residual_squared_budget']),no_q8_state_enumerated=True,full_residual_q8_norm_via_exact_hardcore_commutator=True,source_sha256={str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [gp,gm,pp]})
(HERE/'physical_result.json').write_text(json.dumps(record,indent=2)+'\n')
patch['blocks'][0]['eigen_lower']=[str(ell)];patch['complete_residual_source']='physical_result.json';patch['status']='exact_complete_residual_ground_candidate_pending_independent_review'
(HERE/'patch_8x4_g1d10.json').write_text(json.dumps(patch,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['shifted_rayleigh_display','variance_display','ground_lower_display','improvement_display','conditional_budget_met']},indent=2))
