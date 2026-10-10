"""Independent acceptance: physical first moments, traces, transport, all sizes."""
from audit_physical_minimal import *
SRC=HERE/'snapshot/research_20261010'

def check_snapshot():
    hashes=load(HERE/'INPUT_SHA256.json')
    for name,digest in hashes.items():assert sha(HERE/'snapshot'/name)==digest,name
    inherited=load(HERE/'INHERITED_REVIEWS.json')
    for prior,witness in inherited.items():
        manifest=RESEARCH/prior/'MANIFEST_SHA256.json'
        assert sha(manifest)==witness['manifest_sha256']
        mapping=load(manifest)
        assert sha(RESEARCH/prior/'INPUT_SHA256.json')==mapping['INPUT_SHA256.json']
        assert sha(RESEARCH/prior/'REVIEW.md')==mapping['REVIEW.md']
    accepted=load(RESEARCH/'tail_comparison_review/INPUT_SHA256.json')
    for shape in ['4x4','8x4']:
        for tag in ['g3d100','g1d25','g1d20','g3d50']:
            name=f'low_band/tail_comparison/quadratic/temple_{shape}_{tag}.json'
            assert sha(SRC/name)==accepted[name]
    return hashes

def main():
    check_snapshot();rows=[];physical=[]
    fs=rebuild_fs();save('fs_reconstruction.json',fs)
    short=[]
    for side in range(2,8):
        rec=load(SRC/f'low_band/frontier_g006/small_sizes/number_bins_{side}x{side}_g3d50.json')
        # These exact files were independently accepted in alternative_order_review.
        known=load(RESEARCH/'alternative_order_review/INPUT_SHA256.json')
        name=f'small_sizes/number_bins_{side}x{side}_g3d50.json'
        assert sha(SRC/'low_band/frontier_g006'/name)==known[name]
        short.append(F(rec['bins'][1]['lower']))
    for g,beta in [('3/100','259/20'),('1/25','47/4'),('1/20','199/20'),('3/50','203/20')]:
        g,beta=F(g),F(beta);tag=f'g{g}'.replace('/','d');d=SRC/'low_band/reduced_input'
        gr=load(d/f'largest_ground_{tag}.json');energy,greport=inspect_ground(gr,g)
        tr=load(d/f'largest_triplet_GA_{tag}.json');triplets,modes,treport=inspect_triplet(tr,g)
        physical.append(dict(g=str(g),ground=greport,triplets=treport,all_64_exact_fourier_modes_checked=True))
        smaller=[load(SRC/f'low_band/tail_comparison/quadratic/temple_{shape}_{tag}.json') for shape in ['4x4','8x4']]
        for mode in ['ground_only','trial193']:
            rec=load(d/f'{mode}_{tag}.json');assert F(rec['g'])==g and F(rec['beta_initial'])==beta
            first=rec['largest_first_moment_certificate']
            assert all(first[k]==greport[k] for k in ['norm','shifted_rayleigh','energy_rayleigh'])
            levels=[(1,energy)]+(triplets if mode=='trial193' else [])
            assert first['trial_trace_rank']==sum(m for m,e in levels)
            assert first['optional_triplet_first_moments']==(modes if mode=='trial193' else [])
            ell=sum(m*expi(-2*beta*(e-energy))[0] for m,e in levels)
            assert F(rec['largest_normalized_trace_lower'])<=ell
            s=scalar(beta,*smaller,energy,ell)
            assert [F(rec[k]) for k in ['J1','J2','C0']]==[s[k] for k in ['J1','J2','C0']]
            assert list(map(F,rec['permuted_first_purities']))==s['permuted']
            assert list(map(F,rec['canonical_first_purities']))==s['canonical']
            boot=replay(s['canonical'],2*beta);saved=rec['bootstrap']
            assert boot['gap']==F(saved['uniform_square_gap_lower'])
            assert boot['n']==saved['n']==saved['m'] and boot['beta']==F(saved['beta'])
            assert boot['defects']==list(map(F,saved['defects'])) and boot['u']==F(saved['u'])
            assert boot['updates']==[list(map(F,u['defects'])) for u in saved['updates']]
            states=[s['canonical']]+[[1-x for x in u] for u in boot['updates']]
            windows=[];required=[]
            for j,(abc,wrec) in enumerate(zip(states,rec['finite_windows'])):
                b=2*beta*2**j;n=8*2**j;thermal,wgap=window(abc,b)
                assert n==wrec['n'] and 2*n==wrec['through']
                assert thermal==F(wrec['thermal_lower'])
                reported=F(wrec['gap_lower']);assert 0<reported<=wgap and expi(b*reported)[1]*(1-thermal)<thermal
                windows.append(dict(n=n,through=2*n,gap=str(reported)))
                if n<boot['n']:required.append(reported)
            assert len(states)==len(rec['finite_windows'])
            target=min([boot['gap'],min(short)]+required)
            assert target==F(rec['all_integer_L_ge2_gap']) and min(short)==F(rec['small_L2_through_L7_common_gap'])
            for name,digest in rec['numeric_files_read_sha256'].items():assert sha(SRC/name)==digest
            rows.append(dict(g=str(g),mode=mode,beta_initial=str(beta),numerator_trial_rank=len(levels) if mode=='ground_only' else 193,independent_GK_GA_and_ratios_equal=True,canonical_transport_and_recursion_equal=True,all_integer_square_L_ge=2,asymptotic_onset=boot['n'],finite_windows=windows,gap=str(target),gap_display=float(target)))
            print('REDUCED PASS',g,mode,float(target),flush=True)
        save('physical_first_moments.json',physical);save('all_size_replay.json',rows)
    return rows
if __name__=='__main__': main()
