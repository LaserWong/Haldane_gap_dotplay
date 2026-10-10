"""Exact upper bracket on the supported degree-five gap-polynomial class."""
from replay import *
from exact_utils import positive_definite

out=[]
for shape in ['4x4','8x4','8x8']:
 r=load(HERE/f'weighted_ground_{shape}.json');ex=load(HERE/f'moments_{shape}.json');G,A,B,C=[arr(m) for m in ex['moments_G_A_B_C']]
 a,U,L=map(F,[r['a'],r['U'],r['old_lower']]);ell=F(r['lower'])+F(1,10**10)
 p0=B-(a+ell)*A+a*ell*G;p1=C-(a+ell)*B+a*ell*A
 high=positive_definite(U*p0-p1);low=positive_definite(p1-L*p0)
 print(shape,'upper bracket',float(ell),'U-H',high['positive_definite'],'H-L',low['positive_definite'],flush=True)
 assert high['positive_definite'] and low['positive_definite']
 out.append(dict(shape=shape,L=str(L),U=str(U),a=str(a),ell_upper=str(ell),certified_lower=r['lower'],bracket_width='1/10000000000',upper_weight=high,lower_weight=low))
(HERE/'weight_class_result.json').write_text(json.dumps(dict(status='exact_positive_definite_replay',scope='Degree-five polynomials (x-a)(x-ell) times nonnegative cubic weights on the full inherited support interval [L,U], acting on base B; not all possible M0..M5 methods.',results=out),indent=2)+'\n')
