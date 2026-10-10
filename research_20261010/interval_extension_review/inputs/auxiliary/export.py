"""Fixed inverse-moment witnesses as polynomial scalar trial inputs.

Read-only reuse of existing exact G/A/B at three couplings determines the
matrix polynomial; every one of the 21 saved physical matrices is then checked
against that polynomial. No new physical moments are constructed.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import json,hashlib
HERE=Path(__file__).resolve().parent;PENCIL=HERE.parent/'ground_moment_pencil';RES=HERE.parent.parent
sys.path.insert(0,str(PENCIL))
from propose import paths


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def read(g,nx,ny):
    p=paths(g,nx,ny)[0];j=json.loads(p.read_text());d=j['integer_matrix_denominator']
    G,A,B=[np.array(j[k],dtype=object) for k in ('gram','shifted_hamiltonian_numerator','shifted_H2_numerator')]
    return G,A*F(1,d),B*F(1,d*d),j,p


def serialize(matrix):return [[str(x) for x in row] for row in matrix]


def main():
    summary=[];sources={}
    for nx,ny in ((4,4),(8,4),(8,8)):
        g0,h=F(3,100),F(1,100)
        raw=[read(g0+i*h,nx,ny) for i in range(3)]
        G=raw[0][0];indices=raw[0][3]['selected_basis_indices']
        assert all(np.array_equal(r[0],G) and r[3]['selected_basis_indices']==indices for r in raw)
        A1=(raw[1][1]-raw[0][1])/h;A0=raw[0][1]-g0*A1
        B2=(raw[2][2]-2*raw[1][2]+raw[0][2])/(2*h*h)
        B1=(raw[1][2]-raw[0][2])/h-(2*g0+h)*B2
        B0=raw[0][2]-g0*B1-g0*g0*B2
        polynomial=dict(nx=nx,ny=ny,trial_dimension=len(G),selected_basis_indices=indices,
          energy_shift=raw[0][3]['E00'],gram=serialize(G),shifted_A_coefficients=[serialize(A0),serialize(A1)],
          full_shifted_B_coefficients=[serialize(B0),serialize(B1),serialize(B2)],
          basis='Same g-independent vacuum/pair and A42 pair-orbit basis as the audited full moments',
          derivation='Exact degree1/degree2 interpolation at 3/100,1/25,1/20, checked against all seven couplings. Degree bound follows H(g)=H(0)+gV and fixed basis.')
        for row in raw:sources[str(row[4].relative_to(RES))]=digest(row[4])
        for g in map(F,('3/100','1/25','1/20','3/50','7/100','2/25','1/10')):
            gg,aa,bb,gr,gp=read(g,nx,ny)
            assert np.array_equal(gg,G) and gr['selected_basis_indices']==indices
            assert np.array_equal(aa,A0+g*A1)
            assert np.array_equal(bb,B0+g*B1+g*g*B2)
            source=PENCIL/f'ground_{nx}x{ny}_g{g}.json'.replace('/','d');old=json.loads(source.read_text())
            ep=old['pencil']['endpoints'][0];w=ep['negative_direction_witness'];c=np.array(w['coefficients'],dtype=object)
            norm=F(c@G@c);assert norm>0
            R=[F(c@M@c)/norm for M in (A0,A1)]
            Q=[F(c@M@c)/norm for M in (B0,B1,B2)]
            V=[Q[0]-R[0]**2,Q[1]-2*R[0]*R[1],Q[2]-R[1]**2]
            rho=R[0]+g*R[1];variance=V[0]+g*V[1]+g*g*V[2]
            a=F(old['pencil']['external_cutoff']);l=F(old['ground_lower'])
            endpoint_form=(rho-a)*(rho-l)+variance
            assert endpoint_form==F(w['exact_endpoint_quadratic_form'])/norm<0
            assert variance>=0 and l<rho<a
            temple=rho-variance/(a-rho);assert temple>l
            row=dict(status='auxiliary_fixed_vector_polynomial_candidate_pending_independent_review',nx=nx,ny=ny,N=nx*ny,g_center=str(g),
              ground_trial_dimension=len(G),retained_ground_eigenstates=1,additional_retained_eigenstates=0,
              coefficients=list(map(int,c)),gram_norm=str(norm),gram_common_factor_removed=gr['gram_common_factor_removed'],
              energy_shift=gr['E00'],shifted_rayleigh_coefficients=list(map(str,R)),
              shifted_second_moment_coefficients=list(map(str,Q)),full_residual_squared_coefficients=list(map(str,V)),
              coefficient_order='ascending powers of g; Rayleigh degree1, second moment and full residual squared degree2',
              center_check=dict(external_cutoff=str(a),pencil_lower=str(l),rayleigh=str(rho),residual_squared=str(variance),
                exact_endpoint_form_per_norm=str(endpoint_form),Temple_lower=str(temple),
                older_Rayleigh_upper=old['ground_upper']),
              source_sha256={str(source.relative_to(RES)):digest(source),str(gp.relative_to(RES)):digest(gp)},
              scope='For interval use, fix this coefficient vector. Re-establish a uniform one-low-even-state cutoff, rho(g)<a, and the scalar Temple inequality throughout the interval. Different auxiliary vectors all bound the same unique ground; do not sum or count them as separate eigenstates.')
            path=HERE/f'auxiliary_{nx}x{ny}_g{g}.json'.replace('/','d');path.write_text(json.dumps(row,indent=2));summary.append(row)
            sources[str(gp.relative_to(RES))]=digest(gp);sources[str(source.relative_to(RES))]=digest(source)
        (HERE/f'matrix_polynomial_{nx}x{ny}.json').write_text(json.dumps(polynomial,indent=2))
    (HERE/'summary.json').write_text(json.dumps(dict(status='all_21_polynomial_exports_exactly_checked',new_physical_states=0,new_moments=0,
      source_sha256=sources,rows=summary),indent=2))
    print('PASS 21 fixed witness exports; all matrix polynomial identities and center Temple inequalities exact')

if __name__=='__main__':main()
