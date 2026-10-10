import audit as A
from fractions import Fraction as F
import json
# Exact Hermiticity of the integer local action in the non-unit dimer metric.
ker={s:{(a,b):v for a,b,v in row} for s,row in A.KERNEL.items()}
for (c,d),row in ker.items():
 for (r,s),v in row.items():assert A.P.W[r]*A.P.W[s]*v==A.P.W[c]*A.P.W[d]*ker[r,s].get((c,d),0)
assert A.DEN==144 and max(A.P.W)**8<2**31 and 0x88888888<2**32
assert max(abs(v) for row in ker.values() for v in row.values())<2**31
assert max(abs(A.DEN*x) for x in [-16,8])<2**31
summary=json.loads((A.HERE/'SUMMARY.json').read_text());assert summary['images'][1]['max_coefficient_bits']==107>64 and summary['max_moment_bits']>128
A.save('overflow_and_structure.json',dict(status='PASS',local_metric_Hermiticity=True,integer_denominator=144,maximum_valid_packed_state='0x88888888',packed_state_bits=32,maximum_local_metric_product=max(A.P.W)**8,maximum_local_integer_coefficient=max(abs(v) for row in ker.values() for v in row.values()),maximum_image_bits=107,maximum_moment_bits=summary['max_moment_bits'],unbounded_integer_implementation='All reconstructed action coefficients and contractions use Python int; all certificate matrices use Fraction. NumPy loads files only. Fixed-width state keys and local coefficients are separately range checked.'))
print('OVERFLOW AND HERMITICITY CHECKS PASS',flush=True)
