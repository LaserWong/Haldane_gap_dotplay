#!/usr/bin/env python3
"""Independent decimal fixed-point enclosures and complete half-line coverage."""
import os,resource,time,json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
P=Path(__file__).resolve().parent;SRC=P.parent/'uniform_seed_size_diagnostics';start=time.time();S=10**40;Q=10**26

def floor(x,scale=S):return F(x.numerator*scale//x.denominator,scale)
def ceil(x,scale=S):return F(-((-x.numerator*scale)//x.denominator),scale)
def exp_bounds(x):
    x=F(x)
    if x<0:
        l,u=exp_bounds(-x);return floor(1/u),ceil(1/l)
    k=0
    while x>1:x/=2;k+=1
    xl,xu=floor(x),ceil(x);lo=hi=tl=tu=F(1)
    for j in range(1,97):
        tl=floor(tl*xl/j);tu=ceil(tu*xu/j);lo+=tl;hi+=tu
    remainder=tu*xu/97/(1-xu/98)
    lo=floor(lo);hi=ceil(hi+remainder)
    for _ in range(k):lo=floor(lo*lo);hi=ceil(hi*hi)
    assert lo>0 and lo<=hi
    return lo,hi

def G(x):
    assert 0<x<=1
    return (x*x+2*x-1)/(2*x*x)
def cup(x):return ceil(x,Q)
def root_upper(x):
    v=F(isqrt(x.numerator*S*S//x.denominator)+1,S);assert v*v>x;return v

def canonical(a,b):
    s=cup(a*root_upper(b));t=cup(a*a*b);K=t
    log=[{'stage':'conversion','S_upper':str(s),'T_upper':str(t),'K_upper':str(K)}]
    for k in range(1,100):
        assert 0<s<=1 and 0<t<=1 and 0<=K<=1
        assert min(s,t)<F(99,100), 'Small-defect trigger must not be reached'
        old=s*s*t;z=max(old,K);s=cup(G(z))
        log.append({'round':k,'step':'space','joint_used':bool(K>old),'argument_upper':str(z),'output_upper':str(s)})
        if s<=0:return log
        z=max(t,K)**2*s;t=cup(G(z));K=F(0)
        log.append({'round':k,'step':'time','argument_upper':str(z),'output_upper':str(t)})
        if t<=0:return log
    raise AssertionError('No finite failure established')

# Regressions for enclosure and ratio directions. e^0=1, reciprocal enclosures,
# shift cancellation, Jensen orthonormal sum and a physical-ratio counterexample.
assert exp_bounds(0)[0]<=1<=exp_bounds(0)[1]
for x in [F(1,10),F(1),F(5),F(100)]:
    l,u=exp_bounds(x);a,b=exp_bounds(-x);assert l*b>=1 and u*a<=1
assert G(F(2,5))<0 and G(F(3,10))<0
# Rational thermal weights: small H=diag(0,0), large H=diag(0,1),
# beta=log(2), with the excited large-system trial R=1.
# At 2 beta the true numerator is 1+1/4, the trial numerator only 1/4.
# An upper bound on the chosen recipe is not an upper bound on the physical ratio.
small_trace=F(2);true_large_trace=F(5,4);trial_large_lower=F(1,4)
recipe_ratio=trial_large_lower/small_trace**4;physical_ratio=true_large_trace/small_trace**4
assert recipe_ratio==F(1,64) and physical_ratio==F(5,64) and recipe_ratio<physical_ratio
uv=dict(line.split('=') for line in (P/'d26_contractions.out').read_text().splitlines())
trials=json.loads((P/'independent_trials.json').read_text());prod={r['n']:r for r in json.loads((SRC/'uniform_seed_size_diagnostics.json').read_text())['rows']}
rows=[]
for row in trials['rows']:
    n=row['n'];A=[F(s['Rayleigh']) for s in row['states']];alpha=A[0]
    R=2*n*F(int(uv[f'U{2*n}']),int(uv[f'V{2*n}']));delta=R-2*alpha
    assert R<0 and delta>0 and str(R)==prod[n]['large_Rayleigh'] and str(delta)==prod[n]['delta']
    for shift in [F(-3,7),F(700741,500000),F(9)]:assert R+2*n*shift-2*(alpha+n*shift)==delta
    out={'n':n,'large_Rayleigh':str(R),'delta':str(delta),'delta_display':float(delta),'physical_small_dimension':3**n,'physical_large_dimension':3**(2*n),'MPS_bond_dimension':26,'retained_numerator_states':1}
    if n<10:
        split,cap=(F(3,4),F(29,50)) if n==6 else (F(31,40),F(71,100))
        hot=exp_bounds(-2*split*R)[1]/3**(4*n);cold=exp_bounds(-2*split*delta)[1]
        early=exp_bounds(-R)[1]/3**(4*n);late=exp_bounds(-delta)[1]
        assert max(hot,cold)<cap and early<F(2,5) and late<F(4,5)
        a=cup(G(cap));b=cup(G(F(16,25)*a));delays=[];time_log=[]
        delay=0
        while a>0 and b>0:
            assert min(a,b)<F(99,100)
            delays.append({'completed_time_first_cycles':delay,'base_length':2*n*2**delay,'base_beta_multiplier':2*2**delay,'a_upper':str(a),'b_upper':str(b),'canonical':canonical(a,b)})
            z=a*a*b;a=cup(G(z));time_log.append({'cycle':delay+1,'step':'time','argument_upper':str(z),'output_upper':str(a)})
            if a<=0:break
            z=b*b*a;b=cup(G(z));time_log.append({'cycle':delay+1,'step':'space','argument_upper':str(z),'output_upper':str(b)})
            if b<=0:break
            delay+=1;assert delay<100
        assert time_log and F(time_log[-1]['output_upper'])<=0
        expected=[d['time_first_delay'] for d in prod[n]['all_legal_delayed_conversions']]
        assert [d['completed_time_first_cycles'] for d in delays]==expected
        assert expected==([0] if n==6 else [0,1])
        out.update({'J_cap':str(cap),'beta_global_split':str(split),'global_hot_upper':str(hot),'global_cold_upper':str(cold),'early_beta_end':'1/2','early_upper':str(early),'late_C_upper':str(late),'delays':delays,'time_first_failure':time_log,'verdict':'PASS all allowable completed-cycle delays for the specified joint-aware conversion'})
    else:
        gaps=[x-alpha for x in A[1:]];assert len(gaps)==3 and min(gaps)>0
        cap=F(3,25) if n==10 else F(19,100);hot=exp_bounds(-R)[1]/3**(4*n);cold=exp_bounds(-20*delta)[1]
        assert max(hot,cold)<cap and G(cap)<0
        boxes=[]
        for i in range(2,40):
            l,u=F(i,4),F(i+1,4);den=1+sum(exp_bounds(-u*g)[0] for g in gaps)
            num=exp_bounds(-2*l*delta)[1];bound=ceil(num/den**4)
            den2=1+exp_bounds(-u*gaps[0])[0];bound2=ceil(num/den2**4)
            assert bound<cap and bound2<F(3,10)
            boxes.append({'lower':str(l),'upper':str(u),'four_state_upper':str(bound),'two_state_upper':str(bound2)})
        assert F(boxes[0]['lower'])==F(1,2) and F(boxes[-1]['upper'])==10
        assert all(boxes[i]['upper']==boxes[i+1]['lower'] for i in range(len(boxes)-1))
        assert max(hot,cold)<F(3,10)
        D=3**n;mu=-sum(A)/F(D-4);assert mu>0
        samples=[]
        for beta in [1,2,4,6,8,10]:
            lower=sum(exp_bounds(-beta*x)[0] for x in A)+(D-4)*exp_bounds(-beta*mu)[0]
            assert lower>D # independent complement Jensen genuinely improves simple dimension
            samples.append({'beta':beta,'trace_lower':str(lower)})
        out.update({'J_cap':str(cap),'G_at_cap':str(G(cap)),'hot_ray':[0,'1/2'],'hot_upper':str(hot),'cold_ray':[10,'infinity'],'cold_upper':str(cold),'closed_boxes':boxes,'max_box_upper':str(max(F(b['four_state_upper']) for b in boxes)),'max_box_upper_display':float(max(F(b['four_state_upper']) for b in boxes)),'two_state_cap':'3/10','two_state_max_box_display':float(max(F(b['two_state_upper']) for b in boxes)),'complement_mean':str(mu),'complement_samples':samples,'verdict':'PASS first G fails for all beta even with only two exact trial states'})
    rows.append(out)
    print('PASS all beta n',n,'delta',float(delta),'J cap',out['J_cap'],flush=True)
result={'status':'PASS independent exact arithmetic','arithmetic':'decimal scale 10^40 directed series; 96 Taylor terms on [0,1] with geometric tail; repeated squaring; decimal 10^26 upward recurrence rounding','regressions':['exponential positive and reciprocal enclosures','exact extensive-shift cancellation','closed-box endpoint and gap coverage','orthogonal complement trace identity','negative G targets','no small-defect entry before failure','all completed-cycle delay enumeration'], 'rows':rows,'seconds':time.time()-start,'cpu_seconds':time.process_time(),'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'independent_scalar.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='rows'})
