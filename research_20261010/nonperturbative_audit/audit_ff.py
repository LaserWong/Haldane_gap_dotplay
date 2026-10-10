"""Independent fully-frustrated perturbation audit; no producer imports.
Rebuilds local physical-spin operators, multigraph, occupancy spectra majorant,
full sparse residual and PSD certificate. Scalar enclosures use a distinct
192-bit, 56-term rational Taylor implementation; recursion uses stored 128-bit
rounding and is checked exactly. All file writes are confined to this directory.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[name]='1'
from fractions import Fraction as F
from collections import defaultdict,Counter
from pathlib import Path
from functools import lru_cache
import itertools,math,json,hashlib,time,sys,resource
import numpy as np
BASE=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
V=((0,-1,1,0),(1,0,0,0),(0,1,1,0),(0,0,0,1));W=(2,1,2,1)

def phys_exchange(n,i,j):
    h=[[F(0) for _ in range(1<<n)] for _ in range(1<<n)]
    for c in range(1<<n):
        a=(c>>(n-1-i))&1;b=(c>>(n-1-j))&1
        h[c][c]=F((2*a-1)*(2*b-1),4)
        if a!=b:h[c^(1<<(n-1-i))^(1<<(n-1-j))][c]=F(1,2)
    return h

def pair_kernels():
    cols=[tuple(V[p][i]*V[q][j] for i in range(4) for j in range(4)) for p in range(4) for q in range(4)]
    kernels={}
    for a,b in itertools.product(range(2),repeat=2):
        h=phys_exchange(4,a,2+b);out={}
        for c in range(16):
            hv=[sum(h[i][j]*cols[c][j] for j in range(16)) for i in range(16)]
            out[c//4,c%4]=[(r//4,r%4,x) for r in range(16) if (x:=sum(cols[r][i]*hv[i] for i in range(16))/ (W[r//4]*W[r%4]))]
        kernels[a,b]=out
    return kernels
K=pair_kernels()

def oriented_edges(nx,ny):
    N=nx*ny
    return [(i,((i//ny+1)%nx)*ny+i%ny) for i in range(N)]+[(i,(i//ny)*ny+(i%ny+1)%ny) for i in range(N)]

def multigraph(nx,ny):return Counter(tuple(sorted(edge)) for edge in oriented_edges(nx,ny))

def graph(nx,ny,J,eps):
    return Counter({(i,a,j,b):w*(J+(eps if a==b else 0)) for (i,j),w in multigraph(nx,ny).items() for a,b in itertools.product(range(2),repeat=2)})

@lru_cache(maxsize=30)
def occupancy(nx,ny,J):
    N=nx*ny;edges=multigraph(nx,ny);hist=Counter()
    assert sum(edges.values())==2*N
    for i in range(N):assert sum(w for (u,v),w in edges.items() if i in (u,v))==4
    for q in range(N+1):
        for active in itertools.combinations(range(N),q):
            active=set(active);incident={i:0 for i in active};weight=0
            for (i,j),w in edges.items():
                if i in active and j in active:
                    weight+=w;incident[i]=max(incident[i],w);incident[j]=max(incident[j],w)
            e=q-J*(weight+F(sum(incident.values()),2));hist[q,e]+=3**q
    assert sum(hist.values())==4**N
    for q in range(N+1):assert sum(v for (k,e),v in hist.items() if k==q)==math.comb(N,q)*3**q
    return hist

def local_psd(a,b,eps):
    # Independent physical-spin basis in order rung0layer0, rung0layer1,
    # rung1layer0, rung1layer1. Strict rational LDL needs no pivoting.
    h00=phys_exchange(4,0,1);h11=phys_exchange(4,2,3)
    v0=phys_exchange(4,0,2);v1=phys_exchange(4,1,3)
    A=[[eps*(v0[i][j]+v1[i][j])+a*(h00[i][j]+h11[i][j])+((F(3,2)*a+b) if i==j else 0) for j in range(16)] for i in range(16)]
    pivots=[]
    for k in range(16):
        p=A[k][k];assert p>0,(k,p);pivots.append(p)
        for i in range(k+1,16):
            for j in range(i,16):A[j][i]=A[i][j]=A[i][j]-A[i][k]*A[k][j]/p
    return {'exact_positive_LDL_pivots':list(map(str,pivots)),'inertia':[0,0,16]}

def ground(r,artifact_root,J,eps,physical=False):
    t=time.monotonic();nx=r['nx'];ny=r['ny'];N=nx*ny
    assert r['s']=='1/2' and r['N_dimers']==N and r['physical_sites']==2*N and r['full_dimension']==4**N
    edges=graph(nx,ny,J,eps);stored=Counter()
    for i,a,j,b,c in r['weak_bonds']:stored[i,a,j,b]+=F(c)
    assert stored==edges
    ref=r['reference_certificate'];hist=occupancy(nx,ny,J)
    assert hist==Counter({(row['q'],F(row['energy_lower'])):row['multiplicity'] for row in ref['bins']})
    a=F(ref['a']);b=F(ref['b']);B=2*N*b
    assert B==F(ref['B']) and a>=0
    psd=local_psd(a,b,eps)
    lowest=min(e-4*a*q for q,e in hist if q)
    assert lowest>0 and hist[0,F(0)]==1
    threshold=lowest-B
    assert threshold==F(ref['second_shift_lower'])
    p=artifact_root/r['trial_artifact'];z=np.load(p,allow_pickle=False)
    basis=[tuple(map(int,st)) for st in z['basis']];vec=list(map(int,z['vector']))
    assert len(basis)==len(vec)==r['trial_subspace_dimension']==len(set(basis))
    assert all(len(st)==N and set(st)<={0,1,2,3} for st in basis)
    assert all(sum((0,-1,0,1)[s] for s in st)==0 for st in basis)
    assert max(sum(s!=0 for s in st) for st in basis)==r['trial_max_excited_dimers']
    E00=-F(3*N,4);scale=math.lcm(4,*[v.denominator*x.denominator for key,v in edges.items() for row in K[key[1],key[3]].values() for _,_,x in row])
    # The map includes every nonzero output of each input column, even for zero
    # input amplitudes; the numerical residual includes every actual H psi entry.
    multiply=defaultdict(int);reached=set(basis);nnz=0
    for st,v in zip(basis,vec):
        col=defaultdict(int);col[st]=int(scale*(E00+sum(s!=0 for s in st)))
        for (i,aa,j,bb),c in edges.items():
            for si,sj,x in K[aa,bb][st[i],st[j]]:
                coeff=scale*c*x;assert coeff.denominator==1
                out=list(st);out[i]=si;out[j]=sj;col[tuple(out)]+=int(coeff)
        for out,x in col.items():
            if x:reached.add(out);nnz+=1;multiply[out]+=x*v
    metric=lambda st:math.prod(W[s] for s in st)
    norm=sum(metric(st)*v*v for st,v in zip(basis,vec));num=sum(metric(st)*v*multiply[st] for st,v in zip(basis,vec))
    rho=F(num,scale*norm);r2=F(sum(metric(st)*v*v for st,v in multiply.items()),scale*scale*norm)-rho*rho
    assert rho==F(r['exact_rayleigh']) and r2==F(r['exact_residual_squared']) and r2>=0
    assert len(reached)==r['reached_support_dimension'] and nnz==r['sparse_nnz']
    assert F(r['E00'])==E00 and F(r['Vmin'])==-F(3,4)*sum(edges.values()) and F(r['Vmax'])==F(1,4)*sum(edges.values())
    alpha=E00+threshold;assert alpha==F(r['second_eigenvalue_lower']) and rho<alpha
    lo=rho-r2/(alpha-rho);assert lo==F(r['ground_lower']) and rho==F(r['ground_upper'])
    physical_check=None
    if physical:
        vp=defaultdict(int)
        for st,v in zip(basis,vec):
            if not v:continue
            support=[[(j,x) for j,x in enumerate(V[s]) if x] for s in st]
            for row in itertools.product(*support):
                index=0;value=v
                for j,x in row:index=4*index+j;value*=x
                vp[index]+=value
        hp=defaultdict(int)
        bonds=[(2*i,2*i+1,F(1)) for i in range(N)]+[(2*i+aa,2*j+bb,c) for (i,aa,j,bb),c in edges.items()]
        for st,v in vp.items():
            for i,j,c in bonds:
                bi=1<<(2*N-1-i);bj=1<<(2*N-1-j);up_i=bool(st&bi);up_j=bool(st&bj)
                diag=scale*c*(F(1,4) if up_i==up_j else -F(1,4));assert diag.denominator==1;hp[st]+=int(diag)*v
                if up_i!=up_j:
                    flip=scale*c/2;assert flip.denominator==1;hp[st^bi^bj]+=int(flip)*v
        n=sum(v*v for v in vp.values());p_rho=F(sum(v*hp[st] for st,v in vp.items()),scale*n);p_r2=F(sum(v*v for v in hp.values()),scale*scale*n)-p_rho*p_rho
        assert n==norm and p_rho==rho and p_r2==r2
        physical_check={'exact_physical_basis_Rayleigh_and_full_residual_match':True,'vector_support':sum(v!=0 for v in vp.values()),'H_vector_support':sum(v!=0 for v in hp.values())}
    return {'geometry':[nx,ny],'full_dimension':4**N,'trial_dimension':len(basis),'reached_dimension':len(reached),'matrix_nnz':nnz,'occupied_subsets':2**N,'reference_bins':len(hist),'reference_total_rank':sum(hist.values()),'lowest_nonvacuum_reference_before_B':str(lowest),'second_shift_lower':str(threshold),'ground_width':str(rho-lo),'local_PSD':psd,'exact_sparse_Rayleigh_residual_Temple_match':True,'physical_basis_check':physical_check,'artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'seconds':time.monotonic()-t}

def floor_bits(x,bits=128):x=F(x);return F((x.numerator<<bits)//x.denominator,1<<bits)
def ceil_bits(x,bits=192):return -floor_bits(-F(x),bits)
@lru_cache(maxsize=10000)
def exp192(x):
    x=F(x)
    if x<0:
        lo,hi=exp192(-x);return floor_bits(1/hi,192),ceil_bits(1/lo)
    folds=0
    while x>F(1,4):x/=2;folds+=1
    term=F(1);low=F(1)
    for k in range(1,57):term*=x/k;low+=term
    tail=(term*x/57)/(1-x/58)
    lo=floor_bits(low,192);hi=ceil_bits(low+tail)
    for _ in range(folds):lo=floor_bits(lo*lo,192);hi=ceil_bits(hi*hi)
    return lo,hi

def q_upper(r,beta):
    ref=r['reference_certificate'];a=F(ref['a']);B=F(ref['B']);hi=F(r['ground_upper']);lo=F(r['ground_lower']);E00=F(r['E00'])
    tail=F(0)
    for row in ref['bins']:
        if row['q']:tail+=row['multiplicity']*exp192(-beta*(E00+F(row['energy_lower'])-4*a*row['q']-B-hi))[1]
    return exp192(beta*(hi-lo))[1]+tail,tail

def G(x):assert 0<x<=1;return 1-(1-x)**2/(2*x*x)

def seed_check(records,seed):
    beta=F(seed['beta']);U=[F(r['ground_upper']) for r in records];qs=[q_upper(r,beta)[0] for r in records]
    valid={'A':exp192(-beta*(U[1]-2*U[0]))[0]/qs[0]**2,'B':exp192(-beta*(U[2]-2*U[1]))[0]/qs[1]**2,'C':1/qs[2]**2,'J1':exp192(-beta*(2*U[2]-8*U[0]))[0]/qs[0]**8,'J2':exp192(-beta*(4*U[2]-8*U[1]))[0]/qs[1]**8}
    for key,value in valid.items():assert 0<F(seed[key+'_lower'])<=value<=1,(key,beta)
    A1=floor_bits(G(F(seed['J1_lower'])));b=seed['bootstrap'];accepted=False;rounds=0;n=4;bb=2*beta
    if A1<=0:assert b=={'accepted':False,'failure':'first spatial update'}
    else:
        B1=floor_bits(G(F(seed['J2_lower'])*A1))
        if B1<=0:assert b=={'accepted':False,'failure':'second spatial update'}
        else:
            C1=floor_bits(G(F(seed['C_lower'])**4*A1*A1*B1))
            if C1<=0:assert b=={'accepted':False,'failure':'thermal update'}
            else:
                A,B,C=A1,B1,C1;updates=[]
                for rounds in range(65):
                    u=max(1-A,1-B,1-C)
                    if u<=F(1,500):accepted=True;break
                    failed=False
                    for _ in range(3):
                        new=floor_bits(G(A**4*B**2*C))
                        if new<=0:failed=True;break
                        A,B,C=B,C,new
                    if failed:break
                    n*=2;bb*=2;updates.append(list(map(str,[A,B,C])))
                assert accepted==b['accepted']
                if accepted:
                    assert n==b['n']==b['m'] and bb==F(b['beta']) and rounds==b['rounds'] and u==F(b['u']) and updates==b['updates']
                    assert list(map(str,[A,B,C]))==b['purities']
                    gap=F(b['gap_lower']);assert exp192(bb*gap)[1]<1/(32*u)
    return {'beta':str(beta),'accepted':b['accepted'],'independent_192bit_heat_inputs_valid':True,'exact_128bit_recursion_matches':True,'n':b.get('n'),'gap_lower':b.get('gap_lower'),'gap_display':float(F(b['gap_lower'])) if b.get('gap_lower') else None}

def audit(path,artifact_root=None,physical=False,output=None):
    t=time.monotonic();data=json.loads(path.read_text());J=F(data['J']);eps=F(data['epsilon']);assert J==F(3,10) and eps>=0
    root=artifact_root or path.parent
    checks=[ground(r,root,J,eps,physical=physical and r['N_dimers']<=8) for r in data['ground_certificates']]
    seeds=[seed_check(data['ground_certificates'],s) for s in data['seeds']]
    accepted=[s for s in seeds if s['accepted']]
    bridges=[]
    for s in accepted:
        values=[(L,(F(2,5) if L==2 else F(1))-3*L*L*eps) for L in range(2,s['n'])]
        bound=min((v for L,v in values),default=F(10**6));gap=F(s['gap_lower']);all_gap=min(gap,bound)
        bridges.append({'beta':s['beta'],'bootstrap_n':s['n'],'finite_bridge':[[L,str(v)] for L,v in values],'smallest_bridge':str(bound),'all_integer_L_ge2_gap':str(all_gap) if all_gap>0 else None,'all_integer_L_ge2_gap_display':float(all_gap) if all_gap>0 else None})
    best=max((r for r in bridges if r['all_integer_L_ge2_gap']),key=lambda r:F(r['all_integer_L_ge2_gap']),default=None)
    result={'status':'PASS independent graph, weighted-star counts, physical local PSD, full residual, minmax/Temple, thermal inputs and recursion','source':str(path.relative_to(BASE)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'J':str(J),'epsilon':str(eps),'ground_checks':checks,'seed_checks':seeds,'bridge_checks':bridges,'best_all_sizes':best,'seconds':time.monotonic()-t,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if output is None:output=OUT/(path.stem+'_audit.json')
    output.write_text(json.dumps(result,indent=2));print(json.dumps({'status':result['status'],'epsilon':str(eps),'best_all_sizes':best,'seconds':result['seconds'],'peak_rss_kib':result['peak_rss_kib']}),flush=True)
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('path',nargs='?',type=Path,default=BASE/'low_energy/ff_seed_J3d10_eps1d200_depth0.json');p.add_argument('--physical',action='store_true');a=p.parse_args();audit(a.path,physical=a.physical)
