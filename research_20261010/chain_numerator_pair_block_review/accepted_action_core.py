"""Independent arbitrary-precision physical M8 action and four-dimensional numerator audit."""
import os,sys
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
sys.dont_write_bytecode=True
import json,math,time,resource,hashlib
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import physical_core as P
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=BASE.parent;SNAP=HERE/'snapshot'
DEN=math.lcm(*((F(1,4)*v).denominator for row in P.K.values() for _,_,v in row));assert DEN==144
KERNEL={key:[(a,b,int(DEN*F(1,4)*v)) for a,b,v in row] for key,row in P.K.items()}
assert all(DEN*F(1,4)*v==int(DEN*F(1,4)*v) for row in P.K.values() for _,_,v in row)
EDGES=[(4*((i-1)%8),4*i) for i in range(8)];MASKS=[~((15<<a)|(15<<b)) for a,b in EDGES]
def save(n,x):(HERE/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def weight(key):
 w=1
 for i in range(8):w*=P.W[(key>>(4*i))&15]
 return w
def energy(key):return -16+sum(P.EX[(key>>(4*i))&15] for i in range(8))
def validkey(k):return isinstance(k,int) and 0<=k<2**32 and all(((k>>(4*i))&15)<9 for i in range(8))
def read_packed(path):
 with path.open() as f:
  den,n=map(int,next(f).split());assert den==DEN
  for a in range(9):
   for b in range(9):
    row=list(map(int,next(f).split()));assert len(row)==1+3*row[0]
    triples=[tuple(row[i:i+3]) for i in range(1,len(row),3)];assert triples==KERNEL[a,b]
  vec={};count=0
  for line in f:
   k,v=map(int,line.split());assert validkey(k) and k not in vec;vec[k]=v;count+=1
  assert count==n
 return vec

def verify_file_vector(path,vec,packed=False):
 count=0;seen=set()
 with path.open() as f:
  if packed:
   den,n=map(int,next(f).split());assert den==DEN and n==len(vec)
   for a in range(9):
    for b in range(9):
     row=list(map(int,next(f).split()));assert row[0]*3+1==len(row) and [tuple(row[i:i+3]) for i in range(1,len(row),3)]==KERNEL[a,b]
  for line in f:
   k,v=map(int,line.split());assert validkey(k) and k not in seen and v==vec.get(k) and v!=0;seen.add(k);count+=1
 assert count==len(vec),('missing action entries',path,count,len(vec))

def action(vec):
 out={};visits=0
 for key,x in vec.items():
  assert type(x) is int
  if not x:continue
  out[key]=out.get(key,0)+DEN*energy(key)*x
  for (l,r),mask in zip(EDGES,MASKS):
   for a,b,c in KERNEL[(key>>l)&15,(key>>r)&15]:
    target=(key&mask)|(a<<l)|(b<<r);out[target]=out.get(target,0)+c*x;visits+=1
 return {k:v for k,v in out.items() if v},visits

def dot(a,b):
 if len(a)>len(b):a,b=b,a
 return sum(x*b.get(k,0)*weight(k) for k,x in a.items())

def contract_energy(vec):
 """Full directed physical contraction; outside-bra action is exactly zero, not omitted residual."""
 weighted={k:weight(k)*v for k,v in vec.items()};total=0;visits=0
 for key,x in vec.items():
  total+=DEN*energy(key)*x*weighted[key]
  for (l,r),mask in zip(EDGES,MASKS):
   for a,b,c in KERNEL[(key>>l)&15,(key>>r)&15]:
    target=(key&mask)|(a<<l)|(b<<r);total+=x*c*weighted.get(target,0);visits+=1
 return total,visits

def ldlt(matrix):
 n=len(matrix);a=[[F(x) for x in r] for r in matrix];assert all(a[i][j]==a[j][i] for i in range(n) for j in range(n));piv=[]
 for k in range(n):
  p=a[k][k];assert p>0,('nonpositive pivot',k,p);piv.append(p)
  for i in range(k+1,n):
   for j in range(i,n):a[i][j]=a[j][i]=a[i][j]-a[i][k]*a[j][k]/p
 return piv

def four_span(G,H,rec,rho,target):
 n=4;assert rec['trial_dimension']==n and [list(map(F,r)) for r in rec['Gram']]==G and [list(map(F,r)) for r in rec['H']]==H
 gp=ldlt(G);sp=ldlt([[H[i][j]-target*G[i][j] for j in range(n)] for i in range(n)])
 assert gp==list(map(F,rec['Gram_LDL_pivots'])) and sp==list(map(F,rec['span_target_LDL_pivots']))
 c=list(map(F,rec['coefficients']));assert len(c)==n
 bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(n) for j in range(n));norm=bil(G);assert norm>0;rq=bil(H)/norm
 assert rq==F(rec['exact_rayleigh']) and rho-rq==F(rec['improvement']) and rq>target==F(rec['necessary_target_rayleigh']) and rec['span_exclusion'] is True and rec['meets_necessary_target'] is False
 return dict(rank=4,Gram_positive_pivots=list(map(str,gp)),target_positive_pivots=list(map(str,sp)),target=str(target),exact_rayleigh=str(rq),improvement=str(rho-rq),improvement_display=float(rho-rq),gap_above_necessary_target=str(rq-target),all_complex_coefficients_covered=True)

def main():
 started=time.monotonic();cpu=time.process_time();rec=json.loads((BASE/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];coeff=list(map(int,rec['large']['combination_integers']));assert len(coeff)==2 and coeff[1]!=0
 paths=[BASE/'chain_frontier'/f'chain_s1_M8_g{tag}_depth4_trial.npz' for tag in ['7d40','1d5']];zs=[np.load(p,allow_pickle=False) for p in paths];basis=zs[0]['basis'];assert basis.shape==(43294,8) and np.array_equal(basis,zs[1]['basis'])
 keys=[sum(int(x)<<(4*i) for i,x in enumerate(s)) for s in basis];assert len(set(keys))==43294 and all(validkey(k) for k in keys)
 vectors=[[int(x) for x in z['vector']] for z in zs];assert all(len(v)==43294 for v in vectors)
 psi={k:coeff[0]*vectors[0][j]+coeff[1]*vectors[1][j] for j,k in enumerate(keys)};u=dict(zip(keys,vectors[0]));assert read_packed(SNAP/'packed_input.txt')==psi and read_packed(SNAP/'packed_old_direction.txt')==u
 original_u=u.copy();psi={k:v for k,v in psi.items() if v};u={k:v for k,v in u.items() if v};steps=[]
 phi,visits=action(psi);verify_file_vector(SNAP/'full_image.txt',phi);verify_file_vector(SNAP/'packed_image_input.txt',phi,True);steps.append(dict(image='144Hpsi',support=len(phi),visits=visits,max_coefficient_bits=max(abs(v).bit_length() for v in phi.values())));print('FIRST FULL IMAGE PASS',steps[-1],flush=True)
 phi2,visits=action(phi);verify_file_vector(SNAP/'second_image.txt',phi2);verify_file_vector(SNAP/'packed_second_image.txt',phi2,True);steps.append(dict(image='144^2 H^2 psi',support=len(phi2),visits=visits,max_coefficient_bits=max(abs(v).bit_length() for v in phi2.values())));print('SECOND FULL IMAGE PASS',steps[-1],flush=True)
 chi,visits=action(u);verify_file_vector(SNAP/'old_direction_image.txt',chi);steps.append(dict(image='144Hu',support=len(chi),visits=visits,max_coefficient_bits=max(abs(v).bit_length() for v in chi.values())));print('OLD DIRECTION FULL IMAGE PASS',steps[-1],flush=True)
 m=json.loads((SNAP/'full.json').read_text());m2=json.loads((SNAP/'second.json').read_text());mu=json.loads((SNAP/'old_direction.json').read_text())
 N=dot(psi,psi);q1=dot(psi,phi);q2=dot(phi,phi);q3=dot(phi,phi2);q4=dot(phi2,phi2)
 assert [N,q1,q2,q3]==[int(m[z]) for z in ['norm','moment1_scaled','moment2_scaled','moment3_scaled']]
 assert [q2,q3,q4]==[int(m2[z]) for z in ['norm','moment1_scaled','moment2_scaled']]
 q5,nvis=contract_energy(phi2);assert q5==int(m2['moment3_scaled']) and nvis==m2['contraction_transitions'];print('EXACT FIFTH MOMENT PASS',nvis,flush=True)
 u3,uv=contract_energy(chi);assert [dot(u,u),dot(u,chi),dot(chi,chi),u3]==[int(mu[z]) for z in ['norm','moment1_scaled','moment2_scaled','moment3_scaled']] and uv==mu['contraction_transitions']
 for dat,step in zip([m,m2,mu],steps):assert dat['integer_denominator']==DEN and dat['image_support']==step['support'] and dat['action_transitions']==step['visits'] and dat['image_coefficient_max_bits']==step['max_coefficient_bits']
 assert steps[1]['visits']==m['contraction_transitions']
 energy_replay=json.loads((SNAP/'energy_replay.json').read_text());assert int(energy_replay['value'])==q5 and energy_replay['support']==len(phi2)
 vs=[psi,u,phi,phi2];G=[[F(dot(a,b)) for b in vs] for a in vs];H=[[F(0)]*4 for _ in range(4)]
 for i,image in enumerate([phi,chi,phi2]):
  for j,v in enumerate(vs):H[i][j]=F(dot(image,v),DEN)
 for i in range(3):H[3][i]=H[i][3]
 H[3][3]=F(q5,DEN);assert H==list(map(list,zip(*H)))
 rho=F(q1,DEN*N);assert rho==F(rec['large']['exact_rayleigh']);rho4=F(rec['small']['exact_rayleigh']);target=2*rho4+F(19,1250)
 out=four_span(G,H,json.loads((SNAP/'rayleigh_four.json').read_text()),rho,target);out['new_delta']=str(F(out['exact_rayleigh'])-2*rho4);assert out['new_delta']==json.loads((SNAP/'rayleigh_four.json').read_text())['new_delta']
 save('four_span_review.json',out);save('independent_moments.json',dict(integer_denominator=DEN,norm=str(N),scaled_moments=list(map(str,[N,q1,q2,q3,q4,q5])),Gram=[[str(x) for x in r] for r in G],Hamiltonian=[[str(x) for x in r] for r in H],images=steps))
 report=dict(status='PASS_INDEPENDENT_FULL_ACTION_AND_FOUR_DIMENSIONAL_NUMERATOR_EXCLUSION',g='1/4',trial_dimension=4,full_dimension=9**8,old_span_included_because_second_combination_coefficient_nonzero=coeff[1],physical_sites=16,images=steps,all_coefficients_and_accumulators='Python arbitrary-precision integers, Fraction exact rational arithmetic; NumPy used only for input loading',max_moment_bits=max(abs(v).bit_length() for v in [N,q1,q2,q3,q4,q5]),one_term_target=str(target),exact_new_rayleigh=out['exact_rayleigh'],exact_improvement=out['improvement'],seconds=time.monotonic()-started,cpu_seconds=time.process_time()-cpu,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)),address_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0])
 save('SUMMARY.json',report);print('INDEPENDENT FOUR-DIMENSIONAL AUDIT PASS',report['cpu_seconds'],report['peak_rss_kib'],flush=True)
if __name__=='__main__':main()
