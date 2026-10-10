"""Exact replay of the reported two- and three-direction witnesses from independent moments."""
import audit as A
F=A.F
import json,math
m=json.loads((A.HERE/'independent_moments.json').read_text());raw=list(map(F,m['scaled_moments']));den=m['integer_denominator'];N=raw[0];mu=[raw[i]/(N*den**i) for i in range(6)];rho=mu[1]
rec=json.loads((A.BASE/'chain_frontier_rank195/expanded_inputs.json').read_text())[0];rho4=F(rec['small']['exact_rayleigh']);target=2*rho4+F(19,1250)
cm=[sum(F(math.comb(i,j))*(-rho)**(i-j)*mu[j] for j in range(i+1)) for i in range(6)]
var=mu[2]-rho*rho;hrr=mu[3]-2*rho*mu[2]+rho**3
s=json.loads((A.SNAP/'rayleigh.json').read_text());tau=F(s['tau']);q=(rho+2*tau*var+tau*tau*hrr)/(1+tau*tau*var)
assert var>0 and s['trial_dimension']==2 and F(s['variance'])==var and F(s['centered_H_moment'])==hrr and F(s['residual_direction_rayleigh'])==hrr/var
G2=[[F(1),F(0)],[F(0),var]];H2=[[rho,var],[var,hrr]];piv=A.ldlt([[H2[i][j]-target*G2[i][j] for j in range(2)] for i in range(2)]);assert piv==list(map(F,s['span_target_LDL_pivots'])) and s['span_exclusion'] is True
assert q==F(s['exact_rayleigh']) and rho-q==F(s['improvement']) and q-2*rho4==F(s['new_delta']) and q>target==F(s['necessary_target_rayleigh']) and not s['meets_necessary_target']
r2=dict(rank=2,exact_rayleigh=str(q),improvement=str(rho-q),new_delta=str(q-2*rho4),target_positive_pivots=list(map(str,piv)))
s=json.loads((A.SNAP/'rayleigh_three.json').read_text());G=[[cm[i+j] for j in range(3)] for i in range(3)];K=[[cm[i+j+1] for j in range(3)] for i in range(3)]
assert s['trial_dimension']==3 and list(map(F,s['moments']))==mu and list(map(F,s['centered_moments']))==cm and [list(map(F,r)) for r in s['Gram']]==G and [list(map(F,r)) for r in s['centered_H']]==K
c=list(map(F,s['coefficients']));assert len(c)==3;bil=lambda M:sum(c[i]*M[i][j]*c[j] for i in range(3) for j in range(3));norm=bil(G);assert norm>0;q=rho+bil(K)/norm
piv=A.ldlt([[K[i][j]+(rho-target)*G[i][j] for j in range(3)] for i in range(3)]);gp=A.ldlt(G)
assert piv==list(map(F,s['span_target_LDL_pivots'])) and s['span_exclusion'] is True and q==F(s['exact_rayleigh']) and rho-q==F(s['improvement']) and q-2*rho4==F(s['new_delta']) and q>target==F(s['necessary_target_rayleigh']) and not s['meets_necessary_target']
r3=dict(rank=3,exact_rayleigh=str(q),improvement=str(rho-q),new_delta=str(q-2*rho4),Gram_positive_pivots=list(map(str,gp)),target_positive_pivots=list(map(str,piv)))
A.save('nested_span_review.json',dict(status='PASS',two_dimensional=r2,three_dimensional=r3));print('NESTED TWO AND THREE DIMENSIONAL CHECKS PASS',flush=True)
