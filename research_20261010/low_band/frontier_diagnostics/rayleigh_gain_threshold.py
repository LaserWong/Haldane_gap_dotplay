"""Floating sensitivity only: hypothetical largest-seed Rayleigh improvements.

The modification is not known to be attainable by a physical trial state.  We
discard improvements whose three raw ratio bounds exceed one, avoiding the
overtly inconsistent half-width ablations in optimistic_screens.py.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json, math, hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
import optimistic_screens as S


def shift_stage(raw, ell, beta, gain):
    factor=(math.exp(2*beta*gain)+ell-1)/ell
    ratios=[raw[0]*factor,raw[1]*factor**2,raw[2]*factor]
    if max(ratios)>1+1e-14:
        return None
    j1,j2,c0=ratios
    abc=[]
    for k in range(3):
        z=j1 if k==0 else j2*abc[0] if k==1 else c0**4*abc[0]**2*abc[1]
        abc.append(S.C.G(z))
        if abc[-1]<=0:break
    out=dict(raw_ratios=ratios,prefix=abc,positive_steps=sum(x>0 for x in abc))
    if len(abc)==3 and min(abc)>0:
        out['canonical']=S.transport(*abc,'txy',math.sqrt)
    return out


def main():
    output=[]
    for tag in ('g2d25','g1d10'):
        paths=[S.BAND/'frontier_g007_g010'/tag/f'temple_{nx}x{ny}_{tag}.json'
               for nx,ny in ((4,4),(8,4),(8,8))]
        recs=[json.loads(p.read_text()) for p in paths]
        results=[]
        for target in (0.,.01,.05):
            candidates=[]
            for bi in range(100,601):
                beta=bi/20
                raw=S.initial(recs,beta)['raw_ratios']
                ell=S.C.traces_float(recs[2],2*beta)[0]
                fmax=min(1/raw[0],1/math.sqrt(raw[1]),1/raw[2])
                if fmax<=1:continue
                hi=math.log(1+ell*(fmax-1))/(2*beta)*(1-1e-10)
                def succeeds(gain):
                    st=shift_stage(raw,ell,beta,gain)
                    value,perfect=S.score(st,beta)
                    return value<0 and not perfect and -value>=target
                if not succeeds(hi):continue
                lo=0.
                for _ in range(42):
                    mid=(lo+hi)/2
                    if succeeds(mid):hi=mid
                    else:lo=mid
                st=shift_stage(raw,ell,beta,hi)
                value,_=S.score(st,beta)
                candidates.append(dict(beta=beta,hypothetical_rayleigh_gain=hi,
                    optimistic_scalar_gap=-value,raw_ratios=st['raw_ratios'],
                    canonical=st['canonical']))
            results.append(dict(target_scalar_gap=target,successful_grid_betas=len(candidates),
                minimum_gain_proposal=min(candidates,key=lambda x:x['hypothetical_rayleigh_gain']) if candidates else None))
        row=dict(status='floating_hypothetical_sensitivity_only_not_a_certificate',
            g=recs[0]['g'],grid='beta=5..30 in steps of .05',
            interpretation='Only largest Rayleigh changes; denominator bounds fixed. Raw ratios <=1 is necessary but not sufficient for physical consistency.',
            source_sha256={str(p.relative_to(S.BAND)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            targets=results)
        output.append(row)
        print(json.dumps(row,indent=2),flush=True)
    (S.HERE/'rayleigh_gain_thresholds.json').write_text(json.dumps(output,indent=2))


if __name__=='__main__':main()
