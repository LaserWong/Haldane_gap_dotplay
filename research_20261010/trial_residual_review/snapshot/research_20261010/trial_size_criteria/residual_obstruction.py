"""Exact no-small-residual witnesses inside the fixed six-vector q2 search space."""
from criteria import *
from math import isqrt

def pd_pivots(A):
 A=[[F(v) for v in row] for row in A];piv=[]
 for k in range(len(A)):
  p=A[k][k]
  if p<=0:return None
  piv.append(p)
  for i in range(k+1,len(A)):
   for j in range(i,len(A)):
    A[j][i]=A[i][j]=A[i][j]-A[i][k]*A[k][j]/p
 return piv

def witness(g,target):
 d=read(f'research_20261010/large_seed_moments/block1_4x4_g{g}.json');assert d['selected_basis_indices'][:6]==list(range(6))
 E00=F(d['E00']);broad=read(f'research_20261010/low_band/frontier/bilayer_4x4_g{g}_symmetric_number_low_band.json') if g in ['1d25','1d20'] else None
 lower=(F(broad['blocks'][0]['eigen_lower'][0]) if broad else F(d['ground_lower'])-E00);upper=F(d['ground_upper'])-E00+F(1,1000)
 c=(lower+upper)/2;h=(upper-lower)/2;den=F(d['integer_matrix_denominator']);G0=[[F(v) for v in row[:6]] for row in d['gram'][:6]];A=[[F(v)/den for v in row[:6]] for row in d['shifted_hamiltonian_numerator'][:6]];B=[[F(v)/den**2 for v in row[:6]] for row in d['shifted_H2_numerator'][:6]]
 assert pd_pivots(G0)
 C=[[B[i][j]-2*c*A[i][j]+c*c*G0[i][j] for j in range(6)] for i in range(6)]
 gl=F(0);gh=F(1,10)
 for _ in range(32):
  z=(gl+gh)/2
  if pd_pivots([[C[i][j]-z*G0[i][j] for j in range(6)] for i in range(6)]):gl=z
  else:gh=z
 piv=pd_pivots([[C[i][j]-gl*G0[i][j] for j in range(6)] for i in range(6)]);assert piv
 scale=10**12;alpha=F(isqrt(gl.numerator*scale*scale//gl.denominator),scale);assert alpha*alpha<=gl and alpha>h
 residual_lower=(alpha-h)**2;assert residual_lower>target
 better_res=F(d['exact_residual_squared']);assert better_res<target
 return dict(g=g,status='PASS: no normalized vector in this fixed six-dimensional q2 space with Rayleigh quotient in the stated interval reaches the target; saved eleven-dimensional vector does',q2_search_dimension=6,block1_search_dimension=d['trial_subspace_dimension'],shifted_Rayleigh_interval=[lower,upper],midpoint=c,halfwidth=h,matrix_lower_bound=gl,exact_positive_LDL_pivots=piv,sqrt_lower=alpha,uniform_residual_squared_lower=residual_lower,residual_squared_target=target,block1_residual_squared=better_res,block1_rayleigh_in_interval=(lower<=F(d['ground_upper'])-E00<=upper))
if __name__=='__main__':
 rows=[witness(g,t) for g,t in [('1d50',F(1,10**6)),('3d100',F(1,10**6)),('1d25',F(1,10**5)),('1d20',F(1,10**4))]]
 (OUT/'residual_obstructions.json').write_text(json.dumps(serial(dict(results=rows,input_sha256=READ_HASHES)),indent=2)+'\n')
 for r in rows:print(r['g'],float(r['uniform_residual_squared_lower']),'>',float(r['residual_squared_target']),'>',float(r['block1_residual_squared']))
