#!/usr/bin/env python3
"""Small falsification/regression tests of the acceptance gates, not new physics."""
import audit as A
from fractions import Fraction as F
import copy,time
rows=[]
def reject(name,fn):
    try:fn()
    except AssertionError:rows.append(dict(test=name,rejected=True));return
    raise AssertionError('Gate accepted corrupt case: '+name)

# Non-polynomial stored scaling is not silently mistaken for the physical family.
xs=list(map(F,['3/100','1/25','1/20','3/50','7/100','2/25','1/10']))
recs=[A.load(A.oldpath(4,4,x)) for x in xs]
raw=[F(r['G'][0][0]) for r in recs]
cs=A.fit(xs[:3],raw[:3]);assert any(A.value(cs,x)!=y for x,y in zip(xs[3:],raw[3:]))
rows.append(dict(test='unnormalized stored arrays fail degree-two model',rejected=True))
physical=[F(int(r['B'][0][0]),4*r['matrix_denominator']**4) for r in recs]
corrupt=physical[:];corrupt[-1]+=1
assert any(A.fit(xs,corrupt)[j] for j in [5,6])
rows.append(dict(test='one changed full second-moment checkpoint violates degree four',rejected=True))
# Finite interpolation alone can never prove degree. Explicit counter-polynomial.
point=F(17,200);extra=1
for x in xs:extra*=point-x
assert extra!=0
for x in xs:
 z=1
 for y in xs:z*=x-y
 assert z==0
rows.append(dict(test='seven-point match alone cannot prove degree; literal affine proof is necessary',passed=True))

b=A.load(A.newpath(4,4,F(17,200),'quadratic_bins'))
z=copy.deepcopy(b);z['bins'][2]['multiplicity']=A.math.comb(16,2)*3**2
reject('physical-shell counts substituted for oscillator counts',lambda:A.bins(z))
z=copy.deepcopy(b);z['bins'][2]['first_ordered_index']-=1
reject('incorrect first omitted ordered index',lambda:A.bins(z))
z=copy.deepcopy(b);z['delta_lower']=z['delta_upper']
reject('upward frequency endpoint used as lower bound',lambda:A.bins(z))

# The reconstructed full second moment genuinely contains q=6 leakage.
geo=A.load(A.S/'large_seed_moments/geometry_8x8.json');gr=A.load(A.newpath(8,8,F(17,200),'block1'))
G,H,B=A.E.matrix_at(8,8,F(17,200),geo,True)
z=copy.deepcopy(geo);z['W']=[[0 for x in row] for row in z['W']]
_,_,truncated=A.E.matrix_at(8,8,F(17,200),z,True)
ids=gr['selected_basis_indices'];c=[F(0)]*len(G)
for i,x in zip(ids,map(F,gr['coefficients'])):c[i]=x
loss=A.FM.bil(c,B-truncated)/A.FM.bil(c,G);assert loss>0
accepted=A.load(A.HERE/'results/physical_review.json')
assert loss==F(next(x['q6_residual_mass'] for x in accepted if x['g']=='17/200' and x['shape']==[8,8]))
rows.append(dict(test='omitted q6 leakage changes full variance',rejected=True,missing_mass=str(loss)))

# Verify base, temperature and complete earlier-window gates using in-memory copies.
original_load=A.load;target=A.S/'low_band/frontier_bracket/g17d200/extra_cycles_exact.json';base=original_load(target);short=A.shorts()
def with_mutation(mutator):
    rec=copy.deepcopy(base);mutator(rec)
    def altered(path):return rec if A.Path(path)==target else original_load(path)
    A.load=altered
    try:A.selected_deferred(short)
    finally:A.load=original_load
reject('cycle beta missing common doubling',lambda:with_mutation(lambda r:r['states'][1].__setitem__('beta','177/10')))
reject('transport assigned to wrong spatial base',lambda:with_mutation(lambda r:r['states'][3].__setitem__('n',32)))
reject('earlier finite window deleted',lambda:with_mutation(lambda r:r['states'].pop(2)))
reject('joint product replaced by different-base product',lambda:with_mutation(lambda r:r['states'][1].__setitem__('joint_lower',r['states'][0]['joint_lower'])))
reject('unapproved positive gap inflated',lambda:with_mutation(lambda r:r['candidates'][-1].__setitem__('asymptotic_gap','1')))
A.verify()
A.save('adversarial_review.json',dict(status='PASS',tests=rows,producer_data_mutated=False))
print('ADVERSARIAL PASS',len(rows),'cases',flush=True)
