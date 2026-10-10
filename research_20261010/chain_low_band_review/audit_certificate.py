"""Counted-band full exact audit. Scalar helpers copied from sealed independent joint review.
No producer mathematical module is imported. The earlier review and all source bytes
are hash-checked. Full P/Q moments are independently reconstructed here.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys
sys.dont_write_bytecode=True
import resource
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from collections import Counter
import json,math,hashlib,shutil,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
PROD=HERE.parent/'chain_small_low_band';SNAP=HERE/'snapshot';PRIOR=HERE.parent/'joint_ratio_review'
BITS=384;SCALE=1<<BITS
INPUT={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 INPUT[str(p.relative_to(ROOT))]=sha(p);return json.loads(p.read_text())
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def floor(x,digits=12):return Q(x.numerator*10**digits//x.denominator,10**digits)

def root(x,digits=70):
    D=10**digits;k=math.isqrt(x.numerator*D*D//x.denominator);r=Q(k,D)
    assert r*r<=x<(r+Q(1,D))**2
    return r

def down(x):return Q(x.numerator*SCALE//x.denominator,SCALE)

def up(x):return -down(-x)

@lru_cache(maxsize=4096)
def expbox(x):
    x=Q(x)
    if x<0:
        lo,hi=expbox(-x);return down(1/hi),up(1/lo)
    n=0
    while x>Q(1,16):x/=2;n+=1
    term=Q(1);v=Q(1)
    for j in range(1,111):term=term*x/j;v+=term
    nextterm=term*x/111
    low=down(v);high=up(v+nextterm/(1-x/112))
    for _ in range(n):low=down(low*low);high=up(high*high)
    return low,high

def expectation(mat,c,g):
    k=len(c)
    bil=lambda key:sum(Q(mat[key][i][j])*c[i]*c[j] for i in range(k) for j in range(k))
    norm=bil('G');assert norm>0
    return (bil('K0')+g*bil('K1_scaled')/mat['weak_denominator'])/norm

def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)

def window(win,S,T,K,n,beta):
    assert 0<S<=1 and 0<T<=1 and S*S*T<=K<=1 and K>Q(1,2)
    assert win['cells']==[n,2*n] and Q(win['beta'])==beta
    assert [Q(win[z]) for z in ('S_lower','T_lower','joint_S2T_lower')]==[S,T,K]
    # Check the exact saved 50-decimal root witness, then independently use 70.
    savedw=Q(win['dominant_weight_lower']);savedroot=2*savedw-1
    assert savedroot*savedroot<=2*K-1<(savedroot+Q(1,10**50))**2
    savedr=Q(win['absolute_tail_ratio_upper']);savedd=Q(win['D_lower'])
    assert savedr==(1-savedw)/savedw and savedd==T/(1+savedr*savedr)
    w=(1+root(2*K-1))/2;r=(1-w)/w;d=T/(1+r*r)
    I=(1-r)*min(S*root(d),d)
    saved=Q(win['thermal_purity_lower']);gap=Q(win['gap_lower'])
    assert Q(1,2)<saved<=I and gap>0
    margin=saved-expbox(beta*gap)[1]*(1-saved);assert margin>0
    return dict(cells=[n,2*n],beta=str(beta),thermal_lower=str(saved),gap_lower=str(gap),
        independent_70digit_thermal_lower=str(floor(I,60)),exponential_margin_lower=str(margin))

def scalar(rec,row):
    beta=Q(row['beta']);small=rec['input']['small'];rho=Q(rec['input']['large']['exact_rayleigh'])
    shift=rho-2*Q(small['exact_rayleigh']);assert shift==Q(row['Rayleigh_shift'])
    sm=json.dumps(small,sort_keys=True)
    q1,q2=[Q(row[x]) for x in ('small_Q_beta_upper','small_Q_2beta_upper')]
    assert trace_upper(sm,beta)<=q1 and trace_upper(sm,2*beta)<=q2
    L=expbox(-2*beta*shift)[0];J,cc=[Q(row[x]) for x in ('J_lower','C_lower')]
    assert 0<J<=L/q1**4<=1 and 0<cc<=L/q2**2<=1
    a=floor(G(J));b=floor(G(cc*cc*a))
    assert [a,b]==list(map(Q,row['initial_time_pair'])) and a>0 and b>0
    n=8;be=2*beta;states=row['states'];wins=row['windows'];result=[];i=0
    for _ in range(row['time_steps']):
        K=a*a*b;S=floor(a*root(b));T=floor(K)
        assert states[i]==dict(order='time-space',cells=n,beta=str(be),pair=list(map(str,[a,b])),canonical_joint=str(K))
        result.append(window(wins[i],S,T,K,n,be));i+=1
        na=floor(G(K));nb=floor(G(b*b*na));assert na>0 and nb>0
        a,b=na,nb;n*=2;be*=2
    K=a*a*b;S=floor(a*root(b));T=floor(K)
    assert row['conversion']==dict(cells=n,beta=str(be),time_pair=list(map(str,[a,b])),S_lower=str(S),T_lower=str(T),joint_S2T_lower=str(K))
    assert S*S<=K and T<=K and S*S*T<=K
    conversion_base=[n,str(be)]
    for _ in range(row['canonical_steps']):
        assert states[i]==dict(order='space-time',cells=n,beta=str(be),pair=list(map(str,[S,T])),joint_S2T_lower=str(K))
        result.append(window(wins[i],S,T,K,n,be));i+=1
        S=floor(G(K));T=floor(G(T*T*S));assert 0<S<=1 and 0<T<=1
        K=S*S*T;n*=2;be*=2
    assert i==len(states)==len(wins)
    u=max(1-S,1-T);final=row['final'];d=Q(final['asymptotic_gap_lower'])
    assert final==dict(cells=n,beta=str(be),S_lower=str(S),T_lower=str(T),common_defect_upper=str(u),asymptotic_gap_lower=str(d))
    assert 0<u<=Q(1,100) and d>0
    margin=1-expbox(be*d)[1]*5*u;assert margin>0
    allgap=min([d]+[Q(w['gap_lower']) for w in result]);assert allgap==Q(row['M_ge8_gap_lower'])
    assert [w['cells'][0] for w in result]==[8*2**j for j in range(i)]
    assert n==8*2**i
    return dict(initial_beta=str(beta),time_cycles=row['time_steps'],canonical_cycles=row['canonical_steps'],
        conversion_base_cells_beta=conversion_base,windows=result,asymptotic_cells=n,asymptotic_beta=str(be),
        asymptotic_gap=str(d),asymptotic_exponential_margin_lower=str(margin),M_ge8_gap_lower=str(allgap))

def check_seal(directory,manifest):
 files=load(directory/manifest)
 for name,digest in files.items():assert sha(directory/name)==digest,('changed frozen input',name)
 return dict(manifest_sha256=sha(directory/manifest),files=len(files))

def snapshot():
 assert sha(PROD/'FROZEN_MANIFEST.json')=='2fe7f6300a64381e25bf5d41f19cafec0506a739986ded95784029b40c42470e'
 report=dict(prior_chain=check_seal(PRIOR,'CHAIN_REVIEW_MANIFEST.json'),prior_lemma=check_seal(PRIOR,'LEMMA_REVIEW_MANIFEST.json'),producer=check_seal(PROD,'FROZEN_MANIFEST.json'))
 assert sha(PRIOR/'audit_chain.py')=='f948122be5b31f7a8faea125040fb7f20568413311d56cc5ad6b9aec20ae3f24'
 SNAP.mkdir(exist_ok=True)
 for name,digest in load(PROD/'FROZEN_MANIFEST.json').items():
  p=SNAP/name
  if p.exists():assert sha(p)==digest
  else:p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PROD/name,p)
 external=load(SNAP/'EXTERNAL_INPUT_SHA256.json')
 for name,digest in external.items():assert sha(ROOT/name)==digest,('external drift',name)
 report['external_files_verified']=len(external)
 report['independent_physical_core']=sha(HERE.parent/'chain_frontier_review/independent_core.py')
 assert report['independent_physical_core']=='30c997e6e56135af60cd989ab22e31a8957346dc3ff2235ae8ac6b2c62916a19'
 return report

@lru_cache(maxsize=256)
def trace_upper(small_serialized,beta):
 s=json.loads(small_serialized);info=s['low_band'];rho=Q(s['exact_rayleigh']);lo=Q(s['ground_lower']);a=Q(info['alpha']);B=Q(info['B'])
 terms=[expbox(beta*(rho-lo))[1]]
 terms += [m['multiplicity']*expbox(-beta*(-8+Q(m['eigenvalue_lower'])-rho))[1] for m in info['triplet_modes']]
 terms += [mult*expbox(-beta*(-8+a*e-B-rho))[1] for e,mult in info['complete_reference_bins'] if e>=2]
 return sum(terms)

def verify_moments(mom):
 import verify_blocks as B
 P=[(0,0,0,0)]
 for lab in [1,2,3]:
  for site in range(4):s=[0]*4;s[site]=lab;P.append(tuple(s))
 assert mom['basis']==[list(s) for s in P]
 weights=[B.metric(s) for s in P];cols=[B.action(s) for s in P];ids=set(P)
 assert list(map(Q,mom['Gram_diagonal']))==weights
 K=[[weights[i]*cols[j].get(P[i],Q(0)) for j in range(13)] for i in range(13)]
 J=[[sum(B.metric(s)*v*cols[j].get(s,Q(0)) for s,v in cols[i].items()) for j in range(13)] for i in range(13)]
 R=[[sum(B.metric(s)*v*cols[j].get(s,Q(0)) for s,v in cols[i].items() if s not in ids) for j in range(13)] for i in range(13)]
 for calc,key in [(K,'unit_K'),(J,'unit_J'),(R,'unit_residual_Gram')]:assert calc==[list(map(Q,r)) for r in mom[key]],key
 assert all(J[i][j]-sum(K[i][k]*K[k][j]/weights[k] for k in range(13))==R[i][j] for i in range(13) for j in range(13))
 assert mom['retained_reference_dimension']==13 and mom['full_dimension']==6561
 union=set().union(*(set(c) for c in cols))
 assert mom['full_shifted_H_applied_union_support']==len(union)==172
 assert mom['full_unshifted_H_applied_union_support']==len(union|{P[0]})==173
 assert mom['trial_plus_action_union_support']==len(union|ids)==173
 assert mom['full_residual_union_support']==len(union-ids)==160
 return dict(all_13_columns_rebuilt=True,all_169_entries_G_K_J_residual_Gram_verified=True,P_dimension=13,full_dimension=6561,shifted_H_applied_union_support=172,unshifted_H_applied_union_support=173,trial_plus_action_union_support=173,residual_union_support=160)

def verify_patch(s,g):
 import verify_blocks as B
 assert 0<g<1
 info=s['low_band'];lc=info['local_comparison'];a,b=Q(lc['a']),Q(lc['b'])
 assert Q(lc['coupling'])==g and a==g/2 and b==g+Q(1,10**12)
 A=[[Q(0)]*81 for _ in range(81)]
 for c in range(9):
  for d in range(9):
   j=9*c+d;A[j][j]=(a*(B.EX[c]+B.EX[d])+b)*B.W[c]*B.W[d]
   for r,t,v in B.K[c,d]:A[9*r+t][j]+=g*v*B.W[r]*B.W[t]
 piv=[]
 for m in range(-4,5):
  ids=[j for j in range(81) if B.MAG[j//9]+B.MAG[j%9]==m]
  assert all(A[i][j]==0 for i in ids for j in range(81) if j not in ids)
  p=B.psd([[A[i][j] for j in ids] for i in ids]);assert all(x>0 for x in p);piv.extend(p)
 alpha=1-2*a;BB=4*b;c=2*alpha-BB
 assert [Q(info[x]) for x in ['alpha','B','omitted_cutoff']]==[alpha,BB,c]
 assert info['codimension']==13 and info['remaining_count']==6548 and info['omitted_reference_excitation']==2
 bins=Counter({0:1})
 for _ in range(4):
  nxt=Counter()
  for e,n in bins.items():
   for ee,nn in [(0,1),(1,3),(3,5)]:nxt[e+ee]+=n*nn
  bins=nxt
 assert info['complete_reference_bins']==[[e,n] for e,n in sorted(bins.items())]
 rows=[info['ground_Schur']]+info['triplet_modes'];spec=[(Q(0),Q(16,3),1),(Q(-4,3),Q(6),3),(Q(0),Q(32,9),6),(Q(4,3),Q(14,3),3)]
 lows=[];proof=[]
 for j,(row,(v,r2,mult)) in enumerate(zip(rows,spec)):
  theta=(0 if j==0 else 1)+g*v;var=g*g*r2;disc=(theta-c)**2+4*var;rt=Q(row['root_upper']);lo=Q(row['eigenvalue_lower'])
  assert Q(row['theta'])==theta and Q(row['full_residual_squared'])==var and Q(row['complement_cutoff'])==c
  assert rt*rt>=disc and (rt-Q(1,10**30))**2<disc
  assert lo==floor((theta+c-rt)/2,24) and lo<c and (theta-lo)*(c-lo)>=var
  assert Q(row['Schur_slack'])==(theta-lo)*(c-lo)-var
  if j:
   assert row['multiplicity']==mult and Q(row['V_expectation'])==v and Q(row['residual_unit_squared'])==r2
   assert theta*c>var and lo>0
  else:assert lo<0
  lows.extend([lo]*mult);proof.append(dict(theta=str(theta),variance=str(var),lower=str(lo),multiplicity=mult,quadratic_slack=str((theta-lo)*(c-lo)-var)))
 assert lows==sorted(lows) and len(lows)==13 and all(x<c for x in lows)
 groundlo=Q(s['ground_lower'])+8
 assert lows[0]<groundlo<lows[1] and Q(s['exact_rayleigh'])==Q(s['ground_upper'])
 return dict(full_reference_count=sum(bins.values()),remaining_reference_count=6548,strict_local_LDL_pivots=list(map(str,piv)),complement_cutoff=str(c),comparison_channels=proof,ground_replacement_lower=str(groundlo),physical_low_band_separation_not_assumed=True)

def main():
 st=time.monotonic();provenance=snapshot()
 sys.path.insert(0,str(HERE.parent/'chain_frontier_review'));import independent_core as C
 block=load(HERE/'block_premises.json');assert block['status']=='EXACT_BLOCK_PREMISES_VERIFIED'
 momcheck=verify_moments(load(SNAP/'unit_moments.json'))
 mat=load(PRIOR/'chain_snapshot/M8_two_trial_moments.json')
 # This Gram/strong/weak matrix is part of the sealed earlier independent physical replay.
 prior=load(PRIOR/'results/chain_first_moments.json');assert prior['8']['exact_Gram_strong_and_weak_moments_verified']
 summary=[]
 for path in sorted(SNAP.glob('candidate_g*.json')):
  rec=load(path);g=Q(rec['g']);inp=rec['input'];s=inp['small'];assert Q(inp['g'])==g
  patch=verify_patch(s,g)
  C.DATA=ROOT/inp['small_folder'];trial=C.DATA/s['trial_artifact'];INPUT[str(trial.relative_to(ROOT))]=sha(trial)
  ground=C.check_ground(s)
  rho8=expectation(mat,list(map(Q,inp['large']['combination_integers'])),g)
  assert rho8==Q(inp['large']['exact_rayleigh']) and inp['large']['trial_support']==43294 and inp['large']['full_dimension']==9**8
  paths=[]
  for row in rec['rows']:
   result=scalar(rec,row);bridge=row['all_size_bridge'];beta=Q(row['beta']);J=Q(row['J_lower']);S=floor(root(J));T=J
   initial=window(bridge['initial_M4_M8_window'],S,T,J,4,beta)
   short=[];lc=s['low_band']['local_comparison'];a,b=Q(lc['a']),Q(lc['b'])
   assert len(bridge['M2_M3'])==2
   for M,r in zip([2,3],bridge['M2_M3']):
    gap=1-2*a-M*b
    assert r['M']==M and r['full_dimension']==9**M and r['physical_sites']==2*M and r['trial']=='singlet product'
    assert list(map(Q,[r['rayleigh_upper'],r['second_eigenvalue_lower'],r['gap_lower']]))==[-2*M,-2*M+gap,gap]
    short.append(gap)
   target=min(Q(result['M_ge8_gap_lower']),Q(initial['gap_lower']),*short)
   assert target==Q(bridge['all_M_ge2_gap_lower'])==Q(row['all_M_ge2_gap_lower'])
   result.update(initial_M4_M8_window=initial,M2_M3_gaps=list(map(str,short)),all_M_ge2_gap_lower=str(target));paths.append(result)
  best=max(rec['rows'],key=lambda r:Q(r['all_M_ge2_gap_lower']));assert best==rec['best'];bestidx=rec['rows'].index(best)
  out=dict(g=str(g),gap_lower=best['all_M_ge2_gap_lower'],scope='All integer M>=2; unique finite-volume ground state',patch=patch,ground=ground,large_rayleigh=str(rho8),candidate_paths=len(paths),window_checks=sum(len(r['windows'])+1 for r in paths),selected_path=paths[bestidx],all_paths=paths)
  save('review_g'+str(g).replace('/','d')+'.json',out);summary.append({k:out[k] for k in ['g','gap_lower','scope','candidate_paths','window_checks']});print('PASS',g,best['all_M_ge2_gap_lower'],len(paths),flush=True)
 report=dict(status='PASS_INDEPENDENT_COUNTED_BAND_AND_ALL_SIZE_REVIEW',results=summary,moment_review=momcheck,provenance=provenance,seconds=time.monotonic()-st,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0)))
 save('SUMMARY.json',report);save('INPUT_SHA256SUMS.json',INPUT);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
