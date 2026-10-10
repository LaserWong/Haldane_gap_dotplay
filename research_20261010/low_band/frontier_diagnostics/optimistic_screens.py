"""Unrigorous saved-input sensitivity screens; none is a gap certificate.
Every ablation makes selected denominator bounds unrealistically favorable or
uses a largest-ground lower endpoint as a hypothetical Rayleigh upper endpoint.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import math,json,copy,hashlib
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
sys.path.insert(0,str(BAND));sys.path.insert(0,str(BAND/'frontier_g006'))
import correlated_low_band as C
from transport_orders import transport


def initial(recs,beta):
    e=[float(F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0])) for r in recs]
    q0=C.traces_float(recs[0],beta);q1=C.traces_float(recs[0],2*beta)
    q2=C.traces_float(recs[1],2*beta);q3=C.traces_float(recs[2],2*beta)
    raw=[math.exp(-2*beta*e[2]+8*beta*e[0])*q3[0]/q0[1]**8,
         math.exp(-4*beta*e[2]+16*beta*e[0])*q3[0]**2/q1[1]**8,
         math.exp(-2*beta*e[2]+4*beta*e[1])*q3[0]/q2[1]**2]
    # Some inconsistent optimistic ablations exceed physical purity1. Cap at1
    # before applying G, whose monotonicity is only used on(0,1].
    j1,j2,c0=[min(1.,x) for x in raw];abc=[]
    for idx in range(3):
        x=j1 if idx==0 else j2*abc[0] if idx==1 else c0**4*abc[0]**2*abc[1]
        abc.append(C.G(x))
        if abc[-1]<=0:break
    out=dict(raw_ratios=raw,prefix=abc,positive_steps=sum(x>0 for x in abc))
    if len(abc)==3 and min(abc)>0:out['canonical']=transport(*abc,'txy',math.sqrt)
    return out


def score(st,beta):
    if 'canonical' not in st:return 1.,False
    abc=st['canonical'][:]
    for j in range(16):
        u=max(1-x for x in abc)
        if u<=.002:
            if u<=0:return -1.,True
            return -math.log(1/(32*u))/(beta*2**(j+1)),False
        for _ in range(3):
            val=C.G(abc[0]**4*abc[1]**2*abc[2])
            if val<=0:return 1.+u,False
            abc=abc[1:]+[val]
    return max(1-x for x in abc),False


def change(recs,name):
    out=copy.deepcopy(recs)
    for index in (0,1):
        if name in ('ground_both','all_intervals_both','all_intervals_and_tail_both') or name==f'ground_{index}':
            out[index]['blocks'][0]['eigen_lower']=out[index]['blocks'][0]['eigen_upper'][:]
        if name in ('triplet_both','all_intervals_both','all_intervals_and_tail_both') or name==f'triplet_{index}':
            out[index]['blocks'][1]['eigen_lower']=out[index]['blocks'][1]['eigen_upper'][:]
        if name in ('tail_both','all_intervals_and_tail_both') or name==f'tail_{index}':
            out[index]['number_sector_bins']['bins']=out[index]['number_sector_bins']['bins'][:2]
    if name.startswith('largest_ground_'):
        old=F(out[2]['blocks'][0]['eigen_upper'][0]);lo=F(out[2]['blocks'][0]['eigen_lower'][0])
        fraction=F(1,2) if name.endswith('half_width') else F(1)
        out[2]['blocks'][0]['eigen_upper']=[str(old-fraction*(old-lo))]
    return out


def components(rec,beta):
    lo,hi,tail=C.traces_float(rec,beta);block=rec['blocks'][0]
    ground=math.exp(beta*float(F(block['eigen_upper'][0])-F(block['eigen_lower'][0])))
    return dict(beta=beta,ground_upper_term=ground,triplet_upper_sum=max(0,hi-tail-ground),omitted_upper_tail=tail,total_upper=hi)


def main():
    names=['baseline','ground_0','ground_1','ground_both','triplet_0','triplet_1','triplet_both',
           'tail_0','tail_1','tail_both','all_intervals_both','all_intervals_and_tail_both',
           'largest_ground_half_width','largest_ground_full_width']
    allrows=[]
    for tag in ('g2d25','g1d10'):
        paths=[BAND/'frontier_g007_g010'/tag/f'temple_{nx}x{ny}_{tag}.json' for nx,ny in ((4,4),(8,4),(8,8))]
        recs=[json.loads(p.read_text()) for p in paths];rows=[]
        for name in names:
            rr=change(recs,name);proposals=[];best_stage=None
            for bi in range(100,601):
                beta=bi/20;st=initial(rr,beta);value,perfect=score(st,beta)
                proposals.append((value,beta,perfect,st))
                rank=(st['positive_steps'],min(st.get('canonical',st['prefix'])))
                if best_stage is None or rank>best_stage[0]:best_stage=(rank,beta,st)
            best=min(proposals,key=lambda x:(x[0],x[1]));value,beta,perfect,st=best
            if value>=0:beta,st=best_stage[1],best_stage[2]
            row=dict(variant=name,best_beta=beta,accepted_float_proposals=sum(x[0]<0 for x in proposals),
               optimistic_score_gap=(-value if value<0 and not perfect else None),perfect_purity_screen=perfect,
               first_cycle=st)
            rows.append(row);print(tag,name,beta,row['optimistic_score_gap'],row['accepted_float_proposals'],flush=True)
        baseline_beta=rows[0]['best_beta'];e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
        ell=C.traces_float(recs[2],2*baseline_beta)[0]
        qsmall=components(recs[0],baseline_beta);qsmall2=components(recs[0],2*baseline_beta);qmid=components(recs[1],2*baseline_beta)
        curvature1=e[2]-4*e[0];curvature2=e[2]-2*e[1]
        detail=dict(beta=baseline_beta,largest_minus_four_small_rayleigh=str(curvature1),
            largest_minus_twice_middle_rayleigh=str(curvature2),small_beta=qsmall,small_2beta=qsmall2,middle_2beta=qmid,
            C0_negative_log_contributions=dict(variational_energy_curvature=2*baseline_beta*float(curvature2),
                middle_ground_width_only=4*baseline_beta*float(F(recs[1]['ground_width'])),
                full_middle_upper_trace=2*math.log(qmid['total_upper']),largest_extra_trial_terms=-math.log(ell)))
        out=dict(status='unrigorous_optimistic_sensitivity_screen_not_a_certificate',g=recs[0]['g'],
            grid_scope='beta5..30 step.05; txy followed by canonical transport',
            denominator_index_key={'0':'4x4, at beta and2beta','1':'8x4, at2beta'},
            source_sha256={str(p.relative_to(BAND)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            screens=rows,baseline_loss_decomposition=detail)
        (HERE/f'screens_{tag}.json').write_text(json.dumps(out,indent=2));allrows.append(out)
    (HERE/'summary.json').write_text(json.dumps(allrows,indent=2))


if __name__=='__main__':main()
