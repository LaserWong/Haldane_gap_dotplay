#!/usr/bin/env python3
"""Exact extraction checks, source seal verification, and reproducible static plots."""
import sys; sys.dont_write_bytecode=True
from common import *
import argparse,tempfile
os.environ['MPLCONFIGDIR']=tempfile.mkdtemp(prefix='haldane-stage7-mpl-')
os.environ['XDG_CACHE_HOME']=os.environ['MPLCONFIGDIR']
OUT=HERE
BLUE='#245f8b';GREEN='#2e7d49';ORANGE='#b85c21';GRAY='#5c6570';PURPLE='#735291'

def verify(data):
    accepted=json.loads((HERE/'ACCEPTED_REVIEW_SEALS.json').read_text())
    assert data['snapshot_label']=='stage7'
    assert {s['manifest']:s['sha256'] for s in data['review_seals']}==accepted
    for p,h in data['sources'].items():assert sha(ROOT/p)==h,('source changed',p)
    for p,h in data['preserved_stage6_files'].items():assert sha(ROOT/p)==h,('stage6 changed',p)
    count=0
    for seal in data['review_seals']:
        assert sha(ROOT/seal['manifest'])==seal['sha256']
        n=manifest_check(seal['manifest']);assert n==seal['verified_files'];count+=n
    rows=data['claims'];assert len({r['id'] for r in rows})==len(rows)
    previous=json.loads((ROOT/(R+'overview_stage6/overview_data.json')).read_text())
    lookup={r['id']:r for r in rows}
    for old in previous['claims']:
        new=lookup[old['id']]
        for k in ['gap_lower_exact','primary_source','primary_json_pointer','evidence_status','certificate_route','parameter_exact','parameter_lower_exact','integer_size_min','unit_coupling','boundary']:
            assert new.get(k)==old.get(k),('prior alternative changed',old['id'],k)
    assert len(data['dimensions'])>=len(previous['dimensions'])
    for i,old in enumerate(previous['dimensions']):
        assert all(data['dimensions'][i].get(k)==v for k,v in old.items())
    for name in ['tail_order_comparison.csv','fixed_order_tail_gains.csv','combined_route_comparison.csv','combined_selected_failures.csv']:
        assert sha(HERE/name)==sha(ROOT/(R+'overview_stage6/'+name))
    for r in rows:
        assert F(ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer']))==F(r['gap_lower_exact'])
        assert r['primary_sha256']==data['sources'][r['primary_source']]
        assert floor12(r['gap_lower_exact'])==r['gap_lower_decimal_down_12']
        assert F(r['gap_lower_exact'])>0 and r['integer_size_min']==2
        assert r['proof_family']=='thermal_bootstrap'
        if r['snapshot_stage']=='stage7':
            src=json.loads((ROOT/r['primary_source']).read_text())
            assert F(ptr(src,r['parameter_source_pointer']))==F(r['parameter_exact'])
            if r['parameter_kind']=='closed_interval':assert F(ptr(src,r['parameter_lower_source_pointer']))==F(r['parameter_lower_exact'])
        if r['parameter_kind']=='point' and r['plotted_in_main_figure']:
            assert all(F(r['gap_lower_exact'])>=F(a['gap_lower_exact']) for a in rows if a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'])
        if r['model']=='ordinary_spinhalf_bilayer':assert F(r['parameter_exact'])<=F('17/200')
    pieces=sorted([r for r in rows if r.get('certificate_route') in data['ordinary_interval_piece_routes']],key=lambda r:F(r['parameter_lower_exact']))
    assert len(pieces)==data['ordinary_interval_piece_count']==49
    assert F(pieces[0]['parameter_lower_exact'])==0 and F(pieces[-1]['parameter_exact'])==F(data['ordinary_interval_endpoint'])==F('17/200')
    assert all(F(a['parameter_exact'])==F(b['parameter_lower_exact']) for a,b in zip(pieces,pieces[1:]))
    uniform=max([r for r in rows if r.get('certificate_route')=='uniform_interval_union'],key=lambda r:F(r['parameter_exact']))
    assert F(uniform['gap_lower_exact'])==min(F(r['gap_lower_exact']) for r in pieces)==F('486442811/250000000000')
    assert len([r for r in pieces if F(r['parameter_exact'])<=F('41/500')])==40
    assert len([r for r in pieces if F(r['parameter_lower_exact'])>=F('41/500')])==9
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
            if i==0 and x in [.175,.182,.2]:
                dx,dy,ha=(0,13,'center')
                if x==.16125:dx,dy,ha=-5,-15,'right'
                if x==.175:dx,dy,ha=-8,2,'right'
                if x==.182:dx,dy,ha=4,-13,'left'
                ax.annotate(f'{x:g}',(x,y),xytext=(dx,dy),textcoords='offset points',ha=ha,va='center',fontsize=9,arrowprops={'arrowstyle':'-','lw':.6,'color':GRAY})
            if i==1 and r['parameter_kind']=='point' and x==.085:
                ax.annotate('0.085',(x,y),xytext=(0,10),textcoords='offset points',ha='center',fontsize=9)
        if i==0:
            ax.set_xlim(.038,.21);ax.set_ylim(.0007,.23);ax.set_xticks([.05,.10,.15,.20]);ax.set_ylabel('Certified gap lower bound')
            ax.text(.03,.025,'Every integer cell count M ≥ 2',transform=ax.transAxes,fontsize=10)
        elif i==1:
            ax.set_xlim(-.004,.091);ax.set_ylim(.0011,.70);ax.set_xticks([0,.02,.04,.06,.08] if data['combined_review_included'] else [0,.02,.04,.06,.07])
            ax.annotate('Entire 0 ≤ g ≤ 0.085'+'\nΔ ≥ 0.001945771244',(.036,.001945771244),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10,color=GREEN)
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
    ax.set_yscale('log');ax.set_ylim(.0012,.7);ax.set_xlim(-.001,hi+.001);ax.set_xticks([0,.01,.02,.03,.04,.05,.06,.07]+[.085]);ax.set_xlabel('Intralayer coupling g');ax.set_ylabel('Certified gap lower bound')
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y,p:f'{y:g}'));ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    fig.text(.5,.025,'Green: ground-only denominators through .082. Orange: complete smaller odd bands on [.082,.085]. Every segment covers all integer L ≥ 2.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.10,right=.98,bottom=.16,top=.88)
    save(fig,'ordinary_interval_pieces',plt)

    fig,axes=plt.subplots(1,3,figsize=(18,6.5),gridspec_kw={'width_ratios':[1,1.2,1.1]})
    geometry=['4 × 4','8 × 4','8 × 8'];physical=[2**32,2**64,2**128]
    ax=axes[0];ax.barh(range(3),[float(v) for v in physical],color=BLUE,height=.48);ax.set_yticks(range(3),[f'{s} rungs\n{n} spins' for s,n in zip(geometry,[32,64,128])]);ax.invert_yaxis();ax.set_xscale('log');ax.set_xlim(1,float(2**143));ax.set_xticks([1,1e12,1e24,1e36]);ax.set_title('Physical Hilbert dimension',pad=15);ax.set_xlabel('Number of states (log scale)')
    for i,(n,v) in enumerate(zip([32,64,128],physical)):ax.text(v*1.8,i,f'2^{n}',va='center',fontsize=11)
    ax=axes[1];ys=[0,1,2]
    ax.barh([x-.24 for x in ys],[11,29,29],height=.21,color=BLUE,label='Original ground search')
    ax.barh(ys,[59,125,30],height=.21,color=PURPLE,label='Total trial space / upper bound')
    ax.barh([x+.24 for x in ys],[49,97,1],height=.21,color=GREEN,label='Trace states / numerator contributions')
    ax.set_yticks(ys,geometry);ax.invert_yaxis();ax.set_xlim(0,150);ax.set_title('Final interval [.082, .085]',pad=15);ax.set_xlabel('Distinct linear / trace counts')
    for i,values in enumerate(zip([11,29,29],[59,125,30],[49,97,1])):
        for off,v in zip([-.24,0,.24],values):ax.text(v+2,i+off,('≤' if i==2 and off==0 else '')+str(v),va='center',fontsize=10)
    ax.legend(frameon=False,loc='upper center',fontsize=9,bbox_to_anchor=(.5,-.15))
    ax=axes[2];values=[1,29,30,193];labels=['One numerator contribution','Original ground search','Filtered span (upper)','Separate full-band route']
    ax.barh(range(4),values,color=[GREEN,BLUE,PURPLE,GRAY],height=.45);ax.set_yticks(range(4),labels);ax.invert_yaxis();ax.set_xscale('log');ax.set_xlim(.8,430);ax.set_xticks([1,10,100]);ax.get_xaxis().set_major_formatter(mticker.ScalarFormatter());ax.set_xlabel('Different quantities (log scale)');ax.set_title('Largest 8 × 8 patch',pad=15)
    for i,v in enumerate(values):ax.text(v*1.1,i,('≤' if i==2 else '')+str(v),va='center',fontsize=11)
    for ax in axes:ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.092,'Final denominator spaces: 11 + 48 = 59 and 29 + 96 = 125. Ground-only continuum reaches .082.',ha='center',fontsize=11)
    fig.text(.5,.052,'The largest numerator has dimension ≤30; 30 is not the maximum search/trial dimension across the whole .085 pipeline.',ha='center',fontsize=11)
    fig.text(.5,.014,'Rank one is not a one-dimensional search. These bilayer counts are not MPS bond dimensions. No moments beyond H² enter the .085 continuum.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.073,right=.965,bottom=.34,top=.85,wspace=.87)
    save(fig,'trial_space_counts',plt)

    fig,ax=plt.subplots(figsize=(12.5,4.1));ax.axis('off')
    ax.text(.5,.94,'AKLT: separately proved entangled reference',ha='center',fontsize=20,color=BLUE)
    ax.text(.5,.78,'H = sum of nearest-neighbor spin-2 projectors (coefficient 1)',ha='center',fontsize=13)
    ax.text(.5,.58,'Periodic gap ≥ 1/10 for every L ≥ 5',ha='center',fontsize=23,color=GREEN)
    ax.text(.5,.44,'Unique ground state for L ≥ 3; complete omitted-state count = 3^L − 1',ha='center',fontsize=13)
    ax.text(.5,.26,'MPS bond D = 2    •    One retained state    •    Local proof matrix 81 × 81',ha='center',fontsize=13)
    ax.text(.5,.12,'Finite-size projector criterion. Current thermal-transfer sufficiency fails.',ha='center',fontsize=12,color=ORANGE)
    ax.text(.5,.02,'This is not a thermal-bootstrap certificate or a bilinear-Heisenberg spectral-transfer result.',ha='center',fontsize=11)
    save(fig,'aklt_reference_scope',plt)
    return matplotlib.__version__

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');ap.add_argument('--output-dir');args=ap.parse_args()
    if args.output_dir:OUT=Path(args.output_dir).resolve();OUT.mkdir(parents=True,exist_ok=True)
    elif not args.check_only:assert not (HERE/'MANIFEST_SHA256.json').exists(), 'Frozen snapshot: use --output-dir'
    data=json.loads((HERE/'overview_data.json').read_text());n=verify(data)
    info={'status':'PASS','claims':len(data['claims']),'dimension_rows':len(data['dimensions']),'direct_source_hashes':len(data['sources']),'review_seals':len(data['review_seals']),'sealed_file_hashes_checked':n,'combined_review_included':data['combined_review_included'],'interval_extension_included':data['interval_extension_included'],'cpu_affinity':sorted(os.sched_getaffinity(0)),'address_space_limit_bytes':1024**3,'blas_threads':1,'checks':['source SHA-256','complete selected review manifests','all exact gap JSON pointers','all decimal floors','best point selection','all exact adjacent closed pieces and uniform minimum','Hilbert dimensions','numerator rank separated from search and filtered span','failure gaps remain null','all 207 chain candidate routes','all 49 interval pieces','59/125 denominator trial dimensions','separate AKLT projector reference','all stage6 files preserved']}
    if not args.check_only:
        info['matplotlib']=plot(data);info['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (OUT/'validation.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info))
