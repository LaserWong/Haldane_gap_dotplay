"""Exact moment linkage, Rayleigh and span-exclusion replay after full-image verification."""
import json,math,resource
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(590,600));HERE=Path(__file__).resolve().parent
load=lambda n:json.loads((HERE/n).read_text())
full=load('full.json');second=load('second.json');images=load('image_verification.json');assert images['status']=='ALL_FULL_IMAGES_REPLAYED_WITH_PYTHON_INTEGERS';assert load('energy_replay.json')['value']==second['moment3_scaled'];assert second['norm']==full['moment2_scaled'] and second['moment1_scaled']==full['moment3_scaled']
rec=json.loads((HERE.parent/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];mat=json.loads((HERE.parent/'chain_filter_extension/M8_two_trial_moments.json').read_text());c=list(map(int,rec['large']['combination_integers']));N=sum(c[i]*F(mat['G'][i][j])*c[j] for i in range(2) for j in range(2));den=full['integer_denominator'];assert N==F(full['norm']);rho=F(rec['large']['exact_rayleigh']);assert F(full['moment1_scaled'])==rho*den*N
W=[3,2,2,2,1,2,6,2,1]
def norm(name):
 value=0;count=0
 with (HERE/name).open() as f:
  for line in f:
   key,x=map(int,line.split());value+=math.prod(W[(key>>(4*i))&15] for i in range(8))*x*x;count+=1
 return value,count
n1,c1=norm('full_image.txt');n2,c2=norm('second_image.txt');assert n1==int(full['moment2_scaled']) and n2==int(second['moment2_scaled']);assert c1==full['image_support'] and c2==second['image_support']
mom=[F(1)]+[F(full[f'moment{k}_scaled'])/(den**k*N) for k in range(1,4)]+[F(second['moment2_scaled'])/(den**4*N),F(second['moment3_scaled'])/(den**5*N)]
r2=load('rayleigh.json');var=mom[2]-rho*rho;hrr=mom[3]-2*rho*mom[2]+rho**3;tau=F(r2['tau']);assert F(r2['exact_rayleigh'])==(rho+2*tau*var+tau*tau*hrr)/(1+tau*tau*var)
target=2*F(rec['small']['exact_rayleigh'])+F(19,1250)
def pivots(M):
 M=[r[:] for r in M];ps=[]
 for k in range(len(M)):
  p=M[k][k];assert p>0;ps.append(p)
  for i in range(k+1,len(M)):
   for j in range(k+1,len(M)):M[i][j]-=M[i][k]*M[k][j]/p
 return ps
p2=pivots([[rho-target,var],[var,hrr-target*var]]);assert p2==list(map(F,r2['span_target_LDL_pivots']))
checks=[]
for name in ['rayleigh_three.json','rayleigh_four.json']:
 r=load(name);G=[list(map(F,row)) for row in r['Gram']];n=len(G);c=list(map(F,r['coefficients']));assert min(pivots(G))>0
 if n==3:
  cm=[sum(F(math.comb(k,j))*(-rho)**(k-j)*mom[j] for j in range(k+1)) for k in range(6)];assert list(map(F,r['moments']))==mom and list(map(F,r['centered_moments']))==cm;assert G==[[cm[i+j] for j in range(n)] for i in range(n)];H=[[cm[i+j+1]+rho*G[i][j] for j in range(n)] for i in range(n)]
 else:H=[list(map(F,row)) for row in r['H']]
 bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(n) for j in range(n));en=bil(H)/bil(G);assert en==F(r['exact_rayleigh'])>target;ps=pivots([[H[i][j]-target*G[i][j] for j in range(n)] for i in range(n)]);assert ps==list(map(F,r['span_target_LDL_pivots'])) and r['span_exclusion'] and not r['meets_necessary_target'];checks.append(dict(file=name,dimension=n,rayleigh=str(en),delta=str(en-2*F(rec['small']['exact_rayleigh'])),target_exclusion_pivots=list(map(str,ps))))
(HERE/'certificate_verification.json').write_text(json.dumps(dict(status='PRODUCER_PHYSICAL_AND_EXACT_SPAN_REPLAY_PASS',largest_image_support=c2,moments_verified_through=5,rayleigh_checks=checks,necessary_delta_bound='19/1250',rounding_note='The exact necessary improvement is0.00042614385686183293...; >0.000426143856861 is a safe strict decimal, whereas0.000426143856862 is approximate.'),indent=2));print('CERTIFICATE REPLAY PASS',flush=True)
