"""Independent spin1 large-D sparse-support certificate audit."""
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import math,json,hashlib
import numpy as np
from verify_bilayer import bounded_exp,f,floor,ceiling
BASE=Path(__file__).resolve().parents[2];DIR=BASE/'two_d_numerics/results';OUT=BASE/'audit/independent'

def bond(p,g,N):
 a,b,c,B=[F(p[k]) for k in ['a','b','c','B']];d=2*a-g
 assert b>=0 and a+b>=g and 2*a+g+b>=0 and d+b>=0 and b*(d+b)>=2*g*g
 assert c==1-4*a and B==2*N*b and c>0
 return c,B

def ground(r):
 nx,ny,N=r['nx'],r['ny'],r['N'];g=F(r['g']);den=g.denominator;gg=g.numerator
 z=np.load(DIR/r['trial_artifact']);basis=[tuple(map(int,x)) for x in z['basis']];vec=list(map(int,z['vector']))
 assert N==nx*ny and len(basis)==len(vec)==r['trial_dimension'] and len(set(basis))==len(basis)
 assert all(sum(st)==0 and sum(x!=0 for x in st)<=r['max_excited'] for st in basis)
 idx=lambda x,y:(x%nx)*ny+(y%ny)
 edges=[(idx(x,y),idx(x+dx,y+dy)) for x in range(nx) for y in range(ny) for dx,dy in [(1,0),(0,1)]]
 assert len(edges)==2*N and all(a!=b for a,b in edges)
 hv=defaultdict(int);seen=set(basis);nnz=0
 for st,v in zip(basis,vec):
  col=defaultdict(int);col[st]=den*sum(x*x for x in st)+gg*sum(st[i]*st[j] for i,j in edges)
  for i,j in edges:
   for dx in [-1,1]:
    if -1<=st[i]+dx<=1 and -1<=st[j]-dx<=1:
     dest=list(st);dest[i]+=dx;dest[j]-=dx;col[tuple(dest)]+=gg
  for t,c in col.items():
   if c:hv[t]+=c*v;seen.add(t);nnz+=1
 norm=sum(v*v for v in vec);rho=F(sum(v*hv[st] for st,v in zip(basis,vec)),den*norm)
 r2=F(sum(v*v for v in hv.values()),den*den*norm)-rho*rho
 assert rho==F(r['exact_rayleigh']) and r2==F(r['exact_residual_squared'])
 assert len(seen)==r['reached_dimension'] and nnz==r['sparse_nnz']
 c,B=bond(r['comparison'],g,N);nextlo=c-B
 assert nextlo==F(r['second_eigenvalue_lower']) and rho<nextlo
 assert rho-r2/(nextlo-rho)==F(r['ground_lower']) and rho==F(r['ground_upper'])
 return {'nx':nx,'ny':ny,'trial_dimension':len(basis),'full_residual_support':len(seen),'exact_residual_and_Temple_match':True,'local_PSD_and_ordered_comparison_pass':True,'vector_sha256':hashlib.sha256((DIR/r['trial_artifact']).read_bytes()).hexdigest()}

def run():
 path=DIR/'largeD_g1d100_q2_certificate.json';data=json.loads(path.read_text());recs=data['ground_certificates']
 gc=[ground(r) for r in recs];print('GROUNDS',gc,flush=True);sc=[]
 for seed in data['seeds']:
  beta=F(seed['beta']);qs=[]
  for r,p in zip(recs,seed['tail_comparisons']):
   g=F(r['g']);N=r['N'];c,B=bond(p,g,N);lo=F(r['ground_lower']);hi=F(r['ground_upper'])
   tail=bounded_exp(beta*(B+hi))[1]*((1+2*bounded_exp(-beta*c)[1])**N-1)
   assert tail<=F(p['tail_upper'])
   qs.append(bounded_exp(beta*(hi-lo))[1]+tail)
  E=[F(r['ground_upper']) for r in recs]
  ABC=[floor(bounded_exp(-beta*(E[1]-2*E[0]))[0]/qs[0]**2,18),floor(bounded_exp(-beta*(E[2]-2*E[1]))[0]/qs[1]**2,18),floor(1/qs[2]**2,18)]
  assert list(map(str,ABC))==seed['purity_lowers']
  defects=[1-x for x in ABC];b=seed['bootstrap'];bb=beta;n=2
  for row in b['updates']:
   for _ in range(3):
    x,y,z=defects;defects=defects[1:]+[ceiling(f(1-(1-x)**4*(1-y)**2*(1-z)))]
   assert list(map(str,defects))==row['defects'];n*=2;bb*=2
  if b['status']=='accepted_analytic_scalar_certificate':
   u=max(defects);gap=F(b['uniform_square_gap_lower']);assert u<=F(1,500)
   assert bounded_exp(bb*gap)[1]<1/(32*u)
  sc.append({'beta':str(beta),'purities_and_replay_match':True,'gap_lower':b.get('uniform_square_gap_lower')})
 # A single rational bond inequality bridges every square size 2..7.
 p={'a':'1/20','b':'11/5000','c':'4/5','B':str(2*49*F(11,5000))}
 c,B=bond(p,F(1,100),49);bridge=c-B
 assert bridge==F(1461,2500) and bridge>F('0.086452285325')
 report={'status':'PASS independent full residual, local PSD, spectral bins, all seeds and gap comparisons','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'grounds':gc,'seeds':sc,'small_square_bridge_L2_through_7':str(bridge),'physical_scope':'Every integer periodic square L>=2, gap>=0.086452285325, once spin1 real directional transfers and audited3-purity interpolation are applied.'}
 (OUT/'largeD_g001_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':run()
