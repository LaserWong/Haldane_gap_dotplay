import os,sys,json,hashlib,resource
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
cpus=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in cpus else min(cpus)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
HERE=Path(__file__).resolve().parent;RES=HERE.parent;BAND=RES/'low_band'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['PHYSICAL_MANIFEST.json','SCALAR_MANIFEST.json','POLYNOMIAL_MANIFEST.json']:
 for p,h in load(HERE/name)['files'].items():assert sha(HERE/p)==h,(name,p)
for p,h in load(HERE/'PHYSICAL_INPUT_SHA256.json').items():assert sha(RES/p)==h,p
if len(sys.argv)>1:
 new=load(Path(sys.argv[1]));old=load(HERE/'residual_8x4_origin.json')
 for k in ['Tpsi_q4_norm','Tpsi_q6_norm','CM_norm','commutator_expectation','P_norm','T_norm','q8_creation_norm','Tpsi_q6_norm_on_M_zero_supports','T_norm_on_M_zero_supports']:assert new[k]==old[k],k
import numpy as np
sys.path.insert(0,str(BAND/'third_moment_exact'))
from enlarged_numerator import build
G,K,_=build(load(BAND/'frontier_g007_g010/g1d10/block1_8x4_g1d10.json'),load(BAND/'third_moment_exact/geometry_8x4_origin.json'))
r=load(HERE/'physical_result.json');tr=load(HERE/'ground_8x4_trial.json');c=np.array(tr['coefficients'],dtype=object);norm=F(c@G@c);rho=F(c@K@c)/40/norm;assert norm==F(r['exact_norm']) and rho==F(r['shifted_rayleigh'])
low=[F(K[i,:]@c)**2/F(G[i,i]) for i in range(15)];assert low[0]==F(r['Tpsi_sector_norms']['0']) and sum(low[1:])==F(r['Tpsi_sector_norms']['2'])
variance=sum(map(F,r['Tpsi_sector_norms'].values()))/1600/norm-rho*rho;assert variance==F(r['exact_variance']);assert rho-variance/(F(r['cutoff'])-rho)==F(r['ground_lower'])
sys.path.insert(0,str(BAND/'frontier_g009'))
import scan_joint as S
can=load(HERE/'scalar/candidate.json');ex=can['exact_attempts'][0];recs=[load(HERE/'scalar'/f'input_{s}.json') for s in ['4x4','8x4','8x8']];short=F(load(HERE/'scalar/short_L2_through_L7.json')['gap_lower'])
replay=S.exact_record(recs,F(ex['beta_initial']),'txy',short);assert replay['accepted'] and replay['all_integer_L_ge2_gap']==ex['all_integer_L_ge2_gap']
for a,b in zip(replay['windows'],ex['windows']):assert a['gap_lower']==b['gap_lower'] and a['n']==b['n']
print('All seals, exact physical assembly, and actual all-size scalar replay pass.')
