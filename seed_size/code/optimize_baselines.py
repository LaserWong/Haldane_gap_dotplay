"""Floating proposals followed by independent exact-rational certification."""
import os
for v in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[v]='1'
from fractions import Fraction as Q
from pathlib import Path
from math import exp,log
import json
import numpy as np
from scipy.optimize import differential_evolution, minimize_scalar
from certified_core import exp_bounds,down,up,G,replay,log_lower
OUT=Path(__file__).resolve().parents[1]/'results'

def float_replay(S,T):
    for j in range(64):
        if max(1-S,1-T)<=.01:return j,S,T
        if S*S*T<=.5:return None
        S=1-(1-S*S*T)**2/(2*(S*S*T)**2)
        if S<=0:return None
        x=T*T*S;T=1-(1-x)**2/(2*x*x)
        if T<=0:return None
    return None

def dimer_float(w,beta,n=2):
    z=sum((2*j+1)*exp(-beta*j*(j+1)/2) for j in range(30))
    z2=sum((2*j+1)*exp(-beta*j*(j+1)) for j in range(30))
    return exp(-(beta*n*w)**2/4),exp(-(beta*n*w)**2)*(z2/z**2)**(2*n)

def universal_z(beta):
    """Infinite-spin dimer trace: J>=2 tail geometric ratio <=7/5 exp(-3 beta)."""
    beta=Q(beta)
    e1=exp_bounds(-beta);e3=exp_bounds(-3*beta)
    ratio=up(Q(7,5)*e3[1]);assert ratio<1
    return down(1+3*e1[0]+5*e3[0]),up(1+3*e1[1]+5*e3[1]/(1-ratio))

def dimer_cert(w,beta,n=2):
    w,beta=map(Q,(w,beta));z=universal_z(beta);z2=universal_z(2*beta)
    S=down(exp_bounds(-(beta*n*w)**2/4)[0])
    T=down(exp_bounds(-(beta*n*w)**2)[0]*(z2[0]/z[1]**2)**(2*n))
    boot=replay(S,T,n,beta)
    return {'w':str(w),'beta':str(beta),'n_cells':n,'max_seed_trace_physical_sites':4*n,'m_actual_local_input_sites':2,'m_moment_order':None,
            'S_lower':str(S),'T_lower':str(T),'S_display':float(S),'T_display':float(T),'bootstrap':boot}

def float_3(A,B,C):
    for j in range(64):
        u=max(1-A,1-B,1-C)
        if u<=.01:return j,A,B,C
        x=A**4*B**2*C
        if x<=0:return None
        A=1-(1-x)**2/(2*x*x)
        if A<=0:return None
        x=B**4*C**2*A;B=1-(1-x)**2/(2*x*x)
        if B<=0:return None
        x=C**4*A**2*B;C=1-(1-x)**2/(2*x*x)
        if C<=0:return None
    return None

def bilayer_float(lam,beta):
    x=beta*lam
    return exp(-64*x*x),exp(-256*x*x),exp(-1024*x*x)*(1+3*exp(-beta))**-32

def bilayer_cert(lam,beta):
    lam,beta=map(Q,(lam,beta));x=beta*lam
    A=down(exp_bounds(-64*x*x)[0]);B=down(exp_bounds(-256*x*x)[0])
    C=down(exp_bounds(-1024*x*x)[0]/(1+3*exp_bounds(-beta)[1])**32)
    seed=[A,B,C];updates=[]
    for j in range(65):
        u=max(1-A,1-B,1-C)
        if u<=Q(1,100):
            return {'accepted':True,'lambda':str(lam),'beta':str(beta),
                    'seed_lower':[str(v) for v in seed],'seed_display':[float(v) for v in seed],
                    'rounds':j,'final_defects':[str(1-v) for v in [A,B,C]],
                    'u':str(u),'n_final':2*2**j,'m_final':2*2**j,'beta_final':str(beta*2**j),
                    'updates':updates,'gap_not_emitted':'Awaiting verified all-rectangle interpolation constants'}
        A=down(G(A**4*B**2*C))
        if A<=0:break
        B=down(G(B**4*C**2*A))
        if B<=0:break
        C=down(G(C**4*A**2*B))
        if C<=0:break
        updates.append([str(v) for v in [A,B,C]])
    return {'accepted':False,'lambda':str(lam),'beta':str(beta)}

def threshold(fun,seed,beta,upper):
    lo=0.;hi=upper
    for _ in range(45):
        m=(lo+hi)/2
        if fun(*seed(m,beta)) is not None:lo=m
        else:hi=m
    return lo

def main():
    opt=minimize_scalar(lambda b:-threshold(float_replay,dimer_float,b,.15),bounds=(2.,12.),method='bounded')
    proposal={'beta':float(opt.x),'w':float(-opt.fun),'evidence':'Floating proposal only'}
    print('DIMER PROPOSAL',proposal,flush=True)
    bet=Q(round(opt.x*10000),10000);w=Q(int(-opt.fun*1000000)-1,1000000)
    dcert=dimer_cert(w,bet);assert dcert['bootstrap']['accepted']
    # Also optimize certified final gap among candidate beta and a handful of rounds for legacy w=.03.
    rows=[dimer_cert(Q(3,100),Q(k,20)) for k in range(60,201)]
    accepted=[r for r in rows if r['bootstrap']['accepted']]
    best=max(accepted,key=lambda r:Q(r['bootstrap']['gap_lower']))
    print('DIMER CERT',str(w),str(bet),'rounds',dcert['bootstrap']['rounds'],flush=True)
    print('DIMER w=.03 BEST GAP beta',best['beta'],'gap',float(Q(best['bootstrap']['gap_lower'])),'L0',best['bootstrap']['L0'],flush=True)
    opt=minimize_scalar(lambda b:-threshold(float_3,bilayer_float,b,.01),bounds=(4.,20.),method='bounded')
    prop3={'beta':float(opt.x),'lambda':float(-opt.fun),'evidence':'Floating proposal only'}
    print('BILAYER PROPOSAL',prop3,flush=True)
    bet3=Q(round(opt.x*10000),10000);lam=Q(int(-opt.fun*100000000)-1,100000000)
    bcert=bilayer_cert(lam,bet3);assert bcert['accepted']
    bclean=bilayer_cert(Q(1,1000),Q(10))
    print('BILAYER CERT',str(lam),str(bet3),'rounds',bcert['rounds'],'clean',bclean.get('accepted'),flush=True)
    (OUT/'optimized_baselines.json').write_text(json.dumps({'dimer_float_proposal':proposal,
       'dimer_near_threshold_certificate':dcert,'dimer_w003_best_grid_gap':best,
       'bilayer_float_proposal':prop3,'bilayer_near_threshold_certificate':bcert,
       'bilayer_clean_certificate':bclean},indent=2))
if __name__=='__main__': main()
