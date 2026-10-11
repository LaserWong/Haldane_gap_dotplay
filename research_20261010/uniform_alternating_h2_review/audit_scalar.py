#!/usr/bin/env python3
"""Independent exact variance, Rayleigh weight, pairwise fidelity and effect check."""
import ctypes,hashlib,json,math,os,resource,signal,time
from fractions import Fraction as F
from pathlib import Path
assert resource.getrlimit(resource.RLIMIT_CPU)==(3,3) and resource.getrlimit(resource.RLIMIT_AS)==(256*1024**2,)*2
assert os.sched_getaffinity(0)=={5} and signal.getsignal(signal.SIGXCPU)==signal.SIG_DFL and signal.SIGXCPU not in signal.pthread_sigmask(signal.SIG_BLOCK,set())
death=ctypes.c_int();assert ctypes.CDLL(None).prctl(2,ctypes.byref(death),0,0,0)==0 and death.value==signal.SIGKILL
P=Path(__file__).resolve().parent;R=P.parents[1];GRID=1<<512;ARG=1<<192;start=time.process_time();pins={}
def read(path):
 raw=path.read_bytes();pins[str(path.relative_to(R))]=hashlib.sha256(raw).hexdigest();return json.loads(raw)
def down(x):return F(x.numerator*GRID//x.denominator,GRID)
def up(x):return -down(-x)
def root(x):
 assert x>=0;k=math.isqrt(x.numerator*GRID*GRID//x.denominator);a,b=F(k,GRID),F(k+1,GRID);assert a*a<=x<=b*b;return a,b
def exp_at(x):
 if x<0:
  a,b=exp_at(-x);return down(1/b),up(1/a)
 n=0
 while x>F(1,4):x/=2;n+=1
 tl=th=sl=sh=F(1)
 for k in range(1,121):
  tl=down(tl*x/k);th=up(th*x/k);sl+=tl;sh+=th
 lo=sl;hi=up(sh+(th*x/121)/(1-x/122))
 for _ in range(n):lo=down(lo*lo);hi=up(hi*hi)
 return lo,hi
def exponential(x):
 k=x.numerator*ARG//x.denominator;lo,hi=F(k,ARG),F(k+1,ARG);assert lo<=x<=hi
 return exp_at(lo)[0],exp_at(hi)[1]
def integers(path,L):
 raw=path.read_bytes();pins[str(path.relative_to(R))]=hashlib.sha256(raw).hexdigest()
 names={f'N0_{L}',f'H0_{L}',f'H2_{L}','VARIANCE_NUMERATOR','VARIANCE_DENOMINATOR'}
 return {k:int(v) for line in raw.decode().splitlines() if '=' in line for k,v in [line.split('=',1)] if k in names}
config=read(P/'PRODUCER_PINS.json');rows=[]
for L in (64,32):
 prod=R/config[str(L)]['path'];saved=read(prod/'scalar_result.json');v=integers(P/f'review{L}.out',L);assert v==integers(prod/'pilot.out',L)
 N,H,H2=(v[f'{name}_{L}'] for name in ('N0','H0','H2'));assert N>0
 variance=F(H2*N-H*H,N*N);assert variance>=0 and v['VARIANCE_NUMERATOR']==H2*N-H*H and v['VARIANCE_DENOMINATOR']==N*N and variance==F(saved['variance'])
 if L==64:
  source=next(x for x in read(R/'research_20261010/uniform_smaller_second_initialization/certificate.json')['rows'] if x['n']==32)
  Q=F(source['Q']);mu_source=F(source['shifted_Rayleigh']);anchors=R/'research_20261010/uniform_smaller_second_initialization_review/anchors.out';b2name='independent_scalar_result.json'
 else:
  source=next(x for x in read(R/'research_20261010/uniform_gap_0248_all_sizes/certificate.json')['new_rows'] if x['L']==32)
  Q=F(source['trace_inputs']['32']);mu_source=F(source['shifted_total_Rayleigh']);anchors=R/'research_20261010/uniform_gap_0248_all_sizes_review/anchors.out';b2name='independent_scalar32_result.json'
 anc=integers(anchors,L);assert anc[f'N0_{L}']==N and anc[f'H0_{L}']==H
 q=F(read(R/'research_20261010/uniform_alternating_b2_fixture_review'/b2name)['q_exact']);assert q==F(saved['normalized_trial_B2'])
 beta=F(49,4);mu=F(H,N)+L*F(700741,500000);assert mu==mu_source==F(saved['shifted_trial_mu']) and Q==F(saved['trace_upper'])
 # The new weight uses the variational numerator, separately from purity.
 w=down(exponential(-beta*mu)[0]/Q);assert F(1,2)<w<1 and F(saved['ground_weight_Rayleigh_lower'])<=w
 Elo=F(saved['ground_shifted_energy_lower']);delta=F(saved['finite_gap_lower'])
 if L==64:assert Elo==F(-702409,100000000) and delta==F(19681,100000)
 else:assert Elo==F(-627681,100000000) and delta==F(1783,8000)
 energy_margin=exponential(-beta*Elo)[0]-Q;gap_margin=w-exponential(beta*delta)[1]*(1-w);assert energy_margin>0 and gap_margin>0
 eps0=(mu-Elo)/delta;assert 0<eps0<F(1,2)
 # Ground/excited pairs in the exact spectral variance give F(1-F)delta².
 discriminant=1-4*variance/(delta*delta);assert discriminant>=0
 epsvar=(1-root(discriminant)[0])/2;eps=min(eps0,epsvar);f=1-eps;assert f>F(1,2) and f>q
 saved_eps=F(saved['variance_pairwise_infidelity'])
 assert eps0==F(saved['energy_only_infidelity']) and 0<=saved_eps<=F(1,2) and saved_eps*(1-saved_eps)>=variance/(delta*delta)
 threshold=delta*delta*eps0*(1-eps0);assert threshold==F(saved['variance_helpful_threshold']) and variance<threshold
 alpha=up(f*q+(1-f)*(1-q)+2*root(f*q*(1-f)*(1-q))[1]);assert 0<=alpha<1
 kappa=up(1-w+w*alpha);simple=F(saved['simple_Gibbs_kappa_upper']);assert kappa<simple<1
 assert abs(kappa-F(saved['Gibbs_kappa_upper']))<F(1,10**35)
 rows.append({'physical_length':L,'status':'ACCEPTED','variance_exact':str(variance),'variance_display':float(variance),'Q':str(Q),'shifted_mu':str(mu),'Rayleigh_ground_weight_lower':str(w),'E0_shifted_lower':str(Elo),'finite_gap_lower':str(delta),'energy_margin':str(energy_margin),'finite_gap_margin':str(gap_margin),'energy_only_infidelity_upper':str(eps0),'pairwise_variance_infidelity_upper':str(epsvar),'fidelity_lower':str(f),'normalized_trial_B2':str(q),'ground_B2_effect_upper':str(alpha),'Gibbs_kappa_upper':str(kappa),'simple_Gibbs_kappa_upper':str(simple),'Gibbs_kappa_display':float(kappa),'old_accepted_gap_bounds_unchanged':True})
result={'status':'INDEPENDENT_EXACT_H2_FIDELITY_AND_GIBBS_EFFECT_ACCEPTED','rows':rows,'no_interval_claim':True,'exponential_argument_grid_bits':192,'arithmetic_grid_bits':512,'CPU_seconds':time.process_time()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'scalar_results.json').write_text(json.dumps(result,indent=2)+'\n');(P/'SCALAR_INPUT_SHA256.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'rows':[{k:r[k] for k in ('physical_length','variance_display','simple_Gibbs_kappa_upper','Gibbs_kappa_display')} for r in rows],'CPU_seconds':result['CPU_seconds']},indent=2))
