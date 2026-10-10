#!/usr/bin/env python3
"""Exact extraction checks, source seal verification, and reproducible static plots."""
import sys; sys.dont_write_bytecode=True
from common import *
import argparse,tempfile
os.environ['MPLCONFIGDIR']=tempfile.mkdtemp(prefix='haldane-stage8-mpl-')
os.environ['XDG_CACHE_HOME']=os.environ['MPLCONFIGDIR']
OUT=HERE
BLUE='#245f8b';GREEN='#2e7d49';ORANGE='#b85c21';GRAY='#5c6570';PURPLE='#735291'

def verify(data):
    accepted=json.loads((HERE/'ACCEPTED_REVIEW_SEALS.json').read_text())
    assert data['snapshot_label']=='stage12'
    assert {s['manifest']:s['sha256'] for s in data['review_seals']}==accepted
    for p,h in data['sources'].items():assert sha(ROOT/p)==h,('source changed',p)
    for p,h in data['preserved_stage11_files'].items():assert sha(ROOT/p)==h,('stage6 changed',p)
    count=0
    for seal in data['review_seals']:
        assert sha(ROOT/seal['manifest'])==seal['sha256']
        n=manifest_check(seal['manifest']);assert n==seal['verified_files'];count+=n
    rows=data['claims'];assert len({r['id'] for r in rows})==len(rows)
    previous=json.loads((ROOT/(R+'overview_stage11/overview_data.json')).read_text())
    lookup={r['id']:r for r in rows}
    for old in previous['claims']:
        new=lookup[old['id']]
        for k in ['gap_lower_exact','primary_source','primary_json_pointer','evidence_status','certificate_route','parameter_exact','parameter_lower_exact','integer_size_min','unit_coupling','boundary']:
            assert new.get(k)==old.get(k),('prior alternative changed',old['id'],k)
    assert len(data['dimensions'])>=len(previous['dimensions'])
    for i,old in enumerate(previous['dimensions']):
        assert all(data['dimensions'][i].get(k)==v for k,v in old.items())
    for name in ['tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv']:
        assert sha(HERE/name)==sha(ROOT/(R+'overview_stage11/'+name))
    for r in rows:
        assert F(ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer']))==F(r['gap_lower_exact'])
        assert r['primary_sha256']==data['sources'][r['primary_source']]
        assert floor12(r['gap_lower_exact'])==r['gap_lower_decimal_down_12']
        assert F(r['gap_lower_exact'])>0 and r['integer_size_min']==2
        assert r['proof_family']=='thermal_bootstrap'
        if r['snapshot_stage'] in ['stage7','stage8','stage9','stage10','stage11','stage12']:
            src=json.loads((ROOT/r['primary_source']).read_text())
            assert F(ptr(src,r['parameter_source_pointer']))==F(r['parameter_exact'])
            if r['parameter_kind']=='closed_interval':assert F(ptr(src,r['parameter_lower_source_pointer']))==F(r['parameter_lower_exact'])
        if r['parameter_kind']=='point' and r['plotted_in_main_figure'] and r['snapshot_stage']=='stage12':
            assert all(F(r['gap_lower_exact'])>=F(a['gap_lower_exact']) for a in rows if a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'])
        if r['model']=='ordinary_spinhalf_bilayer':assert F(r['parameter_exact'])<=F('51/500')
    pieces=sorted([r for r in rows if r.get('certificate_route') in data['ordinary_interval_piece_routes']],key=lambda r:F(r['parameter_lower_exact']))
    assert len(pieces)==data['ordinary_interval_piece_count']==data['ordinary_interval_piece_count']
    assert F(pieces[0]['parameter_lower_exact'])==0 and F(pieces[-1]['parameter_exact'])==F(data['ordinary_interval_endpoint'])==F(data['ordinary_interval_endpoint'])
    assert all(F(a['parameter_exact'])==F(b['parameter_lower_exact']) for a,b in zip(pieces,pieces[1:]))
    uniform=max([r for r in rows if r.get('certificate_route')=='uniform_interval_union'],key=lambda r:F(r['parameter_exact']))
    assert F(uniform['gap_lower_exact'])==min(F(r['gap_lower_exact']) for r in pieces)==F('486442811/250000000000')
    assert len([r for r in pieces if F(r['parameter_exact'])<=F('41/500')])==40
    assert len([r for r in pieces if F(r['parameter_lower_exact'])>=F('41/500')])==data['ordinary_interval_piece_count']-40
    for d in data['dimensions']:
        ptr(json.loads((ROOT/d['evidence_source']).read_text()),d['evidence_json_pointer'])
        n=d['dimer_or_rung_count'];assert d['physical_spin_count']==2*n
        assert d['full_Hilbert_dimension']==(9**n if d['model']=='alternating_spin1_chain' else 4**n)
        for key in ['proposal_basis_dimension','retained_low_band_count','numerator_trial_rank','expanded_vector_support','full_H_applied_support']:
            assert d[key] is None or 0<d[key]<=d['full_Hilbert_dimension']
        if d['implicit_filtered_space_dimension_upper'] is not None:
            assert d['implicit_filtered_space_dimension_upper']==d['proposal_basis_dimension']+1
            assert d['filtered_max_triplet_number']==6 and d['original_max_triplet_number']==4
            assert d['numerator_trial_rank']==1
        assert d['MPS_bond_dimension'] is None
        if d.get('total_trial_space_dimension') is not None:
            s=json.loads((ROOT/d['evidence_source']).read_text());reg=ptr(s,d['evidence_json_pointer'])
            k=['4x4','8x4','8x8'].index(d['seed_geometry'])
            assert d['total_trial_space_dimension']==reg['total_augmented_trial_dimensions'][k]
            if k<2:
                assert d['retained_low_band_count']==reg['denominator_retained_states'][k]
                assert d['fixed_witness_span_dimension']==d['retained_low_band_count']
                assert d['odd_trial_space_dimension']==d['retained_low_band_count']-1
                assert d['total_trial_space_dimension']==d['proposal_basis_dimension']+d['odd_trial_space_dimension']
            else:assert d['numerator_trial_rank']==1 and d['total_trial_space_dimension']==30
    latest_band=[d for d in data['dimensions'] if d['support_scope']=='continuous .085 pipeline: complete smaller odd bands']
    assert [d['total_trial_space_dimension'] for d in latest_band]==[59,125,30]
    assert [d['retained_low_band_count'] for d in latest_band]==[49,97,None]
    assert all(r['gap_lower_exact'] is None and not r['plotted_as_zero_gap'] for r in data['unplotted_status'])
    assert len(data['chain_candidate_routes'])==207
    for r in data['chain_candidate_routes']:
        d=json.loads((ROOT/r['primary_source']).read_text());path=ptr(d,r['primary_path_pointer'])
        gap=F(path['all_M_ge2_gap_lower']) if r['route']=='counted_low_band' else min(F(path['M_ge8_gap_lower']),F(ptr(d,r['short_gap_pointer'])))
        assert gap==F(r['gap_lower_exact']) and floor12(gap)==r['gap_decimal_down_12']
        assert r['source_sha256']==data['sources'][r['primary_source']]
    assert len(data['reference_certificates'])==1
    r=data['reference_certificates'][0];e=ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer'])
    assert 'Gap>=1/10 and exactly 3^L-1 omitted states for L>=5' in e
    assert 'Periodic uniqueness L>=3' in e
    assert r['gap_lower_exact']=='1/10' and r['integer_size_min']==5 and r['unique_ground_integer_size_min']==3
    assert r['MPS_bond_dimension']==2 and r['retained_state_count']==1 and r['local_proof_matrix_dimension']==81
    assert r['proof_family']=='finite_size_projector_criterion' and r['thermal_bootstrap_success'] is False
    assert r['full_Hilbert_dimension_formula']=='3^L' and r['omitted_state_count_formula']=='3^L-1'
    new=[r for r in rows if r.get('certificate_route') in ['third_moment_enlarged_numerator','third_moment_two_vector_numerator']]
    assert len(new)==2
    assert {r['gap_lower_exact'] for r in new}=={'27330086079/1000000000000','555972487/500000000000'}
    enlarged=[d for d in data['dimensions'] if d['support_scope']=='independently checked exact enlarged search; scalar use only at largest seed']
    assert [d['proposal_basis_dimension'] for d in enlarged]==[16,43,43]
    assert enlarged[-1]['numerator_trial_rank']==1 and enlarged[-1]['full_Hilbert_dimension']==2**128
    envelopes=data['recipe_upper_envelopes'];assert len(envelopes)==4
    assert [r['denominator_length'] for r in envelopes]==[6,8,10,12]
    for r in envelopes:
        src=json.loads((ROOT/r['primary_source']).read_text())
        assert F(ptr(src,r['primary_json_pointer']))==F(r['upper_cap_exact'])
        assert r['quantity']=='upper cap on attainable certified lower ratio J_lower'
        assert r['gap_lower_exact'] is None and r['not_a_gap_bound'] and r['not_a_physical_purity_upper_bound'] and r['no_all_method_seed_minimum']
        assert r['MPS_bond_dimension']==26 and r['retained_numerator_states']==1
        assert r['physical_denominator_dimension']==3**r['denominator_length'] and r['physical_numerator_dimension']==3**r['numerator_length']
    if data['interval_range_009_included']:
        assert data['ordinary_interval_piece_count'] in [56,66] and F(data['ordinary_interval_endpoint'])>=F('9/100')
        assert R+'interval_range_009_review/MANIFEST_SHA256.json' in accepted
    if data['mps_excited_seed_review_included']:
        assert R+'mps_excited_seed_review/MANIFEST_SHA256.json' in accepted
        rs=data['excited_witness_upper_envelopes'];assert [r['denominator_length'] for r in rs]==[14,16,20,24]
        for r in rs:
            src=ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer'])
            assert F(r['upper_cap_exact'])==F(src['max_J_upper']) and r['unresolved_boxes']==src['unresolved_boxes']
            assert r['all_beta_recipe_excluded']==(r['denominator_length']<24)
            assert r['not_a_gap_bound'] and r['not_a_physical_purity_upper_bound'] and r['no_all_method_seed_minimum'] and r['no_successful_startup_claim']
            assert r['MPS_bond_dimension']==26 and r['excited_MPS_bond_dimension_upper']==52 and r['denominator_orthogonal_witnesses']==3 and r['retained_numerator_states']==1
            assert r['gap_lower_exact'] is None
        boxes=rs[-1]['unresolved_boxes'];assert boxes[0][0]=='13/2' and boxes[-1][1]=='45/4'
        assert all(F(a[1])==F(b[0]) for a,b in zip(boxes,boxes[1:]))
    assert len(previous['claims'])==228
    for old in previous['claims']:
        assert lookup[old['id']]==old, ('stage8 row not preserved',old['id'])
    assert len(rows)==296+(5 if data['stage12_frontier_point_included'] else 0)+(10 if data['stage12_frontier_interval_included'] else 0)
    assert [r for r in pieces if r['snapshot_stage']!='stage11']==[r for r in previous['claims'] if r.get('certificate_route') in previous['ordinary_interval_piece_routes']]
    new=[r for r in rows if r['snapshot_stage']=='stage9']
    assert {r['parameter_exact']:r['gap_lower_decimal_down_12'] for r in new}=={'21/100':'0.101607534008','11/50':'0.065580452251','9/40':'0.045509923956'}
    c=data['stage9_chain_dimensions'];src=json.loads((ROOT/c['source']).read_text())
    assert c['reference_dimension']==src['reference_dimension']==67 and c['omitted_count']==src['omitted_count']==6494
    assert c['full_Hilbert_dimension']==9**c['reference_M']==6561 and c['physical_spin_count']==8
    assert c['ground_trial_dimension']==1099 and c['full_ground_action_support']==1107
    assert c['weak_action_union']==src['full_action_union']==786 and c['residual_union']==src['residual_union']==719
    assert c['largest_M']==8 and c['largest_physical_spin_count']==16 and c['largest_full_Hilbert_dimension']==9**8
    assert c['largest_search_dimension']==2 and c['largest_trial_support']==43294 and c['largest_retained_numerator_states']==1
    assert c['largest_physical_input_unchanged'] and c['MPS_bond_dimension'] is None
    assert [r['extension'] for r in data['mps_extensions']]==['longitudinal_extension','momentum_extension']
    for r in data['mps_extensions']:
        assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text())
        assert r['source_sha256']==data['sources'][r['primary_source']]
        assert r['gap_lower_exact'] is None and r['not_a_gap_bound'] and r['necessary_screen_only']
    v=data['mps_extensions'][1]['verdict']
    assert v['individual_MPS_bond_max']==52 and v['transverse_Gram_rank']==23
    assert v['rows'][1]['retained_denominator_span_dimension']==70
    assert v['rows'][1]['inconclusive_closed_unions']==[['539/64','339/32']]
    assert v['finite_n24_ground_singlet_derived'] and not v['H_eigenstate_assumption_used']
    assert not v['actual_seed_startup_certified'] and not v['spectral_gap_claim']
    r=data['bilayer_g010_diagnostics'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text())
    assert r['source_sha256']==data['sources'][r['primary_source']]
    assert r['gap_lower_exact'] is None and not r['new_gap_proof'] and r['conditional_sensitivity_only'] and not r['unrestricted_M0_M5_optimality']
    assert data['rank195_review_included'] and data['ongoing_current_operator_and_chain_numerator_branches_excluded']
    assert accepted[R+'bilayer_complete_residual_8x4_review/MANIFEST_SHA256.json']=='47ca2166342038a845f45d774bd9e2d91429496235df6e6d0fc39fb678a2b081'
    assert accepted[R+'chain_frontier_rank195_review/MANIFEST_SHA256.json']=='1365bd8c7fe06acf5c4c8bdaf264d1638c17bad5df72c8d753a8ee6ac615c959'
    r=data['complete_residual_review'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text())
    assert r['source_sha256']==data['sources'][r['primary_source']]
    assert r['verdict']['all_integer_L_ge2_gap']=='1559041531/40000000000'
    assert not r['largest_residual_computed'] and not r['production_q8_enumerated']
    assert r['hardcore_signed_commutator'] and r['coherent_sector_interference_preserved'] and r['complete_denominator_tail_retained']
    point=next(r for r in rows if r.get('certificate_route')=='complete_8x4_hardcore_residual')
    assert point['parameter_exact']=='1/10' and point['parameter_kind']=='point' and point['gap_lower_decimal_down_12']=='0.038976038275'
    ds=data['stage10_bilayer_dimensions']
    assert [r['ground_search_dimension'] for r in ds]==[11,43,43]
    assert [r['total_trial_space_dimension'] for r in ds]==[59,139,43]
    assert [r['retained_denominator_states'] for r in ds]==[49,97,None]
    assert [r['retained_numerator_states'] for r in ds]==[None,None,1]
    assert [r['full_Hilbert_dimension'] for r in ds]==[2**32,2**64,2**128]
    assert [r['physical_spin_count'] for r in ds]==[32,64,128] and all(r['MPS_bond_dimension'] is None for r in ds)
    r=data['rank195_obstruction'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text())
    assert r['source_sha256']==data['sources'][r['primary_source']]
    assert r['gap_lower_exact'] is None and r['fixed_early_window_only'] and r['not_physical_gaplessness']
    assert not r['verdict']['new_positive_gap_certificate']
    assert r['necessary_improvement_strict_lower_decimal']=='0.000426143856861' and r['rounded_approximation_only']=='0.000426143856862'
    target=F(r['verdict']['necessary_numerator_target']['exact_required_improvement'])
    assert F(r['necessary_improvement_strict_lower_decimal'])<target<F(r['rounded_approximation_only'])
    assert not any(r['model']=='alternating_spin1_chain' and F(r['parameter_exact'])>=F('1/4') for r in rows)
    if data['interval_range_010_included']:
        assert accepted[R+'interval_range_010_review/MANIFEST_SHA256.json']=='d6eb3e4ce912086fe66dc1eb2917c3ae7381bc6a527a939b99229b97b863f3e5'
        r=data['interval_range_010_review'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text())
        assert r['source_sha256']==data['sources'][r['primary_source']]
        assert data['ordinary_interval_piece_count']==66 and data['ordinary_interval_endpoint']=='1/10'
        extension=[r for r in pieces if r.get('certificate_route')=='range010_interval_piece']
        assert len(extension)==10 and min(F(r['gap_lower_exact']) for r in extension)==F('2190412273/250000000000')
        assert r['verdict']['ground_search_dimensions']==[d['ground_search_dimension'] for d in ds]
        assert r['verdict']['denominator_total_search_dimensions']==[59,139]
        assert r['verdict']['denominator_retained_states']==[49,97] and r['verdict']['largest_retained_numerator_states']==1
        assert r['verdict']['full_Hilbert_dimensions']==[str(d['full_Hilbert_dimension']) for d in ds]
    assert all(r.get('snapshot_stage')!='stage10' or r['model']=='ordinary_spinhalf_bilayer' for r in rows)
    assert not data['cooled_seed_candidates_included'] and data['historical_mps_windows_superseded']
    assert len(data['stage11_review_pins'])==7
    for directory,h in data['stage11_review_pins'].items():assert accepted[R+directory+'/MANIFEST_SHA256.json']==h
    keys=['stage11_integer_window_acceptance','stage11_producer_prose_erratum','stage11_pair_block','stage11_transfer_moments','stage11_transfer_verdicts','stage11_mps_current','stage11_mps_direct_window','stage11_mps_even_completion']
    for key in keys:
        r=data[key];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text())
        assert r['source_sha256']==data['sources'][r['primary_source']]
        assert r['gap_lower_exact'] is None
        if key=='stage11_integer_window_acceptance':assert r['aggregate_acceptance_record']
        else:assert r['not_a_gap_bound']
    new=[r for r in rows if r['snapshot_stage']=='stage11']
    assert {r['parameter_exact']:r['gap_lower_exact'] for r in new}=={'21/100':'26856243/250000000','11/50':'71581253/1000000000','9/40':'20723/400000'}
    f=data['finite_size_certificates'];assert len(f)==1
    f=f[0];assert f['parameter_exact']=='1/4' and f['gap_lower_exact']=='1/100'
    assert f['integer_size_min']==2 and f['integer_size_max']==16 and not f['all_size_certificate'] and f['unique_finite_volume_ground_state']
    assert F(ptr(json.loads((ROOT/f['primary_source']).read_text()),f['primary_json_pointer']))==F(f['gap_lower_exact'])
    assert f['source_sha256']==data['sources'][f['primary_source']] and f['gap_lower_decimal_down_12']==floor12(f['gap_lower_exact'])
    e=data['stage11_producer_prose_erratum']['verdict'];assert not e['numerical_certificate_changed']
    assert F('.54167130')<F(e['exact_lower_endpoint'])<F('.542')
    r=data['stage11_pair_block'];v=r['verdict']
    assert not r['inherited_vectors_exact_symmetry'] and not r['combined_spans_exact_symmetry']
    assert r['only_new_pair_directions_exact_singlets'] and r['old_route_exclusion_only']
    assert v['physical_trial_ranks']==[9,13,17] and v['bare_sector_complete_dimension']==5
    assert not v['inherited_vectors_exact_symmetry'] and not v['combined_spans_claimed_exact_symmetry_sectors']
    assert not v['accepted_denominator_or_global_ground_identification_requires_inherited_M8_singlet']
    assert not v['new_direct_time_first_window_excluded'] and not v['positive_all_size_gap_claimed']
    r=data['stage11_transfer_moments'];assert r['trace_upper_bound_only'] and not r['physical_gap_claim'] and r['cooling_scan_not_universal']
    v=r['verdict'];assert F(v['trace_bounds']['24'])<=F('1.238492320537') and F(v['trace_bounds']['48'])<=F('1.131484383792')
    v=data['stage11_mps_current']['verdict'];assert v['physical_n24_exact_integers']==74 and v['physical_n24_correlations']==37
    assert v['all_beta_recipe_exclusions']==[70,73] and v['retained_denominator_states']==[70,73]
    assert v['MPS_D_ground']==26 and v['MPS_bond_current_combination_upper']==156 and v['local_search_dimension']==2
    assert v['retained_numerator_states']==1 and v['numerator_length']==48
    assert not v['physical_spectral_gap_claim'] and not v['universal_seed_minimum_claim'] and not v['new_direct_window_route_included']
    assert v['rational_pi_trial_differences_display'][0]==.4238202243082572
    v=data['stage11_mps_direct_window']['verdict'];assert v['separately_checked_n']==list(range(6,25,2))
    assert v['all_permitted_continuation_paths_fail'] and v['all_finite_windows_granted'] and not v['universal_necessary_threshold_claim']
    assert v['n24_retained_states']==[70,73] and F(v['n24_joint_upper_max'])<F('99/100')
    v=data['stage11_mps_even_completion']['verdict'];assert [(r['n'],r['retained_denominator_states'],r['numerator_length']) for r in v['all_beta_recipe_exclusions']]==[(18,3,36),(18,4,36),(22,3,44),(22,4,44)]
    assert data['cooled_seed_independent_review_included']
    r=data['stage11_cooled_acceptance'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
    assert all(x['unique_ground_state'] for x in r['verdict']['rows'])
    assert r['verdict']['below_L54']=='NOT CLAIMED' and r['verdict']['minimal_seed']=='NOT CLAIMED'
    r=data['stage11_cooled_review'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
    cs=data['uniform_large_size_certificates'];assert len(cs)==4
    assert [(r['integer_size_min'],r['gap_lower_exact']) for r in cs]==[(60,'51/5000'),(56,'17/2500'),(54,'1/400'),(52,'19/5000')]
    for r in cs:
        src=json.loads((ROOT/r['primary_source']).read_text());assert F(ptr(src,r['primary_json_pointer']))==F(r['gap_lower_exact'])
        assert ptr(src,r['size_source_pointer'])==r['integer_size_min'] and r['primary_sha256']==data['sources'][r['primary_source']]
        assert r['gap_lower_decimal_down_12']==floor12(r['gap_lower_exact'])
        assert r['integer_size_max'] is None and r['unique_finite_volume_ground_state'] and r['all_integers_including_odd'] and not r['claimed_below_minimum'] and not r['minimum_seed_proven']
        assert r['MPS_bond_dimension']==26 and r['retained_numerator_states']==1
        assert r['denominator_full_dimension_formula']=='3^'+str(r['integer_size_min']) and r['numerator_full_dimension_formula']=='3^'+str(2*r['integer_size_min'])
    for i,r in enumerate(previous['uniform_large_size_certificates']):assert data['uniform_large_size_certificates'][i]==r
    assert data['finite_size_certificates']==previous['finite_size_certificates']
    for directory,h in data['stage12_review_pins'].items():assert accepted[R+directory+'/MANIFEST_SHA256.json']==h
    for key in ['stage12_bilayer_direct_acceptance','stage12_bilayer_direct_erratum','stage12_bilayer_continuation','stage12_bilayer_continuation_acceptance','stage12_uniform_n52']:
        r=data[key];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
    v=data['stage12_bilayer_direct_acceptance']['verdict'];assert v['gap_lower']=='55807148827/1000000000000' and v['coupling']=='1/10'
    assert not v['continuous_coupling_claim'] and v['all_integer_square_sides_from']==2 and v['unique_finite_volume_ground']
    v=data['stage12_bilayer_continuation_acceptance']['verdict'];assert v['source_intervals']==66 and v['required_finite_windows']==517
    assert v['uniform_gap_lower']=='4499695659/1000000000000' and v['closed_real_parameter_coverage'] and not v['no_physical_gap_monotonicity_assumption'] is False
    current=sorted([r for r in rows if r.get('certificate_route') in data['current_ordinary_interval_piece_routes']],key=lambda r:F(r['parameter_lower_exact']))
    assert len(current)==data['current_ordinary_interval_piece_count']==(74 if data['stage12_frontier_interval_included'] else 66)
    assert F(current[0]['parameter_lower_exact'])==0 and F(current[-1]['parameter_exact'])==F(data['current_ordinary_interval_endpoint'])==F('51/500' if data['stage12_frontier_interval_included'] else '1/10')
    assert all(F(a['parameter_exact'])==F(b['parameter_lower_exact']) for a,b in zip(current,current[1:]))
    assert min(F(r['gap_lower_exact']) for r in current)==F('4499695659/1000000000000')
    unions=[r for r in rows if r.get('certificate_route')==data['current_ordinary_interval_union_route']]
    assert max(F(r['parameter_exact']) for r in unions)==F(data['current_ordinary_interval_endpoint'])
    assert all(F(r['gap_lower_exact'])==F('4499695659/1000000000000') for r in unions)
    v=data['stage12_uniform_n52']['verdict'];assert v['gap']=='19/5000' and v['all_integer_L_at_least']==52 and v['unique_ground_state']
    assert v['canonical_seed']=={'n':52,'beta':'567/25','thermal_coordinate':'T(104,567/25)'}
    assert v['below52']=='NOT CLAIMED' and v['minimum_seed']=='NOT CLAIMED'
    if data['stage12_source_scope_included']:
        r=data['stage12_source_scope'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
        v=r['verdict'];assert v['status'].startswith('PASS source confirms untwisted all-integer transfer identity for n>=4')
        for filename,h in v['source_sha256'].items():assert sha(ROOT/(R+'uniform_source_scope_review/'+filename))==h
        assert [c['original_even_L_at_least'] for c in v['comparisons']]==[60,2304]
        for c in v['comparisons']:
            lo,hi=map(F,c['original_gap_interval']);assert lo>0 and hi>=lo
            rlo,rhi=map(F,c['ratio_interval']);assert rlo==F(c['our_gap'])/hi and rhi==F(c['our_gap'])/lo
    if data['stage12_frontier_point_included']:
        for key in ['stage12_frontier_point','stage12_frontier_metadata_erratum']:
            r=data[key];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
        v=data['stage12_frontier_point']['verdict'];assert len(v['points'])==5 and v['points'][-1]['g']=='51/500' and v['points'][-1]['gap_lower']=='8254966001/500000000000'
        assert not v['continuous_gap_interval_claim'] and v['fixed_odd_family_z']=='1/10'
        assert v['complete_thermal_tails_checked'] and v['new_coupling_short_size_bounds_checked'] and v['all_integer_square_sides_from']==2
        assert 'fixed z=1/10' in data['stage12_frontier_metadata_erratum']['verdict']['correction']
    if data['stage12_frontier_interval_included']:
        r=data['stage12_frontier_interval'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
        v=r['verdict'];assert v['extension_interval']==['1/10','51/500'] and v['combined_interval']==['0','51/500']
        assert v['extension_uniform_gap']=='13574634391/1000000000000' and v['combined_uniform_gap']=='4499695659/1000000000000'
        assert v['closed_interval_count']==8 and v['combined_closed_interval_count']==74 and v['no_physical_gap_monotonicity_assumed']
        extension=[r for r in current if r['certificate_route']=='stage12_frontier_interval_piece'];assert len(extension)==8
        assert min(F(r['gap_lower_exact']) for r in extension)==F(v['extension_uniform_gap'])
    return count

def save(fig,name,plt):
    fig.savefig(OUT/(name+'.png'),dpi=175,facecolor='white')
    fig.savefig(OUT/(name+'.pdf'),facecolor='white',metadata={'CreationDate':None,'ModDate':None})
    plt.close(fig)

def plot(data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    from matplotlib.lines import Line2D
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':15,'axes.labelsize':12,'xtick.labelsize':10,'ytick.labelsize':10,'pdf.fonttype':42,'savefig.bbox':'tight'})
    models=['alternating_spin1_chain','ordinary_spinhalf_bilayer','fully_frustrated_bilayer']
    fig,axes=plt.subplots(1,3,figsize=(17.6,6.3))
    for i,(ax,model,title) in enumerate(zip(axes,models,['Spin-1 alternating chain','Ordinary spin-1/2 bilayer','Near fully frustrated bilayer'])):
        ax.set_title(title,pad=14);ax.set_yscale('log');ax.spines[['top','right']].set_visible(False)
        ax.set_xlabel('Weak coupling g' if i<2 else 'Perturbation ε (J = 0.3)')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y,p:f'{y:g}'));ax.yaxis.set_minor_formatter(mticker.NullFormatter())
        ax.grid(axis='y',alpha=.13)
        for r in data['claims']:
            if r['model']!=model or not r['plotted_in_main_figure']:continue
            if model=='ordinary_spinhalf_bilayer' and r['parameter_kind']=='closed_interval' and (r.get('certificate_route')!=data['current_ordinary_interval_union_route'] or F(r['parameter_exact'])<F(data['current_ordinary_interval_endpoint'])):continue
            if r['parameter_kind']=='point' and any(a['model']==model and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'] and F(a['gap_lower_exact'])>F(r['gap_lower_exact']) for a in data['claims']):continue
            x=float(F(r['parameter_exact']));y=float(F(r['gap_lower_exact']))
            if r['parameter_kind']=='closed_interval':
                lo=float(F(r['parameter_lower_exact']))
                ax.plot([lo,x],[y,y],color=GREEN,lw=2.3,solid_capstyle='butt')
                ax.plot([lo,x],[y,y],ls='none',marker='|',color=GREEN,ms=9,mew=2)
            elif r['evidence_status'].startswith('root_scalar'):
                ax.scatter(x,y,marker='^',s=62,facecolors='white',edgecolors=ORANGE,linewidths=1.6,zorder=4)
            else:ax.scatter(x,y,color=BLUE,s=43,zorder=4)
            if i==0 and x in [.175]:
                dx,dy,ha=(0,13,'center')
                if x==.16125:dx,dy,ha=-5,-15,'right'
                if x==.175:dx,dy,ha=-8,2,'right'
                if x==.182:dx,dy,ha=4,-13,'left'
                ax.annotate(f'{x:g}',(x,y),xytext=(dx,dy),textcoords='offset points',ha=ha,va='center',fontsize=9,arrowprops={'arrowstyle':'-','lw':.6,'color':GRAY})
            if i==1 and r['parameter_kind']=='point' and x==.1:
                ax.annotate('0.10',(x,y),xytext=(0,10),textcoords='offset points',ha='center',fontsize=9)
        if i==0:
            ax.set_xlim(.038,.237);ax.set_ylim(.0007,.23);ax.set_xticks([.05,.10,.15,.20,.225]);ax.set_ylabel('Certified gap lower bound')
            ax.text(.03,.025,'Every integer cell count M ≥ 2',transform=ax.transAxes,fontsize=10)
        elif i==1:
            ax.set_xlim(-.004,.108);ax.set_ylim(.0011,.70);ax.set_xticks([0,.02,.04,.06,.08,.10] if data['combined_review_included'] else [0,.02,.04,.06,.07])
            ax.annotate(f"Entire 0 ≤ g ≤ {float(F(data['current_ordinary_interval_endpoint'])):g}"+'\nΔ ≥ 0.004499695659',(.036,.001945771244),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10,color=GREEN)
            ax.text(.03,.025,'Every integer square side L ≥ 2',transform=ax.transAxes,fontsize=10)
        else:
            ax.scatter(0,.4,marker='*',color=GRAY,s=115,zorder=4);ax.annotate('ε = 0: 0.4',(0,.4),xytext=(9,0),textcoords='offset points',va='center',fontsize=10)
            ax.set_xlim(-.0004,.0091);ax.set_ylim(.0004,.7);ax.set_xticks([0,.004,.008]);ax.text(.03,.025,'Every integer square side L ≥ 2',transform=ax.transAxes,fontsize=10)
    handles=[Line2D([],[],ls='none',marker='o',color=BLUE,label='Independently reviewed isolated point'),Line2D([],[],color=GREEN,lw=2.3,label='Proved uniform parameter interval'),Line2D([],[],ls='none',marker='^',mfc='white',mec=ORANGE,mew=1.6,label='Finite-size bridge with audited inputs'),Line2D([],[],ls='none',marker='*',color=GRAY,label='Analytic reference')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.08),ncol=2,frameon=False,fontsize=10)
    fig.text(.5,.045,'Dots are separate certificates. Bars certify every parameter in the shown interval. Plot scales are separate.',ha='center',fontsize=10)
    fig.text(.5,.010,'No monotonic physical-gap trend, phase boundary, or interpolation between isolated dots is inferred.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.065,right=.98,top=.89,bottom=.29,wspace=.32)
    save(fig,'certified_bounds',plt)

    pieces=sorted([r for r in data['claims'] if r.get('certificate_route') in data['current_ordinary_interval_piece_routes']],key=lambda r:F(r['parameter_lower_exact']))
    fig,ax=plt.subplots(figsize=(12.5,5.8))
    ax.set_title(f'Ordinary bilayer: all {len(pieces)} certified closed parameter pieces',pad=15)
    for i,r in enumerate(pieces):
        lo,hi,y=map(float,[F(r['parameter_lower_exact']),F(r['parameter_exact']),F(r['gap_lower_exact'])])
        color=ORANGE if lo>=.082 else GREEN
        ax.plot([lo,hi],[y,y],color=color,lw=2.8);ax.scatter([lo,hi],[y,y],s=19,color=color,zorder=3)
    u=max([r for r in data['claims'] if r.get('certificate_route')==data['current_ordinary_interval_union_route']],key=lambda r:F(r['parameter_exact']));v=float(F(u['gap_lower_exact']));hi=float(F(u['parameter_exact']))
    ax.plot([0,hi],[v,v],color=PURPLE,lw=2.3);ax.plot([0,hi],[v,v],marker='|',ms=11,mew=2,color=PURPLE,ls='none')
    ax.annotate('Uniform on the whole union: 0.004499695659',(.014,v),xytext=(0,12),textcoords='offset points',fontsize=11,color=PURPLE)
    ax.set_yscale('log');ax.set_ylim(.0012,.7);ax.set_xlim(-.001,hi+.001);ax.set_xticks([0,.01,.02,.03,.04,.05,.06,.07,.08,.09]+[float(F(data['current_ordinary_interval_endpoint']))]);ax.set_xlabel('Intralayer coupling g');ax.set_ylabel('Certified gap lower bound')
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y,p:f'{y:g}'));ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    fig.text(.5,.025,'Green: ground-only denominators through .082. Orange: complete smaller odd bands after .082. Every segment covers all integer L ≥ 2.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.10,right=.98,bottom=.16,top=.88)
    save(fig,'ordinary_interval_pieces',plt)

    fig,axes=plt.subplots(1,3,figsize=(18,6.5),gridspec_kw={'width_ratios':[1,1.2,1.1]})
    geometry=['4 × 4','8 × 4','8 × 8'];physical=[2**32,2**64,2**128]
    ax=axes[0];ax.barh(range(3),[float(v) for v in physical],color=BLUE,height=.48);ax.set_yticks(range(3),[f'{s} rungs\n{n} spins' for s,n in zip(geometry,[32,64,128])]);ax.invert_yaxis();ax.set_xscale('log');ax.set_xlim(1,float(2**143));ax.set_xticks([1,1e12,1e24,1e36]);ax.set_title('Physical Hilbert dimension',pad=15);ax.set_xlabel('Number of states (log scale)')
    for i,(n,v) in enumerate(zip([32,64,128],physical)):ax.text(v*1.8,i,f'2^{n}',va='center',fontsize=11)
    ax=axes[1];ys=[0,1,2]
    ax.barh([x-.24 for x in ys],[11,43,43],height=.21,color=BLUE,label='Ground / enlarged search')
    ax.barh(ys,[59,139,43],height=.21,color=PURPLE,label='Total trial space')
    ax.barh([x+.24 for x in ys],[49,97,1],height=.21,color=GREEN,label='Trace states / numerator contributions')
    ax.set_yticks(ys,geometry);ax.invert_yaxis();ax.set_xlim(0,150);ax.set_title('Accepted g = .10 pipeline',pad=15);ax.set_xlabel('Distinct linear / trace counts')
    for i,values in enumerate(zip([11,43,43],[59,139,43],[49,97,1])):
        for off,v in zip([-.24,0,.24],values):ax.text(v+2,i+off,str(v),va='center',fontsize=10)
    ax.legend(frameon=False,loc='upper center',fontsize=9,bbox_to_anchor=(.5,-.15))
    ax=axes[2];values=[1,29,43,193];labels=['One numerator contribution','Original ground search','Exact enlarged search (.10)','Separate full-band route']
    ax.barh(range(4),values,color=[GREEN,BLUE,PURPLE,GRAY],height=.45);ax.set_yticks(range(4),labels);ax.invert_yaxis();ax.set_xscale('log');ax.set_xlim(.8,430);ax.set_xticks([1,10,100]);ax.get_xaxis().set_major_formatter(mticker.ScalarFormatter());ax.set_xlabel('Different quantities (log scale)');ax.set_title('Largest 8 × 8 patch',pad=15)
    for i,v in enumerate(values):ax.text(v*1.1,i,str(v),va='center',fontsize=11)
    for ax in axes:ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.092,'Final denominator spaces: 11 + 48 = 59 and 43 + 96 = 139. Ground-only continuum reaches .082.',ha='center',fontsize=11)
    fig.text(.5,.052,'At g=.10 and in the [.09,.10] extension, the largest numerator uses a 43D search and one retained term.',ha='center',fontsize=11)
    fig.text(.5,.014,'The complete hard-core residual improves the 8 × 4 ground lower. Odd levels and complete omitted tails remain in the proof.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.073,right=.965,bottom=.34,top=.85,wspace=.87)
    save(fig,'trial_space_counts',plt)

    fig,ax=plt.subplots(figsize=(8.5,4.7))
    ax.plot([5,20],[.1,.1],color=GREEN,lw=2.5)
    ax.scatter([5],[.1],color=GREEN,s=45)
    ax.set(xlim=(2,20.5),ylim=(0,.14),xlabel='Periodic spin count L',ylabel='Certified gap lower bound',title='AKLT projector reference: every integer L ≥ 5')
    ax.set_xticks([2,5,10,15,20]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    ax.text(7,.108,'Δ ≥ 1/10; continues for every L ≥ 5',fontsize=11,color=GREEN)
    fig.text(.5,.025,'H = ΣP₂; unique ground for L ≥ 3. D = 2 MPS. Separate finite-size projector proof, not thermal bootstrap.',ha='center',fontsize=9)
    fig.subplots_adjust(left=.12,bottom=.19,top=.85,right=.97);save(fig,'aklt_reference_scope',plt)

    fig,ax=plt.subplots(figsize=(9.5,5))
    rs=data['recipe_upper_envelopes'];ax.scatter([r['denominator_length'] for r in rs],[float(F(r['upper_cap_exact'])) for r in rs],color=ORANGE,s=65)
    for r in rs:ax.annotate(r['upper_cap_exact'],(r['denominator_length'],float(F(r['upper_cap_exact']))),xytext=(0,10),textcoords='offset points',ha='center')
    ax.set(xlim=(5,13),ylim=(0,.88),xlabel='Denominator length n (microscopic spins)',ylabel='Upper cap on recipe J lower bound',title='Fixed D26 one-Rayleigh recipe: all-temperature obstructions')
    ax.set_xticks([6,8,10,12]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.text(.5,.065,'n = 6/8: specified delayed canonical conversions fail. n = 10/12: first G update fails.',ha='center',fontsize=10)
    fig.text(.5,.022,'These are recipe upper caps, not physical-purity upper bounds or gap bounds. No all-method minimum seed.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.12,right=.97,bottom=.22,top=.86);save(fig,'recipe_upper_caps',plt)
    fig,ax=plt.subplots(figsize=(10,5.5))
    labels=['3 orthogonal states (core)','4 states (+ longitudinal)','48 states (+ momentum)','70 states (+ exact lowering)']
    windows=[('13/2','45/4'),('31/4','11'),('533/64','679/64'),('539/64','339/32')]
    for i,(lo,hi) in enumerate(windows):
        a,b=float(F(lo)),float(F(hi));ax.plot([a,b],[i,i],lw=7,color=PURPLE,solid_capstyle='butt')
        ax.text((a+b)/2,i-.16,f'[{lo}, {hi}]',ha='center',fontsize=10)
    ax.set_yticks(range(4),labels);ax.invert_yaxis();ax.set_ylim(3.5,-.5)
    ax.set_xlim(6,11.7);ax.set_xlabel('Inverse temperature β (unit exchange)')
    ax.set_title('Historical n = 24 screens, before current-witness completion',pad=15)
    ax.spines[['top','right','left']].set_visible(False);ax.grid(axis='x',alpha=.15)
    fig.text(.5,.075,'Outside each interval, the specified fixed D26 one-Rayleigh recipe is excluded for all β ≥ 0.',ha='center',fontsize=10)
    fig.text(.5,.028,'Historical windows are superseded: the sealed current-witness review excludes the specified old recipe for all β.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.31,right=.98,bottom=.23,top=.87);save(fig,'mps_recipe_windows',plt)
    fig,axes=plt.subplots(1,2,figsize=(12.5,5.5))
    ax=axes[0];rs=[r for r in data['claims'] if r['snapshot_stage']=='stage11']
    ax.scatter([float(F(r['parameter_exact'])) for r in rs],[float(F(r['gap_lower_exact'])) for r in rs],s=65,color=BLUE)
    for r in rs:ax.annotate(f"{float(F(r['gap_lower_exact'])):.9f}",(float(F(r['parameter_exact'])),float(F(r['gap_lower_exact']))),xytext=(0,12),textcoords='offset points',ha='center')
    ax.set(xlim=(.204,.231),ylim=(.035,.135),xlabel='Isolated coupling g',ylabel='Certified gap lower bound',title='All integer M ≥ 2')
    ax.set_xticks([.21,.22,.225]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    ax=axes[1];ax.plot([2,16],[.01,.01],color=ORANGE,lw=3);ax.scatter([2,16],[.01,.01],color=ORANGE,s=45)
    ax.set(xlim=(1,20),ylim=(0,.018),xlabel='Integer cell count M',ylabel='Certified gap lower bound',title='g = .25: finite sizes only')
    ax.set_xticks([2,8,16,20]);ax.text(9,.0113,'Δ ≥ .01 only for 2 ≤ M ≤ 16',ha='center',fontsize=10,color=ORANGE)
    ax.text(18,.004,'No all-size\ncertificate',ha='center',fontsize=10);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.suptitle('Direct time-first integer windows: independently proved scopes',y=.99)
    fig.text(.5,.025,'Inherited reviewed inputs. This chain-window review supplies no coupling interval or uniform-chain gap.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.08,right=.97,top=.83,bottom=.19,wspace=.35);save(fig,'chain_window_refinement',plt)
    fig,ax=plt.subplots(figsize=(12,5.5));ns=data['stage11_mps_direct_window']['verdict']['separately_checked_n']
    ax.scatter(ns,[1]*len(ns),marker='x',s=90,linewidths=2,color=ORANGE)
    for n in ns:ax.annotate(str(n),(n,1),xytext=(0,13),textcoords='offset points',ha='center')
    ax.set(xlim=(5,25),ylim=(.5,1.5),xlabel='Denominator microscopic length n',title='Uniform spin-1: every even n = 6,…,24 separately screened')
    ax.set_xticks(ns);ax.set_yticks([]);ax.spines[['top','right','left']].set_visible(False)
    ax.text(15,.73,'All permitted continuation paths fail, even granting every finite-size bridge.',ha='center',fontsize=11)
    fig.text(.5,.16,'Fixed D26 one-Rayleigh numerator; specified whole time-first delays and accepted canonical / same-base sufficient closure.',ha='center',fontsize=10)
    fig.text(.5,.10,'At n24: current trial difference ≈ .4238202243; 70/73 denominator states; current-combination MPS bond ≤156.',ha='center',fontsize=10)
    fig.text(.5,.035,'This is a recipe obstruction, not a physical-gap bound, universal necessity of P ≥ .99, or all-method minimum seed.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.07,right=.98,top=.82,bottom=.30);save(fig,'accepted_recipe_scope',plt)
    fig,ax=plt.subplots(figsize=(11,5.8));cs=sorted(data['uniform_large_size_certificates'],key=lambda r:r['integer_size_min'])
    colors=[GREEN,GRAY,BLUE,PURPLE]
    for r,color in zip(cs,colors):
        n=r['integer_size_min'];g=float(F(r['gap_lower_exact']));ax.plot([n,120],[g,g],color=color,lw=2.6)
        ax.scatter([n],[g],color=color,s=55);ax.annotate('',xy=(122,g),xytext=(118,g),arrowprops={'arrowstyle':'->','color':color,'lw':2.6})
        ax.text(n+4,g+.00035,f"Δ ≥ {g:g}, every integer L ≥ {n}",color=color,fontsize=11)
    ax.set(xlim=(48,124),ylim=(0,.012),xlabel='Periodic microscopic spin count L',ylabel='Certified gap lower bound',title='Uniform spin-1 Heisenberg chain: independently accepted gaps')
    ax.set_xticks([48,52,56,60,80,100,120]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    ax.axvspan(48,52,color=GRAY,alpha=.07);ax.text(49.8,.006,'No claim\nbelow 52',rotation=90,ha='center',va='center',fontsize=9,color=GRAY)
    fig.text(.5,.065,'Unit bilinear exchange; all integers, including odd L. The strongest bound on overlaps may be selected.',ha='center',fontsize=10)
    fig.text(.5,.025,'D26 single-Rayleigh numerators at lengths 104/108/112/120. No optimality or minimum-seed claim.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.1,right=.97,top=.86,bottom=.22);save(fig,'uniform_gap_frontier',plt)
    if data['stage12_source_scope_included']:
        comparisons=data['stage12_source_scope']['verdict']['comparisons']
        fig,ax=plt.subplots(figsize=(11,5.8));values=[float(F(c['original_gap_interval'][0])) for c in comparisons]+[.0102,.0038]
        labels=['Original theorem\neven L ≥ 60','Original theorem\neven L ≥ 2304','Accepted new bound\nall integer L ≥ 60','Accepted n52 bound\nall integer L ≥ 52']
        ax.bar(range(4),values,color=[GRAY,GRAY,PURPLE,GREEN],width=.58)
        for i,v in enumerate(values):ax.text(i,v*1.12,('≈ ' if i<2 else '')+f'{v:.12f}'.rstrip('0'),ha='center',fontsize=10)
        ax.set_yscale('log');ax.set_ylim(.0003,.021);ax.set_xticks(range(4),labels);ax.set_ylabel('Certified gap lower bound, unit exchange')
        ax.set_title('Uniform spin-1: comparison with the pinned original theorem',pad=16);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
        fig.text(.5,.065,'The .0102 lower bound is ≈21.28584× and ≈2.66940× the two original lower bounds, on their overlapping scopes.',ha='center',fontsize=10)
        fig.text(.5,.025,'Ratios compare sufficient certified bounds, not physical-gap estimates. Original final theorem: even lengths only.',ha='center',fontsize=10)
        fig.subplots_adjust(left=.11,right=.97,top=.86,bottom=.24);save(fig,'uniform_theorem_comparison',plt)
    if data['stage12_frontier_point_included']:
        fig,ax=plt.subplots(figsize=(10.5,5.5));rs=[r for r in data['claims'] if r.get('certificate_route') in ['bilayer_direct_time_first_point','bilayer_frontier_above010_point']]
        ax.scatter([float(F(r['parameter_exact'])) for r in rs],[float(F(r['gap_lower_exact'])) for r in rs],s=55,color=BLUE)
        for r in rs:
            f=F(r['gap_lower_exact']);six=f.numerator*10**6//f.denominator
            ax.annotate(f"{six//10**6}.{six%10**6:06d}",(float(F(r['parameter_exact'])),float(f)),xytext=(0,-20 if r['parameter_exact']=='1001/10000' else 12),textcoords='offset points',ha='center',fontsize=9)
        if data['stage12_frontier_interval_included']:
            g=float(F(data['stage12_frontier_interval']['verdict']['extension_uniform_gap']));ax.plot([.1,.102],[g,g],color=GREEN,lw=2.7);ax.text(.1009,g-.003,'Entire [.10,.102]: Δ ≥ .013574634391',ha='center',color=GREEN,fontsize=10)
        ax.set(xlim=(.09985,.10215),ylim=(.006,.068),xlabel='Intralayer coupling g',ylabel='Certified gap lower bound',title='Ordinary bilayer: independently accepted frontier points')
        ax.set_xticks([.1000,.1005,.1010,.1015,.1020]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
        fig.text(.5,.05,'Every integer square side L ≥ 2. Points are separate certificates; their trend is not a physical-gap estimate.',ha='center',fontsize=10)
        fig.text(.5,.012,'Six-decimal point labels are rounded downward. Exact certificate values are retained in the data.',ha='center',fontsize=9)
        fig.subplots_adjust(left=.11,right=.97,top=.86,bottom=.19);save(fig,'bilayer_frontier',plt)
    return matplotlib.__version__

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');ap.add_argument('--output-dir');args=ap.parse_args()
    if args.output_dir:OUT=Path(args.output_dir).resolve();OUT.mkdir(parents=True,exist_ok=True)
    elif not args.check_only:assert not (HERE/'MANIFEST_SHA256.json').exists(), 'Frozen snapshot: use --output-dir'
    data=json.loads((HERE/'overview_data.json').read_text());n=verify(data)
    info={'status':'PASS','claims':len(data['claims']),'finite_size_certificate_rows':len(data['finite_size_certificates']),'uniform_large_size_certificate_rows':len(data['uniform_large_size_certificates']),'dimension_rows':len(data['dimensions']),'direct_source_hashes':len(data['sources']),'review_seals':len(data['review_seals']),'sealed_file_hashes_checked':n,'combined_review_included':data['combined_review_included'],'interval_extension_included':data['interval_extension_included'],'cpu_affinity':sorted(os.sched_getaffinity(0)),'address_space_limit_bytes':1024**3,'blas_threads':1,'checks':['source SHA-256','complete selected review manifests','all exact gap JSON pointers','all decimal floors','best point selection','all exact adjacent closed pieces and uniform minimum','Hilbert dimensions','numerator rank separated from search and filtered span','failure gaps remain null','all 207 chain candidate routes','all exact interval pieces','59/139 denominator trial dimensions','reference67 versus unchanged M8 search','70 orthogonal MPS states with bond52 and necessary screen only','g010 diagnostic scope without gap promotion','separate AKLT projector reference','all stage11 files and 228 prior certificate rows preserved', 'finite-size g025 kept separate', 'pair symmetry erratum', '74-integer current and even/direct recipe scopes', 'four unique-ground uniform gaps with explicit minima52/54/56/60 including odd lengths', 'historical66 pieces preserved; current74-piece interval through .102', 'new direct point and fixed-family metadata erratum', 'original source n>=4 scope and theorem comparison', 'rank195 fixed early-window obstruction and strict decimal direction']}
    if not args.check_only:
        info['matplotlib']=plot(data);info['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (OUT/'validation.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info))
