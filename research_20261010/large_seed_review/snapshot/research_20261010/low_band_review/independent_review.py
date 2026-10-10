"""Independent rational/physical-spin audit. Imports no producer modules.
Run from any working directory; outputs remain in this review directory.
Exact acceptance uses Fraction Schur complements, not floating eigenvalues.
"""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[name]='1'
import sys, resource
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import itertools,math,json,time,hashlib,argparse,gc
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla
OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'low_band'


def inertia_fraction(matrix):
    """Rational symmetric Gaussian elimination, independently of Bareiss code."""
    a=[[F(v) for v in row] for row in matrix]
    neg=pos=0
    while a:
        n=len(a)
        p=next((i for i in range(n) if a[i][i]),None)
        if p is None:
            pair=next(((i,j) for i in range(n) for j in range(i+1,n) if a[i][j]),None)
            if pair is None:return (neg,n,pos)
            i,j=pair
            # e_i -> e_i+e_j, an invertible congruence.
            for c in range(n):a[i][c]+=a[j][c]
            for r in range(n):a[r][i]+=a[r][j]
            p=i
        a[0],a[p]=a[p],a[0]
        for row in a:row[0],row[p]=row[p],row[0]
        pivot=a[0][0];neg+=pivot<0;pos+=pivot>0
        a=[[a[i][j]-a[i][0]*a[0][j]/pivot for j in range(1,n)] for i in range(1,n)]
    return neg,0,pos


def physical_local_pair():
    # Ordering |down down>, |down up>, |up down>, |up up>.
    # Columns: singlet, triplet M=-1, M=0, M=+1. No production dimer routines.
    p=np.array([[0,1,0,0],[-1,0,1,0],[1,0,1,0],[0,0,0,1]],dtype=object)
    pp=np.kron(p,p);w=np.array([2,1,2,1],dtype=object);ww=np.kron(w,w)
    # 4 times (S_0.S_2+S_1.S_3), with the two layer couplings included together.
    v4=np.zeros((16,16),dtype=object)
    for c in range(16):
        bits=[(c>>(3-j))&1 for j in range(4)]
        for i,j in [(0,2),(1,3)]:
            v4[c,c]+=(2*bits[i]-1)*(2*bits[j]-1)
            if bits[i]!=bits[j]:v4[c^(1<<(3-i))^(1<<(3-j)),c]+=2
    raw=pp.T@v4@pp
    kernel=[]
    for c in range(16):
        kernel.append([(r//4,r%4,F(int(raw[r,c]),4*int(ww[r]))) for r in range(16) if raw[r,c]])
    assert all(ww[r]*sum((v for x,y,v in kernel[c] if 4*x+y==r),F(0)) ==
               ww[c]*sum((v for x,y,v in kernel[r] if 4*x+y==c),F(0)) for r in range(16) for c in range(16))
    return kernel
KERNEL=physical_local_pair()


def edges(nx,ny):
    out=[]
    for x in range(nx):
        for y in range(ny):
            i=x*ny+y
            out += [(i,((x+1)%nx)*ny+y),(i,x*ny+(y+1)%ny)]
    assert len(out)==2*nx*ny
    assert all(i!=j for i,j in out)
    return out


def reconstruct(rec,block):
    trial=np.load(SRC/block['trial_file']);basis=trial['basis'];v=trial['vectors'].astype(object)
    n=rec['N'];g=F(rec['g']);ed=edges(rec['nx'],rec['ny'])
    expected=[]
    for q in range(block['parity'],block['qmax']+1,2):
        for sites in itertools.combinations(range(n),q):
            for vals in itertools.product((1,2,3),repeat=q):
                if sum(x-2 for x in vals)!=block['M']:continue
                state=[0]*n
                for i,x in zip(sites,vals):state[i]=x
                expected.append(state)
    assert np.array_equal(basis,np.array(expected,dtype=np.uint8))
    codes=[sum(int(x)<<(2*i) for i,x in enumerate(state)) for state in basis]
    reached=list(codes);lookup={s:i for i,s in enumerate(reached)}
    den=math.lcm(*( (g*x).denominator for row in KERNEL for _,_,x in row))
    kr=[[(i,j,int(g*x*den)) for i,j,x in row] for row in KERNEL]
    rows=[];cols=[];data=[]
    for c,code in enumerate(codes):
        a=defaultdict(int);a[code]=sum(x!=0 for x in basis[c])*den
        for i,j in ed:
            si=(code>>(2*i))&3;sj=(code>>(2*j))&3
            for pi,pj,val in kr[4*si+sj]:
                changed=code^((si^pi)<<(2*i))^((sj^pj)<<(2*j))
                a[changed]+=val
        for changed,val in a.items():
            if not val:continue
            if changed not in lookup:lookup[changed]=len(reached);reached.append(changed)
            rows.append(lookup[changed]);cols.append(c);data.append(val)
    h=sp.coo_matrix((np.array(data,dtype=np.int64),(rows,cols)),shape=(len(reached),len(basis))).tocsr()
    del rows,cols,data,lookup
    weights=np.array([1<<sum(((code>>(2*i))&1)==0 for i in range(n)) for code in reached],dtype=np.int64)
    for code in reached:
        st=[(code>>(2*i))&3 for i in range(n)]
        assert sum(x!=0 for x in st)%2==block['parity']
        assert sum(x-2 for x in st if x)==block['M']
    hv=np.zeros((len(reached),v.shape[1]),dtype=object)
    for r in range(h.shape[0]):
        for z in range(h.indptr[r],h.indptr[r+1]):hv[r]+=int(h.data[z])*v[h.indices[z]]
    def gram(a,b,ww):
        out=np.zeros((a.shape[1],b.shape[1]),dtype=object)
        for lo in range(0,len(ww),2048):
            hi=min(len(ww),lo+2048)
            out+=a[lo:hi].T@(b[lo:hi]*ww[lo:hi,None].astype(object))
        return out
    independent_den=den
    prod_den=block['matrix_denominator']
    assert prod_den%den==0,(den,prod_den)
    hv*=prod_den//den
    den=prod_den
    G=gram(v,v,weights[:len(v)])
    A=gram(v,hv[:len(v)],weights[:len(v)])
    B=gram(hv,hv,weights)
    # Matrix scales can differ between two independent local constructions.
    prod_den=block['matrix_denominator']
    assert den==prod_den,(den,prod_den)
    for name,matrix in [('G',G),('A',A),('B',B)]:
        saved=np.array([[int(x) for x in row] for row in block[name]],dtype=object)
        assert np.array_equal(matrix,saved),name
    d=[F(x) for x in block['diagonal_proposal']]
    # Rebuild E entry by entry from the directly applied residual, including all leakage.
    rden=math.lcm(den,*(x.denominator for x in d))
    residual=hv*(rden//den)
    for j in range(v.shape[1]):residual[:len(v),j]-=v[:,j]*int(rden*d[j])
    ER=gram(residual,residual,weights)
    eden=int(block['residual_denominator'])
    E=np.array([[int(x) for x in row] for row in block['E']],dtype=object)
    assert np.array_equal(ER*eden,E*rden*rden),'E from direct residual'
    assert inertia_fraction(G)==(0,0,block['k'])
    assert inertia_fraction(E)[0]==0
    eta2=F(block['residual_squared_bound'])
    assert inertia_fraction(eta2*eden*G-E)==(0,0,block['k'])
    endpoint_counts=[];b=F(rec['orthogonal_complement_lower'])
    for i,(lo,hi,evlo) in enumerate(zip(block['ritz_lower'],block['ritz_upper'],block['eigen_lower'])):
        il=inertia_fraction(A-den*F(lo)*G);iu=inertia_fraction(A-den*F(hi)*G)
        assert il[0]<=i and iu[0]>=i+1
        t=F(evlo);assert t<b
        sc=inertia_fraction((b-t)*(A-den*t*G)*eden-den*E)
        assert sc[0]<=i and list(sc)==block['schur_inertia_at_lower'][i]
        endpoint_counts.append(dict(ritz_lower=list(il),ritz_upper=list(iu),schur_lower=list(sc)))
    return dict(parity=block['parity'],M=block['M'],k=block['k'],trial_dimension=len(v),
                reached_dimension=len(reached),independent_matrix_denominator=independent_den,
                exact_Gram_A_B_E_equal=True,exact_inertia_passed=True,
                schur_and_ritz_endpoint_counts=endpoint_counts)


def check_local(rec):
    c=rec['relative_form_bound']['local_certificate'];g=F(rec['g']);aa=F(c['a']);bb=F(c['b'])
    w=[2,1,2,1];mat=np.zeros((16,16),dtype=object)
    for col in range(16):
        for i,j,v in KERNEL[col]:mat[4*i+j,col]+=g*v
        mat[col,col]+=aa*((col//4!=0)+(col%4!=0))+bb
    weighted=np.array([[F(mat[i,j])*w[i//4]*w[i%4] for j in range(16)] for i in range(16)],dtype=object)
    assert np.array_equal(weighted,weighted.T)
    counts=inertia_fraction(weighted);assert counts==(0,0,16)
    alpha=F(rec['relative_form_bound']['alpha']);B=F(rec['relative_form_bound']['B']);n=rec['N']
    assert alpha==1-4*aa and B==2*n*bb and 0<alpha<=1
    a=2*alpha-B;r=max(F(x) for bl in rec['blocks'] for x in bl['ritz_upper'])
    e=max(F(bl['residual_squared_bound']) for bl in rec['blocks'])
    s2=min(F(1),e/(a-r)**2);b=a-(a+B)*s2
    assert a>r and b>r
    assert str(a)==rec['global_lambda_kplus1_lower'] and str(-B)==rec['global_ground_lower']
    assert s2==F(rec['sin_angle_squared_upper']) and b==F(rec['orthogonal_complement_lower'])
    assert rec['retained_full_band_dimension']==1+3*n
    assert sum(bl['k']*bl['multiplicity'] for bl in rec['blocks'])==1+3*n
    assert [(bl['parity'],bl['M'],bl['k'],bl['multiplicity']) for bl in rec['blocks']]==[(0,0,1,1),(1,0,n,1),(1,1,n,2)]
    assert rec['full_hilbert_dimension']==4**n and F(rec['energy_shift'])==-F(3*n,4)
    return dict(local_relative_bound_inertia=list(counts),alpha=str(alpha),B=str(B),
                certified_band_dimension=1+3*n,a=str(a),b=str(b),all_scalar_relations_passed=True)


def physical_matrix(nx,ny,magnetization=None):
    n=nx*ny;ns=2*n;g=F(3,100)
    dim=1<<ns
    states=list(range(dim)) if magnetization is None else [s for s in range(dim) if s.bit_count()-n==magnetization]
    lookup={s:i for i,s in enumerate(states)};rr=[];cc=[];vv=[]
    bonds=[(2*i,2*i+1,F(1)) for i in range(n)]
    bonds += [(2*i+layer,2*j+layer,g) for i,j in edges(nx,ny) for layer in range(2)]
    for c,s in enumerate(states):
        diag=F(3*n,4)
        for i,j,coupling in bonds:
            bi=(s>>i)&1;bj=(s>>j)&1
            diag+=coupling*F((2*bi-1)*(2*bj-1),4)
            if bi!=bj:
                rr.append(lookup[s^(1<<i)^(1<<j)]);cc.append(c);vv.append(float(coupling/2))
        rr.append(c);cc.append(c);vv.append(float(diag))
    h=sp.coo_matrix((vv,(rr,cc)),shape=(len(states),len(states))).tocsr()
    return h


def ed_diagnostic(rec):
    nx,ny=rec['nx'],rec['ny'];n=nx*ny;k=1+3*n
    if n==4:
        h=physical_matrix(nx,ny);ev,vec=np.linalg.eigh(h.toarray())
        resid=np.linalg.norm(h@vec-vec*ev,axis=0)
        exact_count=int(np.sum(ev<float(F(rec['global_lambda_kplus1_lower']))))
        los=[];his=[]
        for b in rec['blocks']:
            for lo,hi in zip(b['eigen_lower'],b['eigen_upper']):
                los += [float(F(lo))]*b['multiplicity'];his += [float(F(hi))]*b['multiplicity']
        los.sort();his.sort()
        assert np.all(np.array(los)<=ev[:k]) and np.all(ev[:k]<=np.array(his))
        assert exact_count==k
        # Relative heat trace tested diagnostically only; full exact inequalities are analytic.
        shift=float(F(rec['blocks'][0]['eigen_upper'][0]));alpha=float(F(rec['relative_form_bound']['alpha']));B=float(F(rec['relative_form_bound']['B']))
        trace=[]
        for beta in [0,1,8,10,20,32]:
            low=sum(math.exp(-beta*(e-shift)) for e in his)
            upper=sum(math.exp(-beta*(e-shift)) for e in los)+math.exp(beta*(B+shift))*sum(math.comb(n,j)*3**j*math.exp(-beta*alpha*j) for j in range(2,n+1))
            actual=float(np.exp(-beta*(ev-shift)).sum())
            assert low<=actual+1e-10 and actual<=upper+1e-10
            trace.append(dict(beta=beta,lower=low,physical_ED_trace=actual,upper=upper))
        return dict(kind='full physical-spin ED, diagnostic only',dimension=h.shape[0],
                    maximum_eigenpair_residual=float(max(resid)),certified_interval_containment=True,
                    diagnostic_modes_below_a=exact_count,first_omitted_eigenvalue=float(ev[k]),heat_trace_tests=trace)
    # M=0,1,2 are separately diagnostic. Completeness is analytic, not inferred from these samples.
    out=[]
    for mag in [0,1,2]:
        h=physical_matrix(nx,ny,mag);nev=2*n+4
        ev,vec=sla.eigsh(h,k=nev,which='SA',tol=1e-12,ncv=max(2*nev+1,60),v0=np.random.default_rng(423+mag).normal(size=h.shape[0]))
        order=np.argsort(ev);ev=ev[order];vec=vec[:,order]
        resid=np.linalg.norm(h@vec-vec*ev,axis=0)
        lows=[];highs=[]
        for bl in rec['blocks']:
            if bl['M']==mag:
                lows += list(map(lambda x:float(F(x)),bl['eigen_lower']))
                highs += list(map(lambda x:float(F(x)),bl['eigen_upper']))
        lows.sort();highs.sort();nk=len(lows)
        if nk:assert np.all(np.array(lows)<=ev[:nk]) and np.all(ev[:nk]<=np.array(highs))
        out.append(dict(M=mag,dimension=h.shape[0],checked_low_modes=nk,maximum_eigenpair_residual=float(max(resid)),
                        certified_interval_containment=bool(nk),first_omitted_eigenvalue=float(ev[nk]),eigenvalues=ev.tolist()))
    return dict(kind='physical-spin fixed-Sz ED, diagnostic only',sectors=out)


def main():
    p=argparse.ArgumentParser();p.add_argument('--shapes',default='2x2,4x2,4x4');p.add_argument('--skip-ed',action='store_true');args=p.parse_args()
    result=dict(status='independent_exact_arithmetic_and_analytic_review',arithmetic='independent Fraction symmetric elimination',
                limits=dict(blas_threads=1,cpu_affinity_count=1,address_space_bytes=1024**3),records=[])
    for shape in args.shapes.split(','):
        start=time.monotonic();path=SRC/f'bilayer_{shape}_g3d100_low_band.json';rec=json.loads(path.read_text())
        r=dict(shape=shape,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),local_and_global=check_local(rec),blocks=[])
        for bl in rec['blocks']:
            r['blocks'].append(reconstruct(rec,bl));gc.collect()
            print('EXACT BLOCK PASS',shape,bl['parity'],bl['M'],flush=True)
        if not args.skip_ed and rec['N']<=8:r['ED_diagnostic']=ed_diagnostic(rec)
        r['seconds']=time.monotonic()-start;r['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['records'].append(r)
        (OUT/'independent_results.json').write_text(json.dumps(result,indent=2))
        print('SHAPE PASS',shape,r['seconds'],r['peak_rss_kib'],flush=True)
    result['status']='passed_all_requested_independent_checks'
    (OUT/'independent_results.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
