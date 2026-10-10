#!/usr/bin/env python3
"""Independent ordinary-bilayer interval audit. No producer imports or eigensolvers.
Exact physical matrix assembly from previously independently rebuilt geometry;
independent dyadic exponential enclosures and rational scalar replay.
"""
import os,resource
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[key]='1'
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import sys,json,math,hashlib,itertools,time
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
from functools import lru_cache
import numpy as np
HERE=Path(__file__).resolve().parent
SRC=HERE/'snapshot'
GRID=1<<512

def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,obj):
    (HERE/'results'/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def floor(x,d=GRID):x=F(x);return F(x.numerator*d//x.denominator,d)
def ceil(x,d=GRID):return -floor(-x,d)
def frs(seq):return list(map(F,seq))
def eqseq(a,b):assert list(a)==frs(b),(a,b)
def arr(a):return np.array([[F(x) for x in row] for row in a],dtype=object)
def zero(m,n):return np.full((m,n),F(0),dtype=object)
def poly(a,x):return sum((c*x**i for i,c in enumerate(a)),F(0))

@lru_cache(None)
def expi(x):
    """112 terms, 512-bit directed arithmetic, reduced to |x|<=1/16."""
    x=F(x);y=abs(x);k=0
    while y>F(1,16):y/=2;k+=1
    lo=hi=tl=th=F(1)
    for j in range(1,113):
        tl=floor(tl*y/j);th=ceil(th*y/j);lo+=tl;hi+=th
    hi+=ceil((th*y/113)/(1-y/114))
    for _ in range(k):lo=floor(lo*lo);hi=ceil(hi*hi)
    assert 0<lo<=hi
    return (lo,hi) if x>=0 else (floor(1/hi),ceil(1/lo))

def sqrtlo(x,digits):
    x=F(x);assert x>=0;d=10**digits;n=math.isqrt(x.numerator*d*d//x.denominator)
    r=F(n,d);assert r*r<=x<(r+F(1,d))**2
    return r

def graph(nx,ny):
    ed=Counter()
    for a in range(nx*ny):
        x,y=divmod(a,ny)
        for b in [((x+1)%nx)*ny+y,x*ny+(y+1)%ny]:ed[tuple(sorted((a,b)))]+=1
    orbits=[];keys={}
    for a,b in itertools.combinations(range(nx*ny),2):
        x,y=divmod(a,ny);xx,yy=divmod(b,ny)
        d=(min((x-xx)%nx,(xx-x)%nx),min((y-yy)%ny,(yy-y)%ny))
        if nx==ny:d=tuple(sorted(d))
        if d not in keys:keys[d]=len(orbits);orbits.append([])
        orbits[keys[d]].append((a,b))
    return ed,orbits

def matrix_at(nx,ny,g,geom,second):
    """Assemble exact <B|H'|B> and, only if needed, <H'B|H'B>.
    H'=Q+gV. Basis = vacuum, pair orbits, and g-independent A42 pair orbits.
    The full image includes q=0,2,4,6; q=6 enters through W, not a truncation.
    """
    ed,orbits=graph(nx,ny);d=len(orbits)+1;q=d-1;h=g/2
    D=np.diag([F(1)]+[F(3*len(o)) for o in orbits]).astype(object)
    C=zero(d,d)
    for col in range(d):
        out=defaultdict(F);vac=F(0)
        if col==0:
            for pair,mul in ed.items():out[pair]+=h*mul
        else:
            for i,j in orbits[col-1]:
                out[i,j]+=2-2*h*ed.get((i,j),0);vac+=3*h*ed.get((i,j),0)
                for (a,b),mul in ed.items():
                    for source,target,other in [(a,b,j),(b,a,j),(a,b,i),(b,a,i)]:
                        hit=i if other==j else j
                        if source==hit and target!=other:out[tuple(sorted((target,other)))]+=h*mul
        C[0,col]=vac
        for row,orb in enumerate(orbits,1):
            values={out[pair] for pair in orb};assert len(values)==1
            C[row,col]=values.pop()
    fm=arr(geom['F']);sm=arr(geom['S']);E=np.vstack([zero(1,q),fm])
    G=np.block([[D,zero(d,q)],[zero(q,d),fm]])
    K=np.block([[D@C,h*E],[h*E.T,4*fm+h*sm]])
    assert np.array_equal(G,G.T) and np.array_equal(K,K.T)
    if not second:return G,K,None
    I=np.vstack([zero(1,q),np.eye(q,dtype=object)])
    Ediv=np.array([[E[i,j]/D[i,i] for j in range(q)] for i in range(d)],dtype=object)
    U=np.column_stack([C,h*Ediv]);J=U.T@D@U
    J[:d,:d]+=h*h*I@fm@I.T
    J[:d,d:]+=h*I@(4*fm+h*sm)
    J[d:,:d]+=h*(4*fm+h*sm.T)@I.T
    J[d:,d:]+=16*fm+4*h*(sm+sm.T)+h*h*(arr(geom['V'])+arr(geom['W']))
    assert np.array_equal(J,J.T)
    return G,K,J

def columns(G):
    a=G.copy();ids=[]
    for i in range(len(a)):
        p=a[i,i];assert p>=0
        if p:
            ids.append(i)
            for j in range(i+1,len(a)):
                for k in range(i+1,len(a)):a[j,k]-=a[j,i]*a[i,k]/p
        else:assert all(a[i,k]==0 for k in range(i,len(a)))
    return ids

def check_local_parity():
    # Reconstruct the two-rung exchange from four physical spin-half sites.
    # Columns are unnormalized singlet, t-, t0, t+; their positive metric
    # does not affect which total-triplet-parity matrix entries vanish.
    p=np.array([[0,1,0,0],[-1,0,1,0],[1,0,1,0],[0,0,0,1]],dtype=object)
    pp=np.kron(p,p);v=zero(16,16)
    for col in range(16):
        bits=[(col>>(3-j))&1 for j in range(4)]
        for i,j in [(0,2),(1,3)]:
            v[col,col]+=F((2*bits[i]-1)*(2*bits[j]-1),4)
            if bits[i]!=bits[j]:v[col^(1<<(3-i))^(1<<(3-j)),col]+=F(1,2)
    first=pp.T@v@pp;count=lambda i:int(i//4!=0)+int(i%4!=0)
    transitions=Counter()
    for i in range(16):
        for j in range(16):
            if first[i,j]:
                assert (count(i)-count(j))%2==0
                transitions[count(i)-count(j)]+=1
    assert set(transitions)=={-2,0,2}
    save('local_parity.json',dict(physical_kernel_rebuilt=True,nonzero_number_changes=dict(transitions),vacuum_pair_and_four_triplet_trial_parity='even'))


def audit_models():
    models=[];reports=[]
    for nx,ny in [(4,4),(8,4),(8,8)]:
        second=nx*ny<64;name=f'{nx}x{ny}'
        geom=load(HERE/'inputs'/f'geometry_{name if second else "fs_"+name}.json')
        if not second:assert set(geom)=={'N','orbits','all_q4','F','S'}
        G,K0,J0=matrix_at(nx,ny,F(0),geom,second)
        _,Kp,Jp=matrix_at(nx,ny,F(1),geom,second)
        ids=columns(G);sub=lambda a:a[np.ix_(ids,ids)]
        kc=[sub(K0),sub(Kp-K0)]
        if second:
            _,_,Jm=matrix_at(nx,ny,F(-1),geom,True)
            jc=[sub(J0),sub((Jp-Jm)/2),sub((Jp+Jm)/2-J0)]
        else:jc=None
        r=load(SRC/f'model_{name}.json');G=sub(G)
        assert G.tolist()==r['G'] and ids==r['selected_basis_indices']
        assert len(ids)==r['trial_dimension']==(11 if nx==ny==4 else 29)
        assert r['geometry']==[nx,ny] and r['N']==nx*ny and r['physical_spins']==2*nx*ny
        assert r['full_hilbert_dimension']==4**(nx*ny)
        assert int(r['gram_common_factor_removed'])==2**(nx*ny)
        assert r['basis']=='B vacuum/pair orbits, followed by g-independent L=A42 pair orbit vectors; inner products divided by 2**N'
        for a,b in zip(kc,r['first_moment_coefficients']):assert np.array_equal(a,arr(b))
        assert len(r['first_moment_coefficients'])==2
        if second:
            assert len(r['full_second_moment_coefficients'])==3
            for a,b in zip(jc,r['full_second_moment_coefficients']):assert np.array_equal(a,arr(b))
        else:assert 'full_second_moment_coefficients' not in r
        models.append((G,kc,jc));reports.append(dict(geometry=[nx,ny],trial_dimension=len(ids),selected_columns=ids,G_equal=True,K0_K1_equal=True,full_J0_J1_J2_equal=second,largest_second_moment_not_formed=not second))
    save('matrix_reconstruction.json',reports)
    return models

def reference(N,g,q):
    C=F(3*N,8)
    return C*(2*g-1)+(C+q)*sqrtlo(1-4*g,60)

def check_trial(t,model,lo,hi):
    G,K,J=model;c=np.array(t['integer_coefficients'],dtype=object)
    assert len(c)==len(G) and all(type(x) is int for x in c)
    norm=c@G@c;assert norm>0 and norm==F(t['integer_metric_norm'])
    rho=[F(c@a@c)/norm for a in K];eqseq(rho,t['rayleigh_coefficients'])
    assert F(t['center'])==(lo+hi)/2
    if J is None:
        assert not any('residual' in key or 'second_moment' in key for key in t)
        return rho,None
    h2=[F(c@a@c)/norm for a in J];eqseq(h2,t['full_second_moment_coefficients'])
    var=[h2[0]-rho[0]**2,h2[1]-2*rho[0]*rho[1],h2[2]-rho[1]**2]
    eqseq(var,t['full_residual_squared_coefficients'])
    assert var[0]>=0 and var[2]>=0 and 4*var[0]*var[2]>=var[1]**2
    ve=[poly(var,g) for g in [lo,hi]];eqseq(ve,t['residual_endpoint_values'])
    vmax=max(ve);assert vmax==F(t['residual_squared_max'])
    ends=[[reference(t['N'],g,q)-poly(rho,g) for g in [lo,hi]] for q in range(1,t['N']+1)]
    for a,b in zip(ends,t['reference_minus_rayleigh_endpoint_lowers']):eqseq(a,b)
    lower=[min(v) for v in ends];eqseq(lower,t['reference_minus_rayleigh_uniform_lowers'])
    assert len(ends)==len(t['reference_minus_rayleigh_endpoint_lowers'])==len(t['reference_minus_rayleigh_uniform_lowers'])
    assert lower[0]>0 and lower[0]==F(t['ground_identification_margin'])
    assert lower[1]>0 and lower[1]==F(t['even_Temple_denominator'])
    width=vmax/lower[1];assert width==F(t['uniform_Temple_width'])
    return rho,dict(width=width,lower=lower,variance=var,minimum_ground_margin=lower[0],even_denominator=lower[1])

def upper(N,p,beta,saved):
    counts=[math.comb(3*N+q-1,q) for q in range(N+1)]
    assert counts[0]==1 and counts[1]==3*N
    assert sum(counts)==math.comb(4*N,N)>=4**N
    ground=expi(beta*p['width'])[1]
    tail=sum((counts[q]*expi(-beta*p['lower'][q-1])[1] for q in range(1,N+1)),F(0))
    assert saved['retained_states']==1 and saved['reference_q_range']==[1,N] and F(saved['beta'])==beta
    assert F(saved['normalized_ground_upper'])>=ground and F(saved['normalized_tail_upper'])>=tail
    assert F(saved['normalized_trace_upper'])==F(saved['normalized_ground_upper'])+F(saved['normalized_tail_upper'])
    assert F(saved['normalized_trace_upper'])>=ground+tail
    return ground+tail

def purity(z):assert 0<z<=1;return 1-(1-z)**2/(2*z*z)

def one(s,t):
    p=s*s*t;assert p>F(1,2)
    w=(1+sqrtlo(2*p-1,40))/2;r=(1-w)/w;d=t/(1+r*r)
    ans=floor((1-r)*min(s*sqrtlo(d,40),d),10**40)
    return ans,dict(p=p,dominant_weight_lower=w,tail_ratio_upper=r,d_lower=d,purity_lower=ans)

def window(abc,row,beta,n):
    a,b,c=abc;assert b>F(1,2)
    sx=a*a*sqrtlo(2*b-1,40);ty,y=one(b,c);thermal,x=one(sx,ty)
    assert thermal==F(row['thermal_lower']) and F(1,2)<thermal<1
    assert row['n']==n and row['through']==2*n and F(row['beta'])==beta
    detail=row['details'];assert F(detail['spatial_lower'])==sx and F(detail['transverse_thermal_lower'])==ty
    for key,sub in [('x',x),('y',y)]:
        for k,v in sub.items():assert F(detail[key][k])==v
    gap=F(row['gap_lower']);assert gap>0 and expi(beta*gap)[1]*(1-thermal)<thermal
    return gap

def audit_record(r,models):
    lo,hi=frs(r['coupling_interval']);assert 0<=lo<hi<=F(7,100)
    assert F(r['fixed_vector_center'])==(lo+hi)/2
    trials=r['denominator_patches']+[r['largest_first_moment_trial']]
    assert len(trials)==3
    rr=[];pp=[]
    for t,m,shape in zip(trials,models,[(4,4),(8,4),(8,8)]):
        assert t['geometry']==list(shape) and t['N']==math.prod(shape) and t['trial_dimension']==len(m[0])
        rho,p=check_trial(t,m,lo,hi);rr.append(rho);pp.append(p)
    energies={}
    for name,weights in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
        s=r['correlated_energy_combinations'][name]
        assert s['weights']==weights
        assert sum(F(-3*math.prod(shape),4)*w for shape,w in zip([(4,4),(8,4),(8,8)],weights))==0
        coeff=[sum(weights[i]*rr[i][j] for i in range(3)) for j in range(2)]
        ends=[poly(coeff,x) for x in [lo,hi]];eqseq(coeff,s['affine_coefficients']);eqseq(ends,s['endpoint_values'])
        energies[name]=min(ends);assert F(s['uniform_lower'])==energies[name]
    beta=F(r['beta_initial']);assert beta>0
    assert len(r['trace_upper_certificates'])==3
    us=[upper(N,p,b,s) for N,p,b,s in zip([16,16,32],[pp[0],pp[0],pp[1]],[beta,2*beta,2*beta],r['trace_upper_certificates'])]
    j1=floor(expi(beta*energies['J1'])[0]/us[0]**8,10**18)
    j2=floor(expi(beta*energies['J2'])[0]/us[1]**8,10**18)
    c0=floor(expi(beta*energies['C0'])[0]/us[2]**2,10**18)
    eqseq([j1,j2,c0],[r['J1'],r['J2'],r['C0']])
    a=floor(purity(j1),10**18);b=floor(purity(j2*a),10**18);c=floor(purity(c0**4*a*a*b),10**18)
    eqseq([a,b,c],r['permuted_first_purities']);assert min(a,b,c)>0
    abc=[floor(x,10**18) for x in [a*sqrtlo(b,60),a*a*b*sqrtlo(c,60),a**4*b*b*c]]
    eqseq(abc,r['canonical_first_purities'])
    boot=r['bootstrap'];assert boot['status']=='accepted_analytic_scalar_certificate' and r['accepted']
    inp=boot['input'];eqseq(abc,[inp[x] for x in ['A_lower','B_lower','C_lower']]);assert inp['n']==inp['m']==8 and F(inp['beta'])==2*beta
    defects=[ceil(1-z,10**18) for z in abc];states=[abc];n=8;bb=2*beta
    for i,update in enumerate(boot['updates'],1):
        assert max(defects)>F(1,500) and update['round']==i
        for _ in range(3):
            p=(1-defects[0])**4*(1-defects[1])**2*(1-defects[2]);new=ceil((1-p)**2/(2*p*p),10**18)
            assert 0<=new<1;defects=defects[1:]+[new]
        eqseq(defects,update['defects']);states.append([1-x for x in defects]);n*=2;bb*=2
    assert n==boot['n']==boot['m'] and bb==F(boot['beta']) and len(boot['updates'])==boot['rounds']
    eqseq(defects,boot['defects']);u=max(defects);assert 0<u<=F(1,500) and u==F(boot['u'])
    asym=F(boot['uniform_square_gap_lower']);assert asym>0 and expi(bb*asym)[1]*32*u<1
    assert len(states)==len(r['finite_windows'])
    gaps=[window(state,row,2*beta*2**j,8*2**j) for j,(state,row) in enumerate(zip(states,r['finite_windows']))]
    shorts=[];assert len(r['short_sizes'])==6
    for L,s in zip(range(2,8),r['short_sizes']):
        ed,_=graph(L,L);N=L*L;S=sum(w*w for w in ed.values());assert S==(16 if L==2 else 2*N)
        C=F(3*S,16);ell=C*(2*hi-1)+(C+1)*sqrtlo(1-4*hi,60)
        assert ell>0 and s['L']==L and s['N']==N and s['edge_square_sum']==S
        assert ell==F(s['lambda2_shifted_lower'])==F(s['gap_lower']) and F(s['ground_Rayleigh_upper'])==0
        shorts.append(ell)
    target=min([asym]+shorts+[g for g,row in zip(gaps,r['finite_windows']) if row['n']<n])
    assert target==F(r['all_integer_L_ge2_gap'])>0
    expi.cache_clear()
    return dict(coupling_interval=[str(lo),str(hi)],beta_initial=str(beta),all_integer_L_ge2_gap=str(target),gap_display=float(target),asymptotic_onset=n,bootstrap_rounds=boot['rounds'],finite_window_count=len(gaps),finite_window_gap_lowers=list(map(str,gaps)),short_size_gap_lowers=list(map(str,shorts)),minimum_ground_identification_margin=str(min(p['minimum_ground_margin'] for p in pp[:2])),minimum_even_Temple_denominator=str(min(p['even_denominator'] for p in pp[:2])),fixed_vectors_rebuilt=3,denominator_full_residuals_rebuilt=2)

def verify_inputs():
    manifest=load(HERE/'INPUT_SHA256.json')
    for rel,h in manifest.items():assert sha(HERE/rel)==h,rel
    frozen=load(HERE/'PRODUCER_FREEZE.json')
    assert sha(HERE/'PRODUCER_FREEZE.json')=='bf38883ef54e3bf0e5d80e1abcac8b9a21355106382d546d27cb413b3734c8c3'
    for rel,h in frozen['files'].items():assert sha(SRC/rel)==h,rel
    for name,rec in load(HERE/'INHERITED_REVIEWS.json').items():
        p=HERE.parent/name/'MANIFEST_SHA256.json';assert sha(p)==rec['manifest_sha256']
        for rel,h in load(p).items():assert sha(p.parent/rel)==h,(name,rel)
    for copied,original in [
        ('geometry_4x4.json','large_seed_review/results/geometry_4x4.json'),
        ('geometry_8x4.json','large_seed_review/results/geometry_8x4.json'),
        ('geometry_fs_8x8.json','reduced_input_review/results/geometry_fs_8x8.json')]:
        assert sha(HERE/'inputs'/copied)==sha(HERE.parent/original)
    return len(manifest)

def main():
    start=time.monotonic();checked=verify_inputs();check_local_parity();models=audit_models();summary=load(SRC/'coverage_summary.json')
    assert summary['coupling_interval']==['0','7/100'] and summary['closed_intervals']==len(summary['intervals'])==16
    assert summary['largest_trace_rank']==1 and summary['denominator_retained_states']==[1,1]
    assert summary['trial_dimensions']==[11,29,29] and summary['largest_physical_spins']==128 and summary['largest_full_dimension']==4**64
    assert summary['largest_residual_required'] is False and summary['maximum_full_residual_geometry']==[8,4]
    previous=F(0);reports=[]
    for i,entry in enumerate(summary['intervals'],1):
        assert entry['file']==f'coverage/interval_{i:03d}.json'
        r=load(SRC/entry['file']);lo,hi=frs(r['coupling_interval']);assert lo==previous;previous=hi
        assert r['coupling_interval']==entry['coupling_interval'] and r['all_integer_L_ge2_gap']==entry['gap_lower'] and r['beta_initial']==entry['beta_initial']
        report=audit_record(r,models);reports.append(report);print('PASS',i,r['coupling_interval'],report['gap_display'],flush=True)
    assert previous==F(7,100)
    gap=min(F(r['all_integer_L_ge2_gap']) for r in reports);assert gap==F(summary['all_integer_L_ge2_uniform_gap'])==F(486442811,250000000000)
    assert F(summary['zero_coupling_exact_gap'])==1
    # Independent exact endpoint constants used in the inherited all-integer theorem.
    u=F(1,500);assert 49/(2*(1-7*u)**2)<32 and 32*u<1 and 5*u<=F(1,100) and 20/(1-20*u)<=32
    result=dict(status='PASS independent exact fixed-vector, whole-space trace, parity-Temple, interval and all-integer-size review',coupling_interval=['0','7/100'],closed_intervals=16,all_integer_L_ge2_uniform_gap=str(gap),uniform_gap_display=float(gap),unique_finite_volume_ground=True,zero_coupling_exact_gap='1',trial_dimensions=[11,29,29],denominator_retained_states=[1,1],largest_trace_rank=1,largest_full_dimension=str(4**64),largest_physical_spins=128,largest_second_moment_formed=False,full_residual_geometry_max=[8,4],producer_modules_imported=0,eigensolver_calls=0,verified_snapshot_inputs=checked,intervals=reports,runtime_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)),address_space_cap_bytes=1024**3,blas_threads=1)
    save('SUMMARY.json',result);print('PASS ALL',gap,'seconds',result['runtime_seconds'],'RSS KiB',result['peak_rss_kib'],flush=True)
if __name__=='__main__':main()
