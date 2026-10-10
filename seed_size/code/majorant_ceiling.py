"""All-beta impossibility within a specified HALF-SPIN BILAYER tail-majorant family.

This is NOT physical seed exclusion. It proves that no choice of beta or local
comparison a can make these ground-record + independent-bin majorants pass
our correlation-aware staircase recursion. It identifies when more ground
accuracy alone is not enough and a better tail/comparison or seed is needed.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from certified_core import G,up,exp_bounds
from optimize_bilayer_tail import sqrt_bounds,g_for
from axis_order_search import nodes,record_for,ROOT,OUT

def delta_upper(rec):
    N=rec['N_dimers'];g=Q(g_for(rec));E00=Q(rec['E00']);U=Q(rec['ground_lower'])
    # Allow any improved ground upper pivot within the already certified interval.
    # Max_a [alpha-2Nb] =1-2g-2g sqrt(3(N-1)); its upper bound
    # remains an upper bound even if unconstrained a* lies outside allowed a<1/4.
    return up(1-2*g-2*g*sqrt_bounds(3*(N-1))[0]+E00-U)

def upper_first_state(records,order,lo,hi):
    lo,hi=Q(lo),Q(hi);vs=nodes(order,Q(1));qfloors=[];Us=[];Ls=[]
    for v in vs:
        rec=record_for(records,v);U=Q(rec['ground_upper']);Us.append(U);Ls.append(Q(rec['ground_lower']))
        delta=delta_upper(rec);N=rec['N_dimers'];mult=v[2]
        b=hi if delta>=0 else lo
        qfloors.append(1+3*N*exp_bounds(-mult*b*delta)[0])
    def ratio(coeff):
        rate=-sum((Q(k)*v[2]*U for k,v,U in zip(coeff,vs,[loU if k>0 else hiU for k,loU,hiU in zip(coeff,Ls,Us)])),Q(0))
        b=hi if rate>=0 else lo
        upper=exp_bounds(b*rate)[1]
        for k,q in zip(coeff,qfloors):
            if k<0:upper/=q**(-k)
        return min(Q(1),up(upper))
    J1=ratio([-8,0,0,1]);J2=ratio([0,-8,0,2]);C=ratio([0,0,-2,1])
    if J1<=Q(1,2):return None
    A1=up(G(J1))
    if A1<=0:return None
    B1=up(G(J2*A1))
    if B1<=0:return None
    C1=up(G(C**4*A1*A1*B1))
    if C1<=0:return None
    return [A1,B1,C1]

def upper_map_excluded(p,max_rounds=100):
    if p is None:return True
    p=list(p)
    for _ in range(max_rounds):
        if p[0]**4*p[1]**2*p[2]<=Q(1,2):return True
        if min(p)>=Q(999,1000):return False
        for k in range(3):
            x=p[0]**4*p[1]**2*p[2]
            if x<=0:return True
            a=up(G(x))
            if a<=0:return True
            p=p[1:]+[min(Q(1),a)]
    return False

def exclude_family(records,order,max_depth=18):
    U=[Q(r['ground_upper']) for r in records];curvature=2*Q(records[2]['ground_lower'])-8*U[0]
    if curvature<=0:return {'majorant_family_excluded':False,'reason':'No corner curvature'}
    B=Q(1)
    while exp_bounds(-B*curvature)[1]>Q(1,2):B*=2
    stack=[(Q(0),B,0)];leaves=[];unknown=[]
    while stack:
        l,h,d=stack.pop();p=upper_first_state(records,order,l,h)
        if upper_map_excluded(p):leaves.append([str(l),str(h)])
        elif d>=max_depth:
            unknown.append([str(l),str(h)])
            # A nonempty interval of viable optimistic envelopes already means
            # this certificate cannot exclude the family; avoid huge pointless subdivision.
            break
        else:
            m=(l+h)/2;stack.extend([(m,h,d+1),(l,m,d+1)])
    return {'majorant_family_excluded':not unknown,'order':order,'beta_tail_start':str(B),
            'corner_curvature':str(curvature),'delta_best_upper':list(map(str,map(delta_upper,records))),
            'excluded_intervals':leaves,'unresolved_intervals':unknown,
            'allows_arbitrarily_sharp_ground_refinement_within_current_intervals':True,'scope':'Only ground-only numerators plus the declared independent-bin comparison family and correlated staircase scheme; permits all improved ground pivots inside current enclosures, zero ground width, all beta and all local a. Not absence of a physical gap or a better certificate.'}

def main():
    out=[]
    cases=[('1/50','bilayer_s1d2_{x}x{y}_g1d50_k1d50_q2_ground.json'),
           ('3/100','bilayer_s1d2_{x}x{y}_g3d100_depth2_ground.json')]
    for g,template in cases:
        paths=[ROOT/'low_energy'/template.format(x=x,y=y) for x,y in [(2,2),(4,2),(4,4)]]
        recs=[json.loads(p.read_text()) for p in paths]
        for order in ['xyt','xty','txy']:
            r=exclude_family(recs,order);r.update(model_id='square_af_bilayer_spin_half_unit_rung',g=g,sources=list(map(str,paths)))
            out.append(r);print('MAJORANT FAMILY',g,order,'excluded',r['majorant_family_excluded'],'leaves',len(r.get('excluded_intervals',[])),flush=True)
    (OUT/'bilayer_majorant_ceiling.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
