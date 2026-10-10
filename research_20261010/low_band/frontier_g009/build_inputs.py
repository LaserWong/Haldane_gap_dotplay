"""New point from audited geometry and exact polynomial translated moments.
No full H action, leaked support construction, or higher moments are performed.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib,resource,importlib.util
import numpy as np
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RES=BAND.parent
for p in (BAND/'translation_band',BAND/'quadratic_boson',RES/'large_seed_moments',BAND/'tail_comparison',BAND/'ground_moment_pencil',RES/'variational_numerator_filter'):
    sys.path.insert(0,str(p))
import translated_band as T
import quadratic_bins as Q
import large_seed_moments as GS
import integrate_tails as I
import filter_rayleigh as VR
spec=importlib.util.spec_from_file_location('ground_pencil_library',BAND/'ground_moment_pencil'/'certify.py')
GP=importlib.util.module_from_spec(spec);spec.loader.exec_module(GP)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def source_path(nx,ny,g):
    if g<F(3,50):parent=BAND/'translation_band'
    elif g==F(3,50):parent=BAND/'frontier_g006'
    else:parent=BAND/'frontier_g007_g010'/f'g{g}'.replace('/','d')
    return parent/f'translated_{nx}x{ny}_g{g}_moments.json'.replace('/','d')


def poly_value(xs,ys,z):
    out=F(0)
    for i,y in enumerate(ys):
        term=y
        for j,x in enumerate(xs):
            if j!=i:term*=F(z-x,xs[i]-x)
        out+=term
    return out


def polynomial_moments(nx,ny,g):
    couplings=list(map(F,('3/100','1/25','1/20','3/50','7/100','2/25','1/10')))
    paths=[source_path(nx,ny,x) for x in couplings]
    records=[json.loads(p.read_text()) for p in paths]
    d=4*g.denominator;arrays={};checks=0
    for key,power,degree in (('G',2,2),('A',3,3),('B',4,4)):
        arr=[]
        for i in range(nx):
            row=[]
            for j in range(ny):
                # Integer stored columns W=2d*w and T=d*H' imply the factors.
                ys=[F(int(r[key][i][j]),4*r['matrix_denominator']**power) for r in records]
                xs=couplings[:degree+1];base=ys[:degree+1]
                for x,y in zip(couplings[degree+1:],ys[degree+1:]):
                    assert poly_value(xs,base,x)==y;checks+=1
                value=poly_value(xs,base,g)*4*d**power
                assert value.denominator==1
                row.append(str(value.numerator))
            arr.append(row)
        arrays[key]=arr
    rec=dict(status='exact_polynomial_moment_evaluation_pending_independent_review',nx=nx,ny=ny,N=nx*ny,g=str(g),
        matrix_denominator=d,column_rule=records[0]['column_rule'],
        polynomial_definition='w_r(g)=(I-C_create(g)/2)|t+_r>; Hprime(g)=Q+gV. w and Hprime are affine in g, giving G/A/B degrees <=2/3/4 before the explicit 4*d^(2/3/4) normalization.',
        source_sha256={str(p.relative_to(RES)):sha(p) for p in paths},
        extra_point_exact_checks=checks,polynomial_degrees={'G':2,'A':3,'B':4},
        no_physical_support_expansion=True,**arrays)
    path=HERE/f'translated_{nx}x{ny}_g{g}_moments.json'.replace('/','d')
    path.write_text(json.dumps(rec,indent=2)+'\n')
    return rec


def main():
    resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
    if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    g=F(9,100);geoms={};summary=[]
    for nx,ny in ((4,4),(8,4),(8,8)):
        gp=RES/'large_seed_moments'/f'geometry_{nx}x{ny}.json';geoms[nx,ny]=json.loads(gp.read_text())
    GS.geometry=lambda nx,ny:geoms[nx,ny]
    GS.OUT=T.HERE=Q.HERE=HERE
    original_read=I.read
    def local_read(path,sources):return original_read(HERE/path.name,sources)
    I.read=local_read
    for nx,ny in ((4,4),(8,4),(8,8)):
        tag=f'{nx}x{ny}_g9d100';gr=GS.certify(nx,ny,g)
        mm=polynomial_moments(nx,ny,g);four=T.fourier_certificate(mm);bins=Q.certify(nx,ny,g)
        old=I.patch(nx,ny,g,'quadratic',HERE)
        a0,a1,a=map(lambda r:F(r['lower']),bins['bins'][:3])
        rho=F(gr['exact_rayleigh'])-F(gr['E00']);assert rho<a1 and F(four['ritz_max_upper'])<a
        for block,floor in zip(old['blocks'],(a0,a1)):
            block['eigen_lower']=[str(max(floor,F(x))) for x in block['eigen_lower']]
        G,K,J=[np.array(gr[k],dtype=object) for k in ('gram','shifted_hamiltonian_numerator','shifted_H2_numerator')]
        den=gr['integer_matrix_denominator'];pencil=GP.certify_pencil(G,K*F(1,den),J*F(1,den*den),a)
        lower=max(F(old['blocks'][0]['eigen_lower'][0]),F(pencil['endpoints'][0]['lower']))
        pp=HERE/f'ground_pencil_{tag}.json'
        pp.write_text(json.dumps(dict(status='new_g009_candidate_pending_independent_review',g=str(g),nx=nx,ny=ny,ground_lower=str(lower),pencil=pencil),indent=2)+'\n')
        gp=HERE/f'block1_{tag}.json';geometrypath=RES/'large_seed_moments'/f'geometry_{nx}x{ny}.json'
        filtered=VR.certificate(gr,gp,geoms[nx,ny],geometrypath)
        fp=HERE/f'filtered_{tag}.json';fp.write_text(json.dumps(filtered,indent=2)+'\n')
        upper=F(filtered['shifted_rayleigh_upper']);assert lower<=upper<=rho
        old['blocks'][0]['unfiltered_eigen_upper']=old['blocks'][0]['eigen_upper'][:]
        old['blocks'][0]['eigen_lower']=[str(lower)];old['blocks'][0]['eigen_upper']=[str(upper)]
        old['ground_width']=str(upper-lower);old['new_trial_residual_claim']=False
        old['status']='new_g009_combined_ground_candidate_pending_independent_review'
        old['extra_source_sha256']={str(p.relative_to(RES)):sha(p) for p in (pp,fp)}
        (HERE/f'combined_patch_{tag}.json').write_text(json.dumps(old,indent=2)+'\n')
        row=dict(nx=nx,ny=ny,g=str(g),ground_lower=str(lower),filtered_ground_upper=str(upper),
            omitted_cutoff=str(a),ritz_max_upper=four['ritz_max_upper'],cutoff_margin=str(a-F(four['ritz_max_upper'])),
            filtered_gain=filtered['filter']['improvement'],polynomial_extra_point_checks=mm['extra_point_exact_checks'])
        summary.append(row);print('READY',nx,ny,'width',float(upper-lower),'margin',float(a-F(four['ritz_max_upper'])),flush=True)
    I.read=original_read
    (HERE/'input_summary.json').write_text(json.dumps(summary,indent=2)+'\n')


if __name__=='__main__':main()
