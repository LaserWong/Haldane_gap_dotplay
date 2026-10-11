import os,resource
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(60,60));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
from fractions import Fraction as F
from collections import Counter
from itertools import product
from pathlib import Path
import json,math,time,hashlib
P=Path(__file__).resolve().parent
def inc(v,i):v=list(v);v[i]+=1;return tuple(v)
def edge(v,i):return Counter({inc(v,i):1,v:-2})
def combine(*terms):
 r=Counter()
 for k,v in terms:
  for x,c in v.items():r[x]+=k*c
 return {x:c for x,c in r.items() if c}
def labels(v,order):
 out=[]
 for i in order:out.append((v,i));v=inc(v,i)
 return out
def mirror(v):return(v[1],v[0],v[2])
def smap(i):return 1-i if i<2 else 2
def G(p):return 1-(1-p)**2/(2*p*p)
def main():
 start=time.process_time();plaquettes=0;rounds=[]
 for f,h in json.loads((P/'INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h
 accepted=json.loads((P/'snapshot/ACCEPTED_DIRECT_MANIFEST.json').read_text());assert hashlib.sha256((P/'snapshot/accepted_direct_PROOF.md').read_bytes()).hexdigest()==accepted['PROOF.md']
 for v in product(range(3),repeat=3):
  for i,j in [(0,1),(0,2),(1,2)]:
   assert combine((1,edge(inc(v,j),i)),(2,edge(v,j)))==combine((1,edge(inc(v,i),j)),(2,edge(v,i)))
   plaquettes+=1
  for i in range(3):
   lhs={mirror(k):z for k,z in edge(v,i).items()};assert lhs==dict(edge(mirror(v),smap(i)))
 for cycle in range(8):
  v=(cycle,cycle,cycle);order=[2,0,1];initial=labels(v,order);steps=[]
  for step in range(3):
   old=labels(v,order);joint=combine(*[(k,edge(*e)) for k,e in zip((4,2,1),old)])
   end=tuple(x+1 for x in v);assert joint=={end:1,v:-8}
   i=order[0];newedge=(end,i);v=inc(v,i);order=order[1:]+[i]
   assert labels(v,order)==old[1:]+[newedge]
   steps.append({'new_base':v,'axis_order':order[:],'new_last_edge':newedge,'square_base':v[0]==v[1]})
  assert v==(cycle+1,)*3 and order==[2,0,1]
  rounds.append({'cycle':cycle,'initial_edges':initial,'steps':steps})
 # Rational probability fixtures independently exercise the two same-axis inequalities.
 count=0
 for weights in product(range(1,5),repeat=4):
  z=sum(weights);w=[F(a,z) for a in weights];p=sum(a*a for a in w);nextp=sum(a**4 for a in w)/(p*p)
  assert nextp>=p and nextp>=G(p);count+=1
 # Legal exact radical fixture: b=9/10,c=41/50, sqrt(2c-1)=4/5.
 b=F(9,10);c=F(41,50);s=b*b*F(4,5);assert s>F(1,2) and c>F(1,2)
 # Replacing b sqrt(c) by b increases the nonnegative first factor; compare squares exactly.
 assert b*b*c<b*b and 2*b-1>0
 out={'status':'PASS_SQUARE_WINDOW_PROOF_AND_BASEPOINT_IDENTITIES','plaquette_symbolic_checks':plaquettes,'same_axis_rational_fixtures':count,'full_cycle_geometry':rounds,'square_bound':'a^4*(2b-1)*sqrt(2*b^2*sqrt(2c-1)-1)','numerical_g011_claim':False,'physical_replay_performed':False,'cpu_seconds':time.process_time()-start}
 (P/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
