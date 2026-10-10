"""Bounded deferred-order and joint-constraint scalar proposal/replay.
All joint-aware results await the separate new scalar-lemma review.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib,argparse,resource
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RES=BAND.parent
for p in (BAND/'tail_comparison',BAND/'joint_trace_bootstrap'):sys.path.insert(0,str(p))
import integrate_tails as I
from scan_transported import stages,score
from transport_orders import transport,sqrt_lower
import joint_scalar as J


def sequence(st,beta,order,exact=False,rounds=10):
    if 'canonical' not in st:return [],'initial_prefix_nonpositive'
    raw=list(st['permuted_prefix']);canonical=list(st['canonical'])
    joint=J.full_product(raw);rows=[]
    for cycle in range(rounds+1):
        if raw is not None:
            converted=transport(*raw,order,sqrt_lower if exact else math.sqrt)
            canonical=converted if canonical is None else [max(x,y) for x,y in zip(canonical,converted)]
            joint=max(joint,J.full_product(raw))
        if canonical is None:return rows,'all_comparison_paths_left_domain'
        joint=max(joint,J.full_product(canonical))
        u=max(1-x for x in canonical)
        rows.append(dict(cycle=cycle,n=8*2**cycle,beta=2*beta*2**cycle,
                         canonical=canonical[:],raw=(None if raw is None else raw[:]),joint=joint,u=u))
        if u<=(F(1,500) if exact else .002):return rows,'accepted_small_defect'
        nxt,args=J.canonical_advance(canonical,joint,exact)
        rows[-1]['canonical_update_arguments']=args
        raw=J.plain_advance(raw,exact) if raw is not None else None
        canonical=nxt
        joint=J.full_product(nxt) if nxt is not None else (F(0) if exact else 0.)
    return rows,'round_limit'


def serial(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,list):return [serial(x) for x in value]
    return value


def exact_record(recs,beta,order,short):
    st=stages(recs,beta,order,True)
    assert all(0<st[k]<=1 for k in ('J1','J2','C0'))
    rows,status=sequence(st,beta,order,True)
    result=dict(status='new_joint_scalar_candidate_pending_independent_review',
        beta_initial=str(beta),order=order,initial=serial(st),sequence_status=status,states=serial(rows),accepted=False)
    if status!='accepted_small_defect':return result
    last=rows[-1];boot=I.L.replay(*last['canonical'],n=last['n'],m=last['n'],beta=last['beta'],rounds=0,digits=80)
    assert boot['status']=='accepted_analytic_scalar_certificate'
    windows=[]
    for row in rows:
        c,detail=J.interpolate_2d_joint(*row['canonical'],row['joint']);g=J.gap(c,row['beta'])
        assert g is not None
        windows.append(dict(n=row['n'],through=2*row['n'],beta=str(row['beta']),
            thermal_lower=str(c),gap_lower=str(g),joint_lower=str(row['joint']),details=detail))
    final=min([F(boot['uniform_square_gap_lower']),short]+[F(w['gap_lower']) for w in windows if w['n']<last['n']])
    result.update(bootstrap=boot,windows=windows,short_L2_through_L7_gap=str(short),
        all_integer_L_ge2_gap=str(final),all_integer_gap_display=float(final),accepted=final>0)
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--tag',default='g9d100');args=ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
    if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if args.tag=='g9d100':paths=[HERE/f'combined_patch_{n}x{m}_{args.tag}.json' for n,m in ((4,4),(8,4),(8,8))]
    else:paths=[BAND/'combined_ground_bounds'/'combined'/f'patch_{n}x{m}_{args.tag}.json' for n,m in ((4,4),(8,4),(8,8))]
    recs=[json.loads(p.read_text()) for p in paths]
    shortpath=BAND/'frontier_g007_g010'/'short_sizes'/'uniform_short_sizes.json'
    short=F(json.loads(shortpath.read_text())['gap_lower'])
    results=[]
    for order in ('txy','xty','xyt'):
        proposals=[];best_partial=None;deferred=[]
        for bi in range(100,501):
            beta=F(bi,20);st=stages(recs,float(beta),order)
            rows,status=sequence(st,float(beta),order)
            if rows:
                rank=(len(rows),-min(row['u'] for row in rows))
            else:rank=(0,st['positive_steps'])
            if best_partial is None or rank>best_partial[0]:best_partial=(rank,beta,st)
            if status=='accepted_small_defect':
                last=rows[-1];u=last['u']
                if u>0:proposals.append((-math.log(1/(32*u))/last['beta'],beta))
            # Pure deferred-transport comparison, without the new joint update.
            raw=st['permuted_prefix'] if len(st['permuted_prefix'])==3 and min(st['permuted_prefix'])>0 else None
            for cycle in range(7):
                if raw is None:break
                can=transport(*raw,order,math.sqrt)
                if max(1-x for x in can)<1e-12:break
                val=score({'canonical':can},float(beta)*2**cycle)
                if val<0:deferred.append((val,beta,cycle))
                raw=J.plain_advance(raw,False)
        selected=[]
        for value,beta in sorted(proposals)[:3]:
            if beta not in selected:selected.append(beta)
        if not selected:selected=[best_partial[1]]
        exacts=[exact_record(recs,beta,order,short) for beta in selected]
        row=dict(order=order,joint_successful_float_proposals=len(proposals),
            exact_selected=exacts,deferred_successful_float_proposals=len(deferred),
            best_deferred_float=(serial(list(min(deferred))) if deferred else None))
        results.append(row)
        print(args.tag,order,'joint floats',len(proposals),'deferred',len(deferred),
              'exact',[(r['beta_initial'],r.get('all_integer_gap_display'),r['sequence_status']) for r in exacts],flush=True)
    result=dict(status='bounded_joint_order_scan_pending_independent_review',g=recs[0]['g'],
        grid='beta5..25 step.05; at most10 coupled cycles or6 deferred txy cycles',
        results=results,source_sha256={str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[shortpath]},
        limitation='A finite-grid failure is not an all-temperature exclusion.')
    (HERE/f'joint_scan_{args.tag}.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
