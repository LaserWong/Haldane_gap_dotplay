"""Counted 13-state Schur lower tail for the M=4 chain denominator."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if hasattr(os,'sched_getaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,time,resource,importlib.util
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict,Counter
from functools import lru_cache
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];FROZEN=HERE.parent/'chain_filter_extension'
sys.path.insert(0,str(HERE.parent/'chain_frontier_review'));import independent_core as C
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));C.exp_bounds=lru_cache(maxsize=4096)(C.exp_bounds)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def loadmod(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def unit_moments():
 N=4;states=[(0,)*N]
 for label in [1,2,3]:
  for site in range(N):s=[0]*N;s[site]=label;states.append(tuple(s))
 weights=[math.prod(C.W[x] for x in s) for s in states];index={s:i for i,s in enumerate(states)};actions=[]
 for state in states:
  out=defaultdict(F)
  for right in range(N):
   left=(right-1)%N
   for a,b,v in C.K[state[left],state[right]]:
    s=list(state);s[left]=a;s[right]=b;out[tuple(s)]+=v
  actions.append({s:v for s,v in out.items() if v})
 K=[[weights[i]*actions[j].get(states[i],F(0)) for j in range(13)] for i in range(13)]
 J=[[sum((math.prod(C.W[x] for x in s)*v*actions[j].get(s,F(0)) for s,v in actions[i].items()),F(0)) for j in range(13)] for i in range(13)]
 R=[[J[i][j]-sum(K[i][k]*K[k][j]/weights[k] for k in range(13)) for j in range(13)] for i in range(13)]
 assert all(K[i][j]==K[j][i] and R[i][j]==R[j][i] for i in range(13) for j in range(13))
 assert all(K[i][j]==R[i][j]==0 for i in range(13) for j in range(13) if (i==0)!=(j==0) or (i and j and (i-1)//4!=(j-1)//4))
 blocks=[]
 for start in [1,5,9]:
  A=[[K[start+i][start+j]/weights[start] for j in range(4)] for i in range(4)]
  E=[[R[start+i][start+j]/weights[start] for j in range(4)] for i in range(4)]
  assert all(A[i][j]==A[0][(j-i)%4] and E[i][j]==E[0][(j-i)%4] for i in range(4) for j in range(4))
  blocks.append((A,E))
 assert blocks[0]==blocks[1]==blocks[2]
 ks,rs=blocks[0][0][0],blocks[0][1][0]
 modes=[]
 for k,mult,c in [(0,3,1),(1,6,0),(2,3,-1)]:
  sign=1 if k%2==0 else -1
  modes.append(dict(momentum_label=k,multiplicity=mult,V_expectation=str(ks[0]+2*c*ks[1]+sign*ks[2]),residual_unit_squared=str(rs[0]+2*c*rs[1]+sign*rs[2])))
 result=dict(N=4,physical_sites=8,full_dimension=9**4,retained_reference_dimension=13,trial_vectors=13,trial_union_support=13,applied_operator='H_4+8I; weak unit V has the same union support',full_shifted_H_applied_union_support=len(set().union(*[set(a) for a in actions])),full_unshifted_H_applied_union_support=len(set(states).union(*[set(a) for a in actions])),trial_plus_action_union_support=len(set(states).union(*[set(a) for a in actions])),full_residual_union_support=len(set().union(*[set(a) for a in actions])-set(states)),basis=[list(s) for s in states],Gram_diagonal=list(map(str,weights)),unit_K=[[str(x) for x in row] for row in K],unit_J=[[str(x) for x in row] for row in J],unit_residual_Gram=[[str(x) for x in row] for row in R],ground=dict(H0_excitation=0,V_expectation=str(K[0][0]/weights[0]),residual_unit_squared=str(R[0][0]/weights[0])),triplet_modes=modes)
 save('unit_moments.json',result);return result

def sqrtupper(x):
 scale=10**30;k=math.isqrt(x.numerator*scale*scale//x.denominator);r=F(k,scale)
 if r*r<x:r+=F(1,scale)
 assert r*r>=x and (r-F(1,scale))**2<x
 return r

def lower_root(theta,var,a):
 root=sqrtupper((theta-a)**2+4*var);lo=C.floor((theta+a-root)/2,24)
 assert lo<a and (theta-lo)*(a-lo)>=var
 return dict(theta=str(theta),full_residual_squared=str(var),complement_cutoff=str(a),root_upper=str(root),eigenvalue_lower=str(lo),Schur_slack=str((theta-lo)*(a-lo)-var))

def patch(rec,mom):
 g=F(rec['g']);local=dict(spin='1',coupling=str(g),a=str(g/2),b=str(g+F(1,10**12)),local_dimension=81,kind='single')
 check=C.local_psd(local);alpha=1-g;B=4*F(local['b']);a2=2*alpha-B
 ground=lower_root(g*F(mom['ground']['V_expectation']),g*g*F(mom['ground']['residual_unit_squared']),a2)
 trip=[]
 for m in mom['triplet_modes']:
  theta=1+g*F(m['V_expectation']);var=g*g*F(m['residual_unit_squared']);trip.append(dict(**m,**lower_root(theta,var,a2)))
 bins=Counter({0:1})
 for i in range(4):bins=Counter({e:sum(m*d for f,m in bins.items() for v,d in [(0,1),(1,3),(3,5)] if f+v==e) for e in range(3*(i+1)+1)})
 assert bins[0]==1 and bins[1]==12 and sum(bins.values())==9**4
 low=[F(ground['eigenvalue_lower'])]+[F(m['eigenvalue_lower']) for m in trip for _ in range(m['multiplicity'])]
 assert low==sorted(low) and len(low)==13 and all(x<a2 for x in low)
 assert F(rec['small']['ground_lower'])+8>low[0]
 info=dict(local_comparison=local,local_exact_PSD=check,alpha=str(alpha),B=str(B),omitted_reference_excitation=2,omitted_cutoff=str(a2),codimension=13,ground_Schur=ground,triplet_modes=trip,complete_reference_bins=[[e,m] for e,m in sorted(bins.items()) if m],remaining_count=sum(m for e,m in bins.items() if e>=2),counting_contract='Schur negative-inertia upper count. Does not require or assert 13 physical eigenvalues below omitted cutoff.')
 out=json.loads(json.dumps(rec));out['small']['low_band']=info
 save('patch_g'+rec['g'].replace('/','d')+'.json',out);return out

TRACE={}
def trace_exact(s,beta):
 beta=F(beta);info=s['low_band'];rho=F(s['exact_rayleigh']);lo=F(s['ground_lower']);alpha=F(info['alpha']);B=F(info['B'])
 terms=[C.exp_bounds(beta*(rho-lo))[1]]
 terms += [m['multiplicity']*C.exp_bounds(-beta*(-8+F(m['eigenvalue_lower'])-rho))[1] for m in info['triplet_modes']]
 terms += [mult*C.exp_bounds(-beta*(-8+alpha*e-B-rho))[1] for e,mult in info['complete_reference_bins'] if e>=2]
 bound=C.ceil(sum(terms),30)
 return bound,dict(low_triplet_upper=str(C.ceil(sum(terms[1:4]),30)),omitted_upper=str(C.ceil(sum(terms[4:]),30)))

def trace_float(s,beta):
 info=s['low_band'];rho=float(F(s['exact_rayleigh']));lo=float(F(s['ground_lower']));alpha=float(F(info['alpha']));B=float(F(info['B']))
 return math.exp(beta*(rho-lo))+sum(m['multiplicity']*math.exp(-beta*(-8+float(F(m['eigenvalue_lower']))-rho)) for m in info['triplet_modes'])+sum(mult*math.exp(-beta*(-8+alpha*e-B-rho)) for e,mult in info['complete_reference_bins'] if e>=2)

def main():
 start=time.monotonic();mom=unit_moments();inputs=json.loads((FROZEN/'inputs.json').read_text());patches=[patch(r,mom) for r in inputs if F(r['g']) in map(F,['9/50','37/200','19/100','39/200','1/5'])]
 save('inputs.json',patches)
 scan=loadmod('saved_scan',FROZEN/'scan_orders.py');scan.trace=trace_float
 rows=[]
 for p in patches:
  hits=[]
  for j in range(40,1601):
   beta=j/20;r=scan.run(p['small'],float(F(p['large']['exact_rayleigh'])),beta)
   if r:
    # Initial joint ratio gives the additional all-integer [4,8] window.
    delta=float(F(p['large']['exact_rayleigh'])-2*F(p['small']['exact_rayleigh']));J=math.exp(-2*beta*delta)/trace_float(p['small'],beta)**4
    gap=scan.interpolate(math.sqrt(J),J,beta,J)
    if gap>0:r['M4_M8_window_gap']=gap;r['all_M_ge4_gap']=min(gap,r['all_M_ge8_gap']);hits.append(r)
  best=max(hits,key=lambda x:x['all_M_ge4_gap']) if hits else None
  rows.append(dict(g=p['g'],passes=len(hits),best=best));print('FLOAT',rows[-1],flush=True)
 save('float_scan.json',rows)
 save('resources.json',dict(seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AS_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],cpu_affinity=sorted(os.sched_getaffinity(0))))
if __name__=='__main__':main()
