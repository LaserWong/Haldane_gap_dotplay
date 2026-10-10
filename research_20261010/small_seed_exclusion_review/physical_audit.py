"""Independent physical audit of final g=.04/.05 small-seed complete bands.
Reuses only the previously independent physical-spin kernel and Fraction inertia
implementation, never producer code. All coupling-specific moments are rebuilt.
One CPU, one BLAS thread, 1 GiB address-space cap (set by reviewed helper).
"""
import sys
from pathlib import Path
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
sys.path.insert(0,str(OUT.parent/'low_band_review'))
import independent_review as I
from independent_review import F,np,defaultdict,math,json,time,hashlib,resource,gc
import gzip
from number_tail_audit import occupancy_dp,audit_local
SRC=OUT.parent/'low_band'/'frontier';I.SRC=SRC
HASHES={}
def read_bytes(p):
    raw=p.read_bytes();key=str(p.relative_to(ROOT));h=hashlib.sha256(raw).hexdigest()
    assert key not in HASHES or HASHES[key]==h
    HASHES[key]=h;return raw
def read(p):return json.loads(read_bytes(p))
for helper in ['independent_review.py','number_tail_audit.py']:
    read_bytes(OUT.parent/'low_band_review'/helper)

def apply(v,n,ed,den,g):
    kr=[[(i,j,int(g*x*den)) for i,j,x in row] for row in I.KERNEL]
    assert all(g*x*den==int(g*x*den) for row in I.KERNEL for _,_,x in row)
    out=defaultdict(int)
    for state,c in v.items():
        digits=[(state>>(2*i))&3 for i in range(n)]
        assert sum(x!=0 for x in digits)%2==0 and sum(x-2 for x in digits if x)==0
        out[state]+=den*sum(x!=0 for x in digits)*c
        for i,j in ed:
            a,b=digits[i],digits[j]
            for x,y,k in kr[4*a+b]:out[state^((a^x)<<(2*i))^((b^y)<<(2*j))]+=c*k
    return {s:c for s,c in out.items() if c}
def scalar(v,w,n):
    mask=sum(1<<(2*i) for i in range(n))
    if len(v)>len(w):v,w=w,v
    return sum(c*w.get(s,0)*(1<<(n-(s&mask).bit_count())) for s,c in v.items())

def ground(rec):
    bl=rec['blocks'][0];source=OUT.parent/bl['source_file'];saved=read(source)
    packed=source.with_name(source.stem+'_basis.json.gz')
    raw=json.loads(gzip.decompress(read_bytes(packed)))
    basis=[{int(s):int(c) for s,c in row} for row in raw]
    n=rec['N'];den=saved['integer_matrix_denominator'];g=F(rec['g'])
    assert bl['source_sha256']==HASHES[str(source.relative_to(ROOT))]
    assert n==saved['N_dimers']==saved['nx']*saved['ny']
    assert saved['nx']==rec['nx'] and saved['ny']==rec['ny'] and F(saved['coupling'])==g
    assert F(saved['E00'])==F(rec['energy_shift'])==-F(3*n,4)
    assert len(basis)==saved['trial_subspace_dimension']
    assert all(len(v)==len(row) and all(c!=0 and 0<=s<4**n for s,c in v.items()) for v,row in zip(basis,raw))
    applied=[apply(v,n,I.edges(rec['nx'],rec['ny']),den,g) for v in basis]
    matrices=[]
    for left,right,key in [(basis,basis,'gram'),(basis,applied,'shifted_hamiltonian_numerator'),(applied,applied,'shifted_H2_numerator')]:
        mat=np.array([[scalar(v,w,n) for w in right] for v in left],dtype=object)
        assert mat.tolist()==[[int(x) for x in row] for row in saved[key]],key
        matrices.append(mat)
    G,A,B=matrices;assert I.inertia_fraction(G)==(0,0,len(basis))
    coeff=np.array(list(map(int,saved['coefficients'])),dtype=object)
    norm=int(coeff@G@coeff);ha=int(coeff@A@coeff);hb=int(coeff@B@coeff)
    assert norm>0
    rho=F(ha,den*norm);r2=F(hb,den*den*norm)-rho*rho
    assert r2==F(saved['exact_residual_squared']) and rho==F(saved['exact_rayleigh'])-F(saved['E00'])
    assert bl['G']==[[str(norm)]] and bl['A']==[[str(ha)]] and bl['B']==[[str(hb)]]
    assert bl['E']==[[str(norm*hb-ha*ha)]]
    assert bl['matrix_denominator']==den and bl['residual_denominator']==den*den*norm
    assert F(bl['residual_squared_bound'])>=r2>=0
    assert list(map(F,bl['ritz_lower']))==list(map(F,bl['ritz_upper']))==[rho]
    support=set().union(*(v.keys() for v in basis));reached=support.union(*(v.keys() for v in applied))
    assert len(support)==saved['trial_expanded_support_dimension'] and len(reached)==saved['reached_support_dimension']
    # Independently cross-check every tiny moment in the physical computational basis.
    if n==4:
        p=np.array([[0,1,0,0],[1,0,1,0],[-1,0,1,0],[0,0,0,1]],dtype=object)
        W=np.zeros((4**n,len(basis)),dtype=object)
        for j,v in enumerate(basis):
            for s,c in v.items():
                tensor=np.array([1],dtype=object)
                for i in reversed(range(n)):tensor=np.kron(tensor,p[:,(s>>(2*i))&3])
                W[:,j]+=c*tensor
        T=np.zeros((4**n,4**n),dtype=object)
        bonds=[(2*i,2*i+1,F(1)) for i in range(n)]+[(2*i+l,2*j+l,g) for i,j in I.edges(rec['nx'],rec['ny']) for l in [0,1]]
        for s in range(4**n):
            diag=F(3*n,4)
            for i,j,c in bonds:
                u=(s>>i)&1;v=(s>>j)&1;diag+=c*F((2*u-1)*(2*v-1),4)
                if u!=v:assert (den*c/2).denominator==1;T[s^(1<<i)^(1<<j),s]+=int(den*c/2)
            assert (den*diag).denominator==1;T[s,s]+=int(den*diag)
        TW=T@W
        assert np.array_equal(W.T@W,G) and np.array_equal(W.T@TW,A) and np.array_equal(TW.T@TW,B)
    return dict(linear_dimension=len(basis),expanded_support=len(support),reached_support=len(reached),all_integer_G_A_B_reconstructed=True,
                shifted_Rayleigh=str(rho),exact_full_residual_squared=str(r2),tiny_computational_spin_check=n==4)

def number_tail(rec):
    n=rec['N'];g=F(rec['g']);shape=f"{rec['nx']}x{rec['ny']}";tag=str(g).replace('/','d')
    number=read(SRC/f'number_bins_{shape}_g{tag}.json');assert number==rec['number_sector_bins']
    assert number['N']==n and number['nx']==rec['nx'] and number['ny']==rec['ny'] and F(number['g'])==g
    occupied,empty=occupancy_dp(rec['nx'],rec['ny'])
    assert occupied==number['graph_counts']['occupied_edge_max'] and empty==number['graph_counts']['empty_edge_max']
    weighted=defaultdict(int)
    for i,j in I.edges(rec['nx'],rec['ny']):weighted[tuple(sorted((i,j)))]+=1
    assert [[i,j,w] for (i,j),w in sorted(weighted.items())]==number['graph_counts']['edges']
    diag=[(1-2*g)*q for q in range(n+1)]
    off=[F(3,4)*g*g*empty[q]*occupied[q+2] for q in range(n-1)]
    assert diag==list(map(F,number['diagonal'])) and off==list(map(F,number['offdiagonal_squared']))
    assert len(number['bins'])==n+1
    prior=None;position=1;total_pivots=0
    for q,row in enumerate(number['bins']):
        assert row['q']==q and row['multiplicity']==math.comb(n,q)*3**q and row['first_ordered_index']==position
        position+=row['multiplicity'];parts=[]
        assert len(row['parity_compressions'])==min(2,n+1-q)
        for part,start in zip(row['parity_compressions'],[q,q+1]):
            indices=list(range(start,n+1,2));assert indices==part['number_indices']
            t=F(part['lower']);piv=[]
            for i,j in enumerate(indices):
                v=diag[j]-t
                if i:v-=off[indices[i-1]]/piv[-1]
                assert v>0;piv.append(v)
            assert piv==list(map(F,part['ldl_positive_pivots']));total_pivots+=len(piv);parts.append(t)
        bound=min(parts) if prior is None else max(min(parts),prior)
        assert bound==F(row['lower']);prior=bound
    assert position==4**n+1
    return dict(local=audit_local(number['local_certificate']),bins=n+1,positive_LDL_pivots=total_pivots,
                whole_Hilbert_multiplicity_sum=position-1,occupied_max=occupied,empty_max=empty)

def complete_band(rec):
    n=rec['N'];assert n==rec['nx']*rec['ny'] and rec['full_hilbert_dimension']==4**n
    assert F(rec['energy_shift'])==-F(3*n,4)
    assert [(b['parity'],b['M'],b['k'],b['multiplicity']) for b in rec['blocks']]==[(0,0,1,1),(1,0,n,1),(1,1,n,2)]
    assert rec['retained_full_band_dimension']==sum(b['k']*b['multiplicity'] for b in rec['blocks'])==1+3*n
    number=rec['number_sector_bins'];a=F(number['bins'][2]['lower']);L0=F(number['bins'][0]['lower'])
    r=max(F(x) for b in rec['blocks'] for x in b['ritz_upper']);eta=max(F(b['residual_squared_bound']) for b in rec['blocks'])
    assert r<a
    s2=eta/(a-r)**2;b=a-(a-L0)*s2
    assert 0<=s2<1 and r<b
    for key,val in [('global_lambda_kplus1_lower',a),('global_ground_lower',L0),('ritz_max_upper',r),('residual_squared_bound',eta),('sin_angle_squared_upper',s2),('orthogonal_complement_lower',b)]:
        assert F(rec[key])==val,key
    endpoints=[]
    for block in rec['blocks']:
        G,A,E=[np.array([[int(x) for x in row] for row in block[key]],dtype=object) for key in ['G','A','E']]
        dd=block['matrix_denominator'];ee=block['residual_denominator'];k=block['k']
        assert I.inertia_fraction(G)==(0,0,k)
        assert I.inertia_fraction(F(block['residual_squared_bound'])*ee*G-E)[0]==0
        assert block['eigen_upper']==block['ritz_upper']
        assert len(block['eigen_lower'])==len(block['eigen_upper'])==k
        rows=[]
        for i,(lo,hi,t0) in enumerate(zip(block['ritz_lower'],block['ritz_upper'],block['eigen_lower'])):
            il=I.inertia_fraction(A-dd*F(lo)*G);iu=I.inertia_fraction(A-dd*F(hi)*G)
            assert il[0]<=i and iu[0]+iu[1]>=i+1  # scalar exact Ritz endpoint may have a zero pivot
            t=F(t0);assert t<b and t<=F(hi)
            sc=I.inertia_fraction((b-t)*(A-dd*t*G)*ee-dd*E)
            assert sc[0]<=i and list(sc)==block['schur_inertia_at_lower'][i]
            rows.append(dict(ritz_lower=list(il),ritz_upper=list(iu),Schur_lower=list(sc)))
        endpoints.append(dict(parity=block['parity'],M=block['M'],rank=k,counts=rows))
    return dict(retained_rank=1+3*n,cutoff=str(a),max_Ritz=str(r),complement_lower=str(b),exact_residual_squared_bound=str(eta),endpoint_inertias=endpoints)

def main():
    start=time.monotonic();report=dict(status='running',physical_model='ordinary spin-1/2 bilayer; rung 1; straight in-layer g; periodic positive-direction multiedges',records=[])
    for g in ['1d25','1d20']:
        for shape in ['2x2','4x2','4x4']:
            t=time.monotonic();p=SRC/f'bilayer_{shape}_g{g}_symmetric_number_low_band.json';rec=read(p)
            item=dict(g=rec['g'],shape=shape,number_tail=number_tail(rec),ground=ground(rec),excited_blocks=[])
            for block in rec['blocks'][1:]:
                read_bytes(SRC/block['trial_file'])
                item['excited_blocks'].append(I.reconstruct(rec,block));gc.collect()
                print('EXACT EXCITED BLOCK PASS',g,shape,block['M'],flush=True)
            item['completeness_and_endpoints']=complete_band(rec)
            item['seconds']=time.monotonic()-t;item['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            report['records'].append(item);report['input_sha256']=HASHES
            (OUT/'physical_results.json').write_text(json.dumps(report,indent=2)+'\n')
            print('PHYSICAL COMPLETE BAND PASS',g,shape,item['seconds'],item['peak_rss_kib'],flush=True);gc.collect()
    # Verify accepted degeneracy-sensitive proposal differs from preserved rejected data.
    accepted=SRC/'bilayer_4x4_g1d20_p1_M1_q3_trial.npz'
    rejected=SRC/'bilayer_4x4_g1d20_p1_M1_q3_rejected_arpack_missing_modes_trial.npz'
    assert read_bytes(accepted)!=read_bytes(rejected)
    rej=read(SRC/'bilayer_4x4_g1d20_p1_M1_q3_rejected_arpack_missing_modes_gram.json')
    assert max(map(F,rej['ritz_upper']))>F(report['records'][-1]['completeness_and_endpoints']['cutoff'])
    report['rejected_proposal_cannot_meet_cutoff']=True
    for p,h in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
    report.update(status='PASS independently reconstructed all six physical complete bands and shell tails',input_sha256=HASHES,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  limits=dict(cpu_count=1,BLAS_threads=1,address_space_bytes=1024**3))
    (OUT/'physical_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],report['seconds'],report['peak_rss_kib'],flush=True)
if __name__=='__main__':main()
