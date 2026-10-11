#!/usr/bin/env python3
"""Exact extraction checks, source seal verification, and reproducible static plots."""
import sys; sys.dont_write_bytecode=True
from common import *
import argparse,tempfile
os.environ['MPLCONFIGDIR']=tempfile.mkdtemp(prefix='haldane-stage8-mpl-')
os.environ['XDG_CACHE_HOME']=os.environ['MPLCONFIGDIR']
OUT=HERE
BLUE='#245f8b';GREEN='#2e7d49';ORANGE='#b85c21';GRAY='#5c6570';PURPLE='#735291'

def signedfloor12(s):
    f=F(s);n=f.numerator*10**12//f.denominator;a=abs(n);return ('-' if n<0 else '')+f'{a//10**12}.{a%10**12:012d}'

def verify(data):
    oldpath=ROOT/(R+'overview_stage18');assert sha(oldpath/'MANIFEST_SHA256.json')=='9bee857d7ffd20440048adef790f9b564b3a81d76673c206ed3ef80d1d4475c1'
    old=json.loads((oldpath/'overview_data.json').read_text())
    mutable={'snapshot_label','schema_version','generated_utc','sources','review_seals','claim_selection'}
    for k,value in old.items():
        if k not in mutable:assert data[k]==value,('prior data changed',k)
    assert data['snapshot_label']=='stage19' and len(data['claims'])==339
    for p,h in old['sources'].items():assert data['sources'][p]==h
    assert data['review_seals'][:len(old['review_seals'])]==old['review_seals']
    for p,h in data['preserved_stage18_files'].items():assert sha(ROOT/p)==h
    accepted=json.loads((HERE/'ACCEPTED_REVIEW_SEALS.json').read_text());assert {s['manifest']:s['sha256'] for s in data['review_seals']}==accepted
    for directory,h in data['stage19_review_pins'].items():assert accepted[R+directory+'/MANIFEST_SHA256.json']==h
    for key,r in data['stage19_evidence'].items():assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
    assert data['stage19_scope']==dict(smallest_accepted_initialization=30,strongest_global_gap='31/1250',strongest_global_gap_tail_initialization=34,uniform_contiguous_coverage_onset=2,isolated24=True,isolated24_alone_proves_uniform_onset=False,direct25_resource_compliance_accepted=False,no_minimum_claim=True,bilayer_new_gap=False,full8x4_m4_accepted=False,compiler_scope='local algebra and512-target samples only',old180_second_production_gate_passed=False,failed_cost_gate_is_universal_nogo=False,active_compiler_included=False)
    assert len(data['stage19_uniform_initializations'])==3 and len(data['stage19_uniform_coverage'])==5 and len(data['stage19_uniform_isolated'])==1
    for key in ['stage19_uniform_initializations','stage19_uniform_coverage','stage19_uniform_isolated','stage19_uniform_finite_certificates']:
        for r in data[key]:
            assert r['primary_sha256']==data['sources'][r['primary_source']] and ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer'])==r['gap_lower_exact']
            assert r['gap_lower_decimal_down_12']==floor12(r['gap_lower_exact']) and r['unique_ground_state']
    for r in data['stage19_uniform_initializations']+data['stage19_uniform_coverage']:assert r['model']=='untwisted_periodic_uniform_spin1_Heisenberg' and r['unit_bilinear_exchange']==1 and r['all_integer_lengths']
    for r in data['stage19_uniform_initializations']:
        assert r['bootstrap_initialization']==r['integer_size_min'] and r['anchor_length']==2*r['bootstrap_initialization']
        assert r['MPS_bond_dimension']==26 and r['trial_span_dimension']==1 and r['physical_anchor_Hilbert_dimension']==3**r['anchor_length']
        assert r['anchor_energy_convention']=='H0 is TOTAL energy; shifted H0/N0+aL, no extra factor L' and r['all_integer_lengths'] and not r['minimum_seed_claim']
    assert {(r['bootstrap_initialization'],r['gap_lower_exact']) for r in data['stage19_uniform_initializations']}=={(34,'31/1250'),(32,'49/2000'),(30,'179/10000')}
    assert {(r['integer_size_min'],r['gap_lower_exact']) for r in data['stage19_uniform_coverage']}=={(28,'179/10000'),(26,'23/10000'),(24,'23/10000'),(2,'23/10000'),(2,'31/1250')}
    for r in data['stage19_uniform_coverage']:assert r['bootstrap_initialization']==(34 if r['id']=='stage19_coverage2_0248' else 30) and r['coverage_only'] and not r['minimum_seed_claim']
    r=data['stage19_uniform_isolated'][0];assert r['certified_lengths']==[24] and not r['all_integer_tail_claim'] and r['gap_lower_exact']=='23/10000' and r['bootstrap_initialization']==30
    v=data['stage19_evidence']['bilayer_connected_rule_compiler_review']['verdict'];assert v['status']=='PASS_LOCAL_OPERATOR_ALGEBRA_ONLY' and v['rules_checked']==297237 and v['implicit_entries_checked']==121251328 and not v['production_feasibility'] and not v['new_gap']
    v=data['stage19_evidence']['bilayer_cartesian_indexed_review']['verdict'];assert v['independent_output_channel_comparisons']==23040 and v['samples_per_family']==512 and v['zero_source_targets_per_family']==285 and v['production_gate']=='FAIL_180_SECOND_EMPIRICAL_PROJECTION' and not v['full_q6_cache_or_pass'] and not v['new_gap']
    for key in ['stage19_direct25_physical','stage19_direct25_resource']:
        r=data[key];assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
    v=data['stage19_direct25_physical']['verdict'];assert v['direct_length']==25 and v['all_integer_L_at_least']==24 and v['bootstrap_initialization']==30 and v['norm_positive'] and F(v['fresh_MPS25_shifted_total_Rayleigh'])>0
    assert 0<F(v['numerator_lower'])<1 and F(v['purity_lower'])>F('1/2') and F(v['strict_gap_margin'])>0
    v=data['stage19_direct25_resource']['verdict'];assert v['status']=='RESOURCE_BUDGET_COMPLIANCE_NOT_ACCEPTED' and v['authorized_reviewer_CPU_seconds']==15 and v['reported_program_process_CPU_seconds']==25.9614 and v['runtime_postexec_limits_not_logged'] and v['external_wait4_utime_stime_not_retained']
    p=data['stage19_small_lengths_physical'];assert p['verdict']==json.loads((ROOT/p['primary_source']).read_text()) and p['source_sha256']==data['sources'][p['primary_source']]
    v=p['verdict'];assert v['all_integer_L_at_least']==2 and v['bootstrap_initialization']==30 and v['all18_physical_input_mapping_verified'] and v['prior_direct25_resource_anomaly_still_unresolved']
    assert [r['L'] for r in v['rows']]==list(range(4,24)) and all(F(r['strict_margin'])>0 and F(r['purity_lower'])>F('1/2') for r in v['rows'])
    assert len(data['stage19_uniform_finite_certificates'])==52 and {r['certified_lengths'][0] for r in data['stage19_uniform_finite_certificates']}==set(range(2,34))
    for r in data['stage19_uniform_finite_certificates']:
        assert not r['all_integer_tail_claim']
        if r['certified_lengths'][0]>=4:assert r['MPS_bond_dimension']==26 and r['trial_span_dimension']==1 and r['physical_Hilbert_dimension']==3**r['certified_lengths'][0]
    g=v['new_guarded_run'];assert g['exit_code']==0 and not g['wall_watchdog_fired'] and g['requested_cpu_soft_hard']==[30,30] and g['external_wall_limit_seconds']==25 and g['wait4_total_cpu_seconds']<30
    p=data['stage19_strong_all_size'];assert p['verdict']==json.loads((ROOT/p['primary_source']).read_text()) and p['source_sha256']==data['sources'][p['primary_source']]
    v=p['verdict'];assert v['gap']=='31/1250' and v['all_integer_L_at_least']==2 and v['bootstrap_initialization_used_for_this_stronger_gap']==34 and v['smallest_separately_certified_initialization']==30 and v['smaller_initialization_gap']=='179/10000'
    assert [r['L'] for r in v['cached_prefix_4_to25']]==list(range(4,26)) and [r['L'] for r in v['new_direct26_to33']]==list(range(26,34))
    assert all(F(r['strict_gap_margin'])>0 and F(r['purity_lower'])>F('1/2') for r in v['cached_prefix_4_to25']+v['new_direct26_to33'])
    assert all(r['norm_positive'] for r in v['new_direct26_to33']) and v['analytic2_3_inherited_verified'] and v['prior_direct25_resource_anomaly_still_unresolved'] and v['no_minimum_claim']
    for r in data['stage19_uniform_finite_certificates']:
        if 'length_source_pointer' in r:assert ptr(json.loads((ROOT/r['primary_source']).read_text()),r['length_source_pointer'])==r['certified_lengths'][0]
    v=data['stage19_evidence']['bilayer_brauer_rule_review']['verdict'];assert v['independent_graph_composition_cases']==58000 and v['diagram_records']==17107 and v['independent_output_channel_comparisons']==23040 and v['production_gate']=='FAIL_180_SECOND_EMPIRICAL_PROJECTION' and not v['full_q6_pass'] and not v['new_gap']
    for r in data['stage19_uniform_finite_certificates']:
        L=r['certified_lengths'][0]
        if L>=4:assert r['anchor_length']==(48 if L==24 else L) and r['physical_anchor_Hilbert_dimension']==3**r['anchor_length']
        if L==24:assert r['id']=='stage19_strong_parity24' and r['proof_kind'].startswith('inherited parity-resolved')
    r=data['stage19_uniform_isolated'][0];assert r['anchor_length']==48 and r['physical_target_Hilbert_dimension']==3**24 and r['physical_anchor_Hilbert_dimension']==3**48
    for p,h in data['sources'].items():assert sha(ROOT/p)==h
    count=0
    for seal in data['review_seals']:
        assert sha(ROOT/seal['manifest'])==seal['sha256'];n=manifest_check(seal['manifest']);assert n==seal['verified_files'];count+=n
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
            if model=='ordinary_spinhalf_bilayer' and r['parameter_kind']=='closed_interval' and r.get('certificate_route')!=data['current_ordinary_interval_union_route']:continue
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
            ax.set_xlim(-.004,.112);ax.set_ylim(.0003,.70);ax.set_xticks([0,.02,.04,.06,.08,.10] if data['combined_review_included'] else [0,.02,.04,.06,.07])
            ax.text(.04,.15,'[0,.108]: Δ ≥ .004499695659\n[0,.10825]: Δ ≥ .000586405978',transform=ax.transAxes,fontsize=9,color=GREEN)
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
    ax.plot([0,.108],[.004499695659]*2,color=GREEN,lw=2);ax.text(.014,.0053,'Stronger nested [0,.108]: .004499695659',color=GREEN,fontsize=10)
    ax.annotate('Broad union: 0.000586405978',(.014,v),xytext=(0,12),textcoords='offset points',fontsize=11,color=PURPLE)
    ax.set_yscale('log');ax.set_ylim(.0003,.7);ax.set_xlim(-.001,hi+.001);ax.set_xticks([0,.01,.02,.03,.04,.05,.06,.07,.08,.09]+[float(F(data['current_ordinary_interval_endpoint']))]);ax.set_xlabel('Intralayer coupling g');ax.set_ylabel('Certified gap lower bound')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,p:f'{x:g}'))
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
    fig,ax=plt.subplots(figsize=(11,5.8));cs=sorted(data['uniform_large_size_certificates'][:3]+data['uniform_coverage_certificates'],key=lambda r:r['integer_size_min'])
    colors=[GREEN,GRAY,BLUE,PURPLE]
    for r,color in zip(cs,colors):
        n=r['integer_size_min'];g=float(F(r['gap_lower_exact']));ax.plot([n,120],[g,g],color=color,lw=2.6)
        ax.scatter([n],[g],color=color,s=55);ax.annotate('',xy=(122,g),xytext=(118,g),arrowprops={'arrowstyle':'->','color':color,'lw':2.6})
        ax.text(n+4,g+.00035,f"Δ ≥ {g:g}, every integer L ≥ {n}",color=color,fontsize=11)
    ax.set(xlim=(46,124),ylim=(0,.012),xlabel='Periodic microscopic spin count L',ylabel='Certified gap lower bound',title='Uniform spin-1: preserved first-dataset gap certificates')
    ax.set_xticks([48,52,56,60,80,100,120]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    ax.plot([48,96],[.0053,.0053],color=ORANGE,lw=2,ls='--');ax.text(65,.00565,'Finite 48–96 only: Δ ≥ .0053',color=ORANGE,fontsize=10)
    fig.text(.5,.065,'Unit bilinear exchange; all integers, including odd L. The strongest bound on overlaps may be selected.',ha='center',fontsize=10)
    fig.text(.5,.025,'First-data route: coverage48, initialization52. Stage18 second-data certificate separately covers every integer L≥36.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.1,right=.97,top=.86,bottom=.22);save(fig,'uniform_gap_frontier',plt)
    if data['stage12_source_scope_included']:
        comparisons=data['stage12_source_scope']['verdict']['comparisons']
        fig,ax=plt.subplots(figsize=(11,5.8));values=[float(F(c['original_gap_interval'][0])) for c in comparisons]+[.0102,.0038]
        labels=['Original theorem\neven L ≥ 60','Original theorem\neven L ≥ 2304','Accepted new bound\nall integer L ≥ 60','Accepted n52 bound\nall integer L ≥ 52']
        ax.bar(range(4),values,color=[GRAY,GRAY,PURPLE,GREEN],width=.58)
        for i,v in enumerate(values):ax.text(i,v*1.12,('≈ ' if i<2 else '')+f'{v:.12f}'.rstrip('0'),ha='center',fontsize=10)
        ax.set_yscale('log');ax.set_ylim(.0003,.021);ax.set_xticks(range(4),labels);ax.set_ylabel('Certified gap lower bound, unit exchange')
        ax.set_title('First thermal dataset: comparison with the original theorem',pad=16);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
        fig.text(.5,.065,'The .0102 lower bound is ≈21.28584× and ≈2.66940× the two original lower bounds, on their overlapping scopes.',ha='center',fontsize=10)
        fig.text(.5,.025,'Ratios compare sufficient certified bounds, not physical-gap estimates. Original final theorem: even lengths only.',ha='center',fontsize=10)
        fig.subplots_adjust(left=.11,right=.97,top=.86,bottom=.24);save(fig,'uniform_theorem_comparison',plt)
    if data['stage12_frontier_point_included']:
        fig,ax=plt.subplots(figsize=(10.5,5.5));rs=[r for r in data['claims'] if r.get('certificate_route') in ['bilayer_direct_time_first_point','bilayer_frontier_above010_point','stage13_actual_point','stage16_symmetry_point']]
        ax.scatter([float(F(r['parameter_exact'])) for r in rs],[float(F(r['gap_lower_exact'])) for r in rs],s=55,color=BLUE)
        for r in rs:
            f=F(r['gap_lower_exact']);six=f.numerator*10**6//f.denominator
            ax.annotate(f"{six//10**6}.{six%10**6:06d}",(float(F(r['parameter_exact'])),float(f)),xytext=(16 if r['parameter_exact']=='1/10' else 0,-20 if r['parameter_exact'] in ['1001/10000','53/500'] else 12),textcoords='offset points',ha='center',fontsize=9)
        if data['stage12_frontier_interval_included']:
            g=float(F(data['stage12_frontier_interval']['verdict']['extension_uniform_gap']));ax.plot([.1,.102],[g,g],color=GREEN,lw=2.7);ax.text(.1009,g-.003,'Entire [.10,.102]: Δ ≥ .013574634391',ha='center',color=GREEN,fontsize=10)
        if data['stage13_interval_included']:
            ax.plot([.102,.105],[.017785998829]*2,color=PURPLE,lw=2.7);ax.text(.1035,.021,'Entire [.102,.105]: Δ ≥ .017785998829',ha='center',color=PURPLE,fontsize=9)
        if data['stage16_interval_included']:
            ax.plot([.105,.106],[.020881493369]*2,color=ORANGE,lw=2.7);ax.text(.1055,.0265,'[.105,.106]\nΔ ≥ .020881493369',ha='center',color=ORANGE,fontsize=8)
        if data['stage16_next_interval_included']:
            ax.plot([.106,.1065],[.019955613868]*2,color=GRAY,lw=3);ax.text(.1055,.008,'[.106,.1065]: Δ ≥ .019955613868',ha='center',color=GRAY,fontsize=8)
        ax.set(xlim=(.0998,.10685),ylim=(.006,.068),xlabel='Intralayer coupling g',ylabel='Certified gap lower bound',title='Ordinary bilayer: inherited frontier points through .1065')
        ax.set_xticks([.1000,.1010,.1020,.1030,.1040,.1050,.1060]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
        fig.text(.5,.05,'Every integer square side L ≥ 2. Points are separate certificates; their trend is not a physical-gap estimate.',ha='center',fontsize=10)
        fig.text(.5,.012,'Six-decimal point labels are rounded downward. Exact certificate values are retained in the data.',ha='center',fontsize=9)
        fig.subplots_adjust(left=.11,right=.97,top=.86,bottom=.19);save(fig,'bilayer_frontier',plt)
    fig,ax=plt.subplots(figsize=(10,5.5))
    import numpy as np
    x=np.arange(3);dims=data['stage13_bilayer_dimensions']
    for off,key,label,col in [(-.24,'ground_search_dimension','Ground search',BLUE),(0,'total_trial_space_dimension','Total trial span',PURPLE),(.24,'retained_low_band_count','Retained states',GREEN)]:
        vals=[r[key] for r in dims];ax.bar(x+off,vals,.23,label=label,color=col)
        for a,b in zip(x+off,vals):ax.text(a,b+2,str(b),ha='center',fontsize=10)
    ax.set_xticks(x,['4×4: full 2³²','8×4: full 2⁶⁴','8×8: full 2¹²⁸']);ax.set_ylim(0,170);ax.set_ylabel('Linear dimension / retained-state count');ax.set_title('Actual g=.105: physical space and trial dimensions separated')
    ax.legend(frameon=False,ncol=3,loc='upper left');ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.025,'The 8×8 numerator retains one Rayleigh vector from its 43D search. These are not MPS bond dimensions.',ha='center',fontsize=10)
    fig.subplots_adjust(bottom=.15,top=.88);save(fig,'stage13_trial_dimensions',plt)
    fig,ax=plt.subplots(figsize=(11,5.7));rs=data['conditional_uniform_certificates']
    for i,r in enumerate(rs):
        g=float(F(r['gap_lower_exact']));color=[GRAY,PURPLE][i];ax.plot([36,100],[g,g],ls='--',color=color,lw=3);ax.scatter([36],[g],marker='D',s=55,color=color)
        ax.text(45,g+.0012,f"Historical conditional Δ ≥ {g:g}, every integer L ≥ 36",color=color,fontsize=11)
    ax.set(xlim=(32,104),ylim=(0,.027),xlabel='Periodic microscopic spin count L',ylabel='Gap lower bound in historical scalar proof',title='Historical conditional proofs: premises discharged in stage18')
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.text(.5,.065,'Historical premise:18 published β=49/4 certificates. Stage18 independently reproduces all18 physical inputs.',ha='center',fontsize=10)
    fig.text(.5,.025,'Historical scalar rows stay unchanged; stage18 separately records both fully discharged local theorems.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.1,right=.97,top=.87,bottom=.22);save(fig,'conditional_uniform_bounds',plt)
    fig,ax=plt.subplots(figsize=(10.5,5.7));rs=data['bilayer_short_size_certificates']
    for r,col in zip(rs,[BLUE,PURPLE,ORANGE]):
        x=float(F(r['parameter_exact']));y=float(F(r['gap_lower_exact']));ax.plot([0,x],[y,y],color=col,lw=2.5);ax.scatter([x],[y],color=col,s=45);ax.text(.035,y*1.23,f"[0,{x:g}]: Δ ≥ {r['gap_lower_decimal_down_12']}",color=col,fontsize=10)
    ax.set_yscale('log');ax.set(xlim=(-.003,.158),ylim=(.0003,.13),xlabel='Intralayer coupling g',ylabel='Finite-size certified gap',title='Ordinary bilayer: short-size bridges only, L=2,…,7')
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.text(.5,.065,'Full-Hilbert spectral comparison; two-dimensional Rayleigh trial span; all short odd sizes included.',ha='center',fontsize=10)
    fig.text(.5,.025,'No all-size frontier extension: the accepted all-L≥2 continuous interval remains [0,.105].',ha='center',fontsize=10)
    fig.subplots_adjust(left=.1,right=.97,top=.87,bottom=.22);save(fig,'bilayer_short_size_bounds',plt)
    rows=data['bilayer_ground_endpoint_certificates'];fig,ax=plt.subplots(figsize=(10.5,5.8));ax.axis('off')
    cells=[[f"{r['geometry'][0]}×{r['geometry'][1]}",f"{float(F(r['parameter_exact'])):g}",str(r['ground_search_dimension']),r['shifted_ground_lower_decimal_down_12']] for r in rows]
    table=ax.table(cellText=cells,colLabels=['Seed geometry','Coupling g','Trial dimension','Shifted ground lower bound'],cellLoc='center',loc='center',colWidths=[.21,.17,.2,.42]);table.auto_set_font_size(False);table.set_fontsize(12);table.scale(1,2.1)
    for (i,j),cell in table.get_celld().items():
        cell.set_edgecolor('#d3dbe1')
        if i==0:cell.set_facecolor('#e9f0f5');cell.set_text_props(weight='bold')
    ax.set_title('Bilayer: independently accepted physical ground endpoints',pad=15)
    fig.text(.5,.085,'Energy convention: shifted H′ of each exact review. Decimal lower endpoints are rounded downward.',ha='center',fontsize=10)
    fig.text(.5,.04,'These are ground-energy lower bounds, not positive gaps or all-size bootstrap certificates.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.06,right=.94,top=.88,bottom=.17);save(fig,'bilayer_ground_endpoints',plt)
    fig,ax=plt.subplots(figsize=(10,5.5));xs=[0,1];rs=data['stage15_matrix_dimensions']
    for off,key,label,col in [(-.18,'unsplit_ground_trial_dimension','Complete unsplit H² basis',BLUE),(.18,'split_ground_trial_dimension','Complete split H² basis',PURPLE)]:
        vals=[r[key] for r in rs];ax.bar([x+off for x in xs],vals,width=.35,color=col,label=label)
        for x,y in zip(xs,vals):ax.text(x+off,y+1,str(y),ha='center',fontsize=12)
    ax.set_xticks(xs,['4×4: full Hilbert space 2³²','8×4: full Hilbert space 2⁶⁴']);ax.set_ylim(0,72);ax.set_ylabel('Exact finite linear basis dimension');ax.set_title('Complete physical H² matrices: unsplit and split spans');ax.legend(frameon=False,loc='upper left');ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.045,'New matrix dimensions do not replace the 49/97 retained states in the existing all-size gap certificates.',ha='center',fontsize=10)
    fig.text(.5,.012,'The largest 8×8 numerator remains one retained vector in physical space 2¹²⁸; MPS bond dimensions are unrelated.',ha='center',fontsize=9)
    fig.subplots_adjust(left=.1,right=.97,top=.87,bottom=.2);save(fig,'bilayer_complete_matrix_dimensions',plt)
    fig,ax=plt.subplots(figsize=(11,5.5));values=[.021451810876,.020945510446,.020227124817];labels=['g=.1065: every integer L ≥ 2','g=.106: every integer L ≥ 2','g=.11: only 2 ≤ L ≤ 32']
    ax.barh([2,1,0],values,color=[GREEN,BLUE,ORANGE],height=.45)
    for y,v in zip([2,1,0],values):ax.text(v+.0005,y,f'{v:.12f}',va='center',fontsize=11)
    ax.set_yticks([2,1,0],labels);ax.set_xlim(0,.029);ax.set_xlabel('Certified gap lower bound');ax.set_title('Square-symmetry certificates: size scopes remain distinct');ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.06,'All-size: g=.106 uses 16/43 grounds; g=.1065 uses 21/57 grounds; both use 43D numerator, retain 49/97/1.',ha='center',fontsize=10)
    fig.text(.5,.02,'g=.11 finite result uses 16/57 denominator and 57D numerator searches. Its all-size targets remain hypothetical.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.28,right=.96,top=.86,bottom=.24);save(fig,'stage16_scope_comparison',plt)

    fig,axes=plt.subplots(1,2,figsize=(13,5.8))
    ax=axes[0];rs=[r for r in data['claims'] if r.get('certificate_route')=='stage17_symmetry_point']
    ax.scatter([float(F(r['parameter_exact'])) for r in rs],[float(F(r['gap_lower_exact'])) for r in rs],color=BLUE,s=50)
    for r in rs:
        x=float(F(r['parameter_exact']));y=float(F(r['gap_lower_exact']));ax.annotate(r['gap_lower_decimal_down_12'],(x,y),xytext=(-5 if x>.108 else 0,12),textcoords='offset points',ha='right' if x>.108 else 'center',fontsize=8)
    ax.set(xlim=(.10655,.10845),ylim=(0,.022),xlabel='Intralayer coupling g',ylabel='Certified gap lower bound',title='Five new isolated point certificates')
    ax.ticklabel_format(axis='x',style='plain',useOffset=False);ax.set_xticks([.10675,.107,.1075,.108,.10825]);ax.tick_params(axis='x',labelrotation=25)
    ax=axes[1]
    for i,(c,col) in enumerate(zip(data['stage17_nested_covers'],[GREEN,PURPLE])):
        end=float(F(c['endpoint']));g=float(F(c['gap_lower']));ax.plot([0,end],[g,g],color=col,lw=3);ax.scatter([0,end],[g,g],color=col,s=30)
        ax.text(.054,g*1.16,f"[0,{end:g}]: Δ ≥ {floor12(c['gap_lower'])}\n{c['closed_pieces']} closed pieces",ha='center',color=col,fontsize=10)
    ax.set(xlim=(-.002,.114),ylim=(.00035,.011),yscale='log',xlabel='Intralayer coupling g',ylabel='Uniform certified gap',title='Both nested covers remain valid')
    for ax in axes:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.text(.5,.025,'Every integer square L ≥ 2; unique ground. Search dimensions 21/57 and 43; retained states 49/97 and one.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.07,right=.98,bottom=.21,top=.87,wspace=.32);save(fig,'stage17_nested_frontier',plt)
    fig,ax=plt.subplots(figsize=(10.5,5.6));vals=[57,58,116];labs=['Inherited complete basis','New complete basis','Basis + Hamiltonian images']
    ax.bar(range(3),vals,color=[GRAY,BLUE,PURPLE],width=.55)
    for j,v in enumerate(vals):ax.text(j,v+3,str(v),ha='center',fontsize=13)
    ax.set_xticks(range(3),labs);ax.set_ylim(0,140);ax.set_ylabel('Linear matrix dimension');ax.set_title('8×4 bilayer: complete physical 58D matrix certification')
    ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.095,'174 new physical entries; 290 coupling-polynomial entries. Gram rank 58; block-Gram rank 87 at g=.11.',ha='center',fontsize=10)
    fig.text(.5,.052,'All 4495 q4 and 169911 q6 supports; full signed q8 contribution. Physical Hilbert space 2⁶⁴.',ha='center',fontsize=10)
    fig.text(.5,.015,'Matrix dimensions do not replace the 21/57 ground and 43 numerator searches in the latest frontier gap certificates.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.1,right=.97,bottom=.24,top=.87);save(fig,'stage18_complete58D_scope',plt)
    fig,axes=plt.subplots(1,2,figsize=(13.5,6));ax=axes[0]
    values=[.0038,.0102,.0046,.0214];labels=['First dataset\nL ≥ 48\ninitialization 52','First dataset\nL ≥ 60','Second dataset\nbaseline\nevery integer L ≥ 36','Signed moments\nimprovement\nevery integer L ≥ 36']
    ax.bar(range(4),values,color=[GRAY,GRAY,BLUE,GREEN],width=.58)
    for j,v in enumerate(values):ax.text(j,v+.0007,f'{v:g}',ha='center',fontsize=12)
    ax.set_xticks(range(4),labels,fontsize=8);ax.set_ylim(0,.027);ax.set_ylabel('Certified gap lower bound, unit exchange');ax.set_title('Uniform spin-1: all physical premises discharged')
    ax=axes[1];old1=(4/105)*__import__('math').log(80/79);old2=__import__('math').log(20)/784
    ax.bar(range(3),[old1,old2,.0214],color=[GRAY,PURPLE,GREEN],width=.55)
    for j,v in enumerate([old1,old2,.0214]):ax.text(j,v*1.2,('≈ ' if j<2 else '')+f'{v:.10f}',ha='center',fontsize=9)
    ax.set_yscale('log');ax.set_ylim(.00025,.05);ax.set_xticks(range(3),['Original even L ≥ 60','Original even L ≥ 2304','New every integer L ≥ 36'],fontsize=9);ax.set_title('Comparison with the original theorem')
    for ax in axes:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.14)
    fig.text(.5,.085,'18 physical inputs, β=49/4; 2428 batches. Exact coarse/refined scalar mapping and prior D26 MPS72 anchor verified.',ha='center',fontsize=10)
    fig.text(.5,.047,'The .0214 lower bound is ≈44.6585× and ≈5.6005× the original bounds on overlapping scopes; not a gap estimate.',ha='center',fontsize=10)
    fig.text(.5,.013,'Original first initialization 60 and second initialization 36. No minimum-size or below 36 claim.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.07,right=.98,bottom=.27,top=.88,wspace=.3);save(fig,'stage18_uniform_physical_completion',plt)
    fig,axes=plt.subplots(1,2,figsize=(13.5,6));ax=axes[0]
    ax.plot([2,64],[.0248,.0248],color=GREEN,lw=3.2);ax.scatter([2],[.0248],color=GREEN,s=55)
    ax.text(8,.026,'Δ ≥ .0248 for every integer L ≥ 2',color=GREEN,fontsize=12)
    for n,g,col in [(2,.0023,GRAY),(28,.0179,BLUE),(32,.0245,PURPLE)]:
        ax.plot([n,64],[g,g],color=col,lw=1.4,ls='--')
    ax.text(5,.0033,'Earlier all-size .0023 retained',color=GRAY,fontsize=9)
    ax.text(32,.0156,'Earlier .0179 from28 retained',color=BLUE,fontsize=9)
    ax.text(35,.0213,'Earlier .0245 from32 retained',color=PURPLE,fontsize=9)
    ax.set(xlim=(0,66),ylim=(0,.033),xlabel='Microscopic spin count L',ylabel='Certified gap lower bound',title='All-size coverage, unit exchange, unique ground')
    ax=axes[1];rs=sorted(data['stage19_uniform_initializations'],key=lambda r:r['bootstrap_initialization'])
    ax.bar([str(r['bootstrap_initialization']) for r in rs],[float(F(r['gap_lower_exact'])) for r in rs],color=[BLUE,PURPLE,GREEN],width=.55)
    for j,r in enumerate(rs):ax.text(j,float(F(r['gap_lower_exact']))+.001,r['gap_lower_decimal_down_12'].rstrip('0'),ha='center',fontsize=11)
    ax.set(ylim=(0,.033),xlabel='Genuine bootstrap initialization size n',ylabel='Certified all-integer tail bound',title='Initialization remains distinct from coverage')
    for ax in axes:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.text(.5,.10,'The .0248 all-size proof joins analytic L2/3, finite L4–33 certificates and the n34 tail.',ha='center',fontsize=11)
    fig.text(.5,.061,'Smallest accepted genuine initialization: n30 at .0179. No smaller-start or minimum-size claim.',ha='center',fontsize=10)
    fig.text(.5,.022,'Fresh D26 anchors use TOTAL energy H0/N0+aL, with no extra L. Prior resource exceptions remain disclosed.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.075,right=.98,bottom=.24,top=.87,wspace=.3);save(fig,'stage19_uniform_initialization_coverage',plt)
    return matplotlib.__version__

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');ap.add_argument('--output-dir');args=ap.parse_args()
    if args.output_dir:OUT=Path(args.output_dir).resolve();OUT.mkdir(parents=True,exist_ok=True)
    elif not args.check_only:assert not (HERE/'MANIFEST_SHA256.json').exists(), 'Frozen snapshot: use --output-dir'
    data=json.loads((HERE/'overview_data.json').read_text());n=verify(data)
    info={'status':'PASS','claims':len(data['claims']),'finite_size_certificate_rows':len(data['finite_size_certificates']),'uniform_large_size_certificate_rows':len(data['uniform_large_size_certificates']),'dimension_rows':len(data['dimensions']),'stage13_dimension_rows':len(data['stage13_bilayer_dimensions']),'conditional_uniform_rows':len(data['conditional_uniform_certificates']),'bilayer_short_size_rows':len(data['bilayer_short_size_certificates']),'bilayer_ground_endpoint_rows':len(data['bilayer_ground_endpoint_certificates']),'historical_partial_accepted_cases':sum(r['full_physical_case_accepted'] for r in data['thermal_partial_cases']),'accepted_full_thermal_cases':18,'historical_stage18_locally_reproduced_uniform_rows':2,'stage19_genuine_initializations':3,'stage19_coverage_records':5,'stage19_finite_certificates':52,'uniform_best_gap':'31/1250','uniform_best_coverage_onset':2,'uniform_best_gap_tail_initialization':34,'smallest_genuine_initialization':30,'stage16_finite_bilayer_rows':len(data['stage16_finite_bilayer_certificates']),'uniform_finite_window_rows':len(data['uniform_finite_windows']),'uniform_coverage_rows':len(data['uniform_coverage_certificates']),'direct_source_hashes':len(data['sources']),'review_seals':len(data['review_seals']),'sealed_file_hashes_checked':n,'combined_review_included':data['combined_review_included'],'interval_extension_included':data['interval_extension_included'],'cpu_affinity':sorted(os.sched_getaffinity(0)),'address_space_limit_bytes':1024**3,'blas_threads':1,'checks':['source SHA-256','complete selected review manifests','all exact gap JSON pointers','all decimal floors','best point selection','all exact adjacent closed pieces and uniform minimum','Hilbert dimensions','numerator rank separated from search and filtered span','failure gaps remain null','all 207 chain candidate routes','all exact interval pieces','historical59/139 and new64/139 denominator trial dimensions','reference67 versus unchanged M8 search','70 orthogonal MPS states with bond52 and necessary screen only','g010 diagnostic scope without gap promotion','separate AKLT projector reference','all stage18 files and all339 main rows preserved', 'finite-size g025 kept separate', 'pair symmetry erratum', '74-integer current and even/direct recipe scopes', 'four preserved uniform bounds; new finite48..96 bridge and all-integerL>=48 coverage with initialization52', 'historical66/74/80 pieces preserved; latest finalized square-symmetry interval cover checked', 'new direct point and fixed-family metadata erratum', 'original source n>=4 scope and theorem comparison', 'rank195 fixed early-window obstruction and strict decimal direction','scoped conditional error budgets; abstract unit-count rank; negative Rayleigh anchors; all-r canonical n48/n50 exclusion without minimum-seed claim','two historical conditional records preserved; new accepted local rows discharge all18 physical inputs','historical short-size bilayer rows stay L2..7; new all-size bounds have separate final reviews','historical4x4 fixture and accepted complete43D/57D8x4 matrices retain sector cutoff obligations','historical kernel/data-plane/supervisor engineering reviews retained unchanged','complete43D/57D physical H2 matrices and exact split compressions','physical ground endpoints separate from gap rows','historical16-case snapshot retained; new18-case acceptance and2979 archived entries verified; mutable campaign excluded','square-isotropic geometry and raw/canonical coordinates distinguished','actual .106/.1065 all-size and .11 finite2..32 scopes separated','selected 16/43 searches distinguished from21/57 ambient matrices','small m4 fixture and scoped envelope barrier only','repair engineering gate does not discharge missing thermal premises','five new points and six closed pieces preserve both nested86/88-piece uniform bounds','fixed-parameter pair-product residual floor is not a universal no-go']}
    if not args.check_only:
        info['matplotlib']=plot(data);info['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (OUT/'validation.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info))
