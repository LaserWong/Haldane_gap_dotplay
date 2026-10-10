#!/usr/bin/env python3
"""Rebuild source cells by physical matrix action, not monomial word recipes."""
import os,resource,time,itertools,json
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1');os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;t0=time.process_time();d=json.loads((P/'inputs/local_tensors.json').read_text());A=[np.array(m,dtype=object) for m in d['A']];q=[x[1]-y[1] for x in d['labels'] for y in d['labels']]
R=np.array([[0,0,0],[1,0,0],[0,1,0]],dtype=object);L=R.T;M=np.diag([-1,0,1]).astype(object);I=np.eye(3,dtype=object);h=np.kron(M,M)+np.kron(R,L)+np.kron(L,R);J=h@np.kron(R,I)-np.kron(R,I)@h
specs=[(1,None,None),(1,('R',0),None),(2,('J',0),None),(2,None,('J',0)),(2,('J',0),('J',0)),(2,('R',0),('J',0)),(2,('R',1),('J',0)),(3,('J',0),('J',1)),(3,('J',1),('J',0))]
def embed(op,start,width,n):
 before=np.eye(3**start,dtype=object);after=np.eye(3**(n-start-width),dtype=object);return np.kron(np.kron(before,op),after)
results=[];total_entries=0
with (P/'inputs/fused/cells.txt').open() as f:
 assert list(map(int,f.readline().split()))==q and int(f.readline())==len(specs)
 for cell,(n,bra,ket) in enumerate(specs):
  assert list(map(int,f.readline().split()))==[cell,n]
  states=list(itertools.product(range(3),repeat=n));words=[]
  for state in states:
   word=np.eye(26,dtype=object)
   for s in state:word=word@A[s]
   words.append(word)
  def act(spec):
   if spec is None:return words
   kind,start=spec;operator=embed(R if kind=='R' else J,start,1 if kind=='R' else 2,n)
   return [sum((int(operator[i,j])*words[j] for j in range(len(states)) if operator[i,j]),np.zeros((26,26),dtype=object)) for i in range(len(states))]
  wb,wk=act(bra),act(ket)
  hint=sum((embed(h,j,2,n) for j in range(n-1)),np.zeros((3**n,3**n),dtype=object))
  observables=[np.eye(3**n,dtype=object),hint]+[embed(op,0,1,n) for op in [M,R,L]]+[embed(op,n-1,1,n) for op in [M,R,L]]
  counts=[];maximum=0
  for obs in observables:
   shift,nz=map(int,f.readline().split());matrix=np.zeros((676,676),dtype=object)
   for i,j in itertools.product(range(3**n),repeat=2):
    if obs[i,j]:matrix+=int(obs[i,j])*np.kron(wb[i],wk[j])
   actual=0
   for i in range(676):
    for j in range(676):
     if matrix[i,j]:
      actual+=1;maximum=max(maximum,abs(int(matrix[i,j])));assert q[j]-q[i]==2*shift
   assert actual==nz
   for _ in range(nz):
    i,j,v=map(int,f.readline().split());assert int(matrix[i,j])==v;matrix[i,j]=0
   assert not any(matrix.flat)
   counts.append(nz);total_entries+=nz
  assert maximum<2**63
  results.append({'cell_id':cell,'length':n,'entry_counts':counts,'max_abs_entry':str(maximum)})
  print('cell',cell,'PASS',flush=True)
 assert not f.read().strip()
metadata=json.loads((P/'inputs/fused/cell_metadata.json').read_text())
for a,b in zip(results,metadata['cells']):assert a['entry_counts']==b['nonzero_counts'] and a['max_abs_entry']==b['max_abs_entry']
out={'status':'PASS independent physical-matrix reconstruction of all72 cell transfers','cells':results,'verified_nonzero_entries':total_entries,'CPU_seconds':time.process_time()-t0,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_cells.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
