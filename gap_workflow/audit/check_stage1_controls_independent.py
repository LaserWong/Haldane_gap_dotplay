"""Independent finite controls; analytic all-size review in companion report."""
import itertools,json
from fractions import Fraction as F
import numpy as np
from gapflow.classical_seed import analytic_thermal_seed,certify_target
from gapflow.degenerate import temporal_defects
from gapflow.transfer_eligibility import bond_realignment_certificate
rng=np.random.default_rng(7391)
counts={'pinned_counting_cases':0,'temporal_fixtures':0,'full_magnon_matrices':0,'structural_reconstructions':0}
for J in [0,1,3]:
 for L in range(2,9):
  energies=[J*sum(bits[i]!=bits[(i+1)%L] for i in range(L))+2*sum(bits) for bits in itertools.product((0,1),repeat=L)]
  assert energies.count(0)==1 and min(e for e in energies if e)>=(2)
  z=sum((F(1,5)**e for e in energies),F(0));assert 1<=z<=(1+F(1,25))**L
  counts['pinned_counting_cases']+=1
for g in range(1,8):
 for _ in range(40):
  weights=[F(int(rng.integers(1,20)),21) for i in range(int(rng.integers(0,12)))]
  c=temporal_defects(g,weights)
  p=[F(1)]*g+weights;p=[x/sum(p) for x in p]
  assert c['defect']==1-g*sum(x*x for x in p)
  p2=[x*x for x in ([F(1)]*g+weights)];p2=[x/sum(p2) for x in p2]
  assert c['doubled_defect']==1-g*sum(x*x for x in p2)
  assert sum(weights)<=c['excited_weight_sum_upper']
  assert c['doubled_defect']<=c['quadratic_upper']
  counts['temporal_fixtures']+=1
for L in range(2,8):
 # Build H=sum(I-swap)/2 directly in bitstring basis, without spin-model code.
 D=2**L;H=np.zeros((D,D));psi=np.zeros(D,dtype=complex)
 for state in range(D):
  for i in range(L):
   j=(i+1)%L;swapped=state
   if ((state>>i)&1)!=((state>>j)&1):swapped=state^(1<<i)^(1<<j)
   H[state,state]+=.5;H[swapped,state]-=.5
 for i in range(L):psi[1<<i]=np.exp(2j*np.pi*i/L)/np.sqrt(L)
 eig=np.linalg.eigvalsh(H);energy=1-np.cos(2*np.pi/L)
 assert sum(abs(eig)<1e-10)==L+1 and eig[0]>-1e-10
 assert np.linalg.norm(H@psi-energy*psi)<1e-12
 # Orthogonality against every ground eigenvector, not merely polarized vacuum.
 vals,vec=np.linalg.eigh(H);assert np.linalg.norm(vec[:,abs(vals)<1e-10].conj().T@psi)<1e-10
 counts['full_magnon_matrices']+=1
for q in [2,3]:
 for _ in range(10):
  factors=[]
  for k in range(3):
   a=rng.integers(-3,4,(q,q));a=a+a.T;factors.append(a)
  H=-sum(np.kron(a,a) for a in factors)
  c=bond_realignment_certificate(H.tolist());assert c['witness_reconstruction_verified']
  reconstructed=[[F(0) for _ in range(q*q)] for _ in range(q*q)]
  for term in c['identical_factor_witness']:
   a=[[F(x) for x in row] for row in term['operator']];coef=F(term['coefficient'])
   for i,j,k,l in itertools.product(range(q),repeat=4):reconstructed[i*q+k][j*q+l]-=coef*a[i][j]*a[k][l]
  assert reconstructed==H.tolist() and c['spatial_transfer_family_certified'] is False
  counts['structural_reconstructions']+=1
seed=analytic_thermal_seed([2],F(1,100000),3,2)
for key,value in [('h','3'),('purities',['1','1']),('analytic_gap_lower_bound','100')]:
 altered=dict(seed);altered[key]=value
 try:certify_target(altered,1)
 except ValueError:pass
 else:raise AssertionError('Tampered seed accepted')
print(json.dumps({'status':'passed','checks':counts,'scope':'Exact rational finite counting/temporal/structural tests plus independent floating full-space swap/magnon check'},indent=2))
