#!/usr/bin/env python3
"""Render static figures from frozen exact data; hash-check the evidence first."""
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
if hasattr(os, 'sched_getaffinity'):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
import resource
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
import tempfile
_CACHE = os.path.join(tempfile.gettempdir(), 'haldane-overview-matplotlib')
os.makedirs(_CACHE, exist_ok=True)
os.environ['MPLCONFIGDIR'] = _CACHE
os.environ['XDG_CACHE_HOME'] = _CACHE
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BLUE, GREEN, ORANGE, GRAY = '#245f8b', '#2e7d49', '#b85c21', '#5c6570'


def read_pointer(doc, pointer):
    for t in pointer.strip('/').split('/') if pointer else []:
        t = t.replace('~1','/').replace('~0','~')
        doc = doc[int(t)] if isinstance(doc, list) else doc[t]
    return doc


def verify(data):
    for path, expected in data['sources'].items():
        observed = hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        if observed != expected:
            raise ValueError(f'Evidence changed: {path}. Review the change before rebuilding.')
    for row in data['claims']:
        doc = json.loads((ROOT/row['primary_source']).read_text())
        assert F(read_pointer(doc,row['primary_json_pointer'])) == F(row['gap_lower_exact'])
        assert F(row['gap_lower_decimal_down_12']) <= F(row['gap_lower_exact'])
        assert F(row['gap_lower_exact']) > 0
        assert row['integer_size_min'] == 2
    for row in data['dimensions']:
        read_pointer(json.loads((ROOT/row['evidence_source']).read_text()), row['evidence_json_pointer'])
        n = int(row['seed_geometry'][2:]) if row['seed_geometry'].startswith('M=') else None
        if n is not None:
            assert row['full_Hilbert_dimension'] == 9**n
        else:
            a,b = map(int,row['seed_geometry'].split('x'))
            assert row['full_Hilbert_dimension'] == 4**(a*b)
        for key in ('retained_low_band_count','proposal_basis_dimension','expanded_vector_support','full_H_applied_support'):
            assert row[key] is None or 0 < row[key] <= row['full_Hilbert_dimension']
        assert row['MPS_bond_dimension'] is None
    assert all(r['gap_lower_exact'] is None for r in data['unplotted_status'])
    assert len(data['claims']) == 27
    assert len({r['id'] for r in data['claims']}) == len(data['claims'])


def save(fig, stem, plt):
    fig.savefig(HERE/f'{stem}.png', dpi=180, facecolor='white')
    fig.savefig(HERE/f'{stem}.pdf', facecolor='white', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def plot(data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    from matplotlib.lines import Line2D
    plt.rcParams.update({'font.size': 12, 'axes.titlesize': 16, 'axes.labelsize': 13,
                         'xtick.labelsize': 11, 'ytick.labelsize': 11,
                         'pdf.fonttype': 42, 'savefig.bbox': 'tight'})
    models=['alternating_spin1_chain','ordinary_spinhalf_bilayer','fully_frustrated_bilayer']
    titles=['Spin-1 alternating chain', 'Ordinary spin-1/2 bilayer', 'Near fully frustrated bilayer']
    fig,axes=plt.subplots(1,3,figsize=(15.6,5.5))
    for i,(ax,model,title) in enumerate(zip(axes,models,titles)):
        rows=[r for r in data['claims'] if r['model']==model and r['plotted_in_main_figure']]
        ax.set_title(title,pad=15)
        ax.set_yscale('log')
        ax.set_xlabel('Weak coupling g' if i<2 else 'Perturbation ε  (J = 0.3)')
        ax.spines[['top','right']].set_visible(False)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y,p:f'{y:g}'))
        ax.yaxis.set_minor_formatter(mticker.NullFormatter())
        for r in rows:
            x=float(F(r['parameter_exact']));y=float(F(r['gap_lower_exact']))
            if r['parameter_kind']=='closed_interval':
                lo=float(F(r['parameter_lower_exact']))
                ax.plot([lo,x],[y,y],color=GREEN,lw=2.3,solid_capstyle='butt')
                ax.plot([lo,x],[y,y],ls='none',marker='|',color=GREEN,ms=9,mew=2)
            elif r['evidence_status'].startswith('root_scalar'):
                ax.scatter(x,y,marker='^',s=75,facecolors='white',edgecolors=ORANGE,linewidths=1.8,zorder=4)
            else:
                ax.scatter(x,y,color=BLUE,s=47,zorder=4)
            if i==0 and x>=0.16:
                ax.annotate(f'{x:g}',(x,y),xytext=(-9,0),textcoords='offset points',ha='right',va='center',fontsize=10)
        if i==0:
            ax.set_xlim(.035,.18);ax.set_ylim(.0007,.22);ax.set_xticks([.05,.1,.15])
            ax.set_ylabel('Certified gap lower bound')
            ax.text(.03,.03,'Every integer M ≥ 2',transform=ax.transAxes,fontsize=11)
        elif i==1:
            ax.set_xlim(.005,.055);ax.set_ylim(.035,.5);ax.set_xticks([.01,.03,.05])
            ax.annotate('0.282017228092',(.03,.282017228092),xytext=(0,12),textcoords='offset points',ha='center',fontsize=11)
            ax.text(.03,.03,'Every integer L ≥ 2',transform=ax.transAxes,fontsize=11)
        else:
            anchor=data['analytic_reference']
            ax.scatter(0,float(F(anchor['gap_lower_exact'])),marker='*',color=GRAY,s=110,zorder=4)
            ax.annotate('ε = 0: 0.4',(0,.4),xytext=(9,0),textcoords='offset points',va='center',fontsize=11)
            ax.set_xlim(-.00045,.0091);ax.set_ylim(.0004,.75)
            ax.set_xticks([0,.004,.008]);ax.ticklabel_format(axis='x',style='plain')
            ax.text(.03,.03,'Every integer square L ≥ 2',transform=ax.transAxes,fontsize=11)
    handles=[Line2D([],[],ls='none',marker='o',color=BLUE,label='Independently reviewed point'),
             Line2D([],[],color=GREEN,lw=2.3,label='Proved uniform ε interval'),
             Line2D([],[],ls='none',marker='^',mfc='white',mec=ORANGE,mew=1.6,label='Scalar bridge + audited inputs'),
             Line2D([],[],ls='none',marker='*',color=GRAY,label='Analytic reference')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.065),ncol=2,frameon=False,fontsize=11)
    fig.text(.5,.025,'Points certify individual parameters; horizontal bars certify entire intervals.',ha='center',fontsize=11)
    fig.subplots_adjust(left=.075,right=.98,top=.88,bottom=.27,wspace=.36)
    save(fig,'certified_bounds',plt)

    # These categories measure different objects; the ordinary-bilayer support entries describe only its ground proposal.
    select=[next(d for d in data['dimensions'] if d['model']==models[0] and d['parameter_exact']=='129/800' and d['seed_geometry']=='M=8'),
            next(d for d in data['dimensions'] if d['model']==models[1] and d['parameter_exact']=='3/100' and d['seed_geometry']=='8x8'),
            next(d for d in data['dimensions'] if d['model']==models[2] and d['parameter_exact'].startswith('0<=epsilon<=171/20000') and d['seed_geometry']=='4x4')]
    keys=['full_Hilbert_dimension','retained_low_band_count','proposal_basis_dimension','expanded_vector_support','full_H_applied_support']
    labels=['Full Hilbert','Retained states','Proposal basis','Expanded support','H-applied support']
    fig,axes=plt.subplots(1,3,figsize=(17,5.2))
    subtitles=['Chain: g = 0.16125, M = 8', 'Ordinary bilayer: g = 0.03, 8 × 8', 'FF interval: ε ≤ 0.00855, 4 × 4']
    for ax,d,title in zip(axes,select,subtitles):
        vals=[d[k] for k in keys]
        local_labels=list(labels)
        if d['seed_geometry']=='8x8':
            vals[3:]=[d['translated_column_support'],d['translated_H_applied_support']]
            local_labels=['Full Hilbert','Retained band','Ground proposal','Triplet column','H-applied column']
        ax.barh(range(5),[float(v) for v in vals],color=BLUE,height=.5)
        ax.set_yticks(range(5),local_labels);ax.invert_yaxis()
        ax.set_xscale('log');ax.set_xlim(.5,float(max(vals))*70)
        ax.set_xticks([1,1e12,1e24,1e36] if d['seed_geometry']=='8x8' else [1,1e3,1e6,1e9]);ax.set_xlabel('Count (log scale)')
        ax.set_title(title,fontsize=14,pad=16)
        ax.spines[['top','right']].set_visible(False)
        for y,v in enumerate(vals):ax.text(v*1.2,y,'2¹²⁸' if v==2**128 else f'{v:,}',va='center',fontsize=10)
    fig.text(.5,.06,'Ordinary bilayer: 29 ground-proposal vectors; 193 retained states; support counts describe one translated triplet column.',ha='center',fontsize=11)
    fig.text(.5,.015,'These are different dimensions. None is an MPS bond dimension; no MPS ansatz is used in these three certificates.',ha='center',fontsize=11)
    fig.subplots_adjust(left=.09,right=.98,bottom=.23,top=.83,wspace=.62)
    save(fig,'trial_space_counts',plt)
    result=dict(status='passed',claims=len(data['claims']),dimension_rows=len(data['dimensions']),source_hashes=len(data['sources']),
                matplotlib=matplotlib.__version__,cpu_affinity=sorted(os.sched_getaffinity(0)) if hasattr(os,'sched_getaffinity') else None,
                address_space_limit_bytes=1024**3,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                checks=['all evidence hashes','every primary exact fraction','decimal displays rounded down','full Hilbert dimensions and dimension source pointers','pending/failure gaps null'])
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');args=ap.parse_args()
    data=json.loads((HERE/'overview_data.json').read_text());verify(data)
    if args.check_only: print(f'PASS: {len(data["sources"])} source hashes and {len(data["claims"])} exact gap pointers.')
    else: plot(data)
