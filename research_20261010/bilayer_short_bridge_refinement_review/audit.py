import os,resource
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_CPU,(120,120));resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2))
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
import itertools,math,json,hashlib,time
H=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Physical swap construction: 2(S0.S0+S1.S1)=P02+P13-I.
rungs=[{1:1,2:-1},{0:1},{1:1,2:1},{3:1}];norm=[sum(x*x for x in v.values()) for v in rungs]
columns=[{(a<<2)|b:x*y for a,x in rungs[i].items() for b,y in rungs[j].items()} for i in range(4) for j in range(4)]
def swap(st,i,j):
 return st^((1<<i)|(1<<j)) if ((st>>i)^(st>>j))&1 else st
A={}
for j,col in enumerate(columns):
 out=defaultdict(int)
 for st,c in col.items():
  out[swap(st,3,1)]+=c;out[swap(st,2,0)]+=c;out[st]-=c
 A[j]=[(i,F(sum(c*out[st] for st,c in col2.items()),norm[i//4]*norm[i%4])) for i,col2 in enumerate(columns) if sum(c*out[st] for st,c in col2.items())]
assert A[0]==[(7,F(-2)),(10,F(1)),(13,F(-2))]
metric16=[norm[i//4]*norm[i%4] for i in range(16)];q16=[int(i//4!=0)+int(i%4!=0) for i in range(16)]
local=[[F(0) for _ in range(16)] for _ in range(16)]
for j,col in A.items():
 for i,x in col:local[i][j]=x
assert all(metric16[i]*local[i][j]==metric16[j]*local[j][i] for i in range(16) for j in range(16))
# Twice the preserving inequality V_pres+Q/2>=0, in the exact metric.
psd=[[metric16[i]*((local[i][j] if q16[i]==q16[j] else 0)+(q16[i] if i==j else 0)) for j in range(16)] for i in range(16)]
local_pivots=[]
for j in range(16):
 pivot=psd[j][j];assert pivot>=0;local_pivots.append(str(pivot))
 if not pivot:assert all(psd[i][j]==0 for i in range(j+1,16));continue
 for i in range(j+1,16):
  for k in range(i,16):psd[k][i]=psd[i][k]=psd[i][k]-psd[i][j]*psd[k][j]/pivot


def geom(L):
 coords=list(itertools.product(range(L),repeat=2));edges=defaultdict(int)
 for i,xy in enumerate(coords):
  for axis in (0,1):
   z=list(xy);z[axis]=(z[axis]+1)%L;j=coords.index(tuple(z));edges[tuple(sorted((i,j)))]+=1
 degree=[sum(w for e,w in edges.items() if i in e) for i in range(L*L)];assert degree==[4]*(L*L)
 S=sum(w*w for w in edges.values());M=sum(w**3 for w in edges.values())
 T=sum(edges.get((a,b),0)*edges.get((a,c),0)*edges.get((b,c),0) for a,b,c in itertools.combinations(range(L*L),3))
 return edges,S,M,T

def moments(L):
 edges,S,M,T=geom(L);B={}
 for (a,b),w in edges.items():
  for state,h in A[0]:B[((state//4)<<(2*a))|((state%4)<<(2*b))]=w*h
 def metric(st):
  v=F(1)
  while st:v*=F(norm[st&3],2);st>>=2
  return v
 n=sum(c*c*metric(st) for st,c in B.items());diagonal=F(0)
 for st,c in B.items():
  for (a,b),w in edges.items():
   x=(st>>(2*a))&3;y=(st>>(2*b))&3
   for v,h in A[4*x+y]:
    t=st^((x^(v//4))<<(2*a))^((y^(v%4))<<(2*b))
    if t in B:diagonal+=c*w*h*B[t]*metric(t)
 assert n==3*S and diagonal==-6*M+18*T
 return dict(L=L,N=L*L,physical_spins=2*L*L,full_Hilbert_dimension=str(4**(L*L)),trial_dimension=2,B_support=len(B),edge_count=len(edges),edge_weight_sum=sum(edges.values()),edge_square_sum=S,edge_cube_sum=M,weighted_triangle_sum=T,weighted_degree=4,reduced_B_norm=str(n),vacuum_A_B=str(n),B_A_B=str(diagonal),pair_diagonal_slope=str(F(diagonal,2*n)))

def sqrt_bounds(x):
 d=1<<288;k=math.isqrt(x.numerator*d*d//x.denominator);return F(k,d),F(k+1,d)
def bounds(L,g):
 _,S,M,T=geom(L);C=F(3*S,16);k=F(-M+3*T,S);E=2+k*g;dl,du=sqrt_bounds(1-4*g);ql,qu=sqrt_bounds(E*E+16*C*g*g)
 lam=(C*(2*g-1)+(C+1)*dl,C*(2*g-1)+(C+1)*du);ritz=((E-qu)/2,(E-ql)/2)
 return lam,ritz,(lam[0]-ritz[1],lam[1]-ritz[0])
def checkrow(row):
 L=row['L'];g=F(row['g']);a,b,c=bounds(L,g)
 for lo,hi,pair in [('second_eigenvalue_lower','second_eigenvalue_upper_comparison_only',a),('Rayleigh_lower_in_trial_space_only','Rayleigh_upper',b),('gap_lower','gap_upper_of_this_bound_only',c)]:assert F(row[lo])<=pair[0]<=pair[1]<=F(row[hi])
 for key,x in [('delta_enclosure',1-4*g),('Ritz_discriminant_enclosure',(2+F(-2 if L==2 else 0 if L==3 else -1)*g)**2+3*geom(L)[1]*g*g)]:
  l,u=map(F,row[key]);assert 0<=l<=u and l*l<=x<=u*u
 return c

def main():
 start=time.monotonic();mf=H/'snapshot/PRODUCER_MANIFEST.json'
 for rel,h in load(mf).items():assert sha(H/'snapshot/producer'/rel)==h
 assert sha(mf)==load(H/'DEPENDENCIES.json')['producer_manifest_sha256'];saved=load(H/'snapshot/producer/result.json');mm=[moments(L) for L in range(2,8)];assert mm==saved['geometry_and_exact_physical_moments']
 # Full-Hilbert reference theorem provenance.
 dm=H/'snapshot/QUADRATIC_MANIFEST.json';assert sha(dm)==load(H/'DEPENDENCIES.json')['quadratic_manifest_sha256'];m=load(dm);m=m.get('files',m);assert sha(H/'snapshot/QUADRATIC_PROOF.md')==m['PROOF.md']
 em=H/'snapshot/EMBEDDING_MANIFEST.json';assert sha(em)==load(H/'DEPENDENCIES.json')['embedding_manifest_sha256'];emf=load(em);emf=emf.get('files',emf);assert sha(H/'snapshot/EMBEDDING_PROOF.md')==emf['PROOF.md']
 endpoints=[]
 for row in saved['continuous_endpoints']:
  g=F(row['continuous_coupling_interval'][1]);assert row['continuous_coupling_interval'][0]=='0' and [x['L'] for x in row['per_size']]==list(range(2,8))
  for x in row['per_size']:assert F(x['g'])==g;checkrow(x)
  fixed=row['fixed_rational_trials'];assert [x['L'] for x in fixed]==list(range(2,8))
  for x in fixed:
   L=x['L'];_,S,M,T=geom(L);k=F(-M+3*T,S);t=F(x['fixed_rational_t']);assert t>=0 and x['coupling_interval']==['0',str(g)]
   n=1+3*S*t*t;ray=lambda z:3*S*((2+k*z)*t*t-z*t)/n
   assert F(x['squared_norm_reduced'])==n and F(x['rayleigh_at_zero'])==ray(F(0)) and F(x['rayleigh_at_upper'])==ray(g)
   assert F(x['gap_lower_at_zero'])==1-ray(F(0)) and F(x['gap_lower_at_upper'])<=bounds(L,g)[0][0]-ray(g)
   assert F(x['uniform_gap_lower'])==min(F(x['gap_lower_at_zero']),F(x['gap_lower_at_upper'])) and x['positive']==(F(x['uniform_gap_lower'])>0)
  low=min(F(x['uniform_gap_lower']) for x in fixed);assert F(row['decimal_gap_lower'])==F(low.numerator*10**12//low.denominator,10**12);assert low==F(row['uniform_short_size_gap']) and row['positive']==(low>0);endpoints.append(dict(g=str(g),gap_lower=str(low),positive=low>0))
 roots=[]
 for r in saved['unique_zero_brackets_of_this_method']:
  lo,hi=F(r['lower']),F(r['upper']);assert 0<lo<hi<F(1,4) and hi-lo<F(1,10**14)
  assert F(r['lower_witness']['g'])==lo and F(r['upper_witness']['g'])==hi
  assert checkrow(r['lower_witness'])[0]>0 and checkrow(r['upper_witness'])[1]<0
  roots.append(dict(L=r['L'],lower=str(lo),upper=str(hi)))
 assert [x['L'] for x in roots]==list(range(2,8));lim=min(roots,key=lambda r:F(r['upper']));assert lim['L']==7 and all(F(lim['upper'])<F(r['lower']) for r in roots if r['L']!=7)
 # Coefficientwise proof D(g)-4 delta(g)^2=(4k+16)g+(k^2+16C)g^2>=0.
 concavity=[]
 for r in mm:
  k=F(r['pair_diagonal_slope']);C=F(3*r['edge_square_sum'],16);assert 4*k+16>=0 and k*k+16*C>0;concavity.append(dict(L=r['L'],D_minus_4delta_squared_coefficients=list(map(str,[4*k+16,k*k+16*C])),initial_derivative='-2',second_derivative_upper='-4/(1-4g)^(3/2)'))
 assert sha(H/'snapshot/PROSE_ERRATUM.json')=='4026967a160aa56ad2513cc1a3162e68054e5126ec76c3d5ea4e1bb0d707a712'
 assert F('.15283831215983547')<=F(lim['lower']) and F('.15283831215983637')>=F(lim['upper'])
 assert bounds(7,F('.15283831215983548'))[2][0]>0 and bounds(7,F('.15283831215983637'))[2][1]<0
 budgets=load(H/'snapshot/producer/next_span_budget.json');assert budgets['status']=='unexecuted_next_span_plan_only'
 for x in budgets['budgets']:
  g=F(x['g']);a,b,c=bounds(7,g);target=F(x['sufficient_ground_Rayleigh_upper_target']);assert target<=a[0]-F(x['desired_gap'])
  upper=F(x['current_two_state_Rayleigh_upper']);lower=F(x['current_two_state_minimum_lower']);assert lower<=b[0]<=b[1]<=upper
  assert F(x['required_Rayleigh_improvement_from_current_upper'])==upper-target and F(x['rigorous_shortfall_of_entire_two_state_span'])==lower-target>0
 assert budgets['L7_disjoint_unordered_edge_pairs']==math.comb(98,2)-49*math.comb(4,2)==4459 and budgets['L7_q4_configuration_support_upper']==9*4459
 target=next(r for r in endpoints if F(r['g'])==F(3,20));rounded=F(50426624396,10**12);assert F(target['gap_lower'])>=rounded>0
 bad=[]
 import copy
 for name,key in [('inflated_ground_upper','Rayleigh_upper'),('inflated_gap','gap_lower'),('inflated_lambda2','second_eigenvalue_lower')]:
  row=copy.deepcopy(saved['continuous_endpoints'][0]['per_size'][-1]);row[key]='-100' if key=='Rayleigh_upper' else '100'
  try:checkrow(row)
  except AssertionError:bad.append(name)
  else:raise AssertionError(name)
 out=dict(status='PASS_SHORT_L2_THROUGH_L7_ONLY',coupling_interval=['0','3/20'],uniform_gap=str(rounded),uniform_gap_display=float(rounded),unique_ground=True,all_size_bootstrap_claim=False,physical_moments=mm,local_preserving_psd_pivots=local_pivots,endpoint_bounds=endpoints,unexecuted_next_span_budget_checked=True,root_brackets=roots,limiting_fixed_method_zero=lim,concavity_certificates=concavity,adversarial_rejections=bad,producer_manifest_sha256=sha(mf),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (H/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['uniform_gap_display'],out['seconds'],out['peak_rss_kib'])
if __name__=='__main__':main()
