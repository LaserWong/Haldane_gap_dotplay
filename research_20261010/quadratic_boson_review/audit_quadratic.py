"""Independent stable-oscillator, full physical count, and exact bin review."""
from independent_base import *
OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'low_band'/'quadratic_boson';SNAP=OUT/'snapshot'
MANIFEST='FROZEN_MANIFEST_1828.json';EXPECTED='ac5c47a1a3ccff0962b7ad5aac3968834b9ff06026644e0abc56601bec750723'
# The inherited helper's file outputs are review-local because it was copied here.

def freeze():
    assert sha(SRC/MANIFEST)==EXPECTED
    manifest=json.loads((SRC/MANIFEST).read_text())['files'];manifest[MANIFEST]=EXPECTED
    for name,h in manifest.items():
        p=SRC/name;assert sha(p)==h;target=SNAP/name
        if target.exists():assert sha(target)==h
        else:shutil.copyfile(p,target)
    (OUT/'INPUT_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');return manifest

def block_inertia(m):return inertia(rmat(m))
def small_oscillators():
    out=[]
    # Signed unequal frequencies ensure the test does not assume all first excitations are one-particle states.
    for label,alpha,lambdas,O,cutoff in [('one_positive',S.Rational(5,4),[S.Rational(3,4)],S.eye(1),8),
      ('one_negative',S.Rational(5,4),[-S.Rational(3,4)],S.eye(1),8),
      ('two_rotated_unequal',S.Rational(5,4),[S.Rational(3,4),-S.Integer(1)],S.Matrix([[S.Rational(3,5),-S.Rational(4,5)],[S.Rational(4,5),S.Rational(3,5)]]),5)]:
        d=len(lambdas);assert O.T*O==S.eye(d);K=O*S.diag(*lambdas)*O.T
        states=[s for q in range(cutoff+1) for s in occupations(d,q)];target=[s for q in range(cutoff+2) for s in occupations(d,q)]
        lookup={s:i for i,s in enumerate(target)};G=monomial_metric(states);Gt=monomial_metric(target)
        aa=[];ad=[]
        for j in range(d):
            a=S.zeros(len(target),len(states));aD=S.zeros(len(target),len(states))
            for col,s in enumerate(states):
                t=list(s);t[j]+=1;aD[lookup[tuple(t)],col]=1
                if s[j]:t=list(s);t[j]-=1;a[lookup[tuple(t)],col]=s[j]
            aa.append(a);ad.append(aD)
        # The exact source-to-target matrices retain creation leakage through cutoff+1.
        c=[];cd=[];omegas=[]
        for j,lam in enumerate(lambdas):
            w=S.sqrt(alpha**2-lam**2);u=S.sqrt((alpha+w)/(2*w));v=lam/S.sqrt(2*w*(alpha+w))
            assert S.simplify(u*u-v*v)==1
            b=sum((O[i,j]*aa[i] for i in range(d)),S.zeros(len(target),len(states)))
            bd=sum((O[i,j]*ad[i] for i in range(d)),S.zeros(len(target),len(states)))
            c.append(u*b+v*bd);cd.append(u*bd+v*b);omegas.append(w)
        for i in range(d):
            for j in range(d):
                comm=(cd[i].H*Gt*cd[j]-c[j].H*Gt*c[i]).applyfunc(S.simplify)
                assert comm==(G if i==j else S.zeros(len(states)))
        H=S.diag(*[alpha*sum(s) for s in states]);idx={s:i for i,s in enumerate(states)}
        for col,s in enumerate(states):
            for i in range(d):
                for j in range(d):
                    t=list(s);t[i]+=1;t[j]+=1
                    if tuple(t) in idx:H[idx[tuple(t)],col]+=K[i,j]/2
                    t=list(s)
                    if t[j]:
                        n=t[j];t[j]-=1
                        if t[i]:
                            n*=t[i];t[i]-=1;H[idx[tuple(t)],col]+=K[i,j]*n/2
        exactE=sum(w-alpha for w in omegas)/2
        gram=sum((w*z.H*Gt*z for w,z in zip(omegas,c)),S.zeros(len(states)))
        assert (G*H-gram-exactE*G).applyfunc(S.simplify)==S.zeros(len(states))
        delta=min(omegas);v=S.trace(K*K)/2;Eb=-v/(alpha+delta)
        assert exactE>=Eb
        inert=block_inertia((G*H-Eb*G).applyfunc(S.simplify));assert inert[0]==0
        out.append(dict(test=label,modes=d,cutoff=cutoff,source_dimension=len(states),image_dimension=len(target),
           alpha=str(alpha),K=[[str(x) for x in row] for row in K.tolist()],frequencies=list(map(str,omegas)),
           exact_ground_shift=str(exactE),lower_ground_shift=str(Eb),exact_CCR=True,exact_full_leakage_factorization=True,
           lower_ground_PSD_inertia=inert))
        print('OSCILLATOR PASS',label,flush=True)
    save('small_oscillators.json',out);return out

def replay_bins():
    out=[]
    for p in sorted(SNAP.glob('quadratic_bins_*.json')):
        r=json.loads(p.read_text());nx,ny,n,g=r['nx'],r['ny'],r['N'],F(r['g']);assert nx*ny==n and 0<=g<F(1,4)
        d=3*n;ed=graph(nx,ny);v=F(3,4)*g*g*sum(w*w for w in ed.values());alpha=1-2*g;x=1-4*g
        assert r['weighted_edges']==[[i,j,w] for (i,j),w in sorted(ed.items())]
        assert F(r['vacuum_creation_norm_squared'])==v and F(r['creation_matrix_norm_squared_upper'])==4*g*g
        assert F(r['alpha'])==alpha and F(r['delta_squared'])==x
        dl,du=F(r['delta_lower']),F(r['delta_upper']);assert 0<dl<du and dl*dl<=x<du*du
        assert du-dl==F(1,10**40)
        # Independently enclose the root on a binary grid and check its compatibility.
        scale=1<<160;root_integer=math.isqrt(x.numerator*scale*scale//x.denominator)
        il,iu=F(root_integer,scale),F(root_integer+1,scale)
        assert il*il<=x<iu*iu and dl<=iu and il<=du
        eb=-v/(alpha+dl);assert F(r['bosonic_ground_lower'])==eb
        assert r['bosonic_modes']==d and r['physical_hilbert_dimension']==4**n and F(r['energy_shift'])==-F(3*n,4)
        mult=1;position=1;last=None
        for q,row in enumerate(r['bins']):
            if q:mult=mult*(d+q-1)//q
            assert mult==math.comb(d+q-1,q)
            assert row['q']==q and F(row['lower'])==eb+q*dl and row['multiplicity']==mult and row['first_ordered_index']==position
            if last is not None:assert F(row['lower'])>last
            last=F(row['lower']);position+=mult
        assert len(r['bins'])==n+1 and position-1==math.comb(d+n,n)>=4**n
        # The bosonic bin q=2 starts immediately after the 1+3N retained levels.
        assert r['bins'][2]['first_ordered_index']==2+3*n
        out.append(dict(source=p.name,sha256=sha(p),nx=nx,ny=ny,g=str(g),vacuum_norm_squared=str(v),
          all_directed_rational_endpoints_verified=True,all_reference_multiplicities_verified=True,
          full_physical_dimension=4**n,finite_reference_count=position-1,
          finite_reference_count_identity='sum(q=0..N) C(D+q-1,q)=C(D+N,N)',
          a012=[row['lower'] for row in r['bins'][:3]],a012_float_display=[float(F(row['lower'])) for row in r['bins'][:3]]))
        print('BINS PASS',p.name,'a2',float(F(r['bins'][2]['lower'])),flush=True)
    assert len(out)==14;save('bin_replay.json',out);return out

def all_physical_counts(kernel):
    n=4;ed=graph(2,2);states=list(itertools.product(range(4),repeat=n));groups=defaultdict(list)
    for st in states:groups[sum(x!=0 for x in st)%2,sum({0:0,1:-1,2:0,3:1}[x] for x in st)].append(st)
    assert sum(map(len,groups.values()))==256
    saved=json.loads((SNAP/'physical_count_validation.json').read_text());out=[]
    for g in (F(3,100),F(3,50)):
        rec=json.loads((SNAP/f'quadratic_bins_2x2_g{g}.json'.replace('/','d')).read_text());alpha=1-2*g;blocks=[]
        for label,stateset in sorted(groups.items()):
            lookup={st:i for i,st in enumerate(stateset)};dim=len(stateset)
            H=[[F(0) for _ in stateset] for _ in stateset];L=[[F(0) for _ in stateset] for _ in stateset]
            for j,st in enumerate(stateset):
                q=sum(x!=0 for x in st);H[j][j]+=q;L[j][j]+=alpha*q
                for (u,v),w in ed.items():
                    old=4*st[u]+st[v]
                    for z in range(16):
                        if kernel[z][old]:
                            target=list(st);target[u],target[v]=divmod(z,4);target=tuple(target);assert target in lookup
                            i=lookup[target];H[i][j]+=g*w*kernel[z][old]
                            if sum(x!=0 for x in target)!=q:L[i][j]+=g*w*kernel[z][old]
            assert all(H[i][j]==H[j][i] and L[i][j]==L[j][i] for i in range(dim) for j in range(dim))
            comp=inertia([[H[i][j]-L[i][j] for j in range(dim)] for i in range(dim)]);assert comp[0]==0
            blocks.append((label,H,L,comp))
        checks=[]
        for row in rec['bins']:
            t=F(row['lower']);allowed=row['first_ordered_index']-1
            if allowed>=256:continue
            countsH=[];countsL=[]
            for label,H,L,comp in blocks:
                countsH.append(inertia([[H[i][j]-t*(i==j) for j in range(len(H))] for i in range(len(H))]))
                countsL.append(inertia([[L[i][j]-t*(i==j) for j in range(len(L))] for i in range(len(L))]))
            negative=sum(x[0] for x in countsH);negativeL=sum(x[0] for x in countsL)
            assert negative<=negativeL<=allowed
            checks.append(dict(q=row['q'],threshold=str(t),physical_negative_count=negative,compressed_quadratic_negative_count=negativeL,
                reference_allowed_negative_count=allowed,physical_block_inertias=countsH,compressed_block_inertias=countsL))
            print('PHYSICAL COUNT PASS',g,row['q'],negative,negativeL,allowed,flush=True)
        producer=next(x for x in saved['cases'] if F(x['g'])==g)
        assert [(x['q'],x['physical_negative_count'],x['reference_allowed_negative_count']) for x in checks]==[(x['q'],x['full_physical_negative_count'],x['reference_allowed_negative_count']) for x in producer['checks']]
        out.append(dict(g=str(g),shape=[2,2],full_Hilbert_dimension=256,all_256_states_counted=True,
          block_labels=[list(l) for l,_,_,_ in blocks],block_dimensions=[len(h) for _,h,_,_ in blocks],
          H_minus_compressed_L_PSD_inertias=[c for _,_,_,c in blocks],checks=checks))
    save('physical_counts.json',out);return out

def main():
    start=time.monotonic();manifest=freeze();osc=small_oscillators();kernel=local_matrix();bins=replay_bins();physical=all_physical_counts(kernel)
    for name,h in manifest.items():assert sha(SRC/name)==sha(SNAP/name)==h
    result=dict(status='passed_independent_quadratic_comparison_proof_exact_small_mode_factorizations_full_physical_counts_and_14_directed_bins',
      producer_manifest_sha256=EXPECTED,exact_small_mode_cases=len(osc),full_Hilbert_physical_cases=len(physical),frozen_bin_files=len(bins),
      no_new_global_gap_claim=True,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      cpu_affinity=sorted(os.sched_getaffinity(0)),address_space_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0])
    save('summary.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
