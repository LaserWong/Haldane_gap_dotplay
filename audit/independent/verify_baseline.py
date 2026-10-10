"""Independent rational and representation-theory audit; no eigensolver or archive imports."""
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import json, hashlib, sys, time
BASE=Path(__file__).resolve().parents[2]
ORIG=BASE/'original/Haldane_extensions'
OUT=BASE/'audit/independent'

def exp_interval(x, N=300):
    x=Q(x)
    if x<0:
        a,b=exp_interval(-x,N)
        return 1/b,1/a
    assert 0<=x<N+2
    terms=[Q(1)]
    for k in range(1,N+1): terms.append(terms[-1]*x/k)
    a=sum(terms)
    remainder=terms[-1]*x/(N+1)/(1-x/(N+2))
    return a,a+remainder

def ceiling(x):
    return Q(-((-x.numerator*10**12)//x.denominator),10**12)
def floor(x):
    return Q(x.numerator*10**12//x.denominator,10**12)
def f(u):
    assert 0<=u<1
    return u*u/(2*(1-u)**2)

def main():
    expected=ORIG/'SHA256SUMS.txt'
    checks=[]
    for line in expected.read_text().splitlines():
        sha,path=line.split(maxsplit=1)
        data=(ORIG/path).read_bytes()
        actual=hashlib.sha256(data).hexdigest()
        assert sha==actual,path
        checks.append({'path':path,'sha256':actual,'bytes':len(data)})
    (OUT/'checksum_verification.json').write_text(json.dumps(checks,indent=2))
    # Three exactly coupled angular momenta on the four-site cycle.
    # A=S1+S3, B=S2+S4; H=A.B. Each pair irrep a,b occurs once.
    levels=Counter()
    for a in range(5):
        for b in range(5):
            for j in range(abs(a-b),a+b+1):
                E=Q(j*(j+1)-a*(a+1)-b*(b+1),2)
                assert E.denominator==1
                levels[int(E)]+=2*j+1
    assert sum(levels.values())==625
    moment_ref=json.loads((ORIG/'results/integer_heat_trace_moments.json').read_text())
    moments=[sum(deg*(32-2*E)**k for E,deg in levels.items()) for k in range(201)]
    assert moments==list(map(int,moment_ref['moments']))
    cuts=[Q(-41,2),Q(-39,2),Q(-37,2),Q(-33,2),Q(-31,2)]
    counts=[sum(m for E,m in levels.items() if E<c) for c in cuts]
    assert counts==[0,1,4,9,9]
    # Independently enclose actual heat trace via exact Casimir spectrum.
    thermal=[]
    for beta in (1,2):
        el,eu=exp_interval(20*beta)
        terms=[(m,exp_interval(-beta*(E+20))) for E,m in levels.items()]
        qlo=sum(m*ab[0] for m,ab in terms)
        qhi=sum(m*ab[1] for m,ab in terms)
        zl,zu=el*qlo,eu*qhi
        stored=[r for r in json.loads((ORIG/'results/exact_heat_trace_certificate.json').read_text()) if r['beta']==str(beta)][0]
        sl,su=Q(stored['Z_lower']),Q(stored['Z_upper'])
        # The independent enclosure is much tighter at beta=2; verify overlap always.
        assert max(zl,sl)<=min(zu,su)
        thermal.append({'beta':beta,'Z_display':float(zl),'independent_enclosure_overlaps_packaged':True,'independent_interval_contained':sl<=zl<=zu<=su})
    # Universal seed: independent exponential series at fixed 300 degree.
    q6=exp_interval(-6)[1]; q18=exp_interval(-18)[1]
    zupper=1+3*q6+5*q18/(1-Q(7,5)*q18)
    assert zupper<Q(1007437,1000000)
    S=floor(exp_interval(-Q(81,2500))[0]); T=floor(exp_interval(-Q(81,625))[0]/Q(1007437,1000000)**8)
    p,q=1-S,1-T
    updates=[]
    n=2; beta=6
    while max(p,q)>Q(1,100):
        p=ceiling(f(1-(1-p)**2*(1-q)))
        q=ceiling(f(1-(1-q)**2*(1-p)))
        n*=2; beta*=2
        updates.append({'p_upper':str(p),'q_upper':str(q)})
        assert len(updates)<=10
    packed=json.loads((ORIG/'results/analytic_dimer_certificates.json').read_text())['universal']
    assert str(S)==packed['S_lower'] and str(T)==packed['T_lower']
    assert all(a['p_upper']==b['p_upper'] and a['q_upper']==b['q_upper'] for a,b in zip(updates,packed['bootstrap']['updates']))
    assert len(updates)==packed['bootstrap']['rounds']==4 and n==32 and beta==96
    u=max(p,q); gap=Q('0.055688426272')
    # Prove gap <= -log(5u)/beta without invoking an implementation of log.
    assert exp_interval(beta*gap)[1] < 1/(5*u)
    uu=Q(1,100)
    constants={
      'spatial_quadratic':9/(2*(1-3*uu)**2)<5,
      'thermal_quadratic':(2+5*uu)**2/(2*(1-(2+5*uu)*uu)**2)<5,
      'integer_interpolation':Q(3,2)+5*uu+2/(1-2*uu)<4,
      'gap_conversion':4/(1-4*uu)<5,
      'short_chain_Weyl':1-31*Q(3,100)>gap}
    assert all(constants.values())
    summary={'checksums_checked':len(checks),'casimir_dimension':sum(levels.values()),'integer_moments_0_through_200_match':True,'exact_levels':sorted(levels.items()),'inertia_counts_match_Casimir':counts,'heat_traces':thermal,'seed':{'S':str(S),'T':str(T),'updates':updates,'final_n_cells':n,'final_beta':beta,'final_u':str(u),'gap_lower':str(gap),'independent_exp_check_of_log_gap':True},'constants':constants,'status':'PASS; hand-derived physical/transfer hypotheses still needed'}
    (OUT/'baseline_verification.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
