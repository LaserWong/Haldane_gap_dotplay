"""Larger-seed large-D certificates with disconnected two-bond virtual pairs.
The trial space includes every two-excitation M=0 configuration and every
four-excitation configuration made by acting on two disjoint lattice bonds.
Integer-encoded output states reduce memory. The exact residual includes every
state reached by H, irrespective of the selected trial support.
"""
from large_d_certificates import *

def certify_pair_patch(nx,ny,g,bits=44):
    g=F(g);N=nx*ny;assert 4<=N<=64
    tag=f'largeD_{nx}x{ny}_g{g}_bp2'.replace('/','d');path=OUT/(tag+'_ground.json')
    if path.exists():return json.loads(path.read_text())
    t0=time.monotonic();idx=lambda x,y:(x%nx)*ny+y%ny
    edges=[e for x in range(nx) for y in range(ny) for e in [(idx(x,y),idx(x+1,y)),(idx(x,y),idx(x,y+1))]]
    unique=sorted(set(tuple(sorted(e)) for e in edges));pw=[3**i for i in range(N)];vacuum=sum(pw)
    trial={vacuum:(0,)*N}
    for i,j in itertools.combinations(range(N),2):
        for sign in [-1,1]:
            st=[0]*N;st[i]=sign;st[j]=-sign;trial[vacuum+sign*(pw[i]-pw[j])]=tuple(st)
    for (i,j),(k,l) in itertools.combinations(unique,2):
        if len({i,j,k,l})<4:continue
        for s,t in itertools.product([-1,1],repeat=2):
            st=[0]*N;st[i]=s;st[j]=-s;st[k]=t;st[l]=-t
            trial[vacuum+s*(pw[i]-pw[j])+t*(pw[k]-pw[l])]=tuple(st)
    ids=list(trial);states=list(trial.values());del trial
    assert len(states)<=40000, 'Trial support exceeds declared resource budget'
    output={v:i for i,v in enumerate(ids)};den=g.denominator;gg=g.numerator;rr=[];cc=[];vv=[]
    for col,(source,st) in enumerate(zip(ids,states)):
        acc=defaultdict(int);acc[source]+=den*sum(m*m for m in st)+gg*sum(st[i]*st[j] for i,j in edges)
        for i,j in edges:
            for sign in [-1,1]:
                if -1<=st[i]+sign<=1 and -1<=st[j]-sign<=1:acc[source+sign*(pw[i]-pw[j])]+=gg
        for dest,value in acc.items():
            if not value:continue
            if dest not in output:output[dest]=len(output)
            rr.append(output[dest]);cc.append(col);vv.append(value)
    reached=len(output);del output
    A=sp.coo_matrix((np.asarray(vv,dtype=np.int64),(rr,cc)),shape=(reached,len(states))).tocsr();del rr,cc,vv
    A.sum_duplicates();A.eliminate_zeros();T=A[:len(states)];assert (T-T.T).nnz==0
    built=time.monotonic();e,v=eigsh(T.astype(float)/den,k=1,which='SA',tol=3e-14,v0=np.random.default_rng(41421).normal(size=len(states)))
    integers=[int(round(float(x)*2**bits)) for x in v[:,0]];norm=sum(x*x for x in integers)
    Hv=[sum(int(A.data[j])*integers[int(A.indices[j])] for j in range(A.indptr[i],A.indptr[i+1])) for i in range(A.shape[0])]
    rho=F(sum(x*y for x,y in zip(integers,Hv)),den*norm);res2=F(sum(y*y for y in Hv),den*den*norm)-rho*rho
    a,b,c,B=max(choices(g,N),key=lambda p:p[2]-p[3]);nextlo=c-B
    assert res2>=0 and rho<nextlo
    elo=rho-res2/(nextlo-rho)
    rec=dict(model='spin1_large_D_square',nx=nx,ny=ny,N=N,g=str(g),D='1',periodic='both axes; length-two lattice multibonds',full_dimension=3**N,trial_dimension=len(states),reached_dimension=reached,support='all two-excitation plus disjoint two-bond four-excitation states',integer_denominator=den,sparse_nnz=A.nnz,dyadic_bits=bits,exact_rayleigh=str(rho),exact_residual_squared=str(res2),ground_lower=str(elo),ground_upper=str(rho),ground_lower_display=float(elo),ground_upper_display=float(rho),ground_width_display=float(rho-elo),second_eigenvalue_lower=str(nextlo),comparison={'a':str(a),'b':str(b),'c':str(c),'B':str(B)},ground_unique_certified=True,proof='Exact full-action integer residual with orthonormal product basis; same exact bond-PSD comparison and Temple isolation as large_d_certificates.py.',full_spectrum_used=False,build_seconds=built-t0,total_seconds=time.monotonic()-t0,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    artifact=OUT/(tag+'_trial.npz');np.savez_compressed(artifact,basis=np.array(states,dtype=np.int8),vector=np.array(integers,dtype=np.int64),bits=bits)
    rec['trial_artifact']=artifact.name;path.write_text(json.dumps(rec,indent=2));print('GROUND',tag,rec['ground_lower_display'],rec['ground_upper_display'],len(states),reached,rec['total_seconds'],rec['peak_rss_kib'],flush=True)
    return rec

def main():
    p=argparse.ArgumentParser();p.add_argument('--g',default='1/50');p.add_argument('--base-size',type=int,default=4);p.add_argument('--betas',default='16,20,24,28,32,40,48,64');args=p.parse_args();n=args.base_size;g=F(args.g)
    recs=[certify_pair_patch(nx,ny,g) for nx,ny in [(n,n),(2*n,n),(2*n,2*n)]];rows=[]
    for beta in args.betas.split(','):
        r=seed(recs,F(beta));rows.append(r);print('SEED',beta,r['purity_lower_displays'],r['bootstrap']['status'],r['bootstrap'].get('uniform_square_gap_lower_display'),flush=True)
    out=dict(model='spin1_large_D_square',g=str(g),D='1',n=n,ground_certificates=recs,seeds=rows)
    (OUT/(f'largeD_g{g}_bp2_n{n}_certificate.json'.replace('/','d'))).write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
