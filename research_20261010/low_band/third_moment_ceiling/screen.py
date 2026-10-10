"""Saved-input resource-prioritization screen, not a gap certificate.
The exact part bounds possible gain in the existing span{psi,(H-rho)psi}.
The floating part asks how small its missing residual Rayleigh would need to be.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib,resource
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RES=BAND.parent
for p in (BAND/'frontier_g009',BAND/'tail_comparison'):sys.path.insert(0,str(p))
from scan_joint import sequence
from scan_transported import stages
from transport_orders import transport
import correlated_low_band as C


def main():
    resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
    if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    fp=BAND/'frontier_g009'/'filtered_8x8_g9d100.json';filtered=json.loads(fp.read_text())
    paths=[BAND/'frontier_g009'/f'combined_patch_{n}x{m}_g9d100.json' for n,m in ((4,4),(8,4),(8,8))]
    recs=[json.loads(p.read_text()) for p in paths];g=F(9,100)
    rho=F(filtered['exact_original_shifted_rayleigh']);v=F(filtered['exact_original_variance'])
    sector=filtered['residual_sector_certificate'];masses=list(map(F,sector['residual_norm_squared_by_number']))
    qmean=sum(F(q)*m for q,m in zip(sector['number_indices'],masses))/v
    cross=2*sum(map(F,sector['cross_term_sqrt_upper']))/v
    low=(1-2*g)*qmean-cross;high=F(sector['residual_normalized_H_expectation_upper'])
    assert high==(1+2*g)*qmean+cross and rho<low<high
    c=low-rho;scale=10**30;rad=c*c+4*v
    root=math.isqrt(rad.numerator*scale*scale//rad.denominator)
    root_upper=F(root+1,scale)
    delta_upper=(root_upper-c)/2
    assert delta_upper*(c+delta_upper)>=v
    old=F(recs[2]['blocks'][0]['eigen_upper'][0]);rf=float(rho);vf=float(v)
    successes=[]
    for bi in range(140,281):
        beta=bi/20;initial=stages(recs,beta,'txy');raw=[initial[k] for k in ('J1','J2','C0')]
        ell=C.traces_float(recs[2],2*beta)[0]
        def evaluate(R):
            c=R-rf;delta=2*vf/(c+math.sqrt(c*c+4*vf));new=rf-delta
            factor=(math.exp(2*beta*(float(old)-new))+ell-1)/ell
            ratios=[raw[0]*factor,raw[1]*factor*factor,raw[2]*factor]
            if max(ratios)>1:return None
            a=C.G(ratios[0])
            if a<=0:return None
            b=C.G(ratios[1]*a)
            if b<=0:return None
            cc=C.G(ratios[2]**4*a*a*b)
            if cc<=0:return None
            st={'permuted_prefix':[a,b,cc],'canonical':transport(a,b,cc,'txy',math.sqrt)}
            rows,status=sequence(st,beta,'txy',False)
            if status!='accepted_small_defect':return None
            last=rows[-1];u=last['u']
            return {'asymptotic_score':math.log(1/(32*u))/last['beta'],'cycle':last['cycle'],'raw_ratios':ratios,'hypothetical_rayleigh':new}
        optimistic=evaluate(float(low))
        if optimistic is None:continue
        lo,hi=float(low),float(high)
        for _ in range(36):
            mid=(lo+hi)/2
            if evaluate(mid) is not None:lo=mid
            else:hi=mid
        successes.append(dict(beta=beta,maximum_residual_Rayleigh_for_float_acceptance=lo,
            optimistic_low_R_result=optimistic,at_threshold=evaluate(lo)))
    result=dict(status='exact_two_vector_gain_ceiling_and_unrigorous_float_feasibility_only',g=str(g),
        rho=str(rho),variance=str(v),residual_number_mean=str(qmean),residual_Rayleigh_lower=str(low),
        residual_Rayleigh_upper=str(high),maximum_possible_two_vector_energy_gain_upper=str(delta_upper),
        current_certified_gain=filtered['filter']['improvement'],
        grid='beta7..14 step.05; txy coupled joint route; asymptotic proposal only, no new finite-window certificate',
        feasible_optimistic_grid_points=len(successes),best_threshold=max(successes,key=lambda r:r['maximum_residual_Rayleigh_for_float_acceptance']) if successes else None,
        source_sha256={str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths+[fp]})
    (HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print('R range',float(low),float(high),'gain ceiling',float(delta_upper),'best',result['best_threshold'],flush=True)


if __name__=='__main__':main()
