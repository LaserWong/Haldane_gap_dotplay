from replay import *
from exact_utils import positive_definite

p=RES/'low_band/third_moment_exact/enlarged_8x8_g1d10.json';r=load(p);G=arr(r['gram']);A=arr(r['shifted_H_numerator'])*F(1,r['integer_matrix_denominator']);up=F(r['shifted_rayleigh_upper']);lo=up-F(1,10**10)
result=positive_definite(A-lo*G);assert result['positive_definite']
c=np.array(r['coefficients'],dtype=object);assert F(c@A@c)/F(c@G@c)==up
out=dict(status='exact_fixed_trial_space_ritz_bracket',lower=str(lo),upper=str(up),width='1/10000000000',trial_dimension=len(G),lower_matrix_positive_definite=result,source_sha256={str(p.relative_to(RES)):sha(p)},limitation='Only the fixed 43D trial space; not a physical ground lower bound and not an exclusion of stronger other numerator spaces.')
(HERE/'numerator_floor.json').write_text(json.dumps(out,indent=2)+'\n');print('43D Ritz bracket',float(lo),float(up))
