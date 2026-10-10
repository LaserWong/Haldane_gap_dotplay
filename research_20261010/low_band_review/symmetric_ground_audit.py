"""Independent physical-kernel reconstruction of symmetry ground replacements.
All three compressed G/K/J matrices and complete leaked supports are rebuilt.
Only g=.03 block-depth-one inputs are in scope.
"""
from independent_review import *
import gzip
SYM=OUT.parent/'symmetry'


def apply_integer(vec,n,ed,den,g):
    kr=[[(i,j,int(g*x*den)) for i,j,x in row] for row in KERNEL]
    assert all(g*x*den==int(g*x*den) for row in KERNEL for _,_,x in row)
    out=defaultdict(int)
    for state,c in vec.items():
        digits=[(state>>(2*i))&3 for i in range(n)]
        assert sum(x!=0 for x in digits)%2==0 and sum(x-2 for x in digits if x)==0
        out[state]+=den*sum(x!=0 for x in digits)*c
        for i,j in ed:
            a,b=digits[i],digits[j]
            for x,y,k in kr[4*a+b]:out[state^((a^x)<<(2*i))^((b^y)<<(2*j))]+=c*k
    return {s:c for s,c in out.items() if c}


def scalar(vec,other,n):
    mask=sum(1<<(2*i) for i in range(n))
    if len(vec)>len(other):vec,other=other,vec
    return sum(c*other.get(s,0)*(1<<(n-(s&mask).bit_count())) for s,c in vec.items())


def audit_shape(shape):
    start=time.monotonic();source=SYM/f'symmetry_{shape}_g3d100_block1.json';saved=json.loads(source.read_text())
    packed=source.with_name(source.stem+'_basis.json.gz');raw=json.loads(gzip.decompress(packed.read_bytes()))
    basis=[{int(s):int(c) for s,c in row} for row in raw]
    assert all(len(b)==len(row) and all(c!=0 for c in b.values()) for b,row in zip(basis,raw))
    n=saved['N_dimers'];den=saved['integer_matrix_denominator'];g=F(saved['coupling']);ed=edges(saved['nx'],saved['ny'])
    assert n==saved['nx']*saved['ny'] and len(basis)==saved['trial_subspace_dimension'] and g==F(3,100)
    assert all(0<=state<4**n for b in basis for state in b)
    applied=[apply_integer(v,n,ed,den,g) for v in basis]
    mats=[]
    for left,right,key in [(basis,basis,'gram'),(basis,applied,'shifted_hamiltonian_numerator'),(applied,applied,'shifted_H2_numerator')]:
        m=np.array([[scalar(v,w,n) for w in right] for v in left],dtype=object)
        assert np.array_equal(m,np.array([[int(x) for x in row] for row in saved[key]],dtype=object)),key
        mats.append(m)
    G,K,J=mats;assert inertia_fraction(G)==(0,0,len(basis))
    support=set().union(*(b.keys() for b in basis));reached=support.union(*(b.keys() for b in applied))
    assert len(support)==saved['trial_expanded_support_dimension'] and len(reached)==saved['reached_support_dimension']
    coeff=np.array([int(x) for x in saved['coefficients']],dtype=object)
    norm=int(coeff@G@coeff);ha=int(coeff@K@coeff);hb=int(coeff@J@coeff)
    rho=F(ha,den*norm);r2=F(hb,den*den*norm)-rho*rho
    assert rho==F(saved['exact_rayleigh'])-F(saved['E00']) and r2==F(saved['exact_residual_squared'])
    target=SRC/f'bilayer_{shape}_g3d100_symmetric_number_low_band.json';rec=json.loads(target.read_text())
    old=json.loads((SRC/f'bilayer_{shape}_g3d100_number_low_band.json').read_text())
    bl=rec['blocks'][0];assert bl['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
    assert bl['G']==[[str(norm)]] and bl['A']==[[str(ha)]] and bl['B']==[[str(hb)]]
    assert bl['E']==[[str(norm*hb-ha*ha)]] and bl['residual_denominator']==den*den*norm
    assert F(bl['residual_squared_bound'])>=r2>=0
    assert F(bl['ritz_upper'][0])==rho==F(bl['ritz_lower'][0])
    assert bl['parity']==0 and bl['M']==0 and bl['multiplicity']==1 and bl['k']==1
    assert rec['number_sector_bins']==old['number_sector_bins']
    e=max(F(x['residual_squared_bound']) for x in rec['blocks']);r=max(F(t) for x in rec['blocks'] for t in x['ritz_upper'])
    number=rec['number_sector_bins'];a=F(number['bins'][2]['lower']);L0=F(number['bins'][0]['lower'])
    s2=e/(a-r)**2;b=a-(a-L0)*s2;assert s2<1 and b>r
    assert e==F(rec['residual_squared_bound']) and r==F(rec['ritz_max_upper'])
    assert b==F(rec['orthogonal_complement_lower']) and s2==F(rec['sin_angle_squared_upper'])
    assert a==F(rec['global_lambda_kplus1_lower']) and L0==F(rec['global_ground_lower'])
    for i in [1,2]:
        unchanged=['G','A','B','E','matrix_denominator','residual_denominator','residual_squared_bound','ritz_upper','ritz_lower','trial_file','parity','M','multiplicity','k']
        assert all(rec['blocks'][i][key]==old['blocks'][i][key] for key in unchanged)
    endpoints=[]
    for block in rec['blocks']:
        GG,AA,EE=[np.array([[int(v) for v in row] for row in block[key]],dtype=object) for key in ['G','A','E']]
        dd=block['matrix_denominator'];ee=block['residual_denominator'];counts=[]
        assert inertia_fraction(F(block['residual_squared_bound'])*ee*GG-EE)[0]==0
        for i,t0 in enumerate(block['eigen_lower']):
            t=F(t0);assert t<b
            count=inertia_fraction((b-t)*(AA-dd*t*GG)*ee-dd*EE)
            assert count[0]<=i and list(count)==block['schur_inertia_at_lower'][i];counts.append(list(count))
        assert block['eigen_upper']==block['ritz_upper']
        endpoints.append(dict(parity=block['parity'],M=block['M'],exact_Schur_inertia=counts))
    # Full physical-spin matrix also independently verifies the entire tiny compressed moment matrices.
    tiny=False
    if n==4:
        p=np.array([[0,1,0,0],[1,0,1,0],[-1,0,1,0],[0,0,0,1]],dtype=object)
        W=np.zeros((4**n,len(basis)),dtype=object)
        for j,v in enumerate(basis):
            for state,c in v.items():
                tensor=np.array([1],dtype=object)
                for i in reversed(range(n)):tensor=np.kron(tensor,p[:,(state>>(2*i))&3])
                W[:,j]+=c*tensor
        # Exact standard computational spin action for T=den*H'.
        T=np.zeros((4**n,4**n),dtype=object)
        bonds=[(2*i,2*i+1,F(1)) for i in range(n)]+[(2*i+l,2*j+l,g) for i,j in ed for l in [0,1]]
        for state in range(4**n):
            diagonal=F(3*n,4)
            for i,j,c in bonds:
                u=(state>>i)&1;v=(state>>j)&1
                diagonal+=c*F((2*u-1)*(2*v-1),4)
                if u!=v:T[state^(1<<i)^(1<<j),state]+=int(den*c/2)
            T[state,state]+=int(den*diagonal)
        TW=T@W
        assert np.array_equal(W.T@W,G) and np.array_equal(W.T@TW,K) and np.array_equal(TW.T@TW,J)
        tiny=True
    result=dict(shape=shape,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),basis_sha256=hashlib.sha256(packed.read_bytes()).hexdigest(),
                updated_band_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                all_G_K_J_integers_reconstructed=True,linear_dimension=len(basis),expanded_support=len(support),full_reached_support=len(reached),
                norm=str(norm),ha=str(ha),hb=str(hb),shifted_Rayleigh=str(rho),residual_squared=str(r2),
                tiny_exact_computational_spin_crosscheck=tiny,endpoint_checks=endpoints,
                seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return result

report=dict(status='passed_independent_symmetry_ground_physical_moment_and_band_checks',records=[])
for shape in ['2x2','4x2','4x4']:
    report['records'].append(audit_shape(shape));gc.collect();print('EXACT SYMMETRY PASS',shape,flush=True)
    (OUT/'symmetric_ground_results.json').write_text(json.dumps(report,indent=2))
