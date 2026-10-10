"""Independent bosonic operator and Jacobi audit. No producer modules imported."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import sys,resource
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1536*1024**2,1536*1024**2))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import itertools,math,json,hashlib,time,shutil
import numpy as np
import scipy.linalg as la
import sympy as S
OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'low_band'/'bosonic_tail'
MANIFEST='FROZEN_MANIFEST_1823.json'
EXPECTED='4bc8db06b3695b37f01dd12b63eb15476853b5dfe5d5bd772897e6d32d81a08e'
SNAP=OUT/'snapshot'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(OUT/'results'/name).write_text(json.dumps(obj,indent=2)+'\n')
def snapshot():
    assert sha(SRC/MANIFEST)==EXPECTED
    manifest=json.loads((SRC/MANIFEST).read_text())['files']
    manifest[MANIFEST]=EXPECTED
    for name,h in manifest.items():
        p=SRC/name;assert sha(p)==h
        target=SNAP/name
        if target.exists():assert sha(target)==h
        else:shutil.copyfile(p,target)
    (OUT/'INPUT_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

def inertia(a):
    a=[[F(v) for v in row] for row in a];negative=positive=0
    while a:
        n=len(a);i=next((i for i in range(n) if a[i][i]),None)
        if i is None:
            pair=next(((i,j) for i in range(n) for j in range(i+1,n) if a[i][j]),None)
            if pair is None:return [negative,n,positive]
            i,j=pair
            for k in range(n):a[i][k]+=a[j][k]
            for k in range(n):a[k][i]+=a[k][j]
        a[0],a[i]=a[i],a[0]
        for row in a:row[0],row[i]=row[i],row[0]
        p=a[0][0];negative+=p<0;positive+=p>0
        a=[[a[i][j]-a[i][0]*a[0][j]/p for j in range(1,n)] for i in range(1,n)]
    return [negative,0,positive]

def rmat(m):return [[F(str(x)) for x in row] for row in m.tolist()]
def psd_hermitian(m):
    assert m==m.H
    real=m.applyfunc(S.re);imag=m.applyfunc(S.im)
    return inertia(rmat(real.row_join(-imag).col_join(imag.row_join(real))))

def occupations(d,q):
    if d==1:return [(q,)]
    return [(k,)+tail for k in range(q+1) for tail in occupations(d-1,q-k)]

def monomial_metric(states):return S.diag(*[math.prod(math.factorial(x) for x in s) for s in states])
def creation(K,q):
    d=K.rows;source=occupations(d,q);target=occupations(d,q+2);index={s:i for i,s in enumerate(target)}
    b=S.zeros(len(target),len(source))
    for col,s in enumerate(source):
        for u in range(d):
            for v in range(d):
                t=list(s);t[u]+=1;t[v]+=1
                b[index[tuple(t)],col]+=K[u,v]/2
    return b

def bosonic_tests():
    matrices=[('single_complex',S.Matrix([[1+2*S.I]]),5),
        ('complex_symmetric_nonnormal',S.Matrix([[1+S.I,S.Rational(1,3)-S.I/2],[S.Rational(1,3)-S.I/2,-S.Rational(2,3)+S.I/4]]),None),
        ('three_mode_identity',S.eye(3),1),
        ('real_symmetric',S.Matrix([[1,S.Rational(1,3)],[S.Rational(1,3),S.Rational(1,2)]]),S.Rational(16,9))]
    out=[]
    for name,K,k2 in matrices:
        assert K==K.T;KK=(K*K.H).applyfunc(S.simplify);v=S.trace(KK)/2
        if k2 is None:k2=max(sum(abs(S.re(x))+abs(S.im(x)) for x in KK.row(i)) for i in range(K.rows))
        assert psd_hermitian(k2*S.eye(K.rows)-KK)[0]==0
        if name=='complex_symmetric_nonnormal':assert K*K.H!=K.H*K
        for q in range(9 if K.rows<=2 else 7):
            states=occupations(K.rows,q);index={s:i for i,s in enumerate(states)};metric=monomial_metric(states)
            b=creation(K,q);gram=(b.H*monomial_metric(occupations(K.rows,q+2))*b).applyfunc(S.simplify)
            lowered=S.zeros(len(states))
            if q>=2:
                prev=creation(K,q-2);lowered=metric*prev*monomial_metric(occupations(K.rows,q-2)).inv()*prev.H*metric
            dgamma=S.zeros(len(states))
            for col,s in enumerate(states):
                for u in range(K.rows):
                    for z in range(K.rows):
                        if s[z]:
                            t=list(s);t[z]-=1;t[u]+=1
                            dgamma[index[tuple(t)],col]+=KK[u,z]*s[z]
            comm=(gram-lowered-metric*dgamma-v*metric).applyfunc(S.simplify)
            assert comm==S.zeros(len(states))
            bound=(q//2+1)*v+k2*((q+1)**2//4)
            residue=(bound*metric-gram).applyfunc(S.simplify);inert=psd_hermitian(residue);assert inert[0]==0
            if name in ('single_complex','three_mode_identity'):assert inert[1]>0
            diagonal=np.diag(np.asarray(metric,dtype=float));normalized=np.asarray(gram,dtype=complex)/np.sqrt(diagonal[:,None]*diagonal[None,:])
            exactnorm=float(la.eigvalsh(normalized)[-1])
            out.append(dict(matrix=name,q=q,dimension=len(states),vacuum_norm_squared=str(v),kappa_squared_upper=str(k2),
              bound=str(bound),commutator_exact=True,complex_realification_PSD_inertia=inert,norm_squared_float_diagnostic=exactnorm))
        print('FOCK PASS',name,flush=True)
    save('fock_tests.json',out);return out

def local_matrix():
    # Physical computational spin order is down-down, down-up, up-down, up-up.
    p=S.Matrix([[0,1,0,0],[-1/S.sqrt(2),0,1/S.sqrt(2),0],[1/S.sqrt(2),0,1/S.sqrt(2),0],[0,0,0,1]])
    assert p.T*p==S.eye(4);pp=S.kronecker_product(p,p);V=S.zeros(16)
    for c in range(16):
        for u,z in ((0,2),(1,3)):
            bu=(c>>(3-u))&1;bz=(c>>(3-z))&1
            V[c,c]+=S.Rational((2*bu-1)*(2*bz-1),4)
            if bu!=bz:V[c^(1<<(3-u))^(1<<(3-z)),c]+=S.Rational(1,2)
    normalized=(pp.T*V*pp).applyfunc(S.simplify)
    assert all(x.is_Rational for x in normalized)
    kernel=rmat(normalized);q=[(i//4!=0)+(i%4!=0) for i in range(16)]
    pres=[[kernel[i][j] if q[i]==q[j] else F(0) for j in range(16)] for i in range(16)]
    for i in range(16):pres[i][i]+=F(q[i],2)
    inert=inertia(pres);assert inert[0]==0
    expected={(1,3):-F(1,2),(2,2):F(1,2),(3,1):-F(1,2)}
    actual={(i//4,i%4):kernel[i][0] for i in range(16) if q[i]==2 and kernel[i][0]}
    assert actual==expected
    assert all(not kernel[i][j] or abs(q[i]-q[j]) in (0,2) for i in range(16) for j in range(16))
    save('physical_local.json',dict(orthonormal_transform_verified=True,number_preserving_PSD_inertia=inert,
         normalized_creation_entries=[[i,j,str(x)] for (i,j),x in actual.items()],full_normalized_kernel=[[str(x) for x in row] for row in kernel]))
    return kernel

def graph(nx,ny):
    edges=Counter()
    for x in range(nx):
        for y in range(ny):
            i=x*ny+y
            for j in (((x+1)%nx)*ny+y,x*ny+(y+1)%ny):edges[tuple(sorted((i,j)))]+=1
    n=nx*ny;assert all(i!=j for i,j in edges)
    assert [sum(w for e,w in edges.items() if i in e) for i in range(n)]==[4]*n
    return edges

def physical_tests(kernel):
    out=[];g=F(1,10)
    for nx,ny,maxq in ((2,2,2),(3,2,2),(3,3,1),(4,2,1)):
        n=nx*ny;ed=graph(nx,ny);v=F(3,4)*g*g*sum(w*w for w in ed.values());k2=4*g*g
        for q in range(maxq+1):
            states=[]
            for sites in itertools.combinations(range(n),q):
                for colors in itertools.product((1,2,3),repeat=q):
                    state=[0]*n
                    for i,c in zip(sites,colors):state[i]=c
                    states.append(tuple(state))
            cols=[]
            for state in states:
                col=defaultdict(F);boson=defaultdict(F)
                for (i,j),w in ed.items():
                    old=4*state[i]+state[j]
                    for new in range(16):
                        a,b=divmod(new,4)
                        if (a!=0)+(b!=0)==(state[i]!=0)+(state[j]!=0)+2 and kernel[new][old]:
                            target=list(state);target[i]=a;target[j]=b;col[tuple(target)]+=g*w*kernel[new][old]
                    # Orthogonal hard-core projection kills repeated occupation at either site.
                    if state[i]==state[j]==0:
                        for a,b,J in ((1,3,-1),(2,2,1),(3,1,-1)):
                            target=list(state);target[i]=a;target[j]=b;boson[tuple(target)]+=g*w*J/2
                assert dict(col)==dict(boson);cols.append(dict(col))
            gram=[[sum((x*cols[j].get(st,0) for st,x in cols[i].items()),F(0)) for j in range(len(states))] for i in range(len(states))]
            bound=(q//2+1)*v+k2*((q+1)**2//4)
            inert=inertia([[bound*(i==j)-gram[i][j] for j in range(len(states))] for i in range(len(states))]);assert inert[0]==0
            if q==0:assert gram==[[v]]
            out.append(dict(nx=nx,ny=ny,q=q,input_dimension=len(states),weighted_edge_square_sum=sum(w*w for w in ed.values()),
              exact_physical_equals_compressed_B=True,vacuum_creation_norm_squared=str(v),bosonic_bound=str(bound),
              bound_minus_orthonormal_gram_inertia=inert,physical_norm_squared_float_diagnostic=float(la.eigvalsh(np.array(gram,dtype=float))[-1])))
            print('PHYSICAL PASS',nx,ny,q,len(states),flush=True)
    save('physical_tests.json',out);return out

def counts(nx,ny):
    n=nx*ny;out=[]
    assert nx>=4 and ny>=4 and nx%2==ny%2==0
    for q in range(n+1):
        h=min(q,n-q);ceil=math.isqrt(4*h)
        if ceil*ceil<4*h:ceil+=1
        iso=2*q-min(ceil,nx,ny)
        direct=min(2*q,q*q//4);rem=n-q;comp=4*q-2*n+min(2*rem,rem*rem//4)
        out.append(min(iso,direct,comp))
    return out,[2*n-4*q+z for q,z in enumerate(out)]

def audit_bins():
    out=[]
    for path in sorted(SNAP.glob('bosonic_bins_*.json')):
        rec=json.loads(path.read_text());nx,ny,n,g=rec['nx'],rec['ny'],rec['N'],F(rec['g']);assert n==nx*ny
        assert 0<=g<F(1,2);ed=graph(nx,ny);v=F(3,4)*g*g*sum(w*w for w in ed.values());k2=4*g*g
        assert [[i,j,w] for (i,j),w in sorted(ed.items())]==rec['weighted_edges']
        assert v==F(rec['vacuum_creation_norm_squared']) and k2==F(rec['creation_matrix_norm_squared_upper'])
        occ,emp=counts(nx,ny);assert rec['graph_counts']['occupied_edge_max']==occ and rec['graph_counts']['empty_edge_max']==emp
        assert rec['graph_counts']['degrees']==[4]*n
        diag=[(1-2*g)*q for q in range(n+1)]
        occupancy=[F(3,4)*g*g*emp[q]*occ[q+2] for q in range(n-1)]
        bosonic=[(q//2+1)*v+k2*((q+1)**2//4) for q in range(n-1)]
        off=[min(a,b) for a,b in zip(occupancy,bosonic)]
        for key,computed in [('diagonal',diag),('occupancy_offdiagonal_squared',occupancy),('bosonic_offdiagonal_squared',bosonic),('offdiagonal_squared',off)]:assert list(map(F,rec[key]))==computed
        index=1;prev=None;totalpivots=0
        for q,row in enumerate(rec['bins']):
            assert q==row['q'] and row['multiplicity']==math.comb(n,q)*3**q and row['first_ordered_index']==index
            index+=row['multiplicity'];parts=row['parity_compressions'];assert len(parts)==min(2,n+1-q);low=[]
            for start,part in zip((q,q+1),parts):
                ids=list(range(start,n+1,2));assert ids==part['number_indices'];t=F(part['lower']);piv=[]
                for z,i in enumerate(ids):
                    p=diag[i]-t-(off[ids[z-1]]/piv[-1] if z else 0);assert p>0;piv.append(p)
                assert piv==list(map(F,part['ldl_positive_pivots']));totalpivots+=len(piv);low.append(t)
            bound=min(low);bound=max(bound,prev) if prev is not None else bound
            assert bound==F(row['lower']);prev=bound
        assert index==4**n+1 and len(rec['bins'])==n+1
        assert F(rec['energy_shift'])==-F(3*n,4)
        olddiag=diag[2::2];oldoff=occupancy[2::2][:len(olddiag)-1]
        olda2=float(la.eigvalsh_tridiagonal(np.array(olddiag,dtype=float),-np.sqrt(np.array(oldoff,dtype=float)),select='i',select_range=(0,0))[0])
        olddiagodd=diag[3::2];oldoffodd=occupancy[3::2][:len(olddiagodd)-1]
        olda2=min(olda2,float(la.eigvalsh_tridiagonal(np.array(olddiagodd,dtype=float),-np.sqrt(np.array(oldoffodd,dtype=float)),select='i',select_range=(0,0))[0]))
        row=dict(source=path.name,sha256=sha(path),nx=nx,ny=ny,g=str(g),vacuum_norm_squared=str(v),
          a012=[r['lower'] for r in rec['bins'][:3]],a2=float(F(rec['bins'][2]['lower'])),
          previous_occupancy_only_a2_float_diagnostic=olda2,positive_rational_LDL_pivots=totalpivots,
          full_Hilbert_dimension=4**n,first_omitted_index=2+3*n,
          strict_bosonic_offdiagonal_improvements=sum(a<b for a,b in zip(bosonic,occupancy)),
          all_bin_multiplicities_indices_and_monotonicity_verified=True)
        out.append(row);print('BINS PASS',path.name,'a2',row['a2'],flush=True)
    assert len(out)==12;save('bin_replay.json',out);return out

def main():
    start=time.monotonic();manifest=snapshot();fock=bosonic_tests();kernel=local_matrix();physical=physical_tests(kernel);bins=audit_bins()
    for name,h in manifest.items():assert sha(SRC/name)==sha(SNAP/name)==h
    result=dict(status='passed_independent_exact_bosonic_lemma_implementation_physical_normalization_and_all_12_frozen_tail_bins',
      analytical_proof='PROOF.md',producer_manifest_sha256=EXPECTED,fock_cases=len(fock),physical_cases=len(physical),bin_files=len(bins),
      positive_rational_LDL_pivots=sum(row['positive_rational_LDL_pivots'] for row in bins),
      no_new_global_gap_claim=True,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      cpu_affinity=sorted(os.sched_getaffinity(0)),address_space_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0])
    save('summary.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
