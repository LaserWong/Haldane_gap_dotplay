"""Exact elementary fixtures and production interval filter sanity checks."""
from certify_range import *
from filter_rayleigh import positive_upper_pivots

def main():
 count=0
 # Formula: fixed t, varying exact variance and residual energy C<=Cmax.
 # Includes zero variance and a 10^60 variation; no denominator reversal.
 for Cmax in map(F,('1/1000','1','1000')):
  for vmin in map(F,('0','1/1000000000000000000000000000000','1','1000')):
   t=1/Cmax;gain=vmin*Cmax/(Cmax*Cmax+vmin)
   for scale in [1,2,10**30,10**60]:
    v=vmin*scale
    for C in [Cmax,-Cmax,F(0),Cmax/2]:
     shifted=v*(-2*t+C*t*t)/(1+t*t*v)
     assert shifted<=-gain;count+=1
 # Exact actual Rayleigh quotient of H=[[rho,s],[s,rho+C]], psi=e1.
 direct=0
 for k in range(21):
  g=F(k,100);rho=F(-3,5)+g;s=F(1,10)+g;C=F(2)-g;t=F(1,3)
  v=s*s;vmin=F(1,100);Cmax=F(3);gain=(2*t-Cmax*t*t)*vmin/(1+t*t*vmin)
  numerator=rho-2*t*v+t*t*v*(rho+C);denominator=1+t*t*v
  assert numerator/denominator<=rho-gain;direct+=1
 # Vertex as well as endpoints must enter a convex quadratic minimum.
 assert quadratic_bounds([F(1,4),F(-1),F(1)],F(0),F(1))==(F(0),F(1,4))
 assert quadratic_bounds([F(0),F(0),F(0)],F(0),F(1))==(F(0),F(0))
 prod=0
 summary=json.loads((HERE/'coverage_summary.json').read_text())
 for item in summary['intervals']:
  r=json.loads((HERE/item['file']).read_text());lo,hi=map(F,r['coupling_interval']);tr=r['largest_base_trial'];ff=r['largest_interval_filter'];var=list(map(F,tr['full_residual_squared_coefficients']));rho=list(map(F,tr['rayleigh_coefficients']))
  vmin,vmax=quadratic_bounds(var,lo,hi);t=F(ff['fixed_t']);Cmax=F(ff['Cmax']);gain=F(ff['uniform_improvement']);comp=ff['compressed_upper_at_high'];Rmax=F(comp['compressed_H_upper'])
  assert gain==vmin*Cmax/(Cmax*Cmax+vmin)>0 and t==1/Cmax
  assert positive_upper_pivots(list(map(F,comp['diagonal'])),list(map(F,comp['offdiagonal_squared'])),Rmax)==list(map(F,comp['upper_LDL_positive_pivots']))
  for k in range(17):
   g=lo+(hi-lo)*F(k,16);v=poly(var,g);C=Rmax-poly(rho,g)
   assert vmin<=v<=vmax and C<=Cmax
   assert v*(-2*t+C*t*t)/(1+t*t*v)<=-gain;prod+=1
 out=dict(status='PASS exact producer filter tests',scalar_cases=count,actual_two_by_two_Rayleigh_fixtures=direct,production_parameter_checks=prod,quadratic_vertex_minimum_test=True,zero_variance_test=True,large_variance_normalization_direction_test=True)
 (HERE/'test_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
