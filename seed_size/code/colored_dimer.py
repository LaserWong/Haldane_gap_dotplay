"""Certified dimer seeds using the two-color joint-mgf Hoeffding bound."""
import os
for v in ['OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS']:os.environ[v]='1'
from fractions import Fraction as Q
from pathlib import Path
from math import exp
import json
from scipy.optimize import minimize_scalar
from certified_core import exp_bounds,down,replay
from optimize_baselines import universal_z,float_replay,threshold,bilayer_cert
OUT=Path(__file__).resolve().parents[1]/'results'

def seed_float(w,beta,n=2):
    z=sum((2*j+1)*exp(-beta*j*(j+1)/2) for j in range(30))
    z2=sum((2*j+1)*exp(-beta*j*(j+1)) for j in range(30))
    return exp(-beta*beta*n*w*w/2),exp(-beta*beta*n*w*w)*(z2/z**2)**(2*n)

def certificate(w,beta,n=2):
    w,beta=map(Q,(w,beta));z=universal_z(beta);z2=universal_z(2*beta)
    S=down(exp_bounds(-beta*beta*n*w*w/2)[0])
    T=down(exp_bounds(-beta*beta*n*w*w)[0]*(z2[0]/z[1]**2)**(2*n))
    boot=replay(S,T,n,beta)
    return {'status':'exact_rational_seed_and_replay_with_analytic_coloring_hypotheses',
            'w':str(w),'beta':str(beta),'n_cells':n,'max_seed_trace_physical_sites':4*n,'m_actual_local_input_sites':2,'m_moment_order':None,
            'S_lower':str(S),'T_lower':str(T),'S_display':float(S),'T_display':float(T),
            'bootstrap':boot}

def main():
    opt=minimize_scalar(lambda b:-threshold(float_replay,seed_float,b,.15),bounds=(2.,12.),method='bounded')
    bet=Q(round(opt.x*10000),10000);w=Q(int(-opt.fun*1000000)-1,1000000)
    cert=certificate(w,bet);assert cert['bootstrap']['accepted']
    clean=certificate(Q(1,25),Q(6));assert clean['bootstrap']['accepted']
    rows=[certificate(Q(3,100),Q(k,20)) for k in range(60,201)]
    accepted=[r for r in rows if r['bootstrap']['accepted']]
    best=max(accepted,key=lambda r:Q(r['bootstrap']['gap_lower']))
    bclean=bilayer_cert(Q(1,1300),Q(9));assert bclean['accepted']
    data={'floating_proposal':{'w':float(-opt.fun),'beta':float(opt.x),'certified':False},
          'near_threshold':cert,'clean_w004':clean,'w003_best_grid_gap':best,'bilayer_clean':bclean}
    (OUT/'colored_dimer_certificates.json').write_text(json.dumps(data,indent=2))
    print('NEW DIMER BOUND proposal',-opt.fun,'beta',opt.x,flush=True)
    for key,row in [('near_threshold',cert),('clean_w004',clean),('w003_best_gap',best)]:
        b=row['bootstrap'];print(key,'w',row['w'],'beta',row['beta'],'S,T',row['S_display'],row['T_display'],'rounds',b.get('rounds'),'L0',b.get('L0'),'gap',float(Q(b['gap_lower'])) if b.get('gap_lower') else None,flush=True)
    print('BILAYER clean lambda=1/1300 beta9 rounds',bclean['rounds'],'nfinal',bclean['n_final'],flush=True)
if __name__=='__main__':main()
