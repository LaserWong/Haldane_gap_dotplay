"""Independent rational-congruence spectral and full thermal replay. No producer imports."""
import os,sys
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
sys.dont_write_bytecode=True
import json,math,itertools,time,resource,hashlib,shutil
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import physical_core as P
import scalar_core as S
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;SOURCE=BASE/'chain_frontier_above_02';SNAP=HERE/'snapshot';ROOT=BASE.parent

def save(n,x):(HERE/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inertia(A):
 """Exact rational congruence, diagonal pivots plus nonsingular 2x2 fallback."""
 A=[[F(x) for x in r] for r in A];neg=zero=0;piv=[]
 assert all(A[i][j]==A[j][i] for i in range(len(A)) for j in range(len(A)))
 while A:
  n=len(A);ix=next((i for i in range(n) if A[i][i]),None)
  if ix is not None:
   order=[ix]+[i for i in range(n) if i!=ix];A=[[A[i][j] for j in order] for i in order];d=A[0][0]
   neg+=d<0;piv.append(str(d));A=[[A[i][j]-A[i][0]*A[0][j]/d for j in range(1,n)] for i in range(1,n)]
  else:
   pair=next(((i,j) for i in range(n) for j in range(i+1,n) if A[i][j]),None)
   if pair is None:zero+=n;break
   i,j=pair;order=[i,j]+[k for k in range(n) if k not in pair];A=[[A[i][j] for j in order] for i in order];b=A[0][1]
   neg+=1;piv.append('2x2 offdiagonal '+str(b));A=[[A[i][j]-(A[i][0]*A[1][j]+A[i][1]*A[0][j])/b for j in range(2,n)] for i in range(2,n)]
 return neg,zero,piv

def moments(mom):
 states=[s for s in itertools.product(range(9),repeat=4) if sum(P.EX[x] for x in s)<3];assert len(states)==67
 assert mom['basis']==list(map(list,states));weights=[P.metric(s) for s in states];ids=set(states);acts=[P.action(s) for s in states]
 K=[[weights[i]*acts[j].get(states[i],F(0)) for j in range(67)] for i in range(67)]
 J=[[sum((P.metric(s)*v*acts[j].get(s,F(0)) for s,v in acts[i].items()),F(0)) for j in range(67)] for i in range(67)]
 # Build full residual directly by projecting leaked physical configurations, not subtracting moments.
 R=[[sum((P.metric(s)*v*acts[j].get(s,F(0)) for s,v in acts[i].items() if s not in ids),F(0)) for j in range(67)] for i in range(67)]
 assert all(R[i][j]==J[i][j]-sum(K[i][k]*K[k][j]/weights[k] for k in range(67)) for i in range(67) for j in range(67))
 assert list(map(F,mom['Gram_diagonal']))==weights
 for key,mat in [('unit_K',K),('unit_J',J),('unit_residual_Gram',R)]:assert [list(map(F,r)) for r in mom[key]]==mat,key
 mags=[sum(P.MAG[x] for x in s) for s in states];blocks=[[i for i in range(67) if mags[i]==m] for m in sorted(set(mags))]
 assert all(K[i][j]==R[i][j]==0 for i in range(67) for j in range(67) if mags[i]!=mags[j])
 bins=Counter();quintets=0
 for st in itertools.product(range(9),repeat=4):
  E=sum(P.EX[x] for x in st);bins[E]+=1
  assert (st in ids)==(E<3)
  if sum(x!=0 for x in st)==1 and E==3:quintets+=1;assert st not in ids
 assert sum(bins.values())==6561 and sum(n for e,n in bins.items() if e>=3)==6494 and quintets==20
 union=set().union(*(set(a) for a in acts));assert mom['full_action_union']==len(union) and mom['residual_union']==len(union-ids)
 rep=dict(reference_dimension=67,orthogonal_product_basis=True,full_dimension=6561,omitted_count=6494,single_quintets_in_complement=quintets,full_action_union=len(union),residual_union=len(union-ids),residual_configurations_with_quintets=sum(any(x>=4 for x in st) for st in union-ids),magnetization_block_dimensions=list(map(len,blocks)),reference_bins=sorted(bins.items()))
 return states,weights,K,J,R,blocks,bins,rep

def local(lc,g):
 assert F(lc['coupling'])==g
 a,b=F(lc['a']),F(lc['b']);A=[[F(0)]*81 for _ in range(81)]
 for c,d in itertools.product(range(9),repeat=2):
  j=9*c+d;A[j][j]=(a*(P.EX[c]+P.EX[d])+b)*P.W[c]*P.W[d]
  for r,s,v in P.K[c,d]:A[9*r+s][j]+=g*v*P.W[r]*P.W[s]
 piv=P.psd(A);assert all(x>0 for x in piv)
 return a,b,list(map(str,piv))

def patch(s,g,data):
 states,w,K,J,R,blocks,bins,_=data;info=s['expanded_band'];a,b,piv=local(info['local_comparison'],g);alpha=1-2*a;B=4*b;cut=3*alpha-B
 assert alpha>0 and [alpha,B,cut]==list(map(F,[info['alpha'],info['B'],info['omitted_cutoff']]))
 assert info['dimension']==67 and info['remaining_count']==6494 and info['omitted_reference_excitation']==3
 assert info['complete_reference_bins']==[list(z) for z in sorted(bins.items())]
 count=0;proof=[];endpoints=info['comparison_endpoints'];previous=None
 for row in endpoints:
  t=F(row['lower']);assert t<cut and (previous is None or previous<t);previous=t;neg=zero=0;p=[]
  for block in blocks:
   mat=[[(cut-t)*((sum(P.EX[x] for x in states[i])-t)*w[i]*(i==j)+g*K[i][j])-g*g*R[i][j] for j in block] for i in block]
   nn,zz,pp=inertia(mat);neg+=nn;zero+=zz;p.append(pp)
  assert neg==count==row['negative_inertia'] and zero==row['zero_inertia']==0
  assert isinstance(row['multiplicity'],int) and row['multiplicity']>0
  proof.append(dict(threshold=str(t),negative=neg,zero=zero,multiplicity=row['multiplicity'],rational_congruence_pivots=p));count+=row['multiplicity']
 assert count==67 and endpoints[0]['multiplicity']==1
 assert F(endpoints[0]['lower'])<F(s['ground_lower'])+8<F(endpoints[1]['lower'])
 return dict(inertia_endpoints=proof,strict_local_pivots=piv,complement_cutoff=str(cut),ground_replacement_lower=s['ground_lower'])

def trace_upper(serialized,beta):
 s=json.loads(serialized);info=s['expanded_band'];rho=F(s['exact_rayleigh']);lo=F(s['ground_lower']);alpha=F(info['alpha']);B=F(info['B'])
 total=S.expbox(beta*(rho-lo))[1]
 for row in info['comparison_endpoints'][1:]:total+=row['multiplicity']*S.expbox(-beta*(-8+F(row['lower'])-rho))[1]
 for e,m in info['complete_reference_bins']:
  if e>=3:total+=m*S.expbox(-beta*(-8+alpha*e-B-rho))[1]
 return total
S.trace_upper=trace_upper

def main():
 start=time.monotonic();data=moments(json.loads((SNAP/'expanded_moments.json').read_text()));save('physical_premises.json',data[-1]);results=[]
 sys.path.insert(0,str(BASE/'chain_frontier_review'));import independent_core as C
 matrix=json.loads((BASE/'joint_ratio_review/chain_snapshot/M8_two_trial_moments.json').read_text())
 for path in sorted(SNAP.glob('candidate_g*.json')):
  rec=json.loads(path.read_text());g=F(rec['g']);s=rec['input']['small'];physical=patch(s,g,data);C.DATA=SNAP;ground=C.check_ground(s)
  large=rec['input']['large'];rho8=S.expectation(matrix,list(map(F,large['combination_integers'])),g);assert rho8==F(large['exact_rayleigh']) and large['full_dimension']==9**8 and large['trial_support']==43294
  paths=[]
  for row in rec['rows']:
   r=S.scalar(rec,row);bb=row['all_size_bridge'];j=F(row['J_lower']);win=S.window(bb['initial_M4_M8_window'],S.floor(S.root(j)),j,j,4,F(row['beta']))
   a,b,piv=local(bb['local_comparison'],g);short=[]
   assert [z['M'] for z in bb['M2_M3']]==[2,3]
   for z in bb['M2_M3']:
    n=z['M'];gap=1-2*a-n*b;assert gap>0 and F(z['gap_lower'])==gap and F(z['second_eigenvalue_lower'])==-2*n+gap
    assert z['full_dimension']==9**n and z['physical_sites']==2*n and F(z['rayleigh_upper'])==-2*n;short.append(gap)
   gap=min(F(r['M_ge8_gap_lower']),F(win['gap_lower']),*short);assert gap==F(row['all_M_ge2_gap_lower'])==F(bb['all_M_ge2_gap_lower'])
   paths.append(dict(scalar=r,initial_window=win,short_gaps=list(map(str,short)),gap=str(gap)))
  assert rec['best'] in rec['rows'];best=F(rec['best']['all_M_ge2_gap_lower']);assert best==max(F(p['gap']) for p in paths)
  result=dict(g=str(g),gap_lower=str(best),physical=physical,ground=ground,large_rayleigh=str(rho8),paths=paths);save('review_g'+str(g).replace('/','d')+'.json',result)
  results.append(dict(g=str(g),gap_lower=str(best),paths=len(paths),window_checks=sum(len(p['scalar']['windows'])+1 for p in paths)));print('INDEPENDENT PASS',g,best,flush=True)
 assert results,'No frozen candidate files'
 save('SUMMARY.json',dict(status='PASS_INDEPENDENT_EXACT_COUNTED_SCHUR_ALL_INTEGER_REVIEW',results=results,scope='Discrete listed couplings; all integer M>=2; unique finite-volume ground states',seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)),address_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0]))
if __name__=='__main__':main()
