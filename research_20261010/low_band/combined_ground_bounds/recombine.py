"""Recombine frozen ground lower/variational upper bounds with existing bands.

All resulting claims remain candidates until both new physical lemmas and this
scalar recombination are independently reviewed. No physical vectors or moments
are generated here. The three filtered upper endpoints refer to implicit even
trial vectors, while excited Ritz upper endpoints and completeness stay fixed.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,argparse,copy
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RESEARCH=BAND.parent
sys.path.insert(0,str(BAND/'tail_comparison'))
import integrate_tails as I
from scan_transported import stages,score


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def verify_manifest(path):
    data=json.loads(path.read_text())
    entries=data.get('files',data)
    assert isinstance(entries,dict) and entries
    checked=0
    for name,expected in entries.items():
        if not isinstance(expected,str) or len(expected)!=64:
            continue
        file=path.parent/name
        assert file.is_file(),(path,name)
        assert digest(file)==expected,(path,name,'hash mismatch')
        checked+=1
    assert checked>0,(path,'no hash entries recognized')
    return digest(path)


def patch(nx,ny,g,variant,out):
    tag=f'{nx}x{ny}_g{g}'.replace('/','d')
    if variant=='combined':
        base=BAND/'ground_moment_pencil'/f'temple_{tag}.json'
    elif g<=F(3,50):
        base=BAND/'tail_comparison'/'quadratic'/f'temple_{tag}.json'
    else:
        base=BAND/'frontier_g007_g010'/f'g{g}'.replace('/','d')/f'temple_{tag}.json'
    fp=RESEARCH/'variational_numerator_filter'/f'filtered_{tag}.json'
    rec=json.loads(base.read_text());filtered=json.loads(fp.read_text())
    assert F(rec['g'])==g==F(filtered['coupling'])
    assert [rec['nx'],rec['ny']]==[nx,ny]==[filtered['nx'],filtered['ny']]
    assert F(rec['energy_shift'])==F(filtered['energy_shift'])
    old=F(rec['blocks'][0]['eigen_upper'][0])
    assert old==F(filtered['exact_original_shifted_rayleigh'])
    upper=F(filtered['shifted_rayleigh_upper']);lower=F(rec['blocks'][0]['eigen_lower'][0])
    assert lower<=upper<=old
    rec['blocks'][0]['unfiltered_eigen_upper']=rec['blocks'][0]['eigen_upper'][:]
    rec['blocks'][0]['eigen_upper']=[str(upper)]
    rec['blocks'][0]['upper_endpoint_meaning']='Certified upper bound for the Rayleigh quotient of an implicit filtered even singlet trial; Jensen supplies a trace lower term.'
    rec['ground_width']=str(upper-lower)
    rec['status']='combined_ground_bound_candidate_pending_independent_review'
    rec['combination_variant']=variant
    rec['new_trial_residual_claim']=False
    rec['recombination_source_sha256']={str(p.relative_to(RESEARCH)):digest(p) for p in (base,fp)}
    (out/f'patch_{tag}.json').write_text(json.dumps(rec,indent=2)+'\n')
    return rec


def exact_selected(recs,beta,order,short):
    st=stages(recs,beta,order,True)
    assert all(0<F(st[key])<=1 for key in ('J1','J2','C0'))
    if 'canonical' in st:
        return I.exact_seed(recs,beta,order,short)
    return dict(beta_initial=str(beta),order_before_transport=order,accepted=False,
        J1=str(st['J1']),J2=str(st['J2']),C0=str(st['C0']),
        permuted_prefix=list(map(str,st['permuted_prefix'])))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pencil-manifest',type=Path,required=True)
    ap.add_argument('--filter-manifest',type=Path,required=True)
    ap.add_argument('--variant',choices=['filter_only','combined'],default='combined')
    ap.add_argument('--couplings',default='2/25,1/10,3/100,1/25,1/20,3/50,7/100')
    args=ap.parse_args()
    manifests=[p.resolve() for p in (args.pencil_manifest,args.filter_manifest)]
    assert all(p.is_file() for p in manifests)
    for p in manifests:verify_manifest(p)
    out=HERE/args.variant;out.mkdir(exist_ok=True)
    short10path=BAND/'frontier_g007_g010'/'short_sizes'/'uniform_short_sizes.json'
    short10=F(json.loads(short10path.read_text())['gap_lower'])
    short06path=BAND/'frontier_g006'/'all_size_bridges.json'
    short06=min(F(row['gap_lower']) for row in json.loads(short06path.read_text())[0]['small_sizes'])
    summaries=[]
    for g in map(F,args.couplings.split(',')):
        recs=[patch(nx,ny,g,args.variant,out) for nx,ny in ((4,4),(8,4),(8,8))]
        short=short06 if g<=F(3,50) else short10
        shortpath=short06path if g<=F(3,50) else short10path
        rows=[]
        for order in ('txy','xty','xyt'):
            candidates=[];best_prefix=None
            for bi in range(100,601):
                beta=F(bi,20);st=stages(recs,float(beta),order)
                assert max(st[k] for k in ('J1','J2','C0'))<=1+1e-12
                rank=(st['positive_steps'],min(st.get('canonical',st['permuted_prefix'])))
                if best_prefix is None or rank>best_prefix[0]:best_prefix=(rank,beta,st)
                candidates.append((score(st,float(beta)),beta))
            value,beta=min(candidates)
            if value>=0:beta=best_prefix[1]
            row=exact_selected(recs,beta,order,short)
            row.update(accepted_float_proposals=sum(v<0 for v,_ in candidates),best_float_score=value)
            if row.get('accepted') and order=='txy':
                # Largest numerator alone needs only an even trial. Removing
                # all optional odd trial terms is a separate exact candidate.
                ground_only=copy.deepcopy(recs)
                ground_only[2]['blocks']=ground_only[2]['blocks'][:1]
                row['largest_ground_only_replay']=exact_selected(ground_only,beta,order,short)
            rows.append(row)
            print(args.variant,g,order,beta,row.get('all_integer_gap_display'),flush=True)
        result=dict(g=str(g),status='candidate_pending_independent_review',variant=args.variant,
            grid_scope='beta5..30 step.05; three proved transported orders; failures are bounded searches only',
            results=rows,source_sha256={str(p.relative_to(RESEARCH)):digest(p) for p in manifests+[shortpath]},
            new_physical_input='None: existing exact ground G/K/J plus geometry and certified filter compression',
            normalization_note='Denominator Rayleigh shifts cancel from the physical trace upper; their lower endpoints control its ground term.')
        (out/f'combined_g{g}.json'.replace('/','d')).write_text(json.dumps(result,indent=2)+'\n')
        summaries.append(result)
    (out/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n')


if __name__=='__main__':main()
