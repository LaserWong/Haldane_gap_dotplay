#!/usr/bin/env python3
"""Corruption rejection, exact filter edge cases and scalar domain guards."""
from audit_joint_interval import *
from copy import deepcopy
verify_sources(final=False);models=models_rebuilt();base=load(SRC/'coverage/interval_002.json')
def put(rec,path,value):
    at=rec
    for k in path[:-1]:at=at[k]
    at[path[-1]]=value
cases=[
 ('wrong fixed center',['fixed_vector_center'],'2/25'),
 ('outside audited coupling',['coupling_interval',1],'81/1000'),
 ('wrong normalization',['denominator_patches',0,'integer_metric_norm'],'1'),
 ('changed affine slope',['denominator_patches',0,'rayleigh_coefficients',1],'0'),
 ('changed complete residual',['denominator_patches',0,'full_residual_squared_coefficients',2],'0'),
 ('wrong even Temple denominator',['denominator_patches',0,'even_Temple_denominator'],'2'),
 ('changed largest full second moment',['largest_base_trial','full_second_moment_coefficients',2],'0'),
 ('inflated residual minimum',['largest_interval_filter','residual_squared_min'],'1'),
 ('wrong residual maximum',['largest_interval_filter','residual_squared_max'],'0'),
 ('invalid compression upper',['largest_interval_filter','compressed_upper_at_high','compressed_H_upper'],'1'),
 ('wrong compression pivot',['largest_interval_filter','compressed_upper_at_high','upper_LDL_positive_pivots',3],'1'),
 ('wrong uniform C',['largest_interval_filter','Cmax'],'1'),
 ('wrong fixed filter t',['largest_interval_filter','fixed_t'],'1'),
 ('inflated filter gain',['largest_interval_filter','uniform_improvement'],'1/10'),
 ('understated augmented dimension',['largest_interval_filter','original_space_plus_residual_dimension_upper'],29),
 ('wrong filtered support',['largest_interval_filter','filtered_trial_max_triplet_number'],4),
 ('omitted first bosonic shell',['trace_upper_certificates',0,'reference_q_range'],[2,16]),
 ('unproved excited retained state',['trace_upper_certificates',0,'retained_states'],2),
 ('wrong denominator temperature',['trace_upper_certificates',1,'beta'],base['beta_initial']),
 ('uncorrelated energy exponent',['correlated_energy_combinations','J1','uniform_lower'],'0'),
 ('wrong initial transport',['canonical_first_purities',0],'1'),
 ('inflated initial joint lower',['initial_joint_product'],'1'),
 ('transported product substituted',['initial_joint_product'],str(full(frs(base['canonical_first_purities'])))),
 ('wrong canonical update argument',['joint_ladder_states',0,'canonical_update_arguments',1],'1'),
 ('nonsequential canonical state',['joint_ladder_states',1,'canonical'],base['joint_ladder_states'][0]['canonical']),
 ('stale propagated joint constraint',['joint_ladder_states',1,'joint_product_lower'],base['initial_joint_product']),
 ('permuted route erased',['joint_ladder_states',1,'permuted'],None),
 ('odd reflected base',['joint_ladder_states',0,'n'],9),
 ('wrong doubled temperature',['joint_ladder_states',1,'beta'],base['joint_ladder_states'][0]['beta']),
 ('missing coupled level',['joint_ladder_states'],base['joint_ladder_states'][1:]),
 ('missing early finite window',['finite_windows'],base['finite_windows'][1:]),
 ('moved finite window',['finite_windows',0,'through'],15),
 ('inflated window thermal purity',['finite_windows',0,'thermal_lower'],'999/1000'),
 ('wrong inner product constraint',['finite_windows',0,'details','inner','p'],'1'),
 ('lost spatial joint factor',['finite_windows',0,'details','spatial_lower'],'1'),
 ('inflated window gap',['finite_windows',0,'gap_lower'],'1'),
 ('moved asymptotic base',['bootstrap','input','n'],128),
 ('inflated asymptotic gap',['bootstrap','uniform_square_gap_lower'],'1'),
 ('omitted short size',['short_sizes'],base['short_sizes'][1:]),
 ('period two multiplicity deduplicated',['short_sizes',0,'edge_square_sum'],8),
 ('inflated final gap',['all_integer_L_ge2_gap'],'1/100'),
]
results=[]
for name,path,val in cases:
    r=deepcopy(base);put(r,path,val)
    try:audit_record(r,models)
    except (AssertionError,KeyError,IndexError,TypeError):results.append(dict(test=name,rejected=True));print('REJECTED',name,flush=True)
    else:raise AssertionError('Invalid modified certificate accepted: '+name)
save('adversarial_rejections.json',results)

# Synthetic exact filter polynomials force branches not reached by both actual records.
lo,hi=map(F,base['coupling_interval']);comp=base['largest_interval_filter']['compressed_upper_at_high'];R=F(comp['compressed_H_upper'])
rho=[F(-1,2),F(1,10)];C=R-min(poly(rho,g) for g in (lo,hi));t=1/C;edgecases=[]
for name,vertex,v0 in [('interior', (lo+hi)/2,F(1,100)),('left boundary',lo,F(1,100)),('right boundary',hi,F(1,100)),('zero variance',None,F(0))]:
    var=[v0,F(0),F(0)] if vertex is None else [v0+vertex*vertex,-2*vertex,F(1)]
    points=[lo,hi]+([vertex] if vertex is not None else []);vals=[poly(var,x) for x in points];mn,mx=min(vals),max(vals);gain=mn*C/(C*C+mn)
    f=dict(compressed_upper_at_high=comp,residual_squared_min=str(mn),residual_squared_max=str(mx),Cmax=str(C),fixed_t=str(t),uniform_improvement=str(gain),filtered_rayleigh_upper_coefficients=[str(rho[0]-gain),str(rho[1])],original_space_plus_residual_dimension_upper=30,filtered_trial_max_triplet_number=6,retained_ground_contributions=1)
    new,_=E.check_filter(f,rho,var,lo,hi);assert mn==v0
    if vertex is not None and lo<vertex<hi:
        bad=deepcopy(f);bad['residual_squared_min']=str(min(poly(var,g) for g in (lo,hi)))
        try:E.check_filter(bad,rho,var,lo,hi)
        except AssertionError:pass
        else:raise AssertionError('Unsafe endpoint-only minimum accepted')
    for j in range(101):
        g=lo+(hi-lo)*F(j,100);v=poly(var,g);value=poly(rho,g)+v*(-2*t+(R-poly(rho,g))*t*t)/(1+t*t*v)
        assert value<=poly(new,g)
    edgecases.append(dict(test=name,passed=True,variance_min=str(mn),variance_max=str(mx),gain=str(gain)))
save('filter_edgecases.json',edgecases)

# Domain and positivity guards; no physical inference is made from synthetic points.
guards=[]
for name,call in [
 ('component over one',lambda:canonical_next([F(1001,1000),F(1),F(1)],F(1))),
 ('zero component',lambda:canonical_next([F(0),F(1),F(1)],F(1))),
 ('joint over one',lambda:canonical_next([F(1)]*3,F(1001,1000))),
 ('negative joint',lambda:canonical_next([F(1)]*3,F(-1,10))),
 ('invalid interpolation product',lambda:one_joint(F(1,2),F(1,2))),
 ('interpolation joint over one',lambda:one_joint(F(1),F(1),F(1001,1000))),
]:
    try:call()
    except AssertionError:guards.append(dict(test=name,rejected=True))
    else:raise AssertionError(name)
for v in [F(1,10),F(1,2)]:
    out,args=canonical_next([v,v,v],v**7);assert out is None
    assert plain_next([v,v,v]) is None
    guards.append(dict(test='nonpositive output discarded at '+str(v),passed=True))
save('scalar_domain_guards.json',guards)
print('PASS',len(results),'certificate corruption tests,',len(edgecases),'filter edgecases,',len(guards),'scalar guards',flush=True)
