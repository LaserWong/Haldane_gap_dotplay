"""Refined large-seed candidates. Old certificates remain untouched.
Uses exact algebraic triplet moments, exact geometry-contracted ground moments,
sector-specific angle estimates, isoperimetric occupancy bounds, and bounded-
denominator outward exponentials. These new variants need independent review.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,time,hashlib,argparse
from translated_band import HERE,RESEARCH,Quad,moments,fourier_certificate
import translated_band as T
import number_sector_tail as NT
import low_band_certificate as L
import correlated_low_band as C
from build_large_certificates import bipartite_counts
sys.path.insert(0,str(RESEARCH/'low_band_review'))
from fast_exp import exp_interval
OUT=HERE/'refined';OUT.mkdir(exist_ok=True)

# Exact graph uppercounts. The new cut estimate is also checked against all
# already audited small-graph occupancy maxima before being used.
def iso_counts(nx,ny):
    assert nx>=2 and ny>=2
    n=nx*ny;upper=[]
    for q in range(n+1):
        h=min(q,n-q);v=math.isqrt(4*h);v+=int(v*v<4*h)
        cut=min(v,nx,ny) if h else 0
        upper.append(2*q-cut)
    if nx>=4 and ny>=4 and nx%2==ny%2==0:
        b=bipartite_counts(nx,ny);upper=[min(a,c) for a,c in zip(upper,b['occupied_edge_max'])]
    empty=[2*n-4*q+u for q,u in enumerate(upper)];assert min(empty)>=0
    return dict(N=n,degrees=[4]*n,occupied_edge_max=upper,empty_edge_max=empty,enumeration_size=0,
       counts_status='proved upper bounds, not exact occupancy maxima',
       proof='Edge boundary/2 >= min(ceil(2sqrt(min(q,N-q))), nx,ny), combined with bipartite uppercount where applicable.')

def check_counts():
    for nx,ny in [(2,2),(4,2),(4,4)]:
        original=json.loads((HERE.parent/f'number_bins_{nx}x{ny}_g3d100.json').read_text())['graph_counts']
        upper=iso_counts(nx,ny)['occupied_edge_max'];actual=original['occupied_edge_max']
        assert all(a<=b for a,b in zip(actual,upper))
    return dict(status='passed_exact_comparison_to_audited_small_graph_enumerations',shapes=[[2,2],[4,2],[4,4]])

def scalar_lower(theta,r2,b):
    v=(float(theta)+float(b)-math.sqrt((float(b)-float(theta))**2+4*float(r2)))/2
    lo=L.lower_round(v,digits=12)
    while (b-lo)*(theta-lo)<r2:lo-=F(1,10**10)
    return lo

def build(nx,ny,g):
    tag=f'translated_{nx}x{ny}_g{g}'.replace('/','d');p=HERE/f'{tag}_fourier.json'
    fourier=json.loads(p.read_text()) if p.exists() else fourier_certificate(moments(nx,ny,g))
    ground_path=RESEARCH/'large_seed_moments'/f'block1_{nx}x{ny}_g{g}.json'.replace('/','d')
    gr=json.loads(ground_path.read_text());rho=F(gr['exact_rayleigh'])-F(gr['E00']);r2=F(gr['exact_residual_squared'])
    c=list(map(int,gr['coefficients']));gd=int(gr['integer_matrix_denominator'])
    def bilinear(key):
        matrix=gr[key]
        return sum(c[i]*int(matrix[i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
    gn=bilinear('gram');ga=bilinear('shifted_hamiltonian_numerator');gb=bilinear('shifted_H2_numerator')
    assert F(ga,gd*gn)==rho and F(gb,gd*gd*gn)-rho*rho==r2
    number=NT.certify_bins(nx,ny,g);a0,a1,a2=[F(row['lower']) for row in number['bins'][:3]]
    assert rho<a1
    assert F(fourier['ritz_max_upper'])<a2
    ground_angle=r2/(a2-rho)**2;assert ground_angle<1
    bground=a2-(a2-a0)*ground_angle
    angles=[];bsectors=[]
    for mode in fourier['modes']:
        # theta_upper and residual_squared_upper are exact rational enclosures
        # of the algebraic symbols, so this rational ratio is directed safely.
        th=F(mode['theta_upper']);rr=F(mode['residual_squared_upper'])
        angle=rr/(a2-th)**2;assert angle<1
        angles.append(angle);bsectors.append(a2-(a2-a1)*angle)
    b=min([bground]+bsectors);assert b>F(fourier['ritz_max_upper'])
    gl=scalar_lower(rho,r2,b);lower=[];upper=[];margins=[]
    for mode in fourier['modes']:
        th=Quad(*map(F,mode['theta']));rr=Quad(*map(F,mode['residual_squared']))
        v=(float(th)+float(b)-math.sqrt((float(b)-float(th))**2+4*float(rr)))/2
        lo=L.lower_round(v,digits=12)
        while ((b-lo)*(th-lo)-rr).sign()<0:lo-=F(1,10**10)
        lower.append(str(lo));upper.append(mode['theta_upper']);margins.append(((b-lo)*(th-lo)-rr).json())
    n=nx*ny
    blocks=[dict(k=1,multiplicity=1,eigen_lower=[str(gl)],eigen_upper=[str(rho)],trial_dimension=gr['trial_subspace_dimension']),
       dict(k=n,multiplicity=3,eigen_lower=lower,eigen_upper=upper,schur_Qsqrt2_margins=margins)]
    rec=dict(status='sector_refined_translation_band_candidate_pending_independent_review',nx=nx,ny=ny,N=n,g=str(g),
       energy_shift=str(-F(3*n,4)),full_hilbert_dimension=4**n,retained_full_band_dimension=1+3*n,
       relative_form_bound=gr['relative_form_bound'],number_sector_bins=number,blocks=blocks,
       global_lambda_kplus1_lower=str(a2),global_ground_lower=str(a0),all_excited_global_lower=str(a1),
       orthogonal_complement_lower=str(b),ground_complement_lower=str(bground),
       triplet_sector_complement_lowers=list(map(str,bsectors)),triplet_angle_squared_upper=list(map(str,angles)),
       ground_source=str(ground_path.relative_to(RESEARCH)),ground_source_sha256=hashlib.sha256(ground_path.read_bytes()).hexdigest(),
       fourier_source=f'{tag}_fourier.json',fourier_source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),ground_width=str(rho-gl))
    (OUT/f'{tag}_block1_low_band.json').write_text(json.dumps(rec,indent=2))
    print('REFINED PATCH',nx,ny,g,'a2',float(a2),'b',float(b),'groundwidth',float(rho-gl),flush=True)
    return rec

def fast_trace(rec,beta):
    beta=F(beta);assert beta>=0;shift=F(rec['blocks'][0]['eigen_upper'][0]);lo=hi=F(0)
    for block in rec['blocks']:
        for l,u in zip(block['eigen_lower'],block['eigen_upper']):
            lo+=block['multiplicity']*exp_interval(-beta*(F(u)-shift))[0]
            hi+=block['multiplicity']*exp_interval(-beta*(F(l)-shift))[1]
    tail=sum(row['multiplicity']*exp_interval(-beta*(F(row['lower'])-shift))[1] for row in rec['number_sector_bins']['bins'][2:])
    return lo,hi+tail,tail

def exact_seed(recs,beta):
    beta=F(beta);q0=fast_trace(recs[0],beta);q1=fast_trace(recs[1],beta);q2=fast_trace(recs[2],beta);q3=fast_trace(recs[2],2*beta)
    e=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
    J1=L.down(exp_interval(-2*beta*e[2]+8*beta*e[0])[0]*q3[0]/q0[1]**8,digits=16)
    J2=L.down(exp_interval(-4*beta*e[2]+8*beta*e[1])[0]*q3[0]**2/q1[1]**8,digits=16)
    c=L.down(q3[0]/q2[1]**2,digits=16)
    assert 0<J1<=1 and 0<J2<=1 and 0<c<=1
    A=L.down(C.G(J1),digits=16);B=L.down(C.G(J2*A),digits=16);CC=L.down(C.G(c**4*A*A*B),digits=16)
    row=dict(beta_initial=str(beta),order='xyt',J1=str(J1),J2=str(J2),C=str(c),first_purities=list(map(str,[A,B,CC])),
       exact_exponential_method='256-bit directed dyadic range-reduced Taylor from independently reviewed fast_exp.py',accepted=False)
    if min(A,B,CC)<=0:return row
    boot=L.replay(A,B,CC,n=2*recs[0]['nx'],m=2*recs[0]['ny'],beta=2*beta,rounds=64,digits=18)
    row.update(bootstrap=boot,accepted=boot['status']=='accepted_analytic_scalar_certificate')
    return row

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--couplings',default='3/100,1/25,1/20');a=p.parse_args()
    (OUT/'count_crosscheck.json').write_text(json.dumps(check_counts(),indent=2))
    NT.OUT=OUT;NT.occupation_counts=iso_counts
    summary=[]
    for g in map(F,a.couplings.split(',')):
        recs=[build(nx,ny,g) for nx,ny in [(4,4),(8,4),(8,8)]]
        grid=sorted((C.float_score(recs,b/20,'xyt'),F(b,20)) for b in range(100,601));ok=[row for row in grid if row[0]<0]
        result=dict(g=str(g),status='larger_seed_candidate_pending_independent_review',accepted_float=len(ok),grid_scope='beta5..30 step.05')
        if ok:
            _,beta=ok[0];result['exact']=exact_seed(recs,beta)
            print('EXACT LARGE SEED',g,beta,result['exact'].get('bootstrap'),flush=True)
        (OUT/f'large_seed_g{g}.json'.replace('/','d')).write_text(json.dumps(result,indent=2));summary.append(result)
    (OUT/'large_seed_summary.json').write_text(json.dumps(summary,indent=2))
