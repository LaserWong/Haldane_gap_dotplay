#!/usr/bin/env python3
"""Independent interval application audit; imports no producer code.
Physical assembly / exact scalar arithmetic reused from a pinned accepted review.
The new joint updates, route merge, windows and coverage are implemented here.
"""
import os,resource,sys,json,hashlib,time,importlib.util,math,argparse
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
sys.dont_write_bytecode=True
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parent;ROOT=RES.parent
PRIOR=RES/'interval_extension_review';SRC=HERE/'snapshot'
PRIOR_SEAL='1af6c2142aa6a3649fd50275a8582add9cfe0a72ff8f21556195185c495eb956'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,x):(HERE/'results'/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def verify_manifest(path,expected=None):
    if expected:assert sha(path)==expected,('manifest hash',str(path))
    m=load(path);files=m.get('files',m)
    for rel,h in files.items():assert sha(path.parent/rel)==h,('sealed file',str(path.parent/rel))
    return len(files)
# Check the complete accepted source seal BEFORE importing any helper.
verify_manifest(PRIOR/'MANIFEST_SHA256.json',PRIOR_SEAL)
spec=importlib.util.spec_from_file_location('sealed_interval_physics',PRIOR/'audit_interval.py')
E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
frs=E.frs;floor=E.floor;ceil=E.ceil;sqrtlo=E.sqrtlo;expi=E.expi;poly=E.poly;eqseq=E.eqseq
Q18=10**18

def models_rebuilt():
    """Fresh exact assembly, with F/S/V/W inherited by explicitly verified seal."""
    models=[];report=[]
    for shape in [(4,4),(8,4),(8,8)]:
        nx,ny=shape;label=f'{nx}x{ny}'
        geom=load(PRIOR/'inputs'/f'geometry_{label}.json')
        G,K0,J0=E.matrix_at(nx,ny,F(0),geom,True)
        _,K1,J1=E.matrix_at(nx,ny,F(1),geom,True)
        _,_,Jm=E.matrix_at(nx,ny,F(-1),geom,True)
        ids=E.columns(G);ix=E.np.ix_(ids,ids);cut=lambda a:a[ix]
        G=cut(G);K=[cut(K0),cut(K1-K0)];J=[cut(J0),cut((J1-Jm)/2),cut((J1+Jm)/2-J0)]
        r=load(PRIOR/'inputs/auxiliary'/f'matrix_polynomial_{label}.json')
        assert ids==r['selected_basis_indices'] and len(ids)==r['trial_dimension']==(11 if nx*ny==16 else 29)
        assert E.np.array_equal(G,E.arr(r['gram']))
        for key,cs in [('shifted_A_coefficients',K),('full_shifted_B_coefficients',J)]:
            assert len(r[key])==len(cs)
            for a,b in zip(cs,r[key]):assert E.np.array_equal(a,E.arr(b))
        models.append((G,K,J));report.append(dict(geometry=list(shape),trial_dimension=len(G),exact_full_polynomial_assembly=True,geometry_sha256=sha(PRIOR/'inputs'/f'geometry_{label}.json'),polynomial_sha256=sha(PRIOR/'inputs/auxiliary'/f'matrix_polynomial_{label}.json')))
    save('physical_polynomials.json',report);return models

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
    lo,hi=frs(r['coupling_interval']);assert F(39,500)<=lo<hi<=F(2,25)
    assert F(r['fixed_vector_center'])==(lo+hi)/2
    trials=r['denominator_patches']+[r['largest_base_trial']];assert len(trials)==3
    rr=[];pp=[]
    for idx,(t,m,shape) in enumerate(zip(trials,models,[(4,4),(8,4),(8,8)])):
        assert t['geometry']==list(shape) and t['N']==math.prod(shape) and t['trial_dimension']==len(m[0])
        rho,p=E.check_trial(t,m,lo,hi,idx<2);rr.append(rho);pp.append(p)
    rr[2],filter_report=E.check_filter(r['largest_interval_filter'],rr[2],pp[2],lo,hi)
    energies={}
    for name,weights in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
        s=r['correlated_energy_combinations'][name];assert s['weights']==weights
        assert sum(F(-3*math.prod(shape),4)*w for shape,w in zip([(4,4),(8,4),(8,8)],weights))==0
        coeff=[sum(weights[i]*rr[i][j] for i in range(3)) for j in range(2)];ends=[poly(coeff,x) for x in (lo,hi)]
        eqseq(coeff,s['affine_coefficients']);eqseq(ends,s['endpoint_values']);energies[name]=min(ends);assert F(s['uniform_lower'])==energies[name]
    beta=F(r['beta_initial']);assert beta>0 and len(r['trace_upper_certificates'])==3
    us=[E.upper(N,p,b,s) for N,p,b,s in zip([16,16,32],[pp[0],pp[0],pp[1]],[beta,2*beta,2*beta],r['trace_upper_certificates'])]
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

def verify_sources(final=False):
    out={'prior_review_manifest':PRIOR_SEAL,'prior_review_files':verify_manifest(PRIOR/'MANIFEST_SHA256.json',PRIOR_SEAL)}
    # Verify all dependencies named by the prior independent physical review.
    rows={}
    for name,rec in load(PRIOR/'INHERITED_REVIEWS.json').items():rows[name]=dict(manifest_sha256=rec['manifest_sha256'],files=verify_manifest(RES/name/'MANIFEST_SHA256.json',rec['manifest_sha256']))
    out['prior_inherited_reviews']=rows
    for rel,h in load(PRIOR/'INPUT_SHA256.json').items():assert sha(PRIOR/rel)==h
    if final:
        gate=load(HERE/'ACCEPTANCE_GATES.json')
        assert gate['prior_review_manifest']==PRIOR_SEAL
        freeze=load(HERE/'PRODUCER_FREEZE.json');assert sha(HERE/'PRODUCER_FREEZE.json')==gate['producer_manifest_sha256']
        for rel,h in freeze.get('files',freeze).items():assert sha(SRC/rel)==h
        assert sha(RES/'interval_joint_extension'/'FROZEN_MANIFEST.json')==gate['producer_manifest_sha256']
        out['producer_files']=len(freeze.get('files',freeze));out['producer_manifest_sha256']=gate['producer_manifest_sha256']
        assert verify_manifest(RES/'interval_joint_extension'/'FROZEN_MANIFEST.json',gate['producer_manifest_sha256'])==out['producer_files']
        for rel,h in load(SRC/'INPUT_SHA256.json').items():assert sha(ROOT/rel)==h,('producer external dependency',rel)
        # Upstream new lemma is a required independent analytic acceptance, not inferred from replay.
        lemma=RES/'joint_ratio_review';seal=gate['joint_review_manifest_sha256']
        out['joint_lemma_review_files']=verify_manifest(lemma/gate['joint_review_manifest_file'],seal)
        accept=load(lemma/gate['joint_review_acceptance_file'])
        assert accept==gate['joint_review_acceptance_record']
        assert accept['status']=='PASS independent analytic and exact-arithmetic scalar audit'
        assert accept['producer_manifest_sha256']=='905a55c3419a08082c05f8fe011116e2655035c23cb9040e4e92ad856ce4e9bc'
        out['joint_review_manifest_sha256']=seal
        for rel,h in load(HERE/'INPUT_SHA256.json').items():assert sha(ROOT/rel)==h,rel
    return out

def main():
    global SRC
    ap=argparse.ArgumentParser();ap.add_argument('--preliminary',action='store_true');a=ap.parse_args();start=time.monotonic()
    if a.preliminary:SRC=RES/'interval_joint_extension'
    sources=verify_sources(final=not a.preliminary);models=models_rebuilt();summary=load(SRC/'coverage_summary.json')
    assert summary['coupling_interval']==['39/500','2/25'] and summary['closed_intervals']==len(summary['intervals'])==2
    assert summary['largest_trace_rank']==1 and summary['denominator_retained_states']==[1,1]
    assert summary['trial_dimensions']==[11,29,29] and summary['largest_physical_spins']==128 and summary['largest_full_dimension']==4**64
    assert summary['largest_residual_required'] and summary['maximum_full_residual_geometry']==[8,8]
    assert summary['filtered_augmented_trial_dimensions']==[11,29,30] and summary['largest_filtered_trial_max_q']==6 and summary['new_higher_moments'] is False
    previous=F(39,500);reports=[]
    for i,entry in enumerate(summary['intervals'],1):
        assert entry['file']==f'coverage/interval_{i:03d}.json';r=load(SRC/entry['file']);lo,hi=frs(r['coupling_interval']);assert lo==previous;previous=hi
        assert r['coupling_interval']==entry['coupling_interval'] and r['all_integer_L_ge2_gap']==entry['gap_lower'] and r['beta_initial']==entry['beta_initial']
        report=audit_record(r,models);reports.append(report);print('REPLAY PASS',i,r['coupling_interval'],report['gap_display'],flush=True)
    assert previous==F(2,25);newgap=min(F(r['all_integer_L_ge2_gap']) for r in reports)
    assert newgap==F(summary['all_integer_L_ge2_uniform_gap'])==F(4107651847,500000000000)
    old=load(PRIOR/'results/SUMMARY.json');assert old['combined_coupling_interval']==['0','39/500'] and old['combined_closed_intervals']==31 and old['unique_finite_volume_ground']
    oldgap=F(old['combined_all_integer_L_ge2_uniform_gap']);assert oldgap==F(486442811,250000000000)
    u=F(1,500);assert 49/(2*(1-7*u)**2)<32 and 32*u<1 and 5*u<=F(1,100) and 20/(1-20*u)<=32
    result=dict(status='PRELIMINARY EXACT REPLAY ONLY; NOT ACCEPTED' if a.preliminary else 'PASS independent joint-aware continuous interval and all-integer-size review',accepted=not a.preliminary,extension_interval=['39/500','2/25'],extension_closed_intervals=2,extension_all_integer_L_ge2_uniform_gap=str(newgap),extension_gap_display=float(newgap),combined_coupling_interval=['0','2/25'],combined_closed_intervals=33,combined_all_integer_L_ge2_uniform_gap=str(min(oldgap,newgap)),combined_uniform_gap_display=float(min(oldgap,newgap)),unique_finite_volume_ground=True,base_trial_dimensions=[11,29,29],filtered_augmented_dimensions=[11,29,30],retained_denominator_levels=[1,1],retained_numerator_contributions=1,maximum_physical_spins=128,maximum_full_Hilbert_dimension=str(4**64),new_moments=False,odd_band_inputs=False,producer_modules_imported=0,eigensolver_calls=0,sources=sources,intervals=reports,runtime_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)),address_space_cap_bytes=1024**3,blas_threads=1)
    save('PRELIMINARY.json' if a.preliminary else 'SUMMARY.json',result);print(result['status'],'gap',newgap,'seconds',result['runtime_seconds'],'RSS',result['peak_rss_kib'],flush=True)
if __name__=='__main__':main()
