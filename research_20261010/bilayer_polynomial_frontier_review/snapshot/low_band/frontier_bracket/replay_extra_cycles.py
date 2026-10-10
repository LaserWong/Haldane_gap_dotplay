"""Exact selected deferred-order cycles with explicit earlier-window bridges."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,resource,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RES=BAND.parent
for p in (BAND/'tail_comparison',BAND/'joint_trace_bootstrap',RES/'root_review'):sys.path.insert(0,str(p))
import integrate_tails as I
from scan_transported import stages
from transport_orders import transport,sqrt_lower
import joint_scalar as J
from finite_window_2d import exp_upper


def asymptotic_gap(u,tau):
    assert 0<u<=F(1,500)
    proposal=F(math.floor(math.log(1/(32*float(u)))/float(tau)*10**12)-1,10**12)
    proposal=max(proposal,F(0))
    while exp_upper(tau*proposal)*32*u>1:proposal-=F(1,10**12)
    assert proposal>0 and exp_upper(tau*proposal)*32*u<=1
    return proposal


def main():
    resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
    if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    out=HERE/'g17d200';beta=F(177,20);order='txy'
    paths=[out/f'combined_patch_{n}x{m}_g17d200.json' for n,m in ((4,4),(8,4),(8,8))]
    recs=[json.loads(p.read_text()) for p in paths]
    st=stages(recs,beta,order,True);assert 'canonical' in st
    raw=st['permuted_prefix'];states=[];rows=[]
    sp=BAND/'frontier_g007_g010'/'short_sizes'/'uniform_short_sizes.json';short=F(json.loads(sp.read_text())['gap_lower'])
    for cycle in range(9):
        digits=max(80,40*2**max(0,cycle-5));tau=2*beta*2**cycle;n=8*2**cycle
        canonical=[J.down(x,digits) for x in transport(*raw,order,lambda x:sqrt_lower(x,digits))]
        joint=J.full_product(raw);u=max(1-x for x in canonical)
        thermal,detail=J.interpolate_2d_joint(*canonical,joint);wg=J.gap(thermal,tau)
        assert wg is not None
        states.append(dict(cycle=cycle,n=n,beta=str(tau),permuted_purities=list(map(str,raw)),
            canonical_purities=list(map(str,canonical)),joint_lower=str(joint),
            u=str(u),rounding_digits=digits,window=dict(thermal_lower=str(thermal),gap_lower=str(wg),details=detail)))
        if cycle>=4 and u<=F(1,500):
            gap=asymptotic_gap(u,tau)
            whole=min([gap,short]+[F(s['window']['gap_lower']) for s in states[:-1]])
            row=dict(cycles_before_transport=cycle,asymptotic_n=n,beta=str(tau),u=str(u),
                asymptotic_gap=str(gap),all_integer_L_ge2_gap=str(whole),gap_display=float(whole),
                positive_log_acceptance='exp_upper(beta*gap)*32*u<=1',accepted=whole>0)
            rows.append(row);print(cycle,float(gap),float(whole),flush=True)
        raw=J.plain_advance(raw,True,max(160,digits*2))
        if raw is None:break
    result=dict(status='exact_deferred_cycle_candidate_pending_independent_review',g='17/200',
        beta_initial=str(beta),order=order,initial={k:str(st[k]) for k in ('J1','J2','C0')},
        states=states,candidates=rows,short_size_lower=str(short),
        source_sha256={str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[sp]})
    (out/'extra_cycles_exact.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
