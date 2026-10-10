"""Confirm independent checker rejects representative counting/Gram errors."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import copy,json
from fractions import Fraction as F
import audit_certificate as A
HERE=Path(__file__).resolve().parent
source=HERE/'snapshot'
if not source.exists():source=HERE.parent/'chain_small_low_band'
mom=json.loads((source/'unit_moments.json').read_text())
rec=json.loads((source/'patch_g1d5.json').read_text());s=rec['small'];g=F(rec['g'])
A.verify_moments(mom);A.verify_patch(s,g)
tests=[]
def reject(name,value,mutate,check):
 x=copy.deepcopy(value);mutate(x)
 try:check(x)
 except AssertionError:tests.append(dict(test=name,status='REJECTED'))
 else:raise AssertionError(('corruption was accepted',name))
reject('wrong P Gram normalization',mom,lambda x:x['Gram_diagonal'].__setitem__(1,'1'),A.verify_moments)
reject('missing residual off-diagonal',mom,lambda x:x['unit_residual_Gram'][1].__setitem__(2,'0'),A.verify_moments)
reject('incorrect full second moment',mom,lambda x:x['unit_J'][0].__setitem__(0,'0'),A.verify_moments)
reject('missing magnetic degeneracy',s,lambda x:x['low_band']['triplet_modes'][0].__setitem__('multiplicity',1),lambda x:A.verify_patch(x,g))
reject('single-quintet omission',s,lambda x:x['low_band']['complete_reference_bins'].__setitem__(3,[3,108]),lambda x:A.verify_patch(x,g))
reject('tail double counts triplets',s,lambda x:x['low_band'].__setitem__('remaining_count',6560),lambda x:A.verify_patch(x,g))
reject('unjustified complement cutoff',s,lambda x:x['low_band'].__setitem__('omitted_cutoff','1'),lambda x:A.verify_patch(x,g))
reject('square root rounded wrong way',s,lambda x:x['low_band']['triplet_modes'][0].__setitem__('root_upper','0'),lambda x:A.verify_patch(x,g))
reject('wrong Hamiltonian ground shift',s,lambda x:x.__setitem__('ground_lower','0'),lambda x:A.verify_patch(x,g))
(HERE/'rejection_guards.json').write_text(json.dumps(dict(status='PASS',tests=tests),indent=2)+'\n');print(json.dumps(tests,indent=2))
