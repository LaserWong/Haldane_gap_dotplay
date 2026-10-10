"""Exact Gram certificates for the full ground-plus-one-triplet band.
All eigensolvers are proposal generators. Exact integer inertia accepts every
spectral/residual endpoint. The rectangular H map retains every leaked state.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'low_energy'))
sys.path.insert(0,str(ROOT/'original/Haldane_extensions/code'))
sys.path.insert(0,str(ROOT/'two_d_theory'))
import math,json,time,itertools,resource,argparse,hashlib
from collections import defaultdict
from fractions import Fraction as F
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigvalsh,eigh
from dimer_subspace import dimer_local,bilayer_bonds
from local_relative_bound import local_bound
from inertia_trace import inertia
from analytic_certificates import exp_bounds,down
from three_purity_certificate import replay
OUT=Path(__file__).resolve().parent

def matrix_integer(A):
    A=np.asarray(A,dtype=object)
    den=math.lcm(*(F(x).denominator for x in A.flat))
    return np.array([[int(F(x)*den) for x in row] for row in A],dtype=object),den

def exact_inertia(A):
    A,_=matrix_integer(A)
    assert np.array_equal(A,A.T)
    neg,zero=inertia(A)
    return neg,zero,len(A)-neg-zero

def pd(A):
    n,z,p=exact_inertia(A)
    return p==len(A)

def upper_round(x,digits=11):
    scale=10**digits
    return F(math.ceil(float(x)*scale)+4,scale)

def lower_round(x,digits=11):
    scale=10**digits
    return F(math.floor(float(x)*scale)-4,scale)

def optimize_tail_bound(g,N,q=2,grid=200):
    labels,weights,kernels=dimer_local(F(1,2));D=16
    G=np.array([weights[i]*weights[j] for i in range(4) for j in range(4)])
    diag=np.array([float(labels[i][2]+labels[j][2]) for i in range(4) for j in range(4)])
    v=np.zeros((D,D))
    for c in range(D):
        for ab in [(0,0),(1,1)]:
            for p,t,x in kernels[ab][c]:v[p*4+t,c]+=float(g*x)*math.sqrt(G[p*4+t]/G[c])
    candidates=[]
    for ai in range(1,grid):
        al=F(ai,4*grid)
        b=max(0,-eigvalsh(v+float(al)*np.diag(diag),subset_by_index=[0,0])[0])
        candidates.append((q*(1-4*float(al))-2*N*b,al))
    _,al=max(candidates)
    local=local_bound(F(1,2),g,al,'bilayer',digits=13)
    return dict(alpha=str(1-4*al),B=str(2*N*F(local['b'])),local_certificate=local,q_optimized=q)

def make_map(nx,ny,g,parity,M,qmax):
    assert nx>=2 and ny>=2 and g>=0
    N=nx*ny;labels,localw,kernels=dimer_local(F(1,2))
    basis=[]
    for nexc in range(parity,qmax+1,2):
        for sites in itertools.combinations(range(N),nexc):
            for vals in itertools.product(range(1,4),repeat=nexc):
                if sum(labels[v][1] for v in vals)!=M:continue
                st=[0]*N
                for i,v in zip(sites,vals):st[i]=v
                basis.append(tuple(st))
    weights=lambda st:math.prod(localw[x] for x in st)
    weak=bilayer_bonds(nx,ny,g,g)
    coeffs=[g*c for _,aa,_,bb,g in weak for row in kernels[aa,bb] for _,_,c in row]
    den=math.lcm(*(x.denominator for x in coeffs))
    ik={}
    for aa,bb,coupling in set((aa,bb,coupling) for _,aa,_,bb,coupling in weak):
        ik[aa,bb,coupling]=[[(p,q,int(c*coupling*den)) for p,q,c in row] for row in kernels[aa,bb]]
    reached=list(basis);lookup={st:i for i,st in enumerate(reached)}
    rows=[];cols=[];values=[]
    for col,st in enumerate(basis):
        acc=defaultdict(int);acc[st]+=sum(v!=0 for v in st)*den
        for i,aa,j,bb,coupling in weak:
            for p,q,value in ik[aa,bb,coupling][st[i]*4+st[j]]:
                new=list(st);new[i]=p;new[j]=q;acc[tuple(new)]+=value
        for new,value in acc.items():
            if not value:continue
            assert sum(v!=0 for v in new)%2==parity
            assert sum(labels[v][1] for v in new)==M
            if new not in lookup:lookup[new]=len(reached);reached.append(new)
            rows.append(lookup[new]);cols.append(col);values.append(value)
    Arect=sp.coo_matrix((np.array(values,dtype=np.int64),(rows,cols)),shape=(len(reached),len(basis))).tocsr()
    Arect.sum_duplicates();Arect.eliminate_zeros()
    w=np.array([weights(st) for st in reached],dtype=np.int64)
    sq=np.sqrt(w[:len(basis)].astype(float))
    H=sp.diags(sq)@(Arect[:len(basis)].astype(float)/den)@sp.diags(1/sq)
    assert np.max(np.abs((H-H.T).data),initial=0)<1e-12
    return basis,Arect,den,w,H

def exact_apply(A,V):
    """Python integer accumulation, no int64 overflow. V is an integer matrix."""
    out=np.zeros((A.shape[0],V.shape[1]),dtype=object)
    Vo=np.asarray(V,dtype=object)
    for row in range(A.shape[0]):
        for off in range(A.indptr[row],A.indptr[row+1]):
            out[row]+=int(A.data[off])*Vo[int(A.indices[off])]
    return out

def exact_gram(V,W,weights,chunk=4096):
    out=np.zeros((V.shape[1],W.shape[1]),dtype=object)
    for lo in range(0,len(weights),chunk):
        hi=min(len(weights),lo+chunk)
        out+=V[lo:hi].T@(W[lo:hi]*weights[lo:hi,None].astype(object))
    return out

def certify_block(nx,ny,g,parity,M,qmax,k,bits=34,check_full=False):
    start=time.monotonic();basis,Arect,den,weights,H=make_map(nx,ny,g,parity,M,qmax)
    if k>=len(basis)-1:
        vals,vecs=np.linalg.eigh(H.toarray());vals=vals[:k];vecs=vecs[:,:k]
    else:
        vals,vecs=eigsh(H,k=k,which='SA',tol=1e-13,ncv=max(2*k+1,20),v0=np.random.default_rng(1701+M+parity).normal(size=len(basis)))
    order=np.argsort(vals);vals=vals[order];vecs=vecs[:,order]
    raw=vecs*np.sqrt(float(weights[0])/weights[:len(basis)].astype(float))[:,None]
    V=np.rint(raw*(2**bits)).astype(np.int64)
    tag=f'bilayer_{nx}x{ny}_g{g}_p{parity}_M{M}_q{qmax}'.replace('/','d')
    np.savez_compressed(OUT/f'{tag}_trial.npz',basis=np.array(basis,dtype=np.uint8),vectors=V,bits=bits)
    V=V.astype(object)
    HV=exact_apply(Arect,V)
    G=exact_gram(V,V,weights[:len(basis)])
    A=exact_gram(V,HV[:len(basis)],weights[:len(basis)]) # denominator den
    B=exact_gram(HV,HV,weights) # denominator den^2
    assert np.array_equal(G,G.T) and np.array_equal(A,A.T) and np.array_equal(B,B.T)
    assert pd(G)
    # Rational approximate coordinate operator D. Orthogonal projection only
    # reduces ||HV-VD||, so E certifies the true Ritz residual without G^-1.
    dscale=10**10;d=np.array([round(float(v)*dscale) for v in vals],dtype=object)
    E=B*dscale*dscale-den*dscale*(A*d[None,:]+d[:,None]*A)+den*den*(d[:,None]*G*d[None,:])
    eden=den*den*dscale*dscale
    assert exact_inertia(E)[0]==0
    Gn=np.array(G,dtype=float);An=np.array(A,dtype=float)/den;En=np.array(E,dtype=float)/eden
    scale=float(max(G.diagonal()));Gn/=scale;An/=scale;En/=scale
    ritz=eigvalsh(An,Gn)
    e=upper_round(max(0,eigvalsh(En,Gn)[-1]),digits=12)
    assert pd(e*eden*G-E)
    lowers=[];uppers=[]
    for i,v in enumerate(ritz):
        lo=lower_round(v);up=upper_round(v)
        while exact_inertia(A-den*lo*G)[0]>i:lo-=F(1,10**9)
        while exact_inertia(A-den*up*G)[0]<i+1:up+=F(1,10**9)
        lowers.append(str(lo));uppers.append(str(up))
    rec=dict(parity=parity,M=M,multiplicity=2 if M==1 else 1,k=k,qmax=qmax,
       trial_dimension=len(basis),reached_dimension=Arect.shape[0],sparse_nnz=Arect.nnz,
       matrix_denominator=den,residual_denominator=eden,
       G=[[str(x) for x in row] for row in G],A=[[str(x) for x in row] for row in A],
       E=[[str(x) for x in row] for row in E],B=[[str(x) for x in row] for row in B],
       diagonal_proposal=[str(F(int(x),dscale)) for x in d],
       residual_squared_bound=str(e),ritz_lower=lowers,ritz_upper=uppers,
       trial_file=f'{tag}_trial.npz',seconds=time.monotonic()-start,
       peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (OUT/f'{tag}_gram.json').write_text(json.dumps(rec,indent=2))
    print('BLOCK',tag,'dim',len(basis),'reached',Arect.shape[0],'eta2',float(e),'seconds',rec['seconds'],flush=True)
    return rec

def unpack(rec):
    mats=[np.array([[int(x) for x in row] for row in rec[key]],dtype=object) for key in ['G','A','E']]
    return *mats,int(rec['matrix_denominator']),int(rec['residual_denominator'])

def finish_block(rec,b):
    G,A,E,den,eden=unpack(rec);k=rec['k']
    scale=float(max(G.diagonal()));Gn=np.array(G,dtype=float)/scale;An=np.array(A,dtype=float)/(den*scale);En=np.array(E,dtype=float)/(eden*scale)
    w,U=eigh(Gn);Gi=U@np.diag(w**-.5)@U.T
    T=Gi@An@Gi;EE=Gi@En@Gi
    w,U=eigh(EE);S=U@np.diag(np.sqrt(np.maximum(0,w)))@U.T
    augmented=np.block([[T,S],[S,float(b)*np.eye(k)]])
    proposals=eigvalsh(augmented)[:k]
    out=[];counts=[]
    for i,v in enumerate(proposals):
        lo=lower_round(v)
        assert lo<b
        def count(t):return exact_inertia((b-t)*(A-den*t*G)*eden-den*E)
        while count(lo)[0]>i:lo-=F(1,10**9)
        out.append(str(lo));counts.append(list(count(lo)))
    rec=rec.copy();rec['eigen_lower']=out;rec['eigen_upper']=rec['ritz_upper'];rec['schur_inertia_at_lower']=counts
    return rec

def make_certificate(nx,ny,g,qeven=2,qodd=3,bits=34,reuse=True):
    N=nx*ny;bound=optimize_tail_bound(g,N)
    alpha=F(bound['alpha']);B=F(bound['B']);a=2*alpha-B;L0=-B
    blocks=[]
    for parity,M,q,k in [(0,0,qeven,1),(1,0,qodd,N),(1,1,qodd,N)]:
        tag=f'bilayer_{nx}x{ny}_g{g}_p{parity}_M{M}_q{q}'.replace('/','d')
        path=OUT/f'{tag}_gram.json'
        block=json.loads(path.read_text()) if reuse and path.exists() else certify_block(nx,ny,g,parity,M,q,k,bits)
        blocks.append(block)
    r=max(F(x) for block in blocks for x in block['ritz_upper'])
    e=max(F(block['residual_squared_bound']) for block in blocks)
    assert a>r,(float(a),float(r))
    s2=min(F(1),e/(a-r)**2);b=a-(a-L0)*s2
    assert b>r,(float(b),float(r))
    blocks=[finish_block(block,b) for block in blocks]
    rec=dict(status='exact_rational_full_low_band_certificate_not_independently_audited',model='ordinary spin-1/2 square bilayer',
       nx=nx,ny=ny,N=N,g=str(g),energy_shift=str(-F(3*N,4)),
       boundary='periodic positive-direction edge multiset, parallel bonds retained for length 2',
       full_hilbert_dimension=4**N,retained_full_band_dimension=1+3*N,
       relative_form_bound=bound,global_lambda_kplus1_lower=str(a),global_ground_lower=str(L0),
       ritz_max_upper=str(r),residual_squared_bound=str(e),sin_angle_squared_upper=str(s2),
       orthogonal_complement_lower=str(b),blocks=blocks)
    path=OUT/f'bilayer_{nx}x{ny}_g{g}_low_band.json'.replace('/','d');path.write_text(json.dumps(rec,indent=2))
    print('CERT',nx,ny,'a',float(a),'b',float(b),'maxritz',float(r),'eta2',float(e),flush=True)
    return rec

def traces(rec,beta):
    beta=F(beta);assert beta>=0
    N=rec['N'];alpha=F(rec['relative_form_bound']['alpha']);B=F(rec['relative_form_bound']['B'])
    shift=F(rec['blocks'][0]['eigen_upper'][0]);low=F(0);high=F(0)
    for block in rec['blocks']:
        mult=block['multiplicity']
        for elo,ehi in zip(block['eigen_lower'],block['eigen_upper']):
            low+=mult*exp_bounds(-beta*(F(ehi)-shift))[0]
            high+=mult*exp_bounds(-beta*(F(elo)-shift))[1]
    # Positive explicit sum avoids subtracting outward-rounded quantities.
    x=exp_bounds(-beta*alpha)[1]
    tailpoly=sum(F(math.comb(N,j)*3**j)*x**j for j in range(2,N+1))
    tail=exp_bounds(beta*(B+shift))[1]*tailpoly
    if "number_sector_bins" in rec:
        tail=sum(F(row["multiplicity"])*exp_bounds(-beta*(F(row["lower"])-shift))[1] for row in rec["number_sector_bins"]["bins"][2:])
    return low,high+tail,tail

def seeds(recs,betas):
    out=[]
    ehi=[F(r['energy_shift'])+F(r['blocks'][0]['eigen_upper'][0]) for r in recs]
    for beta in map(F,betas):
        t=[traces(r,beta) for r in recs];t2=traces(recs[2],2*beta)
        A=down(exp_bounds(-beta*(ehi[1]-2*ehi[0]))[0]*t[1][0]/t[0][1]**2,digits=15)
        B=down(exp_bounds(-beta*(ehi[2]-2*ehi[1]))[0]*t[2][0]/t[1][1]**2,digits=15)
        C=down(t2[0]/t[2][1]**2,digits=15)
        boot=replay(A,B,C,n=2,m=2,beta=beta,rounds=64,digits=18)
        row=dict(beta=str(beta),A=str(A),B=str(B),C=str(C),display=list(map(float,[A,B,C])),
                 tail_display=[float(x[2]) for x in t],bootstrap=boot)
        out.append(row);print('SEED',beta,row['display'],boot,flush=True)
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--g',default='3/100');p.add_argument('--shapes',default='2x2,4x2');p.add_argument('--qeven',type=int,default=2);p.add_argument('--qodd',type=int,default=3);p.add_argument('--bits',type=int,default=34);p.add_argument('--betas',default='8,10,12,14,16,18,20,24,28,32');p.add_argument('--no-reuse',action='store_true')
    a=p.parse_args();g=F(a.g)
    recs=[make_certificate(*map(int,s.split('x')),g,a.qeven,a.qodd,a.bits,not a.no_reuse) for s in a.shapes.split(',')]
    if [(r['nx'],r['ny']) for r in recs]==[(2,2),(4,2),(4,4)]:
        result=dict(certificates=[f"bilayer_{r['nx']}x{r['ny']}_g{g}_low_band.json".replace('/','d') for r in recs],seeds=seeds(recs,a.betas.split(',')))
        (OUT/f'full_low_band_seed_g{g}.json'.replace('/','d')).write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
