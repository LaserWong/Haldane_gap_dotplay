#!/usr/bin/env python3
"""Reject corrupted plot data instead of silently redrawing unsupported claims."""
from common import *
from copy import deepcopy
from plot_overview import verify
base=json.loads((HERE/'overview_data.json').read_text())
cases=[]
def case(name,mutate):
    d=deepcopy(base);mutate(d)
    try:verify(d)
    except (AssertionError,ValueError,KeyError):cases.append({'test':name,'rejected':True});return
    raise AssertionError('Corruption accepted: '+name)
case('changed exact gap',lambda d:d['claims'][0].update(gap_lower_exact='1'))
case('upward display rounding',lambda d:d['claims'][0].update(gap_lower_decimal_down_12='1.000000000000'))
case('missing interval piece',lambda d:d['claims'].remove(next(r for r in d['claims'] if r.get('certificate_route')=='uniform_interval_piece')))
case('changed Hilbert count',lambda d:d['dimensions'][0].update(full_Hilbert_dimension=1))
case('conflated rank-one search',lambda d:next(r for r in d['dimensions'] if r['implicit_filtered_space_dimension_upper'] is not None).update(proposal_basis_dimension=1))
case('failure encoded as zero gap',lambda d:d['unplotted_status'][0].update(gap_lower_exact='0'))
case('changed source digest',lambda d:d['sources'].update({next(iter(d['sources'])):'0'*64}))
print(json.dumps({'status':'PASS','corruptions_rejected':len(cases),'cases':cases},indent=2))
