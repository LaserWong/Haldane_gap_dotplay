import os,resource
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(30,30));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
from collections import defaultdict
from itertools import product
import json,time
from pathlib import Path

def add(*terms):
 d=defaultdict(int)
 for s,v in terms:
  for k,x in v.items():d[k]+=s*x
 return {k:x for k,x in d.items() if x}
def inner(a,b):return sum(v*b.get(k,0) for k,v in a.items())
class Model:
 def __init__(self,L,W):
  self.n=L*W;self.edges=[]
  for y in range(W):
   for x in range(L):
    i=x*W+y
    self.edges.extend([(i,((x+1)%L)*W+y),(i,x*W+(y+1)%W)])
 def op(self,v,kind):
  out=defaultdict(int)
  for s,w in v.items():
   if kind=='Q':out[s]+=w*sum(bool((s>>(2*i))&3) for i in range(self.n));continue
   for i,j in self.edges:
    a=(s>>(2*i))&3;b=(s>>(2*j))&3
    if kind=='up' and a==b==0:
     for c in (1,2,3):out[s|(c<<(2*i))|(c<<(2*j))]+=w
    elif kind=='down' and a==b and a:
     out[s^(a<<(2*i))^(a<<(2*j))]+=w
    elif kind=='D':
     if bool(a)!=bool(b):out[s^((a^b)<<(2*i))^((a^b)<<(2*j))]+=w
     elif a and b:
      out[s^((a^b)<<(2*i))^((a^b)<<(2*j))]+=w
      if a==b:
       z=s^(a<<(2*i))^(b<<(2*j))
       for c in (1,2,3):out[z|(c<<(2*i))|(c<<(2*j))]-=w
  return {s:w for s,w in out.items() if w}
 def chain(self,v,*ops):
  for op in reversed(ops):v=self.op(v,op)
  return v
 def K(self,v):return add((1,self.chain(v,'down','up')),(-1,self.chain(v,'up','down')))
 def E(self,v):return add((1,self.chain(v,'D','up')),(-1,self.chain(v,'up','D')))
 def Edag(self,v):return add((1,self.chain(v,'down','D')),(-1,self.chain(v,'D','down')))
 def N(self,v):return add((1,self.op(self.E(v),'down')),(-1,self.E(self.op(v,'down'))))
 def L(self,v):
  return add((1,self.op(self.K(self.op(v,'up')),'down')),(-1,self.K(self.chain(v,'down','up'))),(-1,self.op(self.op(self.K(v),'down'),'up')),(1,self.op(self.K(self.op(v,'down')),'up')))
 def EE(self,v):return add((1,self.Edag(self.E(v))),(-1,self.E(self.Edag(v))))
 def H(self,v):return add((200,self.op(v,'Q')),(11,self.op(v,'D')),(11,self.op(v,'up')),(11,self.op(v,'down')))

def local_physical_check():
 # Unnormalized s,tx,ty,tz each have norm²2, in spin bits (up,down).
 rung=[{1:1,2:-1},{3:1,0:-1},{0:1j,3:1j},{1:1,2:1}]
 B=[{x+4*y:a*b for x,a in rung[i].items() for y,b in rung[j].items()} for j in range(4) for i in range(4)]
 h=Model(2,1);h.edges=[(0,1)]
 def swap(k,i,j):return k^(((k>>i&1)^(k>>j&1))<<i)^(((k>>i&1)^(k>>j&1))<<j)
 for k,v in enumerate(B):
  z=defaultdict(complex)
  for state,a in v.items():
   z[swap(state,0,2)]+=a;z[swap(state,1,3)]+=a;z[state]-=a
  exact=add((1,h.op({k:1},'up')),(1,h.op({k:1},'down')),(1,h.op({k:1},'D')))
  for j,b in enumerate(B):
   val=sum(a.conjugate()*z.get(state,0) for state,a in b.items())/4
   assert val==exact.get(j,0),(j,k,val,exact.get(j,0))
 return True

def fixture(L,W):
 h=Model(L,W)
 def paired(pairs):
  d={}
  for colors in product((1,2,3),repeat=len(pairs)):
   state=sum(c<<(2*i) for pair,c in zip(pairs,colors) for i in pair);d[state]=1
  return d
 m=add((-1,paired([(0,1),(2,3),(4,5)])),(2,paired([(0,2),(1,3),(4,6)])))
 # This localized tensor is a product of three Cartesian singlet-pair contractions.
 cm=h.op(m,'down');dm=h.op(m,'D');km=h.K(m);upm=h.op(m,'up');nm=h.N(m)
 terms3=[2*inner(cm,h.op(dm,'down')),-inner(cm,h.op(cm,'D')),inner(km,dm),inner(m,nm)]
 direct3=inner(upm,h.op(upm,'D'));assert sum(terms3)==direct3
 terms10=[inner(add((1,h.op(cm,'up')),(1,km)),add((1,h.op(cm,'up')),(1,km))),2*inner(cm,h.op(km,'down')),-inner(cm,h.K(cm)),inner(km,km),inner(m,h.L(m))]
 up2=h.op(upm,'up');direct10=inner(up2,up2);assert sum(terms10)==direct10
 # Integer T=200Q+11A. chi=T psi; q8 chi=11Cdagger m.
 psi=add((3,{0:1}),(-2,paired([(0,1)])),(1,paired([(0,1),(2,3)])),(1,m));chi=h.H(psi);chi6={s:v for s,v in chi.items() if sum(bool((s>>(2*i))&3) for i in range(h.n))==6}
 vv=add((17600,m),(11,chi6),(121,dm));em=h.E(m);cv=h.op(vv,'down');kv=h.K(vv);edm=h.Edag(m)
 cross_ECM=242*inner(vv,h.E(cm));cross_N=242*inner(vv,nm);assert cross_ECM+cross_N==242*inner(vv,h.op(em,'down'))
 terms8=[inner(cv,cv),inner(vv,kv),242*inner(vv,h.op(em,'down')),14641*inner(edm,edm),14641*inner(m,h.EE(m))]
 q8=add((1,h.op(vv,'up')),(121,em));assert sum(terms8)==inner(q8,q8)
 sectors={q:{s:v for s,v in chi.items() if sum(bool((s>>(2*i))&3) for i in range(h.n))==q} for q in range(0,h.n+1,2)}
 gamma=add((1,h.op(cm,'up')),(1,km));assert gamma==h.op(upm,'down')
 normal3=sum(200*q*inner(v,v) for q,v in sectors.items())+11*sum(inner(v,h.op(v,'D')) for q,v in sectors.items() if q<=6)+1331*sum(terms3)+22*sum(inner(sectors[q-2],h.op(sectors[q],'down')) for q in (2,4,6))+242*inner(chi6,gamma)
 direct=h.H(chi);assert normal3==inner(chi,direct)
 parts={q:{s:v for s,v in direct.items() if sum(bool((s>>(2*i))&3) for i in range(h.n))==q} for q in range(0,h.n+1,2)}
 assert parts.get(8,{})==q8 and parts.get(10,{})==add((121,up2))
 for q in (0,2,4,6):
  lower=add((200*q,sectors[q]),(11,h.op(sectors[q],'D')),(11,h.op(sectors.get(q-2,{}),'up')),(121,gamma)) if q==6 else add((200*q,sectors[q]),(11,h.op(sectors[q],'D')),(11,h.op(sectors.get(q-2,{}),'up')),(11,h.op(sectors.get(q+2,{}),'down')))
  assert lower==parts[q]
 m4=inner(direct,direct);normlower=sum(inner(v,v) for q,v in parts.items() if q<=6)
 assert m4==normlower+sum(terms8)+14641*sum(terms10)
 if h.n>=10:assert direct10>0
 return dict(shape=[L,W],m_norm=inner(m,m),m3_q8_terms=terms3,m3_q8_direct=direct3,q10_terms=terms10,q10_direct=direct10,q8_terms=terms8,q8_cross_ECM=cross_ECM,q8_cross_nested=cross_N,q8_direct=inner(q8,q8),integer_T200_11_moments=[inner(psi,psi),inner(psi,chi),inner(chi,chi),inner(chi,direct),m4],support_sizes=dict(m=len(m),chi=len(chi),H2psi=len(direct)),all_oriented_terms_equal=True,normal_m3=normal3,sector_H2_norms={str(q):inner(v,v) for q,v in parts.items()})
def sumvec(m,a,b,c):
 s=sum(x<<(2*i) for i,x in enumerate((a,a,b,b,c,c)));m[s]=1;return m
if __name__=='__main__':
 start=time.monotonic();out={'local_physical_spin_half_check':local_physical_check(),'results':[fixture(4,2),fixture(5,2)],'seconds':time.monotonic()-start,'cpu_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};Path(__file__).with_name('independent.json').write_text(json.dumps(out,indent=2)+'\n');print(out['seconds'],out['peak_rss_kib'])
