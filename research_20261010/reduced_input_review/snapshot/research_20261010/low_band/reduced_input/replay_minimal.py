"""Strict reduced-input txy consumer: largest seed enters only through first moments.

ground_only never reads the optional largest triplet file. Neither mode reads a
largest squared-Hamiltonian moment, residual, cutoff, or full-band certificate.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,argparse
HERE=Path(__file__).resolve().parent;BAND=HERE.parent;RESEARCH=BAND.parent
sys.path.insert(0,str(BAND/'translation_band'));sys.path.insert(0,str(BAND/'frontier_g006'))
sys.path.insert(0,str(RESEARCH/'root_review'))
from translated_band import Quad,symbol
import large_refined_pipeline as P
import low_band_certificate as L
import correlated_low_band as C
from transport_orders import transport,sqrt_lower
from finite_window_2d import interpolate_2d,gap


def read(path,reads):
    reads[str(path.relative_to(RESEARCH))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())


def largest_first_moments(g,mode,reads):
    tag=f'g{g}'.replace('/','d');ground=read(HERE/f'largest_ground_{tag}.json',reads)
    allowed={'nx','ny','N_dimers','s','coupling','E00','gram_common_factor_removed','gram',
       'shifted_hamiltonian_numerator','integer_matrix_denominator','coefficients','trial_subspace_dimension',
       'basis','selected_basis_indices','artifact_role','historical_source','historical_source_sha256'}
    assert set(ground)<=allowed
    coeff=list(map(int,ground['coefficients']));den=ground['integer_matrix_denominator']
    def quadratic(key):return sum(coeff[i]*int(ground[key][i][j])*coeff[j] for i in range(len(coeff)) for j in range(len(coeff)))
    norm=quadratic('gram');mean=F(quadratic('shifted_hamiltonian_numerator'),den*norm);assert norm>0
    energy=F(ground['E00'])+mean;levels=[(1,energy)];theta_records=[]
    if mode=='trial193':
        rec=read(HERE/f'largest_triplet_GA_{tag}.json',reads)
        allowed={'nx','ny','N','g','matrix_denominator','column_rule','G','A','artifact_role','spin_multiplicity',
                 'historical_source','historical_source_sha256'}
        assert set(rec)<=allowed and rec['spin_multiplicity']==3
        nx,ny=rec['nx'],rec['ny'];d=rec['matrix_denominator']
        for kx in range(nx):
            for ky in range(ny):
                gram=symbol(rec['G'],nx,ny,kx,ky);first=symbol(rec['A'],nx,ny,kx,ky)
                assert gram.sign()>0;theta=first/(d*gram)
                upper=-L.down(-theta.bounds(100)[1],digits=12)
                assert (Quad(upper)-theta).sign()>=0
                levels.append((3,F(ground['E00'])+upper))
                theta_records.append(dict(momentum=[kx,ky],theta_exact=theta.json(),theta_upper=str(upper)))
    return energy,levels,dict(norm=str(norm),shifted_rayleigh=str(mean),energy_rayleigh=str(energy),
                             trial_trace_rank=sum(mult for mult,_ in levels),optional_triplet_first_moments=theta_records)


def run(g,beta,mode):
    g,beta=F(g),F(beta);assert 0<g<=F(3,50) and beta>0
    reads={};tag=f'g{g}'.replace('/','d')
    small=read(BAND/'tail_comparison'/'quadratic'/f'temple_4x4_{tag}.json',reads)
    middle=read(BAND/'tail_comparison'/'quadratic'/f'temple_8x4_{tag}.json',reads)
    emax,levels,first=largest_first_moments(g,mode,reads)
    # This is the ONLY largest trace input. Jensen/Peierls gives its lower bound.
    ell=sum(mult*P.exp_interval(-2*beta*(energy-emax))[0] for mult,energy in levels)
    u0=P.fast_trace(small,beta)[1];u1=P.fast_trace(small,2*beta)[1];u2=P.fast_trace(middle,2*beta)[1]
    es=F(small['energy_shift'])+F(small['blocks'][0]['eigen_upper'][0])
    em=F(middle['energy_shift'])+F(middle['blocks'][0]['eigen_upper'][0])
    j1=L.down(P.exp_interval(-2*beta*emax+8*beta*es)[0]*ell/u0**8,digits=16)
    j2=L.down(P.exp_interval(-4*beta*emax+16*beta*es)[0]*ell**2/u1**8,digits=16)
    c0=L.down(P.exp_interval(-2*beta*emax+4*beta*em)[0]*ell/u2**2,digits=16)
    a=L.down(C.G(j1),digits=16);b=L.down(C.G(j2*a),digits=16);c=L.down(C.G(c0**4*a*a*b),digits=16)
    assert all(0<x<=1 for x in (j1,j2,c0,a,b,c))
    abc=[L.down(x,digits=18) for x in transport(a,b,c,'txy',sqrt_lower)]
    boot=L.replay(*abc,n=8,m=8,beta=2*beta,rounds=64,digits=18)
    assert boot['status']=='accepted_analytic_scalar_certificate'
    states=[abc]+[[1-F(x) for x in row['defects']] for row in boot['updates']];windows=[]
    for j,state in enumerate(states):
        thermal,detail=interpolate_2d(*state);gg=gap(thermal,2*beta*2**j)
        windows.append(dict(n=8*2**j,through=16*2**j,thermal_lower=str(thermal),gap_lower=str(gg),details=detail))
    short=[]
    for side in range(2,8):
        bins=read(BAND/'frontier_g006'/'small_sizes'/f'number_bins_{side}x{side}_g3d50.json',reads)
        short.append(F(bins['bins'][1]['lower']))
    target=min([F(boot['uniform_square_gap_lower']),min(short)]+[F(w['gap_lower']) for w in windows if w['n']<boot['n']])
    return dict(status='reduced_largest_input_candidate_pending_independent_review',g=str(g),beta_initial=str(beta),
        largest_mode=mode,largest_first_moment_certificate=first,numeric_files_read_sha256=reads,
        largest_normalized_trace_lower=str(ell),J1=str(j1),J2=str(j2),C0=str(c0),
        permuted_first_purities=list(map(str,[a,b,c])),canonical_first_purities=list(map(str,abc)),
        bootstrap=boot,finite_windows=windows,small_L2_through_L7_common_gap=str(min(short)),
        all_integer_L_ge2_gap=str(target),all_integer_gap_display=float(target))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['ground_only','trial193','both'],default='both');args=ap.parse_args()
    modes=['ground_only','trial193'] if args.mode=='both' else [args.mode];rows=[]
    for g,beta in [('3/100','259/20'),('1/25','47/4'),('1/20','199/20'),('3/50','203/20')]:
        for mode in modes:
            row=run(g,beta,mode);rows.append(row)
            (HERE/f'{mode}_g{g}.json'.replace('/','d')).write_text(json.dumps(row,indent=2))
            print(g,mode,row['all_integer_gap_display'],flush=True)
    (HERE/f'summary_{args.mode}.json').write_text(json.dumps(rows,indent=2))


if __name__=='__main__':main()
