"""Independent exact spin-1 large-D certificates using sparse product support.
H=sum_i (Sz_i)^2 + g sum_lattice_bonds Si.Sj, periodic multigraph.
Float sparse diagonalization proposes one vector. Integer full-action residual,
exact rational bond positivity, ordered eigenvalue comparison and rational
exponential intervals certify the seed. No full Hilbert diagonalization.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import os,sys,math,itertools,time,json,resource,argparse
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from models import square
BASE=Path(__file__).resolve().parent;OUT=BASE/'results'
sys.path.insert(0,str(BASE.parent/'two_d_theory'))
from three_purity_certificate import exp_interval,down,replay

def sqrt_upper(x,digits=18):
    x=F(x);scale=10**digits
    n=math.isqrt((x.numerator*scale*scale)//x.denominator)
    r=F(n,scale)
    return r if r*r==x else F(n+1,scale)

def bond_parameters(g,a):
    """Exact positivity for g Si.Sj + a(ni+nj)+bI on two spin-1 sites.
    M=±2: 2a+g+b; M=±1: a+b±g. M=0 antisymmetric
    2a-g+b; symmetric 2x2 has diagonal b,2a-g+b and off sqrt2*g.
    """
    g,a=F(g),F(a);d=2*a-g
    b=(sqrt_upper(d*d+8*g*g)-d)/2
    assert b>=0 and a+b-g>=0 and 2*a+g+b>=0 and d+b>=0 and b*(d+b)>=2*g*g
    c=1-4*a
    return a,b,c

def choices(g,N):
    # Rational finite search, only a proposal; every used tuple is checked exactly.
    out=[]
    for j in range(1,500):
        a=F(j,2000)
        if a<F(g):continue
        a,b,c=bond_parameters(g,a)
        if c>0:out.append((a,b,c,2*N*b))
    assert out
    return out

def certify_patch(nx,ny,g,max_excited=2,bits=44):
    g=F(g);N=nx*ny;assert g>0 and max_excited%2==0 and ((N<=16) or (N<=64 and max_excited==2))
    tag=f'largeD_{nx}x{ny}_g{g}_q{max_excited}'.replace('/','d');p=OUT/(tag+'_ground.json')
    if p.exists():return json.loads(p.read_text())
    t0=time.monotonic()
    index=lambda x,y:(x%nx)*ny+y%ny
    edges=[edge for x in range(nx) for y in range(ny) for edge in [(index(x,y),index(x+1,y)),(index(x,y),index(x,y+1))]]
    if N<=16:
        graph=square(1.,nx,ny,periodic_x=True,periodic_y=True)
        assert edges==[(e.i,e.j) for e in graph.edges]
    assert len(edges)==2*N
    states=[(0,)*N]
    for ne in range(2,max_excited+1,2):
        for sites in itertools.combinations(range(N),ne):
            for plus in itertools.combinations(range(ne),ne//2):
                st=[0]*N;pp=set(plus)
                for i,pos in enumerate(sites):st[pos]=1 if i in pp else -1
                states.append(tuple(st))
    lookup={st:i for i,st in enumerate(states)};output=dict(lookup);outstates=list(states)
    den=g.denominator;gg=g.numerator;rr=[];cc=[];vv=[]
    for col,st in enumerate(states):
        acc=defaultdict(int);acc[st]+=den*sum(x*x for x in st)+gg*sum(st[i]*st[j] for i,j in edges)
        for i,j in edges:
            for sign in [1,-1]:
                if -1<=st[i]+sign<=1 and -1<=st[j]-sign<=1:
                    dest=list(st);dest[i]+=sign;dest[j]-=sign;acc[tuple(dest)]+=gg
        for dest,value in acc.items():
            if not value:continue
            if dest not in output:output[dest]=len(outstates);outstates.append(dest)
            rr.append(output[dest]);cc.append(col);vv.append(value)
    A=sp.coo_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(len(outstates),len(states))).tocsr();A.sum_duplicates();A.eliminate_zeros()
    trial=A[:len(states)];assert (trial-trial.T).nnz==0
    build=time.monotonic()
    e,v=eigsh(trial.astype(float)/den,k=1,which='SA',tol=3e-14,v0=np.random.default_rng(271828).normal(size=len(states)))
    integers=[int(round(float(x)*2**bits)) for x in v[:,0]]
    norm=sum(x*x for x in integers)
    Hv=[sum(int(A.data[j])*integers[int(A.indices[j])] for j in range(A.indptr[i],A.indptr[i+1])) for i in range(A.shape[0])]
    rho=F(sum(x*y for x,y in zip(integers,Hv)),den*norm)
    res2=F(sum(y*y for y in Hv),den*den*norm)-rho*rho
    opts=choices(g,N);a,b,c,B=max(opts,key=lambda x:x[2]-x[3]);nextlo=c-B
    assert res2>=0 and rho<nextlo
    elo=rho-res2/(nextlo-rho)
    out=dict(model='spin1_large_D_square',nx=nx,ny=ny,N=N,g=str(g),D='1',periodic='both axes; length-two lattice multibonds',full_dimension=3**N,trial_dimension=len(states),reached_dimension=len(outstates),max_excited=max_excited,integer_denominator=den,sparse_nnz=A.nnz,dyadic_bits=bits,exact_rayleigh=str(rho),exact_residual_squared=str(res2),ground_lower=str(elo),ground_upper=str(rho),ground_lower_display=float(elo),ground_upper_display=float(rho),ground_width_display=float(rho-elo),second_eigenvalue_lower=str(nextlo),comparison={'a':str(a),'b':str(b),'c':str(c),'B':str(B)},ground_unique_certified=True,proof='Exact bond PSD implies H >= c H0-BI; ordered second eigenvalue >= c-B. rho<c-B isolates unique ground. Full-action exact residual and Temple enclose it.',full_spectrum_used=False,build_seconds=build-t0,total_seconds=time.monotonic()-t0,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    artifact=OUT/(tag+'_trial.npz');np.savez_compressed(artifact,basis=np.array(states,dtype=np.int8),vector=np.array(integers,dtype=np.int64),bits=bits)
    out['trial_artifact']=artifact.name;p.write_text(json.dumps(out,indent=2));print('GROUND',tag,out['ground_lower_display'],out['ground_upper_display'],len(states),len(outstates),out['total_seconds'],flush=True)
    return out

def q_interval(rec,beta):
    beta=F(beta);N=rec['N'];g=F(rec['g']);elo=F(rec['ground_lower']);ehi=F(rec['ground_upper'])
    def estimate(p):
        a,b,c,B=p;x=math.exp(-float(beta*c))
        return float(beta*(B+ehi))+math.log(math.expm1(N*math.log1p(2*x)))
    a,b,c,B=min(choices(g,N),key=estimate)
    tail=exp_interval(beta*(B+ehi))[1]*((1+2*exp_interval(-beta*c)[1])**N-1)
    ground=exp_interval(beta*(ehi-elo))[1]
    return F(1),ground+tail,dict(a=str(a),b=str(b),c=str(c),B=str(B),tail_upper=str(down(tail+F(1,10**18))),tail_display=float(tail))

def seed(recs,beta):
    beta=F(beta);a,b,c=recs
    assert b['nx']==2*a['nx'] and b['ny']==a['ny'] and c['nx']==b['nx'] and c['ny']==2*b['ny']
    qa=q_interval(a,beta);qb=q_interval(b,beta);qc=q_interval(c,beta)
    ea,eb,ec=[F(r['ground_upper']) for r in recs]
    A=down(exp_interval(-beta*(eb-2*ea))[0]/qa[1]**2)
    B=down(exp_interval(-beta*(ec-2*eb))[0]/qb[1]**2)
    C=down(1/qc[1]**2)
    boot=replay(A,B,C,n=a['nx'],m=a['ny'],beta=beta) if min(A,B,C)>0 and max(A,B,C)<=1 else {'status':'outside_purity_domain'}
    return dict(beta=str(beta),purity_lowers=list(map(str,(A,B,C))),purity_lower_displays=list(map(float,(A,B,C))),tail_comparisons=[qa[2],qb[2],qc[2]],bootstrap=boot)

def main():
    p=argparse.ArgumentParser();p.add_argument('--g',default='1/100');p.add_argument('--max-excited',type=int,default=2);p.add_argument('--betas',default='8,10,12,14,16,20,24');p.add_argument('--base-size',type=int,default=2);args=p.parse_args();g=F(args.g);n=args.base_size
    recs=[certify_patch(nx,ny,g,args.max_excited) for nx,ny in [(n,n),(2*n,n),(2*n,2*n)]]
    seeds=[]
    for beta in args.betas.split(','):
        rec=seed(recs,F(beta));seeds.append(rec);print('SEED',beta,rec['purity_lower_displays'],rec['bootstrap']['status'],rec['bootstrap'].get('uniform_square_gap_lower_display'),flush=True)
    out=dict(model='spin1_large_D_square',g=str(g),D='1',ground_certificates=recs,seeds=seeds)
    (OUT/((f'largeD_g{g}_q{args.max_excited}'+('' if n==2 else f'_n{n}')+'_certificate.json').replace('/','d'))).write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
