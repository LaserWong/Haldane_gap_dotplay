import audit as A
import json,time
from copy import deepcopy
from fractions import Fraction as F
start=time.monotonic();tests=[]
def reject(name,fn):
 try:fn()
 except AssertionError:tests.append(dict(test=name,status='REJECTED'));return
 raise AssertionError('Invalid input accepted: '+name)
pair=json.loads((A.PAIR/'pair_extension.json').read_text());bare=list(map(A.parse,pair['bare_vectors']));bad=bare[1].copy();bad[next(iter(bad))]*=-1;reject('wrong pair singlet coefficient',lambda:A.symmetry(bad))
bad=bare[1].copy();bad.pop(next(iter(bad)));reject('incomplete translation orbit',lambda:A.symmetry(bad))
reject('duplicate sparse state',lambda:A.parse([[0,'1'],[0,'1']]))
reject('invalid dimer label',lambda:A.parse([[15,'1']]))
reject('false positive rank for duplicate vector',lambda:A.pivots([[F(1),F(1)],[F(1),F(1)]]))
r=json.loads((A.BLOCK/'block_2.json').read_text());G=[list(map(F,z)) for z in r['Gram']];H=[list(map(F,z)) for z in r['H']];b=json.loads((A.BASE/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];rho=F(b['large']['exact_rayleigh']);rho4=F(b['small']['exact_rayleigh'])
for name,change in [('altered Gram overlap',lambda z:z['Gram'][4].__setitem__(4,'1')),('altered cross energy',lambda z:z['H'][0].__setitem__(16,'0')),('wrong rational Rayleigh',lambda z:z.update(exact_rayleigh='-17')),('wrong target pivot',lambda z:z['span_target_LDL_pivots'].__setitem__(0,'1')),('misstated delta',lambda z:z.update(new_delta='0'))]:
 z=deepcopy(r);change(z);reject(name,lambda:A.certify(z,G,H,rho,rho4))
def verify_action(v,saved):assert A.A.action(v)[0]==saved
v=bare[2];im,_=A.A.action(v);bad=im.copy();bad.pop(next(iter(bad)));reject('discarded full-action tail',lambda:verify_action(v,bad))
target=2*rho4+F(19,1250);reject('unsafe raised whole-span threshold',lambda:A.pivots([[H[i][j]-(target+1)*G[i][j] for j in range(17)] for i in range(17)]))
A.save('adversarial_tests.json',dict(status='PASS',rejected_count=len(tests),tests=tests,seconds=time.monotonic()-start));print('ADVERSARIAL PASS',len(tests),flush=True)
