"""Certified no-overlap temperature windows for a fixed n.

A failed floating/grid search is not a theorem. This test proves a thermal
necessary lower-beta cutoff and a spatial necessary upper-beta cutoff using
independently counted low levels and an upper excitation tail.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from certified_core import exp_bounds,down,up
from asymmetric_basin import classify
from spectral_search import exact_n2_pair

# Each endpoint is independently checked as a failed scalar seed.
TAU_S=Q(3,4)
TAU_T=Q(79,100)
assert classify(TAU_S,1)[0]=='excluded'
assert classify(1,TAU_T)[0]=='excluded'

def thermal_max_probability_upper(spectrum,beta):
    # Every counted level has gap <= hi, hence it contributes >=exp(-beta hi).
    R=sum((c*exp_bounds(-Q(beta)*hi)[0] for lo,hi,c in spectrum.bins if hi),Q(0))
    return up(1/(1+R))

def spatial_low_temperature_upper(pair,beta):
    # Drop the positive denominator Q_n(beta)^2>=1; this is monotone decreasing.
    return up(exp_bounds(-Q(beta)*pair.Clo)[1]*pair.b.trace(beta)[1])

def window(pair,bits=28):
    if pair.Clo<=0:return {'excluded':False,'reason':'Positive C_lower unavailable'}
    # Largest certified beta below which T<=tau_T. Monotonic P0 makes this a necessary lower cutoff.
    lo=Q(0);hi=Q(1)
    while thermal_max_probability_upper(pair.b,hi)<=TAU_T:lo=hi;hi*=2
    for _ in range(bits):
        m=(lo+hi)/2
        if thermal_max_probability_upper(pair.b,m)<=TAU_T:lo=m
        else:hi=m
    thermal_lower=lo
    # Smallest certified beta above which S<=tau_S. Every numerator-tail term decreases.
    lo=Q(0);hi=Q(1)
    while spatial_low_temperature_upper(pair,hi)>TAU_S:lo=hi;hi*=2
    for _ in range(bits):
        m=(lo+hi)/2
        if spatial_low_temperature_upper(pair,m)<=TAU_S:hi=m
        else:lo=m
    spatial_upper=hi
    return {'n_bootstrap':pair.n,'m_input':pair.m_input,'tau_S':str(TAU_S),'tau_T':str(TAU_T),
            'necessary_beta_greater_than':str(thermal_lower),'necessary_beta_less_than':str(spatial_upper),
            'thermal_cutoff_display':float(thermal_lower),'spatial_cutoff_display':float(spatial_upper),
            'excluded':thermal_lower>=spatial_upper,
            'interpretation':'A rigorous no-overlap proof for this n and scalar recursion, not an m-order obstruction'}

def main():
    rows=[]
    for t in [2,4,6]:
        r=window(exact_n2_pair(t));r['spin']=str(Q(t,2));assert r['excluded'];rows.append(r)
        print('spin',Q(t,2),'necessary beta>',r['thermal_cutoff_display'],'and <',r['spatial_cutoff_display'],flush=True)
    (Path(__file__).resolve().parents[1]/'results'/'necessary_temperature_windows.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
