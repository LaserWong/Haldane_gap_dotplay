"""Exact symbolic Kronecker audit, independent of ladder implementation."""
import json
from fractions import Fraction as F
import numpy as np
import sympy as S
from gapflow.model import Model
from gapflow.certify import pencil_inertia,certify_pencil_gap,certify_pencil_gap_from_vector
cases=[]
for spins in [(F(1,2),F(1)),(F(3,2),F(2)),(F(2),F(2)),(F(1,2),F(1),F(3,2))]:
 n=len(spins);dims=[int(2*s+1) for s in spins];edges=[(i,i+1) for i in range(n-1)]
 m=Model.from_dict({'spins':list(spins),'geometry':{'type':'graph','n_sites':n,'edges':edges},'terms':[{'type':'xxz','Jxy':'3/7','Jz':'-2/5'},{'type':'field_z','h':'1/9'},{'type':'onsite_d','D':'2/11'}]})
 Z=[];P=[]
 for i,s in enumerate(spins):
  s=S.Rational(s.numerator,s.denominator);d=dims[i]
  z=S.diag(*[-s+p for p in range(d)]);p=S.zeros(d)
  for j in range(d-1):
   mj=-s+j;p[j+1,j]=S.sqrt(s*(s+1)-mj*(mj+1))
  Z.append(S.kronecker_product(*[z if j==i else S.eye(dj) for j,dj in enumerate(dims)]))
  P.append(S.kronecker_product(*[p if j==i else S.eye(dj) for j,dj in enumerate(dims)]))
 D=int(np.prod(dims));H=S.zeros(D)
 for i,j in edges:H+=S.Rational(3,14)*(P[i]*P[j].T+P[i].T*P[j])-S.Rational(2,5)*Z[i]*Z[j]
 for z in Z:H+=z/9+S.Rational(2,11)*z*z
 full_states=m.basis().states
 tested=0
 for sector in [None]+list(m.sector_dimensions()):
  A,w=m.exact_pencil(total_m2=sector)
  ids=[full_states.index(state) for state in m.basis(sector).states]
  for i,fi in enumerate(ids):
   for j,fj in enumerate(ids):
    assert S.simplify(S.Rational(A[i][j].numerator,A[i][j].denominator)-S.sqrt(w[i]*w[j])*H[fi,fj])==0
  vals=np.linalg.eigvalsh(np.array(H.extract(ids,ids),dtype=float));t=F(1,13)
  c=pencil_inertia(A,w,t)
  assert (c.negative,c.zero,c.positive)==(sum(vals<float(t)-1e-10),sum(abs(vals-float(t))<=1e-10),sum(vals>float(t)+1e-10))
  tested+=1
 cases.append({'spins':[str(s) for s in spins],'exact_matrix_and_sector_checks':tested})
for s,t in [(F(1,2),F(1)),(F(3,2),F(2)),(F(2),F(2))]:
 m=Model.from_dict({'spins':[s,t],'geometry':{'type':'graph','n_sites':2,'edges':[[0,1]]},'terms':[{'type':'heisenberg','J':1}]})
 A,w=m.exact_pencil();q=abs(s-t);ground=(q*(q+1)-s*(s+1)-t*(t+1))/2;gap=q+1
 c=certify_pencil_gap(A,w,ground,gap)
 assert c['certified'] and c['ground_multiplicity']==2*q+1
 assert not certify_pencil_gap(A,w,ground,gap+F(1,100))['certified']
# Metric validation and no-excitation regression.
for weights in [[0,1],[-1,1],[1],[1.,1]]:
 try:pencil_inertia([[0,0],[0,1]],weights)
 except (TypeError,ValueError):pass
 else:raise AssertionError('invalid metric accepted')
assert not certify_pencil_gap([[2,0],[0,6]],[1,3],2,10)['certified']
assert not certify_pencil_gap_from_vector([[2,0],[0,6]],[1,3],[1,0],3)['certified']
print(json.dumps({'status':'passed','symbolic_kronecker_cases':cases,'exact_heisenberg_pair_gap_checks':3,'scope':'Independent exact symbolic matrix construction; numerical inertia comparison; analytic pair energies'},indent=2))
