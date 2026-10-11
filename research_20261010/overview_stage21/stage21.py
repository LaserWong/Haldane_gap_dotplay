"""Stage21 exact scoped extraction, dependency closure and corruption checks."""
from common import *
BASE_SEAL='de1e346d56f73dc638dba23e97845b8767ed9c6d3b85fe2f609642551e28b853'
B2='uniform_alternating_b2_fixture_review'
FIRST='uniform_alternating_second_moment_robustness_review'
FINAL='uniform_alternating_second_moment_finite_bridge_review'
CONTROL='bilayer_incremental_control_first_review'
FINAL_CONTROL='bilayer_variable_g_control_review'
RESTRICTED='alternating_restricted_cell_seed_proposal'
RESTRICTED_SEAL='867d8d01f6936f6acb3f3c5584a5319dc53e2496c33533f5249ac910132f81ac'

def build_stage21(data):
    sources=data['sources'];inherited_sources=dict(sources);inherited_packages={str(Path(p).parent) for p in sources if p.endswith('/MANIFEST_SHA256.json')};seals=data['review_seals'];deps={};seen=set()
    def pin(p,h=None):
        assert not Path(p).is_absolute() and '..' not in Path(p).parts,p
        actual=sha(ROOT/p)
        if h is not None:assert actual==h,('dependency mismatch',p,h,actual)
        if p in sources:assert sources[p]==actual,('inherited pin changed',p)
        sources[p]=actual;deps[p]=actual
        if p in inherited_sources or any(p.startswith(d+'/') for d in inherited_packages) or '/snapshot/' in p:return # Exact inherited evidence or documentary snapshot boundary; Stage20 seal/transport checks remain active.
        if p in seen:return
        seen.add(p)
        if p.endswith('/INPUT_SHA256.json'):
            q=json.loads((ROOT/p).read_text())
            assert isinstance(q,dict)
            for name,digest in q.items():
                assert isinstance(digest,str) and len(digest)==64,(p,name)
                pin(name,digest)
        if p.endswith('/MANIFEST_SHA256.json') and len(Path(p).parts)==3:
            q=json.loads((ROOT/p).read_text());q=q.get('files',q)
            for name,digest in q.items():pin(str(Path(p).parent/name),digest)
    pins=json.loads((HERE/'stage21_review_pins.json').read_text())
    assert all(x in pins for x in [B2,FIRST,FINAL,CONTROL,FINAL_CONTROL]),'Wait for final immutable finite-purity review.'
    data['stage21_review_pins']=pins;data['stage21_evidence']={}
    for directory,h in pins.items():
        p=R+directory+'/MANIFEST_SHA256.json';pin(p,h);n=manifest_check(p)
        seals.append(dict(directory=R+directory,manifest=p,sha256=h,verified_files=n))
        f='CLAIM_VERDICTS.json' if directory==B2 else 'BENCHMARK.json' if directory==CONTROL else 'STATUS.json' if directory==FINAL_CONTROL else 'results.json'
        p=R+directory+'/'+f
        data['stage21_evidence'][directory]=dict(primary_source=p,source_sha256=sources[p],verdict=json.loads((ROOT/p).read_text()))
    pin(R+RESTRICTED+'/MANIFEST_SHA256.json',RESTRICTED_SEAL)
    data['stage21_dependencies']=dict(sorted(deps.items()))
    (HERE/'STAGE21_DEPENDENCIES.json').write_text(json.dumps(data['stage21_dependencies'],indent=2)+'\n')
    v=data['stage21_evidence'][B2]['verdict'];data['stage21_observables']=[]
    for L in [32,64]:
        data['stage21_observables'].append(dict(id='stage21_gibbs_B2_'+str(L),model='untwisted_periodic_uniform_spin1_Heisenberg',physical_sites=L,physical_Hilbert_dimension=3**L,MPS_bond_dimension=26,trial_span_dimension=1,norm_transfer_dimension=676,all_virtual_charge_blocks=11,normalized_beta='49/4',observable='A_L=B_L^2/(3L/2)^2',bound_type='upper bound in physical uniform Gibbs state',kappa_upper_exact=v['physical']['kappa'+str(L)+'_upper'],new_all_size_gap_claim=False,H2_production_at32_or64=False,thermal_spectral_truncation=False,primary_source=R+B2+'/CLAIM_VERDICTS.json',primary_json_pointer='/physical/kappa'+str(L)+'_upper',primary_sha256=sources[R+B2+'/CLAIM_VERDICTS.json']))
    for directory,key,route in [(FIRST,'stage21_first_intervals','coarse all-size .0248 finite Weyl bridge'),(FINAL,'stage21_finite_intervals','length-resolved finite-purity bridge')]:
        p=R+directory+'/results.json';v=data['stage21_evidence'][directory]['verdict'];data[key]=[]
        for i,c in enumerate(v['rows']):
            data[key].append(dict(id=key+'_'+str(i),model='periodic_alternating_spin1_chain',Hamiltonian='sum_j[h_(2j-1)+g*h_(2j)]',designated_first_bond_coefficient=1,parameter_lower_exact=c['g_closed_interval'][0],parameter_upper_exact=c['g_closed_interval'][1],eta_radius=c['eta_radius'],gap_lower_exact=c['gap'],gap_lower_decimal_down_12=floor12(c['gap']),integer_cell_min=c['cells_from'],all_integer_cells=True,physical_site_count='2M',physical_Hilbert_dimension='3^(2M)=9^M',unique_ground_state=c['unique_ground_state'],initialization_cells=16,initialization_physical_sites=32,physical_anchor_sites=64,physical_anchor_Hilbert_dimension=3**64,MPS_bond_dimension=26,trial_span_dimension=1,normalized_beta='49/4',physical_inverse_temperature='beta/c; c=(1+g)/2',kappa32_upper='17/125',kappa64_upper='157/1000',finite_bridge_cells=[2,15],finite_bridge_route=route,terminal_cell_base=c['terminal_cells_from'],explicit_bootstrap_windows=len(c['windows']),new_physical_computation=False,optimal_neighborhood_claim=False,odd_physical_lengths_claim=False,primary_source=p,primary_json_pointer=f'/rows/{i}/gap',primary_sha256=sources[p]))
    data['stage21_engineering_scope']=[dict(component='first incremental-control review',synthetic_records=2945,synthetic_nonphysical=True,fresh_metadata_assembly_pass=True,committed_restart_output_digest_binding=False,production_gate='FAIL',physical_memory_profile_tested=False,full8x4_moments_computed=False,new_gap=False,full_production_authorized=False,primary_source=R+CONTROL+'/BENCHMARK.json',finding=R+CONTROL+'/FINDING.md')]
    data['stage21_component_scope']=[dict(component='final numerical24 and corrected-control review',component_pass=True,complete_small_dense_fixtures=6,exact_variable_g_pencils=30,fields_per_accumulator=24,physical_K_denominator='22*g_den',physical_J_denominator='(22*g_den)^2',actual8x4_vacuum_targets=1,complete8x4_chunks_required=2945,corrected_control_checks=26,producer_revised_AS_profile_MiB=[64,64,128],producer_revised_profile_evidence_reviewed=True,independent_complete8x4_sweep=False,production_launch_gate='BLOCKED_TWO_EXPLICIT_PRELAUNCH_CONDITIONS',missing_external_accounted_startup_guard=True,missing_independent_accepted57D_m012_controls=True,production_resource_authorization_present=False,new_gap=False,full8x4_moments_computed=False,separate_no_refund_reserved_CPU=[90,8,8],preserved_failed_reviewer_checks=2,first25_parent_CPU_separately_metered=False,all2945_raw_synthetic_records_in_manifest=False,primary_source=R+FINAL_CONTROL+'/STATUS.json',review=R+FINAL_CONTROL+'/FINAL_REVIEW.md')]
    p=R+RESTRICTED+'/STATUS.json';v=json.loads((ROOT/p).read_text())
    data['stage21_restricted_producer_status']=dict(primary_source=p,source_sha256=sources[p],verdict=v)
    data['stage21_unaccepted_findings']=[dict(component='restricted-cell seed producer proposal',producer_manifest=R+RESTRICTED+'/MANIFEST_SHA256.json',producer_manifest_sha256=RESTRICTED_SEAL,independently_accepted=False,mathematical_status=v['mathematical_status'],resource_status=v['resource_status'],actual_child_cpu_seconds=v['actual_child_cpu_seconds'],charged_cpu_seconds_including_reserves=v['charged_cpu_seconds_including_reserves'],authorized_cpu_seconds=v['authorized_cpu_seconds'],cell_seeds_tested=v['cell_seeds_tested'],all_size_bootstrap_closed=False,g09_certified=False,new_gap=False,failure_is_universal_nogo=False)]
    data['stage21_scope']=dict(uniform_all_physical_L_ge2_gap='31/1250',bilayer_new_gap=False,full8x4_m4_accepted=False,full_production_authorized=False,active_bilayer24_control_files_included=False,final_bilayer_component_review_included=True,active_outer_launch_files_included=False,restricted_seed_independently_accepted=False,restricted_seed_resource_compliance_accepted=False,new_thermal_campaign=False,smallest_genuine_uniform_initialization=30,physical24_uses_parity_and_MPS48=True,finite_purity_interval_count=4,first_second_moment_interval_count=4,user_research_hard_cutoff_utc='2026-10-14T00:00:00Z',latest_remote_main_before_snapshot='47a0c919d8c32f65e564ff7a5453a6eca3efd60c',latest_remote_main_verified_utc='2026-10-11T03:52:34Z')

def verify_stage21(data):
    assert data['stage21_dependencies']==json.loads((HERE/'STAGE21_DEPENDENCIES.json').read_text())
    for p,h in data['preserved_stage20_files'].items():assert sha(ROOT/p)==h
    for p,h in data['stage21_dependencies'].items():assert data['sources'][p]==h and sha(ROOT/p)==h
    assert data['stage21_review_pins']==json.loads((HERE/'stage21_review_pins.json').read_text())
    for directory,h in data['stage21_review_pins'].items():assert data['sources'][R+directory+'/MANIFEST_SHA256.json']==h
    for r in data['stage21_evidence'].values():assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
    for key in ['stage21_observables','stage21_first_intervals','stage21_finite_intervals','stage21_engineering_scope','stage21_component_scope','stage21_unaccepted_findings']:
        rows=list(csv.DictReader((HERE/(key+'.csv')).open()))
        expected=[{k:(json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else str(v) if v is not None else '') for k,v in r.items()} for r in data[key]]
        assert rows==expected,('Stage21 CSV mismatch',key)
    v=data['stage21_evidence'][B2]['verdict'];assert v['status']=='ACCEPTED' and v['resource']=='PASS_WITH_PRESERVED_PREEXEC_COMPILE_FAILURE_AND_EXPLICITLY_AUTHORIZED_CORRECTION'
    assert len(v['historical_issues'])==2 and len(v['not_claimed'])==4
    assert len(data['stage21_observables'])==2
    for r,L,kappa in zip(data['stage21_observables'],[32,64],['17/125','157/1000']):
        assert r['physical_sites']==L and r['physical_Hilbert_dimension']==3**L and r['MPS_bond_dimension']==26 and r['trial_span_dimension']==1
        assert r['norm_transfer_dimension']==676 and r['all_virtual_charge_blocks']==11 and r['normalized_beta']=='49/4' and r['kappa_upper_exact']==kappa
        assert r['bound_type']=='upper bound in physical uniform Gibbs state' and r['observable']=='A_L=B_L^2/(3L/2)^2'
        assert not r['new_all_size_gap_claim'] and not r['H2_production_at32_or64'] and not r['thermal_spectral_truncation']
        assert ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer'])==kappa and r['primary_sha256']==data['sources'][r['primary_source']]
    expected_radii=[['6/112525','49/450075','37/225025','99/450025'],['1291/10000000','227/1250000','2159/10000000','37/156250']]
    for j,(key,directory) in enumerate([('stage21_first_intervals',FIRST),('stage21_finite_intervals',FINAL)]):
        rows=data[key];v=data['stage21_evidence'][directory]['verdict'];assert len(rows)==4
        assert [r['eta_radius'] for r in rows]==expected_radii[j] and [r['gap_lower_exact'] for r in rows]==['1/50','3/200','1/100','1/200']
        for i,r in enumerate(rows):
            c=v['rows'][i];eta=F(r['eta_radius'])
            assert r['gap_lower_exact']==c['gap'] and r['gap_lower_decimal_down_12']==floor12(c['gap']) and F(r['gap_lower_exact'])>0
            assert [r['parameter_lower_exact'],r['parameter_upper_exact']]==c['g_closed_interval']
            assert F(r['parameter_lower_exact'])==(1-eta)/(1+eta) and F(r['parameter_upper_exact'])==(1+eta)/(1-eta)
            assert r['integer_cell_min']==2 and r['all_integer_cells'] and r['unique_ground_state'] and r['designated_first_bond_coefficient']==1
            assert r['physical_site_count']=='2M' and r['physical_Hilbert_dimension']=='3^(2M)=9^M' and r['initialization_cells']==16 and r['initialization_physical_sites']==32
            assert r['physical_anchor_sites']==64 and r['physical_anchor_Hilbert_dimension']==3**64 and r['MPS_bond_dimension']==26 and r['trial_span_dimension']==1
            assert r['normalized_beta']=='49/4' and r['physical_inverse_temperature']=='beta/c; c=(1+g)/2'
            assert r['kappa32_upper']=='17/125' and r['kappa64_upper']=='157/1000' and r['finite_bridge_cells']==[2,15]
            assert not r['new_physical_computation'] and not r['optimal_neighborhood_claim'] and not r['odd_physical_lengths_claim']
            assert r['primary_sha256']==data['sources'][r['primary_source']] and ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer'])==r['gap_lower_exact']
            assert r['explicit_bootstrap_windows']==len(c['windows']) and r['terminal_cell_base']==c['terminal_cells_from']
            assert c['windows'][0]['cells'][0]==16 and c['windows'][-1]['cells'][1]>=c['terminal_cells_from'] and F(c['terminal_margin'])>0
            for k,w in enumerate(c['windows']):
                assert w['physical_even_lengths']==[2*m for m in w['cells']] and F(w['margin'])>0
                if k:assert c['windows'][k-1]['cells'][1]==w['cells'][0]
            if not j:assert c['finite_bridge_gap_lower']==c['gap'] and F(c['finite_bridge_margin_exact'])==0
            else:
                assert F(r['eta_radius'])>F(data['stage21_first_intervals'][i]['eta_radius'])
                assert [b['physical_length'] for b in c['finite_bridge_rows']]==list(range(4,31,2))
                assert [b['cell_length'] for b in c['finite_bridge_rows']]==list(range(2,16))
                assert all(F(b['gap_lower'])>F(c['gap']) and F(b['direct_margin'])>0 for b in c['finite_bridge_rows'])
                assert c['bottleneck_physical_length']==24 and F(c['finite_bridge_gap_lower'])==min(F(b['gap_lower']) for b in c['finite_bridge_rows'])
        assert sum(r['explicit_bootstrap_windows'] for r in rows)==[22,39][j]
    v=json.loads((ROOT/(R+FINAL+'/CLAIM_VERDICTS.json')).read_text());assert v['status']=='ACCEPTED' and v['resource']=='PASS' and v['no_optimality_claim'] and not v['new_physical_computation']
    assert v['conservative_review_CPU_seconds_with_three_full_sealing_reserves']==24.081720854 and v['separate_all_compile_CPU_seconds']==16.872037073
    r=data['stage21_restricted_producer_status'];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
    v=r['verdict'];assert v['resource_status']=='NOT_ACCEPTED' and F(v['charged_cpu_seconds_including_reserves'])==F('30.697826')>F(v['authorized_cpu_seconds'])==30
    assert not v['g_0_9_seed_certified'] and not v['restricted_uniform_seed_closed'] and v['scientific_computation_stopped']
    v=data['stage21_unaccepted_findings'][0];assert not v['independently_accepted'] and not v['all_size_bootstrap_closed'] and not v['g09_certified'] and not v['new_gap'] and not v['failure_is_universal_nogo']
    assert v['producer_manifest_sha256']==RESTRICTED_SEAL and v['resource_status']=='NOT_ACCEPTED' and v['charged_cpu_seconds_including_reserves']=='30.697826' and v['authorized_cpu_seconds']=='30'
    assert data['stage21_engineering_scope']==[dict(component='first incremental-control review',synthetic_records=2945,synthetic_nonphysical=True,fresh_metadata_assembly_pass=True,committed_restart_output_digest_binding=False,production_gate='FAIL',physical_memory_profile_tested=False,full8x4_moments_computed=False,new_gap=False,full_production_authorized=False,primary_source=R+CONTROL+'/BENCHMARK.json',finding=R+CONTROL+'/FINDING.md')]
    assert data['stage21_component_scope']==[dict(component='final numerical24 and corrected-control review',component_pass=True,complete_small_dense_fixtures=6,exact_variable_g_pencils=30,fields_per_accumulator=24,physical_K_denominator='22*g_den',physical_J_denominator='(22*g_den)^2',actual8x4_vacuum_targets=1,complete8x4_chunks_required=2945,corrected_control_checks=26,producer_revised_AS_profile_MiB=[64,64,128],producer_revised_profile_evidence_reviewed=True,independent_complete8x4_sweep=False,production_launch_gate='BLOCKED_TWO_EXPLICIT_PRELAUNCH_CONDITIONS',missing_external_accounted_startup_guard=True,missing_independent_accepted57D_m012_controls=True,production_resource_authorization_present=False,new_gap=False,full8x4_moments_computed=False,separate_no_refund_reserved_CPU=[90,8,8],preserved_failed_reviewer_checks=2,first25_parent_CPU_separately_metered=False,all2945_raw_synthetic_records_in_manifest=False,primary_source=R+FINAL_CONTROL+'/STATUS.json',review=R+FINAL_CONTROL+'/FINAL_REVIEW.md')]
    v=data['stage21_evidence'][FINAL_CONTROL]['verdict'];assert v['component_review']=='PASS' and v['production_launch_gate']=='BLOCKED_TWO_EXPLICIT_PRELAUNCH_CONDITIONS' and len(v['conditions'])==2 and not v['new_physical_result']
    q=json.loads((ROOT/(R+FINAL_CONTROL+'/PHYSICAL24_CHECKS.json')).read_text());assert len(q['physical_reference_cases'])==6 and sum(r['variable_g_matrices'] for r in q['physical_reference_cases'])==30 and q['physical_K_denominator']=='22*g_den' and q['physical_J_denominator']=='(22*g_den)^2'
    q=json.loads((ROOT/(R+FINAL_CONTROL+'/control_checks_final/CHECKS.json')).read_text());assert len(q['checks'])==26
    assert data['stage21_scope']==dict(uniform_all_physical_L_ge2_gap='31/1250',bilayer_new_gap=False,full8x4_m4_accepted=False,full_production_authorized=False,active_bilayer24_control_files_included=False,final_bilayer_component_review_included=True,active_outer_launch_files_included=False,restricted_seed_independently_accepted=False,restricted_seed_resource_compliance_accepted=False,new_thermal_campaign=False,smallest_genuine_uniform_initialization=30,physical24_uses_parity_and_MPS48=True,finite_purity_interval_count=4,first_second_moment_interval_count=4,user_research_hard_cutoff_utc='2026-10-14T00:00:00Z',latest_remote_main_before_snapshot='47a0c919d8c32f65e564ff7a5453a6eca3efd60c',latest_remote_main_verified_utc='2026-10-11T03:52:34Z')

def plot_stage21(data,plt,save):
    colors=['#2e7d49','#245f8b','#735291','#b85c21']
    fig,axes=plt.subplots(1,2,figsize=(13.5,6.2));ax=axes[0]
    for r,col in zip(data['stage21_finite_intervals'],colors):
        lo=float(F(r['parameter_lower_exact']));hi=float(F(r['parameter_upper_exact']));gap=float(F(r['gap_lower_exact']))
        ax.plot([lo,hi],[gap,gap],color=col,lw=3.5);ax.scatter([lo,hi],[gap,gap],color=col,s=26)
        ax.text(1,gap+.0008,f'Δ ≥ {gap:g}',ha='center',color=col,fontsize=11)
    ax.axvline(1,color='#5c6570',ls=':',lw=.7)
    ax.set(xlim=(.99946,1.00054),ylim=(0,.025),xlabel='Alternating bond coefficient g',ylabel='Certified gap lower bound',title='Accepted length-resolved finite-purity bridge')
    ax.ticklabel_format(axis='x',style='plain',useOffset=False);ax.set_xticks([.9995,.99975,1,1.00025,1.0005]);ax.tick_params(axis='x',labelrotation=25)
    ax=axes[1]
    for key,label,col,marker in [('stage20_positive_cell_certificates','Stage20 positive-cell','#8b9299','o'),('stage21_first_intervals','B² + coarse finite bridge','#245f8b','s'),('stage21_finite_intervals','B² + finite purities','#2e7d49','D')]:
        rows=data[key][:4];ax.scatter([float(F(r['eta_radius']))*1e6 for r in rows],[float(F(r['gap_lower_exact'])) for r in rows],color=col,marker=marker,label=label,s=40)
    ax.set(xlim=(30,255),ylim=(0,.025),xlabel='Certified η radius r × 10⁶',ylabel='Certified gap lower bound',title='Certified targets, without interpolation');ax.legend(loc='upper right',fontsize=8)
    for ax in axes:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.text(.5,.095,'Every integer cell M ≥ 2; physical sites L = 2M. Unique finite-volume ground state; unit designated first bond.',ha='center',fontsize=10)
    fig.text(.5,.054,'Physical Gibbs κ32 ≤ .136, κ64 ≤ .157; D26 / one trial vector. Cell 16 seed, physical 64 anchor, β = 49/4.',ha='center',fontsize=10)
    fig.text(.5,.014,'39 exact windows and 14 finite lengths per row. Physical 24 uses parity/MPS48. No optimal radius or odd-physical-size claim.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.07,right=.97,bottom=.25,top=.88,wspace=.25);save(fig,'stage21_second_moment_frontier',plt)
