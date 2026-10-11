import os,resource
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(60,60));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import product
import hashlib,json
P=Path(__file__).resolve().parent
def inc(v,i):v=list(v);v[i]+=1;return tuple(v)
def edge(v,i):return {inc(v,i):1,v:-2}
def combine(*terms):
 d=Counter()
 for k,v in terms:
  for x,c in v.items():d[x]+=k*c
 return {x:c for x,c in d.items() if c}
def G(z):return 1-(1-z)**2/(2*z*z)
m=P/'snapshot/MANIFEST_SHA256.json';assert hashlib.sha256(m.read_bytes()).hexdigest()=='890e942c8a7e37cbefc5b8de52f40f8d61cbfefe76e03f8a71f9dec8d66648cc'
assert hashlib.sha256((P/'snapshot/PROOF.md').read_bytes()).hexdigest()==json.loads(m.read_text())['PROOF.md']
rows=[]
for j in range(8):
 oldc=((j+1,j,j+1),1);mirroredc=((j,j+1,j+1),0);ap=((j+1,j+1,j+1),2);tsmall=((j,j+1,j+1),2);d=((j,j+1,j+2),0);bp=((j+1,j+1,j+2),0);cp=((j+2,j+1,j+2),1)
 assert {(k[1],k[0],k[2]):v for k,v in edge(*oldc).items()}==edge(*mirroredc)
 assert combine((1,edge(*d)),(2,edge(*tsmall)))==combine((1,edge(*ap)),(2,edge(*mirroredc)))
 assert (inc(d[0],0),0)==bp
 assert combine((4,edge(*oldc)),(2,edge(*ap)),(1,edge(*bp)))=={cp[0]:1,oldc[0]:-8}
 rows.append(dict(cycle=j,new_a_edge=ap,reflected_c_edge=mirroredc,time_transported_x_edge=d,new_b_edge=bp,new_c_edge=cp))
count=0
for a,b,c in product((F(9,10),F(19,20),F(99,100)),repeat=3):
 ap=G(a**4*b*b*c)
 if ap<=0:continue
 oldb=G(ap*b**4*c*c);bp=G(ap*c*c)
 assert bp>=oldb
 if oldb>0:
  assert G(c**4*ap*ap*bp)>=G(c**4*ap*ap*oldb);count+=1
out=dict(status='PASS_EXACT_SQUARE_PRESERVING_STRENGTHENED_RECURRENCE',geometric_cycles=rows,rational_dominance_fixtures=count,new_g011_claim=False)
(P/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
