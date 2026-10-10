"""Order-one interacting bilayer with exact product singlet ground candidate.
H_shifted=Q+g sum_<ij> T_i.T_j, T_i=Sa_i+Sb_i, Q=sum triplet_projector.
All four positive cross-rung Heisenberg bonds are included for every base edge.
The excited-state interactions do NOT commute with each other; every rung Q_i
is nevertheless conserved. This enables tiny block references, not a small
excited Hilbert space in the thermodynamic limit.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,math,itertools
import numpy as np
import scipy.linalg as la
from models import *
OUT=Path(__file__).resolve().parent/'results'

def frustrated_bilayer(nx,ny,g):
    base=square(.5,nx,ny,periodic_x=True,periodic_y=True);N=nx*ny
    edges=[Edge(2*i,2*i+1,1.,'rung') for i in range(N)]
    edges += [Edge(2*e.i+a,2*e.j+b,float(g),'interrung_'+e.kind) for e in base.edges for a in [0,1] for b in [0,1]]
    return Model(.5,2*N,tuple(edges),f'fully_frustrated_{nx}x{ny}_g{g}',dict(family='fully_frustrated_bilayer',nx=nx,ny=ny,g=str(g),periodic_both=True,shift_to_Q=3*N/4)).validate()

def occupancy_spectrum(nx,ny,g):
    """Exact decomposition by conserved spin0/spin1 rung occupations.
    Full spectrum only on <=8 rungs, max dense Sz block=1107.
    """
    N=nx*ny;assert N<=8;g=float(g);base=square(1.,nx,ny,periodic_x=True,periodic_y=True)
    all_e=[];sector_records=[];cache={};t=time.monotonic()
    for mask in range(1<<N):
        active=[i for i in range(N) if (mask>>i)&1];Q=len(active)
        if not Q:e=np.array([0.])
        else:
            where={old:new for new,old in enumerate(active)}
            pairs=tuple(sorted((min(where[e.i],where[e.j]),max(where[e.i],where[e.j])) for e in base.edges if e.i in where and e.j in where))
            key=(Q,pairs)
            if key not in cache:
                if not pairs:cache[key]=np.zeros(3**Q)
                else:
                    model=Model(1.,Q,tuple(Edge(i,j,g,'occupied') for i,j in pairs),'triplet_sector',{})
                    cache[key]=full_spectrum(model)[0]
            e=cache[key]+Q
        all_e.append(e);sector_records.append(dict(mask=mask,triplets=Q,dimension=len(e),min_energy=float(e[0])))
    e=np.sort(np.concatenate(all_e));assert len(e)==4**N
    return e,sector_records,time.monotonic()-t,len(cache)

def singlet_vector(N):
    # Each rung (|down,up>-|up,down>)/sqrt2, relative sign immaterial.
    p=np.array([0.,1.,-1.,0.]);v=np.array([1.])
    for _ in range(N):v=np.kron(p,v)
    return v/np.linalg.norm(v)

def run():
    rows=[]
    for g in [F(3,10),F(8,25),F(1,3),F(7,20)]:
        m=frustrated_bilayer(2,2,g);e,sec,elapsed,blocks=occupancy_spectrum(2,2,g)
        reference,_=full_spectrum(m);reference+=3.
        np.testing.assert_allclose(e,reference,atol=2e-12)
        H=independent_dense(m)+3*np.eye(256);v=singlet_vector(4)
        assert np.linalg.norm(H@v)<1e-13
        ground=float(e[0]);deg=int(sum(abs(e-ground)<1e-9));gap=float(e[np.searchsorted(e,ground+1e-8)]-ground)
        # Rung-swap singlet product is exact; its energy is identically zero.
        formula=min(1.,2-4*float(g),3-6*float(g),4-12*float(g))
        if g<F(1,3):assert abs(gap-formula)<2e-12 and deg==1
        row=dict(nx=2,ny=2,g=str(g),physical_spins=8,full_dimension=256,ground_energy_shifted=ground,ground_degeneracy=deg,gap=gap,product_ground_residual=float(np.linalg.norm(H@v)),all_occupation_spectrum_matches_physical_ED=True,predicted_product_gap_min=formula,seconds=elapsed)
        rows.append(row);print(row,flush=True)
    for g in [F(3,10)]:
        e,sec,elapsed,blocks=occupancy_spectrum(4,2,g)
        np.savez_compressed(OUT/'fully_frustrated_4x2_g3d10_full_occupation_spectrum.npz',energies=e)
        gap=float(e[1]-e[0]);row=dict(nx=4,ny=2,g=str(g),physical_spins=16,full_dimension=len(e),ground_energy_shifted=float(e[0]),ground_degeneracy=int(sum(abs(e-e[0])<1e-9)),gap=gap,method='Conserved rung occupations and total Sz; max dense block 1107',distinct_occupation_graphs=blocks,seconds=elapsed,triplet_sector_minima=sec)
        rows.append(row);print({k:v for k,v in row.items() if k!='triplet_sector_minima'},flush=True)
    # Independent local angular-momentum bounds as tiny dense diagnostics.
    for weights,bound in [([1,1,1,1],5),([2,1,1],6),([2,2],6)]:
        m=Model(1.,len(weights)+1,tuple(Edge(0,j+1,float(w),'star') for j,w in enumerate(weights)),'star',{})
        e,_=full_spectrum(m);assert e[0]>=-bound-1e-12
        rows.append(dict(kind='spin1_star',weights=weights,dimension=m.dimension,minimum=float(e[0]),analytic_lower=-bound))
    # One plaquette: K+3/2 sum n_i >=0 for every occupied-rung sector.
    base=square(1.,2,2,periodic_x=False,periodic_y=False)
    min_psd=0.
    for mask in range(16):
        active=[i for i in range(4) if mask>>i&1];Q=len(active)
        if not Q:continue
        where={x:i for i,x in enumerate(active)}
        edges=tuple(Edge(where[e.i],where[e.j],1.,'plaquette') for e in base.edges if e.i in where and e.j in where)
        e,_=full_spectrum(Model(1.,Q,edges,'plaquette',{}));min_psd=min(min_psd,float(e[0]+1.5*Q))
    assert min_psd>-1e-12
    rows.append(dict(kind='occupied_plaquette_PSD',all_16_occupations_checked=True,minimum_shifted=float(min_psd),analytic_inequality='K_plaquette >= -(3/2) sum_i n_i'))
    (OUT/'fully_frustrated_checks.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':run()
