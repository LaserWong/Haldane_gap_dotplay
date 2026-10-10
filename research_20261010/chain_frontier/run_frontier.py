"""Reuse archived exact producers with explicit output isolation and bounded resources.
The producer's floating Ritz solve proposes only; saved integer vectors and
rational residual/tail/replay records require independent verification.
"""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys, json, argparse, time, resource
from pathlib import Path
from fractions import Fraction as F
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'low_energy'))
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
resource.setrlimit(resource.RLIMIT_CPU,(590,600))
import dimer_subspace as ds
import local_relative_bound as lb
import ground_tail as gt
import numpy as np
ds.OUT=lb.OUT=gt.OUT=OUT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--g',required=True);ap.add_argument('--n',type=int,default=4);ap.add_argument('--depth',type=int,default=4);ap.add_argument('--betas',default='16,24,32,40,48,56,64,80,96,112,128,160');args=ap.parse_args()
    start=time.monotonic();s,g=F(1),F(args.g);rs=[]
    stem=f'chain_sparse_s1_g{g}_n{args.n}_depth{args.depth}'.replace('/','d')
    output=OUT/(stem+'.json')
    for M in [args.n,2*args.n]:
        bound=lb.optimize_bound(s,g,'chain',M)
        tag=f'chain_s1_M{M}_g{g}_depth{args.depth}'.replace('/','d');path=OUT/(tag+'_ground.json')
        if path.exists():
            r=json.loads(path.read_text())
        else:
            try:
                r=ds.certify_sparse(s,M,ds.columnar_bonds(M,1,g,F(0)),tag=tag,relative_bound=bound,support_depth=args.depth)
            except AssertionError as exc:
                # The existing producer intentionally aborts when Temple does not
                # apply. Preserve its already-computed exact vector and arithmetic
                # as an explicitly UNACCEPTED diagnostic, without altering producer.
                tb=exc.__traceback__
                while tb and tb.tb_frame.f_code.co_name!='certify_sparse':tb=tb.tb_next
                if tb is None:raise
                v=tb.tb_frame.f_locals
                if not {'rho','r2','ints','basis','a'}<=v.keys() or not v['rho']>=v['a']:raise
                artifact=OUT/(tag+'_trial.npz')
                np.savez_compressed(artifact,vector=np.array(v['ints'],dtype=np.int64),basis=np.array(v['basis'],dtype=np.uint8),bits=v['bits'])
                r=dict(status='rejected_whole_space_isolation_exact_residual_only',s=str(s),N_dimers=M,physical_sites=2*M,full_dimension=9**M,retained_states=1,trial_subspace_dimension=len(v['basis']),reached_support_dimension=len(v['output_states']),support_depth=args.depth,E00=str(v['E00']),exact_rayleigh=str(v['rho']),exact_residual_squared=str(v['r2']),second_eigenvalue_lower=str(v['a']),ground_lower=str(v['E00']-F(bound['B'])),ground_upper=str(v['rho']),relative_form_bound=bound,trial_artifact=artifact.name,weak_bonds=[[i,aa,j,bb,str(gg)] for i,aa,j,bb,gg in v['weak']],integer_matrix_denominator=v['den'],sparse_nnz=v['Arect'].nnz,total_seconds=time.monotonic()-v['t0'],peak_process_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,proof='Exact metric Rayleigh and full residual only. Ground interval uses coarse full-spectrum comparison and variational upper bound. Temple uniqueness condition fails; no gap certificate.')
                path.write_text(json.dumps(r,indent=2))
                print('ISOLATION_REJECTED',g,M,args.depth,float(v['rho']),float(v['a']),float(v['r2']),flush=True)
                del v,tb

        r['M']=M;r['W']=1;rs.append(r)
    rows=[]
    record=dict(status='producer_candidate_requires_independent_audit',g=str(g),n=args.n,depth=args.depth,ground_certificates=rs,seeds=rows)
    if any(r['status'].startswith('rejected') for r in rs):
        record['resource_usage']=dict(total_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        output.write_text(json.dumps(record,indent=2));return
    for beta in map(F,args.betas.split(',')):
        _,q1,t1=lb.trace(rs[0],beta);_,q2,t2=lb.trace(rs[1],beta)
        shift=F(rs[1]['ground_upper'])-2*F(rs[0]['ground_upper'])
        S=lb.down(lb.exp_bounds(-beta*shift)[0]/q1**2);T=lb.down(1/q2**2)
        boot=lb.replay(str(S),str(T),args.n,str(beta)) if S>0 and T>0 else dict(status='purity_rounded_to_zero')
        row=dict(beta=str(beta),S_lower=str(S),T_lower=str(T),S_display=float(S),T_display=float(T),tails_display=[float(t1),float(t2)],ground_error_factors_display=[float(lb.exp_bounds(beta*(F(r['ground_upper'])-F(r['ground_lower'])))[1]) for r in rs],bootstrap=boot)
        rows.append(row);output.write_text(json.dumps(record,indent=2))
        print('CHAINSEED',g,args.n,args.depth,beta,float(S),float(T),boot['status'],boot.get('conditional_gap_lower_rational'),flush=True)
    record['resource_usage']=dict(total_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,blas_threads=1,address_space_limit_bytes=2*1024**3)
    output.write_text(json.dumps(record,indent=2))
if __name__=='__main__':main()
