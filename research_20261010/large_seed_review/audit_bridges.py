"""Independent acceptance of local/fixed-window bridge witnesses."""
from audit_tail_trace import *
SRC=RESEARCH/'root_review/large_seed_bridges'

def spin_dot(i,j):
 # Exact orthonormal computational basis, assembled independently.
 m=[[F(0)]*16 for _ in range(16)]
 for ket in range(16):
  a=(ket>>i)&1;b=(ket>>j)&1;m[ket][ket]=F((2*a-1)*(2*b-1),4)
  if a!=b:m[ket^(1<<i)^(1<<j)][ket]=F(1,2)
 return mat(m)

def validate_step(S,T,witness):
 S,T=F(S),F(T);p=S*S*T;assert p>F(1,2) and p==F(witness['p'])
 w=F(witness['dominant_weight_lower']);assert F(1,2)<w<=1 and (2*w-1)**2<=2*p-1
 r=F(witness['tail_ratio_upper']);assert r==(1-w)/w and 0<=r<1
 d=F(witness['d_lower']);assert d==T/(1+r*r)
 lower=F(witness['purity_lower']);scaled=lower/(1-r)
 assert lower>0 and scaled<=d and (scaled/S)**2<=d
 return lower

def main():
 small=load(SRC/'local_small_sizes.json');identity=np.eye(16,dtype=object)
 M=spin_dot(0,2)+spin_dot(1,3)+F(3,2)*(spin_dot(0,1)+spin_dot(2,3)+F(3,2)*identity)+F(1,3)*identity
 assert (24*M).tolist()==small['local_matrix_numerator'] and inertia(M)==(0,0,16)
 report=[]
 for row in load(SRC/'large_seed_bridge_results.json')['records']:
  g=F(row['g']);source=ROOT/row['source'];assert hashlib.sha256(source.read_bytes()).hexdigest()==row['source_sha256'];seed=load(source)['exact'];target=F(row['all_integer_L_ge2_gap'])
  assert target==F(seed['bootstrap']['uniform_square_gap_lower'])
  for small in row['local_L2_L3']:
   L=small['L'];N=L*L;assert small['N']==N and F(small['gap_lower'])==1-(6+F(2*N,3))*g>=target
  coverage={2,3}
  for window in row['finite_windows']:
   n=window['n'];beta=F(window['beta']);A,B,C=map(F,window['purities'])
   if n==4:assert A==B==C==F(seed['J1']) and beta==F(seed['beta_initial'])
   elif n==8:assert [A,B,C]==list(map(F,seed['first_purities'])) and beta==2*F(seed['beta_initial'])
   else:assert False
   detail=window['details'];S=F(detail['spatial_lower']);assert 0<S<=1 and S*S<=A**4*(2*B-1)
   T=validate_step(B,C,detail['y']);assert T==F(detail['transverse_thermal_lower'])
   purity=validate_step(S,T,detail['x']);assert purity==F(window['thermal_lower'])>F(1,2)
   gap=F(window['gap_lower']);assert gap>=target and exp_independent(beta*gap)[1]*(1-purity)<purity
   assert window['through']==2*n;coverage.update(range(n,2*n+1))
  onset=seed['bootstrap']['n'];assert all(L in coverage for L in range(2,onset))
  report.append(dict(g=str(g),all_integer_L_ge=2,gap=str(target),gap_display=float(target),local_L2_L3_PSD_independent=True,all_window_witnesses_and_gap_exponentials_independent=True,asymptotic_onset=onset))
  print('ALL SIZE BRIDGE PASS',g,float(target),flush=True)
 save('all_size_bridge_review.json',dict(status='PASS',records=report))
if __name__=='__main__':main()
