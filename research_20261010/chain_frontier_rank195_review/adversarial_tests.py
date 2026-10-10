import audit as A
import audit_obstructions as O
import json,time
from copy import deepcopy
start=time.monotonic();mom=json.loads((A.SNAP/'expanded_moments.json').read_text());data=A.moments(mom);rec=json.loads((A.SNAP/'expanded_inputs.json').read_text())[0];s=rec['small'];tw=json.loads((A.SNAP/'triplet_witness.json').read_text());tests=[]
def reject(name,fn):
 try:fn()
 except AssertionError:tests.append(dict(test=name,status='REJECTED'));return
 raise AssertionError('Accepted invalid input: '+name)
for name,key,i,j in [('nonunit Gram weight','Gram_diagonal',0,None),('full residual offdiagonal','unit_residual_Gram',0,1),('truncated second moment','unit_J',0,0)]:
 bad=deepcopy(mom)
 if j is None:bad[key][i]=str(A.F(bad[key][i])+1)
 else:bad[key][i][j]=str(A.F(bad[key][i][j])+1)
 reject(name,lambda:A.moments(bad))
bad=deepcopy(mom);quintet=next(i for i,st in enumerate(bad['basis']) if any(x>=4 for x in st));bad['basis'][quintet]=[0,0,0,0];reject('omitted single quintet reference',lambda:A.moments(bad))
for name,edit in [('false spin ladder',lambda t:t['vectors'][0].__setitem__(0,'1')),('wrong triplet metric norm',lambda t:t.update(metric_norm='1')),('wrong variational energy',lambda t:t.update(shifted_rayleigh='0')),('wrong nullspace dimension',lambda t:t.update(highest_weight_nullspace_dimension=23))]:
 bad=deepcopy(tw);edit(bad);reject(name,lambda:A.triplet(bad,s,data))
for name,edit in [('incorrect E>=4 complement cutoff',lambda b:b.update(omitted_cutoff=str(A.F(b['omitted_cutoff'])+1))),('wrong omitted count',lambda b:b.update(remaining_count=6367)),('threshold equals complement cutoff',lambda b:b['comparison_endpoints'][0].update(lower=b['omitted_cutoff']))]:
 bad=deepcopy(s);edit(bad['expanded_band']);reject(name,lambda:A.patch(bad,data))
mat=json.loads((A.BASE/'joint_ratio_review/chain_snapshot/M8_two_trial_moments.json').read_text());ob=json.loads((A.SNAP/'denominator_obstruction_g1d4.json').read_text());lam=A.F(ob['M8_span_rayleigh_lower']);reject('span lower bound shifted unsafely upward',lambda:O.matrix_span(mat,lam+1))
bad=deepcopy(mat);bad['G'][0][0]='-1';reject('nonpositive numerator norm Gram',lambda:O.matrix_span(bad,lam))
delta=A.F(ob['delta_exact']);d=A.F(ob['triplet_excitation_exact'])
for name,edit in [('missing beta interval',lambda b:b['intervals'].pop()),('understated first interval output',lambda b:b['intervals'][0].update(joint_after_first_cycle_upper='-1')),('unsafe triplet excitation upper',lambda b:b.update(triplet_excitation_upper='0'))]:
 bad=deepcopy(ob);edit(bad);reject(name,lambda:O.replay(bad,delta,d,A.F(17,25)))
assert A.inertia([[0,1],[1,0]])[:2]==(1,0) and A.inertia([[0,0],[0,0]])[:2]==(0,2)
A.save('adversarial_tests.json',dict(status='PASS',tests=tests,rejected_count=len(tests),singular_inertia_cases=2,seconds=time.monotonic()-start));print('ADVERSARIAL PASS',len(tests),flush=True)
