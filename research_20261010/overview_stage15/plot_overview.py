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
    oldpath=ROOT/(R+'overview_stage14')
    assert sha(oldpath/'MANIFEST_SHA256.json')=='873769e3e99bf338a9b32548df20d89ecf7ce614aa3e68fad10035f91bf0d41e'
    old=json.loads((oldpath/'overview_data.json').read_text())
    for k,value in old.items():
        if k not in {'snapshot_label','schema_version','generated_utc','sources','review_seals','claim_selection'}:assert data[k]==value,('prior data changed',k)
    assert data['snapshot_label']=='stage15'
    for p,h in old['sources'].items():assert data['sources'][p]==h
    assert data['review_seals'][:len(old['review_seals'])]==old['review_seals']
    for p,h in data['preserved_stage14_files'].items():assert sha(ROOT/p)==h
    accepted=json.loads((HERE/'ACCEPTED_REVIEW_SEALS.json').read_text())
    assert {s['manifest']:s['sha256'] for s in data['review_seals']}==accepted
    for directory,h in data['stage15_review_pins'].items():assert accepted[R+directory+'/MANIFEST_SHA256.json']==h
    for p,h in data['sources'].items():assert sha(ROOT/p)==h
    count=0
    for seal in data['review_seals']:
        assert sha(ROOT/seal['manifest'])==seal['sha256'];n=manifest_check(seal['manifest']);assert n==seal['verified_files'];count+=n
    for key,r in data['stage15_evidence'].items():
        assert r['verdict']==json.loads((ROOT/r['primary_source']).read_text()) and r['source_sha256']==data['sources'][r['primary_source']]
    assert data['stage15_scope']==dict(new_full8x4_43D_H2=True,new_full8x4_57D_H2=True,new_all_size_bilayer_gap=False,current_gap_pipeline_search_dimensions_changed=False,float_diagnostic_failures_are_certificates=False,float_diagnostic_failures_universal_nogo=False,conditional_uniform_gap_promoted=False,full18_physical_inputs_accepted=False,mutable_campaign_inputs_included=False,thermal_campaign_resume_authorized_by_snapshot=False)
    v=data['stage15_evidence']['matrix43']['verdict'];assert v['trial_dimension']==43 and v['complete_H2_coefficient_entries_verified']==5547 and v['M_zero_supports_retained']==96705 and v['M_zero_TT_trace']==4505303808 and v['signed_commutator_and_complete_q8_PSD'] and v['projected_H2_rejected']
    v=data['stage15_evidence']['matrix57']['verdict'];assert v['dimension']==57 and v['complete_H2_polynomial_entries_verified']==9747 and v['individual_split_entries_verified']==980 and v['oriented_cross_blocks_nonsymmetric'] and v['full43D_compression_exact'] and v['M_zero_TT_retained'] and v['no_new_endpoint_or_gap']
    v=data['stage15_evidence']['split_fixture']['verdict'];assert v['dimension']==21 and v['full16D_compression_exact'] and v['full_q8_retained_in_MM']
    v=data['stage15_evidence']['endpoints43']['verdict'];assert v['unique_global_ground'] and v['full_even_singlet_sector_r2_cutoff_verified'] and v['independent_odd_mode_coupling_checks']==96 and v['scoped_target_exclusions']==2 and not v['all_size_gap_claim'] and not v['universal_no_go_claim']
    rows=data['bilayer_ground_endpoint_certificates'];assert len(rows)==(6 if data['stage15_endpoint57_included'] else 4)
    for r in rows:
        src=json.loads((ROOT/r['primary_source']).read_text());g=F(ptr(src,r['primary_json_pointer']));assert g==F(r['shifted_ground_lower_exact'])<0
        a=ptr(src,r['primary_json_pointer'].rsplit('/',1)[0]);assert a['g']==r['parameter_exact']
        assert (a.get('shape') or src.get('geometry'))==r['geometry'] and a.get('basis_dimension',src.get('trial_dimension'))==r['ground_search_dimension']
        assert r['primary_sha256']==data['sources'][r['primary_source']]
        assert r['shifted_ground_lower_decimal_down_12']==signedfloor12(g)
        assert F(r['downward12_decimal_lower_exact'])==F(signedfloor12(g))<=g
        assert r['physical_spin_count']==2*r['geometry'][0]*r['geometry'][1] and r['full_Hilbert_dimension']==2**r['physical_spin_count']
        assert r['ground_search_dimension'] in [16,43,57] and r['parameter_exact'] in ['11/100','3/25'] and r['unique_global_ground'] and r['complete_even_singlet_cutoff_required'] and not r['new_all_size_gap']
    if data['stage15_endpoint57_included']:
        v=data['stage15_evidence']['endpoints57']['verdict'];assert v['exact57D_target_exclusions']==2 and v['target_LDL_independently_generated'] and v['target_cutoff_fixed'] and not v['all_size_gap_claim'] and v['float_temperature_failures_not_no_go']
        for r in rows:
            if r['ground_search_dimension']==57:
                oldr=next(a for a in rows if a['ground_search_dimension']==43 and a['parameter_exact']==r['parameter_exact'])
                assert F(r['gain_over43D_exact'])==F(r['shifted_ground_lower_exact'])-F(oldr['shifted_ground_lower_exact'])>0
    dims=data['stage15_matrix_dimensions'];assert len(dims)==2
    assert [(r['unsplit_ground_trial_dimension'],r['split_ground_trial_dimension'],r['full_Hilbert_dimension'],r['retained_denominator_states_in_existing_gap_pipeline'],r['existing_gap_pipeline_total_trial_dimension']) for r in dims]==[(16,21,2**32,49,64),(43,57,2**64,97,139)]
    assert data['stage15_partial_campaign_review_included']
    v=data['stage15_evidence']['thermal_partial']['verdict'];assert v['full_input_cases']==v['exact_published_W_matches']==16 and v['valid_saved_batches']==990 and v['missing_cases']==['L12_I','L12_P']
    assert not v['all18_thermal_premises_discharged'] and v['second_initialization_gap_status']=='CONDITIONAL, unchanged'
    assert v['charged_CPU_seconds']==16207 and v['remaining_ledger_CPU_seconds']==5393 and v['unknown_failed_reservations_retained']==14640 and v['no_restart_or_refund_authorized']
    o=data['stage15_evidence']['thermal_partial_outcome']['verdict'];assert o['no_active_attempts'] and not o['restart_or_refund_authorized'] and o['valid_completed_case_batches']==962
    assert o['completed_attempt_charges']+o['supervisor_overhead_charge']+o['unknown_failed_attempt_charges']==16207
    assert sum(a['valid_batches'] for a in o['valid_partial_L12_batches'])==28 and all(a['no_full_trace_certificate'] for a in o['valid_partial_L12_batches'])
    rows=data['thermal_partial_cases'];assert len(rows)==18 and len({r['case'] for r in rows})==18
    assert {r['case'] for r in rows if r['full_physical_case_accepted']}=={f'L{n}_{s}' for n in range(4,12) for s in ['I','P']}
    for r in rows:
        assert r['beta_exact']=='49/4' and r['physical_Hilbert_dimension']==3**r['length'] and r['primary_sha256']==data['sources'][r['primary_source']]
        src=json.loads((ROOT/r['primary_source']).read_text());a=ptr(src,r['primary_json_pointer'])
        if r['full_physical_case_accepted']:
            assert r['case']==a['case'] and r['W']==a['W'] and r['published_W_exact_match'] and r['weighted_multiplicity']==3**r['length']==a['multiplicity']
            assert r['trace_lower_exact']==a['lower'] and r['trace_upper_exact']==a['upper'] and F(a['lower'])<=F(a['upper'])
        else:
            assert r['case'] in a and r['length']==12 and r['W'] is None and r['trace_lower_exact'] is None and r['trace_upper_exact'] is None and not r['published_W_exact_match']
    assert all('uniform_second_thermal_campaign_run/' not in p for p in data['sources'])
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
    fig,ax=plt.subplots(figsize=(11,5.8));cs=sorted(data['uniform_large_size_certificates'][:3]+data['uniform_coverage_certificates'],key=lambda r:r['integer_size_min'])
    colors=[GREEN,GRAY,BLUE,PURPLE]
    for r,color in zip(cs,colors):
        n=r['integer_size_min'];g=float(F(r['gap_lower_exact']));ax.plot([n,120],[g,g],color=color,lw=2.6)
        ax.scatter([n],[g],color=color,s=55);ax.annotate('',xy=(122,g),xytext=(118,g),arrowprops={'arrowstyle':'->','color':color,'lw':2.6})
        ax.text(n+4,g+.00035,f"Δ ≥ {g:g}, every integer L ≥ {n}",color=color,fontsize=11)
    ax.set(xlim=(46,124),ylim=(0,.012),xlabel='Periodic microscopic spin count L',ylabel='Certified gap lower bound',title='Uniform spin-1 Heisenberg chain: independently accepted gaps')
    ax.set_xticks([48,52,56,60,80,100,120]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    ax.plot([48,96],[.0053,.0053],color=ORANGE,lw=2,ls='--');ax.text(65,.00565,'Finite 48–96 only: Δ ≥ .0053',color=ORANGE,fontsize=10)
    fig.text(.5,.065,'Unit bilinear exchange; all integers, including odd L. The strongest bound on overlaps may be selected.',ha='center',fontsize=10)
    fig.text(.5,.025,'Coverage starts at 48; infinite bootstrap initialization stays 52. No claim below 48 or minimum seed.',ha='center',fontsize=10)
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
        fig,ax=plt.subplots(figsize=(10.5,5.5));rs=[r for r in data['claims'] if r.get('certificate_route') in ['bilayer_direct_time_first_point','bilayer_frontier_above010_point','stage13_actual_point']]
        ax.scatter([float(F(r['parameter_exact'])) for r in rs],[float(F(r['gap_lower_exact'])) for r in rs],s=55,color=BLUE)
        for r in rs:
            f=F(r['gap_lower_exact']);six=f.numerator*10**6//f.denominator
            ax.annotate(f"{six//10**6}.{six%10**6:06d}",(float(F(r['parameter_exact'])),float(f)),xytext=(0,-20 if r['parameter_exact']=='1001/10000' else 12),textcoords='offset points',ha='center',fontsize=9)
        if data['stage12_frontier_interval_included']:
            g=float(F(data['stage12_frontier_interval']['verdict']['extension_uniform_gap']));ax.plot([.1,.102],[g,g],color=GREEN,lw=2.7);ax.text(.1009,g-.003,'Entire [.10,.102]: Δ ≥ .013574634391',ha='center',color=GREEN,fontsize=10)
        if data['stage13_interval_included']:
            ax.plot([.102,.105],[.017785998829]*2,color=PURPLE,lw=2.7);ax.text(.1035,.021,'Entire [.102,.105]: Δ ≥ .017785998829',ha='center',color=PURPLE,fontsize=9)
        ax.set(xlim=(.0998,.1053),ylim=(.006,.068),xlabel='Intralayer coupling g',ylabel='Certified gap lower bound',title='Ordinary bilayer: independently accepted frontier points')
        ax.set_xticks([.1000,.1010,.1020,.1030,.1040,.1050]);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
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
        ax.text(45,g+.0012,f"Conditional Δ ≥ {g:g}, every integer L ≥ 36",color=color,fontsize=11)
    ax.set(xlim=(32,104),ylim=(0,.027),xlabel='Periodic microscopic spin count L',ylabel='Conditional gap lower bound',title='Published second inputs: conditional scalar theorems only')
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    fig.text(.5,.065,'Premises: 18 published integer-total/error certificates at β=49/4. Full physical rerun is not established here.',ha='center',fontsize=10)
    fig.text(.5,.025,'Separate evidence category: these lines do not replace the locally accepted uniform-gap figure.',ha='center',fontsize=10)
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
    return matplotlib.__version__

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');ap.add_argument('--output-dir');args=ap.parse_args()
    if args.output_dir:OUT=Path(args.output_dir).resolve();OUT.mkdir(parents=True,exist_ok=True)
    elif not args.check_only:assert not (HERE/'MANIFEST_SHA256.json').exists(), 'Frozen snapshot: use --output-dir'
    data=json.loads((HERE/'overview_data.json').read_text());n=verify(data)
    info={'status':'PASS','claims':len(data['claims']),'finite_size_certificate_rows':len(data['finite_size_certificates']),'uniform_large_size_certificate_rows':len(data['uniform_large_size_certificates']),'dimension_rows':len(data['dimensions']),'stage13_dimension_rows':len(data['stage13_bilayer_dimensions']),'conditional_uniform_rows':len(data['conditional_uniform_certificates']),'bilayer_short_size_rows':len(data['bilayer_short_size_certificates']),'bilayer_ground_endpoint_rows':len(data['bilayer_ground_endpoint_certificates']),'accepted_full_thermal_cases':sum(r['full_physical_case_accepted'] for r in data['thermal_partial_cases']),'uniform_finite_window_rows':len(data['uniform_finite_windows']),'uniform_coverage_rows':len(data['uniform_coverage_certificates']),'direct_source_hashes':len(data['sources']),'review_seals':len(data['review_seals']),'sealed_file_hashes_checked':n,'combined_review_included':data['combined_review_included'],'interval_extension_included':data['interval_extension_included'],'cpu_affinity':sorted(os.sched_getaffinity(0)),'address_space_limit_bytes':1024**3,'blas_threads':1,'checks':['source SHA-256','complete selected review manifests','all exact gap JSON pointers','all decimal floors','best point selection','all exact adjacent closed pieces and uniform minimum','Hilbert dimensions','numerator rank separated from search and filtered span','failure gaps remain null','all 207 chain candidate routes','all exact interval pieces','historical59/139 and new64/139 denominator trial dimensions','reference67 versus unchanged M8 search','70 orthogonal MPS states with bond52 and necessary screen only','g010 diagnostic scope without gap promotion','separate AKLT projector reference','all stage14 files and all positive/conditional records preserved', 'finite-size g025 kept separate', 'pair symmetry erratum', '74-integer current and even/direct recipe scopes', 'four preserved uniform bounds; new finite48..96 bridge and all-integerL>=48 coverage with initialization52', 'historical66 and74 pieces preserved; current80-piece interval through .105', 'new direct point and fixed-family metadata erratum', 'original source n>=4 scope and theorem comparison', 'rank195 fixed early-window obstruction and strict decimal direction','scoped conditional error budgets; abstract unit-count rank; negative Rayleigh anchors; all-r canonical n48/n50 exclusion without minimum-seed claim','two conditional published-second-input bounds remain separate from locally accepted uniform family','three short-size bilayer rows only L2..7; no all-size frontier change','complete4x4 H2 fixture with conditional sector cutoff; no full8x4/no new gap','historical kernel/data-plane/supervisor engineering reviews retained unchanged','complete43D/57D physical H2 matrices and exact split compressions','physical ground endpoints separate from gap rows','16 exact physical thermal cases accepted; L12I/P incomplete;990 saved batches; conditional categories unchanged; frozen partial snapshot only']}
    if not args.check_only:
        info['matplotlib']=plot(data);info['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (OUT/'validation.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info))
