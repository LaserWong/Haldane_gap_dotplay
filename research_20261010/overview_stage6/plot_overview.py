#!/usr/bin/env python3
"""Exact extraction checks, source seal verification, and reproducible static plots."""
from common import *
import argparse,tempfile
os.environ['MPLCONFIGDIR']=tempfile.mkdtemp(prefix='haldane-stage6-mpl-')
os.environ['XDG_CACHE_HOME']=os.environ['MPLCONFIGDIR']
OUT=HERE
BLUE='#245f8b';GREEN='#2e7d49';ORANGE='#b85c21';GRAY='#5c6570';PURPLE='#735291'

def verify(data):
    for p,h in data['sources'].items():assert sha(ROOT/p)==h,('source changed',p)
    count=0
    for seal in data['review_seals']:
        assert sha(ROOT/seal['manifest'])==seal['sha256']
        n=manifest_check(seal['manifest']);assert n==seal['verified_files'];count+=n
    rows=data['claims'];assert len({r['id'] for r in rows})==len(rows)
    for r in rows:
        assert F(ptr(json.loads((ROOT/r['primary_source']).read_text()),r['primary_json_pointer']))==F(r['gap_lower_exact'])
        assert r['primary_sha256']==data['sources'][r['primary_source']]
        assert floor12(r['gap_lower_exact'])==r['gap_lower_decimal_down_12']
        assert F(r['gap_lower_exact'])>0 and r['integer_size_min']==2
        if r['parameter_kind']=='point' and r['plotted_in_main_figure']:
            assert all(F(r['gap_lower_exact'])>=F(a['gap_lower_exact']) for a in rows if a['model']==r['model'] and a['parameter_kind']=='point' and a['parameter_exact']==r['parameter_exact'])
    pieces=sorted([r for r in rows if r.get('certificate_route') in ['uniform_interval_piece','filtered_interval_extension_piece']],key=lambda r:F(r['parameter_lower_exact']))
    expected_n=31 if data['interval_extension_included'] else 16
    expected_hi=F('39/500') if data['interval_extension_included'] else F('7/100')
    assert len(pieces)==expected_n and F(pieces[0]['parameter_lower_exact'])==0 and F(pieces[-1]['parameter_exact'])==expected_hi
    assert all(F(a['parameter_exact'])==F(b['parameter_lower_exact']) for a,b in zip(pieces,pieces[1:]))
    uniform=max([r for r in rows if r.get('certificate_route')=='uniform_interval_union'],key=lambda r:F(r['parameter_exact']))
    assert F(uniform['gap_lower_exact'])==min(F(r['gap_lower_exact']) for r in pieces)
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
    assert all(r['gap_lower_exact'] is None and not r['plotted_as_zero_gap'] for r in data['unplotted_status'])
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
            if i==0 and x>=.16:
                dx,dy,ha=(-8,0,'right')
                if x==.1615:dx,dy,ha=-19,15,'right'
                if x==.1625:dx,dy,ha=12,-13,'left'
                if x==.175:dx,dy,ha=3,12,'left'
                ax.annotate(f'{x:g}',(x,y),xytext=(dx,dy),textcoords='offset points',ha=ha,va='center',fontsize=9,arrowprops={'arrowstyle':'-','lw':.6,'color':GRAY} if x in [.1615,.1625] else None)
        if i==0:
            ax.set_xlim(.038,.19);ax.set_ylim(.0007,.23);ax.set_xticks([.05,.10,.15,.175]);ax.set_ylabel('Certified gap lower bound')
            ax.text(.03,.025,'Every integer cell count M ≥ 2',transform=ax.transAxes,fontsize=10)
        elif i==1:
            ax.set_xlim(-.004,.085 if data['combined_review_included'] else .076);ax.set_ylim(.0011,.70);ax.set_xticks([0,.02,.04,.06,.08] if data['combined_review_included'] else [0,.02,.04,.06,.07])
            ax.annotate(('Entire 0 ≤ g ≤ 0.078' if data['interval_extension_included'] else 'Entire 0 ≤ g ≤ 0.07')+'\nΔ ≥ 0.001945771244',(.036,.001945771244),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10,color=GREEN)
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

    pieces=sorted([r for r in data['claims'] if r.get('certificate_route') in ['uniform_interval_piece','filtered_interval_extension_piece']],key=lambda r:F(r['parameter_lower_exact']))
    fig,ax=plt.subplots(figsize=(12.5,5.8))
    ax.set_title(f'Ordinary bilayer: all {len(pieces)} certified closed parameter pieces',pad=15)
    for i,r in enumerate(pieces):
        lo,hi,y=map(float,[F(r['parameter_lower_exact']),F(r['parameter_exact']),F(r['gap_lower_exact'])])
        ax.plot([lo,hi],[y,y],color=GREEN,lw=2.8);ax.scatter([lo,hi],[y,y],s=19,color=GREEN,zorder=3)
    u=max([r for r in data['claims'] if r.get('certificate_route')=='uniform_interval_union'],key=lambda r:F(r['parameter_exact']));v=float(F(u['gap_lower_exact']));hi=float(F(u['parameter_exact']))
    ax.plot([0,hi],[v,v],color=PURPLE,lw=2.3);ax.plot([0,hi],[v,v],marker='|',ms=11,mew=2,color=PURPLE,ls='none')
    ax.annotate('Uniform on the whole union: 0.001945771244',(.014,v),xytext=(0,12),textcoords='offset points',fontsize=11,color=PURPLE)
    ax.set_yscale('log');ax.set_ylim(.0012,.7);ax.set_xlim(-.001,hi+.001);ax.set_xticks([0,.01,.02,.03,.04,.05,.06,.07]+([.078] if data['interval_extension_included'] else []));ax.set_xlabel('Intralayer coupling g');ax.set_ylabel('Certified gap lower bound')
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y,p:f'{y:g}'));ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    fig.text(.5,.025,'Each green segment proves its entire closed interval for every integer L ≥ 2. Bounds need not vary monotonically; no fitted curve is used.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.10,right=.98,bottom=.16,top=.88)
    save(fig,'ordinary_interval_pieces',plt)

    fig,axes=plt.subplots(1,3,figsize=(17.6,6.2),gridspec_kw={'width_ratios':[1,1,1.1]})
    geometry=['4 × 4','8 × 4','8 × 8'];physical=[2**32,2**64,2**128]
    ax=axes[0];ax.barh(range(3),[float(v) for v in physical],color=BLUE,height=.48);ax.set_yticks(range(3),[f'{s} rungs\n{n} spins' for s,n in zip(geometry,[32,64,128])]);ax.invert_yaxis();ax.set_xscale('log');ax.set_xlim(1,float(2**143));ax.set_xticks([1,1e12,1e24,1e36]);ax.set_title('Physical Hilbert dimension',pad=15);ax.set_xlabel('Number of states (log scale)')
    for i,(n,v) in enumerate(zip([32,64,128],physical)):ax.text(v*1.8,i,f'2^{n}',va='center',fontsize=11)
    ax=axes[1];ys=[0,1,2]
    ax.barh([x-.16 for x in ys],[11,29,29],height=.28,color=BLUE,label='Original search')
    ax.barh([x+.16 for x in ys],[12,30,30],height=.28,color=PURPLE,label='Filtered span upper bound')
    ax.set_yticks(ys,geometry);ax.invert_yaxis();ax.set_xlim(0,37);ax.set_title('Search and implicit filtered span',pad=15);ax.set_xlabel('Linear-space dimension')
    for i,(a,b) in enumerate(zip([11,29,29],[12,30,30])):
        ax.text(a+.7,i-.16,str(a),va='center',fontsize=11);ax.text(b+.7,i+.16,'≤'+str(b),va='center',fontsize=11)
    ax.legend(frameon=False,loc='lower right',fontsize=9,bbox_to_anchor=(1,-.27))
    ax=axes[2];values=[1,29,30,193];labels=['One numerator trial','Original ground search','Filtered span (upper)','Complete-band route']
    ax.barh(range(4),values,color=[GREEN,BLUE,PURPLE,GRAY],height=.45);ax.set_yticks(range(4),labels);ax.invert_yaxis();ax.set_xscale('log');ax.set_xlim(.8,400);ax.set_xticks([1,10,100]);ax.get_xaxis().set_major_formatter(mticker.ScalarFormatter());ax.set_xlabel('Different quantities (log scale)');ax.set_title('Largest 8 × 8 patch: distinct counts',pad=15)
    for i,v in enumerate(values):ax.text(v*1.1,i,('≤' if i==2 else '')+str(v),va='center',fontsize=11)
    for ax in axes:ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.10,'Filtering adds at most one implicit residual direction. Original support has q ≤ 4; the filtered trial has q ≤ 6.',ha='center',fontsize=11)
    if data['interval_extension_included']:fig.text(.5,.063,'The continuous extension filters only the largest numerator, giving working dimensions 11/29/≤30.',ha='center',fontsize=10)
    fig.text(.5,.027,'Rank one is not a one-dimensional search. Filtered largest input uses existing G/K/J; the earlier reduced largest input uses G/K.',ha='center',fontsize=10)
    fig.text(.5,-.005,'No displayed count is an MPS bond dimension. The 193-state complete band is not required by the rank-one numerator proof.',ha='center',fontsize=10)
    fig.subplots_adjust(left=.075,right=.975,bottom=.31,top=.86,wspace=.72)
    save(fig,'trial_space_counts',plt)
    return matplotlib.__version__

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');ap.add_argument('--output-dir');args=ap.parse_args()
    if args.output_dir:OUT=Path(args.output_dir).resolve();OUT.mkdir(parents=True,exist_ok=True)
    data=json.loads((HERE/'overview_data.json').read_text());n=verify(data)
    info={'status':'PASS','claims':len(data['claims']),'dimension_rows':len(data['dimensions']),'direct_source_hashes':len(data['sources']),'review_seals':len(data['review_seals']),'sealed_file_hashes_checked':n,'combined_review_included':data['combined_review_included'],'interval_extension_included':data['interval_extension_included'],'cpu_affinity':sorted(os.sched_getaffinity(0)),'address_space_limit_bytes':1024**3,'blas_threads':1,'checks':['source SHA-256','complete selected review manifests','all exact gap JSON pointers','all decimal floors','best point selection','all exact adjacent closed pieces and uniform minimum','Hilbert dimensions','numerator rank separated from search and filtered span','failure gaps remain null']}
    if not args.check_only:
        info['matplotlib']=plot(data);info['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        (OUT/'validation.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info))
