# Exact prior independent audit_record, with declared range and numerator adaptation.
def audit_record(r,models):
    lo,hi=frs(r['coupling_interval']);assert F(9,100)<=lo<hi<=F(1,10)
    assert F(r['fixed_vector_center'])==(lo+hi)/2
    trials=r['denominator_patches']+[r['largest_base_trial']];assert len(trials)==3
    rr=[];pp=[]
    for idx,(t,m,shape) in enumerate(zip(trials,models,[(4,4),(8,4),(8,8)])):
        assert t['geometry']==list(shape) and t['N']==math.prod(shape) and t['trial_dimension']==len(m[0])
        rho,p=check_trial(t,m,lo,hi,idx<2);rr.append(rho);pp.append(p)
    filter_report=dict(replaced_by_fixed_43D_numerator=True); check_numerator_metadata(r)
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
