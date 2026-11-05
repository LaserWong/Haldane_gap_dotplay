"""Exact integer/rational verification of finite synthetic candidate.
This does NOT upgrade estimated spin-2 inputs to a rigorous physical claim.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
c=json.loads(Path('candidate.json').read_text());D=10**180
A={s:[(F(x),int(w)) for x,w in aa]for s,aa in c['atoms'].items()}
assert all((x*D).denominator==1 for aa in A.values() for x,w in aa)
a={s:[(int(x*D),w) for x,w in aa] for s,aa in A.items()}
top=a['J'][0][0]
def mom(s,k):return sum(w*x**k for x,w in a[s])
def z(k):return mom('J',k)+3*mom('N',k)
def p(k):return mom('J',k)-mom('N',k)
checks={'integer_weights':all(w>=1 for aa in a.values() for x,w in aa),'PF':a['J'][0][1]==1 and all(abs(x)<top for s,aa in a.items()for i,(x,w)in enumerate(aa)if not(s=='J'and i==0)),'bulk_cap':all(abs(x)<=F(95,100) for s,aa in A.items()for i,(x,w)in enumerate(aa)if not(s=='J'and i<2))}
errors={}
for k in range(4,9):
    for name,fn in [('Z',z),('P',p)]:
        target=F(c['estimated_data'][name][str(k)])
        er=abs(F(fn(k),D**k)/target-1);errors[f'{name}{k}']=float(er);checks[f'{name}{k}']=er<=F(1,10**8)
# Positive extra J atom harmless; total absolute BULK < top^L suffices for BOTH Z,P.
bulk=[(abs(x),w*(1 if s=='J'else 3))for s,aa in a.items()for i,(x,w)in enumerate(aa)if not(s=='J'and i<2)]
tail=4; bp=[x**4 for x,w in bulk];tp=top**4
while sum(w*v for v,(x,w)in zip(bp,bulk))>=tp:
    tail+=1;bp=[v*x for v,(x,w)in zip(bp,bulk)];tp*=top
    assert tail<=2000
# Every bulk modulus/top<1: the tail remains bounded at all larger L.
failures=[]
powers={s:[x**4 for x,w in aa] for s,aa in a.items()}
for k in range(4,tail):
    J=sum(v*w for v,(x,w)in zip(powers['J'],a['J']));N=sum(v*w for v,(x,w)in zip(powers['N'],a['N']))
    if J+3*N<=0:failures.append(['Z',k])
    if J-N<=0:failures.append(['P',k])
    powers={s:[v*x for v,(x,w)in zip(powers[s],aa)]for s,aa in a.items()}
checks['F4_all_lengths']=not failures
purity={}
for n in (256,300):
    zn=z(n);z2=z(2*n);checks[f'seed_killed_{n}']=2*z2*z2<=zn**4
    purity[str(n)]=z2/(zn**2)
out={'status':'TESTED','accepted':all(checks.values()),'checks':checks,'relative_residuals':errors,'F4_tail_from':tail,'F4_prefix_failures':failures,'S':purity,'candidate_sha256':hashlib.sha256(Path('candidate.json').read_bytes()).hexdigest(),'basis':'Exact integer/Fraction checks against rational synthetic estimates. ED input NOT rigorous.'}
Path('check_integer_result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
assert out['accepted']
