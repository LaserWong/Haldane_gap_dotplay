"""Exact-rational checks for the alternating-spin-chain purity certificate.
All accepted comparisons use Fraction. Floating values are display only.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import sys
import json

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bootstrap_scalar import replay

def exp_pos(x, terms=120):
    x = F(x)
    assert x >= 0 and x < terms + 2
    term = F(1)
    total = term
    for k in range(1, terms + 1):
        term *= x / k
        total += term
    first = term * x / (terms + 1)
    return total, total + first / (1 - x / (terms + 2))

def exp_bounds(x):
    x = F(x)
    if x >= 0:
        return exp_pos(x, max(120, int(x) * 3 + 40))
    lo, hi = exp_pos(-x, max(120, int(-x) * 3 + 40))
    return 1 / hi, 1 / lo

def down(x, digits=12):
    return F(x.numerator * 10**digits // x.denominator, 10**digits)

def cert(s=F(3,2), g=F(1,200), beta=F(6), n=2):
    # Upper bound on the shifted isolated-dimer partition function.
    zlo = F(0)
    zhi = F(0)
    for j in range(int(2*s)+1):
        lo, hi = exp_bounds(-beta * F(j*(j+1), 2))
        zlo += (2*j+1)*lo
        zhi += (2*j+1)*hi
    width = s*(2*s+1)
    delta_n = (beta*g*n*width)**2 / 8
    delta_2n = 4*delta_n
    S = down(exp_bounds(-2*delta_n)[0])
    T = down(exp_bounds(-2*delta_2n)[0] / zhi**(4*n))
    boot = replay(str(S), str(T), n, str(beta))
    return {'s':str(s), 'g':str(g), 'beta':str(beta), 'n_cells':n,
            'max_physical_seed_sites':4*n,
            'dimer_z_upper':str(down(zhi+F(1,10**12))),
            'hoeffding_delta_n':str(delta_n),
            'S_lower':str(S),'T_lower':str(T),
            'S_lower_display':float(S),'T_lower_display':float(T),
            'bootstrap':boot}

def main():
    # Same rescaled perturbation, g*s*(2s+1)=3/100.
    rows=[]
    for s in [F(1),F(3,2),F(2),F(5,2),F(3),F(7,2),F(4),F(5)]:
        g=F(3,100)/(s*(2*s+1))
        r=cert(s,g)
        assert r['bootstrap']['status']=='accepted_conditional_scalar_seed'
        rows.append(r)
        b=r['bootstrap']
        print(s,g,'S,T',r['S_lower_display'],r['T_lower_display'],
              'rounds',b['rounds'],'cells',b['final_n'],'gap',
              b.get('conditional_gap_lower_rational'),flush=True)
    # A spin-independent upper bound: J>=2 terms have ratio at most 7e^-18/5.
    e6=exp_bounds(-6)[1]
    e18=exp_bounds(-18)[1]
    zinf_upper=1+3*e6+5*e18/(1-F(7,5)*e18)
    assert zinf_upper < F(1007437,1000000)
    universal=cert(F(3,2),F(1,200))
    S=down(exp_bounds(-F(81,2500))[0])
    T=down(exp_bounds(-F(81,625))[0] / F(1007437,1000000)**8)
    b=replay(str(S),str(T),2,'6')
    assert b['status']=='accepted_conditional_scalar_seed'
    # Constants used in the extension from even cell counts to every cell count.
    u=F(1,100)
    assert u < F(1,8)
    assert 9/(2*(1-3*u)**2) < 5
    assert (2+5*u)**2/(2*(1-(2+5*u)*u)**2) < 5
    assert F(3,2)+5*u+2/(1-2*u) < 4
    assert 4/(1-4*u) < 5
    data={'status':'exact_rational_scalar_and_exponential_certificates',
          'scope_note':'Analytic transfer and Hoeffding proofs are in REPORT.md. No large-chain diagonalization is used.',
          'rows':rows,
          'universal':{'condition':'abs(g)*s*(2*s+1) <= 3/100',
                       'general_cell_condition':'width(v)<=3/100, invariant under cell time reversal and left-right exchange',
                       'analytic_scope':'Every integer number M>=2 of two-spin cells, by REPORT.md Sections 3-4. Analytic proof is not proof-assistant formalized.',
                       'S_lower':str(S),'T_lower':str(T),
                       'S_lower_display':float(S),'T_lower_display':float(T),
                       'bootstrap':b,
                       'all_integer_cell_interpolation_constants_checked':True}}
    (BASE/'results'/'analytic_dimer_certificates.json').write_text(json.dumps(data,indent=2))
    print('UNIVERSAL',float(S),float(T),b['rounds'],b['final_n'],b['final_common_u'],b['conditional_gap_lower_rational'])

if __name__=='__main__':
    main()
