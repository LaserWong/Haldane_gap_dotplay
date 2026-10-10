"""Cancel common heat traces BEFORE interval evaluation of bootstrap updates."""
import os
for v in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[v]='1'
from fractions import Fraction as Q
from pathlib import Path
from math import exp
import json,sys
from scipy.optimize import minimize_scalar
from certified_core import exp_bounds,down,up,G,replay,log_lower
from optimize_baselines import universal_z,float_replay,threshold
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parents[1]/'results'

def dimer_initial_float(w,beta,n=2):
    z=sum((2*j+1)*exp(-beta*j*(j+1)/2) for j in range(30))
    z2=sum((2*j+1)*exp(-beta*j*(j+1)) for j in range(30))
    # J=S^2*T exact cancellation; T from colored mgf.
    J=exp(-beta*beta*n*w*w)*(z2/z**2)**(2*n)
    T=J # Their certified lower bounds happen to coincide at this n under coloring.
    S1=1-(1-J)**2/(2*J*J)
    if S1<=0:return 0.,0.
    x=T*T*S1;T1=1-(1-x)**2/(2*x*x)
    if T1<=0:return 0.,0.
    return S1,T1

def dimer_certificate(w,beta,n=2):
    w,beta=map(Q,(w,beta));z=universal_z(beta);z2=universal_z(2*beta)
    J=down(exp_bounds(-beta*beta*n*w*w)[0]*(z2[0]/z[1]**2)**(2*n))
    T=J
    S1=down(G(J))
    if S1<=0:return {'accepted':False}
    T1=down(G(T*T*S1))
    if T1<=0:return {'accepted':False}
    b=replay(S1,T1,2*n,2*beta,small=Q(1,40))
    out={'accepted':b['accepted'],'w':str(w),'beta_initial':str(beta),'n_initial_cells':n,
         'max_seed_trace_physical_sites':4*n,'m_actual_local_input_sites':2,'m_moment_order':None,'J1_direct_lower':str(J),'T_initial_lower':str(T),
         'first_S_lower':str(S1),'first_T_lower':str(T1),'bootstrap_after_first_step':b,
         'small_defect_entry':'1/40','arithmetic':'128-bit dyadic outward rounding plus rational Taylor'}
    if b['accepted']:
        # Simple finite-size patch; a positive bound is necessary for all-M claim.
        patch=1-(b['L0']-1)*w
        out['finite_size_Weyl_patch']=str(patch)
        out['all_integer_M_ge2_gap']=str(min(Q(b['gap_lower']),patch)) if patch>0 else None
    return out

def replay3(A,B,C,n,m,beta,max_rounds=64):
    A,B,C,beta=map(Q,(A,B,C,beta));updates=[]
    for j in range(max_rounds+1):
        u=max(1-A,1-B,1-C)
        if u<=Q(1,500):
            return {'accepted':True,'rounds':j,'n':n,'m':m,'beta':str(beta),'u':str(u),
                    'purities':[str(v) for v in [A,B,C]],'updates':updates,
                    'gap_lower':str(down(log_lower(1/(32*u))/beta)) if u else None,
                    'scope':'Every integer square side L>=n if n=m; conditional on audited transfer/interpolation theorem'}
        for idx in range(3):
            x=A**4*B**2*C
            if x<=0:return {'accepted':False,'reason':'Nonpositive argument'}
            new=down(G(x))
            if new<=0:return {'accepted':False,'reason':'Nonpositive purity lower bound'}
            A,B,C=B,C,new
        n*=2;m*=2;beta*=2;updates.append([str(v) for v in [A,B,C]])
    return {'accepted':False,'reason':'Iteration budget; not an exclusion'}

def trace(rec,beta):
    beta=Q(beta);s=Q(rec['s']);N=rec['N_dimers']
    elo=Q(rec['ground_lower']);ehi=Q(rec['ground_upper']);E00=Q(rec['E00'])
    rb=rec.get('relative_form_bound')
    alpha=Q(rb['alpha']) if rb else Q(1);B=Q(rb['B']) if rb else -Q(rec['Vmin'])
    z=Q(1)
    for j in range(1,int(2*s)+1):z+=(2*j+1)*exp_bounds(-beta*alpha*Q(j*(j+1),2))[1]
    tail=up(exp_bounds(-beta*(E00-B-ehi))[1]*(z**N-1))
    return up(exp_bounds(beta*(ehi-elo))[1]+tail)

def bilayer_from_records(records,beta,correlated=True):
    r22,r42,r44=records;beta=Q(beta)
    U22,U42,U44=[Q(r['ground_upper']) for r in records]
    q22,q42,q44=[trace(r,beta) for r in records]
    C=down(1/q44**2)
    if correlated:
        J1=down(exp_bounds(-beta*(2*U44-8*U22))[0]/q22**8)
        J2=down(exp_bounds(-beta*(4*U44-8*U42))[0]/q42**8)
        A1=down(G(J1))
        if A1<=0:return {'accepted':False,'beta_initial':str(beta)}
        B1=down(G(J2*A1))
        if B1<=0:return {'accepted':False,'beta_initial':str(beta)}
        C1=down(G(C**4*A1**2*B1))
        if C1<=0:return {'accepted':False,'beta_initial':str(beta)}
        boot=replay3(A1,B1,C1,4,4,2*beta)
        seed={'J1_direct_lower':str(J1),'J2_direct_lower':str(J2),'C_initial_lower':str(C),
              'first_purities':list(map(str,[A1,B1,C1]))}
    else:
        A=down(exp_bounds(-beta*(U42-2*U22))[0]/q22**2)
        B=down(exp_bounds(-beta*(U44-2*U42))[0]/q42**2)
        boot=replay3(A,B,C,2,2,beta)
        seed={'purities':list(map(str,[A,B,C]))}
    return {'accepted':boot['accepted'],'beta_initial':str(beta),'correlated':correlated,'seed':seed,'bootstrap':boot}

def main():
    opt=minimize_scalar(lambda b:-threshold(float_replay,dimer_initial_float,b,.15),bounds=(2.,12.),method='bounded')
    near=dimer_certificate(Q(int(-opt.fun*1000000)-1,1000000),Q(round(opt.x*10000),10000))
    assert near['accepted']
    drows=[]
    for w in [Q(3,100),Q(1,25),Q(1,20),Q(11,200)]:
        rows=[dimer_certificate(w,Q(k,20)) for k in range(70,201)]
        ok=[r for r in rows if r['accepted']]
        best=max(ok,key=lambda r:Q(r['all_integer_M_ge2_gap'] or 0)) if ok else None
        drows.append({'w':str(w),'best_all_lengths':best})
        if best:print('CORRELATED DIMER',str(w),'beta',best['beta_initial'],'all-M gap',float(Q(best['all_integer_M_ge2_gap'] or 0)),flush=True)
    bilayers=[]
    for g in ['1d100','1d50']:
        paths=[ROOT/'low_energy'/f'bilayer_s1d2_{nx}x{ny}_g{g}_k{g}_q2_ground.json' for nx,ny in [(2,2),(4,2),(4,4)]]
        records=[json.loads(p.read_text()) for p in paths]
        for corr in [False,True]:
            rows=[bilayer_from_records(records,Q(k,2),corr) for k in range(12,81)]
            ok=[r for r in rows if r['accepted']]
            best=max(ok,key=lambda r:Q(r['bootstrap']['gap_lower'])) if ok else None
            bilayers.append({'g':g.replace('d','/'),'correlated':corr,'sources':list(map(str,paths)),'best_grid_gap':best})
            print('BILAYER',g,'correlated',corr,'beta',best['beta_initial'] if best else None,'gap',float(Q(best['bootstrap']['gap_lower'])) if best else None,flush=True)
    data={'dimer_float_proposal':{'w':float(-opt.fun),'beta':float(opt.x),'certified':False},
          'dimer_near_threshold':near,'dimer_examples':drows,'bilayers':bilayers}
    (OUT/'correlated_seed_results.json').write_text(json.dumps(data,indent=2))
if __name__=='__main__':main()
