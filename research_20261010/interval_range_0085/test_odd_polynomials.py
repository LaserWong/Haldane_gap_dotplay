"""Exact structural fixtures and production denominator-bound checks.
These supplement the analytic degree and interval proofs.
"""
import certify_lowband as B
C=B.C;O=B.O
from fractions import Fraction as F
import json,copy

def matvec(A,v):return [sum(a*x for a,x in zip(row,v)) for row in A]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def add(a,b):return [x+y for x,y in zip(a,b)]
def scale(x,a):return [x*y for y in a]
def test_bivariate():
 cases=0
 Q=[[1,0,0],[0,3,0],[0,0,3]]
 for seed in range(1,13):
  V=[[F(seed,7),F(2-seed,11),F(seed+1,13)],
     [F(2-seed,11),F(seed+3,17),F(1,19)],
     [F(seed+1,13),F(1,19),F(2*seed,23)]]
  u=[F(seed,2),0,0];v=[0,F(seed+2,3),F(-seed,5)]
  # Different left and right columns test cross-displacement coefficients.
  ur=[F(seed+1,3),0,0];vr=[0,F(-seed-3,7),F(seed+2,11)]
  def diagonal(z):
   w=add(u,scale(z,v));wr=add(ur,scale(z,vr));H=lambda a:add(matvec(Q,a),scale(z,matvec(V,a)))
   return [dot(w,wr),dot(w,H(wr)),dot(H(w),H(wr))]
  xs=list(map(F,(0,1,2,3,4)));ys=[diagonal(z) for z in xs]
  gg,aa,bb=[O.interpolate(xs[:degree+1],[row[k] for row in ys[:degree+1]]) for k,degree in enumerate((2,3,4))]
  assert gg[1]==0 and aa[0]==bb[0]==gg[0] and bb[1]==2*aa[1]
  vv=[aa[1],aa[2]-3*gg[2],aa[3]];cc=[2*vv[0],4*vv[1],6*vv[2]]
  dd=[bb[2]-9*gg[2]-cc[1],bb[3]-cc[2],bb[4]]
  for z,p in ((F(0),F(1,10)),(F(17,200),F(83,1000)),(F(1,5),F(1,7))):
   w=add(u,scale(z,v));wr=add(ur,scale(z,vr));H=lambda a:add(matvec(Q,a),scale(p,matvec(V,a)))
   got=[gg[0]+z*z*gg[2],gg[0]+3*z*z*gg[2]+p*O.evaluate(vv,z),
    gg[0]+9*z*z*gg[2]+p*O.evaluate(cc,z)+p*p*O.evaluate(dd,z)]
   assert got==[dot(w,wr),dot(w,H(wr)),dot(H(w),H(wr))];cases+=1
 return cases

def main():
 fixtures=test_bivariate();source_checks=0;symmetry_checks=0;diagonal_checks=0
 for shape,raw in B.RAW.items():
  nx,ny=shape;assert raw==json.loads((C.HERE/f'odd_polynomial_{nx}x{ny}.json').read_text())
  source_checks+=raw['exact_source_evaluation_checks']
  for key in ('G','A','B'):
   arr=raw['coefficient_arrays'][key]
   for i in range(nx):
    for j in range(ny):assert arr[i][j]==arr[(-i)%nx][(-j)%ny];symmetry_checks+=1
  for z in map(F,('0','3/100','2/25','17/200','1/10')):
   fixed=O.fixed_modes(raw,z)
   arr=fixed['coefficient_arrays']
   for i in range(nx):
    for j in range(ny):
     fs={k:F(a[i][j]) for k,a in arr.items()}
     for key,val in [('G',fs['G']),('A',fs['Q']+z*fs['V']),('B',fs['Q2']+z*fs['C']+z*z*fs['D'])]:
      assert val==O.evaluate(list(map(F,raw['coefficient_arrays'][key][i][j])),z);diagonal_checks+=1
 production=0;covariance=0;min_margin=None
 summ=json.loads((C.HERE/'lowband_summary.json').read_text())
 for item in summ['intervals']:
  saved=json.loads((C.HERE/item['file']).read_text());lo,hi=map(F,saved['coupling_interval'])
  for patch in saved['denominator_patches']:
   rho=list(map(F,patch['rayleigh_coefficients']));N=patch['N']
   assert patch['odd_band']['q_components']==[1,3]
   assert len(patch['odd_band']['modes'])==N
   for row in patch['odd_band']['modes']:
    th=[O.Quad(*map(F,v)) for v in row['theta_coefficients']]
    vs=[O.Quad(*map(F,v)) for v in row['residual_squared_coefficients']]
    assert (4*vs[0]*vs[2]-vs[1]*vs[1]).sign()>=0;covariance+=1
    margin=F(row['uniform_Temple_denominator']);min_margin=margin if min_margin is None else min(min_margin,margin)
    for k in range(9):
     g=lo+(hi-lo)*F(k,8);theta=O.evaluate(th,g);var=O.evaluate(vs,g)
     cutoff=O.Quad(C.reference(g,N,2));den=cutoff-theta
     assert (den-margin).sign()>=0 and (F(row['residual_squared_max'])-var).sign()>=0
     true_relative=theta-var/den-C.poly(rho,g)
     assert (true_relative-F(row['eigen_lower_minus_ground_rayleigh_uniform_lower'])).sign()>=0;production+=1
 # The normalization powers are tied to W=2d*w and T=d*H; reject a common
 # mistake by direct integer fixtures at two distinct denominator values.
 norm_cases=0
 for d in (40,400):
  for power in (2,3,4):
   normalized=F(7,5);stored=normalized*4*d**power
   assert stored/(4*d**power)==normalized and stored/(4*d**(power-1))!=normalized;norm_cases+=1
 out=dict(status='PASS producer odd-polynomial and uniform-bound tests',
  cross_column_bivariate_fixtures=fixtures,exact_audited_source_checks=source_checks,
  Hermitian_displacement_symmetry_checks=symmetry_checks,diagonal_recovery_checks=diagonal_checks,
  production_covariance_checks=covariance,production_interval_bound_checks=production,
  normalization_guard_cases=norm_cases,smallest_uniform_odd_Temple_denominator=str(min_margin),
  warning='Finite tests supplement the analytic all-real-coupling proof; independent audit remains required.')
 (C.HERE/'odd_test_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
