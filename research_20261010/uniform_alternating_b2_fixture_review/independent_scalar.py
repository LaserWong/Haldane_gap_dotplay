#!/usr/bin/env python3
"""Exact rational scalar cross-check, with a single-root effect inequality."""
import ctypes,json,math,os,resource,signal,time
from fractions import Fraction as F
from pathlib import Path
assert resource.getrlimit(resource.RLIMIT_CPU)==(2,2)
assert resource.getrlimit(resource.RLIMIT_AS)==(256*1024**2,)*2
assert os.sched_getaffinity(0)=={5}
assert signal.getsignal(signal.SIGXCPU)==signal.SIG_DFL
assert signal.SIGXCPU not in signal.pthread_sigmask(signal.SIG_BLOCK,set())
death=ctypes.c_int();assert ctypes.CDLL(None).prctl(2,ctypes.byref(death),0,0,0)==0 and death.value==signal.SIGKILL
P=Path(__file__).resolve().parent;R=P.parents[1];pilot=R/'research_20261010/uniform_alternating_b2_64_pilot'
def values(path):
    return {k:int(v) for line in path.read_text().splitlines() if '=' in line for k,v in [line.split('=',1)] if k in ('N0_64','H0_64','B2_64')}
fresh=values(P/'review64.out');prod=values(pilot/'pilot.out');anchors=values(R/'research_20261010/uniform_smaller_second_initialization_review/anchors.out')
assert fresh==prod and all(fresh[k]==v for k,v in anchors.items())
seed=next(v for v in json.loads((R/'research_20261010/uniform_smaller_second_initialization/certificate.json').read_text())['rows'] if v['n']==32)
Q=F(seed['Q']);C=F(seed['T']);b=F(49,4);q=F(fresh['B2_64'],9216*fresh['N0_64']);mu=F(fresh['H0_64'],fresh['N0_64'])+64*F(700741,500000)
assert mu==F(seed['shifted_Rayleigh'])
grid=10**80
def root(x):
    assert x>=0
    k=math.isqrt(x.numerator*grid*grid//x.denominator)
    lo,hi=F(k,grid),F(k+1,grid)
    assert lo*lo<=x<=hi*hi
    return lo,hi
def exp_positive(x):
    assert 0<=x<3
    term=total=F(1)
    for n in range(1,81):term=term*x/n;total+=term
    tail=term*x/81/(1-x/82)
    return total,total+tail
w=(1+root(2*C-1)[0])/2
E=F(-71,10000);gap=F(19,100)
energy_margin=exp_positive(-b*E)[0]-Q
gap_margin=w-exp_positive(b*gap)[1]*(1-w)
assert energy_margin>0 and gap_margin>0
f=1-(mu-E)/gap
assert 0<=q<f<=1
alpha=f*q+(1-f)*(1-q)+2*root(f*q*(1-f)*(1-q))[1]
kappa=1-w+w*alpha
assert kappa<F(157,1000)
producer=json.loads((pilot/'scalar_result.json').read_text())
assert q==F(producer['normalized_trial_B2']) and f==F(producer['fidelity_lower'])
assert abs(kappa-F(producer['gibbs_kappa_upper']))<F(1,10**75)
result={'status':'INDEPENDENT_EXACT_L64_SCALAR_PASS','full_integer_production_match':True,'accepted_anchor_match':True,'q_exact':str(q),'q_display':float(q),'beta':'49/4','E0_shifted_lower':str(E),'gap_lower':str(gap),'fidelity_lower':str(f),'ground_weight_lower':str(w),'ground_effect_upper':str(alpha),'gibbs_kappa_upper':str(kappa),'simple_kappa_upper':'157/1000','kappa_display':float(kappa),'positive_energy_margin':str(energy_margin),'positive_gap_margin':str(gap_margin),'trial_span_dimension':1,'MPS_bond_dimension':26,'physical_Hilbert_dimension':'3^64','CPU_seconds':time.process_time()}
(P/'independent_scalar_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k in ('status','q_display','kappa_display','simple_kappa_upper','CPU_seconds')},indent=2))
