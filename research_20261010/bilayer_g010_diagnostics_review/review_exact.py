"""Independent rational reconstruction; imports no producer code. Writes only supplied output."""
import os,sys,resource,json,hashlib,time,math
from pathlib import Path
from fractions import Fraction as Q
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
sys.dont_write_bytecode=True
cpu=os.sched_getaffinity(0);os.sched_setaffinity(0,{7 if 7 in cpu else min(cpu)})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));resource.setrlimit(resource.RLIMIT_CPU,(300,300))
import numpy as np
ROOT=Path(__file__).resolve().parent.parent;SRC=ROOT/'bilayer_g010_diagnostics'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mat(x):return np.array([[Q(a) for a in r] for r in x],dtype=object)
def zero(n,m):return np.full((n,m),Q(0),dtype=object)
def eye(n):return np.array([[Q(i==j) for j in range(n)] for i in range(n)],dtype=object)
def same(a,b):assert a.shape==b.shape and (a==b).all()
def pd(A):
    # Rational symmetric Schur complements, independent of producer Bareiss.
    same(A,A.T);S=A.copy();p=[]
    for k in range(len(A)):
        d=S[k,k];assert d>0,(k,str(d));p.append(str(d))
        for i in range(k+1,len(A)):
            for j in range(i,len(A)):
                S[i,j]=S[j,i]=S[i,j]-S[i,k]*S[k,j]/d
    return dict(dimension=len(A),all_rational_LDL_pivots_positive=True,pivot_sha256=hashlib.sha256(json.dumps(p).encode()).hexdigest())
def run():
    start=time.monotonic();assert sha(SRC/'FROZEN_MANIFEST.json')=='64aef0cf10637f509afd325ab230f8a74a97775b961657d1c5962e6c61be04bb'
    frozen=read(SRC/'FROZEN_MANIFEST.json')['files']
    for p,h in frozen.items():assert sha(SRC/p)==h,p
    for p,h in read(SRC/'INPUT_SHA256.json').items():assert sha(ROOT/p)==h,p
    inherited=0
    for s in read(SRC/'INHERITED_SEALS.json'):
        p=ROOT/s['path'];assert sha(p)==s['sha256'];m=read(p);files=m.get('files',m);assert len(files)==s['verified_files']
        for rel,h in files.items():assert sha(p.parent/rel)==h,(p,rel)
        inherited+=len(files)
    rows=[]
    for shape in ['4x4','8x4','8x8']:
        r=read(SRC/f'weighted_ground_{shape}.json');ex=read(SRC/f'moments_{shape}.json')
        for p,h in r['sources'].items():assert sha(ROOT/p)==h
        gr=read(ROOT/next(p for p in r['sources'] if '/block1_' in p));geom=read(ROOT/next(p for p in r['sources'] if '/geometry_' in p));patch=read(ROOT/next(p for p in r['sources'] if '/patch_' in p))
        for rel in r['sources']:
            if '/block1_' in rel or '/patch_' in rel:assert sha(ROOT/rel)==sha(ROOT/'combined_ground_review/snapshot/research_20261010'/rel)
            if '/geometry_' in rel:assert sha(ROOT/rel)==sha(ROOT/'third_moment_review/snapshot/producer'/Path(rel).name)
        n=geom['pair_orbits'];b=n+1;d=gr['integer_matrix_denominator'];g=Q(gr['coupling']);h=g*d/2;N=gr['nx']*gr['ny']
        ms=[mat(x) for x in gr['shifted_integer_moments_M0_to_M4']];gb=ms[0];hb=ms[1]
        FF,SS,VV,WW,XX,YY,ZZ=[mat(geom[k]) for k in ['F','S','V','W','X','Y','Z']]
        fe=np.vstack([zero(1,n),FF]);se=np.vstack([zero(1,n),SS]);C=np.array([[hb[i,j]/gb[i,i] for j in range(b)] for i in range(b)],dtype=object)
        D=np.array([[h*fe[i,j]/gb[i,i] for j in range(n)] for i in range(b)],dtype=object);E=np.column_stack([zero(n,1),eye(n)])
        GG=np.block([[gb,zero(b,n),zero(b,n)],[zero(n,b),FF,SS],[zero(n,b),SS,VV+WW]])
        KK=np.block([[hb,h*fe,h*se],[h*fe.T,4*d*FF+h*SS,4*d*SS+h*(VV+WW)],[h*se.T,4*d*SS+h*(VV+WW),4*d*VV+6*d*WW+h*(XX+YY+YY.T+ZZ)]])
        powers=[np.vstack([eye(b),zero(2*n,b)]),np.vstack([C,h*E,zero(n,b)]),np.vstack([C@C+h*D@E,h*E@C+4*d*h*E,h*h*E])]
        for i in range(3):
            for j in range(3):
                same(powers[i].T@GG@powers[j],ms[i+j])
                if i+j<4:same(powers[i].T@KK@powers[j],ms[i+j+1])
        M5=powers[2].T@KK@powers[2];same(M5,mat(ex['integer_M5']));ms.append(M5)
        # Raw W=(base, centered-H pair) from moments, then quotient dependencies.
        R=zero(2*b,2*b-1);R[:b,:b]=eye(b)
        R[:b,b:]=-C[:,1:]/h;R[b+1:,b:]=eye(n)/h
        ids=gr['selected_basis_indices'];R=R[:,ids]
        moments=[]
        for k in range(4):
            z=R.T@np.block([[ms[k],ms[k+1]],[ms[k+1],ms[k+2]]])@R/Q(d**k)
            same(z,mat(ex['moments_G_A_B_C'][k]));moments.append(z)
            if k<3:same(z,mat(gr[['gram','shifted_hamiltonian_numerator','shifted_H2_numerator'][k]])/Q(d**k))
        G,A,B,C3=moments;gram=pd(G);c=np.array(list(map(Q,r['coefficients'])),dtype=object);v=[c@M@c for M in moments]
        assert list(map(str,v))==r['quadratic_moments_0_to_3']
        a,l,U,L=map(Q,[r['a'],r['lower'],r['U'],r['old_lower']]);assert U==N*(1+g) and L<l<a
        pol=lambda ell: -C3+(U+a+ell)*B-(U*(a+ell)+a*ell)*A+U*a*ell*G
        val=c@pol(l)@c;assert val==Q(r['negative_polynomial_witness'])<0
        ahi=l+Q(1,10**10);P=B-(a+ahi)*A+a*ahi*G;T=C3-(a+ahi)*B+a*ahi*A
        upper=pd(U*P-T);lower=pd(T-L*P)
        assert c@pol(ahi)@c>0 # Adversarial endpoint overshoot rejected.
        assert a==Q(patch['global_lambda_kplus1_lower']) and L==Q(patch['blocks'][0]['eigen_lower'][0])
        a1=Q(patch['all_excited_global_lower']);ray=Q(gr['exact_rayleigh'])-Q(gr['E00'])
        bins=patch['number_sector_bins']['bins'];assert len(bins)==N+1
        offset=1
        for q,entry in enumerate(bins):
            assert entry['q']==q and entry['multiplicity']==math.comb(3*N+q-1,q) and entry['first_ordered_index']==offset
            offset+=entry['multiplicity']
        assert offset>=2**(2*N)+1 and bins[2]['first_ordered_index']==2+3*N
        assert Q(bins[1]['lower'])==a1 and Q(bins[2]['lower'])==a
        odd=patch['blocks'][1];assert len(odd['eigen_upper'])==N and odd['multiplicity']==3
        assert ray<a1<a and max(map(Q,odd['eigen_upper']))<a
        assert patch['retained_full_band_dimension']==1+3*N and patch['full_hilbert_dimension']==2**(2*N)
        new=read(SRC/f'patch_{shape}_g1d10.json');del new['weighted_ground_witness'];new['blocks'][0]['eigen_lower']=patch['blocks'][0]['eigen_lower'];assert new==patch
        # Kernel of [B,HB] is covered by selected W (rank of full Gram equals selected dimension).
        fullH=np.block([[ms[0],ms[1]],[ms[1],ms[2]]]);fullW=zero(2*b,2*b-1);fullW[:b,:b]=eye(b);fullW[:b,b:]=-np.array([[ms[1][i,j]/ms[0][i,i] for j in range(1,b)] for i in range(b)],dtype=object)/h;fullW[b+1:,b:]=eye(n)/h
        # Projection residual zero proves every base/Hbase vector is in selected span.
        gramInv=solve(G,eye(len(G)));overlap=R.T@fullH;same(fullH,overlap.T@gramInv@overlap)
        rows.append(dict(shape=shape,N=N,full_dimension=str(2**(2*N)),trial_dimension=len(G),lower=str(l),old_lower=str(L),improvement=str(l-L),negative_witness=str(val),a=str(a),a1=str(a1),max_odd_upper=str(max(map(Q,odd['eigen_upper']))),rayleigh=str(ray),bracket_upper=str(ahi),gram=gram,upper_weight=upper,lower_weight=lower,all_moment_geometry_and_Hankel_checks=True,complete_affine_base_span=True,odd_count_and_unique_ground_conditions=True,unchanged_patch_other_fields=True))
    num=read(ROOT/'low_band/third_moment_exact/enlarged_8x8_g1d10.json');G=mat(num['gram']);A=mat(num['shifted_H_numerator'])/Q(num['integer_matrix_denominator']);rho=Q(num['shifted_rayleigh_upper']);c=np.array(list(map(Q,num['coefficients'])),dtype=object)
    assert len(G)==43 and (c@A@c)/(c@G@c)==rho
    numcheck=pd(A-(rho-Q(1,10**10))*G);pd(G)
    # Sign and scope adversaries: without even-sector restriction, an excited eigenvalue fools test.
    l,a,U=Q(0),Q(2),Q(4);P=lambda e:(U-e)*(e-a)*(e-l)
    assert all(P(e)>=0 for e in [-1,0,2,3,4]) and P(Q(1))<0
    assert P(5)<0 # Upper support is essential as well.
    for p,h in frozen.items():assert sha(SRC/p)==h,p
    return dict(status='PASS_exact_endpoints_restricted_class_and_numerator_brackets',source_manifest_sha256=sha(SRC/'FROZEN_MANIFEST.json'),source_files=len(frozen),inherited_sealed_files=inherited,results=rows,numerator=dict(dimension=43,lower=str(rho-Q(1,10**10)),upper=str(rho),positive_definite=numcheck,physical_ground_lower=False),adversarial_tests=['endpoint overshoot has positive saved-vector value','extra level below a defeats unrestricted global inference','spectrum above U defeats sign theorem','full affine-base-span exact projection checked','patch changes restricted to ground lower and witness'],cpu_affinity=sorted(os.sched_getaffinity(0)),peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,seconds=time.monotonic()-start)
def solve(A,B):
    a=A.copy();b=B.copy();n=len(a)
    for k in range(n):
        p=a[k,k];assert p!=0;a[k,:]/=p;b[k,:]/=p
        for i in range(n):
            if i!=k:
                f=a[i,k];a[i,:]-=f*a[k,:];b[i,:]-=f*b[k,:]
    return b
if __name__=='__main__':
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('exact_result.json');r=run();out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='results'},indent=2))
