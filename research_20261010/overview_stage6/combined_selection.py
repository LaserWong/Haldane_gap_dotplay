"""The combined audit must already have a final status and intact manifest."""
def add_combined(api):
    source,seal,add,R=map(api.get,['source','seal','add','R'])
    seal('combined_ground_review')
    status_path=R+'combined_ground_review/REVIEW_STATUS.json';status=source(status_path)
    assert str(status['status']).startswith('PASS'),status['status']
    proofs=[status_path,R+'combined_ground_review/REVIEW.md',R+'combined_ground_review/results/summary.json',R+'combined_ground_review/results/dependency_seals.json',R+'combined_ground_review/results/short_size_review.json']
    for file,rank in [('accepted_certificates.json',193),('ground_only_certificates.json',1)]:
        p=R+'combined_ground_review/results/'+file;rows=source(p)
        assert len(rows)==(30 if rank==193 else 11)
        for i,a in enumerate(rows):
            assert a['accepted'] and a['complete_integer_cover']
            assert a['ground_only_numerator']==(rank==1)
            r=add('ordinary_spinhalf_bilayer','g',a['g'],p,f'/{i}/all_integer_L_ge2_gap',proofs,beta=a['beta'],onset=a['onset'],route=a['variant']+('_ground_only' if rank==1 else '_full_band'),rank=rank,higher=True,note='Independent filtered-numerator thermal ratios, exact canonical transport, all finite windows and L=2..7 bridge. Largest filtered numerator consumes existing higher moments even for rank one. Isolated coupling only.')
            r['bootstrap_order']=a['order'];r['tail_variant']='quadratic'
    p=R+'combined_ground_review/results/comparison_review.json';d=source(p)
    comparison=[]
    for i,row in enumerate(d['results']):
        for variant,a in row['variants'].items():
            comparison.append(dict(g=row['g'],variant=variant,**a,evidence_source=p,evidence_sha256=api['sources'][p],evidence_json_pointer=f'/results/{i}/variants/{variant}',qualification=d['comparison']))
    api['COMBINED_COMPARISONS']=comparison
    api['csv_write']('combined_route_comparison.csv',comparison)
    p=R+'combined_ground_review/results/selected_failures.json';d=source(p)
    api['csv_write']('combined_selected_failures.csv',d)
    api['statuses'].append(dict(model='ordinary_spinhalf_bilayer',parameter_exact='1/10',status='combined_filter_bounded_scan_no_success',gap_lower_exact=None,evidence_source=status_path,evidence_sha256=api['sources'][status_path],scope='Recorded bounded temperature and fixed-order proposals only. No all-temperature or all-method obstruction and no physical gaplessness claim.'))
