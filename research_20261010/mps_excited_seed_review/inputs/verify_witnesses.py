#!/usr/bin/env python3
"""Exact integrity checks and extraction of three orthogonal witnesses."""
import os,resource,json,time,hashlib
from pathlib import Path
from fractions import Fraction as F
os.sched_setaffinity(0,{max(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
P=Path(__file__).resolve().parent;ROOT=P.parents[1];t0=time.process_time()
def parse(path): return {k:int(v) for k,v in (line.strip().split('=') for line in path.read_text().splitlines())}
p=parse(P/'contractions_n24.out');g=parse(P/'ground_lengths.out');bench=parse(P/'benchmark_n16.out')
for key,value in bench.items(): assert p[key]==value
for key,value in p.items():
    if key.startswith(('N0_','H0_')) and key in g: assert value==g[key]
checks=json.loads((P/'source_checks.json').read_text())
for row in checks['direct_fixtures']:
    n=row['n']
    for i in [0,1]:
        assert p[f'N{i}_{n}']==int(row['states'][i]['norm'])
        assert p[f'H{i}_{n}']==int(row['states'][i]['energy_numerator'])
old=parse(ROOT/'research_20261010/uniform_seed_size_diagnostics/mps_lengths.out')
for n in [12,16,20,24]:
    assert g[f'N0_{n}']==old[f'V{n}']
    assert g[f'H0_{n}']==n*old[f'U{n}']
# Recover and check the selection rule from the saved physical local tensors.
local=json.loads((P/'local_tensors.json').read_text());labels=local['labels'];A=local['A']
assert len(labels)==26 and len(A)==3
for s,matrix in zip([-1,0,1],A):
    for i,row in enumerate(matrix):
        for j,value in enumerate(row):
            assert not value or labels[j][1]-labels[i][1]==2*s
rows=[]
for n in [14,16,20,24]:
    norm0,norm1=p[f'N0_{n}'],p[f'N1_{n}'];assert norm0>0 and norm1>0
    alpha0=F(p[f'H0_{n}'],norm0);alpha1=F(p[f'H1_{n}'],norm1)
    R=F(g[f'H0_{2*n}'],g[f'N0_{2*n}']);delta=R-2*alpha0;gap=alpha1-alpha0
    assert delta>0 and gap>0
    rows.append({'n':n,'numerator_length':2*n,'full_Hilbert_dimension_denominator':3**n,'full_Hilbert_dimension_numerator':3**(2*n),'retained_denominator_span_dimension':3,'retained_numerator_span_dimension':1,'denominator_MPS_bond_dimensions':[26,52,52],'linear_variational_search':'none; three fixed analytically specified vectors','largest_auxiliary_charge_block_side':162,'norm_psi':str(norm0),'H_numerator_psi':str(p[f'H0_{n}']),'norm_phi_plus_and_minus':str(norm1),'H_numerator_phi_plus_and_minus':str(p[f'H1_{n}']),'alpha0':str(alpha0),'alpha1':str(alpha1),'alpha0_display':float(alpha0),'alpha1_display':float(alpha1),'R_2n':str(R),'R_2n_display':float(R),'delta':str(delta),'delta_display':float(delta),'trial_energy_difference':str(gap),'trial_energy_difference_display':float(gap),'orthogonality':'Exact disjoint total-Sz sectors 0,+1,-1; all norms strictly positive. Spin-flipped raised state has equal norm and Rayleigh by F H F=H, without assuming F psi=psi or any exact total-spin label.'})
out={'status':'PASS producer exact witnesses; independent review pending','rows':rows,'direct_fixture_sizes':[2,4,6],'ground_cross_checks':'All available outputs agree with independent ordinary transfer contractions and archived n12,16,20,24 integers.','physical_support_expansion':'Only direct fixtures n=2,4,6. No new larger physical amplitude vectors, supports, Hamiltonian matrices, or eigensolvers.','cpu_seconds':time.process_time()-t0,'peak_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(P/'exact_witness_data.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows: print(r['n'],r['alpha0_display'],r['alpha1_display'],'delta',r['delta_display'])
