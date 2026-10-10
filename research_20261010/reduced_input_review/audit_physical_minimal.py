"""G/K and G/A replay only; no residual or largest-space spectral data."""
from audit_helpers import *

def kernel():
    p=np.array([[0,1,0,0],[-1,0,1,0],[1,0,1,0],[0,0,0,1]],dtype=object)
    pp=np.kron(p,p);w=np.array([2,1,2,1],dtype=object);ww=np.kron(w,w)
    v=np.zeros((16,16),dtype=object)
    for c in range(16):
        bits=[(c>>(3-j))&1 for j in range(4)]
        for i,j in [(0,2),(1,3)]:
            v[c,c]+=(2*bits[i]-1)*(2*bits[j]-1)
            if bits[i]!=bits[j]:v[c^(1<<(3-i))^(1<<(3-j)),c]+=2
    a=pp.T@v@pp
    return [[(r//4,r%4,F(int(a[r,c]),4*int(ww[r]))) for r in range(16) if a[r,c]] for c in range(16)]
KERNEL=kernel()

def translate(s,nx,ny,dx,dy):
    out=0;mask=(1<<(2*ny))-1;shift=2*(dy%ny)
    for x in range(nx):
        row=(s>>(2*x*ny))&mask
        row=((row<<shift)|(row>>(2*ny-shift)))&mask
        out|=row<<(2*((x+dx)%nx)*ny)
    return out

def apply_restricted(v,nx,ny,g,allowed=None):
    """Exact PHv. P is support union for trial bras, never a residual projection."""
    n=nx*ny;den=4*g.denominator;ed,_,_=graph(nx,ny);mask=sum(1<<(2*i) for i in range(n))
    local=[[(x,y,int(den*g*z)) for x,y,z in row] for row in KERNEL];out=defaultdict(int)
    for s,c in v.items():
        if allowed is None or s in allowed:out[s]+=den*((s|(s>>1))&mask).bit_count()*c
        for (i,j),mul in ed.items():
            a=(s>>(2*i))&3;b=(s>>(2*j))&3
            for x,y,k in local[4*a+b]:
                t=s^((a^x)<<(2*i))^((b^y)<<(2*j))
                if allowed is None or t in allowed:out[t]+=c*mul*k
    return {s:c for s,c in out.items() if c}

def triplet_ga(g):
    nx=ny=8;n=64;den=4*g.denominator;mask=sum(1<<(2*i) for i in range(n));q=lambda s:((s|(s>>1))&mask).bit_count()
    im=apply_restricted({3:1},nx,ny,g)
    w={3:2*den};w.update({s:-c for s,c in im.items() if q(s)==3})
    raise_out=defaultdict(int)
    for s,c in w.items():
        assert q(s) in [1,3] and sum(((s>>(2*i))&3)-2 for i in range(n) if (s>>(2*i))&3)==1
        for i in range(n):
            digit=(s>>(2*i))&3
            if digit in [1,2]:raise_out[s^((digit^(digit+1))<<(2*i))]+=c*(1 if digit==1 else 2)
    assert not any(raise_out.values())
    support={translate(s,nx,ny,dx,dy) for s in w for dx in range(nx) for dy in range(ny)}
    hw=apply_restricted(w,nx,ny,g,support)
    weight=lambda s:1<<(n-(s&mask).bit_count())
    arrays=[[[0]*ny for _ in range(nx)] for _ in range(2)]
    for dx in range(nx):
        for dy in range(ny):
            for z,right in enumerate([w,hw]):
                arrays[z][dx][dy]=sum(c*right.get(translate(s,nx,ny,-dx,-dy),0)*weight(s) for s,c in w.items())
    for arr in arrays:
        assert all(arr[dx][dy]==arr[-dx%8][-dy%8] for dx in range(8) for dy in range(8))
    return arrays,dict(trial_generator_support=len(w),trial_bra_support_union=len(support),restricted_H_image_support=len(hw),exact_highest_weight=True,full_H_image_formed=False,H_squared_formed=False)

def qa(x,y):return x[0]+y[0],x[1]+y[1]
def qs(x,y):return x[0]-y[0],x[1]-y[1]
def qm(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def qd(x,y):
    d=y[0]**2-2*y[1]**2;assert d
    return qm(x,(y[0]/d,-y[1]/d))
def qsign(x):
    a,b=x
    if not a:return (b>0)-(b<0)
    if not b:return (a>0)-(a<0)
    if (a>0)==(b>0):return 1 if a>0 else -1
    z=(a*a>2*b*b)-(a*a<2*b*b);return z if a>0 else -z
ZERO=F(0),F(0)
COS=[(F(1),F(0)),(F(0),F(1,2)),ZERO,(F(0),F(-1,2)),(F(-1),F(0)),(F(0),F(-1,2)),ZERO,(F(0),F(1,2))]
def symbol(a,kx,ky):
    out=ZERO
    for dx in range(8):
        for dy in range(8):out=qa(out,qm((F(a[dx][dy]),F(0)),COS[(kx*dx+ky*dy)%8]))
    return out

def qupper(x):
    den=10**12;n=math.ceil(float(x[0]+x[1]*F.from_float(math.sqrt(2)))*den)
    while qsign(qs((F(n,den),F(0)),x))<0:n+=1
    while qsign(qs((F(n-1,den),F(0)),x))>=0:n-=1
    return F(n,den)

def inspect_ground(rec,g):
    assert rec['nx']==rec['ny']==8 and rec['N_dimers']==64 and F(rec['coupling'])==g
    G,K=ground_gk(8,8,g,load(HERE/'results/geometry_fs_8x8.json'))
    selected=independent_columns(G);assert selected==rec['selected_basis_indices']
    G,K=[a[np.ix_(selected,selected)] for a in [G,K]]
    assert G.tolist()==rec['gram'] and K.tolist()==rec['shifted_hamiltonian_numerator']
    assert len(selected)==rec['trial_subspace_dimension']==29
    c=np.array(rec['coefficients'],dtype=object);norm=int(c@G@c);mean=F(int(c@K@c),4*g.denominator*norm)
    assert norm>0 and F(rec['E00'])==-48 and rec['integer_matrix_denominator']==4*g.denominator
    assert set(rec)<=set('nx ny N_dimers s coupling E00 gram_common_factor_removed gram shifted_hamiltonian_numerator integer_matrix_denominator coefficients trial_subspace_dimension basis selected_basis_indices artifact_role historical_source historical_source_sha256'.split())
    return mean-48,dict(norm=str(norm),shifted_rayleigh=str(mean),energy_rayleigh=str(mean-48),G_K_rebuilt_without_H2=True,trial_linear_dimension=29,retained_trial_count=1)

def inspect_triplet(rec,g):
    assert rec['nx']==rec['ny']==8 and rec['N']==64 and F(rec['g'])==g and rec['spin_multiplicity']==3
    assert set(rec)<=set('nx ny N g matrix_denominator column_rule G A artifact_role spin_multiplicity historical_source historical_source_sha256'.split())
    arrays,stats=triplet_ga(g)
    assert arrays==[[[int(x) for x in row] for row in rec[k]] for k in ['G','A']]
    den=4*g.denominator;assert den==rec['matrix_denominator'];levels=[];modes=[]
    for kx in range(8):
        for ky in range(8):
            gram,first=[symbol(a,kx,ky) for a in arrays];assert qsign(gram)>0
            th=qd(first,qm((F(den),F(0)),gram));up=qupper(th);levels.append((3,up-48))
            modes.append(dict(momentum=[kx,ky],theta_exact=list(map(str,th)),theta_upper=str(up)))
    return levels,modes,stats
