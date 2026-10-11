#!/usr/bin/env python3
"""Bounded guide consistency replay, not a fresh independent physical audit.

Only this directory receives an output file. No imported producer code,
heat columns, MPS contractions, optimizer, network, or external publication.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from decimal import Decimal, localcontext
from datetime import datetime, timezone
import hashlib,json,math,resource,time,sys

resource.setrlimit(resource.RLIMIT_CPU,(60,60))
resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
sys.set_int_max_str_digits(100000)
START=time.process_time()
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
D=json.loads((P/'EXACT_DATA.json').read_text())
PIN=json.loads((P/'SOURCE_PINS.json').read_text())
B=10**160
checks=[]
def done(name):checks.append(name)
def down(x):return F(x.numerator*B//x.denominator,B)
def up(x):return -down(-x)
@lru_cache(None)
def exp_bounds(x):
    x=F(x)
    if x<0:
        l,u=exp_bounds(-x)
        return down(1/u),up(1/l)
    k=0
    while x>F(1,8):x/=2;k+=1
    term=total=F(1)
    for j in range(1,111):term*=x/j;total+=term
    # First omitted term, followed by a uniform ratio upper bound.
    upper=total+(term*x/111)/(1-x/112)
    lo,hi=down(total),up(upper)
    for _ in range(k):lo,hi=down(lo*lo),up(hi*hi)
    return lo,hi
@lru_cache(None)
def power(x,r):
    x,r=F(x),F(r)
    assert x>=0 and r>0
    p,q=r.numerator,r.denominator
    y=x**p
    target=y.numerator*B**q//y.denominator
    if q==1:k=target
    elif q==2:k=math.isqrt(target)
    else:
        lo,hi=0,1<<((target.bit_length()+q-1)//q)
        while hi-lo>1:
            m=(lo+hi)//2
            if m**q<=target:lo=m
            else:hi=m
        k=lo
    l,u=F(k,B),F(k+1,B)
    assert l**q<=y<=u**q
    return l,u
@lru_cache(None)
def pack(m,h,r):
    assert m>=0 and h>0 and r>=1
    q=m//h
    return up(q*power(h,r)[1]+power(m-q*h,r)[1])
def G(z):
    assert 0<z<=1
    return 1-(1-z)**2/(2*z*z)
def floor_grid(x,d):return F(x.numerator*d//x.denominator,d)
def ceil_grid(x,d):return -floor_grid(-x,d)
def bernstein_nonnegative(poly,a,b):
    degree=len(poly)-1
    ordinary=[sum(poly[j]*math.comb(j,k)*a**(j-k)*(b-a)**k for j in range(k,degree+1)) for k in range(degree+1)]
    row=[sum(ordinary[k]*F(math.comb(i,k),math.comb(degree,k)) for k in range(i+1)) for i in range(degree+1)]
    pending=[(row,0)];leaves=maxdepth=0
    while pending:
        row,depth=pending.pop()
        if min(row)>=0:
            leaves+=1;maxdepth=max(maxdepth,depth);continue
        assert depth<30 and row[0]>=0 and row[-1]>=0
        tri=[row]
        while len(tri[-1])>1:tri.append([(u+v)/2 for u,v in zip(tri[-1],tri[-1][1:])])
        pending.append(([v[0] for v in tri],depth+1))
        pending.append(([v[-1] for v in tri[::-1]],depth+1))
    return leaves,maxdepth

def readjson(rel):return json.loads((ROOT/'research_20261010'/rel).read_text())
# Identity of every source read in creating this guide.
for rel,h in PIN['consumed_file_sha256'].items():
    assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
for folder,h in {**PIN['accepted_review_manifests'],**PIN['producer_manifests']}.items():
    p=ROOT/'research_20261010'/folder
    b=(p/'MANIFEST_SHA256.json').read_bytes()
    assert hashlib.sha256(b).hexdigest()==h
    for name,filehash in json.loads(b).items():
        assert hashlib.sha256((p/name).read_bytes()).hexdigest()==filehash,(folder,name)
for source in PIN['original_sources']:
    b=(ROOT/source['local_path']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==source['git_blob_sha1']
    assert hashlib.sha256(b).hexdigest()==source['sha256']
done('66 consumed-source identities, 15 complete package manifests and 6 original Git blobs')
# The exact-data excerpt must agree with its pinned origins.
assert D['physical_inputs']==readjson('uniform_second_thermal_full_review/provenance_results.json')['cases']
for field in ['moment_intervals','filters']:
    assert D[field]==readjson('uniform_second_moment_optimization/certificate.json')[field]
assert D['bootstrap_rows']==readjson('uniform_smaller_second_initialization/certificate.json')['rows']
assert D['direct_4_to23']==readjson('uniform_small_lengths_completion/certificate.json')['rows']
assert D['direct_26_to33']==readjson('uniform_gap_0248_all_sizes/certificate.json')['new_rows']
assert D['direct25']==readjson('uniform_direct25_coverage/certificate.json')
assert D['long_majorants']=={**readjson('uniform_smaller_second_initialization/long_certificate.json'),**readjson('uniform_small_lengths_completion/long_certificate.json')}
for a,b in [('accepted_stronger_prefix_4_to25','cached_prefix_4_to25'),('accepted_stronger_26_to33','new_direct26_to33')]:
    assert D[a]==readjson('uniform_gap_0248_all_sizes_review/results.json')[b]
done('exact-data extraction matches pinned producer/reviewer fields')

A=F(700741,500000);beta=F(49,4);delta=F(31,1250)
assert D['theorem']['gap']=='31/1250' and D['theorem']['all_integer_L_at_least']==2 and D['theorem']['unique_ground_state']
assert D['theorem']['bootstrap_initialization_used_for_this_stronger_gap']==34
assert D['theorem']['smallest_separately_certified_initialization']==30 and F(D['theorem']['smaller_initialization_gap'])==F(179,10000)
assert D['theorem']['prior_direct25_resource_anomaly_still_unresolved']
assert beta*delta==F(1519,5000)
assert D['model']['physical_dimension']=='3^L' and D['model']['MPS_bond_dimension']==26 and D['model']['MPS_norm_transfer_dimension']==26**2 and D['model']['trial_span_dimension']==1 and D['model']['L2_bond_multiplicity']==2
assert sum(v+1 for v in D['MPS_tensor_definition']['virtual_types_ell'])==26
done('exact model, dimensions, gap, initialization and historical-exception labels')

# Recompute physical enclosure conversion from W. This does NOT recompute W.
trace={}
for c in D['physical_inputs']:
    label=c['case'];n=int(label[1:].split('_')[0]);W=int(c['W'])
    r=math.isqrt(W);assert r*r<=W<(r+1)**2
    d=math.isqrt(3**n)+1;E=d*(281*(d+1)+1)
    x=beta*n*(F(3,2)-A);assert 0<x<15
    term=total=F(1)
    for k in range(1,101):term*=x/k;total+=term
    low=total*max(0,r-E)**2/2**110
    high=(total+term)*(r+1+E)**2/2**110
    interval=(floor_grid(low,10**18),ceil_grid(high,10**18))
    assert interval==tuple(map(F,c['refined_rounded_interval']))
    trace[label]=interval
M={s:[tuple(map(F,x)) for x in rows] for s,rows in D['moment_intervals'].items()}
for j,n in enumerate(range(4,13)):
    zl,zu=trace[f'L{n}_I'];pl,pu=trace[f'L{n}_P']
    assert M['J'][j]==((zl+3*pl)/4,(zu+3*pu)/4)
    assert M['N'][j]==((zl-pu)/4,(zu-pl)/4)
    if n%2:assert M['N'][j][1]<0
done('18 exact W-to-trace enclosures and all signed moment endpoints, including negative odd N')

# Independent short implementation of the guide's elementary filter test.
for name,v in D['filters'].items():
    q=list(map(F,v['q']));r=F(v['cap']);sign=1 if name[-1]=='+' else -1
    coeff=[sum(q[i]*q[j] for i in range(5) for j in range(5) if i+j==k) for k in range(9)]
    summed=sum(c*(u if c>=0 else l) for c,(l,u) in zip(coeff,M[name[0]]))
    assert summed==F(v['upper_filter_sum'])
    at=sum(q[i]*(sign*r)**i for i in range(5))
    assert r**4*at**2>summed
    shifted=[sum(q[j]*sign**j*math.comb(j,k)*r**(j-k) for j in range(k,5)) for k in range(5)]
    assert min(shifted)>0 and shifted==list(map(F,v['positive_shift_coefficients']))
done('four rational support filters exclude whole exterior rays with correct coefficient signs')

polynomial_count=0
for key,v in D['long_majorants'].items():
    s,k=key[0],int(key[1:]);q=list(map(F,v['coeff']))
    assert len(q)==9 and k>=13
    poly=q+[F(0)]*(k-3-len(q));poly[-1]-=1
    left=-F(D['filters'][s+'-']['cap']);right=F(D['filters'][s+'+']['cap'])
    leaves,depth=bernstein_nonnegative(poly,left,right)
    bound=sum(c*(u if c>=0 else l) for c,(l,u) in zip(q,M[s]))
    assert bound==F(v['bound'])
    assert (leaves,depth)==(v['bernstein_leaf_count'],v['bernstein_max_depth'])
    polynomial_count+=1
done('40 complete-domain rational Bernstein majorants and sign-directed moment sums')

mj,mn=M['J'][-1][1],M['N'][-1][1]
U=max(F(D['filters']['J+']['cap']),F(D['filters']['J-']['cap']))
V=max(F(D['filters']['N+']['cap']),F(D['filters']['N-']['cap']))
@lru_cache(None)
def sector(s,k):
    m,h=(mj,U**12) if s=='J' else (mn,V**12)
    value=pack(m,h,F(k,12))
    key=f'{s}{k}'
    if key in D['long_majorants']:value=min(value,F(D['long_majorants'][key]['bound']))
    return value

def full(k):return sector('J',k)+3*sector('N',k)

def anchor(anchors,n):
    norm=int(anchors[f'N0_{n}']);total=int(anchors[f'H0_{n}'])
    assert norm>0
    return F(total,norm)+n*A

def seed_check(n,ell,s,t,margin):
    force=1-pack(mj,ell**12,F(2*n,12))-3*sector('N',2*n)
    assert 0<margin<=force and ell>max(V,F(D['filters']['J-']['cap']))
    residual=mj-ell**12;assert 0<residual<ell**12
    tail=power(residual,F(n,12))[1]+3*sector('N',n)
    assert 0<s<=(1+tail/ell**n)**-2<=1
    assert 0<t<=full(2*n)**-2<=1

row=next(r for r in D['bootstrap_rows'] if r['n']==34)
ray=anchor(D['bootstrap_anchors'],68)
assert ray==F(row['shifted_Rayleigh'])<0
seed_check(34,F(row['ell']),F(row['S']),F(row['T']),F(row['forcing_margin']))
window_margins=[];previous=None
for j,(state,w) in enumerate(zip(row['states'],row['windows'])):
    n=34*2**j;b=beta*2**j;s,t=F(state['S']),F(state['T'])
    assert state['n']==n and F(state['beta'])==b and 0<s<=1 and 0<t<=1
    if previous is None:
        assert s==F(row['S']) and t==F(row['T'])
    else:
        assert s<=G(previous[0]**2*previous[1])
        assert t<=G(previous[1]**2*s)
    K=s*s*t;assert K>F(1,2)
    root=power(2*K-1,F(1,2))[0]
    rho=(1-root)/(1+root);d=t/(1+rho*rho)
    C=(1-rho)*min(s*power(d,F(1,2))[0],d)
    cc=F(w['purity'])
    assert F(1,2)<cc<=C and (w['from'],w['to'])==(n,2*n)
    margin=cc-exp_bounds(b*delta)[1]*(1-cc)
    assert 0<F(w['margin'])<=margin
    window_margins.append(margin);previous=(s,t)
assert len(row['states'])==len(row['windows'])==10
asym=row['asymptotic'];u=max(1-s,1-t)
assert n==17408 and b==6272 and asym['from']==n and F(asym['beta'])==b and F(asym['defect'])==u
assert 0<u<=F(1,100) and 0<F(asym['margin'])<=1-5*u*exp_bounds(b*delta)[1]
e=F(1,100)
assert 9/(2*(1-e)**6)<5
assert (2+5*e)**2/(2*(1-2*e-5*e*e)**2)<5
assert e<=F(4,49) and e<=F(1,63)
done('n34 physical integer quotient, dominant-atom seed, 10 staggered states/windows and infinite-closure scalar conditions')

# All cached finite endpoints, including their direct numerator and denominator.
purities={}
for r in D['direct_4_to23']:
    n=r['L'];ray=anchor(D['direct_4_to23_anchors'],n)
    assert ray==F(r['shifted_total_Rayleigh'])
    q=F(r['trace_upper'])
    if n<=12:assert q==trace[f'L{n}_I'][1]
    else:assert 0<full(n)<=q
    num=F(r['numerator_lower']);cc=F(r['purity_lower'])
    assert 0<num<=exp_bounds(-2*beta*ray)[0]
    assert F(1,2)<cc<=num/q**2<=1
    purities[n]=cc
n24=D['isolated24'];r=n24['seed'];s,t=F(r['S']),F(r['T'])
assert F(n24['anchor48_shifted_total_Rayleigh'])==F(r['anchor_shifted_Rayleigh'])<0
seed_check(24,F(r['ell']),s,t,F(r['forcing_margin']))
root=power(2*s*s*t-1,F(1,2))[0];rho=(1-root)/(1+root)
cc=F(n24['accepted']['purity_lower']);assert F(1,2)<cc<=s*power(t/(1+rho*rho),F(1,2))[0]
purities[24]=cc
r=D['direct25'];ray=anchor(D['direct25_anchors'],25)
assert ray==F(r['shifted_total_Rayleigh'])>0
assert 0<full(24)<=F(r['Q24']) and 0<full(26)<=F(r['Q26'])
den=F(r['Q24'])*F(r['Q26']);assert den==F(r['Z25_squared_upper'])
num=F(r['Z25_2beta_lower']);assert 0<num<=exp_bounds(-2*beta*ray)[0]<1
cc=F(r['purity_lower']);assert F(1,2)<cc<=num/den<=1;purities[25]=cc
for r in D['direct_26_to33']:
    n=r['L'];ray=anchor(D['direct_26_to33_anchors'],n)
    assert ray==F(r['shifted_total_Rayleigh'])
    required=[n-1,n+1] if n%2 else [n]
    assert set(r['trace_inputs'])==set(map(str,required))
    q={k:F(r['trace_inputs'][str(k)]) for k in required}
    assert all(0<full(k)<=v for k,v in q.items())
    den=q[n-1]*q[n+1] if n%2 else q[n]**2
    assert den==F(r['trace_squared_upper'])
    num=F(r['numerator_lower']);cc=F(r['purity_lower'])
    assert 0<num<=exp_bounds(-2*beta*ray)[0]
    assert F(1,2)<cc<=num/den<=1;purities[n]=cc
assert set(purities)==set(range(4,34))
stronger=D['accepted_stronger_prefix_4_to25']+D['accepted_stronger_26_to33']
assert {r['L'] for r in stronger}==set(range(4,34))
for r in stronger:
    cc=purities[r['L']];assert cc==F(r['purity_lower'])
    margin=cc-exp_bounds(beta*delta)[1]*(1-cc)
    assert 0<F(r['strict_gap_margin'])<=margin
# Angular momentum multiplicities independently from finite tensor-product rules.
multiplicity={1:1}
for count in [2,3]:
    new={}
    for j,m in multiplicity.items():
        for k in range(abs(j-1),j+2):new[k]=new.get(k,0)+m
    multiplicity=new
    assert sum((2*j+1)*m for j,m in new.items())==3**count
    energies={j:(F(j*(j+1))-4 if count==2 else F(j*(j+1)-6,2)) for j in new}
    ordered=sorted(energies.items(),key=lambda v:v[1])
    assert ordered[0][0]==0 and new[0]==1
    gap=ordered[1][1]-ordered[0][1]
    assert gap==F(D['analytic2_3'][str(count)]['gap'])>delta
assert set(range(2,4))|set(purities)==set(range(2,34))
done('own-length finite numerator signs, even/odd denominators, isolated24, all30 stronger-gap checks and analytic2/3 coverage')

# Ratio comparison using exact atanh-series logarithm enclosures.
def log_bounds(x):
    assert x>1
    z=(x-1)/(x+1);terms=120
    s=2*sum(z**(2*k+1)/(2*k+1) for k in range(terms))
    err=2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
    return s,s+err
la,ua=log_bounds(F(80,79));l2,u2=log_bounds(F(2));l5,u5=log_bounds(F(5,4))
lb,ub=4*l2+l5,4*u2+u5
old1=(F(4,105)*la,F(4,105)*ua);old2=(lb/784,ub/784)
ratios=[(delta/old1[1],delta/old1[0]),(delta/old2[1],delta/old2[0])]
assert F(51753817602864,10**12)<ratios[0][0]<=ratios[0][1]<F(51753817602865,10**12)
assert F(6490299607759,10**12)<ratios[1][0]<=ratios[1][1]<F(6490299607760,10**12)
with localcontext() as c:
    c.prec=30
    decimal=lambda x:str(Decimal(x.numerator)/Decimal(x.denominator))
    displays=[decimal(sum(r)/2) for r in ratios]
done('original lower-bound formulas and exact rational enclosures for both comparison ratios')
result={
 'status':'PASS_GUIDE_CONSISTENCY_CHECK_NOT_INDEPENDENT_PHYSICAL_REVIEW',
 'checked_utc':datetime.now(timezone.utc).isoformat(),
 'checks':checks,
 'full_domain_majorants_checked':polynomial_count,
 'finite_purities_checked':len(purities),
 'strong_tail_n':34,'strong_tail_gap':'31/1250','all_integer_L_at_least':2,
 'minimum_n34_window_margin_display':str(float(min(window_margins))),
 'comparison_ratio_enclosures':[[str(x) for x in pair] for pair in ratios],
 'comparison_ratio_displays':displays,
 'physical_work_performed':False,
 'independent_review_of_this_guide':'PENDING',
 'resource_observation_within_declared_limits':time.process_time()-START<60 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<256*1024,
 'prior_attempt':'history/SELF_CHECK_ATTEMPT1.json retains mathematical PASS with measured CPU 30.21035921 exceeding the declared 30-second limit. Cause not diagnosed. Current replay uses a 60-second limit and a rigorous shorter Taylor sum.',
 'resources':{'CPU_seconds':time.process_time()-START,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'CPU_limit_seconds':60,'address_space_limit_MiB':256}
}
(P/'SELF_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','full_domain_majorants_checked','finite_purities_checked','comparison_ratio_displays','resources']},indent=2))
