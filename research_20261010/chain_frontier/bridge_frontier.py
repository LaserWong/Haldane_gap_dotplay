"""Producer bridge using the parent's independently reviewed scalar lemma.
Physical inputs and these arithmetic evaluations still need a separate audit.
"""
import os
for x in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[x]='1'
import sys,json,argparse,importlib.util
from pathlib import Path
from fractions import Fraction as F
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
spec=importlib.util.spec_from_file_location('root_window',ROOT/'research_20261010/root_review/finite_window_2d.py');window=importlib.util.module_from_spec(spec);spec.loader.exec_module(window)
sys.path.insert(0,str(ROOT/'low_energy'))
from local_relative_bound import optimize_bound
import dimer_subspace as ds
ds.OUT=OUT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source');args=ap.parse_args();p=Path(args.source).resolve();rec=json.loads(p.read_text());n=rec['n'];g=F(rec['g'])
    short_bound=optimize_bound(F(1),g,'chain',2*n-2)
    short_gap=F(short_bound['second_shift_lower']);rows=[]
    M=2*n-1;edge_bound=optimize_bound(F(1),g,'chain',M)
    tag=f'chain_s1_M{M}_g{g}_depth2'.replace('/','d');gp=OUT/(tag+'_ground.json')
    edge=json.loads(gp.read_text()) if gp.exists() else ds.certify_sparse(F(1),M,ds.columnar_bonds(M,1,g,F(0)),tag=tag,relative_bound=edge_bound,support_depth=2)
    edge_gap=F(edge['second_eigenvalue_lower'])-F(edge['ground_upper'])
    short_gap=min(short_gap,edge_gap)
    for seed in rec['seeds']:
        boot=seed['bootstrap']
        if not boot['status'].startswith('accepted'):continue
        beta=F(boot['input']['beta']);nn=boot['input']['n'];states=[(F(seed['first_S_lower']),F(seed['first_T_lower']))]+[(1-F(r['p_upper']),1-F(r['q_upper'])) for r in boot['updates']];wins=[]
        for S,T in states:
            if nn>=boot['final_n']:break
            c,detail=window.interpolate_1d(S,T);gap=window.gap(c,beta)
            wins.append(dict(cells=[nn,2*nn],beta=str(beta),S_lower=str(S),T_lower=str(T),thermal_purity_lower=str(c),thermal_purity_display=float(c),gap_lower=str(gap),gap_display=float(gap),details=detail));nn*=2;beta*=2
        allgap=min([short_gap,F(boot['conditional_gap_lower_rational'])]+[F(r['gap_lower']) for r in wins]);rows.append(dict(initial_beta=seed['beta'],asymptotic_from=boot['final_n'],asymptotic_gap=boot['conditional_gap_lower_rational'],short_size_max=2*n-1,short_gap_lower=str(short_gap),windows=wins,all_M_ge2_gap_lower=str(max(F(0),allgap)),all_M_ge2_gap_display=float(max(F(0),allgap))))
    best=max(rows,key=lambda r:F(r['all_M_ge2_gap_lower'])) if rows else None
    out=dict(status='producer_all_size_bridge_candidate_requires_independent_audit',source=str(p.relative_to(ROOT)),g=str(g),short_local_comparison=short_bound,short_local_cells=[2,2*n-2],short_edge_ground_certificate=edge,short_edge_gap_lower=str(edge_gap),rows=rows,best=best)
    (OUT/(p.stem+'_bridges.json')).write_text(json.dumps(out,indent=2));print('BRIDGE',str(g),None if best is None else {k:v for k,v in best.items() if k!='windows'},flush=True)
if __name__=='__main__':main()
