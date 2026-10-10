"""Recombine ground improvements with frozen bands; exact selected scalar replay."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
sys.path.insert(0,str(BAND/'tail_comparison'))
import integrate_tails as I
from scan_transported import stages,score


def main():
    sp=BAND/'frontier_g007_g010'/'short_sizes'/'uniform_short_sizes.json'
    short10=F(json.loads(sp.read_text())['gap_lower']);summary=[]
    sp06=BAND/'frontier_g006'/'all_size_bridges.json'
    short06=min(F(row['gap_lower']) for row in json.loads(sp06.read_text())[0]['small_sizes'])
    for g in map(F,('3/100','1/25','1/20','3/50','7/100','2/25','1/10')):
        short=short06 if g<=F(3,50) else short10
        short_source=sp06 if g<=F(3,50) else sp
        paths=[HERE/f'temple_{nx}x{ny}_g{g}.json'.replace('/','d') for nx,ny in ((4,4),(8,4),(8,8))]
        recs=[json.loads(p.read_text()) for p in paths];rows=[]
        baseline_path=(BAND/'tail_comparison'/'quadratic'/f'recombined_g{g}.json'.replace('/','d')) if g<F(7,100) else (BAND/'frontier_g007_g010'/f'g{g}'.replace('/','d')/'frontier_results.json')
        baseline=json.loads(baseline_path.read_text())['results']
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
            oldrows=[row for row in baseline if row.get('order_before_transport')==order and row.get('accepted')]
            compared=[]
            for oldrow in oldrows:
                oldbeta=F(oldrow['beta_initial'])
                if oldbeta!=F(exact['beta_initial']):
                    alternate=I.exact_seed(recs,oldbeta,order,short)
                    compared.append(alternate)
                    if alternate.get('accepted') and F(alternate['all_integer_L_ge2_gap'])>F(exact.get('all_integer_L_ge2_gap','0')):
                        exact=dict(alternate)
            if compared:exact['additional_baseline_beta_replays']=compared
            exact.update(accepted_float_proposals=sum(v<0 for v,_ in candidates),best_float_score=value)
            rows.append(exact);print(g,order,beta,exact.get('all_integer_gap_display'),exact.get('bootstrap',{}).get('status'),flush=True)
        result=dict(g=str(g),status='ground_pencil_scalar_candidate_pending_independent_review',
          grid_scope='beta5..30 step.05; three properly transported orders; failures are not all-beta exclusions',results=rows,
          source_sha256={str(p.relative_to(BAND.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[short_source,baseline_path]})
        (HERE/f'scalar_g{g}.json'.replace('/','d')).write_text(json.dumps(result,indent=2));summary.append(result)
    (HERE/'scalar_summary.json').write_text(json.dumps(summary,indent=2))

if __name__=='__main__':main()
