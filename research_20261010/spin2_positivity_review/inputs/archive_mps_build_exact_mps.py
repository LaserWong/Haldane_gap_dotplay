"""Exact spin-2 periodic MPS contractions from rounded reduced coefficients.
All entries after rounding are integers. SU(2) highest-weight reduction is
checked by exact intertwining identities, not assumed from floating point.
"""
from pathlib import Path
from math import comb, lcm, gcd
import sympy as sy
from sympy.physics.wigner import clebsch_gordan
import numpy as np
import json,argparse,time
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--prefix',default='mps48');p.add_argument('--scale',type=int,default=10**8);p.add_argument('--from-json',action='store_true',help='Validate the recorded integer tensor without redoing any floating-point rounding')
args=p.parse_args()
if args.from_json:
 source=json.loads((ROOT/(args.prefix+'_integer_tensor.json')).read_text());st={'N':source['N_search']}
 reps=source['virtual_spins'];pars=[];allowed=[]
else:
 st=np.load(ROOT/(args.prefix+'_state.npz'))
 reps=[int(x) for x in st['reps']];pars=st['params'];allowed=[tuple(map(int,x)) for x in st['allowed']]
lab=[(a,j,m) for a,j in enumerate(reps) for m in range(-j,j+1)];D=len(lab);C=[comb(4,r) for r in range(5)]
# Virtual gauge D_j(m)=sqrt(binomial(2j,j+m)).
B=np.zeros((5,D,D),dtype=object);records=[];t0=time.time()
cache={}
if args.from_json:
 B=np.array(source['B_integer'],dtype=object);records=source['reduced_parameters']
 assert B.shape==(5,D,D)
for (a,b),pval in zip(allowed,pars):
 j,k=reps[a],reps[b]
 if (j,k) not in cache:
  vv={}
  for mu in range(-j,j+1):
   for m in range(-2,3):
    nu=mu+m
    if abs(nu)>k:continue
    cg=clebsch_gordan(j,2,k,mu,m,nu)
    if cg:
     vv[m,mu,nu]=sy.simplify(cg*sy.sqrt(sy.Rational(comb(2*k,k+nu),comb(2*j,j+mu)))/sy.sqrt(C[m+2]))
  base=next(iter(vv.values()));rr={x:sy.simplify(v/base) for x,v in vv.items()}
  assert all(v.is_Rational for v in rr.values())
  den=lcm(*(int(v.q) for v in rr.values()));ri={x:int(v*den) for x,v in rr.items()}
  cache[j,k]=(base,den,ri)
 base,den,ri=cache[j,k];q=int(round(args.scale*float(pval)*float(base)/den))
 records.append({'a':a,'b':b,'j':j,'k':k,'integer_reduced_coefficient':q,'cg_base':str(base),'denominator':den})
 ii={(jj,mu):i for i,(aa,jj,mu) in enumerate(lab) if aa==a};jj={(kk,nu):i for i,(bb,kk,nu) in enumerate(lab) if bb==b}
 for (m,mu,nu),v in ri.items():B[m+2,ii[j,mu],jj[k,nu]]=q*v
BB=[[B[r]@B[s] for s in range(5)] for r in range(5)]
charges=np.array([m for a,j,m in lab]);diff=(charges[:,None]-charges[None,:]).ravel()
weights=np.array([comb(2*j,j+m) for a,j,m in lab],dtype=object)
blocks=[];allnorm=[]
for J in range(2*max(reps)+1):
 ids=np.flatnonzero(diff==J);da=len(ids);ii=ids//D;kk=ids%D
 # Exact magnetic block of the transfer and the bilinear energy insertion.
 T=np.zeros((da,da),dtype=object);O=T.copy()
 for r in range(5):T+=C[r]*(B[r][np.ix_(ii,ii)]*B[r][np.ix_(kk,kk)])
 for r in range(5):
  for s in range(5):
   coef=(r-2)*(s-2)*C[r]*C[s]
   if coef:O+=coef*(BB[r][s][np.ix_(ii,ii)]*BB[r][s][np.ix_(kk,kk)])
 for r in range(4):
  for s in range(1,5):
   coef=C[r]*C[s]*(4-r)*s
   assert coef%2==0;coef//=2
   X=BB[r][s];Y=BB[r+1][s-1]
   O+=coef*(X[np.ix_(ii,ii)]*Y[np.ix_(kk,kk)]+Y[np.ix_(ii,ii)]*X[np.ix_(kk,kk)])
 # One exact highest-weight vector for each virtual irrep pair containing J.
 vecs=[]
 for a,j in enumerate(reps):
  for b,k in enumerate(reps):
   if not abs(j-k)<=J<=j+k:continue
   pos=[u for u,(i,z) in enumerate(zip(ii,kk)) if lab[i][0]==a and lab[z][0]==b]
   v=[]
   for u in pos:
    mu=lab[ii[u]][2];nu=lab[kk[u]][2]
    x=(-1)**(k-nu)*clebsch_gordan(j,k,J,mu,-nu,J)/sy.sqrt(comb(2*j,j+mu)*comb(2*k,k+nu))
    v.append(sy.simplify(x))
   base=next(x for x in v if x!=0);rr=[sy.simplify(x/base) for x in v]
   assert all(x.is_Rational for x in rr)
   den=lcm(*(int(x.q) for x in rr));r=np.array([int(x*den) for x in rr],dtype=object)
   gg=gcd(*(int(abs(x)) for x in r));r=r//gg
   pos=np.array(pos);w=weights[ii[pos]]*weights[kk[pos]];lv=w*r;norm=int(np.sum(lv*r))
   vecs.append((pos,r,lv,norm,a,b));allnorm.append(norm)
 m=len(vecs);Tr=np.zeros((m,m),dtype=object);Or=Tr.copy()
 for v,(pos,r,lv,norm,a,b) in enumerate(vecs):
  tr=T[:,pos]@r;orr=O[:,pos]@r
  for u,(po,rr,ll,nn,_,_) in enumerate(vecs):
   tn=int(ll@tr[po]);on=int(ll@orr[po]);Tr[u,v]=tn;Or[u,v]=on
   assert all(nn*tr[po]==rr*tn),('T covariance failed',J,u,v)
   assert all(nn*orr[po]==rr*on),('O covariance failed',J,u,v)
 blocks.append((J,Tr,Or,[v[3] for v in vecs]))
 print('J',J,'magnetic dim',da,'reduced dim',m,'exact covariance passed','t',time.time()-t0,flush=True)
assert sum((2*J+1)*len(norms) for J,T,O,norms in blocks)==D*D
Q=lcm(*allnorm)
out=ROOT/(args.prefix+'_exact_blocks.txt')
with out.open('w') as f:
 f.write(str(len(blocks))+'\n')
 for J,T,O,norms in blocks:
  f.write(f'{J} {len(norms)}\n')
  for M,isO in [(T,False),(O,True)]:
   for row,norm in zip(M,norms):
    fac=(Q**2 if isO else Q)//norm
    f.write(' '.join(str(int(x)*fac) for x in row)+'\n')
meta={'physical_spin':2,'bond_dimension':D,'N_search':int(st['N']),'virtual_spins':reps,'reduced_rounding_scale':args.scale,'projection_scale':str(Q),'physical_weights':C,'reduced_parameters':records,'B_integer':B.tolist(),'highest_weight_dims':[len(x[3]) for x in blocks],'exact_covariance_checks':'PASS'}
(ROOT/(args.prefix+'_integer_tensor.json')).write_text(json.dumps(meta,indent=2))
print('WROTE',out,'scale',Q,'seconds',time.time()-t0,flush=True)
