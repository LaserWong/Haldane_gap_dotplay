"""Uniform epsilon interval from one product trial and complete reference bins.
The local comparison is affine in epsilon; exact PSD at both interval endpoints
establishes it throughout. The full product-state residual is exactly quadratic.
"""
import os,sys,json,copy,math
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
OUT=Path(__file__).resolve().parent;BASE=OUT.parents[1]
sys.path.insert(0,str(OUT));sys.path.insert(0,str(BASE/'low_energy'))
import fully_frustrated as producer
from audit_ff import occupancy,multigraph,local_psd,seed_check,K,W
from scan_epsilon import float_seed
from trianglefree_bridge import bridge as improved_bridge

def verify_vacuum_local_residual():
    # v=S00.S10+S01.S11 acting on unnormalised singlet tensor singlet.
    out=Counter()
    for aa in range(2):
        for s,t,x in K[aa,aa][0,0]:out[s,t]+=x
    assert not out[0,0]
    assert all(s and t for (s,t),x in out.items() if x)
    square=sum(W[s]*W[t]*x*x for (s,t),x in out.items())/(W[0]*W[0])
    assert square==F(3,4)
    return square

def run():
    c=verify_vacuum_local_residual();reports=[]
    hist={s:occupancy(*s,F(3,10)) for s in [(2,2),(4,2),(4,4)]}
    for ep in ['1/250','9/2000','19/4000','1/200']:
        eps=F(ep);records=[];checks=[]
        for nx,ny in [(2,2),(4,2),(4,4)]:
            N=nx*ny;bins=[dict(q=q,energy_lower=str(e),multiplicity=m) for (q,e),m in sorted(hist[nx,ny].items())]
            ref=producer.optimize_comparison(N,eps,bins);a=F(ref['a']);b=F(ref['b']);B=2*N*b
            endpoints=[local_psd(a,b,eta) for eta in [F(0),eps]]
            d=min(e-4*a*q for q,e in hist[nx,ny] if q)-B
            assert d==F(ref['second_shift_lower']) and d>0
            square_weight=sum(w*w for w in multigraph(nx,ny).values());r2=c*eps*eps*square_weight;E00=-F(3*N,4)
            rec=dict(nx=nx,ny=ny,N_dimers=N,E00=str(E00),ground_upper=str(E00),ground_lower=str(E00-r2/d),reference_certificate=ref)
            records.append(rec);checks.append(dict(geometry=[nx,ny],full_dimension=4**N,linear_trial_dimension=1,retained_vectors=1,reached_dimension_at_nonzero_epsilon=1+3*len(multigraph(nx,ny)),edge_squared_weight=square_weight,residual_squared_at_upper_endpoint=str(r2),uniform_second_shift_lower=str(d),uniform_ground_width=str(r2/d),local_PSD_at_both_endpoints=[r['inertia'] for r in endpoints]))
        grid=[x for k in range(24,241) if (x:=float_seed(records,k/2))]
        selected=set()
        if grid:
            selected.add(max(grid,key=lambda r:r['gap'])['beta'])
            nmin=min(r['n'] for r in grid);selected.add(max((r for r in grid if r['n']==nmin),key=lambda r:r['gap'])['beta'])
        seeds=[]
        for beta in sorted(selected):
            seed=producer.seed3(records,F(beta));check=seed_check(records,seed);assert check['accepted']
            bridge=improved_bridge(eps,check['n']);bound=F(bridge['bound']) if bridge['bound'] else -1
            if bridge.get('b') is not None:local_psd(F(bridge['a']),F(bridge['b']),F(0))
            seeds.append(dict(seed=seed,audit=check,uniform_bridge=bridge,uniform_all_integer_L_ge2_gap=str(min(F(check['gap_lower']),bound)) if bound>0 else None))
        best=max((r for r in seeds if r['uniform_all_integer_L_ge2_gap']),key=lambda r:F(r['uniform_all_integer_L_ge2_gap']),default=None)
        result=dict(epsilon_interval=['0',str(eps)],endpoint_PSD_implies_uniform_by_affinity=True,analytic_local_vacuum_residual_squared=str(c),ground_checks=checks,uniform_ground_records=records,float_grid=[12,120,.5],float_success_count=len(grid),seeds=seeds,best_uniform_all_sizes_gap=best['uniform_all_integer_L_ge2_gap'] if best else None,best_beta=best['audit']['beta'] if best else None,best_n=best['audit']['n'] if best else None,status='uniform exact certificate' if best else 'tested grid does not yield all-size certificate')
        reports.append(result)
        print(json.dumps({k:v for k,v in result.items() if k not in ['ground_checks','uniform_ground_records','seeds']}),flush=True)
        (OUT/'vacuum_interval_certificates.json').write_text(json.dumps(reports,indent=2))
    return reports
if __name__=='__main__':run()
