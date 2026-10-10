"""Independent spin-one rank195 exact physics and obstruction review."""
import os,sys
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
sys.dont_write_bytecode=True
import json,math,itertools,time,resource,hashlib
from fractions import Fraction as F
from pathlib import Path
from collections import Counter,defaultdict
import physical_core as P
import scalar_core as S
from exact_inertia import inertia
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=BASE.parent;SNAP=HERE/'snapshot'
def save(n,x):(HERE/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def moments(mom):
 states=[s for s in itertools.product(range(9),repeat=4) if sum(P.EX[x] for x in s)<4];n=len(states);assert n==195 and mom['dimension']==n and mom['basis']==list(map(list,states))
 ids=set(states);weights=[P.metric(s) for s in states];assert list(map(F,mom['Gram_diagonal']))==weights
 acts=[P.action(s) for s in states];rows=defaultdict(list)
 for j,col in enumerate(acts):
  for st,v in col.items():rows[st].append((j,v))
 K=[[weights[i]*acts[j].get(states[i],F(0)) for j in range(n)] for i in range(n)]
 J=[[F(0)]*n for _ in range(n)];R=[[F(0)]*n for _ in range(n)]
 for st,col in rows.items():
  w=P.metric(st)
  for i,x in col:
   for j,y in col:
    z=w*x*y;J[i][j]+=z
    if st not in ids:R[i][j]+=z
 residual_check=[r[:] for r in J]
 for k in range(n):
  nz=[i for i in range(n) if K[i][k]]
  for i in nz:
   for j in nz:residual_check[i][j]-=K[i][k]*K[k][j]/weights[k]
 assert residual_check==R
 for key,mat in [('unit_K',K),('unit_J',J),('unit_residual_Gram',R)]:assert [list(map(F,r)) for r in mom[key]]==mat,key
 mags=[sum(P.MAG[x] for x in s) for s in states];blocks=[[i for i in range(n) if mags[i]==m] for m in sorted(set(mags))]
 assert blocks==mom['magnetic_blocks'] and list(map(len,blocks))==[4,22,44,55,44,22,4]
 assert all(K[i][j]==R[i][j]==0 for i in range(n) for j in range(n) if mags[i]!=mags[j])
 bins=Counter(sum(P.EX[x] for x in st) for st in itertools.product(range(9),repeat=4));assert sum(bins.values())==6561 and sum(c for e,c in bins.items() if e>=4)==6366
 quintets=[s for s in states if any(x>=4 for x in s)];assert len(quintets)==20 and all(sum(x!=0 for x in s)==1 and sum(P.EX[x] for x in s)==3 for s in quintets)
 union=set(rows);assert mom['full_action_union']==len(union) and mom['residual_union']==len(union-ids)
 report=dict(reference_dimension=n,full_dimension=6561,omitted_count=6366,single_quintets_in_P=20,Gram_orthogonality_verified=True,full_action_union=len(union),residual_union=len(union-ids),residual_configurations_with_quintets=sum(any(x>=4 for x in st) for st in union-ids),magnetic_block_sizes=list(map(len,blocks)),reference_bins=sorted(bins.items()),all_entries_checked_per_matrix=n*n)
 return states,weights,acts,K,J,R,blocks,bins,mags,report

def local(lc,g):
 assert F(lc['coupling'])==g
 a,b=F(lc['a']),F(lc['b']);A=[[F(0)]*81 for _ in range(81)]
 for c,d in itertools.product(range(9),repeat=2):
  j=9*c+d;A[j][j]=(a*(P.EX[c]+P.EX[d])+b)*P.W[c]*P.W[d]
  for r,s,v in P.K[c,d]:A[9*r+s][j]+=g*v*P.W[r]*P.W[s]
 piv=P.psd(A);assert min(piv)>0
 return a,b,piv

def patch(s,data):
 states,w,acts,K,J,R,blocks,bins,mags,_=data;n=len(states);g=F(1,4);info=s['expanded_band'];a,b,piv=local(info['local_comparison'],g);alpha=1-2*a;B=4*b;cut=4*alpha-B
 assert alpha>0 and [alpha,B,cut]==list(map(F,[info['alpha'],info['B'],info['omitted_cutoff']]))
 assert info['dimension']==195 and info['remaining_count']==6366 and info['omitted_reference_excitation']==4
 assert info['complete_reference_bins']==[list(z) for z in sorted(bins.items())]
 count=0;previous=None;proof=[]
 for row in info['comparison_endpoints']:
  t=F(row['lower']);assert t<cut and (previous is None or previous<t);previous=t;neg=zero=0;p=[];bc=[]
  for block in blocks:
   mat=[[(cut-t)*((sum(P.EX[x] for x in states[i])-t)*w[i]*(i==j)+g*K[i][j])-g*g*R[i][j] for j in block] for i in block]
   nn,zz,pp=inertia(mat);neg+=nn;zero+=zz;p.append(pp);bc.append([len(block),nn,zz])
  assert neg==count==row['negative_inertia'] and zero==row['zero_inertia']==0 and bc==row['magnetic_block_counts']
  assert isinstance(row['multiplicity'],int) and row['multiplicity']>0
  proof.append(dict(threshold=str(t),negative=neg,zero=zero,multiplicity=row['multiplicity'],magnetic_blocks=bc,exact_congruence_pivots=p));count+=row['multiplicity']
  print('ENDPOINT PASS',len(proof),neg,flush=True)
 assert count==195 and info['comparison_endpoints'][0]['multiplicity']==1
 assert F(info['comparison_endpoints'][0]['lower'])<F(s['ground_lower'])+8<F(info['comparison_endpoints'][1]['lower'])
 return dict(inertia_endpoints=proof,strict_local_pivots=list(map(str,piv)),complement_cutoff=str(cut))

def ladder(vec,op,data):
 states=data[0];n=len(states);idx=dict(zip(states,range(n)));out=[F(0)]*n
 for j,v in enumerate(vec):
  if not v:continue
  for site in range(4):
   for dest in range(9):
    c=P.O[0,op][dest][states[j][site]]+P.O[1,op][dest][states[j][site]]
    if c:
     st=list(states[j]);st[site]=dest;assert tuple(st) in idx;out[idx[tuple(st)]]+=v*c
 return out

def triplet(tw,s,data):
 states,w,acts,K,J,R,blocks,bins,mags,_=data;n=len(states);vv=[list(map(F,v)) for v in tw['vectors']];assert len(vv)==3 and all(len(v)==n for v in vv)
 assert all(x==0 for x in ladder(vv[0],'+',data)) and all(x==0 for x in ladder(vv[2],'-',data))
 for i in [0,1]:assert ladder(vv[i],'-',data)==vv[i+1] and ladder(vv[i+1],'+',data)==vv[i]
 norms=[];energies=[]
 for vec,mag in zip(vv,[1,0,-1]):
  assert all(x==0 or mags[i]==mag for i,x in enumerate(vec));norm=sum(wi*x*x for wi,x in zip(w,vec));assert norm==F(tw['metric_norm'])>0;norms.append(norm)
  action=defaultdict(F)
  for j,v in enumerate(vec):
   if v:
    action[states[j]]+=sum(P.EX[x] for x in states[j])*v
    for st,x in acts[j].items():action[st]+=F(1,4)*v*x
  en=sum(w[i]*v*action[states[i]] for i,v in enumerate(vec))/norm;assert en==F(tw['shifted_rayleigh']);energies.append(en)
 assert all(sum(w[k]*vv[i][k]*vv[j][k] for k in range(n))==0 for i in range(3) for j in range(i))
 assert len(set(norms))==len(set(energies))==1
 ids=[i for i,z in enumerate(mags) if z==1];targets=[i for i,z in enumerate(mags) if z==2];raising=[]
 for j in ids:
  v=[F(0)]*n;v[j]=1;rv=ladder(v,'+',data);assert all(x==0 or i in targets for i,x in enumerate(rv));raising.append([rv[i] for i in targets])
 mat=list(map(list,zip(*raising)));assert mat==[list(map(F,row)) for row in tw['raising_matrix']] and ids==tw['highest_weight_ids'] and targets==tw['target_magnetization_two_ids']
 ns=[list(map(F,row)) for row in tw['nullspace_basis']];assert len(ns)==22 and len(ids)==44
 assert all(sum(x*y for x,y in zip(row,v))==0 for row in mat for v in ns)
 # Exact rank by Gaussian elimination; twenty-two independent kernel vectors are checked separately.
 def rank(mat):
  a=[r[:] for r in mat];r=0
  for j in range(len(a[0])):
   k=next((k for k in range(r,len(a)) if a[k][j]),None)
   if k is None:continue
   a[r],a[k]=a[k],a[r];pivot=a[r][j]
   for k in range(r+1,len(a)):
    if a[k][j]:c=a[k][j]/pivot;a[k]=[x-c*y for x,y in zip(a[k],a[r])]
   r+=1
   if r==len(a):break
  return r
 assert rank(mat)==22 and rank(ns)==22 and tw['highest_weight_nullspace_dimension']==22
 co=list(map(F,tw['combination_integers']));assert len(co)==22
 assert all(vv[0][j]==sum(c*v[i] for c,v in zip(co,ns)) for i,j in enumerate(ids))
 d=energies[0]-8-F(s['exact_rayleigh']);assert d==F(tw['excitation_relative_to_ground_rayleigh']) and F(tw['unshifted_rayleigh'])==energies[0]-8
 return dict(status='EXACT_ORTHOGONAL_SPIN_ONE_TRIPLET_VERIFIED',norm=str(norms[0]),shifted_energy=str(energies[0]),excitation=str(d),orthogonal_magnetizations=[1,0,-1],raising_rank=22,highest_weight_kernel_dimension=22)

def main():
 start=time.monotonic();data=moments(json.loads((SNAP/'expanded_moments.json').read_text()));save('physical_premises.json',data[-1]);print('MOMENTS PASS',data[-1],flush=True)
 rec=json.loads((SNAP/'expanded_inputs.json').read_text())[0];assert rec['g']=='1/4';s=rec['small']
 tw=triplet(json.loads((SNAP/'triplet_witness.json').read_text()),s,data);save('triplet_review.json',tw);print('TRIPLET PASS',tw['excitation'],flush=True)
 physics=patch(s,data);save('physical_endpoint_review.json',physics)
 sys.path.insert(0,str(BASE/'chain_frontier_review'));import independent_core as C
 C.DATA=ROOT/rec['small_folder'];ground=C.check_ground(s);save('ground_review.json',ground)
 save('PHYSICS_SUMMARY.json',dict(status='PASS_EXACT_RANK195_PHYSICS_AND_SPIN_ONE_TRIALS',seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)),address_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0]));print('ALL PHYSICS PASS',flush=True)
if __name__=='__main__':main()
