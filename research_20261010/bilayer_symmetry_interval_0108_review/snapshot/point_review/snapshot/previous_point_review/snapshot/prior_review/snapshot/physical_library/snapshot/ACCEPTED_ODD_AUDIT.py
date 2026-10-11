#!/usr/bin/env python3
"""Independent fixed-center odd-band interval audit; no producer code imports.
Ground assembly, directed scalar arithmetic and the joint recurrence are reused
from explicitly pinned independent reviews. New odd reconstruction is written
here; all source and helper hashes are checked before import.
"""
import os,resource,sys
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:os.environ[k]='1'
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import json,hashlib,math,time,importlib.util,ast,copy,itertools
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
HERE=Path(__file__).resolve().parent;RES=HERE.parent;ROOT=RES.parent;SRC=HERE/'snapshot'
FREEZE='cd21cbf09698816bf8cb096fe1680c89dff47ba5a895b1bedc1693ed2bec56dc'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,obj):(HERE/'results'/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def manifest(p,expected):
    assert sha(p)==expected,('manifest',str(p));r=load(p);files=r.get('files',r)
    for k,v in files.items():assert sha(p.parent/k)==v,('sealed file',str(p.parent/k))
    return len(files)
def verify():
    assert sha(HERE/'PRODUCER_FREEZE.json')==FREEZE
    assert manifest(RES/'interval_range_0085/FROZEN_MANIFEST.json',FREEZE)==52
    for p,h in load(HERE/'PRODUCER_FREEZE.json')['files'].items():assert sha(SRC/p)==h
    gates=load(HERE/'ACCEPTANCE_GATES.json');assert gates['producer_manifest_sha256']==FREEZE
    pins={'interval_joint_review':'cc57b7779f77d91164ec68d612979817846a1ec91a66ab45c86b243becdabc8d','joint_ratio_review':'18fd9df56ad4023b2f174a3a54d122550670dcf0863176270cd000d48c00fe91','bilayer_polynomial_frontier_review':'9cb0484af6d424e74e5520d8d995c88d63ab2c6396938634b98acf3927684930'}
    rows=[]
    for r in gates['reviews']:
        assert r['folder'] not in pins or r['sha256']==pins[r['folder']]
        n=manifest(RES/r['folder']/r['manifest'],r['sha256']);assert n==r['file_count'];rows.append(dict(**r,verified_files=n))
    assert pins.keys()<=set(r['folder'] for r in rows)
    inputs=load(SRC/'INPUT_SHA256.json')
    for p,h in inputs.items():assert sha(ROOT/p)==h,('direct dependency',p)
    accepted=load(RES/'bilayer_polynomial_frontier_review/PHYSICAL_ACCEPTANCE.json')
    assert accepted['status']=='PASS independently accepted reusable polynomial moments and finite-seed certificates'
    assert accepted['stored_to_physical_divisors']=={'G':'4*d^2','A':'4*d^3','B':'4*d^4'}
    assert sha(RES/'bilayer_polynomial_frontier_review'/accepted['coefficients_file'])==accepted['coefficients_sha256']
    lemma=load(RES/'joint_ratio_review/LEMMA_ACCEPTANCE.json');assert lemma['status']=='PASS independent analytic and exact-arithmetic scalar audit'
    return dict(frozen_files=52,direct_inputs=len(inputs),inherited_seals=rows,required_pins=pins)
SOURCES=verify()
p=RES/'interval_joint_review/audit_joint_interval.py'
spec=importlib.util.spec_from_file_location('accepted_joint_audit',p);J=importlib.util.module_from_spec(spec);spec.loader.exec_module(J)
E=J.E
frs=E.frs;floor=E.floor;ceil=E.ceil;sqrtlo=E.sqrtlo;expi=E.expi;poly=E.poly;eqseq=E.eqseq;Q18=10**18
# No functions from a producer module are imported or executed.

def models_rebuilt():
    result=[];report=[]
    for nx,ny in [(4,4),(8,4),(8,8)]:
        label=f'{nx}x{ny}';geom=load(E.HERE/'inputs'/f'geometry_{label}.json')
        G,K0,J0=E.matrix_at(nx,ny,F(0),geom,True);_,K1,J1=E.matrix_at(nx,ny,F(1),geom,True);_,_,Jm=E.matrix_at(nx,ny,F(-1),geom,True)
        ids=E.columns(G);ix=E.np.ix_(ids,ids);G=G[ix];K=[K0[ix],(K1-K0)[ix]];B=[J0[ix],((J1-Jm)/2)[ix],((J1+Jm)/2-J0)[ix]]
        r=load(E.HERE/'inputs/auxiliary'/f'matrix_polynomial_{label}.json')
        assert ids==r['selected_basis_indices'] and len(ids)==r['trial_dimension']==(11 if nx*ny==16 else 29)
        assert E.np.array_equal(G,E.arr(r['gram']))
        for cs,key in [(K,'shifted_A_coefficients'),(B,'full_shifted_B_coefficients')]:
            assert len(cs)==len(r[key])
            for a,b in zip(cs,r[key]):assert E.np.array_equal(a,E.arr(b))
        result.append((G,K,B));report.append(dict(geometry=[nx,ny],trial_dimension=len(ids),full_H2_includes_q6=True,geometry_sha256=sha(E.HERE/'inputs'/f'geometry_{label}.json'),matrix_polynomial_sha256=sha(E.HERE/'inputs/auxiliary'/f'matrix_polynomial_{label}.json')))
    save('ground_matrix_reconstruction.json',report);return result

# Independent Q(sqrt(2)) arithmetic, represented by a pair of rationals.
Z=(F(0),F(0));ONE=(F(1),F(0))
def q(a):return (F(a),F(0))
def qa(a,b):return (a[0]+b[0],a[1]+b[1])
def qs(a,b):return (a[0]-b[0],a[1]-b[1])
def qm(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def qd(a,b):
    norm=b[0]*b[0]-2*b[1]*b[1];assert norm
    return qm(a,(b[0]/norm,-b[1]/norm))
def sign(x):
    a,b=x
    if not b:return (a>0)-(a<0)
    if not a:return (b>0)-(b<0)
    if a*b>0:return (a>0)-(a<0)
    return ((a*a>2*b*b)-(a*a<2*b*b))*((a>0)-(a<0))
def bounds(x,bits=160):
    d=2**bits;lo=F(math.isqrt(2*d*d),d);hi=lo+F(1,d);assert lo*lo<2<hi*hi
    a,b=x;return (a+b*lo,a+b*hi) if b>=0 else (a+b*hi,a+b*lo)
def qpoly(c,x):
    v=Z
    for a in reversed(c):v=qa(qm(v,q(x)),a)
    return v
def qlist(row):return [tuple(map(F,x)) for x in row]
COS=[ONE,(F(0),F(1,2)),Z,(F(0),F(-1,2)),q(-1),(F(0),F(-1,2)),Z,(F(0),F(1,2))]
def symbol(arr,nx,ny,kx,ky):
    ans=Z
    for i in range(nx):
        for j in range(ny):ans=qa(ans,qm(q(arr[i][j]),COS[((8*kx*i)//nx+(8*ky*j)//ny)%8]))
    return ans

def fit(xs,ys):
    """Independent full-degree Newton difference table, using reversed points."""
    dd=list(ys);cs=[F(0)]*len(xs);basis=[F(1)]
    for k in range(len(xs)):
        for j,b in enumerate(basis):cs[j]+=dd[0]*b
        dd=[(dd[j+1]-dd[j])/(xs[j+k+1]-xs[j]) for j in range(len(dd)-1)]
        nxt=[F(0)]*(len(basis)+1)
        for j,b in enumerate(basis):nxt[j]-=xs[k]*b;nxt[j+1]+=b
        basis=nxt
    return cs

def oldpath(nx,ny,g):
    folder='low_band/translation_band' if g<F(3,50) else 'low_band/frontier_g006' if g==F(3,50) else 'low_band/frontier_g007_g010/g'+str(g).replace('/','d')
    return RES/folder/(f'translated_{nx}x{ny}_g{g}_moments.json'.replace('/','d'))
def decompose(gg,aa,bb):
    assert len(gg)==3 and len(aa)==4 and len(bb)==5
    assert gg[1]==0 and aa[0]==bb[0]==gg[0] and bb[1]==2*aa[1]
    v=[aa[1],aa[2]-3*gg[2],aa[3]];c=[2*v[0],4*v[1],6*v[2]]
    d=[bb[2]-9*gg[2]-c[1],bb[3]-c[2],bb[4]]
    return v,c,d

def odd_polynomials():
    accepted=load(RES/'bilayer_polynomial_frontier_review/results/polynomial_coefficients.json')
    out={};nchecks=extras=symmetry=diagonal=0
    for nx,ny in [(4,4),(8,4)]:
        xs=list(reversed(list(map(F,['3/100','1/25','1/20','3/50','7/100','2/25','1/10']))));records=[load(oldpath(nx,ny,g)) for g in xs]
        raw=load(SRC/f'odd_polynomial_{nx}x{ny}.json');assert (raw['nx'],raw['ny'],raw['N'])==(nx,ny,nx*ny)
        assert raw['degrees']=={'G':2,'A':3,'B':4} and raw['normalization']=={'G':'4*d^2','A':'4*d^3','B':'4*d^4'}
        for x,r in zip(xs,records):assert (r['nx'],r['ny'],r['N'],F(r['g']),r['matrix_denominator'])==(nx,ny,nx*ny,x,4*x.denominator)
        for rel,h in raw['source_sha256'].items():assert sha(RES/rel)==h
        cs={}
        for key,degree,power in [('G',2,2),('A',3,3),('B',4,4)]:
            cs[key]=[[None]*ny for _ in range(nx)]
            for i in range(nx):
                for j in range(ny):
                    ys=[F(int(r[key][i][j]),4*r['matrix_denominator']**power) for r in records]
                    coeff=fit(xs,ys);assert not any(coeff[degree+1:]);coeff=coeff[:degree+1]
                    assert coeff==fit(xs[:degree+1],ys[:degree+1])
                    assert coeff==frs(raw['coefficient_arrays'][key][i][j])==frs(accepted[f'{nx}x{ny}'][key][i][j])
                    for x,y in zip(xs,ys):assert poly(coeff,x)==y;nchecks+=1
                    extras+=7-degree-1;cs[key][i][j]=coeff
            for i in range(nx):
                for j in range(ny):assert cs[key][i][j]==cs[key][(-i)%nx][(-j)%ny];symmetry+=1
        for i in range(nx):
            for j in range(ny):
                gg,aa,bb=[cs[key][i][j] for key in ['G','A','B']];v,c,d=decompose(gg,aa,bb)
                for z in map(F,['0','-1/3','3/100','17/200','1/10']):
                    assert gg[0]+z*z*gg[2]==poly(gg,z)
                    assert gg[0]+3*z*z*gg[2]+z*poly(v,z)==poly(aa,z)
                    assert gg[0]+9*z*z*gg[2]+z*poly(c,z)+z*z*poly(d,z)==poly(bb,z);diagonal+=3
        assert raw['exact_source_evaluation_checks']==21*nx*ny
        out[nx,ny]=cs
    assert nchecks==1008 and extras==432
    save('odd_polynomial_reconstruction.json',dict(source_evaluations=nchecks,extra_point_checks=extras,displacement_Hermitian_checks=symmetry,diagonal_recovery_checks=diagonal,coefficients={f'{nx}x{ny}':v for (nx,ny),v in out.items()},method='reversed seven-point Newton with exact degree truncation; match independent accepted coefficients'))
    return out
ODD=None

def fixed_arrays(nx,ny,z):
    raw=ODD[nx,ny];out={k:[[F(0)]*ny for _ in range(nx)] for k in ['G','Q','V','Q2','C','D']}
    for i in range(nx):
        for j in range(ny):
            gg,aa,bb=[raw[k][i][j] for k in ['G','A','B']];v,c,d=decompose(gg,aa,bb)
            values=[poly(gg,z),gg[0]+3*z*z*gg[2],poly(v,z),gg[0]+9*z*z*gg[2],poly(c,z),poly(d,z)]
            for key,value in zip(out,values):out[key][i][j]=value
    return out
ODD_REPORTS=[]
def check_odd(t,rho,lo,hi):
    nx,ny=t['geometry'];N=nx*ny;z=(lo+hi)/2;b=t['odd_band'];assert (nx,ny) in [(4,4),(8,4)]
    assert F(b['fixed_center'])==z and b['q_components']==[1,3] and b['per_spin_projection_dimension']==N and b['spin_multiplicity']==3 and b['retained_odd_dimension']==3*N and b['all_modes_below_global_q2_cutoff'] is True
    assert b['trial_family']=='w_r(z)=|t+_r>−z C_create(1)|t+_r>/2'
    assert len(b['modes'])==N and [r['momentum'] for r in b['modes']]==[list(k) for k in itertools.product(range(nx),range(ny))]
    arr=fixed_arrays(nx,ny,z);lowers=[];widths=[];margins=[];sample_checks=0
    for row in b['modes']:
        kx,ky=row['momentum'];mom={k:symbol(a,nx,ny,kx,ky) for k,a in arr.items()};G=mom['G'];assert sign(G)>0 and tuple(map(F,row['gram_symbol']))==G
        theta=[qd(mom['Q'],G),qd(mom['V'],G)];second=[qd(mom[k],G) for k in ['Q2','C','D']]
        var=[qs(second[0],qm(theta[0],theta[0])),qs(second[1],qm(q(2),qm(theta[0],theta[1]))),qs(second[2],qm(theta[1],theta[1]))]
        assert theta==qlist(row['theta_coefficients']) and second==qlist(row['second_moment_coefficients']) and var==qlist(row['residual_squared_coefficients'])
        assert sign(var[0])>=0 and sign(var[2])>=0 and sign(qs(qm(q(4),qm(var[0],var[2])),qm(var[1],var[1])))>=0
        ts=[qpoly(theta,p) for p in (lo,hi)];vs=[qpoly(var,p) for p in (lo,hi)];assert all(sign(v)>=0 for v in vs)
        tb=[bounds(x) for x in ts];vb=[bounds(x) for x in vs]
        assert tb==[tuple(map(F,r)) for r in row['theta_endpoint_enclosures']] and vb==[tuple(map(F,r)) for r in row['residual_squared_endpoint_enclosures']]
        vmax=max(v[1] for v in vb);assert vmax==F(row['residual_squared_max'])
        ms=[bounds(qs(q(E.reference(N,p,2)),th))[0] for p,th in zip((lo,hi),ts)];eqseq(ms,row['cutoff_minus_theta_endpoint_lowers'])
        margin=min(ms);assert margin>0 and margin==F(row['uniform_Temple_denominator']);width=vmax/margin;assert width==F(row['uniform_Temple_width'])
        rel=[bounds(qs(th,q(poly(rho,p))))[0] for p,th in zip((lo,hi),ts)];eqseq(rel,row['theta_minus_ground_rayleigh_endpoint_lowers'])
        ell=min(rel)-width;assert ell==F(row['eigen_lower_minus_ground_rayleigh_uniform_lower'])
        # Independent diagnostic points supplement, never replace, the convexity proof.
        for j in range(9):
            p=lo+(hi-lo)*F(j,8);th=qpoly(theta,p);v=qpoly(var,p);den=qs(q(E.reference(N,p,2)),th)
            assert sign(qs(den,q(margin)))>=0 and sign(qs(q(vmax),v))>=0
            endpoint=qs(qs(th,qd(v,den)),q(poly(rho,p)));assert sign(qs(endpoint,q(ell)))>=0;sample_checks+=1
        lowers.append(ell);widths.append(width);margins.append(margin)
    counts=[math.comb(3*N+k-1,k) for k in range(N+1)];assert counts[:2]==[1,3*N]
    assert sum(counts)==math.comb(4*N,N)>=4**N and sum(counts[2:])>=4**N-(1+3*N)
    ODD_REPORTS.append(dict(geometry=[nx,ny],interval=list(map(str,(lo,hi))),center=str(z),modes=N,retained_states=1+3*N,first_omitted_ordered_index=3*N+2,reference_count=str(sum(counts)),minimum_odd_Temple_margin=str(min(margins)),maximum_odd_Temple_width=str(max(widths)),covariance_checks=N,within_interval_checks=sample_checks))
    return lowers

def check_trial(t,model,lo,hi,denominator=True):
    rho,var=E.check_trial(t,model,lo,hi,False)
    if not denominator:assert 'odd_band' not in t;return rho,var
    if hi<=F(41,500):
        label='x'.join(map(str,t['geometry']));old=load(E.HERE/'inputs/auxiliary'/f'auxiliary_{label}_g2d25.json');assert t['integer_coefficients']==old['coefficients'] and 'odd_band' not in t
    else:assert lo>=F(41,500) and 'odd_band' in t
    ve=[poly(var,p) for p in (lo,hi)];eqseq(ve,t['residual_endpoint_values']);vmax=max(ve);assert vmax==F(t['residual_squared_max'])
    ends=[[E.reference(t['N'],p,k)-poly(rho,p) for p in (lo,hi)] for k in range(1,t['N']+1)]
    assert len(ends)==len(t['reference_minus_rayleigh_endpoint_lowers'])
    for a,b in zip(ends,t['reference_minus_rayleigh_endpoint_lowers']):eqseq(a,b)
    lowers=[min(x) for x in ends];eqseq(lowers,t['reference_minus_rayleigh_uniform_lowers'])
    assert lowers[0]>0 and lowers[0]==F(t['ground_identification_margin']);assert lowers[1]>0 and lowers[1]==F(t['even_Temple_denominator'])
    width=vmax/lowers[1];assert width==F(t['uniform_Temple_width'])
    out=dict(width=width,lower=lowers,variance=var,minimum_ground_margin=lowers[0],even_denominator=lowers[1])
    if 'odd_band' in t:out['odd_lowers']=check_odd(t,rho,lo,hi)
    return rho,out

def upper(N,p,beta,saved):
    if 'odd_lowers' not in p:return E.upper(N,p,beta,saved)
    counts=[math.comb(3*N+k-1,k) for k in range(N+1)];assert sum(counts)>=4**N
    ground=expi(beta*p['width'])[1];band=3*sum((expi(-beta*x)[1] for x in p['odd_lowers']),F(0))
    tail=sum((counts[k]*expi(-beta*p['lower'][k-1])[1] for k in range(2,N+1)),F(0))
    assert saved['retained_states']==1+3*N and saved['reference_q_range']==[2,N] and saved['odd_mode_count']==N and saved['spin_multiplicity']==3 and F(saved['beta'])==beta
    terms=[F(saved[k]) for k in ['normalized_ground_upper','normalized_odd_band_upper','normalized_tail_upper']]
    assert all(x>=y for x,y in zip(terms,[ground,band,tail]))
    assert F(saved['normalized_trace_upper'])==sum(terms)>=ground+band+tail
    return ground+band+tail

# Scalar implementation copied from the pinned independent joint review.
# audit_record changes only coupling range and the physical trial/trace callbacks.

def full(abc):return abc[0]**4*abc[1]**2*abc[2]

def valid_components(x):assert len(x)==3 and all(F(0)<a<=F(1) for a in x)

def G(z):
    assert 0<z<=1
    return 1-(1-z)**2/(2*z*z)

def transport(p):
    valid_components(p);a,b,c=p
    return [floor(x,Q18) for x in [a*sqrtlo(b,60),a*a*b*sqrtlo(c,60),a**4*b*b*c]]

def canonical_next(abc,K):
    valid_components(abc);assert 0<K<=1;a,b,c=abc;args=[];out=[]
    z=max(full(abc),K);args.append(z);d=floor(G(z),Q18)
    if d<=0:return None,args
    out.append(d);z=max(b**4*c*c,K*K)*d;args.append(z);e=floor(G(z),Q18)
    if e<=0:return None,args
    out.append(e);z=max(c,K)**4*d*d*e;args.append(z);f=floor(G(z),Q18)
    if f<=0:return None,args
    out.append(f);valid_components(out);return out,args

def plain_next(p):
    if p is None:return None
    valid_components(p);out=list(p)
    for j in range(3):
        z=full(out);d=floor(G(z),Q18)
        if d<=0:return None
        out=out[1:]+[d]
    valid_components(out);return out

def one_joint(s,t,K=F(0)):
    assert 0<s<=1 and 0<t<=1 and 0<=K<=1
    p=max(s*s*t,K);assert F(1,2)<p<=1
    w=(1+sqrtlo(2*p-1,40))/2;r=(1-w)/w;d=t/(1+r*r)
    ans=floor((1-r)*min(s*sqrtlo(d,40),d),10**40)
    assert 0<ans<=1
    return ans,dict(joint_lower=K,p=p,dominant_weight_lower=w,tail_ratio_upper=r,d_lower=d)

def joint_window(abc,K,row,beta,n):
    valid_components(abc);assert 0<K<=1 and n>=8 and n%2==0
    a,b,c=abc;assert b>F(1,2);root=sqrtlo(2*b-1,40)
    sx=max(a*a*root,sqrtlo(K,40)*root/b)
    ty,inner=one_joint(b,c,K);thermal,outer=one_joint(sx,ty)
    assert F(1,2)<thermal<1 and thermal==F(row['thermal_lower'])
    assert row['n']==n and row['through']==2*n and F(row['beta'])==beta
    detail=row['details'];assert F(detail['joint_lower'])==K
    assert F(detail['spatial_lower'])==sx and F(detail['transverse_thermal_lower'])==ty
    for name,sub in [('inner',inner),('outer',outer)]:
        assert set(detail[name])==set(sub)
        for k,v in sub.items():assert F(detail[name][k])==v
    d=F(row['gap_lower']);assert d>0 and expi(beta*d)[1]*(1-thermal)<thermal
    return d

def scalar_tail(abc,beta,n,boot):
    # General retained old tail is checked even though both current records enter directly.
    valid_components(abc);inp=boot['input']
    assert boot['status']=='accepted_analytic_scalar_certificate'
    eqseq(abc,[inp[x] for x in ['A_lower','B_lower','C_lower']])
    assert inp['n']==inp['m']==n and F(inp['beta'])==beta
    defects=[ceil(1-z,Q18) for z in abc]
    for i,update in enumerate(boot['updates'],1):
        assert max(defects)>F(1,500) and update['round']==i
        for k in range(3):
            z=(1-defects[0])**4*(1-defects[1])**2*(1-defects[2]);d=ceil((1-z)**2/(2*z*z),Q18)
            assert 0<=d<1;defects=defects[1:]+[d]
        eqseq(defects,update['defects']);n*=2;beta*=2
    assert n==boot['n']==boot['m'] and beta==F(boot['beta']) and len(boot['updates'])==boot['rounds']
    eqseq(defects,boot['defects']);u=max(defects);assert 0<u<=F(1,500) and u==F(boot['u'])
    d=F(boot['uniform_square_gap_lower']);assert d>0 and expi(beta*d)[1]*32*u<1
    return d,n

def audit_record(r,models):
    lo,hi=frs(r['coupling_interval']);assert F(2,25)<=lo<hi<=F(17,200)
    assert F(r['fixed_vector_center'])==(lo+hi)/2
    trials=r['denominator_patches']+[r['largest_base_trial']];assert len(trials)==3
    rr=[];pp=[]
    for idx,(t,m,shape) in enumerate(zip(trials,models,[(4,4),(8,4),(8,8)])):
        assert t['geometry']==list(shape) and t['N']==math.prod(shape) and t['trial_dimension']==len(m[0])
        rho,p=check_trial(t,m,lo,hi,idx<2);rr.append(rho);pp.append(p)
    rr[2],filter_report=E.check_filter(r['largest_interval_filter'],rr[2],pp[2],lo,hi)
    energies={}
    for name,weights in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
        s=r['correlated_energy_combinations'][name];assert s['weights']==weights
        assert sum(F(-3*math.prod(shape),4)*w for shape,w in zip([(4,4),(8,4),(8,8)],weights))==0
        coeff=[sum(weights[i]*rr[i][j] for i in range(3)) for j in range(2)];ends=[poly(coeff,x) for x in (lo,hi)]
        eqseq(coeff,s['affine_coefficients']);eqseq(ends,s['endpoint_values']);energies[name]=min(ends);assert F(s['uniform_lower'])==energies[name]
    beta=F(r['beta_initial']);assert beta>0 and len(r['trace_upper_certificates'])==3
    us=[upper(N,p,b,s) for N,p,b,s in zip([16,16,32],[pp[0],pp[0],pp[1]],[beta,2*beta,2*beta],r['trace_upper_certificates'])]
    j1=floor(expi(beta*energies['J1'])[0]/us[0]**8,Q18);j2=floor(expi(beta*energies['J2'])[0]/us[1]**8,Q18);c0=floor(expi(beta*energies['C0'])[0]/us[2]**2,Q18)
    eqseq([j1,j2,c0],[r['J1'],r['J2'],r['C0']])
    a=floor(G(j1),Q18);b=floor(G(j2*a),Q18);c=floor(G(c0**4*a*a*b),Q18)
    per=[a,b,c];valid_components(per);eqseq(per,r['permuted_first_purities'])
    abc=transport(per);eqseq(abc,r['canonical_first_purities']);K=floor(full(per),Q18)
    assert K==F(r['initial_joint_product'])
    states=r['joint_ladder_states'];windows=r['finite_windows'];assert len(states)==len(windows)>0
    gaps=[];merges=[]
    for j,(state,row) in enumerate(zip(states,windows)):
        n=8*2**j;bb=2*beta*2**j;valid_components(abc);assert 0<K<=1
        assert state['level']==j and state['n']==n and F(state['beta'])==bb
        eqseq(abc,state['canonical']);assert K==F(state['joint_product_lower'])
        if per is None:assert state['permuted'] is None
        else:eqseq(per,state['permuted']);valid_components(per)
        gaps.append(joint_window(abc,K,row,bb,n))
        if j==len(states)-1:
            assert max(1-x for x in abc)<=F(1,500) and 'canonical_update_arguments' not in state
            break
        assert max(1-x for x in abc)>F(1,500)
        can,args=canonical_next(abc,K);eqseq(args,state['canonical_update_arguments'])
        per=plain_next(per);trans=transport(per) if per is not None else None
        assert can is not None or trans is not None
        oldK=K
        abc=trans if can is None else can if trans is None else [max(x,y) for x,y in zip(can,trans)]
        K=floor(max(full(abc),full(per) if per is not None else F(0)),Q18)
        # Both routes start and end at the same all-directions-doubled base.
        valid_components(abc);assert 0<K<=1
        merges.append(dict(from_n=n,to_n=2*n,canonical_available=can is not None,permuted_available=per is not None,canonical_selected=[can is not None and (trans is None or x>=y) for x,y in zip(can or [F(0)]*3,trans or [F(0)]*3)],previous_joint=str(oldK),new_joint=str(K)))
    asym,onset=scalar_tail(abc,bb,n,r['bootstrap']);assert onset==n # Otherwise more finite bridges would be needed.
    assert r['accepted'] is True
    shorts=[];assert len(r['short_sizes'])==6
    for L,s in zip(range(2,8),r['short_sizes']):
        ed,_=E.graph(L,L);N=L*L;S=sum(w*w for w in ed.values());assert S==(16 if L==2 else 2*N)
        C=F(3*S,16);ell=C*(2*hi-1)+(C+1)*sqrtlo(1-4*hi,60)
        assert ell>0 and s['L']==L and s['N']==N and s['edge_square_sum']==S
        assert ell==F(s['lambda2_shifted_lower'])==F(s['gap_lower']) and F(s['ground_Rayleigh_upper'])==0
        shorts.append(ell)
    target=min([asym]+shorts+[g for g,row in zip(gaps,windows) if row['n']<onset]);assert target==F(r['all_integer_L_ge2_gap'])>0
    expi.cache_clear()
    return dict(coupling_interval=list(map(str,(lo,hi))),beta_initial=str(beta),all_integer_L_ge2_gap=str(target),gap_display=float(target),asymptotic_onset=onset,joint_ladder_states=len(states),canonical_updates=len(merges),finite_window_count=len(gaps),required_finite_windows=len(gaps)-1,finite_window_gap_lowers=list(map(str,gaps)),short_size_gap_lowers=list(map(str,shorts)),minimum_ground_identification_margin=str(min(p['minimum_ground_margin'] for p in pp[:2])),minimum_even_Temple_denominator=str(min(p['even_denominator'] for p in pp[:2])),filter=filter_report,merges=merges)

def literal_definition_check():
    """Read-only AST verification of the literal producer definition; never import it."""
    p=RES/'low_band/translation_band/translated_band.py';s=p.read_text();tree=ast.parse(s)
    fun=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='moments')
    text=ast.unparse(fun)
    required=['bare = {3: 1}','Tbare = m.apply(bare)','W = {3: 2 * m.den}','W.update({st: -c for st, c in Tbare.items() if m.q(st) == 3})','TW = m.apply(W)','assert all((m.q(st) in [1, 3, 5] for st in TW))']
    for snippet in required:assert snippet in text,snippet
    model=RES/'symmetry/symmetric_ground.py';mt=ast.parse(model.read_text());cls=next(n for n in mt.body if isinstance(n,ast.ClassDef) and n.name=='Model');txt=ast.unparse(cls)
    for snippet in ['self.den = 4 * self.g.denominator','out[st] += self.den * n * c','out[st1] += c * p * m * k','return 1 << self.N - (st & self.lowmask).bit_count()']:
        assert snippet in txt,snippet
    save('literal_definition.json',dict(status='PASS literal source and previously accepted physical reconstruction',translated_source_sha256=sha(p),model_source_sha256=sha(model),trial='w_r(z)=u_r+z v_r; u_r=e_r; v_r=-P3 V e_r/2',Q_eigenvalues=[1,3],v_has_Q1_component=False,physical_metric_independent_of_g=True,integer_to_physical_scaling=['4*d^2','4*d^3','4*d^4'],operator_identity_for_all_real_trial_and_physical_parameters=True))

def verify_reused_functions():
    original=Path(J.__file__).read_text();ours=Path(__file__).read_text()
    names=['full','valid_components','G','transport','canonical_next','plain_next','one_joint','joint_window','scalar_tail','audit_record'];verified=[]
    source={n.name:n for n in ast.parse(original).body if isinstance(n,ast.FunctionDef)}
    target={n.name:n for n in ast.parse(ours).body if isinstance(n,ast.FunctionDef)}
    for name in names:
        txt=ast.get_source_segment(original,source[name])
        if name=='audit_record':txt=txt.replace('F(39,500)<=lo<hi<=F(2,25)','F(2,25)<=lo<hi<=F(17,200)').replace('E.check_trial(', 'check_trial(').replace('E.upper(', 'upper(')
        assert ast.dump(ast.parse(txt).body[0],include_attributes=False)==ast.dump(target[name],include_attributes=False)
        verified.append(name)
    save('review_component_reuse.json',dict(status='PASS accepted independent scalar code copied exactly with declared callback/range changes',source_sha256=sha(Path(J.__file__)),functions=verified))

def physical_normalization():
    np=E.np;P=np.array([[0,1,0,0],[-1,0,1,0],[1,0,1,0],[0,0,0,1]],dtype=object);U=np.kron(P,P);metric=U.T@U
    def exchange(edges):
        H=E.zero(16,16)
        for col in range(16):
            bits=[(col>>(3-i))&1 for i in range(4)]
            for i,j in edges:
                H[col,col]+=F((2*bits[i]-1)*(2*bits[j]-1),4)
                if bits[i]!=bits[j]:H[col^(1<<(3-i))^(1<<(3-j)),col]+=F(1,2)
        return U.T@H@U
    rung=exchange([(0,1),(2,3)]);straight=exchange([(0,2),(1,3)]);number=[int(i//4!=0)+int(i%4!=0) for i in range(16)]
    assert all(metric[i,j]==0 for i in range(16) for j in range(16) if i!=j)
    assert all(rung[i,j]==(F(number[i])-F(3,2))*metric[i,j] for i in range(16) for j in range(16))
    preserve=E.zero(16,16);changes=set()
    for i in range(16):
        for j in range(16):
            if straight[i,j]:changes.add(number[i]-number[j]);assert (number[i]-number[j])%2==0
            if number[i]==number[j]:preserve[i,j]=straight[i,j]
    assert changes=={-2,0,2}
    diagonal=np.diag([F(number[i],2)*metric[i,i] for i in range(16)]).astype(object)
    ranks=[len(E.columns(diagonal+sgn*preserve)) for sgn in [-1,1]];assert ranks==[12,11]
    creation=[F(straight[i,0]**2,metric[i,i]*metric[0,0]) for i in range(16) if number[i]==2 and straight[i,0]];assert creation==[F(1,4)]*3
    save('physical_normalization.json',dict(status='PASS direct four-spin rational reconstruction',rung_coupling=1,ordinary_straight_layers=2,crossed_bonds=0,shifted_rung_spectrum=[0,1],two_rung_shift='3/2',number_changes=sorted(changes),creation_norm_squared='3/4',number_preserving_both_sign_bounds_PSD_ranks=ranks,physical_metric_diagonal=list(map(str,np.diag(metric)))))

def assert_module_boundary():
    seen=[str(Path(J.__file__).relative_to(ROOT)),str(Path(E.__file__).relative_to(ROOT))]
    for name,module in list(sys.modules.items()):
        path=getattr(module,'__file__',None)
        if path:
            p=Path(path).resolve()
            if p.is_relative_to(ROOT):
                assert any(p.is_relative_to(d) for d in [HERE,RES/'interval_joint_review',RES/'interval_extension_review']),('unauthorized mathematical module',name,str(p))
                seen.append(str(p.relative_to(ROOT)))
    save('import_boundary.json',dict(status='PASS no producer mathematical modules',local_modules=sorted(set(seen))))

def basepoint_ledger(records):
    from collections import Counter
    out=[]
    def ladder(base,order):
        loc=list(base);prod=Counter();rows=[]
        for i,axis in enumerate(order):
            old=tuple(loc);loc['xyt'.index(axis)]*=2;new=tuple(loc);power=2**(2-i);prod[new]+=power;prod[old]-=2*power;rows.append(dict(axis=axis,base=list(map(str,old)),target=list(map(str,new))))
        return {k:v for k,v in prod.items() if v},rows
    for r in records:
        rows=[]
        for s in r['joint_ladder_states']:
            base=(s['n'],s['n'],F(s['beta']));p,txy=ladder(base,'txy');qv,xyt=ladder(base,'xyt')
            assert p==qv=={tuple(2*x for x in base):1,base:-8}
            rows.append(dict(level=s['level'],base=list(map(str,base)),same_base_joint_identity=True,txy=txy,xyt=xyt))
        out.append(dict(interval=r['coupling_interval'],states=rows))
    save('basepoint_ledger.json',out)

def main():
    global ODD
    started=time.monotonic();verify_reused_functions();literal_definition_check();physical_normalization();models=models_rebuilt();ODD=odd_polynomials()
    summary=load(SRC/'coverage_summary.json');assert summary['coupling_interval']==['2/25','17/200'] and summary['closed_intervals']==len(summary['intervals'])==16
    reports=[];records=[];cursor=F(2,25)
    for idx,ent in enumerate(summary['intervals']):
        prefix='ground_only' if idx<7 else 'lowband';j=idx+1 if idx<7 else idx-6;assert ent['file']==f'{prefix}/interval_{j:03d}.json'
        r=load(SRC/ent['file']);lo,hi=frs(r['coupling_interval']);assert lo==cursor;cursor=hi
        assert r['coupling_interval']==ent['coupling_interval'] and r['all_integer_L_ge2_gap']==ent['gap_lower'] and r['beta_initial']==ent['beta_initial']
        rep=audit_record(r,models);reports.append(rep);records.append(r)
        print('PASS interval',idx+1,r['coupling_interval'],rep['gap_display'],'windows',rep['finite_window_count'],flush=True)
    assert cursor==F(17,200);assert records[6]['coupling_interval'][1]==records[7]['coupling_interval'][0]=='41/500'
    regimes=[]
    for name,rs,dims,retained in [('ground_only',reports[:7],[11,29,30],[1,1]),('lowband',reports[7:],[59,125,30],[49,97])]:
        raw=load(SRC/f'{name}_summary.json');gap=min(F(r['all_integer_L_ge2_gap']) for r in rs)
        assert raw['closed_intervals']==len(rs) and F(raw['all_integer_L_ge2_uniform_gap'])==gap
        assert raw['coupling_interval']==[rs[0]['coupling_interval'][0],rs[-1]['coupling_interval'][1]]
        assert raw['denominator_retained_states']==retained and raw['total_augmented_trial_dimensions']==dims
        assert raw['ground_trial_dimensions']==[11,29,29] and raw['largest_trace_rank']==1 and raw['largest_physical_spins']==128 and raw['largest_full_dimension']==4**64
        assert raw['largest_residual_required'] is True and raw['maximum_full_residual_geometry']==[8,8] and raw['largest_filtered_trial_max_q']==6 and raw['new_higher_moments'] is False
        regimes.append(dict(coupling_interval=raw['coupling_interval'],closed_intervals=len(rs),uniform_gap=str(gap),denominator_retained_states=retained,total_augmented_trial_dimensions=dims))
    assert summary['regimes']==regimes
    gap=min(F(r['all_integer_L_ge2_gap']) for r in reports);assert gap==F(summary['all_integer_L_ge2_uniform_gap'])==F(1682875193,500000000000)
    prior=load(RES/'interval_joint_review/results/SUMMARY.json');assert prior['accepted'] and prior['unique_finite_volume_ground']
    assert prior['combined_coupling_interval']==['0','2/25'] and prior['combined_closed_intervals']==33
    oldgap=F(prior['combined_all_integer_L_ge2_uniform_gap']);assert oldgap==F(486442811,250000000000)
    assert sum(r['finite_window_count'] for r in reports)==sum(r['joint_ladder_states'] for r in reports)==100 and sum(len(r['short_size_gap_lowers']) for r in reports)==96
    assert sum(r['canonical_updates'] for r in reports)==84 and max(r['asymptotic_onset'] for r in reports)==1024
    u=F(1,500);assert 49/(2*(1-7*u)**2)<32 and 32*u<1 and 5*u<=F(1,100) and 20/(1-20*u)<=32
    basepoint_ledger(records);save('odd_interval_endpoints.json',ODD_REPORTS);assert_module_boundary()
    result=dict(status='PASS independent continuous .085 fixed-center physical and all-integer-size audit',accepted=True,producer_manifest_sha256=FREEZE,extension_interval=['2/25','17/200'],extension_closed_intervals=16,extension_all_integer_L_ge2_uniform_gap=str(gap),extension_gap_display=float(gap),combined_coupling_interval=['0','17/200'],combined_closed_intervals=49,combined_all_integer_L_ge2_uniform_gap=str(min(gap,oldgap)),combined_uniform_gap_display=float(min(gap,oldgap)),unique_finite_volume_ground=True,regimes=regimes,finite_windows=100,required_finite_windows=84,short_size_rows=96,coupled_ladder_states=100,coupled_transitions=84,odd_mode_endpoint_certificates=sum(r['modes'] for r in ODD_REPORTS),largest_patch_physical_spins=128,largest_full_Hilbert_dimension=str(4**64),ground_search_dimensions=[11,29,29],maximum_augmented_dimensions=[59,125,30],largest_numerator_retained_states=1,largest_odd_input_used=False,producer_modules_imported=0,eigensolver_calls=0,new_sparse_support=False,new_moments_above_H2=False,intervals=reports,sources=SOURCES,runtime_seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)),address_space_cap_bytes=1024**3)
    save('SUMMARY.json',result);print('PASS 49-piece union gap',result['combined_uniform_gap_display'],'seconds',result['runtime_seconds'],'RSS KiB',result['peak_rss_kib'],flush=True)
if __name__=='__main__':main()
