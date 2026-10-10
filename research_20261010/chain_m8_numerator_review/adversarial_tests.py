import audit as A
import json,tempfile,time
from copy import deepcopy
start=time.monotonic();tests=[]
def reject(name,fn):
 try:fn()
 except AssertionError:tests.append(dict(test=name,status='REJECTED'));return
 raise AssertionError('Invalid data accepted: '+name)
# Tiny complete-action guards use the same full reconstruction/comparison logic as the large replay.
vec={0:1};image,_=A.action(vec)
with tempfile.TemporaryDirectory(dir=A.HERE) as tmp:
 from pathlib import Path
 p=Path(tmp)/'image.txt';items=sorted(image.items())
 p.write_text(''.join(f'{k} {v}\n' for k,v in items[:-1]));reject('missing leaked action state',lambda:A.verify_file_vector(p,image))
 p.write_text(''.join(f'{k} {v+(i==0)}\n' for i,(k,v) in enumerate(items)));reject('wrong large-image coefficient',lambda:A.verify_file_vector(p,image))
 p.write_text(''.join(f'{k} {v}\n' for k,v in items)+f'{items[0][0]} {items[0][1]}\n');reject('duplicate image state',lambda:A.verify_file_vector(p,image))
 p.write_text(f'{2**32} 1\n');reject('out-of-range packed state',lambda:A.verify_file_vector(p,image))
 p.write_text('145 1\n');reject('wrong integer Hamiltonian denominator',lambda:A.read_packed(p))
 p.write_text('144 1\n0\n');reject('missing local physical coupling',lambda:A.read_packed(p))
m=json.loads((A.HERE/'independent_moments.json').read_text());G=[list(map(A.F,r)) for r in m['Gram']];H=[list(map(A.F,r)) for r in m['Hamiltonian']];rec=json.loads((A.SNAP/'rayleigh_four.json').read_text());rho=H[0][0]/G[0][0];target=A.F(rec['necessary_target_rayleigh'])
for name,edit in [('wrong trial Gram entry',lambda r:r['Gram'][0].__setitem__(0,'1')),('wrong contracted H entry',lambda r:r['H'][3].__setitem__(3,'0')),('wrong exact Rayleigh quotient',lambda r:r.update(exact_rayleigh='-17')),('wrong whole-span exclusion pivot',lambda r:r['span_target_LDL_pivots'].__setitem__(0,'1'))]:
 bad=deepcopy(rec);edit(bad);reject(name,lambda:A.four_span(G,H,bad,rho,target))
reject('dependent trial Gram masquerading as rank four',lambda:A.ldlt([[A.F(1)]*4 for _ in range(4)]))
reject('unsafe raised Rayleigh lower threshold',lambda:A.ldlt([[H[i][j]-(target+1)*G[i][j] for j in range(4)] for i in range(4)]))
# Demonstrate why fixed 64-bit image storage cannot certify the saved image.
big=2**95+3;wrapped=((big+2**63)%2**64)-2**63;assert wrapped!=big
A.save('adversarial_tests.json',dict(status='PASS',rejected_count=len(tests),tests=tests,fixed_64bit_wrap_detected=True,seconds=time.monotonic()-start));print('ADVERSARIAL PASS',len(tests),flush=True)
