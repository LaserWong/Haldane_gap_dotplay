#!/usr/bin/env python3
"""Independent full tiny-Hilbert vectors, current algebra and source automaton."""
import os,resource,time,itertools,json
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1');os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import numpy as np
P=Path(__file__).resolve().parent;t0=time.process_time();A=[np.array(m,dtype=object) for m in json.loads((P/'inputs/local_tensors.json').read_text())['A']];B=[np.zeros((26,26),dtype=object),A[0],A[1]];Z=[(s-1)*A[s] for s in range(3)]
R=np.array([[0,0,0],[1,0,0],[0,1,0]],dtype=object);L=R.T;M=np.diag([-1,0,1]).astype(object);I=np.eye(3,dtype=object)
h=np.kron(M,M)+np.kron(R,L)+np.kron(L,R);R0=np.kron(R,I);R1=np.kron(I,R);Mt=np.kron(M,I)+np.kron(I,M)
J=h@R0-R0@h
assert np.array_equal(J,np.kron(R,M)-np.kron(M,R)) and np.array_equal(h@R1-R1@h,-J)
assert np.array_equal(J@(R0+R1),(R0+R1)@J) and np.array_equal(Mt@J-J@Mt,J)
assert np.array_equal((np.kron(L,I)+np.kron(I,L))@J-J@(np.kron(L,I)+np.kron(I,L)),np.kron(R,L)-np.kron(L,R))
words=[A[s]@A[t] for s,t in itertools.product(range(3),repeat=2)]
Gamma=[sum((int(J[x,y])*words[y] for y in range(9)),np.zeros((26,26),dtype=object)).tolist() for x in range(9)]
assert Gamma==json.loads((P/'inputs/tiny/current_two_site_tensors.json').read_text())['word_tensors']
source=json.loads((P/'inputs/tiny/tiny_results.json').read_text());rows=[]
for n in [2,4,6]:
 basis=list(itertools.product(range(3),repeat=n));ix={w:i for i,w in enumerate(basis)};d=len(basis)
 def site(v,op,j):
  out=[0]*d
  for w,a in zip(basis,v):
   if a:
    for s in range(3):
     c=int(op[s,w[j]])
     if c:out[ix[w[:j]+(s,)+w[j+1:]]]+=c*a
  return out
 def pair(v,op,j):
  out=[0]*d;k=(j+1)%n
  for w,a in zip(basis,v):
   if a:
    for s,t in itertools.product(range(3),repeat=2):
     c=int(op[3*s+t,3*w[j]+w[k]])
     if c:
      target=list(w);target[j]=s;target[k]=t;out[ix[tuple(target)]]+=c*a
  return out
 def total(v,op,stagger=False):
  out=[0]*d
  for j in range(n):out=[a+(-1 if stagger and j%2 else 1)*b for a,b in zip(out,site(v,op,j))]
  return out
 def H(v):return [sum(x) for x in zip(*(pair(v,h,j) for j in range(n)))]
 def current(v):return [sum(2*(-1)**j*x[j] for j in range(n)) for x in zip(*(pair(v,J,j) for j in range(n)))]
 def dot(a,b):return sum(x*y for x,y in zip(a,b))
 psi=[]
 for w in basis:
  product=np.eye(26,dtype=object)
  for s in w:product=product@A[s]
  psi.append(int(np.trace(product)))
 assert any(psi) and not any(total(psi,R)) and not any(total(psi,L)) and not any(total(psi,M))
 v=total(psi,R,True);Hpsi=H(psi);Hv=H(v);w=[a-b for a,b in zip(Hv,total(Hpsi,R,True))];assert w==current(psi)
 Hw=H(w);assert not any(total(w,R)) and total(w,M)==w
 assert all(not c or w[ix[state[1:]+state[:1]]]==-c for state,c in zip(basis,w))
 # Verify the commutator identity as an operator, not only on psi, at n2 andn4.
 if n<=4:
  for k in range(d):
   unit=[int(j==k) for j in range(d)]
   assert [a-b for a,b in zip(H(total(unit,R,True)),total(H(unit),R,True))]==current(unit)
 # Four open-chain source channels plus two wrap monomials implement7v+3w.
 # Only charge+1 outputs can be nonzero; that selection rule is exact.
 for state,target in zip(basis,[7*a+3*b for a,b in zip(v,w)]):
  if sum(state)!=n+1:assert target==0;continue
  before=np.eye(26,dtype=object);pendingR=np.zeros((26,26),dtype=object);pendingM=pendingR.copy();done=pendingR.copy()
  for j,s in enumerate(state):
   done=done@A[s]+pendingR@Z[s]+pendingM@B[s]+7*(-1)**j*(before@B[s])
   pendingR,pendingM=6*(-1)**j*(before@B[s]),-6*(-1)**j*(before@Z[s])
   before=before@A[s]
  wrapR=Z[state[0]];wrapM=B[state[0]]
  for s in state[1:-1]:wrapR=wrapR@A[s];wrapM=wrapM@A[s]
  wrap=6*(-1)**(n-1)*(wrapR@B[state[-1]]-wrapM@Z[state[-1]])
  assert int(np.trace(done+wrap))==target
 G=[[dot(x,y) for y in [v,w]] for x in [v,w]];HH=[[dot(x,y) for y in [Hv,Hw]] for x in [v,w]];saved=next(r for r in source['rows'] if r['n']==n)
 assert G==[[int(x) for x in r] for r in saved['Gram']] and HH==[[int(x) for x in r] for r in saved['H_form']]
 lowered=[total(x,L) for x in [v,w]]
 assert lowered[0]==[-x for x in total(psi,M,True)]
 assert lowered[1]==[-a+b for a,b in zip(H(total(psi,M,True)),total(Hpsi,M,True))]
 flipped=[[x[ix[tuple(2-s for s in state)]] for state in basis] for x in [v,w]]
 for component in [lowered,flipped]:
  assert [[dot(x,y) for y in component] for x in component]==G
  assert [[dot(x,H(y)) for y in component] for x in component]==HH
 for first,second in [([v,w],lowered),([v,w],flipped),(lowered,flipped)]:
  assert all(dot(x,y)==0 for x in first for y in second)
 assert all(dot(psi,x)==0 for x in lowered)
 det=G[0][0]*G[1][1]-G[0][1]**2;assert det==int(saved['Gram_determinant']) and det>=0
 rv=site(psi,R,0);currents=[pair(psi,J,j) for j in range(n)];Hcurrents=[H(x) for x in currents];correlations={}
 for j in range(n):
  correlations.update({f'C_mix_{n}_{j}':dot(rv,currents[j]),f'K_mix_{n}_{j}':dot(rv,Hcurrents[j]),f'C_jj_{n}_{j}':dot(currents[0],currents[j]),f'K_jj_{n}_{j}':dot(currents[0],Hcurrents[j])})
 for prefix,target in [('C',G),('K',HH)]:
  assert 2*n*sum((-1)**j*correlations[f'{prefix}_mix_{n}_{j}'] for j in range(n))==target[0][1]
  assert 4*n*sum((-1)**j*correlations[f'{prefix}_jj_{n}_{j}'] for j in range(n))==target[1][1]
 if n>=4:
  expected={k:int(v) for k,v in (line.split('=') for line in (P/f'inputs/fused/fixtures_n{n}.out').read_text().splitlines())};assert correlations==expected
 alpha=F(dot(psi,Hpsi),dot(psi,psi));initial=F(HH[0][0],G[0][0]);shortcut_diff=[F(a)-alpha*b-c for a,b,c in zip(Hv,v,w)]
 row={'n':n,'Gram':[[str(x) for x in r] for r in G],'H_form':[[str(x) for x in r] for r in HH],'Gram_determinant':str(det),'normalized_lowering_and_spinflip_all_Gram_H_forms_pass':True,'periodic_current_equals_full_commutator':True,'highest_weight_charge_and_momentum_checked':True,'explicit_bond156_mixed_automaton_checked':True,'not_equal_to_H_minus_Rayleigh_applied_to_v':any(shortcut_diff),'exact_displacement_correlations':{k:str(v) for k,v in correlations.items()}}
 if det:
  coeff=HH[0][0]*G[1][1]+HH[1][1]*G[0][0]-2*HH[0][1]*G[0][1];detH=HH[0][0]*HH[1][1]-HH[0][1]**2;disc=coeff*coeff-4*det*detH;D=10**60;a=isqrt(disc*D*D);lo,hi=(F(coeff)-F(a+1,D))/(2*det),(F(coeff)-F(a,D))/(2*det)
  pLo,pHi=map(F,saved['generalized_minimum_interval']);assert pLo<=lo<=hi<=pHi
  t=F(saved['fixed_rational_mixing_t']);mixed=[F(a)+t*b for a,b in zip(v,w)];ray=F(dot(mixed,H(mixed)),dot(mixed,mixed));assert ray==F(saved['mixed_Rayleigh']) and ray<initial
  row.update({'fixed_mix':str(t),'exact_mixed_Rayleigh':str(ray),'gap_relative_psi_display':float(ray-alpha),'improvement_display':float(initial-ray),'independent_generalized_minimum_interval':[str(lo),str(hi)]})
 else:assert saved['retained_span_dimension']==1
 rows.append(row)
out={'status':'PASS independent local current, physical tiny vectors and explicit compact automaton','rows':rows,'local_tensor_count':9,'physical_expansion_max_n':6,'safe_mixed_MPS_bond_bound':156,'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_tiny.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
