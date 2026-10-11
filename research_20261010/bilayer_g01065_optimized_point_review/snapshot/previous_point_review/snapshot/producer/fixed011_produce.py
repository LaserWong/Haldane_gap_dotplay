"""Bounded cached-matrix point tests, fixed g=.11 rational vectors.
No full-space contraction, new eigensolver or new trial-vector optimization.
"""
import os,resource,math,json,time,hashlib,ast
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
os.sched_setaffinity(0,{2});resource.setrlimit(resource.RLIMIT_CPU,(80,80));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
HERE=Path(__file__).resolve().parent;RES=HERE.parent;start=time.process_time();D=10**60;GRID=1<<384
load=lambda p:json.loads(p.read_text())
# Reuse only explicitly listed pure scalar functions from our frozen pilot.
names={'down','up','sqrtlo','G','raw','advance','window','canonical','float_path','gap_witness'}
source=RES/'bilayer_symmetry_scalar_pilot/exact_pilot.py'
for node in ast.parse(source.read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name in names:exec(compile(ast.Module(body=[node],type_ignores=[]),'sealed_scalar_helpers','exec'))
@lru_cache(None)
def exp(x):
 # Fully directed termwise recurrence avoids growth of exact series denominators.
 x=F(x);y=abs(x);k=0
 while y>F(1,8):y/=2;k+=1
 lot=hit=los=his=F(1)
 for j in range(1,91):
  lot=down(lot*y/j,GRID);hit=up(hit*y/j,GRID);los+=lot;his+=hit
 lo=down(los,GRID);hi=up(his+(hit*y/91)/(1-y/92),GRID)
 for _ in range(k):lo=down(lo*lo,GRID);hi=up(hi*hi,GRID)
 return (lo,hi) if x>=0 else (down(1/hi,GRID),up(1/lo,GRID))

def poly(c,g):return sum(x*g**i for i,x in enumerate(c))
def root60(x):
 den=10**60;k=math.isqrt(x.numerator*den*den//x.denominator);r=F(k,den);assert r*r<=x<(r+F(1,den))**2;return r

def ref(N,g,q):
 C=F(3*N,8);return C*(2*g-1)+(C+q)*root60(1-4*g)

def qload(z):return tuple(map(F,z))
def qadd(a,b):return a[0]+b[0],a[1]+b[1]
def qmul(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def qsign(z):
 a,b=z
 if not a:return (b>0)-(b<0)
 if not b:return (a>0)-(a<0)
 if (a>0)==(b>0):return 1 if a>0 else -1
 u=(a*a>2*b*b)-(a*a<2*b*b);return u if a>0 else -u
rt2=root60(F(2))
def qbound(z):
 a,b=z;u=a+b*rt2;v=a+b*(rt2+F(1,10**60));return min(u,v),max(u,v)
def qpoly(c,g):
 out=(F(0),F(0))
 for j,z in enumerate(c):out=qadd(out,qmul(qload(z),(g**j,F(0))))
 return out

def verify_seal(group,expected=None):
 mf=RES/group/'MANIFEST_SHA256.json';digest=hashlib.sha256(mf.read_bytes()).hexdigest()
 if expected:assert digest==expected
 for name,h in load(mf).items():assert hashlib.sha256((mf.parent/name).read_bytes()).hexdigest()==h,name
 return digest
seals={}
for group,expected in [('bilayer_symmetry_scalar_pilot','11c4405ac1528973eebaecaa1d7c8d655f6b14aa4d240f0b491446239b46d45e'),('bilayer_complete_split_H2_8x4_review','874c87f1ff9b4b58f795ef5e01aad45ff4f22e560e4721c7a933ed27380166a5'),('bilayer_split_H2_fixture_review',None),('bilayer_split_pencil_optimization_review','fc205510f91902c1c9da6ba9bbdedefe69900a0fb1505fbd541aefe312417381'),('bilayer_residual_pencil_optimization_review',None)]:seals[group]=verify_seal(group,expected)
M16=load(RES/'bilayer_split_H2_fixture_review/snapshot/producer/complete_H2_polynomial_4x4.json');M32=load(RES/'bilayer_complete_split_H2_8x4_review/audit.json')
w16=next(x for x in load(RES/'bilayer_residual_pencil_optimization_review/snapshot/optimization/result.json')['results'] if x['shape']==[4,4] and F(x['g'])==F(11,100))
w32=next(x for x in load(RES/'bilayer_split_pencil_optimization_review/snapshot/producer/result.json')['results'] if F(x['g'])==F(11,100))
c16=w16['integer_coefficients'];assert len(c16)==16;c16=c16[:11]+c16[11:]+c16[11:];assert len(c16)==21
c32=w32['integer_coefficients'];assert len(c32)==57
energy=load(RES/'bilayer_split_pencil_optimization_review/snapshot/REOPTIMIZATION.json')['results']
energy={math.prod(x['shape']):x['split'] for x in energy if F(x['g'])==F(11,100)}
base=next(x['data'] for x in load(RES/'bilayer_symmetry_scalar_pilot/snapshot/bilayer_frontier_above_010/exploration.json')['results'] if F(x['g'])==F(11,100))
def bil(c,m):return sum(F(c[i])*F(m[i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
mom={}
for N,c,M in [(16,c16,M16),(32,c32,M32)]:
 norm=bil(c,M['gram']);rho=[bil(c,m)/norm for m in M['H_coefficients']];h2=[bil(c,m)/norm for m in M['H2_coefficients']];assert norm>0
 var=[h2[0]-rho[0]**2,h2[1]-2*rho[0]*rho[1],h2[2]-rho[1]**2]
 assert var[0]>=0 and var[2]>=0 and 4*var[0]*var[2]>=var[1]**2
 mom[N]=dict(N=N,coefficients=c,norm=str(norm),rho=list(map(str,rho)),second=list(map(str,h2)),variance=list(map(str,var)))
 # Check the independent moment recombination against the accepted .11 endpoint.
 rr=poly(rho,F(11,100));vv=poly(var,F(11,100));ll=rr-vv/(ref(N,F(11,100),2)-rr)
 assert ll==F((w16 if N==16 else w32)['Temple_lower'])
(HERE/'fixed_moment_polynomials.json').write_text(json.dumps(dict(source_seals=seals,moments=list(mom.values()),energy_upper_coefficients={N:energy[N]['rayleigh_coefficients'] for N in [16,32,64]}),indent=2)+'\n')

def physical(g):
 patches=[]
 for ix,N in enumerate([16,32]):
  m=mom[N];rho=poly(list(map(F,m['rho'])),g);var=poly(list(map(F,m['variance'])),g);a=ref(N,g,2);r1=ref(N,g,1)
  assert var>=0 and rho<r1<a
  lower=rho-var/(a-rho);pivot=poly(list(map(F,energy[N]['rayleigh_coefficients'])),g);assert lower<=pivot<r1
  odd=[];margins=[];details=[]
  for row in base['denominator_patches'][ix]['odd_band']['modes']:
   assert qsign(qload(row['gram_symbol']))>0
   theta=qpoly(row['theta_coefficients'],g);variance=qpoly(row['residual_squared_coefficients'],g);assert qsign(variance)>=0
   lo,hi=qbound(theta);vlo,vhi=qbound(variance);assert hi<a;margins.append(a-hi)
   ell=max(r1,lo-max(F(0),vhi)/(a-hi));odd.append(ell-pivot)
   details.append(dict(momentum=row['momentum'],gram_symbol=row['gram_symbol'],theta=list(map(str,theta)),variance=list(map(str,variance)),cutoff_margin=str(a-hi),lower=str(ell)))
  assert len(odd)==N and len({tuple(r['momentum']) for r in details})==N
  patches.append(dict(N=N,rho=str(rho),variance=str(var),r1=str(r1),r2=str(a),ground_lower=str(lower),pivot=str(pivot),ground_width=str(pivot-lower),global_ground_margin=str(r1-rho),odd_min_cutoff_margin=str(min(margins)),odd=list(map(str,odd)),odd_details=details,tail=[str(ref(N,g,q)-pivot) for q in range(2,N+1)]))
 rho=[F(x['pivot']) for x in patches]+[poly(list(map(F,energy[64]['rayleigh_coefficients'])),g)]
 combos={k:sum(a*b for a,b in zip(weights,rho)) for k,weights in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]}
 return dict(g=str(g),patches=patches,numerator_rayleigh=str(rho[2]),energy_combinations={k:str(v) for k,v in combos.items()},retained_counts=[49,97,1],ground_trial_dimensions=[16,57,57],energy_trial_dimensions=[21,57,57])

def ratios(phys,beta,exact=True):
 exup=(lambda z:exp(z)[1]) if exact else lambda z:math.exp(float(z))
 exlo=(lambda z:exp(z)[0]) if exact else lambda z:math.exp(float(z))
 uppers=[]
 for ix,mult in [(0,1),(0,2),(1,2)]:
  p=phys['patches'][ix];b=mult*beta;N=p['N']
  ground=exup(b*F(p['ground_width']));odd=3*sum(exup(-b*F(x)) for x in p['odd']);tail=sum(math.comb(3*N+q-1,q)*exup(-b*F(v)) for q,v in enumerate(p['tail'],2));uppers.append(ground+odd+tail)
 r={k:exlo(beta*F(phys['energy_combinations'][k]))/u**power for k,u,power in zip(['J1','J2','C0'],uppers,[8,8,2])}
 return {k:down(v) for k,v in r.items()} if exact else r

def score(r,beta):
 abc=raw(r,False)
 if abc is None:return None
 bounds=[]
 for j in range(18):
  can=canonical(abc,False);u=max(1-x for x in can);bb=2*float(beta)*2**j
  if 1e-12<u<=.002:return min(bounds+[math.log(1/(32*u))/bb])
  v=window(abc,False)
  if v<=.5:return None
  bounds.append(math.log(v/(1-v))/bb);abc=advance(abc,False)
  if abc is None:return None
 return None

def certificate(phys,beta):
 r=ratios(phys,beta);abc=raw(r);assert abc is not None;states=[]
 for j in range(20):
  can=canonical(abc);u=max(1-x for x in can);bb=2*beta*2**j
  row=dict(n=8*2**j,beta=str(bb),raw=list(map(str,abc)),canonical=list(map(str,can)),common_defect=str(u))
  if 0<u<=F(1,500):
   prop=F(math.floor(math.log(float(1/(32*u)))/float(bb)*10**12)-1,10**12)
   while exp(bb*prop)[1]*32*u>=1:prop-=F(1,10**12)
   row['asymptotic_gap']=str(prop);row['exp_witness']=str(exp(bb*prop)[1]*32*u);states.append(row);break
  v=window(abc);assert v>F(1,2);row['thermal_lower']=str(v);row['finite_window_gap']=str(gap_witness(v,bb));states.append(row);abc=advance(abc);assert abc is not None
 assert 'asymptotic_gap' in states[-1]
 short=F(50426624396,10**12);gap=min([short]+[F(s.get('finite_window_gap',s.get('asymptotic_gap'))) for s in states]);assert gap>0
 return dict(status='EXACT_POINT_CANDIDATE_PENDING_INDEPENDENT_REVIEW',g=phys['g'],beta_initial=str(beta),ratios={k:str(v) for k,v in r.items()},states=states,short_sizes=dict(L_from=2,L_through=7,gap=str(short),coupling_interval=['0','3/20']),all_integer_L_ge2_gap=str(gap),gap_display=float(gap),physical=phys)

out=[]
for g in map(F,['53/500','107/1000','27/250','109/1000']):
 phys=physical(g);proposals=[]
 for i in range(160,261):
  beta=F(i,20);r=ratios(phys,beta,False);v=score(r,beta)
  if v is not None:proposals.append((v,beta))
 row=dict(g=str(g),all_point_physical_gates_pass=True,successful_grid_proposals=len(proposals))
 if proposals:
  best,beta=max(proposals);row['certificate']=certificate(phys,beta);row['float_score']=best
 else:row['physical']=phys
 out.append(row);(HERE/'checkpoint.json').write_text(json.dumps(dict(results=out,cpu_seconds=time.process_time()-start),indent=2)+'\n');print(g,'grid',len(proposals),'gap',row.get('certificate',{}).get('gap_display'),flush=True);exp.cache_clear()
(HERE/'result.json').write_text(json.dumps(dict(status='CACHED_FIXED_VECTOR_POINT_CANDIDATES_PENDING_REVIEW',results=out,cpu_seconds=time.process_time()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,no_new_physical_contraction=True,no_gap_interpolation=True),indent=2)+'\n')
