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
    assert data['snapshot_label']=='stage10'
    assert {s['manifest']:s['sha256'] for s in data['review_seals']}==accepted
    for p,h in data['sources'].items():assert sha(ROOT/p)==h,('source changed',p)
    for p,h in data['preserved_stage9_files'].items():assert sha(ROOT/p)==h,('stage6 changed',p)
    count=0
    for seal in data['review_seals']:
        assert sha(ROOT/seal['manifest'])==seal['sha256']
        n=manifest_check(seal['manifest']);assert n==seal['verified_files'];count+=n
    rows=data['claims'];assert len({r['id'] for r in rows})==len(rows)
    previous=json.loads((ROOT/(R+'overview_stage9/overview_data.json')).read_text())
    lookup={r['id']:r for r in rows}
    for old in previous['claims']:
        new=lookup[old['id']]
        for k in ['gap_lower_exact','primary_source','primary_json_pointer','evidence_status','certificate_route','parameter_exact','parameter_lower_exact','integer_size_min','unit_coupling','boundary']:
            assert new.get(k)==old.get(k),('prior alternative changed',old['id'],k)
    assert len(data['dimensions'])>=len(previous['dimensions'])
    for i,old in enumerate(previous['dimensions']):
        assert all(data['dimensions'][i].get(k)==v for k,v in old.items())
    for name in ['tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv']:
        assert sha(HERE/name)==sha(ROOT/(R+'overview_stage9/'+name))
    for r in rows:
        assert F(ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer']))==F(r['gap_lower_exact'])
        assert r['primary_sha256']==data['sources'][r['primary_source']]
        assert floor12(r['gap_lower_exact'])==r['gap_lower_decimal_down_12']
        assert F(r['gap_lower_exact'])>0 and r['integer_size_min']==2
        assert r['proof_family']=='thermal_bootstrap'
        if r['snapshot_stage'] in ['stage7','stage8','stage9','stage10']:
            src=json.loads((ROOT/r['primary_source']).read_text())
            assert F(ptr(src,r['parameter_source_pointer']))==F(r['parameter_exact'])
            if r['parameter_kind']=='closed_interval':assert F(ptr(src,r['parameter_lower_source_pointer']))==F(r['parameter_lower_exact'])
        if r['parameter_kind']=='point' and r['plotted_in_main_figure']:
            assert all(F(r['gap_lower_exact'])>=F(a['gap_lower_exact']) for a in rows if a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'])
        if r['model']=='ordinary_spinhalf_bilayer':assert F(r['parameter_exact'])<=F('1/10')
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
    assert len(previous['claims'])==212
    for old in previous['claims']:
        assert lookup[old['id']]==old, ('stage8 row not preserved',old['id'])
    assert len(rows)==(225 if data['interval_range_010_included'] else 213)
    assert [r for r in pieces if r['snapshot_stage']!='stage10']==[r for r in previous['claims'] if r.get('certificate_route') in previous['ordinary_interval_piece_routes']]
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
            ax.annotate(f"Entire 0 ≤ g ≤ {float(F(data['ordinary_interval_endpoint'])):g}"+'\nΔ ≥ 0.001945771244',(.036,.001945771244),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10,color=GREEN)
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

    pieces=sorted([r for r in data['claims'] if r.get('certificate_route') in data['ordinary_interval_piece_routes']],key=lambda r:F(r['parameter_lower_exact']))
    fig,ax=plt.subplots(figsize=(12.5,5.8))
    ax.set_title(f'Ordinary bilayer: all {len(pieces)} certified closed parameter pieces',pad=15)
    for i,r in enumerate(pieces):
        lo,hi,y=map(float,[F(r['parameter_lower_exact']),F(r['parameter_exact']),F(r['gap_lower_exact'])])
        color=ORANGE if lo>=.082 else GREEN
        ax.plot([lo,hi],[y,y],color=color,lw=2.8);ax.scatter([lo,hi],[y,y],s=19,color=color,zorder=3)
    u=max([r for r in data['claims'] if r.get('certificate_route')=='uniform_interval_union'],key=lambda r:F(r['parameter_exact']));v=float(F(u['gap_lower_exact']));hi=float(F(u['parameter_exact']))
    ax.plot([0,hi],[v,v],color=PURPLE,lw=2.3);ax.plot([0,hi],[v,v],marker='|',ms=11,mew=2,color=PURPLE,ls='none')
    ax.annotate('Uniform on the whole union: 0.001945771244',(.014,v),xytext=(0,12),textcoords='offset points',fontsize=11,color=PURPLE)
    ax.set_yscale('log');ax.set_ylim(.0012,.7);ax.set_xlim(-.001,hi+.001);ax.set_xticks([0,.01,.02,.03,.04,.05,.06,.07]+[float(F(data['ordinary_interval_endpoint']))]);ax.set_xlabel('Intralayer coupling g');ax.set_ylabel('Certified gap lower bound')
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
    ax.set_title('Uniform spin-1 chain, n = 24: unresolved recipe screens',pad=15)
    ax.spines[['top','right','left']].set_visible(False);ax.grid(axis='x',alpha=.15)
    fig.text(.5,.075,'Outside each interval, the specified fixed D26 one-Rayleigh recipe is excluded for all β ≥ 0.',ha='center',fontsize=10)
    fig.text(.5,.028,'Inside is inconclusive: no actual startup, gap certificate, physical-purity bound or universal seed minimum.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.31,right=.98,bottom=.23,top=.87);save(fig,'mps_recipe_windows',plt)
    return matplotlib.__version__

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');ap.add_argument('--output-dir');args=ap.parse_args()
    if args.output_dir:OUT=Path(args.output_dir).resolve();OUT.mkdir(parents=True,exist_ok=True)
    elif not args.check_only:assert not (HERE/'MANIFEST_SHA256.json').exists(), 'Frozen snapshot: use --output-dir'
    data=json.loads((HERE/'overview_data.json').read_text());n=verify(data)
    info={'status':'PASS','claims':len(data['claims']),'dimension_rows':len(data['dimensions']),'direct_source_hashes':len(data['sources']),'review_seals':len(data['review_seals']),'sealed_file_hashes_checked':n,'combined_review_included':data['combined_review_included'],'interval_extension_included':data['interval_extension_included'],'cpu_affinity':sorted(os.sched_getaffinity(0)),'address_space_limit_bytes':1024**3,'blas_threads':1,'checks':['source SHA-256','complete selected review manifests','all exact gap JSON pointers','all decimal floors','best point selection','all exact adjacent closed pieces and uniform minimum','Hilbert dimensions','numerator rank separated from search and filtered span','failure gaps remain null','all 207 chain candidate routes','all exact interval pieces','59/139 denominator trial dimensions','reference67 versus unchanged M8 search','70 orthogonal MPS states with bond52 and necessary screen only','g010 diagnostic scope without gap promotion','separate AKLT projector reference','all stage9 files and 212 prior certificate rows preserved', 'g010 complete residual and 66-piece interval', 'rank195 fixed early-window obstruction and strict decimal direction']}
    if not args.check_only:
        info['matplotlib']=plot(data);info['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (OUT/'validation.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info))
