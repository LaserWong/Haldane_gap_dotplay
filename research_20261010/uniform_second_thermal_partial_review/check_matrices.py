#!/usr/bin/env python3
"""Rebuild physical sparse matrix digests, no matrix powers or heat columns."""
from pathlib import Path
from itertools import product
import hashlib,json,os,resource,time
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));start=time.process_time()
P=Path(__file__).resolve().parent;RUN=P/'snapshot/campaign'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':')).encode()
results=[]
for n in range(4,13):
 files=[RUN/'cases'/f'L{n}_{t}'/'case.json' for t in ('I','P')]
 if not all(p.exists() for p in files):continue
 cases=[]
 for p in files:
  o=json.loads(p.read_text());assert o['sha256']==sha(canonical(o['payload']));cases.append(o['payload'])
 cache=P/f'matrix_L{n}.json'
 if cache.exists():
  o=json.loads(cache.read_text());assert o['sha256']==sha(canonical(o['payload']));got=o['payload']
 else:
  # Base-three numeric order equals lexicographic physical word order.
  byweight=[[] for _ in range(n+1)]
  for c,w in enumerate(product((-1,0,1),repeat=n)):
   m=sum(w)
   if m>=0:byweight[m].append(c)
  powers=[3**(n-1-k) for k in range(n)];got=[]
  for m,codes in enumerate(byweight):
   idx={c:j for j,c in enumerate(codes)};d=len(codes);metas=[c['sectors'][m] for c in cases];nnz=metas[0]['nnz'];assert metas[1]['nnz']==nnz
   hs=[hashlib.sha256(f'MATRIX {n} {t} {m} {d} {nnz}\n'.encode()) for t in ('I','P')];count=0
   for i,c in enumerate(codes):
    w=[c//p%3-1 for p in powers];diag=32-3*n-2*sum(w[k]*w[(k+1)%n] for k in range(n));row=[(i,diag,diag)]
    for k in range(n):
     l=(k+1)%n
     for delta in (-1,1):
      if -1<=w[k]+delta<=1 and -1<=w[l]-delta<=1:
       cc=c+delta*(powers[k]-powers[l]);row.append((idx[cc],-2,2 if k==n-1 else -2))
    row.sort();count+=len(row)
    for j,a,b in row:hs[0].update(f'{i} {j} {a} 0\n'.encode());hs[1].update(f'{i} {j} {b} 0\n'.encode())
   assert count==nnz
   got.append({'M':m,'dimension':d,'nnz':nnz,'I_matrix_sha256':hs[0].hexdigest(),'P_matrix_sha256':hs[1].hexdigest()})
  cache.write_text(json.dumps({'payload':got,'sha256':sha(canonical(got))},indent=2)+'\n')
 for row in got:
  for t,c in zip(('I','P'),cases):
   sec=c['sectors'][row['M']];assert sec['dimension']==row['dimension'] and sec['nnz']==row['nnz'] and sec['matrix_sha256']==row[t+'_matrix_sha256']
 results.append(n);print('independent physical matrix digests PASS L',n,flush=True)
(P/'matrix_results.json').write_text(json.dumps({'status':'PASS','lengths_checked':results,'CPU_seconds':time.process_time()-start,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'no_thermal_columns':True},indent=2)+'\n');print('CPU',time.process_time()-start)
