import os,sys,json,time,hashlib,resource
from pathlib import Path
from fractions import Fraction as F
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;RES=HERE.parent
sys.path.insert(0,str(RES/'bilayer_seed_error_budget'))
from budget import P,C
import numpy as np
os.sched_setaffinity(0,{3});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))

def export(shape,folder):
 p=RES/f'low_band/third_moment_exact/enlarged_{shape}_g9d100.json';q=RES/f'low_band/third_moment_exact/geometry_{shape}_origin.json';old,geo=[json.load(open(x)) for x in (p,q)];G=np.array(old['gram'],dtype=object);n=geo['pair_orbits'];d=n+1;assert len(G)==3*n+1 and old['selected_basis_indices']==list(range(len(G)))
 A=np.array([[F(x,old['integer_matrix_denominator']) for x in row] for row in old['shifted_H_numerator']],dtype=object);t=F(old['coupling'])/2;gb=G[:d,:d];ff,ss,vv,ww,xx,yy,zz=[np.array(geo[k],dtype=object) for k in ['F','S','V','W','X','Y','Z']];z=np.zeros((d,n),dtype=object);nq=[0]+[2]*n
 Qb=np.array([[gb[i,j]*nq[j] for j in range(d)] for i in range(d)],dtype=object);Qb2=2*Qb
 Q=np.block([[Qb,z,z],[z.T,4*ff,4*ss],[z.T,4*ss.T,4*vv+6*ww]])
 Q2=np.block([[Qb2,z,z],[z.T,16*ff,16*ss],[z.T,16*ss.T,16*vv+36*ww]])
 Ab=(A[:d,:d]-Qb)/t;QAb=np.array([[(nq[i]+nq[j])*Ab[i,j] for j in range(d)] for i in range(d)],dtype=object)
 fe=np.vstack([np.zeros((1,n),dtype=object),ff]);se=np.vstack([np.zeros((1,n),dtype=object),ss])
 QA=np.block([[QAb,6*fe,6*se],[6*fe.T,8*ss,8*vv+10*ww],[6*se.T,8*vv+10*ww,8*xx+10*(yy+yy.T)+12*zz]]);assert np.array_equal(QA,QA.T)
 phys=json.load(open(RES/folder/'physical_result.json'));trial=json.load(open(RES/folder/'trial.json'));c=np.array(trial['trial']['integer_coefficients'],dtype=object);norm=F(c@G@c);q1=F(c@Q@c);a1=(F(c@A@c)-q1)/t;q2=F(c@Q2@c);qa=F(c@QA@c);g=F(phys['g']);tp=g/2;a2=(F(phys['second_moment'])*norm-q2-tp*qa)/tp**2;assert a2>=0
 rho=[q1/norm,a1/(2*norm)];m2=[q2/norm,qa/(2*norm),a2/(4*norm)];var=[m2[0]-rho[0]**2,m2[1]-2*rho[0]*rho[1],m2[2]-rho[1]**2]
 assert C.poly(rho,g)==F(phys['shifted_Rayleigh']) and C.poly(var,g)==F(phys['complete_variance']);assert var[0]>=0 and var[2]>=0 and 4*var[0]*var[2]>=var[1]**2
 paths=[p,q,RES/folder/'physical_result.json',RES/folder/'trial.json',RES/folder/'MANIFEST_SHA256.json']
 out=dict(status='new_exact_fixed_vector_polynomial_export_pending_independent_review',geometry=trial['trial']['geometry'],N=geo['N'],trial_dimension=len(G),integer_coefficients=list(map(int,c)),integer_metric_norm=str(norm),rayleigh_coefficients=C.st(rho),full_second_moment_coefficients=C.st(m2),full_residual_squared_coefficients=C.st(var),unnormalized_expectations={k:str(v) for k,v in zip(['Q','A','Q2','QA_plus_AQ','A2'],[q1,a1,q2,qa,a2])},point_reproduced=str(g),source_sha256={str(x.relative_to(RES)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths})
 (HERE/f'ground_polynomial_{shape}_check.json').write_text(json.dumps(out,indent=2)+'\n');return out
if __name__=='__main__':
 for shape,folder in [('4x4','bilayer_16d_4x4_residual_g0105'),('8x4','bilayer_optimized_residual_g0105')]:export(shape,folder)
 print('Both exact complete fixed-vector polynomials exported')
