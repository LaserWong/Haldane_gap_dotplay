"""Exact third moment and two-vector variational numerator; no filtered residual.

Only the original G/K/J and geometric F/S/V/W/X/Y/Z matrices are consumed.
All acceptance arithmetic uses Fraction or Python arbitrary-precision integers.
"""
import sys, json, hashlib
from pathlib import Path
from fractions import Fraction as F
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RES = HERE.parents[1]
sys.path.insert(0, str(RES / 'variational_numerator_filter'))
from filter_rayleigh import optimize_filter

def dot(x, matrix, y=None):
    if y is None: y=x
    return sum(a*F(matrix[i][j])*b for i,a in enumerate(x) for j,b in enumerate(y))

def third_moment(record, geom, coefficients=None):
    n=geom['pair_orbits']; d=n+1
    v=list(map(F, record['coefficients'] if coefficients is None else coefficients))
    indices=record['selected_basis_indices']
    assert indices[:d] == list(range(d))
    full=[F(0)]*(2*n+1)
    for i,c in zip(indices,v): full[i]=c
    b,c=full[:d],full[d:]
    G,K,J=[record[k] for k in ('gram','shifted_hamiltonian_numerator','shifted_H2_numerator')]
    den=record['integer_matrix_denominator'];t=F(record['coupling'])/2
    norm=dot(v,G);m1=dot(v,K)/den/norm;m2=dot(v,J)/den**2/norm
    a=[sum(F(K[i][j])*v[j] for j in range(len(v)))/den/F(G[i][i]) for i in range(d)]
    u=[4*c[i]+t*b[i+1] for i in range(n)]
    ff,ss,vv,ww=[geom[k] for k in ('F','S','V','W')]
    combined=[[geom['X'][i][j]+geom['Y'][i][j]+geom['Y'][j][i]+geom['Z'][i][j] for j in range(n)] for i in range(n)]
    low=sum(a[i]*F(K[i][j])*a[j]/den for i in range(d) for j in range(d))
    terms={
      'low_sector':low,
      'cross_q2_q4':2*t*(dot(a[1:],ff,u)+t*dot(a[1:],ss,c)),
      'q4_number':4*(dot(u,ff)+2*t*dot(u,ss,c)+t*t*dot(c,vv)),
      'q4_interaction_known':t*dot(u,ss)+2*t*t*dot(u,vv,c),
      'q6_number':6*t*t*dot(c,ww),
      'cross_q4_q6_known':2*t*t*dot(u,ww,c),
      'additional_contraction':t**3*dot(c,combined)
    }
    m3=sum(terms.values())/norm
    variance=m2-m1*m1
    rHr=m3-2*m1*m2+m1**3
    return dict(norm=norm,m1=m1,m2=m2,m3=m3,variance=variance,rHr=rHr,
                residual_Rayleigh=rHr/variance if variance else None,
                terms={k:v/norm for k,v in terms.items()}, combined=combined)

def certificate(record,geom):
    m=third_moment(record,geom);rho,v,R=m['m1'],m['variance'],m['residual_Rayleigh']
    assert rho+F(record['E00'])==F(record['exact_rayleigh'])
    assert v==F(record['exact_residual_squared']) and v>0 and R>rho
    filtered=optimize_filter(rho,v,R,digits=36)
    return dict(status='exact_third_moment_two_vector_variational_candidate_pending_independent_review',
       nx=record['nx'],ny=record['ny'],coupling=record['coupling'],
       physical_spins=2*record['nx']*record['ny'],full_dimension=record['full_dimension'],
       original_trial_dimension=len(record['coefficients']),filter_plane_dimension_upper=2,
       original_space_plus_residual_dimension_upper=len(record['coefficients'])+1,
       retained_numerator_states=1,original_max_triplet_number=4,filtered_max_triplet_number=6,
       no_q8_support_constructed=True,no_filtered_residual_claim=True,no_H4_of_original_trial_claim=True,
       exact_original_norm=str(m['norm']),exact_original_shifted_rayleigh=str(rho),
       exact_second_moment=str(m['m2']),exact_third_moment=str(m['m3']),
       exact_original_variance=str(v),exact_residual_H_expectation=str(m['rHr']),
       exact_residual_Rayleigh=str(R),residual_Rayleigh_display=float(R),
       rational_two_vector_gram=[['1','0'],['0',str(v)]],
       rational_two_vector_H=[[str(rho),str(v)],[str(v),str(m['rHr'])]],
       third_moment_contributions={k:str(v) for k,v in m['terms'].items()},
       filter=filtered,shifted_rayleigh_upper=filtered['shifted_rayleigh_upper'],
       energy_rayleigh_upper=str(F(record['E00'])+F(filtered['shifted_rayleigh_upper'])),
       shifted_rayleigh_upper_display=float(F(filtered['shifted_rayleigh_upper'])),
       variational_improvement_display=float(F(filtered['improvement'])))

def main():
    source=Path(sys.argv[1]).resolve();gp=Path(sys.argv[2]).resolve();out=Path(sys.argv[3])
    r=certificate(json.loads(source.read_text()),json.loads(gp.read_text()))
    r['source_sha256']={str(p.relative_to(RES)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,gp)}
    out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ('nx','ny','residual_Rayleigh_display','shifted_rayleigh_upper_display','variational_improvement_display')}))
if __name__=='__main__':main()
