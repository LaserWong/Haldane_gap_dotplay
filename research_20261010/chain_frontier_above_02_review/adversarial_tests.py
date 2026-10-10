import audit as A
from copy import deepcopy
import json,time
start=time.monotonic();mom=json.loads((A.SNAP/'expanded_moments.json').read_text());data=A.moments(mom);rec=json.loads((A.SNAP/'expanded_inputs.json').read_text())[0];s=rec['small'];g=A.F(rec['g']);tests=[]
def reject(name,f):
 try:f()
 except AssertionError:tests.append(dict(test=name,status='REJECTED'));return
 raise AssertionError('Corruption accepted: '+name)
def mutate_moment(name,key,i,j):
 m=deepcopy(mom)
 if j is None:m[key][i]=str(A.F(m[key][i])+1)
 else:m[key][i][j]=str(A.F(m[key][i][j])+1)
 reject(name,lambda:A.moments(m))
mutate_moment('wrong nonunit Gram normalization','Gram_diagonal',0,None)
mutate_moment('dropped residual offdiagonal','unit_residual_Gram',0,1)
mutate_moment('truncated full second moment','unit_J',0,0)
for name,edit in [
 ('wrong weighted complement cutoff',lambda b:b.update(omitted_cutoff=str(A.F(b['omitted_cutoff'])+1))),
 ('quintet omission from reference multiplicity',lambda b:b['complete_reference_bins'][3].__setitem__(1,b['complete_reference_bins'][3][1]-20)),
 ('wrong complement dimension',lambda b:b.update(remaining_count=6495)),
 ('unsafe threshold at complement',lambda b:b['comparison_endpoints'][0].update(lower=b['omitted_cutoff'])),
 ('wrong negative inertia count',lambda b:b['comparison_endpoints'][0].update(negative_inertia=1)),
 ('zero threshold multiplicity',lambda b:b['comparison_endpoints'][0].update(multiplicity=0)),
 ('nonpositive local form',lambda b:b['local_comparison'].update(b='-10'))]:
 z=deepcopy(s);edit(z['expanded_band']);reject(name,lambda:A.patch(z,g,data))
assert A.inertia([[0,1],[1,0]])[:2]==(1,0)
assert A.inertia([[0,0],[0,0]])[:2]==(0,2)
assert A.inertia([[0,1,0],[1,0,0],[0,0,0]])[:2]==(1,1)
assert A.inertia([[1,1],[1,1]])[:2]==(0,1)
A.save('adversarial_tests.json',dict(status='PASS',rejected=tests,exact_zero_and_2x2_pivot_cases=4,seconds=time.monotonic()-start));print('ADVERSARIAL PASS',len(tests),flush=True)
