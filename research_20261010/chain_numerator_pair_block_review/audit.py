"""Independent exact singlet pair-sector, block-action and reusable numerator audit."""
import sys
sys.dont_write_bytecode=True;sys.set_int_max_str_digits(0)
import accepted_action_core as A
import json,math,time,resource
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;PAIR=HERE/'pair_snapshot';BLOCK=HERE/'block_snapshot';OLD=BASE/'chain_m8_numerator_review/snapshot'
def save(n,x):(HERE/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def parse(rows):
 out={}
 for k,x in rows:
  k=int(k);assert A.validkey(k) and k not in out;out[k]=int(x);assert out[k]!=0
 return out
R={op:{i:[(j,int(v)) for j in range(9) if (v:=A.P.O[0,op][j][i]+A.P.O[1,op][j][i])!=0] for i in range(9)} for op in ['+','-']}
assert all(A.P.O[0,op][j][i]+A.P.O[1,op][j][i]==int(A.P.O[0,op][j][i]+A.P.O[1,op][j][i]) for op in ['+','-'] for i in range(9) for j in range(9))
def spin(v,op):
 out=defaultdict(int)
 for k,x in v.items():
  for site in range(8):
   sh=4*site
   for dst,c in R[op][(k>>sh)&15]:out[(k&~(15<<sh))|(dst<<sh)]+=c*x
 return {k:x for k,x in out.items() if x}
def symmetry(v):
 translated={((k<<4)&0xffffffff)|(k>>28):x for k,x in v.items()};reflected={}
 for k,x in v.items():
  labs=[(k>>(4*i))&15 for i in range(8)];assert sum(A.P.MAG[z] for z in labs)==0
  key=sum(z<<(4*(7-i)) for i,z in enumerate(labs));reflected[key]=x*(-1)**sum(z in [1,2,3] for z in labs)
 assert translated==reflected==v and not spin(v,'+') and not spin(v,'-')

def pivots(mat,zero_allowed=False):
 m=[[F(x) for x in row] for row in mat];n=len(m);assert all(m[i][j]==m[j][i] for i in range(n) for j in range(n));out=[]
 for i in range(n):
  p=m[i][i];out.append(p)
  if p==0:
   assert zero_allowed and i==n-1;return out
  assert p>0
  for j in range(i+1,n):
   for k in range(j,n):m[j][k]=m[k][j]=m[j][k]-m[j][i]*m[k][i]/p
 return out

def readold():
 ans=[]
 for name,skip in [('packed_input.txt',82),('packed_old_direction.txt',82),('full_image.txt',0),('second_image.txt',0)]:
  v={}
  with (OLD/name).open() as f:
   for _ in range(skip):next(f)
   for line in f:
    k,x=map(int,line.split());assert k not in v
    if x:v[k]=x
  ans.append(v)
 return ans

def matrices(old,small,images):
 n=4+len(small);G=[[F(0)]*n for _ in range(n)];H=[[F(0)]*n for _ in range(n)]
 prior=json.loads((BASE/'chain_m8_numerator_review/independent_moments.json').read_text())
 for i in range(4):
  for j in range(4):G[i][j]=F(prior['Gram'][i][j]);H[i][j]=F(prior['Hamiltonian'][i][j])
 allv=old+small
 for i,(v,im) in enumerate(zip(small,images),4):
  for j,w in enumerate(allv):G[i][j]=G[j][i]=F(A.dot(v,w));H[i][j]=H[j][i]=F(A.dot(im,w),144)
 # Check both physical orientations whenever both scaled actions are explicit.
 for i,im in enumerate(images):
  for j in range(len(small)):assert A.dot(im,small[j])==A.dot(small[i],images[j])
 for i,(v,im) in enumerate(zip(small,images)):
  assert A.dot(im,old[0])==A.dot(v,old[2])
  assert A.dot(im,old[2])==A.dot(v,old[3])
 return G,H

def certify(rec,G,H,rho,rho4):
 n=len(G);assert G==[list(map(F,r)) for r in rec['Gram']] and H==[list(map(F,r)) for r in rec['H']]
 gp=pivots(G);assert gp==list(map(F,rec['Gram_LDL_pivots']));target=2*rho4+F(19,1250);sp=pivots([[H[i][j]-target*G[i][j] for j in range(n)] for i in range(n)])
 assert sp==list(map(F,rec['span_target_LDL_pivots']))
 c=list(map(F,rec['coefficients']));assert len(c)==n
 bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(n) for j in range(n));norm=bil(G);en=bil(H);q=en/norm
 assert norm>0 and q==F(rec['exact_rayleigh']) and q-2*rho4==F(rec['new_delta']) and q>target
 assert F(rec.get('necessary_target',rec.get('necessary_target_rayleigh')))==target and rec.get('span_excluded',rec.get('span_exclusion')) is True and rec['meets_necessary_target'] is False
 assert F(rec.get('improvement',rec.get('improvement_from_original')))==rho-q
 return dict(rank=n,exact_norm=str(norm),exact_energy_numerator=str(en),exact_rayleigh=str(q),delta=str(q-2*rho4),delta_display=float(q-2*rho4),Gram_pivots=list(map(str,gp)),old_target_pivots=list(map(str,sp)),scope='Old canonical-transport route only; does not exclude the newly proposed direct time-first window')

def main():
 start=time.monotonic();cpu=time.process_time();rec=json.loads((PAIR/'pair_extension.json').read_text());base=json.loads((BASE/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];rho=F(base['large']['exact_rayleigh']);rho4=F(base['small']['exact_rayleigh']);small=[{0:1}];orbits=[]
 allpairs=set()
 for sep in [1,2,3,4]:
  pairs=sorted({tuple(sorted((i,(i+sep)%8))) for i in range(8)});assert not(allpairs&set(pairs));allpairs.update(pairs);v={}
  for i,j in pairs:
   for a,b,c in [(1,3,1),(2,2,-1),(3,1,1)]:v[(a<<(4*i))|(b<<(4*j))]=c
  small.append(v);orbits.append(dict(separation=sep,pairs=list(map(list,pairs)),orbit_size=len(pairs)))
 assert len(allpairs)==28 and orbits==rec['orbits'];assert small==list(map(parse,rec['bare_vectors'])) and list(map(len,small))==[1,24,24,24,12]
 for j,v in enumerate(small):symmetry(v);assert all(A.energy(k)+16==(0 if j==0 else 2) for k in v)
 assert [A.dot(v,v) for v in small]==[6561,69984,69984,69984,34992]
 assert all(A.dot(small[i],small[j])==0 for i in range(5) for j in range(i))
 images=[A.action(v)[0] for v in small];assert images==list(map(parse,rec['bare_H_images_scaled']))
 for v in images:symmetry(v)
 need=set().union(*map(set,small),*map(set,images));old=readold();assert len(set().union(*map(set,images)))==rec['bare_action_union']==1961 and len(need)==rec['needed_support_size']
 assert [{k:x for k,x in v.items() if k in need} for v in old]==list(map(parse,rec['old_vector_values_on_needed_support']))
 G,H=matrices(old,small,images);reports=[certify(rec,G,H,rho,rho4)]
 ix=[0,1,4,5,6,7,8];assert pivots([[G[i][j] for j in ix] for i in ix])==list(map(F,rec['old_two_union_Gram_LDL_pivots']))
 assert rec['bare_sector_dimension']==5 and rec['combined_trial_dimension']==9 and rec['intersection_with_bare_sector_dimension']==0
 print('PAIR SECTOR AND RANK9 PASS',reports[-1]['delta_display'],flush=True);front=images[:];ranklogs=[];image_stats=[]
 for level in [1,2]:
  rec=json.loads((BLOCK/f'block_{level}.json').read_text());oldn=len(G);selected=[];logs=[]
  for ci,im in enumerate(front):
   divisor=math.gcd(*im.values());assert divisor>0;v={k:x//divisor for k,x in im.items()};row=[F(A.dot(v,z)) for z in old+small];trial=[G[i]+[row[i]] for i in range(len(G))]+[row+[F(A.dot(v,v))]];pp=pivots(trial,True);ind=pp[-1]>0
   log=dict(candidate=ci,support=len(v),independent=ind,last_Gram_pivot=str(pp[-1]));assert log==rec['rank_tests'][ci];logs.append(log)
   if ind:G=trial;small.append(v);selected.append(v)
  assert len(logs)==len(rec['rank_tests']) and small==list(map(parse,rec['small_vectors']))
  added=[]
  for v in selected:
   symmetry(v);im,visits=A.action(v);symmetry(im);added.append(im);image_stats.append(dict(level=level,support=len(im),full_transitions=visits))
  assert added==list(map(parse,rec['next_frontier']));images.extend(added);freshG,H=matrices(old,small,images);assert freshG==G
  assert rec['previous_rank']==oldn and rec['trial_rank']==len(G)==9+4*level and rec['new_rank']==len(selected)==4
  reports.append(certify(rec,G,H,rho,rho4));ranklogs.append(logs);front=added
  print('BLOCK PASS',level,len(G),reports[-1]['delta_display'],flush=True)
 num=json.loads((BLOCK/'numerator_input.json').read_text());r=reports[-1];assert num['g']=='1/4' and num['M']==8 and num['physical_Hilbert_dimension']==9**8 and num['trial_rank']==17
 assert num['trial_source']=='block_2.json' and num['trial_source_sha256']==A.sha(BLOCK/'block_2.json')
 for target,key in [('exact_norm','exact_norm'),('exact_energy_numerator','exact_energy_numerator'),('exact_rayleigh','exact_rayleigh'),('exact_delta_against_saved_M4','delta')]:assert F(num[target])==F(r[key])
 save('certified_numerator.json',dict(status='INDEPENDENTLY_CERTIFIED_REUSABLE_RAYLEIGH_INPUT',g='1/4',M=8,full_dimension=9**8,trial_rank=17,retained_numerator_terms=1,exact_norm=r['exact_norm'],exact_energy_numerator=r['exact_energy_numerator'],exact_rayleigh=r['exact_rayleigh'],exact_delta_against_saved_M4=r['delta'],source_sha256=A.sha(BLOCK/'numerator_input.json'),new_direct_time_first_window_excluded=False))
 save('exact_reviews.json',dict(reports=reports,rank_tests=ranklogs,full_new_images=image_stats,bare_spin_zero_translation_even_reflection_even=True,all_new_vectors_and_images_quantum_numbers_verified=True))
 save('SUMMARY.json',dict(status='PASS_PHYSICAL_PAIR_SECTOR_AND_RANK9_13_17_NUMERATOR_INPUTS',ranks=[9,13,17],delta_displays=[r['delta_display'] for r in reports],new_direct_window_excluded=False,old_target_scope_only=True,bare_sector_dimension=5,unordered_pairs=28,translation_orbit_lengths=[8,8,8,4],bare_action_union=1961,rank17_numerator_input_certified=True,cpu_seconds=time.process_time()-cpu,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(A.os.sched_getaffinity(0)),address_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0]));print('ALL PAIR/BLOCK PHYSICS PASS',flush=True)
if __name__=='__main__':main()
