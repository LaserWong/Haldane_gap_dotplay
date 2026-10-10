#!/usr/bin/env python3
"""Independent .085/.09 polynomial-input and .085 all-size audit.
No producer code is executed, no physical sparse support is expanded, and no
eigensolver is called. Reused independent functions are extracted unchanged
from separately accepted, hash-pinned reviews before point-specific replay.
"""
import os,sys,resource
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
import json,hashlib,math,itertools,time,ast,types,importlib.util,copy
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import numpy as np
HERE=Path(__file__).resolve().parent;S=HERE/'snapshot';RES=HERE.parent;ROOT=RES.parent
SHAPES=[(4,4),(8,4),(8,8)]
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,o):(HERE/'results'/n).write_text(json.dumps(o,indent=2,default=str)+'\n')
def verify():
    manifest=load(HERE/'INPUT_SHA256.json')
    for p,h in manifest.items():assert sha(S/p)==h,p
    prior=load(HERE/'PRIOR_REVIEW_SHA256.json')
    for name,entry in prior.items():
        p=RES/name/entry.get('manifest_filename','MANIFEST_SHA256.json')
        assert sha(p)==entry['manifest_sha256'],p
        assert load(p)==entry['files']
        for rel,h in entry['files'].items():assert sha(p.parent/rel)==h,(name,rel)
    assert prior['joint_ratio_review']['manifest_sha256']=='18fd9df56ad4023b2f174a3a54d122550670dcf0863176270cd000d48c00fe91'
    assert load(S/'joint_ratio_review/LEMMA_ACCEPTANCE.json')['status']=='PASS independent analytic and exact-arithmetic scalar audit'
    for r in load(HERE/'PRODUCER_FREEZES.json').values():
        assert sha(S/r['folder']/r['name'])==r['manifest_sha256']
        assert sha(RES/r['folder']/r['name'])==r['manifest_sha256']
        for rel,h in r['files'].items():assert sha(RES/r['folder']/rel)==h and sha(S/r['folder']/rel)==h
    for rel,h in load(S/'low_band/frontier_bracket/DEPENDENCIES.json')['code_and_geometry_sha256'].items():assert sha(ROOT/rel)==h,rel
    return prior
PRIOR=verify()
def defs(relative,names,extra=None):
    p=S/relative;name=relative.split('/')[0]
    assert sha(p) in PRIOR[name]['files'].values(),relative
    nodes=[n for n in ast.parse(p.read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names]
    assert {n.name for n in nodes}==set(names)
    ns=dict(F=F,math=math,np=np,itertools=itertools,Counter=Counter,defaultdict=defaultdict)
    if extra:ns.update(extra)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
    return types.SimpleNamespace(**ns)
E=defs('interval_extension_review/audit_interval.py',['graph','arr','zero','matrix_at','columns'])
FM=defs('variational_filter_review/audit_filter.py',['bil','graph','upper_data','pivots','replay_upper','replay_filter','sector_masses'])
P=defs('ground_moment_review/audit_ground.py',['inertia','combine','quadratic'])
Q=defs('bilayer_frontier_review/audit_physical.py',['qa','qn','qs','qm','qd','qsign','qload','symbol'],{'ZERO':(F(0),F(0)),'COS':[(F(1),F(0)),(F(0),F(1,2)),(F(0),F(0)),(F(0),F(-1,2)),(F(-1),F(0)),(F(0),F(-1,2)),(F(0),F(0)),(F(0),F(1,2))]})
p=S/'combined_ground_review/independent_math.py';assert sha(p) in PRIOR['combined_ground_review']['files'].values()
spec=importlib.util.spec_from_file_location('pinned_independent_scalar',p);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

def oldpath(nx,ny,g):
    folder='low_band/translation_band' if g<F(3,50) else 'low_band/frontier_g006' if g==F(3,50) else 'low_band/frontier_g007_g010/g'+str(g).replace('/','d')
    return S/folder/(f'translated_{nx}x{ny}_g{g}_moments.json'.replace('/','d'))
def newpath(nx,ny,g,kind):
    folder=S/('low_band/frontier_bracket/g17d200' if g==F(17,200) else 'low_band/frontier_g009')
    tag=f'{nx}x{ny}_g{g}'.replace('/','d')
    return folder/(f'translated_{tag}_{kind}.json' if kind in ['moments','fourier'] else f'{kind}_{tag}.json')
def fit(xs,ys):
    """Newton divided differences and monomial conversion, unlike Lagrange producer."""
    dd=list(ys);c=[F(0)]*len(xs);basis=[F(1)]
    for k in range(len(xs)):
        for j,v in enumerate(basis):c[j]+=dd[0]*v
        dd=[(dd[j+1]-dd[j])/(xs[j+k+1]-xs[j]) for j in range(len(dd)-1)]
        z=[F(0)]*(len(basis)+1)
        for j,v in enumerate(basis):z[j]-=xs[k]*v;z[j+1]+=v
        basis=z
    return c
def value(c,x):
    out=F(0)
    for a in reversed(c):out=out*x+a
    return out

def polynomials():
    couplings=list(map(F,['3/100','1/25','1/20','3/50','7/100','2/25','1/10']));report=[];coeffs={};checks=0
    accepted={name:set(v['files'].values()) for name,v in PRIOR.items()}
    for rel in ['low_band/translation_band/translated_band.py','symmetry/symmetric_ground.py']:
        assert sha(S/rel) in accepted['large_seed_review'],rel
    for nx,ny in SHAPES:
        records=[load(oldpath(nx,ny,g)) for g in couplings];paths=[oldpath(nx,ny,g) for g in couplings]
        for g,r,p in zip(couplings,records,paths):
            name='large_seed_review' if g<F(3,50) else 'alternative_order_review' if g==F(3,50) else 'bilayer_frontier_review'
            assert sha(p) in accepted[name]
            assert (r['nx'],r['ny'],F(r['g']),r['matrix_denominator'])==(nx,ny,g,4*g.denominator)
            assert r['column_rule']==records[0]['column_rule']
        cc={};local_checks=0
        for key,power,degree in [('G',2,2),('A',3,3),('B',4,4)]:
            cc[key]=[]
            for i in range(nx):
                row=[]
                for j in range(ny):
                    ys=[F(int(r[key][i][j]),4*r['matrix_denominator']**power) for r in records]
                    # Fit LAST points in reverse order, disjoint from producer's choice where possible.
                    ix=list(reversed(range(7-degree-1,7)));cs=fit([couplings[k] for k in ix],[ys[k] for k in ix])
                    allcs=fit(couplings,ys);assert all(x==0 for x in allcs[degree+1:]) and allcs[:degree+1]==cs
                    for x,y in zip(couplings,ys):assert value(cs,x)==y
                    local_checks+=7-(degree+1);row.append(list(map(str,cs)))
                    for g in [F(17,200),F(9,100)]:
                        r=load(newpath(nx,ny,g,'moments'));d=4*g.denominator
                        z=value(cs,g)*4*d**power;assert z.denominator==1 and z==int(r[key][i][j])
                        assert r['matrix_denominator']==d and r['polynomial_degrees']=={'G':2,'A':3,'B':4}
                        assert (r['nx'],r['ny'],r['N'],F(r['g']))==(nx,ny,nx*ny,g) and r['extra_point_exact_checks']==9*nx*ny
                        assert len(r[key])==nx and all(len(row)==ny for row in r[key])
                        for rel,h in r['source_sha256'].items():assert sha(S/rel)==h
                cc[key].append(row)
        assert local_checks==9*nx*ny;checks+=local_checks;coeffs[f'{nx}x{ny}']=cc
        report.append(dict(shape=[nx,ny],exact_extra_checks=local_checks,old_source_hashes=[sha(p) for p in paths],full_seven_point_degree_check=True,independent_reverse_newton_fit=True,both_new_points_match=True))
    assert checks==1008
    save('polynomial_coefficients.json',coeffs);save('polynomial_review.json',dict(status='PASS',literal_affine_definition_verified_in_PROOF=True,extra_point_checks=checks,shapes=report))
    print('POLYNOMIAL PASS: 1008 extra-point equalities; .085 and .09 matrices exact',flush=True)

def local_matrix(g,a,b):
    # Direct physical four-spin construction in a fixed rational orthogonal rung basis.
    T=np.array([[0,1,0,0],[-1,0,1,0],[1,0,1,0],[0,0,0,1]],dtype=object);U=np.kron(T,T);v=np.zeros((16,16),dtype=object)
    for col in range(16):
        bits=[(col>>(3-j))&1 for j in range(4)]
        for i,j in [(0,2),(1,3)]:
            v[col,col]+=F((2*bits[i]-1)*(2*bits[j]-1),4)
            if bits[i]!=bits[j]:v[col^(1<<(3-i))^(1<<(3-j)),col]+=F(1,2)
    K=U.T@v@U;metric=U.T@U
    for i in range(16):
        for j in range(16):
            if K[i,j]:assert (int(i//4!=0)+int(i%4!=0)-int(j//4!=0)-int(j%4!=0))%2==0
    return [[g*K[i,j]+(a*(int(i//4!=0)+int(i%4!=0))+b)*metric[i,j] for j in range(16)] for i in range(16)]

def bins(rec):
    nx,ny=rec['nx'],rec['ny'];N=nx*ny;g=F(rec['g']);ed,_=E.graph(nx,ny)
    assert rec['N']==N and F(rec['energy_shift'])==-F(3*N,4)
    assert rec['weighted_edges']==[[i,j,w] for (i,j),w in sorted(ed.items())]
    assert [sum(w for e,w in ed.items() if i in e) for i in range(N)]==[4]*N
    v=F(3,4)*g*g*sum(w*w for w in ed.values());alpha=1-2*g;dl,du=map(F,[rec['delta_lower'],rec['delta_upper']]);assert 0<dl<du and dl*dl<=1-4*g<du*du
    assert rec['bosonic_modes']==3*N and rec['physical_hilbert_dimension']==4**N and F(rec['alpha'])==alpha
    assert F(rec['vacuum_creation_norm_squared'])==v and F(rec['creation_matrix_norm_squared_upper'])==4*g*g and F(rec['delta_squared'])==1-4*g
    e=-v/(alpha+dl);assert F(rec['bosonic_ground_lower'])==e
    first=1;assert len(rec['bins'])==N+1
    for q,r in enumerate(rec['bins']):
        mult=math.comb(3*N+q-1,q);assert r['q']==q and r['multiplicity']==mult and r['first_ordered_index']==first and F(r['lower'])==e+q*dl;first+=mult
    assert first-1==math.comb(4*N,N)>=4**N and rec['bins'][2]['first_ordered_index']==2+3*N
    return e,e+dl,e+2*dl,first-1

def audit_patch(nx,ny,g):
    N=nx*ny;den=4*g.denominator;gr=load(newpath(nx,ny,g,'block1'));geom=load(S/f'large_seed_moments/geometry_{nx}x{ny}.json')
    assert (gr['nx'],gr['ny'],gr['N_dimers'],gr['physical_sites'],F(gr['coupling']),F(gr['E00']))==(nx,ny,N,2*N,g,-F(3*N,4))
    independent=load(S/f'large_seed_review/results/geometry_{nx}x{ny}.json')
    assert sha(S/f'large_seed_review/results/geometry_{nx}x{ny}.json') in PRIOR['large_seed_review']['files'].values()
    assert all(geom[k]==independent[k] for k in ['F','S','V','W'])
    G,A,B=E.matrix_at(nx,ny,g,geom,True);ids=E.columns(G);assert ids==gr['selected_basis_indices'];ix=np.ix_(ids,ids);GG,AA,BB=[x[ix] for x in (G,A,B)]
    assert np.array_equal(GG,np.array(gr['gram'],dtype=object))
    assert np.array_equal(AA*den,np.array(gr['shifted_hamiltonian_numerator'],dtype=object)) and np.array_equal(BB*den**2,np.array(gr['shifted_H2_numerator'],dtype=object))
    c=list(map(F,gr['coefficients']));norm=FM.bil(c,GG);rho=FM.bil(c,AA)/norm;var=FM.bil(c,BB)/norm-rho*rho;assert norm>0 and var>0
    assert rho==F(gr['exact_rayleigh'])+F(3*N,4) and var==F(gr['exact_residual_squared'])
    assert gr['full_dimension']==4**N and gr['trial_subspace_dimension']==len(ids)==(11 if N==16 else 29) and gr['integer_matrix_denominator']==den and F(gr['gram_common_factor_removed'])==2**N
    loc=gr['relative_form_bound'];l=loc['local_certificate'];aa,bb=F(l['a']),F(l['b']);assert F(l['coupling'])==g
    assert P.inertia(local_matrix(g,aa,bb))==[0,0,16];assert F(loc['alpha'])==1-4*aa>0 and F(loc['B'])==2*N*bb and F(loc['second_shift_lower'])==1-4*aa-2*N*bb
    # Independently rebuild every Fourier symbol and full leaked residual.
    moments=load(newpath(nx,ny,g,'moments'));four=load(newpath(nx,ny,g,'fourier'));assert four['source_moments']==moments
    assert len(four['modes'])==N and {tuple(m['momentum']) for m in four['modes']}==set(itertools.product(range(nx),range(ny)))
    for m in four['modes']:
        kx,ky=m['momentum'];gg,aa,bb=[Q.symbol(moments[k],nx,ny,kx,ky) for k in ['G','A','B']];assert Q.qsign(gg)>0
        theta=Q.qd(aa,Q.qm((F(den),F(0)),gg));variance=Q.qs(Q.qd(bb,Q.qm((F(den*den),F(0)),gg)),Q.qm(theta,theta));assert Q.qsign(variance)>=0
        for k,z in zip(['G','A','B','theta','residual_squared'],[gg,aa,bb,theta,variance]):assert Q.qload(m[k])==z
        assert Q.qsign(Q.qs(theta,(F(m['theta_lower']),F(0))))>=0 and Q.qsign(Q.qs((F(m['theta_upper']),F(0)),theta))>=0 and Q.qsign(Q.qs((F(m['residual_squared_upper']),F(0)),variance))>=0
    assert F(four['ritz_max_upper'])==max(F(m['theta_upper']) for m in four['modes']) and four['triplet_multiplicity']==3 and four['retained_triplet_band_dimension']==3*N
    b=load(newpath(nx,ny,g,'quadratic_bins'));a0,a1,a2,count=bins(b);old=load(newpath(nx,ny,g,'temple'));rec=load(newpath(nx,ny,g,'combined_patch'))
    assert old['number_sector_bins']==rec['number_sector_bins']==b
    for p in [old,rec]:
        assert (p['nx'],p['ny'],p['N'],F(p['g']),F(p['energy_shift']))==(nx,ny,N,g,-F(3*N,4))
        assert p['full_hilbert_dimension']==4**N and p['retained_full_band_dimension']==1+3*N and p['relative_form_bound']==loc
        assert [F(p[k]) for k in ['global_ground_lower','all_excited_global_lower','global_lambda_kplus1_lower']]==[a0,a1,a2]
        for rel,h in p['source_sha256'].items():assert sha(S/rel)==h
    assert rho<a1<a2 and F(four['ritz_max_upper'])<a2
    ground,trip=old['blocks'];assert ground['k']==ground['multiplicity']==1 and trip['k']==N and trip['multiplicity']==3
    assert F(ground['eigen_lower'][0])==rho-var/(a2-rho) and F(ground['eigen_upper'][0])==rho
    assert len(trip['eigen_lower'])==len(trip['eigen_upper'])==len(trip['exact_Qsqrt2_Temple_endpoints'])==N
    for m,l,u,z,newl in zip(four['modes'],trip['eigen_lower'],trip['eigen_upper'],trip['exact_Qsqrt2_Temple_endpoints'],rec['blocks'][1]['eigen_lower']):
        theta,variance=Q.qload(m['theta']),Q.qload(m['residual_squared']);distance=Q.qs((a2,F(0)),theta);assert Q.qsign(distance)>0
        endpoint=Q.qs(theta,Q.qd(variance,distance));assert endpoint==Q.qload(z) and Q.qsign(Q.qs(endpoint,(F(l),F(0))))>=0
        assert Q.qsign(Q.qs((F(l)+F(1,10**14),F(0)),endpoint))>0 and (F(l)*10**14).denominator==1
        assert u==m['theta_upper'] and F(newl)==max(a1,F(l))<=F(u)<a2
    # Unique even eigenvalue below a2 follows from full-space count and 3N odd states.
    pp=load(newpath(nx,ny,g,'ground_pencil'));pc=pp['pencil'];ep=pc['endpoints'][0];low=F(ep['lower']);high=F(ep['optimal_pencil_endpoint_upper']);m=len(ids)
    assert F(pc['external_cutoff'])==a2 and pc['external_low_count_required']==pc['negative_inverse_ritz_count']==1 and pc['trial_dimension']==m and len(pc['endpoints'])==1
    matrices=[GG,AA-a2*GG,BB-2*a2*AA+a2*a2*GG,BB-(a2+low)*AA+a2*low*GG,BB-(a2+high)*AA+a2*high*GG]
    inertias=[P.inertia(x.tolist()) for x in matrices];assert inertias==[[0,0,m],[1,0,m-1],[0,0,m],[1,0,m-1],[0,0,m]]
    assert inertias==[pc['gram_inertia'],pc['cutoff_ritz_inertia'],pc['shifted_squared_moment_inertia'],ep['endpoint_pencil_inertia'],ep['upper_pencil_inertia']]
    w=ep['negative_direction_witness'];assert len(w['coefficients'])==m and all(type(x) is int for x in w['coefficients']);v=list(map(F,w['coefficients']));q=FM.bil(v,matrices[3]);assert q==F(w['exact_endpoint_quadratic_form'])<0
    assert low<high<a2 and high-low==F(ep['pencil_root_bracket_width']) and ep['sector_eigenvalue_index_one_based']==1
    targetlow=max(a0,F(ground['eigen_lower'][0]),low);assert F(pp['ground_lower'])==targetlow==F(rec['blocks'][0]['eigen_lower'][0])
    # Full q<=6 residual-sector filter; no new filtered residual is claimed.
    f=load(newpath(nx,ny,g,'filtered'));assert sha(S/f['source'].removeprefix('research_20261010/'))==f['source_sha256'] and sha(S/f['geometry_source'].removeprefix('research_20261010/'))==f['geometry_source_sha256']
    assert (f['nx'],f['ny'],F(f['coupling']),F(f['energy_shift']))==(nx,ny,g,-F(3*N,4))
    assert F(f['exact_original_shifted_rayleigh'])==rho and F(f['exact_original_variance'])==var and F(f['original_squared_norm_reduced'])==norm and F(f['original_gram_common_factor_removed'])==2**N
    R,diagonal,off=FM.replay_upper(f['compressed_upper_certificate'],nx,ny,g);globalgain=FM.replay_filter(f['global_upper_filter'],rho,var,R)
    masses=FM.sector_masses(gr,geom,G,A*den,norm,rho);assert min(masses)>=0 and sum(masses)==var
    sec=f['residual_sector_certificate'];assert list(map(F,sec['residual_norm_squared_by_number']))==masses and F(sec['variance_sum_exact'])==var and sec['number_indices']==[0,2,4,6]
    products=[off[i]*masses[i]*masses[i+1] for i in range(3)];assert list(map(F,sec['cross_term_squared']))==products
    roots=list(map(F,sec['cross_term_sqrt_upper']));unit=F(1,10**36)
    for z,r in zip(products,roots):assert r>=0 and r*r>=z and (r==0 or (r-unit)**2<z) and (r/unit).denominator==1
    numerator=sum(x*y for x,y in zip(diagonal,masses))+2*sum(roots);sectorR=numerator/var
    assert numerator==F(sec['residual_H_expectation_numerator_upper']) and sectorR==F(sec['residual_normalized_H_expectation_upper'])
    gain=FM.replay_filter(f['filter'],rho,var,min(R,sectorR));upper=rho-gain
    assert gain>=globalgain and upper==F(f['shifted_rayleigh_upper'])==F(rec['blocks'][0]['eigen_upper'][0]) and targetlow<=upper<rho
    assert f['new_residual_claim'] is False and f['reads_higher_moments'] is False and f['implicit_filtered_trial_states']==1 and f['local_filter_plane_dimension_upper']==2 and f['original_space_plus_residual_dimension_upper']==m+1 and f['filtered_trial_max_triplet_number']==6
    assert f['physical_spins']==2*N and f['full_dimension']==4**N and f['original_trial_dimension']==m and f['residual_parity']=='even'
    expected=copy.deepcopy(old);expected['status']=rec['status'];expected['extra_source_sha256']=rec['extra_source_sha256'];expected['new_trial_residual_claim']=False;expected['ground_width']=str(upper-targetlow)
    expected['blocks'][0]['unfiltered_eigen_upper']=old['blocks'][0]['eigen_upper'][:];expected['blocks'][0]['eigen_lower']=[str(targetlow)];expected['blocks'][0]['eigen_upper']=[str(upper)]
    expected['blocks'][1]['eigen_lower']=[str(max(a1,F(x))) for x in trip['eigen_lower']]
    assert rec==expected
    for rel,h in rec['extra_source_sha256'].items():assert sha(S/rel)==h
    print('PHYSICAL PASS',g,nx,ny,'full residual',float(var),'ground width',float(upper-targetlow),flush=True)
    return dict(g=str(g),shape=[nx,ny],physical_spins=2*N,full_dimension=str(4**N),trial_dimension=m,retained_band_dimension=1+3*N,full_residual_squared=str(var),ground_lower=str(targetlow),ground_upper=str(upper),ground_identification_margin=str(a1-rho),triplet_cutoff_margin=str(a2-F(four['ritz_max_upper'])),q6_residual_mass=str(masses[-1]),pencil_inertias=inertias,reference_count=str(count),full_physical_inputs_accepted=True)

def down(x,digits=80):x=F(x);d=10**digits;return F(x.numerator*d//x.denominator,d)
def sqrtlo(x,digits=40):
    x=F(x);assert x>=0;d=10**digits;n=math.isqrt(x.numerator*d*d//x.denominator);z=F(n,d);assert z*z<=x<(z+F(1,d))**2;return z
def full(v):return v[0]**4*v[1]**2*v[2]
def valid(v):assert len(v)==3 and all(0<x<=1 for x in v)
def move(v,order='txy',digits=40):
    valid(v);a,b,c=v
    return [a,b,c] if order=='xyt' else [a,b*sqrtlo(c,digits),b*b*c] if order=='xty' else [a*sqrtlo(b,digits),a*a*b*sqrtlo(c,digits),full(v)]
def advance(v,digits=80):
    if v is None:return None
    valid(v);v=list(v)
    for j in range(3):
        x=down(M.G(full(v)),digits)
        if x<=0:return None
        v=v[1:]+[x]
    return v
def canonical_next(v,K):
    valid(v);a,b,c=v;args=[];ans=[]
    z=max(full(v),K);args.append(z);d=down(M.G(z));ans.append(d)
    if d<=0:return None,args
    z=max(b**4*c*c,K*K)*d;args.append(z);e=down(M.G(z));ans.append(e)
    if e<=0:return None,args
    z=max(c,K)**4*d*d*e;args.append(z);f=down(M.G(z));ans.append(f)
    return (ans if f>0 else None),args

def one_window(s,t,K=F(0)):
    assert 0<s<=1 and 0<t<=1 and 0<=K<=1
    p=max(s*s*t,K);assert p>F(1,2)
    w=(1+sqrtlo(2*p-1))/2;r=(1-w)/w;d=t/(1+r*r)
    result=down((1-r)*min(s*sqrtlo(d),d),40)
    return result,dict(joint_lower=str(K),p=str(p),dominant_weight_lower=str(w),tail_ratio_upper=str(r),d_lower=str(d))
def window(v,K):
    valid(v);a,b,c=v;assert b>F(1,2) and 0<K<=1
    root=sqrtlo(2*b-1);sx=max(a*a*root,sqrtlo(K)*root/b);ty,inner=one_window(b,c,K);thermal,outer=one_window(sx,ty)
    return thermal,dict(joint_lower=str(K),spatial_lower=str(sx),transverse_thermal_lower=str(ty),inner=inner,outer=outer)

def shorts():
    s=load(S/'low_band/frontier_g007_g010/short_sizes/uniform_short_sizes.json');sums=[];rows=[]
    assert s['sides']==list(range(2,8)) and F(s['g_max'])==F(1,10)
    for L in range(2,8):
        ed,_=E.graph(L,L);assert [sum(w for e,w in ed.items() if i in e) for i in range(L*L)]==[4]*(L*L)
        ss=sum(w*w for w in ed.values());sums.append(ss);rows.append(dict(L=L,edge_square_sum=ss,physical_dimension=str(4**(L*L))))
    assert sums==s['weighted_edge_square_sums']==[16,18,32,50,72,98] and s['max_weighted_edge_square_sum']==98
    alpha,delta,v=map(F,[s['alpha_lower'],s['delta_lower'],s['vacuum_creation_norm_squared_upper']])
    assert alpha==F(4,5) and 0<delta*delta<=F(3,5) and v==F(147,200)
    gap=delta-v/(alpha+delta);assert gap==F(s['gap_lower'])>0
    save('short_size_review.json',dict(status='PASS',uniform_g_interval=['0','1/10'],gap=str(gap),gap_display=float(gap),cases=rows,ground_product_upper=0,physical_gap_monotonicity_assumed=False))
    return gap

def initial(recs,beta,order,saved):
    independently=M.ratios(recs,beta,order)
    supplied=[F(saved[k]) for k in ['J1','J2','C0']]
    assert all(0<x<=y<=1 for x,y in zip(supplied,independently)),list(zip(supplied,independently))
    v=M.first_steps(supplied)
    return v,dict(independent_direct_trace_ratios=list(map(str,independently)),saved_ratios=list(map(str,supplied)),conservative=True)

def formal_ledger(beta):
    def add(*terms):
        out=Counter()
        for term in terms:
            for k,v in term.items():out[k]+=v
        return {k:v for k,v in out.items() if v}
    def power(p,k):return {x:k*v for x,v in p.items()}
    def ladder(base,order):
        p=list(base);terms=[];edges=[]
        for axis in order:
            old=tuple(p);p['xyt'.index(axis)]*=2;new=tuple(p);terms.append({new:1,old:-2});edges.append(dict(axis=axis,base=list(map(str,old)),target=list(map(str,new))))
        product=add(power(terms[0],4),power(terms[1],2),terms[2]);assert product=={tuple(p):1,tuple(base):-8}
        return product,edges
    rows=[]
    for cycle in range(9):
        base=(8*2**cycle,8*2**cycle,2*beta*2**cycle)
        a,edges=ladder(base,'txy');b,canonical=ladder(base,'xyt');assert a==b
        p=list(base);order=list('txy');micro=[]
        for j in range(3):
            old=tuple(p);axis=order.pop(0);p['xyt'.index(axis)]*=2;order.append(axis);micro.append(dict(direction=axis,old_base=list(map(str,old)),new_base=list(map(str,p)),new_order=''.join(order)))
        assert tuple(p)==tuple(2*x for x in base) and ''.join(order)=='txy'
        rows.append(dict(cycle=cycle,base=list(map(str,base)),permuted_edges=edges,canonical_edges=canonical,full_product_order_identity=True,rotating_microsteps=micro))
    save('basepoint_ledger.json',rows)

def selected_deferred(short):
    path=S/'low_band/frontier_bracket/g17d200/extra_cycles_exact.json';r=load(path);beta=F(r['beta_initial']);assert beta==F(177,20) and r['order']=='txy' and F(r['g'])==F(17,200)
    for rel,h in r['source_sha256'].items():assert sha(S/rel)==h
    recs=[load(newpath(nx,ny,F(17,200),'combined_patch')) for nx,ny in SHAPES]
    raw,initial_report=initial(recs,beta,'txy',r['initial']);valid(raw);states=r['states'];assert len(states)==9
    windows=[]
    for cycle,s in enumerate(states):
        n=8*2**cycle;tau=2*beta*2**cycle;digits=max(80,40*2**max(0,cycle-5))
        assert s['cycle']==cycle and s['n']==n and F(s['beta'])==tau and s['rounding_digits']==digits
        assert raw==list(map(F,s['permuted_purities']));canonical=[down(x,digits) for x in move(raw,digits=digits)];valid(canonical)
        assert canonical==list(map(F,s['canonical_purities']));joint=full(raw);assert joint==F(s['joint_lower']) and joint>=full(canonical)
        u=max(1-x for x in canonical);assert u==F(s['u'])>0
        thermal,detail=window(canonical,joint);assert F(s['window']['thermal_lower'])==thermal and s['window']['details']==detail and F(1,2)<thermal<1
        gap=F(s['window']['gap_lower']);assert gap>0 and M.exponential(tau*gap)[1]*(1-thermal)<thermal
        windows.append(dict(cycle=cycle,n=n,through=2*n,beta=str(tau),u=str(u),joint=str(joint),thermal_lower=str(thermal),gap_lower=str(gap),gap_display=float(gap),both_inverse_purity_margins_positive=True))
        if cycle<8:raw=advance(raw,max(160,digits*2));assert raw is not None
    assert F(r['short_size_lower'])==short
    accepted=[];assert len(r['candidates'])==5
    for cycle,c in zip(range(4,9),r['candidates']):
        w=windows[cycle];n=w['n'];tau=F(w['beta']);u=F(w['u']);gap=F(c['asymptotic_gap'])
        assert c['cycles_before_transport']==cycle and c['asymptotic_n']==n and F(c['beta'])==tau and F(c['u'])==u and 0<u<=F(1,500)
        witness=M.exponential(tau*gap)[1]*32*u;assert gap>0 and witness<1
        # Old asymptotic theorem's constants hold on the entire declared domain.
        ub=F(1,500);assert 49/(2*(1-7*ub)**2)<32 and 32*ub<1 and 20/(1-20*ub)<32 and 5*ub<=F(1,100)
        cursor=8
        for prev in windows[:cycle]:assert prev['n']==cursor;cursor=prev['through']
        assert cursor==n
        overall=min([gap,short]+[F(x['gap_lower']) for x in windows[:cycle]])
        assert overall==F(c['all_integer_L_ge2_gap']) and c['gap_display']==float(overall) and c['accepted'] is True
        accepted.append(dict(additional_txy_cycles=cycle,total_txy_cycles_including_seed=cycle+1,asymptotic_n=n,beta=str(tau),asymptotic_gap=str(gap),all_integer_L_ge2_gap=str(overall),gap_display=float(overall),required_windows=cycle,positive_exponential_witness=str(witness),coverage='L2..7 short; adjacent boxes from L8; all L>=onset by small-defect theorem'))
    assert accepted[-1]['all_integer_L_ge2_gap']=='27887084487/1000000000000'
    save('deferred_review.json',dict(status='PASS independent exact all-integer review',initial=initial_report,windows=windows,candidates=accepted,selected=accepted[-1],last_window_required=False))
    formal_ledger(beta)
    print('ALL-SIZE PASS .085',accepted[-1]['gap_display'],'onset',accepted[-1]['asymptotic_n'],'eight earlier windows',flush=True)
    return accepted[-1]

def g09_selected_failures():
    r=load(S/'low_band/frontier_g009/joint_scan_g9d100.json');recs=[load(newpath(nx,ny,F(9,100),'combined_patch')) for nx,ny in SHAPES];out=[]
    for rel,h in r['source_sha256'].items():assert sha(S/rel)==h
    assert [x['order'] for x in r['results']]==['txy','xty','xyt']
    for result in r['results']:
        order=result['order'];assert result['joint_successful_float_proposals']==result['deferred_successful_float_proposals']==0
        for c in result['exact_selected']:
            assert not c['accepted'];beta=F(c['beta_initial']);st=c['initial'];raw,trace=initial(recs,beta,order,st)
            assert raw==list(map(F,st['permuted_prefix']))
            if len(raw)<3 or min(raw)<=0:
                assert c['states']==[] and c['sequence_status']=='initial_prefix_nonpositive';out.append(dict(order=order,beta=str(beta),exact_failure='initial nonpositive',trace=trace));continue
            canonical=move(raw,order);assert canonical==list(map(F,st['canonical']));joint=full(raw)
            for i,s in enumerate(c['states']):
                if raw is not None:
                    converted=move(raw,order);canonical=converted if canonical is None else [max(x,y) for x,y in zip(canonical,converted)];joint=max(joint,full(raw))
                assert canonical is not None;joint=max(joint,full(canonical))
                assert s['cycle']==i and s['n']==8*2**i and F(s['beta'])==2*beta*2**i and canonical==list(map(F,s['canonical'])) and joint==F(s['joint']) and max(1-x for x in canonical)==F(s['u'])
                assert (raw is None and s['raw'] is None) or raw==list(map(F,s['raw']))
                assert max(1-x for x in canonical)>F(1,500)
                nxt,args=canonical_next(canonical,joint);assert args==list(map(F,s['canonical_update_arguments']));raw=advance(raw);canonical=nxt;joint=full(nxt) if nxt is not None else F(0)
            assert raw is None and canonical is None and c['sequence_status']=='all_comparison_paths_left_domain'
            out.append(dict(order=order,beta=str(beta),exact_failure='both recorded comparison paths left positivity',states=len(c['states']),trace=trace))
    save('g09_diagnostic_review.json',dict(status='PASS selected exact failures only',records=out,producer_bounded_grid='beta5..25 step.05; 10 coupled cycles or six deferred cycles',all_beta_exclusion=False,physical_gaplessness=False,new_g09_gap_certificate=False,independent_float_grid_replay=False))
    print('G09 DIAGNOSTIC PASS: three selected exact failures; no all-beta exclusion',flush=True)

def main():
    start=time.monotonic();polynomials();physical=[]
    for g in [F(17,200),F(9,100)]:
        for nx,ny in SHAPES:physical.append(audit_patch(nx,ny,g));save('physical_review.json',physical)
    short=shorts();selected=selected_deferred(short);g09_selected_failures();verify()
    summary=dict(status='PASS independent polynomial physical inputs and .085 all-integer gap certificate',accepted_g='17/200',all_integer_L_ge2_gap=selected['all_integer_L_ge2_gap'],gap_display=selected['gap_display'],finite_volume_unique_ground=True,continuous_coupling_claim=False,physical_inputs_accepted_g=['17/200','9/100'],physical_geometries=len(physical),extra_polynomial_checkpoints=1008,required_finite_windows=8,short_sizes=list(range(2,8)),asymptotic_onset=2048,physical_spins_max=128,full_Hilbert_dimension_max=str(4**64),ground_search_dimensions=[11,29,29],retained_full_band_dimensions=[49,97,193],g09_new_gap=False,all_beta_exclusion=False,producer_modules_executed=0,physical_support_expansions=0,eigensolver_calls=0,resource=dict(cpus=list(os.sched_getaffinity(0)),address_space_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),seconds=time.monotonic()-start)
    save('SUMMARY.json',summary);print(summary['status'],'seconds',summary['seconds'],flush=True)
if __name__=='__main__':main()
