"""Stage22 extraction and integrity checks; no physical or scalar research is run."""
from common import *
H2='uniform_alternating_h2_review'
INTERVAL='uniform_alternating_variance_refined_robustness_review'
LAUNCH='bilayer_full_m4_launch_review'
WATCHDOG='bilayer_full_m4_watchdog_review'
STREAM='bilayer_streaming_startup_review'
TERMINAL='bilayer_m4_checkpoint100_terminal_review'
CHECK100='bilayer_m4_checkpoint100_review'
REPAIR='bilayer_stable_observer_review'
REPAIR_JOB='c2c9f79a9d55bbc0867f3ef38103d54cb98fc44c185adc280360ca25a969fd01'
FAIL_REVIEW='bilayer_streaming_observer_failure_review'
FAILED='bilayer_full_m4_production_run'
FAILED_SEAL='0dd76472806a818c4489fac4b093b7636468dc33771bbb0c8fa6ae3b9875aa32'
LAUNCH_JOB='8bd34794ff776ba9222058c06ade5c76ffd85515518dbc7462d8fc7e49b21a14'
OLD_JOB='db32cbc51cf71726756f7910921ef26b684e6c3020a8e8f0a0e5eecd17d24556'
NEW_JOB='845b55d815552ca70bb870f0efd6be20a94850f952e63a87dc7a0338553e8a0e'

def scope():
    return dict(uniform_all_integer_physical_gap='31/1250',smallest_genuine_uniform_initialization=30,uniform_coverage_from=2,new_uniform_gap=False,new_bilayer_gap=False,new_thermal_campaign=False,full8x4_high_moments_accepted=False,active_successor_files_included=False,streaming_gate_job_id=NEW_JOB,streaming_actual_status='FAILED_AFTER63_COMMITS',streaming_specific_failure_cause_proven=False,proposed_clean_generation_partition=dict(standard=16800,control=1800,retry=3000),required_control_carry=716,required_retired_worker_retry_charge=492,current_production_gate='FAIL_PENDING_INCOMPLETE_IDENTITY_REPAIR',terminal_failure_included=True,repaired_gate_job_id=REPAIR_JOB,repaired_gate_review_accepted=True,repaired_runtime_checkpoint_included=True,maximum_independently_reviewed_committed_chunks=100,checkpoint400_included=False,no_q6_cost_evidence=True,pending_new_repairs_excluded=True,successor_initial_cap_reported_by_root=100,successor_initial_authority_reported_utc='2026-10-11 05:11 UTC',all_stage_transitions_need_separate_token=True,physical24_retains_parity_MPS48=True,original_failed_job_zero_workers=True,original_failed_control_charge_retained=220,latest_remote_main_before_snapshot='2d31755efbf0637cb15579ae52d4138b19326ab4',latest_remote_main_verified_utc='2026-10-11T05:01:48Z',user_research_hard_cutoff_utc='2026-10-14T00:00:00Z')

def engineering_rows():
    return [
        dict(component='accepted57D controls and bounded outer launch',review=LAUNCH,job_id=LAUNCH_JOB,status='PASS scoped controls and startup; external wall watchdog still missing at this historical seal',reserved_review_CPU=[30],physical_workers=0,full_moments_accepted=False,new_gap=False,accepted57D_m012=True,initial_cap=100,separate_stage_tokens=[100,400,2945]),
        dict(component='external startup watchdog',review=WATCHDOG,job_id=OLD_JOB,status='PASS exact pinned bounded staged-launch gate; no authority created by review',reserved_review_CPU=[5],physical_workers=0,full_moments_accepted=False,new_gap=False,accepted57D_m012=True,initial_cap=100,separate_stage_tokens=[100,400,2945]),
        dict(component='streaming full-pin startup correction',review=STREAM,job_id=NEW_JOB,status='PASS actual three verifier cutpoints and final26 pins under AS64; fresh authority and precharge required',reserved_review_CPU=[10,8],physical_workers=0,full_moments_accepted=False,new_gap=False,accepted57D_m012=True,initial_cap=100,separate_stage_tokens=[100,400,2945]),
        dict(component='stable observer and checksum-preserving correction',review=REPAIR,job_id=REPAIR_JOB,status='PASS bounded observer tests and final28-pin AS64 startup; no full lifetime or scientific result',reserved_review_CPU=[8,6],physical_workers=0,full_moments_accepted=False,new_gap=False,accepted57D_m012=True,initial_cap=100,separate_stage_tokens=[100,400,2945])
    ]

def build_stage22(data):
    sources=data['sources'];inherited=dict(sources);oldpkgs={str(Path(p).parent) for p in inherited if p.endswith('/MANIFEST_SHA256.json')};deps={};seen=set()
    def pin(p,h=None):
        assert not Path(p).is_absolute() and '..' not in Path(p).parts,p
        a=sha(ROOT/p)
        if h is not None:assert a==h,(p,h,a)
        if p in sources:assert sources[p]==a,('existing source drift',p)
        sources[p]=a;deps[p]=a
        if p in inherited or any(p.startswith(q+'/') for q in oldpkgs) or '/snapshot/' in p:return
        if p in seen:return
        seen.add(p)
        if p.endswith(('/INPUT_SHA256.json','/SCALAR_INPUT_SHA256.json')):
            for q,h in json.loads((ROOT/p).read_text()).items():pin(q,h)
        if p.endswith(('/MANIFEST_SHA256.json','/FAILED_START_MANIFEST_SHA256.json')) and len(Path(p).parts)==3:
            m=json.loads((ROOT/p).read_text());m=m.get('files',m)
            for q,h in m.items():pin(str(Path(p).parent/q),h)
    pins=json.loads((HERE/'stage22_review_pins.json').read_text());assert set(pins)=={H2,INTERVAL,LAUNCH,WATCHDOG,STREAM,FAIL_REVIEW,REPAIR,CHECK100,TERMINAL}
    data['stage22_review_pins']=pins;data['stage22_evidence']={}
    for d,h in pins.items():
        p=R+d+'/MANIFEST_SHA256.json';pin(p,h);n=manifest_check(p)
        data['review_seals'].append(dict(directory=R+d,manifest=p,sha256=h,verified_files=n))
        f='scalar_results.json' if d==H2 else 'results.json' if d==INTERVAL else 'correction/CHECKS.json' if d==STREAM else 'CHECKS.json' if d==FAIL_REVIEW else 'REVIEW.json' if d==REPAIR else 'CHECKS.json' if d in [CHECK100,TERMINAL] else 'STATUS.json'
        p=R+d+'/'+f;data['stage22_evidence'][d]=dict(primary_source=p,source_sha256=sources[p],verdict=json.loads((ROOT/p).read_text()))
    for q in json.loads((ROOT/(R+H2+'/PRODUCER_PINS.json')).read_text()).values():pin(q['path']+'/MANIFEST_SHA256.json',q['manifest'])
    pin(R+'uniform_alternating_h2_design/MANIFEST_SHA256.json')
    pin(R+'bilayer_streaming_hash_revision/MANIFEST_SHA256.json','88aa9e771ab91a958d43a339a9bbd96e627240f2ca82cdc0d4234ddf0908fbee')
    pin(R+FAILED+'/FAILED_START_MANIFEST_SHA256.json',FAILED_SEAL)
    data['stage22_dependencies']=dict(sorted(deps.items()));(HERE/'STAGE22_DEPENDENCIES.json').write_text(json.dumps(data['stage22_dependencies'],indent=2)+'\n')
    data['stage22_observables']=[];v=data['stage22_evidence'][H2]['verdict'];p=R+H2+'/scalar_results.json'
    for i,c in enumerate(v['rows']):
        L=c['physical_length'];data['stage22_observables'].append(dict(id='stage22_H2_'+str(L),model='untwisted_periodic_uniform_spin1_Heisenberg',unit_bilinear_exchange=1,physical_sites=L,physical_Hilbert_dimension=3**L,MPS_bond_dimension=26,trial_span_dimension=1,norm_transfer_dimension=676,charge_blocks=11,total_variance_exact=c['variance_exact'],total_variance_decimal_down_12=floor12(c['variance_exact']),variance_convention='H2/N-(H/N)^2; total energy; no extra L',normalized_beta='49/4',finite_gap_lower=c['finite_gap_lower'],finite_gap_is_all_size=False,shifted_ground_energy_lower=c['E0_shifted_lower'],Rayleigh_ground_weight_lower=c['Rayleigh_ground_weight_lower'],energy_only_infidelity_upper=c['energy_only_infidelity_upper'],pairwise_variance_infidelity_upper=c['pairwise_variance_infidelity_upper'],fidelity_lower=c['fidelity_lower'],small_root_branch='independently proved F>1/2 before variance inversion',Gibbs_kappa_upper_exact=c['simple_Gibbs_kappa_upper'],Gibbs_kappa_fine_upper=c['Gibbs_kappa_upper'],observable='A_L=B_L^2/(3L/2)^2',bound_type='physical uniform Gibbs expectation',new_all_size_interval=False,new_thermal_computation=False,primary_source=p,primary_json_pointer=f'/rows/{i}/variance_exact',primary_sha256=sources[p]))
    data['stage22_refined_intervals']=[];v=data['stage22_evidence'][INTERVAL]['verdict'];p=R+INTERVAL+'/results.json'
    for i,c in enumerate(v['rows']):
        row=dict(data['stage21_finite_intervals'][i]);row.update(id='stage22_variance_refined_'+str(i),parameter_lower_exact=c['g_closed_interval'][0],parameter_upper_exact=c['g_closed_interval'][1],eta_radius=c['eta_radius'],gap_lower_exact=c['gap'],gap_lower_decimal_down_12=floor12(c['gap']),kappa32_upper='969/10000',kappa64_upper='119/1000',terminal_cell_base=c['terminal_cells_from'],explicit_bootstrap_windows=len(c['windows']),primary_source=p,primary_json_pointer=f'/rows/{i}/gap',primary_sha256=sources[p]);data['stage22_refined_intervals'].append(row)
    data['stage22_engineering_scope']=engineering_rows()
    p=R+FAILED+'/FAILED_PREINNER.json';v=json.loads((ROOT/p).read_text());data['stage22_failed_jobs']=[dict(v,source=p,source_sha256=sources[p],sealed_failure_manifest=R+FAILED+'/FAILED_START_MANIFEST_SHA256.json',sealed_failure_manifest_sha256=FAILED_SEAL)]
    v=data['stage22_evidence'][FAIL_REVIEW]['verdict']
    data['stage22_failure_summary']=[dict(job_id=OLD_JOB,status='FAILED_PREINNER',committed_chunks=0,worker_charge=0,control_charge=220,total_charge=220,cause_proven=True,scope='MemoryError in whole-file startup pin hashing; no physical worker',primary_source=R+FAILED+'/FAILED_PREINNER.json'),dict(job_id=NEW_JOB,status='FAILED_OBSERVER_AFTER63_COMMITS',committed_chunks=v['committed_chunks'],worker_charge=v['worker_charge'],control_charge=v['control_charge'],total_charge=v['total_charge'],cause_proven=v['exact_failure_cause_proven'],scope='Partial receipt/accounting PASS; production FAIL pending observer repair',primary_source=R+FAIL_REVIEW+'/CHECKS.json')]
    v=data['stage22_evidence'][CHECK100]['verdict'];data['stage22_checkpoint100']=[dict(job_id=v['job'],checkpoint_digest=v['checkpoint_digest'],committed_chunks=v['committed'],q0_targets=v['coverage']['0'],q2_targets=v['coverage']['2'],q4_targets=v['coverage']['4'],q6_targets=v['coverage']['6'],all24_signed_chains_verified=v['all24_signed_chains_verified'],first63_values_equal_preserved_prior_generation=v['first63_values_equal_preserved_prior_generation'],retired_worker_charges=v['retired_worker_charges'],worker_charged=v['worker_charged'],control_charged=v['control_charged'],total_charged=v['total_charged'],verified_role_map_available=v['verified_role_map_available'],idle_evidence=v['idle_evidence'],no_q6_cost_sample=v['no_q6_cost_sample'],full_moments=v['full_moments'],review_wrote_token=v['token_written'],review_scientific_workers_launched=v['scientific_workers_launched'],primary_source=R+CHECK100+'/CHECKS.json')]
    v=data['stage22_evidence'][TERMINAL]['verdict']
    data['stage22_terminal100']=[dict(job_id=v['job'],checkpoint_digest=v['checkpoint'],authorized_token_cap=v['authorized_token_cap'],actual_committed=v['actual_committed'],no_new_scientific_receipts=v['no_new_scientific_receipts'],coverage=v['coverage'],worker_charge=v['worker_charge'],control_charge=v['control_charge'],total_charge=v['total_charge'],unchanged_scientific_and_checkpoint_files=v['unchanged_scientific_and_checkpoint_files'],both_locks_available_and_held=v['both_locks_available_and_held'],namespace_caveat=v['namespace_caveat'],verified_roles=v['verified_roles'],vacuum_runtime_identity_sampled=False,interpretation=v['interpretation'],new_launch_authorized_by_review=v['new_launch_authorized_by_review'],new_physics_or_fork_tests=False,full_moments=False,checkpoint400_exists=False,primary_source=R+TERMINAL+'/CHECKS.json')]
    data['stage22_failure_summary'].append(dict(job_id=REPAIR_JOB,status='FAILED_RESUME100_WITH_INCOMPLETE_ARGV',committed_chunks=100,worker_charge=492,control_charge=716,total_charge=1208,cause_proven=False,scope='Classifier rejection of incomplete argv reproduced; reason for empty argv unproven; no new science',primary_source=R+TERMINAL+'/CHECKS.json') )
    data['stage22_scope']=scope()

def verify_stage22(data):
    assert data['stage22_scope']==scope()
    assert data['stage22_engineering_scope']==engineering_rows()
    assert data['stage22_review_pins']==json.loads((HERE/'stage22_review_pins.json').read_text())
    assert data['stage22_dependencies']==json.loads((HERE/'STAGE22_DEPENDENCIES.json').read_text())
    for p,h in data['preserved_stage21_files'].items():assert sha(ROOT/p)==h
    for p,h in data['stage22_dependencies'].items():assert data['sources'][p]==h and sha(ROOT/p)==h
    assert not any(R+'bilayer_full_m4_production_run_streaming/' in p for p in data['sources'])
    for r in data['stage22_evidence'].values():assert r['source_sha256']==data['sources'][r['primary_source']] and r['verdict']==json.loads((ROOT/r['primary_source']).read_text())
    for key in ['stage22_observables','stage22_refined_intervals','stage22_engineering_scope','stage22_failed_jobs','stage22_failure_summary','stage22_checkpoint100','stage22_terminal100']:
        rows=list(csv.DictReader((HERE/(key+'.csv')).open()));expected=[{k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else str(v) if v is not None else '' for k,v in r.items()} for r in data[key]];assert rows==expected,(key,'CSV mismatch')
    assert len(data['stage22_observables'])==2
    for i,r in enumerate(data['stage22_observables']):
        c=data['stage22_evidence'][H2]['verdict']['rows'][i];L=c['physical_length']
        assert r['physical_sites']==L and L in [32,64] and r['physical_Hilbert_dimension']==3**L and r['MPS_bond_dimension']==26 and r['trial_span_dimension']==1 and r['norm_transfer_dimension']==676 and r['charge_blocks']==11
        assert r['total_variance_exact']==c['variance_exact'] and r['total_variance_decimal_down_12']==floor12(c['variance_exact']) and F(c['variance_exact'])>=0
        assert r['variance_convention']=='H2/N-(H/N)^2; total energy; no extra L' and r['small_root_branch']=='independently proved F>1/2 before variance inversion'
        for a,b in [('finite_gap_lower','finite_gap_lower'),('shifted_ground_energy_lower','E0_shifted_lower'),('Rayleigh_ground_weight_lower','Rayleigh_ground_weight_lower'),('energy_only_infidelity_upper','energy_only_infidelity_upper'),('pairwise_variance_infidelity_upper','pairwise_variance_infidelity_upper'),('fidelity_lower','fidelity_lower'),('Gibbs_kappa_upper_exact','simple_Gibbs_kappa_upper'),('Gibbs_kappa_fine_upper','Gibbs_kappa_upper')]:assert r[a]==c[b]
        assert F(r['Rayleigh_ground_weight_lower'])>F('1/2') and 0<F(r['pairwise_variance_infidelity_upper'])<F(r['energy_only_infidelity_upper'])<F('1/2')
        assert F(r['fidelity_lower'])==1-F(r['pairwise_variance_infidelity_upper'])
        assert F(r['Gibbs_kappa_fine_upper'])<F(r['Gibbs_kappa_upper_exact']) and r['Gibbs_kappa_upper_exact']=={32:'969/10000',64:'119/1000'}[L]
        assert r['finite_gap_lower']=={32:'1783/8000',64:'19681/100000'}[L] and not r['finite_gap_is_all_size'] and not r['new_all_size_interval'] and not r['new_thermal_computation']
        assert r['bound_type']=='physical uniform Gibbs expectation' and r['observable']=='A_L=B_L^2/(3L/2)^2' and r['normalized_beta']=='49/4'
        assert ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer'])==r['total_variance_exact'] and r['primary_sha256']==data['sources'][r['primary_source']]
    rows=data['stage22_refined_intervals'];v=data['stage22_evidence'][INTERVAL]['verdict'];assert len(rows)==4 and not v['physical_work'] and v['search_candidates_not_replayed']
    assert [r['eta_radius'] for r in rows]==['751/5000000','2089/10000000','99/400000','109/400000']
    assert [r['gap_lower_exact'] for r in rows]==['1/50','3/200','1/100','1/200'] and [r['explicit_bootstrap_windows'] for r in rows]==[10,9,9,9]
    for i,r in enumerate(rows):
        c=v['rows'][i];eta=F(r['eta_radius']);old=data['stage21_finite_intervals'][i]
        modified={'id','parameter_lower_exact','parameter_upper_exact','eta_radius','gap_lower_exact','gap_lower_decimal_down_12','kappa32_upper','kappa64_upper','terminal_cell_base','explicit_bootstrap_windows','primary_source','primary_json_pointer','primary_sha256'}
        for k,value in old.items():
            if k not in modified:assert r[k]==value
        assert r['kappa32_upper']=='969/10000' and r['kappa64_upper']=='119/1000' and eta>F(old['eta_radius'])
        assert [r['parameter_lower_exact'],r['parameter_upper_exact']]==c['g_closed_interval'] and F(r['parameter_lower_exact'])==(1-eta)/(1+eta) and F(r['parameter_upper_exact'])==(1+eta)/(1-eta)
        assert r['gap_lower_exact']==c['gap'] and r['gap_lower_decimal_down_12']==floor12(c['gap'])
        assert r['terminal_cell_base']==c['terminal_cells_from'] and r['explicit_bootstrap_windows']==len(c['windows']) and F(c['terminal_margin'])>0
        assert r['primary_sha256']==data['sources'][r['primary_source']] and ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer'])==r['gap_lower_exact']
        assert c['windows'][0]['cells'][0]==16 and c['windows'][-1]['cells'][1]>=c['terminal_cells_from']
        for j,w in enumerate(c['windows']):
            assert w['physical_even_lengths']==[2*k for k in w['cells']] and F(w['margin'])>0
            if j:assert c['windows'][j-1]['cells'][1]==w['cells'][0]
        assert [b['physical_length'] for b in c['finite_bridge_rows']]==list(range(4,31,2)) and [b['cell_length'] for b in c['finite_bridge_rows']]==list(range(2,16))
        assert all(F(b['gap_lower'])>F(c['gap']) and F(b['direct_margin'])>0 for b in c['finite_bridge_rows'])
        assert c['bottleneck_physical_length']==24 and F(c['finite_bridge_gap_lower'])==min(F(b['gap_lower']) for b in c['finite_bridge_rows'])
    v=data['stage22_evidence'][STREAM]['verdict'];assert v['status']=='PASS_ALL_THREE_REAL_STARTUPS_FINAL26_PINS_AS64' and v['job_id']==NEW_JOB and v['read_block_bytes']==65536 and v['total_hash_reads']==1605 and v['python_binary_bytes']==30894944
    assert v['old_failed_control_charge']==220 and v['successor_standard_control_total']==1130 and v['remaining_control_margin']==70 and v['unchanged_global_CPU_cap']==21600
    assert v['no_physical_workers'] and v['no_real_authority_or_ledger_created'] and len(v['contexts'])==3 and v['large_pin_mutation_rejected']
    for c in v['contexts']:assert c['pins']==26 and c['limits']['address_space']==[64*1024**2,128*1024**2] and c['memory']['VmPeak']==40042496
    v=data['stage22_evidence'][WATCHDOG]['verdict'];assert v['job_id']==OLD_JOB and v['initial_cap']==100 and v['only_stage_transitions']==[[100,400],[400,2945]] and v['no_physical_workers'] and v['full_physical_moments']=='NOT_COMPUTED'
    v=data['stage22_evidence'][LAUNCH]['verdict'];assert v['controls']=='PASS_FULL57D_EXACT' and v['no_physical_workers'] and v['charged_cpu_seconds']==30
    assert json.loads((ROOT/(R+LAUNCH+'/PROPOSED_JOB_ID.json')).read_text())['job_id']==LAUNCH_JOB
    v=data['stage22_evidence'][FAIL_REVIEW]['verdict'];assert v['status']=='PASS_PARTIAL_RECEIPT_AND_FAILURE_ACCOUNTING' and v['production_gate']=='FAIL_REQUIRES_OBSERVER_REPAIR' and not v['full_moments'] and not v['exact_failure_cause_proven']
    assert v['committed_chunks']==63 and v['covered_targets']=={'0':1,'2':496,'4':864,'6':0} and v['uncommitted_reserved_attempt']==63
    assert v['worker_charge']==192 and v['control_charge']==463 and v['total_charge']==655 and v['locks_available'] and v['no_matching_processes']==[]
    assert v['all24_signed_accumulators_preserved'] and v['new_partition_proposal']==dict(standard=16800,control=1600,retry=3200,retired_workers=192,control_carry=463,control_forecast=1373,retry_remaining=3008)
    assert data['stage22_failure_summary']==[dict(job_id=OLD_JOB,status='FAILED_PREINNER',committed_chunks=0,worker_charge=0,control_charge=220,total_charge=220,cause_proven=True,scope='MemoryError in whole-file startup pin hashing; no physical worker',primary_source=R+FAILED+'/FAILED_PREINNER.json'),dict(job_id=NEW_JOB,status='FAILED_OBSERVER_AFTER63_COMMITS',committed_chunks=63,worker_charge=192,control_charge=463,total_charge=655,cause_proven=False,scope='Partial receipt/accounting PASS; production FAIL pending observer repair',primary_source=R+FAIL_REVIEW+'/CHECKS.json'),dict(job_id=REPAIR_JOB,status='FAILED_RESUME100_WITH_INCOMPLETE_ARGV',committed_chunks=100,worker_charge=492,control_charge=716,total_charge=1208,cause_proven=False,scope='Classifier rejection of incomplete argv reproduced; reason for empty argv unproven; no new science',primary_source=R+TERMINAL+'/CHECKS.json')]
    v=data['stage22_evidence'][REPAIR]['verdict'];assert v['status']=='PASS_OBSERVER_CORRECTION_AND_SCOPED_BUDGET_DELTA' and v['job']==REPAIR_JOB and v['pins']==28
    assert v['source_seal']=='6b810258d0d4f593d6d19308b5d19690dedde8d69ac721e9554b6dff66cc9d5a' and v['actual_startup_cutpoints']==['outer','supervisor','controller'] and v['actual_AS']==[64*1024**2,128*1024**2]
    for k in ['true_bad_CPU_rejected','true_bad_AS_rejected','injected_bad_affinity_rejected','read_crossing_exec_deferred','same_identity_limit_change_rechecked','mismatch_diagnostics_persisted','all_test_children_reaped','restored193600_nonzero_n8_checked','no_physical_worker']:assert v[k]
    assert v['barrier_cases']==3 and v['control_carry']==463 and v['worker_carry']==192 and v['global_cap']==21600 and v['control_pool']==1600 and v['retry_pool']==3200 and v['retry_remaining']==3008 and v['control_forecast']==1373
    assert not v['production_authority_created'] and not v['full_lifecycle_tested'] and not v['full_scientific_result'] and v['review_reservations']==dict(failed_pin_count=8,corrected=6,total=14)
    v=data['stage22_evidence'][CHECK100]['verdict'];assert v['status']=='PASS_INITIAL100_CHECKPOINT_FOR_ROOT_CONTINUATION_DECISION' and v['job']==REPAIR_JOB and v['committed']==100 and v['coverage']=={'0':1,'2':496,'4':1456,'6':0}
    assert v['checkpoint_digest']=='01d7a5098422a5dcb210fff8c77782e57099ff439e9e49b4b323cba06aea2418' and v['worker_charged']==492 and v['control_charged']==711 and v['total_charged']==1203 and v['retired_worker_charges']==192
    assert v['all24_signed_chains_verified'] and v['first63_values_equal_preserved_prior_generation'] and v['no_q6_cost_sample'] and not v['verified_role_map_available'] and not v['full_moments'] and not v['token_written'] and v['scientific_workers_launched']==0
    assert data['stage22_checkpoint100']==[dict(job_id=v['job'],checkpoint_digest=v['checkpoint_digest'],committed_chunks=v['committed'],q0_targets=v['coverage']['0'],q2_targets=v['coverage']['2'],q4_targets=v['coverage']['4'],q6_targets=v['coverage']['6'],all24_signed_chains_verified=v['all24_signed_chains_verified'],first63_values_equal_preserved_prior_generation=v['first63_values_equal_preserved_prior_generation'],retired_worker_charges=v['retired_worker_charges'],worker_charged=v['worker_charged'],control_charged=v['control_charged'],total_charged=v['total_charged'],verified_role_map_available=v['verified_role_map_available'],idle_evidence=v['idle_evidence'],no_q6_cost_sample=v['no_q6_cost_sample'],full_moments=v['full_moments'],review_wrote_token=v['token_written'],review_scientific_workers_launched=v['scientific_workers_launched'],primary_source=R+CHECK100+'/CHECKS.json')]
    v=data['stage22_evidence'][TERMINAL]['verdict'];assert v['status']=='PASS_TERMINAL_EVIDENCE_GATE_FAIL_PENDING_INCOMPLETE_IDENTITY_REPAIR' and v['job']==REPAIR_JOB and v['checkpoint']==data['stage22_checkpoint100'][0]['checkpoint_digest']
    assert v['authorized_token_cap']==400 and v['actual_committed']==100 and v['no_new_scientific_receipts'] and v['coverage']==dict(q0=1,q2=496,q4=1456,q6=0)
    assert v['worker_charge']==492 and v['control_charge']==716 and v['total_charge']==1208 and v['unchanged_scientific_and_checkpoint_files']==1021 and v['both_locks_available_and_held']
    assert v['verified_roles']==dict(native=99,supervisor=1,controller=1,external_watchdog=1) and v['verified_native_chunk_ids']==list(range(1,100))
    f=v['failed_tuple'];assert f['before']['argv']==f['after']['argv']==[] and f['before']['exe']==f['after']['exe'] and f['cpu']==[3,20] and f['address_space']==[64*1024**2,128*1024**2] and f['affinity']=='6' and f['expected_role']=='supervisor'
    assert v['old_control_forecast_without_new_launcher']==1383 and v['old_control_forecast_with_new_launcher']==1603 and v['old_control_pool']==1600
    assert v['proposed_new_partition']==dict(standard=16800,control=1800,retry=3000,retired_workers=492,remaining_retry=2508,control_forecast=1626,control_spare=174)
    assert v['no_new_physics_or_fork_tests'] and not v['new_launch_authorized_by_review']
    assert data['stage22_terminal100']==[dict(job_id=v['job'],checkpoint_digest=v['checkpoint'],authorized_token_cap=v['authorized_token_cap'],actual_committed=v['actual_committed'],no_new_scientific_receipts=v['no_new_scientific_receipts'],coverage=v['coverage'],worker_charge=v['worker_charge'],control_charge=v['control_charge'],total_charge=v['total_charge'],unchanged_scientific_and_checkpoint_files=v['unchanged_scientific_and_checkpoint_files'],both_locks_available_and_held=v['both_locks_available_and_held'],namespace_caveat=v['namespace_caveat'],verified_roles=v['verified_roles'],vacuum_runtime_identity_sampled=False,interpretation=v['interpretation'],new_launch_authorized_by_review=v['new_launch_authorized_by_review'],new_physics_or_fork_tests=False,full_moments=False,checkpoint400_exists=False,primary_source=R+TERMINAL+'/CHECKS.json')]
    assert len(data['stage22_failed_jobs'])==1;r=data['stage22_failed_jobs'][0];v=json.loads((ROOT/r['source']).read_text())
    for k,val in v.items():assert r[k]==val
    assert r['state']=='FAILED_PREINNER' and r['job_id']==OLD_JOB and r['workers_dispatched']==0 and r['inner_sessions_started']==0 and r['charged_control']==220 and r['next_generation_must_carry_control_charge']==220 and not r['retry_performed'] and r['wait4_cpu_unavailable']
    assert r['source_sha256']==data['sources'][r['source']] and r['sealed_failure_manifest_sha256']==FAILED_SEAL and sha(ROOT/r['sealed_failure_manifest'])==FAILED_SEAL

def plot_stage22(data,plt,save):
    colors=['#2e7d49','#245f8b','#735291','#b85c21'];fig,axes=plt.subplots(1,2,figsize=(13.5,6.2));ax=axes[0]
    for r,col in zip(data['stage22_refined_intervals'],colors):
        gap=float(F(r['gap_lower_exact']));ax.plot([float(F(r['parameter_lower_exact'])),float(F(r['parameter_upper_exact']))],[gap,gap],color=col,lw=3.5);ax.scatter([float(F(r['parameter_lower_exact'])),float(F(r['parameter_upper_exact']))],[gap,gap],color=col,s=26);ax.text(1,gap+.0008,f'Δ ≥ {gap:g}',ha='center',color=col,fontsize=11)
    ax.axvline(1,color='#5c6570',ls=':',lw=.7);ax.set(xlim=(.9994,1.0006),ylim=(0,.025),xlabel='Alternating bond coefficient g',ylabel='Certified gap lower bound',title='Accepted variance-refined closed intervals');ax.ticklabel_format(axis='x',style='plain',useOffset=False);ax.set_xticks([.9995,.99975,1,1.00025,1.0005]);ax.tick_params(axis='x',labelrotation=25)
    ax=axes[1]
    for key,label,col,marker in [('stage21_finite_intervals','Stage 21: B² + finite bridge','#7a838b','o'),('stage22_refined_intervals','Stage 22: H²-refined fidelity','#2e7d49','D')]:
        rows=data[key];ax.scatter([float(F(r['eta_radius']))*1e6 for r in rows],[float(F(r['gap_lower_exact'])) for r in rows],color=col,marker=marker,label=label,s=40)
    ax.set(xlim=(115,290),ylim=(0,.025),xlabel='Certified η radius r × 10⁶',ylabel='Certified gap lower bound',title='Certified targets, without interpolation');ax.legend(loc='upper right',fontsize=8)
    for ax in axes:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.text(.5,.095,'Every integer cell M ≥ 2; physical L = 2M; unit designated bond; unique finite-volume ground state.',ha='center',fontsize=10)
    fig.text(.5,.054,'Physical Gibbs κ32 ≤ .0969, κ64 ≤ .119. One D26 trial vector; independently verified F > 1/2 branch.',ha='center',fontsize=10)
    fig.text(.5,.014,'37 windows + 56 finite bridges + four tails. Physical 24 retains parity/MPS48. No optimal-width or odd-physical-size claim.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.07,right=.97,bottom=.25,top=.88,wspace=.25);save(fig,'stage22_variance_refined_frontier',plt)
