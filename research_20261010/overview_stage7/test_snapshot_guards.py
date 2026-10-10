#!/usr/bin/env python3
"""Reject scope, dimensions, exclusions, exact-data and provenance corruption."""
import sys; sys.dont_write_bytecode=True
from common import *
from copy import deepcopy
from plot_overview import verify
base=json.loads((HERE/'overview_data.json').read_text());cases=[]
def case(name,mutate):
 d=deepcopy(base);mutate(d)
 try:verify(d)
 except (AssertionError,ValueError,KeyError,StopIteration):cases.append({'test':name,'rejected':True});return
 raise AssertionError('Corruption accepted: '+name)
def final_patch(d,shape):
 return next(r for r in d['dimensions'] if r['support_scope']=='continuous .085 pipeline: complete smaller odd bands' and r['seed_geometry']==shape)
case('changed exact gap',lambda d:d['claims'][0].update(gap_lower_exact='1'))
case('upward display rounding',lambda d:d['claims'][0].update(gap_lower_decimal_down_12='1.000000000000'))
case('missing inherited interval piece',lambda d:d['claims'].remove(next(r for r in d['claims'] if r.get('certificate_route')=='uniform_interval_piece')))
case('missing newest interval piece',lambda d:d['claims'].remove(next(r for r in d['claims'] if r.get('certificate_route')=='range0085_interval_piece')))
case('gap in exact interval cover',lambda d:next(r for r in d['claims'] if r.get('certificate_route')=='range0085_interval_piece').update(parameter_lower_exact='801/10000'))
case('changed Hilbert count',lambda d:d['dimensions'][0].update(full_Hilbert_dimension=1))
case('conflated rank-one search',lambda d:next(r for r in d['dimensions'] if r['implicit_filtered_space_dimension_upper'] is not None).update(proposal_basis_dimension=1))
case('false maximum 30 trial dimensions',lambda d:final_patch(d,'8x4').update(total_trial_space_dimension=30))
case('drop smaller complete odd band',lambda d:final_patch(d,'4x4').update(retained_low_band_count=1))
case('conflate 125 trial space with 97 trace states',lambda d:final_patch(d,'8x4').update(retained_low_band_count=125))
case('change largest numerator rank',lambda d:final_patch(d,'8x8').update(numerator_trial_rank=193))
case('failure encoded as zero physical gap',lambda d:d['unplotted_status'][0].update(gap_lower_exact='0'))
case('changed source digest',lambda d:d['sources'].update({next(iter(d['sources'])):'0'*64}))
case('unaccepted review seal',lambda d:d['review_seals'][0].update(sha256='0'*64))
case('remove prior accepted alternative',lambda d:d['claims'].pop(0))
case('change chain candidate gap',lambda d:d['chain_candidate_routes'][0].update(gap_lower_exact='1'))
case('drop chain candidate route',lambda d:d['chain_candidate_routes'].pop())
case('move accepted point to unsupported .084 parameter',lambda d:next(r for r in d['claims'] if r.get('certificate_route')=='polynomial_frontier_full_band').update(parameter_exact='21/250'))
case('promote unreviewed .09 point',lambda d:next(r for r in d['claims'] if r.get('certificate_route')=='polynomial_frontier_full_band').update(parameter_exact='9/100'))
case('AKLT assigned thermal-bootstrap success',lambda d:d['reference_certificates'][0].update(thermal_bootstrap_success=True))
case('AKLT gap applied from L2',lambda d:d['reference_certificates'][0].update(integer_size_min=2))
case('AKLT MPS bond conflated with local matrix',lambda d:d['reference_certificates'][0].update(MPS_bond_dimension=81))
case('AKLT omitted spectrum count changed',lambda d:d['reference_certificates'][0].update(omitted_state_count_formula='1'))
print(json.dumps({'status':'PASS','corruptions_rejected':len(cases),'cases':cases},indent=2))
