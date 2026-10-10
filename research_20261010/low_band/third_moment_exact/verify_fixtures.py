"""Producer crosschecks: full/fixed-origin/physical and exact H'^3 fixtures."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys,json,time
from fractions import Fraction as F
from pathlib import Path
sys.dont_write_bytecode=True
from exact_filter import HERE,RES,third_moment
sys.path.insert(0,str(RES/'large_seed_moments'))
from large_seed_moments import matrices
start=time.monotonic();results=[]
translation_checks=[]
for nx,ny in ((2,2),(4,2),(4,4),(8,4),(8,8)):
    data=list(map(int,(RES/'large_seed_moments'/f'geometry_{nx}x{ny}.txt').read_text().split()))
    N,n,E=data[:3];assert N==nx*ny
    at=3;edges={}
    for _ in range(E):
        i,j,w=data[at:at+3];at+=3;edges[tuple(sorted((i,j)))]=w
    ids={}
    for i in range(N):
        for j in range(i+1,N):ids[i,j]=data[at];at+=1
    assert at==len(data)
    for site in range(N):assert sum(w for pair,w in edges.items() if site in pair)==4
    for dx,dy in ((1,0),(0,1)):
        perm=[((i//ny+dx)%nx)*ny+(i%ny+dy)%ny for i in range(N)]
        for i in range(N):
            for j in range(i+1,N):
                other=tuple(sorted((perm[i],perm[j])))
                assert edges.get((i,j),0)==edges.get(other,0)
                assert ids[i,j]==ids[other]
    translation_checks.append(dict(geometry=f'{nx}x{ny}',both_generating_translations_preserve_all_edges_and_orbit_ids=True,weighted_degree=4))
for nx,ny in ((2,2),(4,2),(4,4)):
    tag=f'{nx}x{ny}'
    origin=json.loads((HERE/f'geometry_{tag}_origin.json').read_text())
    full=json.loads((HERE/f'geometry_{tag}_full.json').read_text())
    physical=json.loads((HERE/f'physical_{tag}.json').read_text())
    old=json.loads((RES/'large_seed_moments'/f'geometry_{tag}.json').read_text())
    for key in ('F','S','V','W','X','Y','Z'):
        assert origin[key]==full[key]==physical[key],(tag,key)
    for key in ('F','S','V','W'):assert origin[key]==old[key],(tag,key)
    for key in ('X','Z'):assert origin[key]==list(map(list,zip(*origin[key])))
    model,G,K,J,_=matrices(nx,ny,F(9,100),old)
    n=old['pair_orbits'];v=[7]+[(-1)**i*(i+1) for i in range(n)]+[-(-1)**i*(i+2) for i in range(n)]
    record=dict(coefficients=v,selected_basis_indices=list(range(len(v))),gram=G.tolist(),shifted_hamiltonian_numerator=K.tolist(),shifted_H2_numerator=J.tolist(),integer_matrix_denominator=model.den,coupling='9/100')
    m=third_moment(record,origin);p=physical['fixture'];assert m['norm']==p['norm']
    for k in (1,2,3):assert m[f'm{k}']==F(p[f'H{k}_numerator'],p['integer_H_denominator']**k*p['norm']),(tag,k)
    results.append(dict(geometry=tag,all_F_S_V_W_X_Y_Z_entries_exact=True,fixed_origin_equals_full=True,baseline_F_S_V_W_exact=True,physical_H1_H2_H3_exact=True,physical_support={k:physical[k] for k in ('support_B','support_L','support_R','support_M')},third_moment=str(m['m3']),physical_seconds=physical['total_seconds'],physical_peak_rss_kib=physical['peak_rss_kib']))
    print(tag,'PASS: every geometric entry and explicit sparse H1/H2/H3 fixture',flush=True)
(HERE/'fixture_tests.json').write_text(json.dumps(dict(status='producer_checks_pass_independent_review_pending',tests=results,translation_checks=translation_checks,total_python_seconds=time.monotonic()-start),indent=2)+'\n')
