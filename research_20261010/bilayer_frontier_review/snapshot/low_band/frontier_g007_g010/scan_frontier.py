"""Exact bounded scans after all physical cutoff/residual checks pass."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
sys.path.insert(0,str(BAND/'tail_comparison'));sys.path.insert(0,str(BAND/'quadratic_boson'))
import integrate_tails as I
import quadratic_bins as Q
from scan_transported import stages,score


def main():
    shortdir=HERE/'short_sizes';shortdir.mkdir(exist_ok=True);Q.HERE=shortdir
    q=Q.certify(7,7,F(1,10));short=F(q['bins'][1]['lower'])
    shortrec=dict(status='uniform_short_size_comparison_pending_independent_review',g_max='1/10',
       sides=list(range(2,8)),weighted_edge_square_sums=[16,18,32,50,72,98],max_weighted_edge_square_sum=98,
       alpha_lower=q['alpha'],delta_lower=q['delta_lower'],vacuum_creation_norm_squared_upper=q['vacuum_creation_norm_squared'],
       gap_lower=str(short),proof='For every L2..7 and g<=.1, alpha>=.8, ||K||<=.2 and v<=.735; oscillator lambda2>=Eb+delta. Product trial gives lambda1<=0.')
    (shortdir/'uniform_short_sizes.json').write_text(json.dumps(shortrec,indent=2))
    original_read=I.read;summary=[]
    for g in map(F,('7/100','2/25','1/10')):
        out=HERE/f'g{g}'.replace('/','d');feasible=json.loads((out/'feasibility.json').read_text())
        if not all(r['ground_identified'] and r['band_separated'] for r in feasible):
            summary.append(dict(g=str(g),status='stopped_at_physical_count_feasibility'));continue
        # Reuse the independently audited arithmetic helper, with an explicit
        # local-only source resolver. Every recorded hash refers to this actual
        # coupling-specific source, never its hypothetical legacy location.
        def local_read(path,sources):
            actual=out/path.name
            assert actual.is_file()
            return original_read(actual,sources)
        I.read=local_read
        recs=[I.patch(nx,ny,g,'quadratic',out) for nx,ny in ((4,4),(8,4),(8,8))]
        for rec in recs:
            a0=F(rec['global_ground_lower']);a1=F(rec['all_excited_global_lower'])
            rec['blocks'][0]['unclipped_eigen_lower']=rec['blocks'][0]['eigen_lower'][:]
            rec['blocks'][1]['unclipped_eigen_lower']=rec['blocks'][1]['eigen_lower'][:]
            rec['blocks'][0]['eigen_lower']=[str(max(a0,F(x))) for x in rec['blocks'][0]['eigen_lower']]
            rec['blocks'][1]['eigen_lower']=[str(max(a1,F(x))) for x in rec['blocks'][1]['eigen_lower']]
            assert all(F(l)<=F(u) for block in rec['blocks'] for l,u in zip(block['eigen_lower'],block['eigen_upper']))
            rec['global_floor_clipping']='All energies>=a0; every triplet sector is orthogonal to the unique ground and hence >=a1.'
            rec['ground_width']=str(F(rec['blocks'][0]['eigen_upper'][0])-F(rec['blocks'][0]['eigen_lower'][0]))
            (out/f'temple_{rec["nx"]}x{rec["ny"]}_g{g}.json'.replace('/','d')).write_text(json.dumps(rec,indent=2))
        rows=[]
        for order in ('xyt','xty','txy'):
            candidates=[];best_prefix=None
            for bi in range(100,601):
                beta=F(bi,20);st=stages(recs,float(beta),order)
                rank=(st['positive_steps'],min(st.get('canonical',st['permuted_prefix'])))
                if best_prefix is None or rank>best_prefix[0]:best_prefix=(rank,beta,st)
                candidates.append((score(st,float(beta)),beta))
            value,beta=min(candidates)
            if value<0:
                exact=I.exact_seed(recs,beta,order,short)
            else:
                beta=best_prefix[1];st=stages(recs,beta,order,True)
                if 'canonical' in st:exact=I.exact_seed(recs,beta,order,short)
                else:exact=dict(beta_initial=str(beta),order_before_transport=order,accepted=False,
                   J1=str(st['J1']),J2=str(st['J2']),C0=str(st['C0']),permuted_prefix=list(map(str,st['permuted_prefix'])))
            exact.update(accepted_float_proposals=sum(v<0 for v,_ in candidates),best_float_score=value)
            rows.append(exact);print(g,order,beta,exact.get('all_integer_gap_display'),exact.get('bootstrap',{}).get('status'),flush=True)
        result=dict(g=str(g),status='new_coupling_candidate_pending_independent_review',
          grid_scope='beta5..30 step.05; three properly transported orders; failures are not all-beta exclusions',results=rows,
          short_size_certificate='../short_sizes/uniform_short_sizes.json')
        (out/'frontier_results.json').write_text(json.dumps(result,indent=2));summary.append(result)
    I.read=original_read
    (HERE/'frontier_summary.json').write_text(json.dumps(summary,indent=2))


if __name__=='__main__':main()
