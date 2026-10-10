#!/usr/bin/env python3
"""Fresh Python integer matrices/columns; no producer code imports or execution."""
from pathlib import Path
from itertools import product
from math import factorial,isqrt
import json,hashlib,os,resource,time
os.sched_setaffinity(0,{5});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(120,120));st=time.process_time()
P=Path(__file__).resolve().parent;A=P.with_name('uniform_second_thermal_pilot');Q=2**55
v=[98**j*(factorial(280)//factorial(j)) for j in range(281)];den=sum(v);co=[Q*x//den for x in v];assert max(j for j,c in enumerate(co) if c)==191
assert list(map(int,(A/'coefficients.txt').read_text().split()))==co
assert Q+281*(730+1)<2*Q and 76*2*Q<2**63-1 and 64*(2*Q)**2<2**128
# Python // is mathematical floor, including negative numerators.
for x in range(-1000,1001):assert (x//32)==(x//32 if x>=0 else -((-x+31)//32))
def code(w):
 z=0
 for s in w:z=3*z+s+1
 return z
def orbit(w,m):
 seen={w};todo=[w]
 while todo:
  x=todo.pop();ys=[x[1:]+x[:1],x[::-1]]
  if m==0:ys.append(tuple(-a for a in x))
  for y in ys:
   if y not in seen:seen.add(y);todo.append(y)
 return seen
records=[];matrix_tests=[];comparison=0
for n in (4,5):
 allwords=list(product((-1,0,1),repeat=n));assert len(allwords)==3**n
 for twist in ('I','P'):
  totalmult=0;W=0
  for m in range(n+1):
   ws=[w for w in allwords if sum(w)==m];index={w:j for j,w in enumerate(ws)};d=len(ws);mat=[[0]*d for _ in range(d)]
   for j,w in enumerate(ws):
    diag=sum(w[k]*w[(k+1)%n] for k in range(n));mat[j][j]=32-3*n-2*diag
    for b in range(n):
     c=(b+1)%n
     for delta in (-1,1):
      u=list(w);u[b]+=delta;u[c]-=delta
      if all(-1<=z<=1 for z in u):mat[index[tuple(u)]][j]+=2 if twist=='P' and b==n-1 else -2
   assert all(mat[i][j]==mat[j][i] for i in range(d) for j in range(d))
   assert max(sum(abs(a) for a in row) for row in mat)<=76
   # Reversal leaves seam, digit negation maps weight m to -m.
   rv=[index[w[::-1]] for w in ws];assert all(mat[rv[i]][rv[j]]==mat[i][j] for i in range(d) for j in range(d))
   # Left shift moves seam; restoring gauge on first n-1 sites has phase
   # (-1)^(sum first n-1 rotated digits). Test the signed permutation exactly.
   sh=[index[w[1:]+w[:1]] for w in ws]
   phases=[(-1)**sum((w[1:]+w[:1])[:n-1]) if twist=='P' else 1 for w in ws]
   assert all(mat[sh[i]][sh[j]]*phases[i]*phases[j]==mat[i][j] for i in range(d) for j in range(d))
   reps=[]
   for w in ws:
    orb=orbit(w,m)
    if w==min(orb):reps.append((w,len(orb)*(2 if m>0 else 1)))
   totalmult+=sum(mu for w,mu in reps)
   oldpath=A/f'L{n}_{twist}_M{m}_start0_count100000.json';old=json.loads(oldpath.read_text()) if oldpath.exists() else None
   oldmap={r['code']:(r['multiplicity'],r['norm_squared']) for r in old['records']} if old else {}
   if old:assert len(oldmap)==len(old['records'])==len(reps)
   sparse=[[(j,a) for j,a in enumerate(row) if a] for row in mat]
   for w,mu in reps:
    col=[0]*d;k=index[w]
    for cj in reversed(co):
     col=[sum(a*col[j] for j,a in row)//32 for row in sparse];col[k]+=cj
    norm=sum(a*a for a in col);W+=mu*norm
    if old:assert oldmap[code(w)]==(mu,norm);comparison+=1
    records.append({'n':n,'twist':twist,'weight':m,'code':code(w),'multiplicity':mu,'norm_squared':str(norm)})
   matrix_tests.append({'n':n,'twist':twist,'weight':m,'dimension':d,'symmetric':True,'signed_rotation_covariant':True,'reversal_covariant':True})
  assert totalmult==3**n
  print(n,twist,'W',W)
  if n==4:assert str(W) in (P.parent/'uniform_second_initialization_review/sources/thermal72.tex').read_text()
(P/'fixture_results.json').write_text(json.dumps({'status':'PASS','records':records,'matrix_tests':matrix_tests,'existing_pilot_records_exactly_matched':comparison,'CPU_seconds':time.process_time()-st,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n');print('PASS CPU',time.process_time()-st,'matched',comparison)
