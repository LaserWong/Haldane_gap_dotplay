import os,sys,json,hashlib,resource
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
p=BAND/'frontier_g007_g010/g1d10/block1_8x4_g1d10.json';q=BAND/'third_moment_exact/geometry_8x4_origin.json';gr,geom=[json.loads(x.read_text()) for x in [p,q]]
phys=json.loads((HERE/'physical_result.json').read_text());trial=json.loads((HERE/'ground_8x4_trial.json').read_text());G,K,_=build(gr,geom);d=15;n=14;t=F(1,20);c=np.array(trial['coefficients'],dtype=object);assert trial['selected_basis_indices']==list(range(43))
A=K*F(1,gr['integer_matrix_denominator']);gb=G[:d,:d];ff,ss,vv,ww,xx,yy,zz=[np.array(geom[k],dtype=object) for k in ['F','S','V','W','X','Y','Z']]
z=np.zeros((d,n),dtype=object);nq=[0]+[2]*n
Qb=np.array([[gb[i,j]*nq[j] for j in range(d)] for i in range(d)],dtype=object);Qb2=2*Qb
Q=np.block([[Qb,z,z],[z.T,4*ff,4*ss],[z.T,4*ss.T,4*vv+6*ww]])
Q2=np.block([[Qb2,z,z],[z.T,16*ff,16*ss],[z.T,16*ss.T,16*vv+36*ww]])
Ab=(A[:d,:d]-Qb)/t;QAb=np.array([[(nq[i]+nq[j])*Ab[i,j] for j in range(d)] for i in range(d)],dtype=object)
fe=np.vstack([np.zeros((1,n),dtype=object),ff]);se=np.vstack([np.zeros((1,n),dtype=object),ss])
QA=np.block([[QAb,6*fe,6*se],[6*fe.T,8*ss,8*vv+10*ww],[6*se.T,8*vv+10*ww,8*xx+10*(yy+yy.T)+12*zz]])
assert np.array_equal(QA,QA.T)
norm=F(c@G@c);q1=F(c@Q@c);a1=(F(c@A@c)-q1)/t;q2=F(c@Q2@c);qa=F(c@QA@c);a2=(F(phys['exact_second_moment'])*norm-q2-t*qa)/t**2
assert a2>=0
rho=[q1/norm,a1/(2*norm)];mu2=[q2/norm,qa/(2*norm),a2/(4*norm)];var=[mu2[0]-rho[0]**2,mu2[1]-2*rho[0]*rho[1],mu2[2]-rho[1]**2]
g=F(1,10);assert sum(v*g**i for i,v in enumerate(rho))==F(phys['shifted_rayleigh']);assert sum(v*g**i for i,v in enumerate(var))==F(phys['exact_variance'])
out=dict(status='exact_fixed_vector_coupling_polynomials_pending_independent_review_no_interval_claim',shape='8x4',fixed_vector_source='ground_8x4_trial.json',hamiltonian='Hprime(g)=Q+(g/2)A',normalization='same reduced matching metric as physical point seal',norm=str(norm),unnormalized_expectations=dict(Q=str(q1),A=str(a1),Q2=str(q2),QA_plus_AQ=str(qa),A2=str(a2)),rayleigh_coefficients_in_g=list(map(str,rho)),full_second_moment_coefficients_in_g=list(map(str,mu2)),full_variance_coefficients_in_g=list(map(str,var)),exact_point_reproduced=True,physical_seal_sha256=hashlib.sha256((HERE/'PHYSICAL_MANIFEST.json').read_bytes()).hexdigest())
(HERE/'fixed_vector_coupling_polynomials.json').write_text(json.dumps(out,indent=2)+'\n');print('Exact affine mean/quadratic full second moment and variance exported; no interval claim.')
