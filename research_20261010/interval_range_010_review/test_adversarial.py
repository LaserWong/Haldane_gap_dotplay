#!/usr/bin/env python3
import audit as T
from audit import *
from copy import deepcopy
models=prepare();base=load(S/'coverage/interval_001.json')
def put(rec,path,value):
    at=rec
    for k in path[:-1]:at=at[k]
    at[path[-1]]=value
cases=[
 ('wrong fixed center',['fixed_vector_center'],'2/25'),
 ('outside audited coupling',['coupling_interval',1],'11/100'),
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
 ('omitted first bosonic shell',['trace_upper_certificates',0,'reference_q_range'],[3,16]),
 ('unproved excited retained state',['trace_upper_certificates',0,'retained_states'],2),
 ('wrong denominator temperature',['trace_upper_certificates',1,'beta'],base['beta_initial']),
 ('uncorrelated energy exponent',['correlated_energy_combinations','J1','uniform_lower'],'0'),
 ('wrong initial transport',['canonical_first_purities',0],'1'),
 ('inflated initial joint lower',['initial_joint_product'],'1'),
 ('transported product substituted',['initial_joint_product'],str(A.full(A.frs(base['canonical_first_purities'])))),
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
 ('moved asymptotic base',['bootstrap','input','n'],7),
 ('inflated asymptotic gap',['bootstrap','uniform_square_gap_lower'],'1'),
 ('omitted short size',['short_sizes'],base['short_sizes'][1:]),
 ('period two multiplicity deduplicated',['short_sizes',0,'edge_square_sum'],8),
 ('inflated final gap',['all_integer_L_ge2_gap'],'1'),
]
cases += [
 ('wrong odd center',['denominator_patches',0,'odd_band','fixed_center'],'2/25'),
 ('wrong Q support',['denominator_patches',0,'odd_band','q_components'],[1,3,5]),
 ('wrong spin multiplicity',['denominator_patches',0,'odd_band','spin_multiplicity'],1),
 ('duplicated momentum',['denominator_patches',0,'odd_band','modes',1,'momentum'],[0,0]),
 ('missing odd mode',['denominator_patches',0,'odd_band','modes'],base['denominator_patches'][0]['odd_band']['modes'][1:]),
 ('invalid odd Gram',['denominator_patches',0,'odd_band','modes',0,'gram_symbol'],['0','0']),
 ('raw unnormalized odd theta',['denominator_patches',0,'odd_band','modes',0,'theta_coefficients',0],['800','0']),
 ('dropped odd full leakage',['denominator_patches',0,'odd_band','modes',0,'second_moment_coefficients',2],['0','0']),
 ('wrong mixed QV coefficient',['denominator_patches',0,'odd_band','modes',0,'second_moment_coefficients',1],['0','0']),
 ('compressed odd residual',['denominator_patches',0,'odd_band','modes',0,'residual_squared_coefficients'],[['0','0']]*3),
 ('wrong odd theta enclosure',['denominator_patches',0,'odd_band','modes',0,'theta_endpoint_enclosures',0],['0','0']),
 ('wrong odd residual enclosure',['denominator_patches',0,'odd_band','modes',0,'residual_squared_endpoint_enclosures',0],['0','0']),
 ('inflated odd Temple denominator',['denominator_patches',0,'odd_band','modes',0,'uniform_Temple_denominator'],'10'),
 ('zero odd Temple width',['denominator_patches',0,'odd_band','modes',0,'uniform_Temple_width'],'0'),
 ('inflated odd lower endpoint',['denominator_patches',0,'odd_band','modes',0,'eigen_lower_minus_ground_rayleigh_uniform_lower'],'1'),
 ('omitted entire odd band trace',['trace_upper_certificates',0,'normalized_odd_band_upper'],'0'),
 ('omitted bosonic trace tail',['trace_upper_certificates',0,'normalized_tail_upper'],'0'),
 ('wrong trace spin count',['trace_upper_certificates',0,'spin_multiplicity'],1),
 ('understated retained-state count',['trace_upper_certificates',0,'retained_states'],17),
 ('wrong trace mode count',['trace_upper_certificates',0,'odd_mode_count'],8),
]
cases=[(n,p,v) for n,p,v in cases if p[0]!='largest_interval_filter' and not (p[0]=='largest_base_trial' and p[1]=='full_second_moment_coefficients')]
cases += [
 ('numerator rank mistaken for retained count',['largest_numerator','retained_states'],43),
 ('numerator omitted q6 support',['largest_numerator','max_triplet_number'],4),
 ('numerator incorrect norm',['largest_base_trial','integer_metric_norm'],'1'),
 ('numerator incorrect slope',['largest_base_trial','rayleigh_coefficients',1],'0'),
 ('numerator coefficients altered',['largest_base_trial','integer_coefficients',1],base['largest_base_trial']['integer_coefficients'][1]+1),
 ('numerator claimed residual',['largest_numerator','residual_required'],True),
 ('numerator Hilbert dimension conflated',['largest_numerator','full_dimension'],43),
]
cases += [
 ('altered complete vector',['denominator_patches',1,'integer_coefficients',0],base['denominator_patches'][1]['integer_coefficients'][0]+1),
 ('wrong complete norm',['denominator_patches',1,'integer_metric_norm'],'1'),
 ('dropped q8 residual',['denominator_patches',1,'max_full_residual_triplet_number'],6),
 ('changed complete variance',['denominator_patches',1,'full_residual_squared_coefficients',2],'0'),
 ('wrong complete second moment',['denominator_patches',1,'full_second_moment_coefficients',2],'0'),
 ('wrong ground identification',['denominator_patches',1,'ground_identification_margin'],'1'),
 ('wrong even-singlet threshold',['denominator_patches',1,'even_Temple_denominator'],'1'),
 ('zero complete Temple width',['denominator_patches',1,'uniform_Temple_width'],'0'),
 ('wrong joint physical base',['joint_ladder_states',0,'joint_product_physical_base'],[16,8,base['joint_ladder_states'][0]['beta']]),
 ('wrong canonical edge axis',['joint_ladder_states',0,'canonical_edge_labels',0,'axis'],'t'),
 ('wrong permuted edge endpoint',['joint_ladder_states',0,'permuted_edge_labels',0,'endpoint',0],16),
]
results=[]
for name,path,val in cases:
 r=deepcopy(base);put(r,path,val)
 try:audit_record(r,models)
 except (AssertionError,ValueError,KeyError,IndexError,TypeError):results.append(dict(test=name,rejected=True));print('REJECTED',name,flush=True)
 else:raise AssertionError('Invalid certificate accepted: '+name)
 E.expi.cache_clear()
records=[load(S/x['file']) for x in load(S/'coverage_summary.json')['intervals']]
for name,fn in [('gap in coverage',lambda r:r[1]['coupling_interval'].__setitem__(0,'861/10000')),('missing interval',lambda r:r.pop(2)),('swapped intervals',lambda r:r.reverse()),('missing top endpoint',lambda r:r[-1]['coupling_interval'].__setitem__(1,'899/10000'))]:
 r=deepcopy(records);fn(r)
 try:coverage(r)
 except AssertionError:results.append(dict(test=name,rejected=True))
 else:raise AssertionError(name)
for name,call in [('component above one',lambda:A.canonical_next([F(1001,1000),F(1),F(1)],F(1))),('zero component',lambda:A.canonical_next([F(0),F(1),F(1)],F(1))),('invalid joint',lambda:A.canonical_next([F(1)]*3,F(1001,1000))),('invalid window product',lambda:A.one_joint(F(1,2),F(1,2)))]:
 try:call()
 except AssertionError:results.append(dict(test=name,rejected=True))
 else:raise AssertionError(name)
G,K,_=models[2];check_numerator_export=N.check_numerator_export
for name,path in [('wrong constant Gram',['gram',29,29]),('dropped q6 number weight',['shifted_A_coefficients',0,29,29]),('lost interaction cross block',['shifted_A_coefficients',1,15,29]),('wrong numerator slope matrix',['shifted_A_coefficients',1,29,29])]:
 r=load(S/'numerator_matrix_polynomial.json');at=r
 for x in path[:-1]:at=at[x]
 at[path[-1]]=str(F(at[path[-1]])+1)
 try:check_numerator_export(r,G,K)
 except AssertionError:results.append(dict(test=name,rejected=True))
 else:raise AssertionError(name)
save('adversarial_rejections.json',results)
print('PASS',len(results),'independent corruption and domain guards',flush=True)
