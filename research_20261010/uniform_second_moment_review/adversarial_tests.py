#!/usr/bin/env python3
"""Negative fixtures for the independent checker; no producer execution."""
import copy,json,time
from fractions import Fraction as F
import audit as a
st=time.process_time();c=a.js(a.A/'certificate.json');lc=a.js(a.A/'long_certificate.json');ct=a.js(a.A/'continuation_certificate.json')
M={s:[tuple(map(F,x)) for x in rows] for s,rows in c['moment_intervals'].items()};results={}
def reject(name,f):
 try:f()
 except (AssertionError,ValueError,ZeroDivisionError):results[name]='REJECTED';return
 raise AssertionError('Fixture was accepted: '+name)
def capmut(name,mut):
 x=copy.deepcopy(c['filters']['N-']);mut(x);reject(name,lambda:a.check_cap(x,'N',-1,M))
capmut('smaller unsupported negative cap',lambda x:x.__setitem__('cap','4/5'))
capmut('false exterior margin',lambda x:x.__setitem__('exterior_margin','1'))
capmut('corrupted filter coefficient',lambda x:x['q'].__setitem__(0,str(F(x['q'][0])+1)))
capmut('nonpositive shifted coefficient',lambda x:x['positive_shift_coefficients'].__setitem__(0,'0'))
capmut('nonexclusion outside support cap',lambda x:x.__setitem__('midpoint_square_method_nonexclusion_at','-1'))
wrong=copy.deepcopy(M)
for j in [1,3,5,7]:wrong['N'][j]=tuple(sorted(abs(t) for t in wrong['N'][j]))
reject('replace signed odd moments with absolute values',lambda:a.check_cap(c['filters']['N-'],'N',-1,wrong))
wrong=copy.deepcopy(M);wrong['N'][1]=(M['N'][1][1],M['N'][1][0])
reject('reverse adverse odd interval direction',lambda:a.check_cap(c['filters']['N-'],'N',-1,wrong))
# Positive endpoints alone cannot certify a majorant: x^2-1/4 is negative at zero.
reject('endpoint-only interior positivity',lambda:a.bernstein_positive([F(-1,4),F(0),F(1)],F(-1),F(1)))
reject('omitted zero condition',lambda:a.bernstein_positive([F(-1,1000)],F(-1),F(1)))
# The Bernstein checker accepts exact positive examples that may need subdivision.
assert a.bernstein_positive([F(1,100),F(0),F(1)],F(-1),F(1))
assert a.bernstein_positive([F(0)]*9,F(-1),F(1))==(1,0)
results['zero and nonnegative fixture polynomials']='PASS'
S0=F(ct['seed']['S']);T0=F(ct['seed']['T72'])
def mutate(name,mut):
 x=copy.deepcopy(ct);mut(x);reject(name,lambda:a.check_continuation(x,S0,T0))
mutate('missing integer window',lambda x:x['all_integer_windows'].pop(3))
mutate('gap in finite windows',lambda x:x['all_integer_windows'][1].__setitem__('from',73))
mutate('wrong window inverse temperature',lambda x:x['all_integer_windows'][2].__setitem__('beta','98'))
mutate('wrong spatial base coordinate',lambda x:x['states'][1].__setitem__('n',144))
mutate('thermal coordinate silently unstaggered',lambda x:x['seed'].__setitem__('T72',str(S0)))
mutate('inflated recurrence purity',lambda x:x['states'][1].__setitem__('S','1'))
mutate('inflated finite window purity',lambda x:x['all_integer_windows'][0].__setitem__('purity_lower','1'))
mutate('inflated target gap',lambda x:x['conditional_conclusion'].__setitem__('gap','1/10'))
mutate('premature asymptotic onset',lambda x:x['asymptotic'].__setitem__('from',18432))
mutate('false terminal common defect',lambda x:x['asymptotic'].__setitem__('defect','0'))
# Multiplicity and unit atom safeguards, with exact witnesses.
ell=F(c['dominant']['ell']);mj=M['J'][-1][1];n36=F(lc['N36']['bound'])
wrongS=(1+((mj-ell**12)**3+n36)/ell**36)**-2
assert wrongS>S0
results['omitting N multiplicity 3 changes seed optimistically']='PASS'
# Weighted measures do not justify unit-atom exclusion. A mass 1/2 at t=2
# contributes m4=8, but subtracting a whole atom produces first pivot -8.
reject('fractional mass treated as a full spectral occurrence',lambda:a.positive_definite([[F(-8)]]))
# A negative leading eigenvalue gives high even purity, but negative odd traces.
assert (F(10)**4+1)/(F(10)**2+1)**2>F(1,2) and (-10)**5+1<0
results['negative leading sign requires positive odd physical traces']='PASS'
# Signed interval linear bounds: exhaustive corners verify endpoint directions.
count=0
for s in 'JN':
 q=list(map(F,c['filters'][s+'-']['q']));co=a.square(q);B=a.dot_upper(co,M[s])
 for mask in range(512):
  value=sum(co[j]*M[s][j][(mask>>j)&1] for j in range(9));assert value<=B;count+=1
results['all signed moment box corners']=count
out={'status':'PASS','fixtures':results,'rejected_mutations':sum(v=='REJECTED' for v in results.values()),'cpu_seconds':time.process_time()-st}
(a.P/'adversarial_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
