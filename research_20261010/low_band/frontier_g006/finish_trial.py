"""Exact counted sector-Temple patches and bounded scalar scan at g=.06."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,copy,math
HERE=Path(__file__).resolve().parent;BAND=HERE.parent
sys.path.insert(0,str(BAND/'translation_band'))
from translated_band import Quad
import large_refined_pipeline as P
import correlated_low_band as C
import low_band_certificate as L


def build(nx,ny):
    paths=[HERE/f'block1_{nx}x{ny}_g3d50.json',HERE/f'translated_{nx}x{ny}_g3d50_fourier.json',HERE/f'number_bins_{nx}x{ny}_g3d50.json']
    gr,four,number=[json.loads(p.read_text()) for p in paths]
    rho=F(gr['exact_rayleigh'])-F(gr['E00']);r2=F(gr['exact_residual_squared'])
    a0,a1,a=[F(x['lower']) for x in number['bins'][:3]]
    assert rho<a1 and F(four['ritz_max_upper'])<a
    c=list(map(int,gr['coefficients']));den=gr['integer_matrix_denominator']
    def quadratic(key):return sum(c[i]*int(gr[key][i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
    gn,ga,gb=[quadratic(k) for k in ('gram','shifted_hamiltonian_numerator','shifted_H2_numerator')]
    assert F(ga,den*gn)==rho and F(gb,den*den*gn)-rho*rho==r2
    ground_lower=rho-r2/(a-rho);lower=[];upper=[];endpoints=[]
    for mode in four['modes']:
        th=Quad(*map(F,mode['theta']));rr=Quad(*map(F,mode['residual_squared']))
        assert (a-th).sign()>0 and rr.sign()>=0
        endpoint=th-rr/(a-th);lo=L.down(endpoint.bounds(128)[0],digits=14)
        assert ((a-th)*(th-lo)-rr).sign()>=0
        lower.append(str(lo));upper.append(mode['theta_upper']);endpoints.append(endpoint.json())
    rec=dict(status='exact_first_order_g006_candidate_pending_independent_review',nx=nx,ny=ny,N=nx*ny,g='3/50',
        energy_shift=gr['E00'],full_hilbert_dimension=4**(nx*ny),retained_full_band_dimension=1+3*nx*ny,
        relative_form_bound=gr['relative_form_bound'],number_sector_bins=number,
        global_lambda_kplus1_lower=str(a),all_excited_global_lower=str(a1),global_ground_lower=str(a0),
        ground_width=str(rho-ground_lower),
        source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        blocks=[dict(k=1,multiplicity=1,eigen_lower=[str(ground_lower)],eigen_upper=[str(rho)]),
                dict(k=nx*ny,multiplicity=3,eigen_lower=lower,eigen_upper=upper,exact_Qsqrt2_Temple_endpoints=endpoints)])
    (HERE/f'temple_{nx}x{ny}_g3d50.json').write_text(json.dumps(rec,indent=2))
    return rec


def main():
    recs=[build(x,y) for x,y in [(4,4),(8,4),(8,8)]]
    variants={'full':recs}
    for name in ('no_number_tail','exact_triplet_intervals','exact_ground_interval','exact_all_intervals'):
        rr=copy.deepcopy(recs)
        for rec in rr:
            if name=='no_number_tail':rec['number_sector_bins']['bins']=rec['number_sector_bins']['bins'][:2]
            if name in ('exact_triplet_intervals','exact_all_intervals'):rec['blocks'][1]['eigen_lower']=rec['blocks'][1]['eigen_upper']
            if name in ('exact_ground_interval','exact_all_intervals'):rec['blocks'][0]['eigen_lower']=rec['blocks'][0]['eigen_upper']
        variants[name]=rr
    summary={}
    for name,rr in variants.items():
        rows=[]
        for order in ('xyt','xty','txy'):
            grid=sorted((C.float_score(rr,b/20,order),F(b,20)) for b in range(100,601))
            score,beta=grid[0]
            rows.append(dict(order=order,best_beta=str(beta),score=score,accepted_proposals=sum(s<0 for s,_ in grid),
                             best_first_purities=C.float_initial(rr,float(beta),order)))
        summary[name]=rows
    canonical=summary['full'][0]
    # If every full first cycle fails, select the least bad thermal step among
    # grid points with both preceding spatial steps positive. Do not select the
    # first tied sentinel returned by the floating bootstrap score.
    thermal_proposals=[]
    e=[float(F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0])) for r in recs]
    for bi in range(100,601):
        beta=bi/20;q0=C.traces_float(recs[0],beta);q1=C.traces_float(recs[1],beta)
        q2=C.traces_float(recs[2],beta);q3=C.traces_float(recs[2],2*beta)
        j1=math.exp(-2*beta*e[2]+8*beta*e[0])*q3[0]/q0[1]**8
        j2=math.exp(-4*beta*e[2]+8*beta*e[1])*q3[0]**2/q1[1]**8
        cc=q3[0]/q2[1]**2;aa=C.G(j1)
        if aa<=0:continue
        bb=C.G(j2*aa)
        if bb<=0:continue
        thermal_proposals.append((C.G(cc**4*aa*aa*bb),F(bi,20),aa,bb))
    best_thermal=max(thermal_proposals) if thermal_proposals else None
    beta=best_thermal[1] if canonical['accepted_proposals']==0 and best_thermal else F(canonical['best_beta'])
    exact=P.exact_seed(recs,beta)
    result=dict(status='bounded_first_order_frontier_trial',g='3/50',
                grid_scope='beta5..30 step.05, three axis placements; not an all-beta exclusion',
                diagnostic_ablations_are_not_certificates=True,float_diagnostics=summary,
                best_failed_thermal_step=None if best_thermal is None else dict(beta=str(best_thermal[1]),A=best_thermal[2],B=best_thermal[3],C=best_thermal[0]),
                exact_canonical_proposal=exact)
    (HERE/'first_order_frontier_result.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
