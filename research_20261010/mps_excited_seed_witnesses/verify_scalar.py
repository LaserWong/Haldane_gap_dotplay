#!/usr/bin/env python3
"""Directed-rational all-beta recipe exclusions or explicitly bounded screens."""
import os,resource,time,json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
P=Path(__file__).resolve().parent;t0=time.process_time();B=1<<160;PARAM=1<<64
def down(x): return F(x.numerator*B//x.denominator,B)
def up(x): return F(-(-x.numerator*B//x.denominator),B)
def exp_i(x):
    x=F(x)
    if x<0:
        l,u=exp_i(-x);return down(1/u),up(1/l)
    k=0
    while x>F(1,16): x/=2;k+=1
    term=total=F(1)
    for j in range(1,41):term=term*x/j;total+=term
    nxt=term*x/41;l=down(total);u=up(total+nxt/(1-x/42))
    for _ in range(k):l=down(l*l);u=up(u*u)
    return l,u
def G(x):
    assert 0<x<=1
    return 1-(1-x)**2/(2*x*x)
def sqrt_up(x):
    v=F(isqrt(x.numerator*B*B//x.denominator)+1,B);assert v*v>x;return v
def canonical(a,b):
    s=up(a*sqrt_up(b));t=up(a*a*b);K=t;hist=[]
    for k in range(32):
        if min(s,t)>=F(99,100):return {'outcome':'inconclusive: optimistic upper orbit reaches target region','round':k,'history':hist}
        z=max(s*s*t,K);s=up(G(z))
        if s<=0:return {'outcome':'excluded','failure':'canonical spatial','round':k+1,'argument_upper':str(z),'output_upper':str(s),'history':hist}
        z=max(t,K)**2*s;t=up(G(z));K=F(0)
        if t<=0:return {'outcome':'excluded','failure':'canonical thermal','round':k+1,'argument_upper':str(z),'output_upper':str(t),'history':hist}
        hist.append({'round':k+1,'S_upper':str(s),'T_upper':str(t)})
    return {'outcome':'inconclusive: finite replay limit','round':32,'history':hist}
def recipe(j,c):
    a=up(G(j))
    if a<=0:return {'outcome':'excluded','failure':'initial first G','argument_upper':str(j),'output_upper':str(a)}
    z=c*c*a;b=up(G(z))
    if b<=0:return {'outcome':'excluded','failure':'initial second G','argument_upper':str(z),'output_upper':str(b)}
    trials=[]
    for delay in range(32):
        if min(a,b)>=F(99,100):return {'outcome':'inconclusive: optimistic time-first upper orbit reaches target','conversions':trials}
        converted=canonical(a,b)
        trials.append({'time_first_delay':delay,'a_upper':str(a),'b_upper':str(b),'canonical':converted})
        if converted['outcome']!='excluded':return {'outcome':'inconclusive: canonical upper envelope survives','conversions':trials}
        z=a*a*b;a=up(G(z))
        if a<=0:return {'outcome':'excluded','failure':'continued time-first first G','argument_upper':str(z),'output_upper':str(a),'conversions':trials}
        z=b*b*a;b=up(G(z))
        if b<=0:return {'outcome':'excluded','failure':'continued time-first second G','argument_upper':str(z),'output_upper':str(b),'conversions':trials}
    return {'outcome':'inconclusive: finite time-first replay limit','conversions':trials}
def merge_boxes(boxes):
    out=[]
    for box in boxes:
        lo,hi=box['beta_lower'],box['beta_upper']
        if out and out[-1]['beta_upper']==lo:out[-1]['beta_upper']=hi
        else:out.append({'beta_lower':lo,'beta_upper':hi})
    return out
rows=[]
for r in json.loads((P/'exact_witness_data.json').read_text())['rows']:
    n=r['n'];delta=F(r['delta']);gap=F(r['trial_energy_difference']);R=F(r['R_2n'])
    d=F(delta.numerator*PARAM//delta.denominator,PARAM)
    g=F(-(-gap.numerator*PARAM//gap.denominator),PARAM)
    Rlo=F(R.numerator*PARAM//R.denominator,PARAM)
    assert 0<d<=delta and g>=gap>0 and Rlo<=R<0
    hot=up(exp_i(-Rlo)[1]/3**(4*n));assert hot<F(2,5) and G(F(2,5))<0
    cold=10
    while exp_i(-2*cold*d)[1]>=F(2,5):cold*=2
    cold_bound=exp_i(-2*cold*d)[1]
    boxes=[]
    for i in range(2,4*cold):
        lo,hi=F(i,4),F(i+1,4)
        num=exp_i(-2*lo*d)[1]
        j=up(num/(1+2*exp_i(-hi*g)[0])**4)
        c=up(num/(1+2*exp_i(-2*hi*g)[0])**2)
        result=recipe(j,c)
        boxes.append({'beta_lower':str(lo),'beta_upper':str(hi),'J_upper':str(j),'C_upper':str(c),'J_upper_display':float(j),'C_upper_display':float(c),'replay':result})
    unresolved=[b for b in boxes if b['replay']['outcome']!='excluded']
    counts={}
    for b in boxes:
        label=b['replay'].get('failure',b['replay']['outcome']);counts[label]=counts.get(label,0)+1
    cap=max(hot,cold_bound,max(F(b['J_upper']) for b in boxes))
    out={'n':n,'status':'PASS all-beta recipe-specific exclusion' if not unresolved else 'BOUNDED necessary-condition screen; no all-beta exclusion','delta_lower':str(d),'trial_energy_difference_upper':str(g),'R_lower':str(Rlo),'hot_closed_interval':['0','1/2'],'hot_J_upper':str(hot),'cold_closed_interval':[str(cold),'infinity'],'cold_J_upper':str(cold_bound),'exact_global_J_upper':str(cap),'global_J_upper_display':float(cap),'warm_box_width':'1/4','warm_box_count':len(boxes),'failure_counts':counts,'inconclusive_closed_box_unions':merge_boxes(unresolved),'warm_boxes':boxes}
    rows.append(out)
    print(n,out['status'],'global J cap',float(cap),'inconclusive',out['inconclusive_closed_box_unions'],flush=True)
result={'status':'Producer directed-rational results; independent review pending','scope':'Uniform periodic spin1 H=sum S_j dot S_(j+1), fixed exact archived D26 one-Rayleigh numerator at length 2n; denominator trial-trace lower bound from psi_n and two spin-flip-related staggered raised witnesses; specified thermal-first G initialization and any fixed whole-cycle time-first delay followed by the accepted joint-aware canonical conversion. n24 unresolved boxes are not feasibility or physical-spectrum claims.','rows':rows,'cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'scalar_results.json').write_text(json.dumps(result,indent=2)+'\n')
print('CPU seconds',result['cpu_seconds'],'peak KiB',result['peak_kb'])
