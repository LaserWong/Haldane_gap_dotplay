#!/usr/bin/env python3
"""Independent in-memory corruption and exact interval-edge regression tests."""
from audit_interval import *
from copy import deepcopy
verify_inputs();models=audit_models();base=load(SRC/'coverage/interval_012.json')

def setpath(rec,path,val):
    at=rec
    for key in path[:-1]:at=at[key]
    at[path[-1]]=val

cases=[
 ('metric norm', ['denominator_patches',0,'integer_metric_norm'],'1'),
 ('affine Rayleigh slope', ['denominator_patches',0,'rayleigh_coefficients',1],'0'),
 ('full quadratic residual', ['denominator_patches',0,'full_residual_squared_coefficients',2],'0'),
 ('even Temple denominator', ['denominator_patches',0,'even_Temple_denominator'],'2'),
 ('largest full second moment', ['largest_base_trial','full_second_moment_coefficients',2],'0'),
 ('inflated residual minimum', ['largest_interval_filter','residual_squared_min'],'1'),
 ('wrong residual maximum', ['largest_interval_filter','residual_squared_max'],'0'),
 ('invalid compression upper', ['largest_interval_filter','compressed_upper_at_high','compressed_H_upper'],'1'),
 ('inflated compression pivot', ['largest_interval_filter','compressed_upper_at_high','upper_LDL_positive_pivots',3],'1'),
 ('wrong uniform C', ['largest_interval_filter','Cmax'],'1'),
 ('wrong fixed filter t', ['largest_interval_filter','fixed_t'],'1'),
 ('inflated filter gain', ['largest_interval_filter','uniform_improvement'],'1/10'),
 ('understated augmented dimension', ['largest_interval_filter','original_space_plus_residual_dimension_upper'],29),
 ('incorrect filtered support', ['largest_interval_filter','filtered_trial_max_triplet_number'],4),
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

# Dedicated exact minima tests, including the branch not visited by production intervals.
lo,hi=F(7,100),F(39,500);R=F(load(SRC/'coverage/interval_015.json')['largest_interval_filter']['compressed_upper_at_high']['compressed_H_upper'])
comp=load(SRC/'coverage/interval_015.json')['largest_interval_filter']['compressed_upper_at_high']
rho=[F(-1,2),F(1,10)];C=R-min(poly(rho,g) for g in (lo,hi));t=1/C
edges=[]
for name,vertex,basevar in [('interior minimum',F(37,500),F(1,100)),('left endpoint vertex',lo,F(1,100)),('right endpoint vertex',hi,F(1,100)),('zero variance',None,F(0))]:
    var=[basevar,F(0),F(0)] if vertex is None else [basevar+vertex*vertex,-2*vertex,F(1)]
    points=[lo,hi]+([vertex] if vertex is not None and lo<=vertex<=hi else [])
    vals=[poly(var,g) for g in points];mn,mx=min(vals),max(vals);gain=mn*C/(C*C+mn)
    f=dict(compressed_upper_at_high=comp,residual_squared_min=str(mn),residual_squared_max=str(mx),Cmax=str(C),fixed_t=str(t),uniform_improvement=str(gain),filtered_rayleigh_upper_coefficients=[str(rho[0]-gain),str(rho[1])],original_space_plus_residual_dimension_upper=30,filtered_trial_max_triplet_number=6,retained_ground_contributions=1)
    new,report=check_filter(f,rho,var,lo,hi);assert mn==basevar
    if vertex is not None and lo<vertex<hi:
        corrupted=deepcopy(f);corrupted['residual_squared_min']=str(min(poly(var,g) for g in (lo,hi)))
        try:check_filter(corrupted,rho,var,lo,hi)
        except AssertionError:pass
        else:raise AssertionError('Endpoint-only residual minimum accepted despite interior vertex')
    # Fixed t uniformity checked on a dense rational fixture, supplementing analytic proof.
    for j in range(101):
        g=lo+(hi-lo)*F(j,100);v=poly(var,g);upper=poly(rho,g)+v*(-2*t+(R-poly(rho,g))*t*t)/(1+t*t*v)
        assert upper<=poly(new,g)
    edges.append(dict(test=name,passed=True,variance_min=str(mn),variance_max=str(mx),gain=str(gain)))
save('filter_edgecases.json',edges);print('PASS 21 rejection guards and 4 exact filter edgecases')
