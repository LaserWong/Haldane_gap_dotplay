#!/usr/bin/env python3
"""Independent exact acceptance audit of saved ordinary-bilayer candidates.

No generating code, floating optimizer, eigensolver, or prior audit module is
imported. Exact integer trial vectors are reconstructed in their full H-applied
support. Exponentials are independently enclosed at 220 bits with 48 Taylor
terms (saved candidates used 128 bits / 32 terms). Rational scalar updates are
checked from stored valid lower inputs. Only this directory is written.
"""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_k]='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
if hasattr(os,'sched_getaffinity'):
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:2])
from fractions import Fraction as Q
from collections import defaultdict,Counter
from functools import lru_cache
from pathlib import Path
import hashlib,json,math,time,sys,platform
import numpy as np
import sympy as sp
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
SOURCE=ROOT/'seed_size/results/optimized_bilayer_tail_results.json'
SCALE=1<<128
FINE=1<<220


def down(x,scale=SCALE):
    x=Q(x);return Q(x.numerator*scale//x.denominator,scale)
def up(x,scale=SCALE):
    x=Q(x);return Q(-((-x.numerator*scale)//x.denominator),scale)
@lru_cache(maxsize=None)
def exponential(x):
    """Positive Taylor sum + geometric tail, followed by exact interval squaring."""
    x=Q(x)
    if x<0:
        lo,hi=exponential(-x)
        return down(1/hi,FINE),up(1/lo,FINE)
    k=0
    while x>Q(1,16):x/=2;k+=1
    term=Q(1);total=term
    for j in range(1,49):term=term*x/j;total+=term
    next_term=term*x/49
    lo=down(total,FINE);hi=up(total+next_term/(1-x/50),FINE)
    for _ in range(k):lo=down(lo*lo,FINE);hi=up(hi*hi,FINE)
    return lo,hi

def G(x):
    assert 0<x<=1
    return 1-(1-x)**2/(2*x*x)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

# Unnormalised rung basis in dd,du,ud,uu physical product order.
V=((0,-1,1,0),(1,0,0,0),(0,1,1,0),(0,0,0,1))
WEIGHTS=tuple(sum(v*v for v in row) for row in V)
assert WEIGHTS==(2,1,2,1)

def spin_ops(layer):
    answer={}
    for kind in ('z','+','-'):
        phys=[[Q(0) for _ in range(4)] for _ in range(4)]
        for j in range(4):
            bits=[j//2,j%2]
            if kind=='z':phys[j][j]=Q(2*bits[layer]-1,2)
            elif kind=='+' and bits[layer]==0:
                bits[layer]=1;phys[2*bits[0]+bits[1]][j]=1
            elif kind=='-' and bits[layer]==1:
                bits[layer]=0;phys[2*bits[0]+bits[1]][j]=1
        answer[kind]=[[sum(V[i][r]*phys[r][c]*V[j][c] for r in range(4) for c in range(4))/WEIGHTS[i] for j in range(4)] for i in range(4)]
    return answer
OPS=[spin_ops(0),spin_ops(1)]
KERNEL={}
for layer in (0,1):
    o=OPS[layer]
    for i in range(4):
        for j in range(4):
            entries=[]
            for r in range(4):
                for s in range(4):
                    c=o['z'][r][i]*o['z'][s][j]+(o['+'][r][i]*o['-'][s][j]+o['-'][r][i]*o['+'][s][j])/2
                    if c:entries.append((r,s,c))
            KERNEL[layer,i,j]=entries

def local_spectrum_and_transfer():
    a,g,z=sp.symbols('a g z',real=True);R=sp.Rational
    spin=(sp.Matrix([[0,R(1,2)],[R(1,2),0]]),sp.Matrix([[0,sp.I/2],[-sp.I/2,0]]),sp.diag(-R(1,2),R(1,2)))
    def at(op,k):
        mats=[sp.eye(2) for _ in range(4)];mats[k]=op
        return sp.kronecker_product(*mats)
    site=[[at(op,k) for op in spin] for k in range(4)]
    dot=lambda i,j:sum((site[i][k]*site[j][k] for k in range(3)),sp.zeros(16))
    h=dot(0,1)+dot(2,3)+R(3,2)*sp.eye(16)
    matrix=a*h+g*(dot(0,2)+dot(1,3))
    expected=(z-2*a-g/2)**5*(z-2*a+g/2)**3*(z-a-g/2)**3*(z-a+g/2)**3*((z-a+g/2)**2-(a*a-a*g+g*g))
    cp=matrix.charpoly(z)
    assert sp.Poly(cp.as_expr().subs(cp.gen,z),z,a,g)==sp.Poly(expected,z,a,g)
    P=sp.Matrix.hstack(sp.Matrix([0,1,-1,0]),sp.Matrix([0,sp.I,sp.I,0]),sp.Matrix([1,0,0,1]),sp.Matrix([sp.I,0,0,-sp.I]))
    J=sp.Matrix([[0,1],[-1,0]])
    assert P.conjugate().T*P==2*sp.eye(4)
    assert sp.kronecker_product(J,J)*P.conjugate()==P
    antisymmetric=[]
    for layer in (0,1):
        for op in spin:
            phys=sp.kronecker_product(op,sp.eye(2)) if layer==0 else sp.kronecker_product(sp.eye(2),op)
            A=P.conjugate().T*phys*P/(2*sp.I)
            assert A==A.conjugate() and A.T==-A and A.T*A==sp.eye(4)/4
            antisymmetric.append([[str(v) for v in A.row(i)] for i in range(4)])
    rung=sum((sp.kronecker_product(op,op) for op in spin),sp.zeros(4))
    assert P.conjugate().T*rung*P/2==sp.diag(-R(3,4),R(1,4),R(1,4),R(1,4))
    return {'exact_symbolic_characteristic_polynomial':str(sp.factor(expected)),
            'physical_product_dimension':16,'time_reversal_real_basis_verified':True,
            'six_real_antisymmetric_factors_norm_half':antisymmetric,
            'both_directions':'same positive g and same-layer interactions; history proof in PROOF.md',
            'local_spectrum_formula_verified':True}

def check_local(a,b,g):
    assert g>=0 and g/2<=a<Q(1,4) and b>=0
    assert b+a-g/2>=0
    assert (b+a-g/2)**2>=a*a-a*g+g*g

def graph(nx,ny,g):
    idx=lambda x,y:(x%nx)*ny+(y%ny)
    return [(idx(x,y),l,idx(x+dx,y+dy),l,g) for x in range(nx) for y in range(ny) for dx,dy in ((1,0),(0,1)) for l in (0,1)]

def audit_ground(r,nx,ny,g):
    start=time.monotonic();N=nx*ny
    assert r['s']=='1/2' and r['N_dimers']==N and r['physical_sites']==2*N and r['full_dimension']==4**N and r['retained_states']==1
    path=ROOT/'low_energy'/r['trial_artifact']
    with np.load(path,allow_pickle=False) as arr:
        states=[tuple(map(int,st)) for st in arr['basis']]
        vector=list(map(int,arr['vector']))
    assert len(states)==len(vector)==r['trial_subspace_dimension'] and len(set(states))==len(states)
    assert all(len(st)==N and all(0<=i<4 for i in st) for st in states)
    assert all(sum(x!=0 for x in st)<=r['trial_max_excited_dimers'] for st in states)
    assert all(sum((0,-1,0,1)[i] for i in st)==0 for st in states)
    expected=graph(nx,ny,g)
    edges=[(i,l,j,ll,Q(c)) for i,l,j,ll,c in r['weak_bonds']]
    assert Counter(edges)==Counter(expected) and len(edges)==4*N
    denominator=800;E00=-Q(3*N,4)
    mv=defaultdict(int);support=set(states);nnz=0
    for st,v in zip(states,vector):
        col=defaultdict(int)
        col[st]=int(denominator*(E00+sum(x!=0 for x in st)))
        for i,l,j,ll,c in edges:
            assert i!=j and l==ll
            for ri,rj,co in KERNEL[l,st[i],st[j]]:
                integer=denominator*c*co
                assert integer.denominator==1
                out=list(st);out[i]=ri;out[j]=rj
                col[tuple(out)]+=int(integer)
        for dest,c in col.items():
            if c:
                support.add(dest);nnz+=1;mv[dest]+=c*v
    metric=lambda st:math.prod(WEIGHTS[i] for i in st)
    norm=sum(metric(st)*v*v for st,v in zip(states,vector))
    assert norm>0
    rho=Q(sum(metric(st)*v*mv[st] for st,v in zip(states,vector)),denominator*norm)
    residual=Q(sum(metric(st)*v*v for st,v in mv.items()),denominator**2*norm)-rho*rho
    assert rho==Q(r['exact_rayleigh']) and residual==Q(r['exact_residual_squared']) and residual>=0
    assert len(support)==r['reached_support_dimension'] and nnz==r['sparse_nnz']
    assert Q(r['Vmin'])==-3*g*N and Q(r['Vmax'])==g*N and Q(r['E00'])==E00
    if 'relative_form_bound' in r:
        rb=r['relative_form_bound'];lc=rb['local_certificate']
        assert Q(lc['coupling'])==g and lc['spin']=='1/2' and lc['kind']=='bilayer'
        a,b=Q(lc['a']),Q(lc['b']);check_local(a,b,g)
        alpha=1-4*a;B=2*N*b
        assert Q(rb['alpha'])==alpha and Q(rb['B'])==B and Q(rb['second_shift_lower'])==alpha-B
        second=E00+alpha-B
    else:second=E00+1-3*g*N
    assert second==Q(r['second_eigenvalue_lower']) and second>E00 and rho<second
    lower=rho-residual/(second-rho)
    assert lower==Q(r['ground_lower']) and rho==Q(r['ground_upper'])
    return {'shape':[nx,ny],'g':str(g),'physical_spins':2*N,'full_Hilbert_dimension':4**N,
            'linear_trial_dimension':len(states),'retained_states':1,'MPS_bond_dimension':None,
            'full_H_applied_union_support':len(support),'exact_matrix_nonzeros':nnz,
            'trial_npz_sha256':sha(path),'integer_norm':str(norm),'Rayleigh_exact':str(rho),
            'full_residual_squared':str(residual),'ground_lower':str(lower),'ground_upper':str(rho),
            'second_eigenvalue_lower':str(second),'passed':True,'seconds':time.monotonic()-start}

def canonicalize(p,order):
    p=list(p);labels=list(order)
    for at,target in enumerate('xyt'):
        i=labels.index(target)
        while i>at:
            left,right=p[i-1:i+1]
            p[i-1:i+1]=[down(left*right),down(left*left*right)]
            labels[i-1],labels[i]=labels[i],labels[i-1];i-=1
    assert labels==list('xyt')
    return p

def audit_scalar(row):
    best=row['best_grid_gap'];nodes=best['thermal_tail_nodes'];rec=best['ground_certificate_records']
    assert len(nodes)==4
    state=[2,2,Q(best['beta_initial'])];coordinates=[state.copy()]
    for axis in row['order']:
        state=state.copy();state['xyt'.index(axis)]*=2;coordinates.append(state)
    qs=[];Us=[];betas=[];node_results=[]
    for i,(node,coord) in enumerate(zip(nodes,coordinates)):
        nx,ny,beta=coord;N=nx*ny;r=rec[{4:0,8:1,16:2}[N]]
        assert [node['nx'],node['ny'],Q(node['beta'])]==coord and node['node_index']==i and node['N_dimers']==N and Q(node['g'])==Q(row['g'])
        for name in ('ground_lower','ground_upper','E00'):assert node[name]==r[name]
        p=node['parameters'];a,b,alpha,B=map(Q,(p['a'],p['b_upper'],p['alpha'],p['B_upper']))
        g=Q(row['g']);lo,U,E00=map(Q,(node['ground_lower'],node['ground_upper'],node['E00']))
        check_local(a,b,g);assert alpha==1-4*a and B==2*N*b
        tail=exponential(beta*(B+U-E00))[1]*((1+3*exponential(-beta*alpha)[1])**N-1)
        assert Q(p['tail_upper'])>=tail
        q=exponential(beta*(U-lo))[1]+Q(p['tail_upper'])
        assert Q(p['upper_Q'])>=q
        qs.append(Q(p['upper_Q']));Us.append(U);betas.append(beta)
        node_results.append({'coordinates':[nx,ny,str(beta)],'a':str(a),'b':str(b),'alpha':str(alpha),'B':str(B),
                             'stored_tail_upper':p['tail_upper'],'independent_tail_upper_220bit':str(up(tail,FINE)),
                             'stored_Q_upper':p['upper_Q'],'independent_Q_upper_220bit':str(up(q,FINE)),'passed':True})
    def ratio_lower(co):
        x=-sum((Q(c)*beta*U for c,beta,U in zip(co,betas,Us)),Q(0))
        value=exponential(x)[0]
        for c,q in zip(co,qs):
            if c<0:value/=q**(-c)
        return value
    p0=list(map(Q,best['initial_ordered_purities']))
    for val,co in zip(p0,((-2,1,0,0),(0,-2,1,0),(0,0,-2,1))):assert 0<val<=ratio_lower(co)<=1
    J1,J2=Q(best['correlated_J1']),Q(best['correlated_J2'])
    assert 0<J1<=ratio_lower((-8,0,0,1))<=1
    assert 0<J2<=ratio_lower((0,-8,0,2))<=1
    A=down(G(J1));B=down(G(J2*A));C=down(G(p0[2]**4*A*A*B))
    p=[A,B,C];assert list(map(str,p))==best['correlated_first_step']
    n=4;beta=2*Q(best['beta_initial']);stages=[{'n':n,'beta':str(beta),'purities':list(map(str,p))}]
    for recorded in best['updates']:
        assert max(1-v for v in canonicalize(p,row['order']))>Q(1,500)
        for _ in range(3):p=p[1:]+[down(G(p[0]**4*p[1]**2*p[2]))]
        n*=2;beta*=2
        assert list(map(str,p))==recorded
        stages.append({'n':n,'beta':str(beta),'purities':list(map(str,p))})
    cp=canonicalize(p,row['order']);u=max(1-v for v in cp);gap=Q(best['gap_lower'])
    assert best['accepted'] and best['rounds_after_input']==len(best['updates'])
    assert n==best['n']==best['m'] and beta==Q(best['beta'])
    assert list(map(str,p))==best['ordered_purities'] and list(map(str,cp))==best['canonical_purities']
    assert u==Q(best['u_canonical']) and 0<u<=Q(1,500)
    assert exponential(beta*gap)[1]<1/(32*u)
    return {'g':row['g'],'order':row['order'],'tail_nodes':node_results,'all_stages':stages,
            'n':n,'beta':str(beta),'u':str(u),'gap_exact':str(gap),'gap_display':float(gap),
            'gap_decimal_down_12':str(down(gap,10**12)),'gap_exp_check_220bit':True,'passed':True}

def interpolation_and_bridges(rows):
    # Verify the only endpoint constants needed by the analytic monotonic proofs.
    v=Q(1,40)
    spatial=(3-3*v+v*v)**2/(2*(1-v)**6)
    assert spatial<5
    assert 1-5*v-v*v>0
    interp=Q(3,2)+5*v+2/(1-2*v)
    assert interp<4
    u=Q(1,200)
    assert 5*u<=v and 49/(2*(1-7*u)**2)<32 and 32*u*u<=u
    assert 20*u/(1-20*u)<=32*u
    r001=next(r for r in rows if r['g']=='1/100' and r['order']=='xyt')
    r002=next(r for r in rows if r['g']=='1/50' and r['order']=='xyt')
    small001=Q(73,100)
    assert small001>Q(r001['gap_exact'])
    # One single rational local comparison works for all 2<=L<=7 at g=.02.
    a,b,g=Q(1,20),Q(9,2500),Q(1,50)
    check_local(a,b,g)
    small002=1-4*a-2*49*b
    assert small002==Q(559,1250) and small002>Q(r002['gap_exact'])
    stage=next(v for v in r002['all_stages'] if v['n']==8)
    assert stage['beta']=='49'
    u8=max(1-Q(v) for v in stage['purities'])
    assert u8<Q(1,200) and 5*u8<Q(1,40)
    thermal=1-20*u8;ratio=(1-thermal)/thermal
    assert thermal>Q(1,2)
    gap=Q(r002['gap_exact'])
    assert exponential(49*gap)[1]*ratio<1
    # Set the stronger bridge decimal by exact integer bisection, no logarithm.
    lo,hi=0,10**12
    while hi-lo>1:
        mid=(lo+hi)//2
        if exponential(Q(49*mid,10**12))[1]*ratio<1:lo=mid
        else:hi=mid
    finite_gap=Q(lo,10**12)
    assert finite_gap>gap and exponential(49*finite_gap)[1]*ratio<1
    return {'one_dimensional_domain':'0<=v<=1/40','1d_spatial_squaring_coefficient_at_endpoint':str(spatial),
            '1d_interpolation_endpoint':str(interp),'two_dimensional_domain':'0<=u<=1/200',
            'g001':{'squares_2_to_3_gap':str(small001),'squares_ge_4_gap':r001['gap_exact'],'all_integer_squares_ge_2_gap':r001['gap_exact']},
            'g002':{'squares_2_to_7':{'a':str(a),'b':str(b),'gap_lower':str(small002)},
                    'squares_8_to_16':{'base_n':8,'beta':'49','u':str(u8),'u_display':float(u8),
                                          'thermal_purity_lower':str(thermal),'excitation_weight_ratio_upper':str(ratio),
                                          'gap_lower_decimal_down_12':str(finite_gap),'gap_display':float(finite_gap)},
                    'squares_ge_16_gap':r002['gap_exact'],'all_integer_squares_ge_2_gap':r002['gap_exact']},
            'passed':True}

def main():
    start=time.monotonic();data=json.loads(SOURCE.read_text());hashes={str(SOURCE.relative_to(ROOT)):sha(SOURCE)}
    local=local_spectrum_and_transfer();print('LOCAL SPECTRUM AND TRANSFER IDENTITIES PASS',flush=True)
    grounds=[];seen={}
    for row in data:
        assert row['model_id']=='square_af_bilayer_spin_half_unit_rung'
        best=row['best_grid_gap']
        if best is None:continue
        for r,shape in zip(best['ground_certificate_records'],((2,2),(4,2),(4,4))):
            key=(row['g'],shape)
            source=ROOT/'low_energy'/(r['trial_artifact'].replace('_trial.npz','_ground.json'))
            assert json.loads(source.read_text())==r
            hashes[str(source.relative_to(ROOT))]=sha(source)
            trial=ROOT/'low_energy'/r['trial_artifact'];hashes[str(trial.relative_to(ROOT))]=sha(trial)
            if key in seen:
                assert seen[key]==r
                continue
            seen[key]=r
            result=audit_ground(r,*shape,Q(row['g']));grounds.append(result)
            print('GROUND PASS',row['g'],shape,'dim',result['full_Hilbert_dimension'],'support',result['full_H_applied_union_support'],flush=True)
    rows=[]
    for row in data:
        if row['best_grid_gap'] is None:continue
        result=audit_scalar(row);rows.append(result)
        print('OPTIMIZED SCALAR PASS',row['g'],row['order'],'gap',result['gap_display'],flush=True)
    bridge=interpolation_and_bridges(rows)
    print('ALL-INTEGER G=.02 BRIDGE PASS',bridge['g002']['squares_8_to_16']['gap_display'],flush=True)
    report={'status':'PASS independent exact input, full residual, physical local identity, all 24 optimized-tail nodes, six scalar paths and finite-size bridges',
            'baseline':'main 6be889a as supplied by parent; this extracted workspace has no .git metadata',
            'model':'ordinary spin-1/2 square bilayer; rung 1; both intralayer directions g; no cross-layer bonds; oriented positive-neighbor periodic multigraph, L=2 bonds doubled',
            'input_sha256':hashes,'local':local,'ground_checks':grounds,'optimized_scalar_checks':rows,
            'bridges':bridge,'claims':{'g_1_over_100_all_integer_L_ge_2':'0.168921021674','g_1_over_50_all_integer_L_ge_2':'0.057308457817'},
            'limitations':['No full-space many-body diagonalization.','No proof-assistant formalization.','These two fixed couplings do not establish a maximal certifiable coupling or a physical phase boundary.','Square sizes, and stated same-scale rectangles only; not arbitrary aspect ratios.'],
            'runtime':{'seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,'sympy':sp.__version__,'BLAS_threads':1,'affinity_CPUs':sorted(os.sched_getaffinity(0)) if hasattr(os,'sched_getaffinity') else None}}
    (OUT/'optimized_bilayer_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['claims']),flush=True)
if __name__=='__main__':main()
