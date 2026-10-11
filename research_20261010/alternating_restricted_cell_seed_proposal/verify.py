import ast,json,math,hashlib,time,sys
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(100000)
P=Path(__file__).resolve().parent;R=P.parents[1];st=time.process_time();G=10**90;inputs={}
def read(p):
 b=p.read_bytes();inputs[str(p.relative_to(R))]=hashlib.sha256(b).hexdigest();return b
def down(x):return F(x.numerator*G//x.denominator,G)
def up(x):return F(-(-x.numerator*G//x.denominator),G)
def expi(x):
 if x<0:
  l,u=expi(-x);return down(1/u),up(1/l)
 c=0
 while x>F(1,16):x/=2;c+=1
 t=s=F(1)
 for k in range(1,101):t=t*x/k;s+=t
 nx=t*x/101;l=down(s);u=up(s+nx/(1-x/102))
 for _ in range(c):l=down(l*l);u=up(u*u)
 return l,u
def root(x,k):
 assert x>=0
 if k==1:return down(x),up(x)
 lo=0;hi=G
 while F(hi,G)**k<x:hi*=2
 while hi-lo>1:
  md=(hi+lo)//2
  if F(md,G)**k<=x:lo=md
  else:hi=md
 assert F(lo,G)**k<=x<=F(hi,G)**k
 return F(lo,G),F(hi,G)
def power(x,p):
 p=F(p);return root(x**p.numerator,p.denominator)
def conv(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def shift(q,a):return [sum((q[j]*math.comb(j,i)*a**(j-i) for j in range(i,len(q))),F()) for i in range(len(q))]
def solve(A,b):
 A=[list(a)+[v] for a,v in zip(A,b)];n=len(b)
 for j in range(n):
  p=next(i for i in range(j,n) if A[i][j]);A[j],A[p]=A[p],A[j];z=A[j][j];A[j]=[x/z for x in A[j]]
  for i in range(n):
   if i!=j:
    z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[j])]
 return [a[-1] for a in A]
# Rebuild ONLY physical L=4,6,8,10,12 I/P intervals from certified printed integers.
src=R/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py'
tree=ast.parse(read(src));tab=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='B' for t in n.targets));D={}
for j,(n,c,W) in enumerate(tab):
 if n%2:continue
 x=F(49,4)*n*(F(3,2)-F(700741,500000));s=sum((x**k/F(math.factorial(k)) for k in range(101)),F());d=math.isqrt(3**n)+1;err=d*(281*(d+1)+1);rr=math.isqrt(W)
 lo=s*max(0,rr-err)**2/2**110;hi=(s+x**100/F(math.factorial(100)))*(rr+1+err)**2/2**110
 grid=10**18;D[n,j%2]=(F(lo.numerator*grid//lo.denominator,grid),F(-(-hi.numerator*grid//hi.denominator),grid))
assert sorted(D)==[(n,j) for n in [4,6,8,10,12] for j in [0,1]]
M={s:[] for s in ['J','N']}
for n in [4,6,8,10,12]:
 z,p=D[n,0],D[n,1];M['J'].append(((z[0]+3*p[0])/4,(z[1]+3*p[1])/4));M['N'].append(((z[0]-p[1])/4,(z[1]-p[0])/4))
C=json.loads(read(P/'candidates.json'));assert C['moments']=={s:[[str(x) for x in v] for v in a] for s,a in M.items()}
for folder,h in [('uniform_alternating_positive_cell_review','abb8e04fa7478e939d18c831a3a4b201c0ec6baf9b8e3e494b5b867a4347f872'),('uniform_second_thermal_full_review','792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94'),('uniform_smaller_second_initialization_review','54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f')]:
 assert hashlib.sha256(read(P.parent/folder/'MANIFEST_SHA256.json')).hexdigest()==h
 read(P.parent/folder/'PROOF.md')
U={};caps={}
def bound(q,s):return sum((c*(u if c>=0 else l) for c,(l,u) in zip(q,M[s])),F())
for s in ['J','N']:
 q=list(map(F,C['support'][s]['coeff']));U[s]=F(C['support'][s]['cap']);B=bound(conv(q,q),s);sh=shift(q,U[s]);assert min(sh)>0
 margin=U[s]**2*sh[0]**2-B;assert margin>0
 caps[s]={'cap':str(U[s]),'q':list(map(str,q)),'filter_sum_upper':str(B),'ray_margin':str(margin),'positive_shift_coefficients':list(map(str,sh))}
# Exact degree-four Hermite upper envelope on [0,U]. f=x^(k-2), f^(5)>=0;
# f-p = f^(5)(xi)/5! (x-a)^2(x-b)^2(x-U) <=0.
def hermite(s,k,cap):
 a,b=map(F,C['nodes'][s]);assert 0<a<b<cap;d=k-2;A=[];rhs=[]
 for x in [a,b]:
  A.append([x**j for j in range(5)]);rhs.append(x**d)
  A.append([F(0)]+[j*x**(j-1) for j in range(1,5)]);rhs.append(d*x**(d-1))
 A.append([cap**j for j in range(5)]);rhs.append(cap**d);q=solve(A,rhs)
 for v,z in zip(A,rhs):assert sum(x*y for x,y in zip(q,v))==z
 return q,bound(q,s)
long={}
for s in ['J','N']:
 for k in [15,16,17,30,32,34]:
  q,B=hermite(s,k,U[s]);long[f'{s}{k}']={'coeff':list(map(str,q)),'bound':str(B),'display':float(B)}
  print('majorant',s,k,float(B),flush=True)
# Anchors only read, never recomputed.
ints={}
for f in ['anchors.out','anchor60.out']:
 ints.update({k:int(v) for line in read(P.parent/'uniform_smaller_second_initialization'/f).decode().splitlines() for k,v in [line.split('=')]})
rows=[]
for n in [15,16,17]:
 L=4*n;N=ints[f'N0_{L}'];H=ints[f'H0_{L}'];assert N>0;R0=F(H,N)+L*F(700741,500000);assert R0<0
 zlow=expi(-F(49,4)*R0)[0];nup=F(long[f'N{2*n}']['bound']);Q=F(long[f'J{2*n}']['bound'])+3*nup
 lo=990000000;hi=int(U['J']*10**9)
 def pack(m,h,r):
  ct=m//h;return up(ct*power(h,r)[1]+power(m-ct*h,r)[1])
 while hi-lo>1:
  mid=(lo+hi)//2;ell=F(mid,10**9);q,b=hermite('J',2*n,ell)
  if min(b,pack(M['J'][-1][1],ell**6,F(n,3)))+3*nup<zlow:lo=mid
  else:hi=mid
 ell=F(lo,10**9);fq,fb0=hermite('J',2*n,ell);fb=min(fb0,pack(M['J'][-1][1],ell**6,F(n,3)));forcing=zlow-fb-3*nup;assert forcing>0
 residual=M['J'][-1][1]-ell**6;assert residual>0
 tail=power(residual,F(n,6))[1]+3*F(long[f'N{n}']['bound']);S=down((1+tail/ell**n)**-2);T=down(expi(-F(49,2)*R0)[0]/Q**2)
 print('seed',n,'ell',float(ell),'R',float(R0),'tail',float(tail),'Q',float(Q),'S',float(S),'T',float(T),flush=True)
 s,t=S,T;beta=F(49,4);states=[];success=False;why=None
 gap=F(1,1000)
 for j in range(16):
  Cpos=down(min(s*root(t,2)[0],t));e=expi(beta*gap)[1];margin=Cpos-e*(1-Cpos);u=max(1-s,1-t)
  states.append({'cell_base':n*2**j,'beta':str(beta),'S':str(s),'T':str(t),'Cpos':str(Cpos),'gap_margin':str(margin),'display':[float(s),float(t),float(Cpos)]})
  print('state',n,j,float(s),float(t),float(Cpos),flush=True)
  if margin<=0:why='positive_window_fails';break
  if u<=F(1,100) and 5*u*e<1:success=True;why='positive_window_and_small_defect_close';break
  g=lambda x:1-(1-x)**2/(2*x*x)
  s=down(g(down(s*s*t)))
  if s<=0:why='spatial_recurrence_nonpositive';break
  t=down(g(down(t*t*s)))
  if t<=0:why='thermal_recurrence_nonpositive';break
  beta*=2
 rows.append({'cell_seed':n,'physical_seed':2*n,'anchor_length':L,'anchor_R':str(R0),'anchor_Z_beta_lower':str(zlow),'ell':str(ell),'forcing_coeff':list(map(str,fq)),'forcing_bound':str(fb),'forcing_hermite_bound':str(fb0),'forcing_method':'minimum of Hermite and exact unit-mass convex packing','forcing_margin':str(forcing),'tail':str(tail),'Q':str(Q),'S':str(S),'T':str(T),'gap_test':str(gap),'closed':success,'status':why,'states':states})
out={'status':'RESTRICTED_INPUT_EXACT_PRODUCER','physical_lengths_used':[4,6,8,10,12],'cell_moment_orders':[2,3,4,5,6],'odd_physical_moments_used':False,'moments':{s:[[str(x) for x in v] for v in a] for s,a in M.items()},'supports':caps,'hermite_nodes':C['nodes'],'majorants':long,'rows':rows,'internal_cpu_seconds':time.process_time()-st}
(P/'certificate.json').write_text(json.dumps(out,indent=2)+'\n');(P/'INPUT_SHA256.json').write_text(json.dumps(inputs,indent=2)+'\n');print('DONE',out['internal_cpu_seconds'],flush=True)
