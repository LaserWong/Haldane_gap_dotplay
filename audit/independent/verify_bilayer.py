"""Independent sparse-support spin-half bilayer verifier; no worker imports or eigensolver."""
from fractions import Fraction as Q
from pathlib import Path
from collections import defaultdict, Counter
import math,json,hashlib,time
import numpy as np
from verify_baseline import exp_interval, f
BASE=Path(__file__).resolve().parents[2];OUT=BASE/'audit/independent'
# Explicit unnormalised rung vectors in |down down>,|down up>,|up down>,|up up>.
V=[[0,-1,1,0],[1,0,0,0],[0,1,1,0],[0,0,0,1]]
weights=[sum(x*x for x in v) for v in V]
assert weights==[2,1,2,1]

def local_ops(site):
 result={}
 for name in ['z','+','-']:
  o=[[Q(0) for _ in range(4)] for _ in range(4)]
  for c in range(4):
   bits=[c//2,c%2]
   if name=='z':o[c][c]=Q(2*bits[site]-1,2)
   elif name=='+' and bits[site]==0:
    b=bits.copy();b[site]=1;o[2*b[0]+b[1]][c]=1
   elif name=='-' and bits[site]==1:
    b=bits.copy();b[site]=0;o[2*b[0]+b[1]][c]=1
  result[name]=[[sum(V[r][i]*o[i][j]*V[c][j] for i in range(4) for j in range(4))/weights[r] for c in range(4)] for r in range(4)]
 return result
OPS=[local_ops(0),local_ops(1)]

def kernel(a,b):
 A=OPS[a];B=OPS[b];out={}
 for c in range(4):
  for d in range(4):
   out[c,d]=[]
   for r in range(4):
    for s in range(4):
     x=A['z'][r][c]*B['z'][s][d]+(A['+'][r][c]*B['-'][s][d]+A['-'][r][c]*B['+'][s][d])/2
     if x:out[c,d].append((r,s,x))
 return out
K={(a,b):kernel(a,b) for a in range(2) for b in range(2)}

def graph(nx,ny,g):
 idx=lambda x,y:(x%nx)*ny+(y%ny)
 return [(idx(x,y),l,idx(x+1,y),l,g) for x in range(nx) for y in range(ny) for l in (0,1)]+[(idx(x,y),l,idx(x,y+1),l,g) for x in range(nx) for y in range(ny) for l in (0,1)]

def floor(x,d=15):return Q(x.numerator*10**d//x.denominator,10**d)
def ceiling(x,d=18):return Q(-((-x.numerator*10**d)//x.denominator),10**d)
def bounded_exp(x):
 # Outward rational argument compression preserves strict certification and makes replay faster.
 q=Q(x);lo=floor(q,34);hi=ceiling(q,34)
 return exp_interval(lo)[0],exp_interval(hi)[1]

def ground(r,nx,ny,g):
 t=time.monotonic();N=nx*ny;assert r['N_dimers']==N and r['s']=='1/2'
 p=BASE/'low_energy'/r['trial_artifact'];z=np.load(p)
 basis=[tuple(map(int,a)) for a in z['basis']];vec=list(map(int,z['vector']))
 assert len(basis)==len(vec)==r['trial_subspace_dimension']
 assert len(set(basis))==len(basis)
 assert all(sum(x!=0 for x in st)<=r['trial_max_excited_dimers'] for st in basis)
 assert all(sum((0,-1,0,1)[v] for v in st)==0 for st in basis)
 edges=[(i,a,j,b,Q(c)) for i,a,j,b,c in r['weak_bonds']]
 assert Counter(edges)==Counter(graph(nx,ny,g))
 assert len(edges)==4*N and all(i!=j for i,a,j,b,c in edges)
 scale=800;E00=-Q(3*N,4)
 multiply=defaultdict(int);seen=set(basis);nonzeros=0
 for st,v in zip(basis,vec):
  col=defaultdict(int)
  col[st]=int(scale*(E00+sum(x!=0 for x in st)))
  for i,a,j,b,c in edges:
   for ri,rj,val in K[a,b][st[i],st[j]]:
    coeff=scale*c*val;assert coeff.denominator==1
    state=list(st);state[i]=ri;state[j]=rj
    col[tuple(state)]+=int(coeff)
  for state,coeff in col.items():
   if coeff:
    seen.add(state);nonzeros+=1;multiply[state]+=coeff*v
 metric=lambda st:math.prod(weights[x] for x in st)
 norm=sum(metric(st)*v*v for st,v in zip(basis,vec))
 rho=Q(sum(metric(st)*v*multiply[st] for st,v in zip(basis,vec)),scale*norm)
 r2=Q(sum(metric(st)*v*v for st,v in multiply.items()),scale*scale*norm)-rho*rho
 assert rho==Q(r['exact_rayleigh']) and r2==Q(r['exact_residual_squared'])
 assert len(seen)==r['reached_support_dimension'] and nonzeros==r['sparse_nnz']
 vmin=-Q(3,4)*sum(c for i,a,j,b,c in edges);vmax=Q(1,4)*sum(c for i,a,j,b,c in edges)
 assert E00==Q(r['E00']) and vmin==Q(r['Vmin']) and vmax==Q(r['Vmax'])
 if 'relative_form_bound' in r:
  rb=r['relative_form_bound'];lc=rb['local_certificate'];aa=Q(lc['a']);bb=Q(lc['b'])
  assert aa>=g/2 and aa<Q(1,4)
  assert bb+aa-g/2>=0 and (bb+aa-g/2)**2>=aa*aa-aa*g+g*g
  alpha=1-4*aa;B=2*N*bb
  assert alpha==Q(rb['alpha']) and B==Q(rb['B']) and alpha-B==Q(rb['second_shift_lower'])
  a=E00+alpha-B
 else:a=E00+1+vmin
 assert a==Q(r['second_eigenvalue_lower']) and a>E00 and rho<a
 lo=rho-r2/(a-rho);assert lo==Q(r['ground_lower']) and rho==Q(r['ground_upper'])
 return {'nx':nx,'ny':ny,'full_dimension':4**N,'trial_dimension':len(basis),'full_residual_support':len(seen),'exact_matrix_nonzeros':nonzeros,'exact_rayleigh_matches':True,'full_residual_matches':True,'Temple_interval_matches':True,'full_space_second_energy_bound':str(a),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'seconds':time.monotonic()-t}

def tail(r,beta):
 lo=Q(r['ground_lower']);hi=Q(r['ground_upper']);E00=Q(r['E00']);vmin=Q(r['Vmin']);N=r['N_dimers']
 zz=1+3*bounded_exp(-beta)[1]
 t=bounded_exp(-beta*(E00+vmin-hi))[1]*(zz**N-1)
 q=bounded_exp(beta*(hi-lo))[1]+t
 return q,t

def run(path):
 data=json.loads(path.read_text());assert data['g']=='1/100'
 rec=data['ground_certificates'];g=Q(data['g'])
 checks=[ground(r,*shape,g) for r,shape in zip(rec,[(2,2),(4,2),(4,4)])]
 print('GROUND CHECKS',json.dumps(checks),flush=True)
 seedchecks=[]
 for seed in data['seeds']:
  beta=Q(seed['beta']);qs=[tail(r,beta)[0] for r in rec]
  E=[Q(r['ground_upper']) for r in rec]
  ABC=[floor(bounded_exp(-beta*(E[1]-2*E[0]))[0]/qs[0]**2),floor(bounded_exp(-beta*(E[2]-2*E[1]))[0]/qs[1]**2),floor(1/qs[2]**2)]
  assert list(map(str,ABC))==[seed[k+'_lower'] for k in 'ABC']
  defects=[1-x for x in ABC]
  saved=seed['bootstrap'];bb=beta;n=2
  for row in saved['updates']:
   for axis in range(3):
    a,b,c=defects
    new=ceiling(f(1-(1-a)**4*(1-b)**2*(1-c)))
    defects=defects[1:]+[new]
   assert list(map(str,defects))==row['defects']
   bb*=2;n*=2
  accepted=saved['status']=='accepted_analytic_scalar_certificate'
  if accepted:
   u=max(defects);gap=Q(saved['uniform_square_gap_lower'])
   assert u<=Q(1,500) and n==saved['n']==saved['m'] and bb==Q(saved['beta'])
   assert bounded_exp(bb*gap)[1]<1/(32*u)
  seedchecks.append({'beta':str(beta),'A':str(ABC[0]),'B':str(ABC[1]),'C':str(ABC[2]),'independent_rounds_match':True,'accepted':accepted,'gap_lower':saved.get('uniform_square_gap_lower')})
 report={'status':'PASS: independent graph, rung basis, full sparse-support residual, full-space Weyl/Temple, heat traces and 3-purity replay','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'ground_checks':checks,'seed_checks':seedchecks,'transfer_and_interpolation':'Hand-derived independently; see audit/BILAYER_PHYSICAL_PROOF.md'}
 (OUT/'bilayer_g001_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':run(BASE/'low_energy/bilayer_seed_s1d2_g1d100_relativeFalse_q2.json')
