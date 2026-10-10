"""Exact local spin-half bilayer transfer identities in an explicit TR-real cell basis."""
import json
from pathlib import Path
import sympy as s
I=s.I;q=s.Rational
# Product basis dd,du,ud,uu; all columns have norm sqrt(2).
P=s.Matrix.hstack(s.Matrix([0,1,-1,0]),s.Matrix([0,I,I,0]),s.Matrix([1,0,0,1]),s.Matrix([I,0,0,-I]))
J=s.Matrix([[0,1],[-1,0]]);TR=s.kronecker_product(J,J)
assert P.conjugate().T*P==2*s.eye(4)
assert TR*P.conjugate()==P
spin=[s.Matrix([[0,q(1,2)],[q(1,2),0]]),s.Matrix([[0,I/2],[-I/2,0]]),s.diag(-q(1,2),q(1,2))]
A=[]
for layer in range(2):
 for op in spin:
  phys=s.kronecker_product(op,s.eye(2)) if layer==0 else s.kronecker_product(s.eye(2),op)
  real=(P.conjugate().T*phys*P)/(2*I)
  assert real==real.conjugate() and real.T==-real
  A.append(real)
h=sum((s.kronecker_product(op,op) for op in spin),s.zeros(4))
hreal=P.conjugate().T*h*P/2
assert hreal==s.diag(-q(3,4),q(1,4),q(1,4),q(1,4))
# In the cell basis each inter-rung two-layer Heisenberg bond is -sum A⊗A.
result={'status':'PASS exact symbolic local identities','basis_columns_unnormalized':[[str(x) for x in P[:,j]] for j in range(4)],'common_normalization':'1/sqrt(2)','time_reversal_is_complex_conjugation':True,'rung_H':str(hreal),'six_real_antisymmetric_A':[[[str(x) for x in mat.row(j)] for j in range(4)] for mat in A],'positive_history_decomposition':'-g*sum_(layer,alpha) S_layer^alpha tensor S_layer^alpha = g*sum A tensor A, g>=0','operator_norm_each_A':'1/2'}
(Path(__file__).resolve().parent/'bilayer_transfer_identity.json').write_text(json.dumps(result,indent=2))
print('PASS exact rung basis, antiunitary real form, six antisymmetric factors, rung energies')
