#!/usr/bin/env python3
"""Targeted in-memory corruption tests; never changes frozen producer inputs."""
from audit_interval import *
from copy import deepcopy
verify_inputs();models=audit_models();base=load(SRC/'coverage/interval_016.json')


def setpath(rec,path,val):
    at=rec
    for key in path[:-1]:at=at[key]
    at[path[-1]]=val

cases=[
 ('metric norm', ['denominator_patches',0,'integer_metric_norm'],'1'),
 ('affine Rayleigh slope', ['denominator_patches',0,'rayleigh_coefficients',1],'0'),
 ('full quadratic residual', ['denominator_patches',0,'full_residual_squared_coefficients',2],'0'),
 ('even Temple denominator', ['denominator_patches',0,'even_Temple_denominator'],'2'),
 ('omitted first bosonic shell', ['trace_upper_certificates',0,'reference_q_range'],[2,16]),
 ('unproved retained excited state', ['trace_upper_certificates',0,'retained_states'],2),
 ('uncorrelated exponent', ['correlated_energy_combinations','J1','uniform_lower'],'0'),
 ('wrong canonical transport', ['canonical_first_purities',0],'1'),
 ('missing intermediate window', ['finite_windows'],base['finite_windows'][1:]),
 ('deduplicated period-two graph', ['short_sizes',0,'edge_square_sum'],8),
 ('inflated final uniform gap', ['all_integer_L_ge2_gap'],'1/100'),
]
results=[]
for name,path,value in cases:
    rec=deepcopy(base);setpath(rec,path,value)
    try:audit_record(rec,models)
    except (AssertionError,KeyError,IndexError):results.append(dict(test=name,rejected=True));print('REJECTED',name,flush=True)
    else:raise AssertionError('Invalid modified certificate accepted: '+name)
save('rejection_guards.json',results)
