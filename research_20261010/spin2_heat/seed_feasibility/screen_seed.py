#!/usr/bin/env python3
"""Scalar-only screening of cached optimistic order-10 moments; NOT a certificate."""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def mass(m,h,r):
    q=math.floor(m/h)
    return q*h**r+max(0,m-q*h)**r

def main():
    rows=json.loads((ROOT/'exploratory_moment_inputs.json').read_text());out=[]
    for a in [4.76121,4.761235250999516]:
      for old in rows:
        beta=old['beta'];scale=math.exp(-beta*(a-old['a']));order=old['max_moment']
        vJ=old['caps']['J']['cap']*scale;vN=old['caps']['N']['cap']*scale
        mJ=old['moments']['J'][str(order)]*scale**order;mN=old['moments']['N'][str(order)]*scale**order
        ratio=mN/vN**order
        trial=[]
        for N in [128,256,512,1024]:
            nontriv=3*mass(mN,vN**order,N/order) if N*math.log(vN)<650 else math.inf
            target=(8/7)**(1/(2*N))
            # Even with no remainder, cJ^N as denominator and MPS numerator 1
            # certifies only cJ^(-2N), far below the scalar startup basin.
            tground=math.exp(-2*N*math.log(vJ)) if 2*N*math.log(vJ)<700 else 0.0
            trial.append({'N':N,'nontrivial_sector_exclusion_upper_bound':nontriv if math.isfinite(nontriv) else '>exp(650)','exclusion_required_less_than':1,'method_fails_before_ell_search':nontriv>=1,'ground_numerator_one_T_lower_even_without_remainder':tground,'J_cap_required_for_T_at_least_7_over_8_even_without_remainder':target})
        assert all(t['method_fails_before_ell_search'] for t in trial)
        out.append({'a':a,'shift_status':'archived_D124_certified' if a==4.76121 else 'D180_infinite_chain_numerical_only','beta':beta,'max_moment':order,'J_cap_rescaled':vJ,'N_cap_rescaled':vN,'N_moment_divided_by_cap_power':ratio,'vN_gt_one_and_mN_ge_vN_power':vN>1 and ratio>=1,'trials':trial})
    result={'status':'EXPLORATORY_ONLY_NOT_A_NO_GO_THEOREM_FOR_MODEL','rows':out,'successful_tested_seeds':0,'diagonalizations_performed':0,'recommendation':'Do not allocate full L9/L10 traces for the archived independent one-atom-cap + MPS numerator-one startup at beta 6..32. A materially different scalar certificate is needed first.'}
    (ROOT/'seed_screen.json').write_text(json.dumps(result,indent=2)+'\n')
    for r in out:
        if r['a']==4.76121:print(r['beta'],r['J_cap_rescaled'],r['N_cap_rescaled'],r['N_moment_divided_by_cap_power'],r['trials'][0]['nontrivial_sector_exclusion_upper_bound'])
if __name__=='__main__':main()
