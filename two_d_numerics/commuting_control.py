"""Exact trace-histogram control with nonzero interactions along both axes.
Spin-1 H=sum_i (Sz_i)^2 + g*sum_edges (Sz_i)^2(Sz_j)^2.
All terms commute. g>=0 implies a unique zero-energy all-m=0 ground state
and gap exactly one. Weighted binary occupancy enumeration replaces full ED.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import sys,json
import numpy as np
from models import square
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/'two_d_theory'))
from three_purity_certificate import exp_interval,replay,down

def histogram(nx,ny,g):
    g=F(g);den=g.denominator
    assert g>=0 and nx*ny<=16
    edges=square(1.,nx,ny,periodic_x=True,periodic_y=True).edges
    counts=Counter()
    for bits in range(1<<(nx*ny)):
        k=bits.bit_count();b=sum(((bits>>e.i)&1)*((bits>>e.j)&1) for e in edges)
        E=den*k+g.numerator*b
        counts[E]+=1<<k
    assert sum(counts.values())==3**(nx*ny)
    assert counts[0]==1 and min(e for e in counts if e)>0
    assert min(e for e in counts if e)==den
    return counts,den

def partition(counts,den,beta):
    lo=F(0);hi=F(0)
    for e,m in counts.items():
        a,b=exp_interval(-F(beta)*e/den);lo+=m*a;hi+=m*b
    return lo,hi

def certify(g=F(1,10),beta=F(8)):
    recs=[]
    for nx,ny in [(2,2),(4,2),(4,4)]:
        h,den=histogram(nx,ny,g);lo,hi=partition(h,den,beta)
        recs.append(dict(nx=nx,ny=ny,dimension=3**(nx*ny),enumerated_occupancies=2**(nx*ny),energy_denominator=den,counts={str(e):c for e,c in sorted(h.items())},Zlo=lo,Zhi=hi))
    z2lo,z2hi=partition(h,den,2*beta)
    A=down(recs[1]['Zlo']/recs[0]['Zhi']**2)
    B=down(recs[2]['Zlo']/recs[1]['Zhi']**2)
    C=down(z2lo/recs[2]['Zhi']**2)
    out=dict(model='spin1_commuting_occupancy_control',g=str(g),beta=str(beta),periodic='both, length-two multibonds',unique_ground=True,exact_gap='1',full_spectrum_diagonalization=False,purity_lowers=list(map(str,(A,B,C))),purity_lower_displays=list(map(float,(A,B,C))),bootstrap=replay(A,B,C,beta=beta),histograms=[{k:v for k,v in r.items() if k not in ['Zlo','Zhi']} for r in recs])
    (BASE/'results/commuting_control_certificate.json').write_text(json.dumps(out,indent=2))
    print({k:v for k,v in out.items() if k!='histograms'})
if __name__=='__main__':certify()
