#!/usr/bin/env python3
"""Exact complex off-diagonal fixtures and physical normalization rejection.
These test implementation only; literal operator algebra proves the identity.
"""
import audit as A
from audit import F,save,fit,poly,decompose,load,oldpath
from dataclasses import dataclass
@dataclass(frozen=True)
class C:
    re:F=F(0)
    im:F=F(0)
    def __post_init__(self):object.__setattr__(self,'re',F(self.re));object.__setattr__(self,'im',F(self.im))
    @staticmethod
    def cast(x):return x if isinstance(x,C) else C(x)
    def __add__(self,b):b=C.cast(b);return C(self.re+b.re,self.im+b.im)
    __radd__=__add__
    def __neg__(self):return C(-self.re,-self.im)
    def __sub__(self,b):return self+-C.cast(b)
    def __rsub__(self,b):return C.cast(b)+-self
    def __mul__(self,b):b=C.cast(b);return C(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
    __rmul__=__mul__
    def __truediv__(self,b):b=C.cast(b);d=b.re*b.re+b.im*b.im;return self*C(b.re/d,-b.im/d)
    def conj(self):return C(self.re,-self.im)
    def __bool__(self):return bool(self.re or self.im)
    def __eq__(self,b):b=C.cast(b);return self.re==b.re and self.im==b.im

def mv(M,v):return [sum((a*b for a,b in zip(row,v)),C()) for row in M]
def add(a,b):return [x+y for x,y in zip(a,b)]
def scale(a,v):return [a*x for x in v]
def dot(a,b):return sum((C.cast(x).conj()*y for x,y in zip(a,b)),C())
def fixture(seed):
    charges=[1,1,3,3,5];n=len(charges);Q=[[C(charges[i] if i==j else 0) for j in range(n)] for i in range(n)]
    V=[[C() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i,n):
            z=C(F(seed+3*i-j,7+i+j),F(seed+i+2*j,11+i+j) if i!=j else 0);V[i][j]=z;V[j][i]=z.conj()
    u=[C(seed,1),C(2,seed),C(),C(),C()];v=[C(),C(),C(F(seed,3),F(2,7)),C(-2,seed),C()]
    ur=[C(1,-seed),C(seed+1,1),C(),C(),C()];vr=[C(),C(),C(3,1),C(F(seed,11),-2),C()]
    def direct(z,p):
        left=add(u,scale(z,v));right=add(ur,scale(z,vr));hl=add(mv(Q,left),scale(p,mv(V,left)));hr=add(mv(Q,right),scale(p,mv(V,right)))
        return [dot(left,right),dot(left,hr),dot(hl,hr)]
    xs=list(map(F,[4,-2,0,3,1]));values=[direct(x,x) for x in xs]
    coeff=[]
    for i,degree in enumerate([2,3,4]):
        cs=fit(xs,[y[i] for y in values]);assert not any(cs[degree+1:]);coeff.append(cs[:degree+1])
    gg,aa,bb=coeff;vv,cc,dd=decompose(gg,aa,bb);checks=0;nonreal=0;distinct=0;leak=0
    for z,p in [(F(0),F(1,10)),(F(17,200),F(83,1000)),(F(-1,5),F(1,7)),(F(7,10),F(-2,3)),(F(3,10),F(0))]:
        got=[gg[0]+z*z*gg[2],gg[0]+3*z*z*gg[2]+p*poly(vv,z),gg[0]+9*z*z*gg[2]+p*poly(cc,z)+p*p*poly(dd,z)]
        actual=direct(z,p);assert got==actual;checks+=1;nonreal+=bool(actual[1].im or actual[2].im)
        left=add(u,scale(z,v));right=add(ur,scale(z,vr));term1=dot(mv(Q,left),mv(V,right));term2=dot(mv(V,left),mv(Q,right));assert term1+term2==poly(cc,z);distinct+=term1!=term2
        hr=add(mv(Q,right),scale(p,mv(V,right)));leak+=bool(hr[-1])
    assert nonreal and distinct and leak
    return dict(seed=seed,fixed_center_checks=checks,nonreal_cross_columns=nonreal,unequal_QV_VQ_terms=distinct,full_H2_leakage_fixtures=leak)

def main():
    fixtures=[fixture(k) for k in range(1,13)]
    normalization=[]
    for nx,ny in [(4,4),(8,4)]:
        xs=list(map(F,['3/100','1/25','1/20','3/50','7/100','2/25','1/10']));rs=[load(oldpath(nx,ny,g)) for g in xs]
        for key,power,degree in [('G',2,2),('A',3,3),('B',4,4)]:
            raw=[F(r[key][0][0]) for r in rs];wrong=[v/(4*r['matrix_denominator']**(power-1)) for v,r in zip(raw,rs)];correct=[v/(4*r['matrix_denominator']**power) for v,r in zip(raw,rs)]
            assert not any(fit(xs,correct)[degree+1:]);assert any(fit(xs,raw)[degree+1:]);assert any(fit(xs,wrong)[degree+1:])
            normalization.append(dict(geometry=[nx,ny],moment=key,raw_integer_fit_rejected=True,off_by_one_denominator_power_rejected=True,correct_physical_degree=True))
    # Finite-point matching cannot establish the degree: construct a vanishing
    # factor that preserves seven source evaluations but changes a new point.
    z=F(17,200);xs=list(map(F,['3/100','1/25','1/20','3/50','7/100','2/25','1/10']))
    def obstruction(y):
        out=F(1)
        for x in xs:out*=y-x
        return out
    assert all(obstruction(x)==0 for x in xs) and obstruction(z)!=0
    # Q(sqrt(2)) arithmetic exercises both directed sign branches and tiny gaps.
    qguards=[]
    for value in [(F(0),F(0)),(F(1),F(-1)),(F(-1),F(1)),(F(2),F(-1)),(F(-2),F(1)),(F(0),F(1)),(F(0),F(-1))]:
        lo,hi=A.bounds(value);assert lo<=hi and (A.sign(value)>=0 if lo>=0 else True) and (A.sign(value)<=0 if hi<=0 else True)
        qguards.append(dict(value=list(map(str,value)),bounds=list(map(str,(lo,hi))),exact_sign=A.sign(value)))
    save('bivariate_fixtures.json',dict(status='PASS',complex_cross_column_cases=sum(x['fixed_center_checks'] for x in fixtures),fixtures=fixtures,physical_normalization_guards=normalization,sample_only_degree_inference_rejected=True,quadratic_field_guards=qguards))
    print('PASS',sum(x['fixed_center_checks'] for x in fixtures),'exact complex Hermitian fixtures;',len(normalization)*2,'physical normalization rejection tests',flush=True)
if __name__=='__main__':main()
