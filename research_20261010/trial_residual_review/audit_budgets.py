"""Independent signed-Taylor replay of entropy ranks and startup budgets.

Physical spectral intervals retain their separate independent-review scope.
No producer code is imported and no floating point is used in acceptance.
"""
from audit_residual import F, OUT, ROOT, read, serial, READ_HASHES, digest
from functools import lru_cache
import json, time, resource

SCALE=1<<256

def ceiling(n,d):
    return -((-n)//d)

@lru_cache(maxsize=5000)
def exponential(x):
    """Signed Taylor enclosure with a two-sided Lagrange remainder.

    Reduce |y| <= 1/16, sum through order 80, bound the remainder by
    2 |y|^81/81!, then square positive endpoints. This avoids the producer's
    positive-Taylor/reciprocal construction for negative inputs.
    """
    x=F(x)
    s=0
    y=x
    while abs(y)>F(1,16):
        y/=2
        s+=1
    tl=tu=sl=su=ab=SCALE
    for n in range(1,81):
        den=y.denominator*n
        if y>=0:
            tl,tu=tl*y.numerator//den,ceiling(tu*y.numerator,den)
        else:
            tl,tu=tu*y.numerator//den,ceiling(tl*y.numerator,den)
        ab=ceiling(ab*abs(y.numerator),den)
        sl+=tl
        su+=tu
    rem=2*ceiling(ab*abs(y.numerator),y.denominator*81)
    sl-=rem
    su+=rem
    assert 0<sl<=su
    for _ in range(s):
        sl=sl*sl//SCALE
        su=ceiling(su*su,SCALE)
    return F(sl,SCALE),F(su,SCALE)

def exp_sum(terms,beta):
    lower=upper=F(0)
    for energy,multiplicity in terms:
        a,b=exponential(-beta*energy)
        lower+=multiplicity*a
        upper+=multiplicity*b
    return lower,upper

def band_terms(rec):
    shift=F(rec['blocks'][0]['eigen_upper'][0])
    lows=[]
    highs=[]
    for block in rec['blocks']:
        mult=block['multiplicity']
        assert len(block['eigen_lower'])==len(block['eigen_upper'])
        for lo,hi in zip(block['eigen_lower'],block['eigen_upper']):
            assert F(lo)<=F(hi)
            lows.append((F(hi)-shift,mult))
            highs.append((F(lo)-shift,mult))
    tail=[(F(b['lower'])-shift,b['multiplicity']) for b in rec['number_sector_bins']['bins'][2:]]
    assert sum(m for _,m in lows)+sum(m for _,m in tail)==rec['full_hilbert_dimension']
    return lows,highs,tail

def load_bands(tag):
    base='research_20261010/low_band/'
    if tag!='3d100':
        base+='frontier/'
    return [read(base+f'bilayer_{shape}_g{tag}_symmetric_number_low_band.json') for shape in ('2x2','4x2','4x4')]

def G(x):
    assert x>0
    return 1-(1-x)**2/(2*x*x)

def audit_entropy():
    proposed=read('research_20261010/trial_size_criteria/entropy_rank.json')
    rows=[]
    beta=F(909,100)
    index=0
    for tag in ('3d100','1d25','1d20'):
        for rec in load_bands(tag):
            _,_,terms=band_terms(rec)
            lo,hi=exp_sum(terms,beta)
            shift=F(rec['blocks'][0]['eigen_upper'][0])
            a1=F(rec['number_sector_bins']['bins'][1]['lower'])
            wlo,whi=exponential(-beta*(a1-shift))
            n=rec['N']
            for tolerance in (F(1,10000),F(1,1000)):
                prop=proposed['results'][index]
                index+=1
                assert prop['g']==tag
                if lo>tolerance:
                    assert prop['status']=='inconclusive even after keeping q1'
                    rows.append(dict(g=tag,N=n,beta=beta,tolerance=tolerance,
                                     status='FAIL for this tail majorant even with all q1 kept',
                                     q_ge_2_tail=[lo,hi]))
                    continue
                assert hi<=tolerance
                allowed_low=max(0,min(3*n,int((tolerance-hi)//whi)))
                allowed_high=max(0,min(3*n,int((tolerance-lo)//wlo)))
                assert allowed_low==allowed_high
                r=allowed_low
                assert hi+r*whi<=tolerance
                if r<3*n:
                    assert lo+(r+1)*wlo>tolerance
                rank=1+3*n-r
                assert prop['maximum_omitted_q1_states']==r
                assert prop['minimum_retained_rank_for_test']==rank
                saved_lo,saved_hi=map(F,prop['q_ge_2_tail'])
                assert saved_lo<=lo<=hi<=saved_hi
                old_wlo,old_whi=map(F,prop['one_omitted_q1_weight'])
                assert old_wlo<=wlo<=whi<=old_whi
                rows.append(dict(g=tag,N=n,beta=beta,tolerance=tolerance,
                                 status='PASS exact specified-majorant minimum',
                                 maximum_omitted_q1_states=r,minimum_retained_rank=rank,
                                 q_ge_2_tail=[lo,hi],one_slot_weight=[wlo,whi]))
    assert index==len(proposed['results'])==18
    return rows

def audit_startup():
    recs=load_bands('3d100')
    examples=read('research_20261010/trial_size_criteria/examples.json')
    prop=examples['startup_budget']
    beta=F(prop['beta'])
    p=list(map(F,prop['target_first_state']))
    h=list(map(F,prop['inverse_G_upper']))
    assert all(0<x<=1 and G(x)>=goal for x,goal in zip(h,p))
    terms=[band_terms(rec) for rec in recs]
    L=[exp_sum(t[0],beta) for t in terms]
    U=[exp_sum(t[1]+t[2],beta)[1] for t in terms]
    N=exp_sum(terms[2][0],2*beta)[0]
    shifts=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
    star=[exponential(beta*(-2*shifts[2]+8*shifts[0]))[0]*N/L[0][1]**8,
          exponential(beta*(-4*shifts[2]+8*shifts[1]))[0]*N*N/L[1][1]**8,
          N/L[2][1]**2]
    factors=[U[i]/L[i][0] for i in range(3)]
    budgets=[star[0]/h[0],star[1]*p[0]/h[1],star[2]**4*p[0]**2*p[1]/h[2]]
    assert all(f**8<=budget for f,budget in zip(factors,budgets))
    old_star=list(map(F,prop['idealized_truncated_inputs_lower']))
    old_factor=list(map(F,prop['actual_trace_factor_upper']))
    assert all(old<=new for old,new in zip(old_star,star))
    assert all(new<=old for new,old in zip(factors,old_factor))
    old_budget=[old_star[0]/h[0],old_star[1]*p[0]/h[1],old_star[2]**4*p[0]**2*p[1]/h[2]]
    assert old_budget==list(map(F,prop['allowed_trace_factor_eighth_power']))
    assert all(f**8<=budget for f,budget in zip(old_factor,old_budget))
    state=p[:]
    history=[]
    for _ in range(100):
        if min(state)>=F(499,500):
            break
        value=G(state[0]**4*state[1]**2*state[2])
        value=F((value.numerator*SCALE)//value.denominator,SCALE)
        assert value>0
        state=state[1:]+[value]
        history.append(value)
    assert min(state)>=F(499,500)
    assert len(history)==prop['target_state_replay']['updates']==13
    return dict(status='PASS exact eighth-power startup inequalities',
                beta=beta,target=p,inverse_G_upper=h,truncated_input_lower=star,
                trace_factor_upper=factors,allowed_trace_factor_power8=budgets,
                recurrence_updates=len(history),final=state)

def main():
    started=time.monotonic()
    entropy=audit_entropy()
    startup=audit_startup()
    result=dict(status='PASS independent entropy-rank and startup-budget arithmetic',
                exponential_method='256-bit signed Taylor order 80 with two-sided Lagrange remainder and squaring',
                entropy_rank=entropy,startup=startup,input_sha256=READ_HASHES,
                seconds=time.monotonic()-started,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (OUT/'results/budget_review.json').write_text(json.dumps(serial(result),indent=2)+'\n')
    for rel,sha in READ_HASHES.items():
        assert digest((ROOT/rel).read_bytes())==sha
    print('PASS 18 entropy-rank tests, 3 startup budget inequalities and 13-step target replay',flush=True)
    print('seconds',result['seconds'],'peak RSS KiB',result['peak_rss_kib'],flush=True)
    for row in entropy:
        print(row['g'],row['N'],row['tolerance'],row.get('minimum_retained_rank'),row['status'])

if __name__=='__main__':
    main()
