"""Exact vacuum/two-triplet singlet orbits and a small Rayleigh-only extension."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
import sys,json,math,time,resource
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OLD=HERE.parent/'chain_numerator_krylov_025'
sys.path.insert(0,str(HERE.parent/'chain_frontier_review'));import independent_core as C
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(590,600));START=time.process_time()
def wt(key):return math.prod(C.W[(key>>(4*i))&15] for i in range(8))
def energy(key):return sum(C.EX[(key>>(4*i))&15] for i in range(8))
def mag(key):return sum(C.MAG[(key>>(4*i))&15] for i in range(8))
def translated(v):return {((k<<4)&0xffffffff)|(k>>28):x for k,x in v.items()}
def reflected(v):
 out={}
 for k,x in v.items():
  labels=[(k>>(4*i))&15 for i in range(8)];key=sum(z<<(4*(7-i)) for i,z in enumerate(labels));out[key]=x*(-1)**sum(z in [1,2,3] for z in labels)
 return out
def total_spin_action(v,op):
 out=defaultdict(F)
 for k,x in v.items():
  for site in range(8):
   src=(k>>(4*site))&15
   for dst in range(9):
    c=C.OPS[0,op][dst][src]+C.OPS[1,op][dst][src]
    if c:out[(k&~(15<<(4*site)))|(dst<<(4*site))]+=x*c
 return {k:x for k,x in out.items() if x}
bs=[{0:1}];orbits=[]
for sep in [1,2,3,4]:
 pairs=sorted({tuple(sorted((i,(i+sep)%8))) for i in range(8)});v={}
 for i,j in pairs:
  for a,b,c in [(1,3,1),(2,2,-1),(3,1,1)]:v[(a<<(4*i))|(b<<(4*j))]=c
 bs.append(v);orbits.append(dict(separation=sep,pairs=pairs,orbit_size=len(pairs)))
assert [len(x) for x in bs]==[1,24,24,24,12]
for j,v in enumerate(bs):
 assert translated(v)==v and reflected(v)==v and not total_spin_action(v,'+') and not total_spin_action(v,'-')
 assert all(mag(k)==0 and energy(k)==(0 if j==0 else 2) for k in v)
assert sum(len(v) for v in bs)==85
# Full physical action of every new bare vector, including all leakage.
g=F(1,4);den=math.lcm(*((g*c).denominator for row in C.K.values() for _,_,c in row));kernel={key:[(a,b,int(den*g*c)) for a,b,c in row] for key,row in C.K.items()}
def action(v):
 out=defaultdict(int)
 for key,x in v.items():
  out[key]+=den*(-16+energy(key))*x
  for right in range(8):
   left=(right+7)%8;ls,rs=4*left,4*right
   for a,b,c in kernel[(key>>ls)&15,(key>>rs)&15]:out[(key&~((15<<ls)|(15<<rs)))|(a<<ls)|(b<<rs)]+=c*x
 return {k:x for k,x in out.items() if x}
images=[action(v) for v in bs];need=set().union(*map(set,bs),*map(set,images));large=[]
for name,skip in [('packed_input.txt',82),('packed_old_direction.txt',82),('full_image.txt',0),('second_image.txt',0)]:
 vals={}
 with (OLD/name).open() as f:
  for _ in range(skip):next(f)
  for line in f:
   a,b=line.split();key=int(a)
   if key in need:vals[key]=int(b)
 large.append(vals)
def dot(a,b):return sum(wt(k)*x*b.get(k,0) for k,x in a.items())
old=json.loads((OLD/'rayleigh_four.json').read_text());G=[[F(0)]*9 for _ in range(9)];H=[[F(0)]*9 for _ in range(9)]
for i in range(4):
 for j in range(4):G[i][j]=F(old['Gram'][i][j]);H[i][j]=F(old['H'][i][j])
for i in range(5):
 for j in range(5):G[4+i][4+j]=F(dot(bs[i],bs[j]));H[4+i][4+j]=F(dot(bs[i],images[j]),den)
 for j in range(4):G[j][4+i]=G[4+i][j]=F(dot(bs[i],large[j]));H[j][4+i]=H[4+i][j]=F(dot(images[i],large[j]),den)
assert G==list(map(list,zip(*G))) and H==list(map(list,zip(*H)))
assert [G[i][i] for i in range(4,9)]==list(map(F,[6561,69984,69984,69984,34992]))
def ldl(M):
 n=len(M);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
 for i in range(n):
  d=M[i][i]-sum(L[i][k]**2*D[k] for k in range(i));D.append(d)
  if not d:return L,D
  for j in range(i+1,n):L[j][i]=(M[j][i]-sum(L[j][k]*L[i][k]*D[k] for k in range(i)))/d
 return L,D
_,Dold=ldl([[G[i][j] for j in [0,1,4,5,6,7,8]] for i in [0,1,4,5,6,7,8]]);assert len(Dold)==7 and min(Dold)>0
L,D=ldl(G);assert len(D)==9 and min(D)>0 # No new direction is already in the old four-dimensional span.
n=9;Li=[[F(0)]*n for _ in range(n)]
for j in range(n):
 for i in range(n):Li[i][j]=F(i==j)-sum(L[i][k]*Li[k][j] for k in range(i))
B=list(map(list,zip(*Li)));rec=json.loads((HERE.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];rho=F(rec['large']['exact_rayleigh']);K=[[H[i][j]-rho*G[i][j] for j in range(n)] for i in range(n)];KK=[[sum(B[i][a]*K[i][j]*B[j][b] for i in range(n) for j in range(n)) for b in range(n)] for a in range(n)];sc=np.sqrt([float(x) for x in D]);nf=np.array(KK,dtype=float)/np.outer(sc,sc);assert np.max(np.abs(nf-nf.T))<1e-9
es,v=eigh(nf);aa=v[:,0]/sc;aa/=max(abs(aa));aa=list(map(lambda x:F(float(x)),aa));c=[sum(B[i][j]*aa[j] for j in range(n)) for i in range(n)]
bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(n) for j in range(n));norm=bil(G);assert norm>0;new=bil(H)/norm;target=2*F(rec['small']['exact_rayleigh'])+F(19,1250);_,tp=ldl([[H[i][j]-target*G[i][j] for j in range(n)] for i in range(n)]);excluded=len(tp)==n and min(tp)>0
out=dict(status='EXACT_NUMERATOR_CANDIDATE_PENDING_INDEPENDENT_REVIEW',g='1/4',bare_sector_dimension=5,old_saved_span_dimension=2,old_krylov_span_dimension=4,combined_trial_dimension=9,old_two_span_union_bare_rank=7,old_four_span_union_bare_rank=9,intersection_with_bare_sector_dimension=0,orbits=orbits,bare_vectors=[[[k,str(x)] for k,x in sorted(v.items())] for v in bs],bare_H_images_scaled=[[[k,str(x)] for k,x in sorted(v.items())] for v in images],H_integer_denominator=den,bare_support_union=85,bare_action_union=len(set().union(*map(set,images))),old_vector_values_on_needed_support=[[[k,str(x)] for k,x in sorted(v.items())] for v in large],needed_support_size=len(need),Gram=[[str(x) for x in r] for r in G],H=[[str(x) for x in r] for r in H],Gram_LDL_pivots=list(map(str,D)),old_two_union_Gram_LDL_pivots=list(map(str,Dold)),coefficients=list(map(str,c)),exact_rayleigh=str(new),improvement_from_original=str(rho-new),improvement_display=float(rho-new),increment_over_four_span=str(F(old['exact_rayleigh'])-new),increment_display=float(F(old['exact_rayleigh'])-new),new_delta=str(new-2*F(rec['small']['exact_rayleigh'])),new_delta_display=float(new-2*F(rec['small']['exact_rayleigh'])),necessary_target_rayleigh=str(target),meets_necessary_target=new<target,span_exclusion=excluded,span_target_LDL_pivots=list(map(str,tp)),cpu_seconds=time.process_time()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,contract='Exact total-spin-zero, translation-even/reflection-even bare vacuum and two-triplet separation orbits. All five add independent directions to the old4D span. New full actions only on85 bare configurations; no new large H image or residual.')
(HERE/'pair_extension.json').write_text(json.dumps(out,indent=2));print('PAIR RESULT dimension',n,'gain',float(rho-new),'extra',out['increment_display'],'delta',out['new_delta_display'],'targetmet',new<target,'spanexcluded',excluded,'cpu',out['cpu_seconds'],'rss',out['peak_rss_kib'],flush=True)
