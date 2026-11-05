"""Separate exact-Fraction checker of exported rational candidate.
Compatibility is with synthetic rationalized estimates, NOT physical boxes.
"""
from fractions import Fraction as F
import json,hashlib
from pathlib import Path
c=json.loads(Path('candidate.json').read_text())
a={s:[(F(x),int(w)) for x,w in v] for s,v in c['atoms'].items()}
def moment(s,k): return sum((w*x**k for x,w in a[s]),F(0))
def z(k):return moment('J',k)+3*moment('N',k)
def p(k):return moment('J',k)-moment('N',k)
top=a['J'][0][0]
checks={'integer_weights':all(w>=1 for aa in a.values() for x,w in aa),'PF':a['J'][0][1]==1 and all(abs(x)<top for s,aa in a.items() for i,(x,w) in enumerate(aa) if not(s=='J' and i==0))}
errors={}
for k in range(4,9):
    for name,fn in [('Z',z),('P',p)]:
        target=F(c['estimated_data'][name][str(k)]); error=abs(fn(k)/target-1)
        checks[f'{name}{k}']=error<=F(1,10**8);errors[f'{name}{k}']=float(error)
# For L>=tail, all bulk absolute contributions are bounded by PF; second positive J is harmless.
bulk=[(abs(x/top),w*(1 if sec=='J' else 3)) for sec,aa in a.items() for i,(x,w) in enumerate(aa) if not(sec=='J' and i<2)]
tail=4
while sum((w*x**tail for x,w in bulk),F(0))>=1:
    tail+=1
    assert tail<=2000
failures=[]
for k in range(4,tail):
    if z(k)<=0:failures.append(['Z',k])
    if p(k)<=0:failures.append(['P',k])
checks['F4_all_lengths']=not failures
purity={}
for n in (256,300):
    zn=z(n); z2=z(2*n); checks[f'seed_killed_{n}']=2*z2*z2<=zn**4
    purity[str(n)]=float(z2/zn**2)
out={'status':'TESTED','accepted':all(checks.values()),'checks':checks,'relative_residuals':errors,'F4_tail_from':tail,'F4_prefix_failures':failures,'S':purity,'candidate_sha256':hashlib.sha256(Path('candidate.json').read_bytes()).hexdigest(),'basis':'Exact Fraction checks for rational synthetic estimates; ED input not rigorous.'}
Path('check_result.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
