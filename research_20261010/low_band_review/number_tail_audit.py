"""Independent exact audit of shell-number Jacobi bounds and updated band.
No producer code imported. Graph occupancy DP differs from producer enumeration.
"""
from independent_review import *
import scipy.linalg as la


def occupancy_dp(nx,ny):
    n=nx*ny;ed=edges(nx,ny);neighbors=[[] for _ in range(n)]
    for i,j in ed:neighbors[i].append(j);neighbors[j].append(i)
    assert all(len(row)==4 for row in neighbors)
    occ=[0]*(1<<n);best=[0]*(n+1);empty=[0]*(n+1)
    for mask in range(1,1<<n):
        bit=mask&-mask;i=bit.bit_length()-1;rest=mask^bit
        occ[mask]=occ[rest]+sum((rest>>j)&1 for j in neighbors[i])
        q=mask.bit_count();best[q]=max(best[q],occ[mask])
    full=(1<<n)-1
    for mask in range(1<<n):empty[mask.bit_count()]=max(empty[mask.bit_count()],occ[full^mask])
    assert empty==[2*n-4*q+best[q] for q in range(n+1)]
    return best,empty


def audit_local(saved):
    w=[2,1,2,1];q=[int(i//4!=0)+int(i%4!=0) for i in range(16)]
    v=np.zeros((16,16),dtype=object)
    for j,row in enumerate(KERNEL):
        for a,b,x in row:v[4*a+b,j]+=x
    m=np.array([[v[i,j] if q[i]==q[j] else F(0) for j in range(16)] for i in range(16)],dtype=object)
    for i in range(16):m[i,i]+=F(q[i],2)
    metric=[w[i//4]*w[i%4] for i in range(16)]
    m=m*np.array(metric,dtype=object)[:,None]
    assert np.array_equal(m,m.T)
    inert=inertia_fraction(m);assert inert[0]==0
    assert list(inert)==saved['preserving_plus_half_number_inertia']
    entries=[]
    for i in range(16):
        for j in range(16):
            assert v[i,j]==0 or abs(q[i]-q[j]) in [0,2]
            if q[i]==q[j]+2 and v[i,j]:
                val=F(v[i,j])**2*F(metric[i],metric[j]);assert val==F(1,4)
                entries.append([i,j,str(val)])
    assert entries==saved['creation_entries_abs_squared'] and len(entries)==3
    return dict(preserving_inertia=list(inert),pair_creation_exact_absolute_square='1/4',pair_creation_count=3)


def audit_shape(shape):
    p=SRC/f'number_bins_{shape}_g3d100.json';number=json.loads(p.read_text())
    bp=SRC/f'bilayer_{shape}_g3d100_number_low_band.json';rec=json.loads(bp.read_text())
    old=json.loads((SRC/f'bilayer_{shape}_g3d100_low_band.json').read_text())
    assert rec['number_sector_bins']==number
    n=number['N'];g=F(number['g']);nx=number['nx'];ny=number['ny'];assert n==nx*ny and 0<=g<F(1,2)
    occupied,empty=occupancy_dp(nx,ny)
    assert occupied==number['graph_counts']['occupied_edge_max'] and empty==number['graph_counts']['empty_edge_max']
    weighted=defaultdict(int)
    for i,j in edges(nx,ny):weighted[tuple(sorted((i,j)))]+=1
    assert [[i,j,w] for (i,j),w in sorted(weighted.items())]==number['graph_counts']['edges']
    diag=[(1-2*g)*q for q in range(n+1)]
    off=[F(3,4)*g*g*empty[q]*occupied[q+2] for q in range(n-1)]
    assert diag==list(map(F,number['diagonal'])) and off==list(map(F,number['offdiagonal_squared']))
    results=[];prior=None;position=1
    for q,row in enumerate(number['bins']):
        assert row['q']==q and row['multiplicity']==math.comb(n,q)*3**q and row['first_ordered_index']==position
        position+=row['multiplicity'];parts=[]
        assert len(row['parity_compressions'])==min(2,n+1-q)
        for part,start in zip(row['parity_compressions'],[q,q+1]):
            inds=list(range(start,n+1,2));assert inds==part['number_indices'];t=F(part['lower']);piv=[]
            for i,j in enumerate(inds):
                x=diag[j]-t
                if i:x-=off[inds[i-1]]/piv[-1]
                assert x>0;piv.append(x)
            assert piv==list(map(F,part['ldl_positive_pivots']))
            parts.append(t)
        expected=min(parts) if prior is None else max(min(parts),prior)
        assert F(row['lower'])==expected;prior=expected
        results.append(dict(q=q,lower=str(expected),all_parity_LDL_pivots_positive=True))
    assert position==4**n+1
    a=F(number['bins'][2]['lower']);L0=F(number['bins'][0]['lower']);r=F(old['ritz_max_upper']);e=F(old['residual_squared_bound'])
    s2=min(F(1),e/(a-r)**2);b=a-(a-L0)*s2
    assert r<a and r<b
    assert a==F(rec['global_lambda_kplus1_lower']) and L0==F(rec['global_ground_lower'])
    assert s2==F(rec['sin_angle_squared_upper']) and b==F(rec['orthogonal_complement_lower'])
    blocks=[]
    for bl,oldbl in zip(rec['blocks'],old['blocks']):
        unchanged=['parity','M','multiplicity','k','G','A','B','E','matrix_denominator','residual_denominator','residual_squared_bound','ritz_lower','ritz_upper','eigen_upper','trial_file']
        assert all(bl[key]==oldbl[key] for key in unchanged)
        G,A,E=[np.array([[int(v) for v in row] for row in bl[key]],dtype=object) for key in ['G','A','E']]
        den=bl['matrix_denominator'];eden=bl['residual_denominator'];counts=[]
        for i,tl in enumerate(bl['eigen_lower']):
            t=F(tl);assert t<b
            count=inertia_fraction((b-t)*(A-den*t*G)*eden-den*E)
            assert count[0]<=i and list(count)==bl['schur_inertia_at_lower'][i];counts.append(list(count))
        blocks.append(dict(parity=bl['parity'],M=bl['M'],unchanged_exact_Gram_data=True,Schur_endpoint_inertia=counts))
    return dict(shape=shape,number_source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),updated_band_sha256=hashlib.sha256(bp.read_bytes()).hexdigest(),
                local=audit_local(number['local_certificate']),graph_DP_verified=True,occupied_edge_max=occupied,empty_edge_max=empty,
                bins=results,band_complement_lower=str(b),blocks=blocks)


def tiny_diagnostic():
    number=json.loads((SRC/'number_bins_2x2_g3d100.json').read_text());n=4
    h=physical_matrix(2,2).toarray();ev=la.eigvalsh(h)
    p=np.array([[0,1,0,0],[1,0,1,0],[-1,0,1,0],[0,0,0,1]],dtype=float)@np.diag([2**-.5,1,2**-.5,1])
    transform=p
    for _ in range(n-1):transform=np.kron(transform,p)
    dimer=transform.T@h@transform
    q=np.array([sum(d!=0 for d in state) for state in itertools.product(range(4),repeat=n)])
    out=[]
    for j,row in enumerate(number['bins']):
        binlo=float(F(row['lower']));actual=float(ev[row['first_ordered_index']-1]);assert actual>=binlo
        ind=np.flatnonzero(q==j)
        mindiag=float(la.eigvalsh(dimer[np.ix_(ind,ind)])[0]);diagbound=float(F(number['diagonal'][j]));assert mindiag>=diagbound-1e-12
        item=dict(q=j,ordered_actual_eigenvalue=actual,bin_lower=binlo,number_preserving_minimum=mindiag,number_preserving_bound=diagbound)
        if j+2<=n:
            ind2=np.flatnonzero(q==j+2)
            norm2=float(la.svdvals(dimer[np.ix_(ind2,ind)])[0]**2);bound=float(F(number['offdiagonal_squared'][j]));assert norm2<=bound+1e-12
            item.update(actual_creation_norm_squared=norm2,creation_norm_squared_bound=bound)
        out.append(item)
    return dict(status='passed_floating_diagnostic_only',rows=out)


def main():
    start=time.monotonic();results=[]
    for shape in ['2x2','4x2','4x4']:
        results.append(audit_shape(shape));print('EXACT NUMBER PASS',shape,flush=True)
    rec=dict(status='passed_independent_exact_number_shell_and_updated_band_checks',records=results,
             physical_2x2_diagnostic=tiny_diagnostic(),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (OUT/'number_results.json').write_text(json.dumps(rec,indent=2))
if __name__=='__main__':main()
