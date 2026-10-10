"""Independent large-seed audit. No producer Python modules are imported.
Frozen earlier independent physical kernel and independently sealed geometry are reused by hash.
This file specializes the independent large-seed auditor to the new coupling 3/50.
"""
import os,resource
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
resource.setrlimit(resource.RLIMIT_AS,(1536*1024**2,1536*1024**2))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,itertools,time,gzip,hashlib,importlib.util
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import numpy as np
PRIOR=Path(__file__).resolve().parent.parent/'large_seed_review'
sys.path.insert(0,str(PRIOR))
from rebuild_geometry import graph
OUT=Path(__file__).resolve().parent;ROOT=PRIOR/'snapshot';RESEARCH=ROOT/'research_20261010';GROUND=OUT/'snapshot';BAND=OUT/'snapshot';REF=BAND
spec=importlib.util.spec_from_file_location('frozen_independent_kernel',RESEARCH/'low_band_review/independent_review.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
KERNEL=core.KERNEL;inertia=core.inertia_fraction

def save(name,obj):
 (OUT/'results'/name).write_text(json.dumps(obj,indent=2)+'\n')
def load(path):return json.loads(path.read_text())
def mat(x):return np.array(x,dtype=object)
def independent_columns(G):
 # Exact rational Schur elimination, retaining lexical pivot order.
 residual=[[F(x) for x in row] for row in G];selected=[]
 for j in range(len(G)):
  p=residual[j][j];assert p>=0
  if p:
   selected.append(j)
   for r in range(j+1,len(G)):
    for c in range(j+1,len(G)):residual[r][c]-=residual[r][j]*residual[j][c]/p
  else:assert all(residual[j][k]==0 for k in range(j,len(G)))
 return selected

def local_relative(rec):
 bound=rec['relative_form_bound'];c=bound['local_certificate'];g=F(rec['coupling']);a=F(c['a']);b=F(c['b']);n=rec['N_dimers'];w=[2,1,2,1]
 m=[[F(0) for _ in range(16)] for _ in range(16)]
 for j in range(16):
  for x,y,v in KERNEL[j]:m[4*x+y][j]+=g*v
  m[j][j]+=a*((j//4!=0)+(j%4!=0))+b
 m=[[m[i][j]*w[i//4]*w[i%4] for j in range(16)] for i in range(16)]
 assert inertia(m)==(0,0,16)
 assert F(bound['alpha'])==1-4*a>0 and F(bound['B'])==2*n*b
 assert F(bound['second_shift_lower'])==F(bound['alpha'])-F(bound['B'])
 return True

def ground_matrices(nx,ny,g,geom):
 edges,orbits,ids=graph(nx,ny);N=nx*ny;d=1+len(orbits);p=g.numerator;den=4*g.denominator;h=2*p
 D=np.diag([1]+[3*len(o) for o in orbits]).astype(object)
 C=np.zeros((d,d),dtype=object)
 for col in range(d):
  target=defaultdict(int);vacuum=0
  if col==0:
   for pair,mul in edges.items():target[pair]+=h*mul
  else:
   for i,j in orbits[col-1]:
    target[i,j]+=2*den;mul=edges.get((i,j),0);target[i,j]-=2*h*mul;vacuum+=3*h*mul
    for (a,b),mul in edges.items():
     if a==i and b!=j:target[tuple(sorted((b,j)))]+=h*mul
     elif b==i and a!=j:target[tuple(sorted((a,j)))]+=h*mul
     elif a==j and b!=i:target[tuple(sorted((i,b)))]+=h*mul
     elif b==j and a!=i:target[tuple(sorted((i,a)))]+=h*mul
  C[0,col]=vacuum
  for row,orb in enumerate(orbits,1):
   vals={target[pair] for pair in orb};assert len(vals)==1;C[row,col]=next(iter(vals))
 Fm,S,V,W=[mat(geom[k]) for k in ['F','S','V','W']];q=d-1
 I=np.vstack([np.zeros((1,q),dtype=object),np.eye(q,dtype=object)]);E=I@Fm
 Ediv=np.array([[F(E[i,j],D[i,i]) for j in range(q)] for i in range(d)],dtype=object)
 G=np.block([[D,np.zeros((d,q),dtype=object)],[np.zeros((q,d),dtype=object),Fm]])
 K=np.block([[D@C,h*E],[h*E.T,4*den*Fm+h*S]])
 # Complete H images decomposed by q<=2, q=4 and q=6, independently assembled.
 U=np.column_stack([C,h*Ediv]);J=U.T@D@U
 J[:d,:d]+=h*h*I@Fm@I.T
 J[:d,d:]+=h*I@(4*den*Fm+h*S);J[d:,:d]+=h*(4*den*Fm+h*S.T)@I.T
 J[d:,d:]+=16*den*den*Fm+4*den*h*(S+S.T)+h*h*(V+W)
 assert all(F(x).denominator==1 for x in J.flat);J=np.array([[int(x) for x in row] for row in J],dtype=object)
 X=np.vstack([C,h*I.T]);mom=[D,D@C,J[:d,:d],X.T@K@X,X.T@J@X]
 return G,K,J,mom

def audit_ground():
 results=[]
 for nx,ny in [(4,4),(8,4),(8,8)]:
  geom=load(PRIOR/'results'/f'geometry_{nx}x{ny}.json')
  for g in map(F,['3/50']):
   f=GROUND/(f'block1_{nx}x{ny}_g{g}.json'.replace('/','d'));r=load(f);G,K,J,mom=ground_matrices(nx,ny,g,geom)
   assert [a.tolist() for a in mom]==r['shifted_integer_moments_M0_to_M4']
   selected=independent_columns(G);assert selected==r['selected_basis_indices']
   GG,KK,JJ=[a[np.ix_(selected,selected)] for a in [G,K,J]]
   for a,key in zip([GG,KK,JJ],['gram','shifted_hamiltonian_numerator','shifted_H2_numerator']):assert a.tolist()==r[key]
   c=mat(r['coefficients']);norm=int(c@GG@c);ha=int(c@KK@c);hb=int(c@JJ@c);den=4*g.denominator
   rho=F(ha,den*norm);r2=F(hb,den*den*norm)-rho*rho;assert r2>=0
   assert rho-F(3*nx*ny,4)==F(r['exact_rayleigh']) and r2==F(r['exact_residual_squared'])
   assert r['full_dimension']==4**(nx*ny) and r['trial_subspace_dimension']==len(selected) and r['integer_matrix_denominator']==den
   local_relative(r);a=F(r['relative_form_bound']['second_shift_lower'])
   assert F(r['second_eigenvalue_lower'])==a-F(3*nx*ny,4)
   if rho<a:assert F(r['ground_lower'])==rho-r2/(a-rho)-F(3*nx*ny,4)
   else:assert r['ground_lower'] is None
   results.append(dict(shape=f'{nx}x{ny}',g=str(g),dimension=len(selected),all_M0_M4_and_G_K_J_equal=True,rayleigh_and_full_residual_equal=True,local_relative_form_verified=True,Temple_available=rho<a))
   print('GROUND PASS',nx,ny,g,flush=True)
 save('ground_replay.json',results)

# Exact independent Q(sqrt2) arithmetic represented by pairs.
def qa(x,y):return x[0]+y[0],x[1]+y[1]
def qn(x):return -x[0],-x[1]
def qs(x,y):return qa(x,qn(y))
def qm(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def qd(x,y):
 d=y[0]**2-2*y[1]**2;assert d;return qm(x,(y[0]/d,-y[1]/d))
def qsign(x):
 a,b=x
 if not a:return (b>0)-(b<0)
 if not b:return (a>0)-(a<0)
 if (a>0)==(b>0):return 1 if a>0 else -1
 z=(a*a>2*b*b)-(a*a<2*b*b);return z if a>0 else -z
ZERO=(F(0),F(0));COS=[(F(1),F(0)),(F(0),F(1,2)),ZERO,(F(0),F(-1,2)),(F(-1),F(0)),(F(0),F(-1,2)),ZERO,(F(0),F(1,2))]
def qload(x):return tuple(map(F,x))
def symbol(a,nx,ny,kx,ky):
 r=ZERO
 for dx in range(nx):
  for dy in range(ny):r=qa(r,qm((F(a[dx][dy]),F(0)),COS[(8*kx*dx//nx+8*ky*dy//ny)%8]))
 return r

def apply(v,nx,ny,g):
 n=nx*ny;den=4*g.denominator;kernel=[[(x,y,int(g*z*den)) for x,y,z in row] for row in KERNEL];ed,_,_=graph(nx,ny);out=defaultdict(int);mask=sum(1<<(2*i) for i in range(n))
 for state,c in v.items():
  out[state]+=den*((state|(state>>1))&mask).bit_count()*c
  for (i,j),mul in ed.items():
   a=(state>>(2*i))&3;b=(state>>(2*j))&3
   for x,y,k in kernel[4*a+b]:out[state^((a^x)<<(2*i))^((b^y)<<(2*j))]+=c*mul*k
 return {s:c for s,c in out.items() if c}

def translate(s,nx,ny,dx,dy):
 # Independently rotates each row and places it into its new row location.
 out=0;mask=(1<<(2*ny))-1;shift=2*(dy%ny)
 for x in range(nx):
  row=(s>>(2*x*ny))&mask
  row=((row<<shift)|(row>>(2*ny-shift)))&mask
  out|=row<<(2*((x+dx)%nx)*ny)
 return out

def audit_translation():
 results=[]
 for nx,ny in [(4,4),(8,4),(8,8)]:
  n=nx*ny;mask=sum(1<<(2*i) for i in range(n));q=lambda s:((s|(s>>1))&mask).bit_count();weight=lambda s:1<<(n-(s&mask).bit_count())
  # Check every one-site basis digit: linearity then proves all state permutations.
  for dx in range(nx):
   for dy in range(ny):
    for i in range(n):
     x,y=divmod(i,ny)
     for digit in [1,2,3]:assert translate(digit<<(2*i),nx,ny,dx,dy)==digit<<(2*(((x+dx)%nx)*ny+(y+dy)%ny))
  for g in map(F,['3/50']):
   start=time.monotonic();tag=f'translated_{nx}x{ny}_g{g}'.replace('/','d');r=load(BAND/f'{tag}_moments.json');den=4*g.denominator
   bare_image=apply({3:1},nx,ny,g);w={3:2*den};w.update({s:-c for s,c in bare_image.items() if q(s)==3});hw=apply(w,nx,ny,g)
   with gzip.open(BAND/f'{tag}_column.json.gz','rt') as f:saved=json.load(f)
   assert w=={int(s):int(c) for s,c in saved['W']} and hw=={int(s):int(c) for s,c in saved['TW']}
   assert len(w)==r['trial_column_support'] and len(hw)==r['reached_column_support']
   raised=defaultdict(int)
   for state,c in w.items():
    assert q(state) in [1,3];assert sum(((state>>(2*i))&3)-2 for i in range(n) if (state>>(2*i))&3)==1
    for i in range(n):
     digit=(state>>(2*i))&3
     if digit in [1,2]:raised[state^((digit^(digit+1))<<(2*i))]+=c*(1 if digit==1 else 2)
   assert not any(raised.values())
   arrays=[[[0]*ny for _ in range(nx)] for _ in range(3)]
   for dx in range(nx):
    for dy in range(ny):
     for z,(left,right) in enumerate([(w,w),(w,hw),(hw,hw)]):
      arrays[z][dx][dy]=sum(c*right.get(translate(s,nx,ny,-dx,-dy),0)*weight(s) for s,c in left.items())
   assert all(a==[[int(x) for x in row] for row in r[k]] for a,k in zip(arrays,['G','A','B']))
   fourier=load(BAND/f'{tag}_fourier.json');assert fourier['source_moments']==r
   for mode in fourier['modes']:
    kx,ky=mode['momentum'];G,A,B=[symbol(a,nx,ny,kx,ky) for a in arrays];assert qsign(G)>0
    theta=qd(A,qm((F(den),F(0)),G));r2=qs(qd(B,qm((F(den*den),F(0)),G)),qm(theta,theta));assert qsign(r2)>=0
    for k,v in zip(['G','A','B','theta','residual_squared'],[G,A,B,theta,r2]):assert qload(mode[k])==v
    assert qsign(qs(theta,(F(mode['theta_lower']),F(0))))>=0
    assert qsign(qs((F(mode['theta_upper']),F(0)),theta))>=0
    assert qsign(qs((F(mode['residual_squared_upper']),F(0)),r2))>=0
   assert len(fourier['modes'])==n and len({tuple(x['momentum']) for x in fourier['modes']})==n
   results.append(dict(shape=f'{nx}x{ny}',g=str(g),W_support=len(w),HW_support=len(hw),all_displacement_G_A_B_equal=True,exact_highest_weight=True,all_Qsqrt2_symbols_and_bounds_equal=True,seconds=time.monotonic()-start))
   save('translation_replay.json',results);print('TRANSLATION PASS',nx,ny,g,time.monotonic()-start,flush=True)

if __name__=='__main__':
 inherited=load(OUT/'PRIOR_REVIEW_SHA256.json')
 assert hashlib.sha256((PRIOR/'MANIFEST_SHA256.json').read_bytes()).hexdigest()==inherited['manifest_sha256']
 for name,h in inherited['files'].items():assert hashlib.sha256((PRIOR/name).read_bytes()).hexdigest()==h,name
 for name,h in load(OUT/'INPUT_SHA256.json').items():assert hashlib.sha256((OUT/'snapshot'/name).read_bytes()).hexdigest()==h,name
 print('ALL INPUT HASHES PASS',flush=True)
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--part',choices=['ground','translation'],required=True);args=p.parse_args()
 if args.part=='ground':audit_ground()
 else:audit_translation()
