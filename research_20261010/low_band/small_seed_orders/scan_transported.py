"""Bounded small-seed order scan with exact checks and correct basepoint transport."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
sys.path.insert(0,str(BAND/'translation_band'));sys.path.insert(0,str(BAND/'frontier_g006'))
import large_refined_pipeline as P
import correlated_low_band as C
import low_band_certificate as L
from transport_orders import transport,sqrt_lower


def stages(recs,beta,order,exact=False):
    beta=F(beta) if exact else float(beta)
    trace=P.fast_trace if exact else C.traces_float
    e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
    if not exact:e=list(map(float,e))
    exp=(lambda x:P.exp_interval(x)[0]) if exact else math.exp
    down=(lambda x:L.down(x,digits=16)) if exact else (lambda x:x)
    q0=trace(recs[0],beta);q3=trace(recs[2],2*beta)
    i1,b1=(0,2*beta) if order[0]=='t' else (1,beta)
    i2,b2=(2,beta) if order[-1]=='t' else (1,2*beta)
    q1=trace(recs[i1],b1);q2=trace(recs[i2],b2)
    j1=down(exp(-2*beta*e[2]+8*beta*e[0])*q3[0]/q0[1]**8)
    j2=down(exp(-4*beta*e[2]+8*b1*e[i1])*q3[0]**2/q1[1]**8)
    c0=down(exp(-2*beta*e[2]+2*b2*e[i2])*q3[0]/q2[1]**2)
    abc=[]
    for index in range(3):
        product=j1 if index==0 else j2*abc[0] if index==1 else c0**4*abc[0]**2*abc[1]
        new=down(C.G(product));abc.append(new)
        if new<=0:break
    out=dict(J1=j1,J2=j2,C0=c0,permuted_prefix=abc,positive_steps=sum(x>0 for x in abc))
    if len(abc)==3 and min(abc)>0:
        out['canonical']=transport(*abc,order,sqrt_lower if exact else math.sqrt)
    return out


def score(st,beta):
    if 'canonical' not in st:return 1.
    abc=st['canonical'][:]
    for j in range(16):
        u=max(1-x for x in abc)
        if u<=.002:return -math.log(1/(32*u))/(beta*2**(j+1)) if u>0 else -1.
        for _ in range(3):
            x=C.G(abc[0]**4*abc[1]**2*abc[2])
            if x<=0:return 1.+u
            abc=abc[1:]+[x]
    return max(1-x for x in abc)


def exact_record(recs,beta,order):
    st=stages(recs,beta,order,True)
    out=dict(beta=str(beta),order=order,J1=str(st['J1']),J2=str(st['J2']),C0=str(st['C0']),
             permuted_prefix=list(map(str,st['permuted_prefix'])),positive_steps=st['positive_steps'])
    if 'canonical' in st:
        abc=[L.down(x,digits=18) for x in st['canonical']]
        out['canonical_first_purities']=list(map(str,abc))
        out['bootstrap']=L.replay(*abc,n=4,m=4,beta=2*beta,rounds=64,digits=18)
        out['accepted']=out['bootstrap']['status']=='accepted_analytic_scalar_certificate'
    else:out['accepted']=False
    return out


def main():
    result=[]
    for g in ('1d25','1d20'):
        paths=[BAND/'frontier'/f'bilayer_{nx}x{ny}_g{g}_symmetric_number_low_band.json' for nx,ny in [(2,2),(4,2),(4,4)]]
        recs=[json.loads(p.read_text()) for p in paths];orders=[]
        for order in ('xyt','xty','txy'):
            candidates=[];best_prefix=None;positive=accepted=0
            for bi in range(40,2401):
                beta=F(bi,40);st=stages(recs,float(beta),order)
                rank=(st['positive_steps'],min(st.get('canonical',st['permuted_prefix'])))
                if best_prefix is None or rank>best_prefix[0]:best_prefix=(rank,beta,st)
                value=score(st,float(beta));positive+=int('canonical' in st);accepted+=int(value<0)
                candidates.append((value,beta))
            best=min(candidates)
            selected=best[1] if best[0]<0 else best_prefix[1]
            exact=exact_record(recs,selected,order)
            orders.append(dict(order=order,positive_first_cycles=positive,accepted_float_proposals=accepted,
                best_float_score=best[0],best_prefix_beta=str(best_prefix[1]),
                best_prefix_display=list(map(float,best_prefix[2]['permuted_prefix'])),exact_selected=exact))
            print(g,order,'positive',positive,'accepted',accepted,'selected',selected,'exact',exact.get('bootstrap',exact['permuted_prefix']),flush=True)
        row=dict(g=recs[0]['g'],status='bounded_transported_order_scan_not_an_all_beta_exclusion',
            beta_grid='1 through 60 in steps of 1/40',canonical_base_after_first_cycle=[4,4],
            source_sha256={str(p.relative_to(BAND)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},orders=orders)
        (HERE/f'small_orders_g{g}.json').write_text(json.dumps(row,indent=2));result.append(row)
    (HERE/'summary.json').write_text(json.dumps(result,indent=2))


if __name__=='__main__':main()
