"""Outward-certified boundary brackets for the sequential two-purity map.

Success is proved with lower trajectories; failure with upper trajectories.
Failure of lower bounds alone is deliberately never an exclusion certificate.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from certified_core import G,down,up

SMALL=Q(1,40)

def classify(S,T,max_rounds=100):
    loS=hiS=Q(S);loT=hiT=Q(T)
    if not (0<=loS<=1 and 0<=loT<=1):raise ValueError('Purities outside [0,1]')
    for j in range(max_rounds+1):
        if min(loS,loT)>=1-SMALL:return 'accepted',j
        if hiS*hiS*hiT<=Q(1,2):return 'excluded',j
        if j==max_rounds:return 'unresolved',j
        # Once a lower endpoint reaches zero, retain zero, without interpreting it as failure.
        loS=max(Q(0),down(G(loS*loS*loT))) if loS*loT else Q(0)
        hiS=up(G(hiS*hiS*hiT))
        if hiS<=0:return 'excluded',j+1
        loT=max(Q(0),down(G(loT*loT*loS))) if loT*loS else Q(0)
        hiT=up(G(hiT*hiT*hiS))
        if hiT<=0:return 'excluded',j+1

def boundary(S,bits=36):
    S=Q(S)
    if classify(S,1)[0]!='accepted':return {'S':str(S),'status':'No accepted T<=1 found'}
    lo=Q(0);hi=Q(1)
    for j in range(bits):
        mid=(lo+hi)/2;status,_=classify(S,mid)
        if status=='accepted':hi=mid
        elif status=='excluded':lo=mid
        else:break
    ls,lj=classify(S,lo);hs,hj=classify(S,hi)
    assert ls=='excluded' and hs=='accepted'
    return {'S':str(S),'T_excluded_through':str(lo),'T_accepted_from':str(hi),
            'T_lower_display':float(lo),'T_upper_display':float(hi),'bracket_width':str(hi-lo),
            'exclude_iterations':lj,'accept_iterations':hj,'small_defect_entry':str(SMALL)}

def main():
    rows=[boundary(Q(k,1000)) for k in [700,750,800,825,850,875,900,925,950,975,990,999,1000]]
    data={'status':'Exact rational outward-certified asymmetric boundary brackets',
          'boundary_scope':'Legacy sequential map with improved but analytically equivalent basin entry u<=1/40',
          'rows':rows}
    (Path(__file__).resolve().parents[1]/'results'/'asymmetric_basin.json').write_text(json.dumps(data,indent=2))
    for r in rows:print(r['S'],r.get('T_lower_display'),r.get('T_upper_display'),flush=True)
if __name__=='__main__':main()
