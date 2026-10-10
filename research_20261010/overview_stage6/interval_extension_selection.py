"""Add the separately sealed continuous extension, with no interpolation of dots."""
def add_interval_extension(api):
    source,seal,add,dim,R=map(api.get,['source','seal','add','dim','R'])
    seal('interval_extension_review')
    p=R+'interval_extension_review/results/SUMMARY.json';s=source(p)
    assert s['status']=='PASS independent auxiliary/filter continuous extension and all-integer-size review'
    assert s['extension_closed_intervals']==15 and s['combined_closed_intervals']==31
    proofs=[R+'interval_extension_review/REVIEW_STATUS.json',R+'interval_extension_review/REVIEW.md',R+'ordinary_interval_review/REVIEW_STATUS.json']
    add('ordinary_spinhalf_bilayer','g','39/500',p,'/combined_all_integer_L_ge2_uniform_gap',proofs,kind='closed_interval',lo='0',route='uniform_interval_union',rank=1,higher=True,note='Union of the separately sealed 16 G/K-only-largest pieces on [0,.07] and 15 filtered-largest pieces on [.07,.078]. Uniform for every integer L>=2. Existing higher moments enter only the filtered-largest extension.')
    x=add('ordinary_spinhalf_bilayer','g','39/500',p,'/extension_all_integer_L_ge2_uniform_gap',proofs,kind='closed_interval',lo='7/100',route='filtered_interval_extension_union',rank=1,higher=True,note='Whole 15-piece extension [.07,.078]. Only the largest numerator is filtered. Search dimensions 11/29/29 and total working spans 11/29/<=30.')
    x['plotted_in_main_figure']=False
    for i,a in enumerate(s['intervals']):
        lo,hi=a['coupling_interval']
        x=add('ordinary_spinhalf_bilayer','g',hi,p,f'/intervals/{i}/all_integer_L_ge2_gap',proofs,kind='closed_interval',lo=lo,beta=a['beta_initial'],onset=a['asymptotic_onset'],route='filtered_interval_extension_piece',rank=1,higher=True,note='Independent fixed-vector closed interval, auxiliary-ground denominator and filtered-largest numerator, every integer L>=2. No additional physical higher moments beyond existing G/K/J.')
        x['plotted_in_main_figure']=False
    for k,(shape,n) in enumerate([('4x4',16),('8x4',32),('8x8',64)]):
        d=dim('ordinary_spinhalf_bilayer','7/100<=g<=39/500',shape,4**n,s['base_trial_dimensions'][k],p,f'/base_trial_dimensions/{k}','continuous filtered-largest extension',retained=1 if k<2 else None,rank=1 if k==2 else None,upper=30 if k==2 else None,q=6 if k==2 else None,note='Only the largest numerator receives a residual-direction filter. The working dimensions are 11/29/<=30. Largest existing higher moments are used, unlike the baseline interval.')
        d['original_max_triplet_number']=4
    for r in api['claims']:
        if r.get('certificate_route')=='uniform_interval_union' and r['parameter_exact']=='7/100':r['plotted_in_main_figure']=False
