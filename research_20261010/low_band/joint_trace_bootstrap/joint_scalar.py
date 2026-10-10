"""Exact joint-aware scalar bounds. New lemma awaiting independent review."""
from fractions import Fraction as F
from pathlib import Path
import sys,math
sys.dont_write_bytecode=True
BAND=Path(__file__).resolve().parents[1];RES=BAND.parent
sys.path.insert(0,str(RES/'root_review'))
from finite_window_2d import sqrt_lower,gap


def down(x,digits=48):
    x=F(x);d=10**digits
    return F(x.numerator*d//x.denominator,d)


def G(x):return 1-(1-x)**2/(2*x*x)


def full_product(abc):return abc[0]**4*abc[1]**2*abc[2]


def canonical_advance(abc,joint,exact=True,digits=80):
    rnd=(lambda x:down(x,digits)) if exact else (lambda x:x)
    a,b,c=abc
    arguments=[];values=[]
    z=max(full_product(abc),joint);arguments.append(z)
    d=rnd(G(z));values.append(d)
    if d<=0:return None,arguments
    z=max(b**4*c**2,joint**2)*d;arguments.append(z)
    e=rnd(G(z));values.append(e)
    if e<=0:return None,arguments
    z=max(c,joint)**4*d*d*e;arguments.append(z)
    f=rnd(G(z));values.append(f)
    if f<=0:return None,arguments
    return values,arguments


def plain_advance(abc,exact=True,digits=80):
    rnd=(lambda x:down(x,digits)) if exact else (lambda x:x)
    out=list(abc)
    for _ in range(3):
        val=rnd(G(full_product(out)))
        if val<=0:return None
        out=out[1:]+[val]
    return out


def interpolate_1d_joint(s,t,joint=F(0)):
    s,t,joint=map(F,(s,t,joint))
    assert 0<s<=1 and 0<t<=1 and 0<=joint<=1
    p=max(s*s*t,joint)
    if p<=F(1,2):return F(0),{'failed':'joint inverse purity <=1/2','p':str(p)}
    w=(1+sqrt_lower(2*p-1))/2;r=(1-w)/w;d=t/(1+r*r)
    result=down((1-r)*min(s*sqrt_lower(d),d),40)
    return result,dict(joint_lower=str(joint),p=str(p),dominant_weight_lower=str(w),tail_ratio_upper=str(r),d_lower=str(d))


def interpolate_2d_joint(a,b,c,joint):
    a,b,c,joint=map(F,(a,b,c,joint))
    assert all(0<x<=1 for x in (a,b,c)) and 0<=joint<=1
    if b<=F(1,2):return F(0),{'failed':'B<=1/2'}
    root=sqrt_lower(2*b-1)
    sx=max(a*a*root,sqrt_lower(joint)*root/b)
    ty,inner=interpolate_1d_joint(b,c,joint)
    if ty<=0:return F(0),dict(failed='transverse thermal',inner=inner)
    value,outer=interpolate_1d_joint(sx,ty)
    return value,dict(joint_lower=str(joint),spatial_lower=str(sx),transverse_thermal_lower=str(ty),inner=inner,outer=outer)
