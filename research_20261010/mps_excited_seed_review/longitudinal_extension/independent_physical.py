#!/usr/bin/env python3
"""Independent sparse local contractions and explicit physical fixtures."""
import os,resource,time,json,itertools,hashlib
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
os.sched_setaffinity(0,{sorted(os.sched_getaffinity(0))[len(os.sched_getaffinity(0))//2]})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
from pathlib import Path
from collections import defaultdict
import numpy as np
P=Path(__file__).resolve().parent
S=P/'inputs'; t0=time.process_time()
data=json.loads((S/'local_tensors.json').read_text()); A=[np.array(a,dtype=object) for a in data['A']]
assert data['physical_order']==[-1,0,1]
labels=data['labels']; assert len(labels)==26
q=[x[1]-y[1] for x in labels for y in labels]
# Check exact U(1) selection rule; closed trace forces sum m=0.
for s in range(3):
 for i,j in itertools.product(range(26),repeat=2):
  assert not A[s][i,j] or labels[j][1]-labels[i][1]==2*(s-1)
# Explicit physical single-site raising, unit matrix elements = S+/sqrt(2).
R=np.diag([-1,0,1]).astype(object)
B=[sum((R[s,t]*A[t] for t in range(3)),np.zeros((26,26),dtype=object)) for s in range(3)]

def sparse(M):return [(i,j,int(M[i,j])) for i,j in itertools.product(range(26),repeat=2) if M[i,j]]
def add_outer(out,X,Y,c):
 for i,j,a in sparse(X):
  for k,l,b in sparse(Y):out[(26*i+k,26*j+l)]+=c*a*b
# Form h directly from spin ladder identity, avoiding imported h or W.
h={}
for s,t in itertools.product(range(3),repeat=2):
 h[(s,t,s,t)]=(s-1)*(t-1)
 if s<2 and t>0:h[(s+1,t-1,s,t)]=1
 if s>0 and t<2:h[(s-1,t+1,s,t)]=1
E=[];O=[]
for v,u in itertools.product(range(2),repeat=2):
 e=defaultdict(int);o=defaultdict(int)
 for s in range(3):add_outer(e,(A,B)[u][s],(A,B)[v][s],1)
 # Enumerate each source placement on the Hamiltonian bond explicitly.
 for (s,t,x,y),c in h.items():
  for bra in ([None] if u==0 else [0,1]):
   for ket in ([None] if v==0 else [0,1]):
    X=(B[s] if bra==0 else A[s])@(B[t] if bra==1 else A[t])
    Y=(B[x] if ket==0 else A[x])@(B[y] if ket==1 else A[y])
    add_outer(o,X,Y,c*(-1 if bra==1 else 1)*(-1 if ket==1 else 1))
 E.append({k:v for k,v in e.items() if v});O.append({k:v for k,v in o.items() if v})
words=iter((S/'sources.txt').read_text().split());assert [int(next(words)) for _ in range(676)]==q
for family in (E,O):
 for expected in family:
  n=int(next(words)); actual={(int(next(words)),int(next(words))):int(next(words)) for _ in range(n)}
  assert actual==expected
assert next(words,None) is None
# Establish byte-exact agreement with the previously audited ground blocks.
lines=[str(len(set(q)))]
for charge in sorted(set(q)):
 ids=[i for i in range(676) if q[i]==charge];lines.append(f'{charge} {len(ids)}')
 for M in [E[0],O[0]]:
  for i in ids:lines.append(' '.join(str(M.get((i,j),0)) for j in ids))
assert ('\n'.join(lines)+'\n').encode()==(S/'mps_blocks.txt').read_bytes()
# Independent full physical vector construction including all 3^n words, no sector prefilter.
fixtures=[]
for n in [2,4,6]:
 vec={}
 for state in itertools.product(range(3),repeat=n):
  product=np.eye(26,dtype=object)
  for s in state: product=product@A[s]
  amp=int(np.trace(product))
  if amp:vec[state]=amp
 raised={w:amp*sum((-1)**j*(s-1) for j,s in enumerate(w)) for w,amp in vec.items()}
 raised={w:a for w,a in raised.items() if a}
 assert sum(a*raised.get(w,0) for w,a in vec.items())==0
 assert all(raised.get(w[1:]+w[:1],0)==-a for w,a in raised.items())
 row={'n':n,'states':[]}
 for name,v,charge in [('psi',vec,0),('phi_z',raised,0)]:
  assert all(sum(w)-n==charge for w in v)
  Hv=defaultdict(int)
  for w,amp in v.items():
   for j in range(n):
    k=(j+1)%n
    for (s,t,x,y),c in h.items():
     if (x,y)==(w[j],w[k]) and c:
      target=list(w);target[j]=s;target[k]=t;Hv[tuple(target)]+=c*amp
  norm=sum(a*a for a in v.values());assert norm>0
  energy=sum(a*Hv[w] for w,a in v.items())
  row['states'].append(dict(name=name,norm=str(norm),energy_numerator=str(energy),nonzero_support=len(v),H_action_support=sum(a!=0 for a in Hv.values())))
 fixtures.append(row)
expected=json.loads((S/'source_checks.json').read_text())['fixtures']
for row,saved in zip(fixtures,expected):
 z=row['states'][1]
 assert row['n']==saved['n'] and z['norm']==saved['norm'] and z['energy_numerator']==saved['H_numerator'] and z['nonzero_support']==saved['physical_support']
result={'status':'PASS','local_E_entries':[len(m) for m in E],'local_O_entries':[len(m) for m in O],'direct_fixtures':fixtures,'cpu_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_physical.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
