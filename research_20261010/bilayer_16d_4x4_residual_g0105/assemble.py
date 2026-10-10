import sys,os,json,time,resource
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;RES=HERE.parent
import math
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
g=F(21,200);tr=json.load(open(HERE/'trial.json'));raw=json.load(open(Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'raw_residual.json'));assert raw['N']==16 and raw['fixed_origin'] and not raw['partial'] and raw['q4_processed']==455 and raw['q6_processed']==3003
old=json.load(open(RES/'low_band/third_moment_exact/enlarged_4x4_g9d100.json'));geo=json.load(open(RES/'low_band/third_moment_exact/geometry_4x4_origin.json'));n=geo['pair_orbits'];b=n+1;G=old['gram'];rank=len(G);assert rank==16
K0=[[F(0) for _ in range(rank)] for _ in range(rank)]
for i in range(b):
 for j in range(b):K0[i][j]=G[i][j]*(0 if j==0 else 2)
for i in range(n):
 for j in range(n):
  K0[b+i][b+j]=4*geo['F'][i][j];K0[b+i][b+n+j]=4*geo['S'][i][j];K0[b+n+j][b+i]=4*geo['S'][i][j];K0[b+n+i][b+n+j]=4*geo['V'][i][j]+6*geo['W'][i][j]
K=[[K0[i][j]+g/F(old['coupling'])*(F(old['shifted_H_numerator'][i][j],old['integer_matrix_denominator'])-K0[i][j]) for j in range(rank)] for i in range(rank)]
d=400;h=21;c=tr['trial']['integer_coefficients'];norm=sum(F(c[i]*G[i][j]*c[j]) for i in range(rank) for j in range(rank));rho=sum(c[i]*K[i][j]*c[j] for i in range(rank) for j in range(rank))/norm;assert norm==F(tr['trial']['integer_metric_norm']) and rho==F(tr['candidate_shifted_rayleigh'])
KI=[[d*x for x in row] for row in K];assert all(F(v).denominator==1 for row in KI for v in row)
def reference(q):
 x=1-4*g;D=10**60;k=math.isqrt(x.numerator*D*D//x.denominator);root=F(k,D);assert root*root<=x<(root+F(1,D))**2
 return 6*(2*g-1)+(6+q)*root
low=[]
for i in range(6):
 x=sum(KI[i][j]*c[j] for j in range(rank));low.append(x*x/F(G[i][i]))
q0,q2=low[0],sum(low[1:]);q4=F(raw['Tpsi_q4_norm']);q6=F(raw['Tpsi_q6_norm']);q8=h*h*F(raw['q8_creation_norm']);assert F(raw['q8_creation_norm'])==F(raw['CM_norm'])+F(raw['commutator_expectation'])
m2=(q0+q2+q4+q6+q8)/d**2/norm;var=m2-rho*rho;assert var>=0;a=reference(2);a1=reference(1);assert rho<a1<a;ell=rho-var/(a-rho);budget=F(tr['residual_squared_budget'])
r=dict(status='new_physical_complete_residual_candidate_pending_independent_review',g=str(g),geometry=[4,4],search_dimension=16,retained_ground_states=1,full_Hilbert_dimension=str(2**32),integer_denominator=d,integer_A_coefficient=h,norm=str(norm),shifted_Rayleigh=str(rho),second_moment=str(m2),complete_variance=str(var),variance_display=float(var),sector_Tint_norms={str(q):str(v) for q,v in [(0,q0),(2,q2),(4,q4),(6,q6),(8,q8)]},global_first_excited_lower=str(a1),even_sector_cutoff=str(a),ground_lower=str(ell),ground_lower_display=float(ell),target_ground_lower=tr['target_ground_lower'],target_variance_budget=str(budget),target_met=var<=budget,full_q8_obligation_met=True,contraction_seconds=raw['seconds'],peak_rss_kib=raw['peak_rss_kib'])
(Path(sys.argv[2]) if len(sys.argv)>2 else HERE/'physical_result_check.json').write_text(json.dumps(r,indent=2)+'\n');print({k:r[k] for k in ['variance_display','ground_lower_display','target_met','contraction_seconds','peak_rss_kib']})
