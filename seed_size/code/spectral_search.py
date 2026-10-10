"""Certified size-temperature search from independently certified energy bins.

Every bin contains exactly `count` eigenvalues in [lo,hi]. All inputs are
rational strings. Ground must be unique and isolated from all other bins.
No residual, fitted energy, or floating eigenvalue becomes a proof here.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from certified_core import exp_bounds,down,up,replay
from exact_n2_exclusion import polynomials

class Spectrum:
    def __init__(self,record):
        if record.get('provenance_status')!='certified':
            raise ValueError('Spectrum provenance must independently establish exact counts/enclosures')
        self.record=record
        self.e0lo=Q(record['ground']['lo']);self.e0hi=Q(record['ground']['hi'])
        assert self.e0lo<=self.e0hi
        self.bins=[(0,0,1)]
        for b in record['excited_bins']:
            lo,hi=Q(b['lo'])-self.e0hi,Q(b['hi'])-self.e0lo
            assert 0<lo<=hi and b['count']>0
            self.bins.append((lo,hi,int(b['count'])))
        self.dimension=sum(c for l,h,c in self.bins)
        assert self.dimension==record['dimension']
    def trace(self,beta_lo,beta_hi=None):
        a=Q(beta_lo);b=a if beta_hi is None else Q(beta_hi)
        assert 0<=a<=b
        L=Q(0);U=Q(0)
        for lo,hi,c in self.bins:
            L+=c*exp_bounds(-b*hi)[0];U+=c*exp_bounds(-a*lo)[1]
        return down(L),up(U)
    def mean_gap(self,a,b):
        a,b=Q(a),Q(b);Nlo=Q(0);Nhi=Q(0)
        for lo,hi,c in self.bins:
            if hi==0:continue
            # Lower bound at beta=b, energy endpoint with smaller x exp(-b*x).
            lower=min(lo*exp_bounds(-b*lo)[0],hi*exp_bounds(-b*hi)[0])
            # Upper bound at beta=a; x exp(-a*x) has only the maximum x=1/a.
            pts=[lo,hi]
            if a and lo<=1/a<=hi:pts.append(1/a)
            upper=max(x*exp_bounds(-a*x)[1] for x in pts)
            Nlo+=c*lower;Nhi+=c*upper
        Zlo,Zhi=self.trace(a,b)
        return down(Nlo/Zhi),up(Nhi/Zlo)

class Pair:
    def __init__(self,small,large,n,m_input,unit='physical_sites'):
        self.n=n;self.m_input=m_input;self.unit=unit
        self.a=Spectrum(small);self.b=Spectrum(large)
        self.Clo=self.b.e0lo-2*self.a.e0hi
        self.Chi=self.b.e0hi-2*self.a.e0lo
        if self.Clo<0: self.Clo=Q(0) # Analytic transfer structure establishes C>=0.
    def purities(self,beta):
        beta=Q(beta);a=self.a.trace(beta);b=self.b.trace(beta);b2=self.b.trace(2*beta)
        Slo=down(exp_bounds(-beta*self.Chi)[0]*b[0]/a[1]**2)
        Shi=min(Q(1),up(exp_bounds(-beta*self.Clo)[1]*b[1]/a[0]**2))
        Tlo=down(b2[0]/b[1]**2);Thi=min(Q(1),up(b2[1]/b[0]**2))
        return (Slo,Shi),(Tlo,Thi)
    def W_bounds(self,a,b=None):
        a=Q(a);b=a if b is None else Q(b)
        small=self.a.trace(a,b);large=self.b.trace(2*a,2*b)
        return (down(exp_bounds(-2*b*self.Chi)[0]*large[0]/small[1]**4),
                up(exp_bounds(-2*a*self.Clo)[1]*large[1]/small[0]**4))
    def log_derivative(self,a,b):
        ma=self.a.mean_gap(a,b);mb=self.b.mean_gap(2*a,2*b)
        return down(-2*self.Chi-2*mb[1]+4*ma[0]),up(-2*self.Clo-2*mb[0]+4*ma[1])
    def exclude_all_beta(self,threshold=Q(1,2),max_depth=24):
        if self.Clo<=0:return {'excluded':False,'reason':'No positive ground-energy-defect lower bound'}
        B=Q(1)
        while self.b.dimension*exp_bounds(-2*B*self.Clo)[1]>=threshold:B*=2
        tail=up(self.b.dimension*exp_bounds(-2*B*self.Clo)[1])
        stack=[(Q(0),B,0)];leaves=[];unresolved=[]
        while stack:
            a,b,depth=stack.pop();U=self.W_bounds(a,b)[1];method='direct_interval'
            if U>=threshold:
                dl,du=self.log_derivative(a,b)
                Ua=self.W_bounds(a)[1];Ub=self.W_bounds(b)[1]
                Uleft=up(Ua*exp_bounds(max(Q(0),du)*(b-a))[1])
                Uright=up(Ub*exp_bounds(max(Q(0),-dl)*(b-a))[1])
                if min(Uleft,Uright)<U:U=min(Uleft,Uright);method='log_derivative_envelope'
            if U<threshold:
                leaves.append({'beta_lo':str(a),'beta_hi':str(b),'W_upper':str(U),'method':method})
            elif depth>=max_depth:
                unresolved.append([str(a),str(b)])
            else:
                m=(a+b)/2;stack.extend([(m,b,depth+1),(a,m,depth+1)])
        return {'excluded':not unresolved,'n_bootstrap':self.n,'m_input':self.m_input,
                'length_unit':self.unit,'threshold':str(threshold),'C_lower':str(self.Clo),
                'beta_tail_start':str(B),'tail_W_upper':str(tail),'finite_interval_leaves':leaves,
                'unresolved':unresolved,'scope':'Only the stated scalar recursion at this n; not all larger n from the same moment input'}
    def grid_search(self,betas):
        accepted=[]
        for beta in betas:
            beta=Q(beta);S,T=self.purities(beta);b=replay(S[0],T[0],self.n,beta)
            if b['accepted']:
                accepted.append({'beta':str(beta),'S':list(map(str,S)),'T':list(map(str,T)),
                                 'n_bootstrap':self.n,'m_input':self.m_input,'bootstrap':b})
        return {'accepted_seeds':accepted,'search_is_complete_exclusion':False}

def exact_n2_pair(t):
    # Spectrum Q2 uses x=e^-2beta; Q4 uses x=e^-beta here.
    num,den=polynomials(t)
    e02=-Q(t*(t+2),2);e04=-t*(t+1)
    small={'provenance_status':'certified','provenance':'Analytic two-spin total-J decomposition',
           'dimension':(t+1)**2,'ground':{'lo':str(e02),'hi':str(e02)},'excited_bins':[]}
    for j in range(1,t+1):
        e=e02+j*(j+1);small['excited_bins'].append({'lo':str(e),'hi':str(e),'count':2*j+1})
    large={'provenance_status':'certified','provenance':'H4=(S1+S3).(S2+S4); exact a,b,J decomposition',
           'dimension':(t+1)**4,'ground':{'lo':str(e04),'hi':str(e04)},'excited_bins':[]}
    for gap,c in enumerate(num[t:]):
        if gap and c:
            e=e04+gap;large['excited_bins'].append({'lo':str(e),'hi':str(e),'count':c})
    return Pair(small,large,2,4)

def main():
    out=[]
    for t in [2,4,6]:
        pair=exact_n2_pair(t);r=pair.exclude_all_beta();assert r['excluded']
        r['spin']=str(Q(t,2));out.append(r)
        print('spin',Q(t,2),'interval all-beta exclusion leaves',len(r['finite_interval_leaves']),flush=True)
    (Path(__file__).resolve().parents[1]/'results'/'interval_all_beta_validation.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
