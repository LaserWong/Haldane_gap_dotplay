"""Exact independent scalar replay and finite-size bridges.
No frozen producer file is modified. The larger physical inputs are conditional
until their separate independent physical audit is complete.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import sys,resource
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
from functools import lru_cache
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent))
from finite_window_2d import interpolate_2d,gap


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def floor_grid(x,d):return F(x.numerator*d//x.denominator,d)
def ceil_grid(x,d):return -floor_grid(-x,d)
@lru_cache(None)
def independent_exp_upper(x):
    """Range-reduced positive Taylor series, 80 terms and 256-bit rounding."""
    x=F(x);assert x>=0
    k=0
    while x>F(1,8):x/=2;k+=1
    t=s=F(1)
    for j in range(1,81):t*=x/j;s+=t
    s=ceil_grid(s+(t*x/81)/(1-x/82),1<<256)
    for _ in range(k):s=ceil_grid(s*s,1<<256)
    return s


def positive_ldl(a):
    """No pivoting is needed for the positive definite local matrix."""
    a=[[F(x) for x in row] for row in a]
    pivots=[]
    while a:
        p=a[0][0];assert p>0;pivots.append(p)
        a=[[a[i][j]-a[i][0]*a[0][j]/p for j in range(1,len(a))] for i in range(1,len(a))]
    return pivots


def local_small_certificate():
    """Independently assemble four physical spins in an orthonormal basis."""
    def dot4(i,j):
        a=[[0]*16 for _ in range(16)]
        for col in range(16):
            bi=(col>>i)&1;bj=(col>>j)&1
            a[col][col]=(2*bi-1)*(2*bj-1)
            if bi!=bj:a[col^(1<<i)^(1<<j)][col]=2
        return a
    rung1,rung2=dot4(0,1),dot4(2,3)
    edge1,edge2=dot4(0,2),dot4(1,3)
    # M = V + (3/2)(Q_i+Q_j) + I/3, with Q=S.S+3I/4.
    # 24 M = 6(V4) + 9(rung1_4+rung2_4+6I) + 8I.
    m=[[6*(edge1[i][j]+edge2[i][j])+9*(rung1[i][j]+rung2[i][j])+(62 if i==j else 0)
        for j in range(16)] for i in range(16)]
    assert all(m[i][j]==m[j][i] for i in range(16) for j in range(16))
    pivots=positive_ldl(m)
    rows=[]
    for g in (F(3,100),F(1,25),F(1,20)):
        alpha=1-6*g;assert alpha>0
        for L in (2,3):
            N=L*L;B=2*N*g/3;bound=alpha-B;assert bound>0
            rows.append(dict(g=str(g),L=L,N=N,full_hilbert_dimension=4**N,
                             alpha=str(alpha),B=str(B),gap_lower=str(bound),gap_display=float(bound)))
    return dict(status='PASS exact physical-spin positive-definite local comparison and full-space minmax',
                local_matrix_denominator=24,local_matrix_numerator=m,exact_LDL_pivots=list(map(str,pivots)),
                a_over_g='3/2',b_over_g='1/3',inequality='V+(3/2)(Q_i+Q_j)+(1/3)I > 0',
                global_inequality='H-E00 >= (1-6g) Q_total - (2 N g/3) I',
                product_singlet_rayleigh_quotient='0',small_sizes=rows)


def validate_one(S,T,d):
    S,T=F(S),F(T);p=S*S*T;assert p>F(1,2) and p==F(d['p'])
    w=F(d['dominant_weight_lower']);assert F(1,2)<w<=1
    assert (2*w-1)**2<=2*p-1
    r=F(d['tail_ratio_upper']);assert r==(1-w)/w
    dd=F(d['d_lower']);assert dd==T/(1+r*r)
    c=F(d['purity_lower']);assert 0<c<=1
    scaled=c/(1-r);assert scaled<=dd and (scaled/S)**2<=dd
    return c


def window(A,B,C,n,beta):
    A,B,C,beta=map(F,(A,B,C,beta))
    thermal,det=interpolate_2d(A,B,C);assert thermal>F(1,2)
    sx=F(det['spatial_lower']);assert sx*sx<=A**4*(2*B-1)
    ty=validate_one(B,C,det['y']);assert ty==F(det['transverse_thermal_lower'])
    assert validate_one(sx,ty,det['x'])==thermal
    g=gap(thermal,beta);assert g>0
    exp=independent_exp_upper(beta*g);assert exp*(1-thermal)<thermal
    return dict(n=n,through=2*n,beta=str(beta),purities=list(map(str,(A,B,C))),
                thermal_lower=str(thermal),gap_lower=str(g),gap_display=float(g),
                independent_gap_exp_upper=str(exp),details=det)


def check_first_cycle(row):
    J1,J2,C=map(F,(row['J1'],row['J2'],row['C']))
    assert all(0<x<=1 for x in (J1,J2,C))
    def G(x):return 1-(1-x)**2/(2*x*x)
    A=floor_grid(G(J1),10**16)
    B=floor_grid(G(J2*A),10**16)
    CC=floor_grid(G(C**4*A*A*B),10**16)
    assert [A,B,CC]==list(map(F,row['first_purities']))
    return [A,B,CC]


def check_recurrence(row,dyadic=False):
    boot=row['bootstrap'];inp=boot['input'];seed=check_first_cycle(row)
    assert seed==[F(inp[k+'_lower']) for k in 'ABC']
    n,m,beta=inp['n'],inp['m'],F(inp['beta'])
    grid=1<<128 if dyadic else 10**18
    q=[ceil_grid(1-v,grid) for v in seed]
    states=[(n,beta,seed)];updates=[];levels=[]
    for j,step in enumerate(boot['updates']):
        if dyadic:
            bits=128*2**max(0,j-3);assert step['dyadic_bits']==bits;grid=1<<bits
        for axis in range(3):
            x=(1-q[0])**4*(1-q[1])**2*(1-q[2]);assert 0<x<=1
            new=ceil_grid((1-x)**2/(2*x*x),grid);assert 0<=new<1
            q=q[1:]+[new]
        assert step['round']==j+1 and q==list(map(F,step['defects']))
        n*=2;m*=2;beta*=2
        states.append((n,beta,[1-v for v in q]))
        updates.append(dict(round=j+1,all_three_exact_rounded_updates_equal=True,rounding_denominator=str(grid)))
    assert n==boot['n'] and m==boot['m'] and beta==F(boot['beta'])
    assert q==list(map(F,boot['defects'])) and len(updates)==boot['rounds']
    u=max(q);assert u==F(boot['u']) and 0<u<=F(1,500)
    proposed=F(boot['uniform_square_gap_lower']);exp=independent_exp_upper(beta*proposed)
    assert exp*32*u<1
    for level in row.get('continued_scalar_levels',[]):
        nr,br,st=states[level['round']];ur=max(1-v for v in st)
        assert nr==level['n'] and br==F(level['beta']) and ur==F(level['u']) and ur<=F(1,500)
        assert independent_exp_upper(br*F(level['gap']))*32*ur<1
        levels.append(dict(round=level['round'],gap_lower=level['gap'],exact_exponential_acceptance=True))
    return states,dict(first_cycle_equal=True,updates=updates,asymptotic_n=n,asymptotic_beta=str(beta),u=str(u),
                       gap_lower=str(proposed),gap_display=float(proposed),independent_gap_exp_upper=str(exp),continued_levels=levels)


def large_bridges(small):
    reports=[]
    for tag in ('3d100','1d25','1d20'):
        p=ROOT/'research_20261010/low_band/translation_band/refined'/f'large_seed_g{tag}.json'
        source=json.loads(p.read_text());row=source['exact'];g=F(source['g'])
        states,replay=check_recurrence(row);assert states[0][0]==8
        # At base side 4, the exact product telescopes: J1 = A^4 B^2 C.
        # As each true purity is <=1, all three true purities are >= J1.
        j=F(row['J1']);base_beta=F(row['beta_initial'])
        assert F(row['bootstrap']['input']['beta'])==2*base_beta
        windows=[window(j,j,j,4,base_beta)]
        windows += [window(*state,n,beta) for n,beta,state in states if n<replay['asymptotic_n']]
        target=F(replay['gap_lower'])
        short=[r for r in small['small_sizes'] if F(r['g'])==g]
        assert len(short)==2 and all(F(r['gap_lower'])>=target for r in short)
        assert all(F(r['gap_lower'])>=target for r in windows)
        reports.append(dict(g=str(g),source=str(p.relative_to(ROOT)),source_sha256=sha(p),
                            physical_input_status='conditional on separate independent large-seed physical audit',
                            exact_scalar_replay=replay,base_canonical_n=4,first_updated_n=8,
                            base_bridge_input_reason='Exact identity J1=A^4 B^2 C with 0<A,B,C<=1 implies A,B,C>=J1.',
                            finite_windows=windows,local_L2_L3=short,
                            all_integer_L_ge2_gap=str(target),all_integer_gap_display=float(target),
                            size_partition=['L=2,3 local positive comparison','L=4..7 base-window interpolation',
                                            'L=8..15 first-state interpolation when needed',
                                            'L>=accepted_n independently replayed asymptotic theorem']))
        print('LARGE EXACT BRIDGE',g,float(target),[(r['n'],r['gap_display']) for r in windows],flush=True)
    return dict(status='PASS exact full-integer scalar/local bridges; larger physical seed inputs remain separately conditional',records=reports)


def scalar_refinement(small):
    p=ROOT/'research_20261010/low_band/scalar_refinement/symmetric_beta909d100_eight_rounds.json'
    old=ROOT/'research_20261010/low_band/symmetric_correlated_beta909d100_FINAL.json'
    evidence=ROOT/'research_20261010/low_band_review/symmetric_correlated_fast_results.json'
    row=json.loads(p.read_text())[0];frozen=json.loads(old.read_text())[0];audited=json.loads(evidence.read_text())
    assert row['source_sha256']==sha(old)==audited['source_sha256']
    for key in ['beta_initial','order','J1','J2','C','first_purities']:
        assert row[key]==frozen[key]
    assert row['first_purities']==audited['records'][0]['first_purities']
    assert row['bootstrap']['input']==frozen['bootstrap']['input']
    states,replay=check_recurrence(row,dyadic=True)
    assert len(states)==9 and replay['asymptotic_n']==1024
    windows=[window(*state,n,beta) for n,beta,state in states if n<1024]
    target=F(replay['gap_lower'])
    # Retain the already independently reviewed elementary estimate .19 here.
    weyl=[dict(L=L,gap_lower=str(1-3*F(3,100)*L*L)) for L in (2,3)]
    assert min(F(r['gap_lower']) for r in weyl)>target
    assert all(F(r['gap_lower'])>target for r in windows)
    print('SCALAR EXACT EIGHT-ROUND ALL-SIZE PASS',float(target),flush=True)
    return dict(status='PASS independent exact eight-round replay and all-integer bridge, inheriting frozen independently audited physical inputs',
                source=str(p.relative_to(ROOT)),source_sha256=sha(p),frozen_source=str(old.relative_to(ROOT)),frozen_source_sha256=sha(old),
                prior_independent_audit=str(evidence.relative_to(ROOT)),prior_independent_audit_sha256=sha(evidence),
                exact_scalar_replay=replay,finite_windows=windows,small_L2_L3_weyl=weyl,
                minimum_missing_window_gap=str(min(F(r['gap_lower']) for r in windows)),
                all_integer_L_ge2_gap=str(target),all_integer_gap_display=float(target))


def main():
    start=time.monotonic()
    # Pin every reviewed source, including the producer's freeze manifest.
    for name,expected in json.loads((HERE/'SOURCE_MANIFEST_SHA256.json').read_text()).items():
        assert sha(ROOT/name)==expected,('source changed',name)
    td=ROOT/'research_20261010/low_band/translation_band'
    frozen=json.loads((td/'FROZEN_MANIFEST_1759.json').read_text())
    for tag in ('3d100','1d25','1d20'):
        name=f'refined/large_seed_g{tag}.json'
        assert sha(td/name)==frozen[name]
    small=local_small_certificate()
    (HERE/'local_small_sizes.json').write_text(json.dumps(small,indent=2)+'\n')
    result=large_bridges(small);(HERE/'large_seed_bridge_results.json').write_text(json.dumps(result,indent=2)+'\n')
    scalar=scalar_refinement(small);(HERE/'eight_round_scalar_results.json').write_text(json.dumps(scalar,indent=2)+'\n')
    manifest={str(p.relative_to(ROOT)):sha(p) for p in sorted(HERE.glob('*')) if p.is_file() and p.name!='MANIFEST_SHA256.json'}
    (HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('seconds',time.monotonic()-start,'maxrss_kib',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)

if __name__=='__main__':main()
