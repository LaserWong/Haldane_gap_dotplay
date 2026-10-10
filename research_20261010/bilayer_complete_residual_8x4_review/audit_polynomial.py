"""Independent decomposition into separately homogeneous B,L,R,M sectors."""
from pathlib import Path
from fractions import Fraction as F
import json
R=Path(__file__).resolve().parent;P=R.parent
rd=lambda p:json.loads(p.read_text())
trial=rd(R/'snapshot/ground_8x4_trial.json');geo=rd(P/'third_moment_review/results/geometry_8x4.json');gr=rd(P/'low_band/frontier_g007_g010/g1d10/block1_8x4_g1d10.json');phys=rd(R/'assembly_result.json');prod=rd(R/'snapshot_polynomial/fixed_vector_coupling_polynomials.json')
b=15;n=14;D=57;c=trial['coefficients']+trial['coefficients'][-14:];q=[0]+[2]*14+[4]*28+[6]*14
G=[[F(0)]*D for _ in range(D)];A=[[F(0)]*D for _ in range(D)]
base=gr['shifted_integer_moments_M0_to_M4'];gb=base[0];ab=base[1]
for i in range(b):
 for j in range(b):G[i][j]=F(gb[i][j]);A[i][j]=(F(ab[i][j])-40*q[j]*G[i][j])/2
ff,ss,vv,ww,xx,yy,zz=[geo[k] for k in ['F','S','V','W','X','Y','Z']]
for i in range(n):
 for j in range(n):
  f,s,v,w,x,y,z=map(F,[ff[i][j],ss[i][j],vv[i][j],ww[i][j],xx[i][j],yy[i][j],zz[i][j]])
  li,ri,mi=b+i,b+n+i,b+2*n+i;lj,rj,mj=b+j,b+n+j,b+2*n+j
  G[li][lj]=f;G[li][rj]=G[rj][li]=s;G[ri][rj]=v;G[mi][mj]=w
  A[1+i][lj]=A[lj][1+i]=f;A[1+i][rj]=A[rj][1+i]=s
  A[li][lj]=s;A[li][rj]=A[rj][li]=v;A[li][mj]=A[mj][li]=w;A[ri][rj]=x;A[ri][mj]=A[mj][ri]=y;A[mi][mj]=z
assert A==list(map(list,zip(*A))) and G==list(map(list,zip(*G)))
expect=lambda mat,weight:sum(F(c[i])*mat[i][j]*c[j]*weight(i,j) for i in range(D) for j in range(D))
norm=expect(G,lambda i,j:1);q1=expect(G,lambda i,j:q[j]);q2=expect(G,lambda i,j:q[i]*q[j]);a1=expect(A,lambda i,j:1);qa=expect(A,lambda i,j:q[i]+q[j]);t=F(1,20)
a2=(F(phys['second_moment'])*norm-q2-t*qa)/(t*t)
expected=dict(Q=str(q1),A=str(a1),Q2=str(q2),QA_plus_AQ=str(qa),A2=str(a2));assert expected==prod['unnormalized_expectations'] and str(norm)==prod['norm']
mean=[q1/norm,a1/(2*norm)];second=[q2/norm,qa/(2*norm),a2/(4*norm)];var=[second[0]-mean[0]**2,second[1]-2*mean[0]*mean[1],second[2]-mean[1]**2]
for name,coeff in [('rayleigh',mean),('full_second_moment',second),('full_variance',var)]:assert list(map(str,coeff))==prod[name+'_coefficients_in_g']
assert var[0]>0 and var[2]>0 and 4*var[0]*var[2]-var[1]**2>0
assert sum(v*F(1,10)**i for i,v in enumerate(var))==F(phys['variance'])
out=dict(status='PASS_exact_fixed_vector_coupling_polynomials',unnormalized_expectations=expected,independent_sector_family_dimension=57,actual_enlarged_trial_dimension=43,variance_quadratic_positive_all_real_g=True,continuous_gap_interval_claim=False)
(R/'polynomial_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
