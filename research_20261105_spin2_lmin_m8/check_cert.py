"""Exact integer/Fraction verification of the finite fake against the RIGOROUS boxes cert/enclosures.json.
Independent of the fitter. Checks F1-F4 (finite diagonal operator), every Z_k,P_k (k=4..8) strictly inside its box,
and 2 Z_2n^2 <= Z_n^4 (i.e. S(n) <= 1/sqrt2 given Z>0) at n=256,300."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
c=json.loads(Path('candidate_cert.json').read_text());enc=json.loads(Path('cert/enclosures.json').read_text())
A={s:[(F(x),int(w)) for x,w in aa]for s,aa in c['atoms'].items()}
den=1
for aa in A.values():
    for x,w in aa: den=max(den,x.denominator)
D=10**len(str(den))
assert all((x*D).denominator==1 for aa in A.values() for x,w in aa)
a={s:[(int(x*D),w) for x,w in aa] for s,aa in A.items()}
top=a['J'][0][0]
def mom(s,k):return sum(w*x**k for x,w in a[s])
def z(k):return mom('J',k)+3*mom('N',k)
def p(k):return mom('J',k)-mom('N',k)
checks={'integer_weights':all(w>=1 for aa in a.values() for x,w in aa),
 'PF_simple_dominant':a['J'][0][1]==1 and top>0 and all(abs(x)<top for s,aa in a.items()for i,(x,w)in enumerate(aa)if not(s=='J'and i==0)),
 'bulk_cap_.95':all(abs(x)<=F(95,100) for s,aa in A.items()for i,(x,w)in enumerate(aa)if not(s=='J'and i<2)),
 'second_J_atom_positive':a['J'][1][0]>0}
margins={}
for k in range(4,9):
    for name,fn in [('Z',z),('P',p)]:
        lo,hi=F(enc[f'{name}{k}']['lo']),F(enc[f'{name}{k}']['hi']);v=F(fn(k),D**k)
        checks[f'{name}{k}_in_box']=lo<v<hi
        margins[f'{name}{k}']=[float((v-lo)/(hi-lo)),float((hi-lo)/hi)]
# F4 for all L>=4: exact prefix, then tail: sum_bulk mult*|x|^L < top^L at L=tail implies for all L>=tail
# (each |x|<top), and the second J atom is positive so it only helps Z and P (it is in J; P=J-N, Z=J+3N).
bulk=[(abs(x),w*(1 if s=='J'else 3))for s,aa in a.items()for i,(x,w)in enumerate(aa)if not(s=='J'and i<2)]
tail=4; bp=[x**4 for x,w in bulk];tp=top**4
while sum(w*v for v,(x,w)in zip(bp,bulk))>=tp:
    tail+=1;bp=[v*x for v,(x,w)in zip(bp,bulk)];tp*=top
    assert tail<=2000
failures=[]
for k in range(4,max(tail,9)):
    if z(k)<=0:failures.append(['Z',k])
    if p(k)<=0:failures.append(['P',k])
checks['F4_all_lengths']=not failures
S={}
for n in (256,300):
    zn=z(n);z2=z(2*n);checks[f'seed_killed_{n}']=2*z2*z2<=zn**4
    S[str(n)]=float(F(z2,1)/F(zn,1)**2*D**(0))  # D^(2n)/D^(2n) cancels
out={'accepted':all(checks.values()),'checks':checks,'box_position_and_relwidth':margins,'F4_tail_from':tail,'F4_prefix_failures':failures,'S':S,
 'candidate_sha256':hashlib.sha256(Path('candidate_cert.json').read_bytes()).hexdigest(),
 'enclosures_sha256':hashlib.sha256(Path('cert/enclosures.json').read_bytes()).hexdigest()}
Path('check_cert_result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
assert out['accepted']
