#!/usr/bin/env python3
"""Independent exact AKLT checks using integer characteristic polynomials."""
import os, resource
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import sympy as s, itertools as it, json, time
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parent
t0=time.time()
# Start with the physical Cartesian spin generators, not the producer's projector.
spin=[]
for a in range(3):
 spin.append(s.Matrix(3,3,lambda b,c:-s.I*s.LeviCivita(a,b,c)))
assert sum((x*x for x in spin),s.zeros(3))==2*s.eye(3)
bond=sum((s.kronecker_product(x,x) for x in spin),s.zeros(9))
h=(bond*bond+3*bond+2*s.eye(9))/6
assert h*h==h and h.rank()==5
swap=s.Matrix(9,9,lambda i,j:int(i//3==j%3 and i%3==j//3))
omega=s.Matrix([int(i//3==i%3) for i in range(9)])
assert h==(s.eye(9)+swap)/2-omega*omega.T/3
assert s.kronecker_product(h,s.eye(3))*s.kronecker_product(s.eye(3),h)!=s.kronecker_product(s.eye(3),h)*s.kronecker_product(h,s.eye(3))
q=6*h
assert all(x.is_Integer for x in q)

def build(L,periodic):
 states=list(it.product(range(3),repeat=L))
 loc={v:i for i,v in enumerate(states)}
 entries={}
 for col,v in enumerate(states):
  for a in range(L if periodic else L-1):
   b=(a+1)%L
   for x in range(3):
    for y in range(3):
     z=q[3*x+y,3*v[a]+v[b]]
     if z:
      w=list(v);w[a]=x;w[b]=y
      key=(loc[tuple(w)],col)
      entries[key]=entries.get(key,0)+z
 B=s.MutableSparseMatrix(3**L,3**L,entries)
 groups={}
 for j,v in enumerate(states):groups.setdefault(tuple(v.count(c)%2 for c in range(3)),[]).append(j)
 for (i,j),value in B.todok().items():
  if value:assert tuple(states[i].count(c)%2 for c in range(3))==tuple(states[j].count(c)%2 for c in range(3))
 return states,B,groups

def positive_by_characteristic(M):
 # For a real symmetric matrix, (-1)^degree p(-x) has nonnegative
 # coefficients exactly when all elementary symmetric functions are >=0.
 # Such a polynomial is positive for x>0, hence M has no negative eigenvalue.
 assert M==M.T
 coeff=[int(v) for v in M.charpoly().all_coeffs()]
 elementary=[(-1)**j*v for j,v in enumerate(coeff)]
 assert all(v>=0 for v in elementary)
 null=0
 for v in reversed(coeff):
  if v:break
  null+=1
 return {'dimension':M.rows,'nullity':null,'characteristic_coefficients':list(map(str,coeff))}

cert=[]
for L,periodic in [(2,False),(3,False),(4,False),(3,True),(4,True),(5,True)]:
 states,B,groups=build(L,periodic)
 rows=[]
 for par,indices in sorted(groups.items()):
  block=s.Matrix(B.extract(indices,indices))
  r={'parity':par,'H_scaled_by_6':positive_by_characteristic(block)}
  if L==4 and not periodic:r['gap_polynomial_5B2_minus_12B']=positive_by_characteristic(5*block*block-12*block)
  if L==5 and periodic:r['gap_polynomial_5B2_minus_3B']=positive_by_characteristic(5*block*block-3*block)
  rows.append(r)
 assert sum(r['H_scaled_by_6']['nullity'] for r in rows)==(1 if periodic else 4)
 cert.append({'L':L,'periodic':periodic,'blocks':rows})
 print('exact local check',L,periodic,flush=True)

pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
W=lambda L:s.Matrix([[s.trace(__import__('functools').reduce(lambda a,b:a*b,[pauli[x] for x in v],s.eye(2))*X) for X in [s.eye(2),*pauli]] for v in it.product(range(3),repeat=L)])
assert W(1).rank()==3 and W(2).rank()==4 and W(3).rank()==4
assert h*W(2)==s.zeros(9,4)
_,B3,_=build(3,False)
assert B3*W(3)==s.zeros(27,4)
mps=[]
for L in range(3,7):
 vec=W(L)[:,0]
 _,B,_=build(L,True)
 assert B*vec==s.zeros(3**L,1)
 norm=(s.conjugate(vec).T*vec)[0]
 assert norm==3**L+3*(-1)**L
 assert sum(x!=0 for x in vec)==norm/4
 # Every one-site reduced density matrix has full rank, proving entanglement.
 wave=s.Matrix(3,3**(L-1),list(vec));rdm=wave*s.conjugate(wave.T)
 assert rdm==norm*s.eye(3)/3
 mps.append({'L':L,'norm':int(norm),'nonzero_amplitudes':int(norm/4),'one_site_reduced_density':'I/3'})
E=sum((s.kronecker_product(A,s.conjugate(A)) for A in pauli),s.zeros(4))
assert E.charpoly().as_expr().factor()==(s.Symbol('lambda')-3)*(s.Symbol('lambda')+1)**3
# Pauli multiplication modulo phase is the Klein four group. Three nonidentity
# letters have convolution spectrum (3,-1,-1,-1), giving the support count.
Q=s.diag(1,-1,0)
witness=sum(-h[3*a+c,3*b+d]*Q[a,b]*Q[c,d] for a,b,c,d in it.product(range(3),repeat=4))
assert witness==-s.Rational(1,3)
# Count every unordered pair of periodic bonds, including the short L=5 case.
wrapping=[]
for L in range(5,21):
 windows=[{i,(i+1)%L,(i+2)%L} for i in range(L)]
 counts={pair:sum(set(pair)<=w for w in windows) for pair in it.combinations(range(L),2)}
 for (i,j),multiplicity in counts.items():
  adjacent=(j-i in (1,L-1))
  assert multiplicity==(2 if adjacent else (1 if min(j-i,L-j+i)==2 else 0))
  assert multiplicity<=2
 wrapping.append({'L':L,'adjacent_multiplicity':2,'distance_two_multiplicity':1,'other_multiplicity':0})
# Exact thermal tail upper bounds. No giant many-body matrix is built.
thermal=[]
for L,beta in [(8,160),(16,240)]:
 bound=F(3**L-1,1)/(1+F(beta,40960))**4096
 assert bound<F(1,100)
 thermal.append({'L':L,'beta':beta,'omitted':3**L-1,'tail_upper_exact_expression':f'({3**L-1})*(40960/{40960+beta})^4096','tail_upper_display':float(bound),'norm':3**L+3*(-1)**L,'nonzero_amplitudes':(3**L+3*(-1)**L)//4})
result={'status':'PASS','method':'independent Cartesian generators, integer characteristic-polynomial positivity, direct periodic checks, bond-pair counting','local_checks':cert,'mps_checks':mps,'wrapping_checks':wrapping,'realignment_witness':str(witness),'thermal_examples':thermal,'seconds':time.time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'aklt_independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['local_checks','thermal_examples','wrapping_checks']},indent=2))
