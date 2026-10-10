import sys,json,time
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parent
sys.path.insert(0,str(RES/'bilayer_seed_error_budget'))
from budget import C,P
r=json.load(open(RES/'low_band/third_moment_exact/enlarged_4x4_g9d100.json'));geo=json.load(open(RES/'low_band/third_moment_exact/geometry_4x4_origin.json'));n=geo['pair_orbits'];d=n+1;np=P.np
G=np.array(r['gram'],dtype=object);K0=np.zeros_like(G);K0[:d,:d]=G[:d,:d]@np.diag([0]+[2]*n)
ff,ss,vv,ww=[np.array(geo[k],dtype=object) for k in ('F','S','V','W')]
K0[d:d+n,d:d+n]=4*ff;K0[d:d+n,d+n:]=4*ss;K0[d+n:,d:d+n]=4*ss.T;K0[d+n:,d+n:]=4*vv+6*ww
K=np.array([[F(x,r['integer_matrix_denominator']) for x in row] for row in r['shifted_H_numerator']],dtype=object);K1=(K-K0)/F(r['coupling']);assert len(G)==16
model={'geometry':[4,4],'N':16,'trial_dimension':16,'G':G,'first_moment_coefficients':[K0,K1]};g=F(21,200);v=C.optimized_vector(model,g);tr=C.trial(model,g,v);rho=C.poly(list(map(F,tr['rayleigh_coefficients'])),g);a=C.reference(g,16,2);target=F(json.load(open(RES/'bilayer_seed_error_budget/joint_targets.json'))['results'][0]['target_ground16_lower']);budget=(rho-target)*(a-rho)
r={'status':'uncontracted16D_trial_and_residual_target_only','g':str(g),'trial':tr,'shifted_Rayleigh':str(rho),'shifted_Rayleigh_display':float(rho),'target_ground_lower':str(target),'complete_residual_squared_budget':str(budget),'budget_display':float(budget),'budget_positive':budget>0,'full_image_max_q':8,'fixed_origin_q4_supports':455,'fixed_origin_q6_supports':3003,'basis':'B(6) + L(5) + U(5): adds five already-known H-applied directions to the11D B+L space','cost_estimate':'Same exact commutator technique;about56.6-fold fewer q6 supports than8x4. Expected well below1s plus startup, not measured. Conservative initial gate40CPU seconds/100MiB.'}
(HERE/'outline_4x4.json').write_text(json.dumps(r,indent=2)+'\n');print({k:r[k] for k in ['shifted_Rayleigh_display','budget_display','budget_positive']})
