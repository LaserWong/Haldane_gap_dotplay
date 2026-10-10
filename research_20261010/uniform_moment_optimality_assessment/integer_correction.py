#!/usr/bin/env python3
"""A uniform, small but strict integer-count correction for trivial L26."""
from pathlib import Path
from fractions import Fraction as F
import json,os,resource,time
os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600));start=time.process_time()
import sympy as sp
P=Path(__file__).resolve().parent;rr=json.load(open(P/'results.json'))['sectors']['trivial'];h=F(rr['support_cap']['exact']);t=F(rr['radau_node']['exact']);dd=json.load(open(P.parent/'uniform_transfer_moment_assessment/results.json'))['hankel_caps']['trivial']['moment_intervals'];m={int(j):[F(v['exact']) for v in iv] for j,iv in dd.items()};k=10
cc=(h**k-t**k-k*t**(k-1)*(h-t))/(h-t)**2;bb=k*t**(k-1)-2*cc*t;aa=t**k-k*t**k+cc*t*t
x=sp.Symbol('x');Q=sp.Rational(aa.numerator,aa.denominator)+sp.Rational(bb.numerator,bb.denominator)*x+sp.Rational(cc.numerator,cc.denominator)*x*x
ss=lambda v:sp.Rational(v.numerator,v.denominator)
quotient,remainder=sp.div(Q-x**k,(x-ss(t))**2*(ss(h)-x),domain=sp.QQ)
assert remainder==0
coeff=[F(v.p,v.q) for v in sp.Poly(quotient,x).all_coeffs()];assert all(v>=0 for v in coeff) and coeff[-1]>=h**7
et=eh=F(1,100000)
assert 0<t-et<t+et<h-eh<h and t+et<3*h/4
variance_lower=m[5][0]-2*t*m[4][1]+t*t*m[3][0];assert variance_lower>0
dH=eh*h**7*variance_lower
N=(m[3][1]-(h-eh)**3)//(t-et)**3;assert N==53
gmax=(t+et)**3*(h-t-et)/(t**3*(h-t))
effective_lower=(h*m[3][0]-m[4][1])/(t**3*(h-t))
K=1/(t**3*(h-t)*et*et*h**7)
deficit=effective_lower-N*gmax;assert deficit>0
dT=deficit/K;delta=min(dH,dT);assert delta>F(149,10**16)
upper=sum(c*m[j][1 if c>=0 else 0] for c,j in zip((aa,bb,cc),(3,4,5)))
row=lambda v:{'exact':str(v),'display':float(v)}
out={'status':'PASS strict integer-multiplicity improvement, trivial sector L26, all archived sector intervals','Hermite_upper':row(upper),'safe_improved_upper':row(upper-delta),'minimum_Hermite_slack':row(delta),'simple_slack_lower':'149/10000000000000000','epsilon_t':str(et),'epsilon_h':str(eh),'near_t_integer_count_upper':int(N),'variance_lower':row(variance_lower),'large_gap_threshold':row(dH),'effective_tail_count_lower':row(effective_lower),'g_max_near_t':row(gmax),'outside_ratio_K':row(K),'count_deficit':row(deficit),'polynomial_quotient_coefficients':[str(v) for v in coeff],'cpu_seconds':time.process_time()-start}
(P/'integer_correction.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='polynomial_quotient_coefficients'},indent=2))
