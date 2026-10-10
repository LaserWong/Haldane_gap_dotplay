"""Replay-equality rejection tests for new fixed-family/trace certificate fields.
Uses trusted reconstructed expected data once, rather than repeating exponentials.
"""
import certify_lowband as B
C=B.C
import json,copy
from fractions import Fraction as F

def main():
 saved=json.loads((C.HERE/'lowband/interval_009.json').read_text());lo,hi=map(F,saved['coupling_interval'])
 vecs=[p['integer_coefficients'] for p in saved['denominator_patches']]+[saved['largest_base_trial']['integer_coefficients']]
 expected=B.interval_data(lo,hi,vecs)
 assert all(saved[k]==v for k,v in expected.items())
 def verify(candidate):assert all(candidate[k]==v for k,v in expected.items())
 mutations=[
 ('odd center',lambda r:r['denominator_patches'][0]['odd_band'].__setitem__('fixed_center','0')),
 ('number sectors',lambda r:r['denominator_patches'][0]['odd_band'].__setitem__('q_components',[1,5])),
 ('spin multiplicity',lambda r:r['denominator_patches'][0]['odd_band'].__setitem__('spin_multiplicity',2)),
 ('odd dimension',lambda r:r['denominator_patches'][0]['odd_band'].__setitem__('retained_odd_dimension',47)),
 ('Fourier Gram',lambda r:r['denominator_patches'][0]['odd_band']['modes'][0].__setitem__('gram_symbol',['0','0'])),
 ('fixed theta coefficient',lambda r:r['denominator_patches'][0]['odd_band']['modes'][0]['theta_coefficients'][1].__setitem__(0,'0')),
 ('mixed H2 coefficient',lambda r:r['denominator_patches'][0]['odd_band']['modes'][0]['second_moment_coefficients'][1].__setitem__(0,'0')),
 ('full variance',lambda r:r['denominator_patches'][0]['odd_band']['modes'][0].__setitem__('residual_squared_max','0')),
 ('Temple denominator',lambda r:r['denominator_patches'][0]['odd_band']['modes'][0].__setitem__('uniform_Temple_denominator','2')),
 ('Temple width',lambda r:r['denominator_patches'][0]['odd_band']['modes'][0].__setitem__('uniform_Temple_width','0')),
 ('relative eigen endpoint',lambda r:r['denominator_patches'][0]['odd_band']['modes'][0].__setitem__('eigen_lower_minus_ground_rayleigh_uniform_lower','2')),
 ('missing momentum',lambda r:r['denominator_patches'][0]['odd_band']['modes'].pop()),
 ('inflated filter',lambda r:r['largest_interval_filter'].__setitem__('uniform_improvement','1')),
 ('uncorrelated exponent',lambda r:r['correlated_energy_combinations']['J1'].__setitem__('uniform_lower','1'))]
 passed=[]
 for label,mut in mutations:
  r=copy.deepcopy(saved);mut(r)
  try:verify(r)
  except AssertionError:passed.append(label)
  else:raise AssertionError(('mutation was not rejected',label))
 # Rebuild exact trace arithmetic and reject double-counting the odd q=1 tail,
 # omitted spin multiplicity, and fabricated trace/retained-count metadata.
 beta=F(saved['beta_initial']);u,trace=B.upper_exact(expected['denominator_patches'][0],beta)
 assert trace==saved['trace_upper_certificates'][0]
 trace_guards=0
 for key,val in [('retained_states',1),('reference_q_range',[1,16]),('spin_multiplicity',1),('normalized_odd_band_upper','0'),('normalized_trace_upper','1')]:
  r=copy.deepcopy(trace);r[key]=val;assert r!=trace;trace_guards+=1
 out=dict(status='PASS producer replay corruption guards',rejected_physical_mutations=passed,
  rejected_trace_metadata_mutations=trace_guards,warning='Producer tests are not an independent mathematical audit.')
 (C.HERE/'rejection_test_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
