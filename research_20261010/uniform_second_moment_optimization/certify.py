#!/usr/bin/env python3
import os,resource,time,json,hashlib,math
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1';os.sched_setaffinity(0,{6});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));start=time.process_time()
from explore import M,D,P,R,F
C=json.loads((P/'candidates.json').read_text())
def conv(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def val(p,x):return sum(c*x**i for i,c in enumerate(p))
def psd(A):
 A=[list(r) for r in A];pivs=[]
 for i in range(len(A)):
  d=A[i][i];pivs.append(d)
  if d<=0:return False,pivs
  for j in range(i+1,len(A)):
   for k in range(j,len(A)):
    A[j][k]-=A[j][i]*A[k][i]/d;A[k][j]=A[j][k]
 return True,pivs
out={'conditional_on_published_thermal_totals':True,'physical_thermal_rerun':False,'filters':{},'moment_intervals':{k:[[str(l),str(u)] for l,u in v] for k,v in M.items()}}
for name,c in C.items():
 sector=name[0];sg=1 if name[1]=='+' else -1;q=[F(str(a)) for a in c['q']];co=conv(q,q);mom=M[sector]
 B=sum(a*(u if a>=0 else l) for a,(l,u) in zip(co,mom))
 # Integer bisection followed by exact shifted-coefficient proof on entire ray.
 lo=int(c['cap']*10**10)-100;hi=lo+200
 while hi-lo>1:
  m=(lo+hi)//2;t=F(m,10**10)
  if t**4*val(q,sg*t)**2>B:hi=m
  else:lo=m
 t=F(hi,10**10);assert t**4*val(q,sg*t)**2>B
 shift=[sum(q[j]*sg**j*F(math.comb(j,k))*t**(j-k) for j in range(k,5)) for k in range(5)]
 assert all(a>0 for a in shift), (name,shift)
 # Find an exact midpoint-data obstruction to any degree4 square filter.
 mids=[(l+u)/2 for l,u in mom];H=[[mids[i+j] for j in range(5)] for i in range(5)]
 below=F(int(c['cap']*10**6)-100,10**6)
 for k in range(int(below*10**6),int(t*10**6)+1):
  b=F(k,10**6);x=sg*b;A=[[H[i][j]-x**(i+j+4) for j in range(5)] for i in range(5)];ok,piv=psd(A)
  if ok:below=b;lastpiv=piv
  else:break
 assert below<t
 out['filters'][name]={'q':list(map(str,q)),'cap':str(t),'upper_filter_sum':str(B),'exterior_margin':str(t**4*val(q,sg*t)**2-B),'positive_shift_coefficients':list(map(str,shift)),'midpoint_square_method_nonexclusion_at':str(sg*below),'residual_ldl_pivots':list(map(str,lastpiv))}
 print(name,'cap',float(t),'square nonexclusion',float(sg*below))
def cap(m,h,r):
 n=m//h;return n*h**r+(m-n*h)**r
U=F(out['filters']['J+']['cap']);V=F(out['filters']['N-']['cap']);mj=M['J'][-1][1];mn=M['N'][-1][1]
assert U>F(out['filters']['J-']['cap']) and V>F(out['filters']['N+']['cap'])
long={}
for k in [12,24,36,48,60,72,120,144]:
 z=cap(mj,U**12,k//12)+3*cap(mn,V**12,k//12)
 old=cap(F('1.0657205'),F('1.00139')**12,k//12)+3*cap(F('.2783155'),F('.872')**12,k//12)
 assert z<=old
 long[k]={'new':str(z),'new_decimal':float(z),'official_caps_recipe':float(old)}
# Largest grid lower threshold whose absence contradicts Z72>1.
lo,hi=9900000000,10000000000
while hi-lo>1:
 k=(lo+hi)//2;ell=F(k,10**10)
 if cap(mj,ell**12,6)+3*cap(mn,V**12,6)<1:lo=k
 else:hi=k
ell=F(lo,10**10);contr=1-cap(mj,ell**12,6)-3*cap(mn,V**12,6);assert contr>0
assert ell>F(out['filters']['J-']['cap']) # distinguished eigenvalue is positive
RA=lambda k:(mj-ell**12)**(k//12)+3*cap(mn,V**12,k//12)
p=1-(1+RA(36)/ell**36)**-2;q=1-(U**72+RA(72))**-2
out['long_even_moments']=long;out['dominant']={'ell':str(ell),'positive':True,'absence_contradiction_margin':str(contr),'p0':str(p),'q0':str(q),'p0_decimal':float(p),'q0_decimal':float(q)}
print('dominant',float(ell),'p,q',float(p),float(q));print('traces',{k:v['new_decimal'] for k,v in long.items()})
out['cpu_seconds']=time.process_time()-start
(P/'certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS exact rational certificate; CPU',out['cpu_seconds'])
