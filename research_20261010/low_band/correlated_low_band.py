"""Correlated heat-trace cancellation with complete low-band numerators."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,math,argparse
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize_scalar
from low_band_certificate import OUT,traces,exp_bounds,down,replay

def G(x):return 1-(1-x)**2/(2*x*x)
def load(g='3d100',number=False):
    return [json.loads((OUT/f'bilayer_{x}x{y}_g{g}_{"number_" if number else ""}low_band.json').read_text()) for x,y in [(2,2),(4,2),(4,4)]]
def traces_float(rec,beta):
    N=rec['N'];alpha=float(F(rec['relative_form_bound']['alpha']));B=float(F(rec['relative_form_bound']['B']))
    shift=float(F(rec['blocks'][0]['eigen_upper'][0]));lo=0.;hi=0.
    for b in rec['blocks']:
        lo+=b['multiplicity']*sum(math.exp(-beta*(float(F(e))-shift)) for e in b['eigen_upper'])
        hi+=b['multiplicity']*sum(math.exp(-beta*(float(F(e))-shift)) for e in b['eigen_lower'])
    tail=math.exp(beta*(B+shift))*sum(math.comb(N,j)*3**j*math.exp(-beta*alpha*j) for j in range(2,N+1))
    if "number_sector_bins" in rec:
        tail=sum(row["multiplicity"]*math.exp(-beta*(float(F(row["lower"]))-shift)) for row in rec["number_sector_bins"]["bins"][2:])
    return lo,hi+tail,tail

def float_initial(recs,beta,order='xyt'):
    # Axis swaps x<->y are identical because each retained seed patch is square
    # or its rotated rectangle. Three placements of the temperature axis remain.
    q=lambda i,b:traces_float(recs[i],b)
    e=[float(F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0])) for r in recs]
    q0=q(0,beta);q3=q(2,2*beta)
    if order[0]=='t':i1,b1=0,2*beta
    else:i1,b1=1,beta
    if order[-1]=='t':i2,b2=2,beta
    else:i2,b2=1,2*beta
    q1=q(i1,b1);q2=q(i2,b2)
    J1=math.exp(-2*beta*e[2]+8*beta*e[0])*q3[0]/q0[1]**8
    J2=math.exp(-4*beta*e[2]+8*b1*e[i1])*q3[0]**2/q1[1]**8
    C=math.exp(-2*beta*e[2]+2*b2*e[i2])*q3[0]/q2[1]**2
    A1=G(J1)
    if A1<=0:return None
    B1=G(J2*A1)
    if B1<=0:return None
    C1=G(C**4*A1**2*B1)
    if C1<=0:return None
    return [A1,B1,C1]

def float_score(recs,beta,order):
    ABC=float_initial(recs,beta,order)
    if ABC is None:return 1.
    for r in range(16):
        u=max(1-x for x in ABC)
        if u<=.002:return -math.log(1/(32*u))/(beta*2**(r+1)) if u>0 else -1.
        for _ in range(3):
            val=G(ABC[0]**4*ABC[1]**2*ABC[2])
            if val<=0:return 1.+u
            ABC=ABC[1:]+[val]
    return max(1-x for x in ABC)

def exact(recs,beta,order='xyt'):
    beta=F(beta);e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
    q0=traces(recs[0],beta);q3=traces(recs[2],2*beta)
    if order[0]=='t':i1,b1=0,2*beta
    else:i1,b1=1,beta
    if order[-1]=='t':i2,b2=2,beta
    else:i2,b2=1,2*beta
    q1=traces(recs[i1],b1);q2=traces(recs[i2],b2)
    J1=down(exp_bounds(-2*beta*e[2]+8*beta*e[0])[0]*q3[0]/q0[1]**8,digits=16)
    J2=down(exp_bounds(-4*beta*e[2]+8*b1*e[i1])[0]*q3[0]**2/q1[1]**8,digits=16)
    C=down(exp_bounds(-2*beta*e[2]+2*b2*e[i2])[0]*q3[0]/q2[1]**2,digits=16)
    row=dict(beta_initial=str(beta),order=order,J1=str(J1),J2=str(J2),C=str(C),accepted=False)
    A1=down(G(J1),digits=16)
    if A1<=0:return row
    B1=down(G(J2*A1),digits=16)
    if B1<=0:return row
    C1=down(G(C**4*A1**2*B1),digits=16)
    if C1<=0:return row
    boot=replay(A1,B1,C1,n=4,m=4,beta=2*beta,rounds=64,digits=18)
    row.update(first_purities=list(map(str,[A1,B1,C1])),first_purities_display=list(map(float,[A1,B1,C1])),bootstrap=boot,accepted=boot['status']=='accepted_analytic_scalar_certificate')
    if order!='xyt':row['scope_caveat']='Axis-permuted scalar replay requires transfer/interpolation proof in the same staircase order.'
    return row

def main():
    p=argparse.ArgumentParser();p.add_argument('--g',default='3d100');p.add_argument('--number',action='store_true');a=p.parse_args();recs=load(a.g,a.number)
    proposals=[];exactrows=[]
    for order in ['xyt','xty','txy']:
        grid=[(float_score(recs,b/20,order),F(b,20)) for b in range(100,501)]
        best=sorted(grid)[:4]
        for score,beta in best:
            print('PROPOSAL',order,float(beta),score,flush=True)
            row=exact(recs,beta,order);exactrows.append(row)
            print('EXACT',order,beta,row.get('first_purities_display'),row.get('bootstrap'),flush=True)
        proposals.append(dict(order=order,best_grid=[dict(beta=str(b),score=s) for s,b in best]))
    (OUT/f'correlated_full_low_band_g{a.g}_{"number" if a.number else "affine"}.json').write_text(json.dumps(dict(float_proposals=proposals,exact_results=exactrows),indent=2))
if __name__=='__main__':main()
