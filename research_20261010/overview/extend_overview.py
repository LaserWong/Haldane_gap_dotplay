"""Explicit additions from the sealed 18:09 UTC angle-based review snapshot."""
from fractions import Fraction as F


def add_extensions(api):
    R,source,claim,dimension,rows,dims,status,sources = [api[x] for x in ('R','source','claim','dimension','ROWS','DIMS','STATUS','SOURCES')]
    p=R+'epsilon_interval_review/audit_results.json';d=source(p)
    assert d['status'].startswith('PASS independent complete continuum')
    for endpoint,pointer in [('17/2000','/uniform_gap_through_17_over_2000'),('171/20000','/uniform_gap')]:
        claim('fully_frustrated_bilayer','epsilon',endpoint,p,pointer,[R+'epsilon_interval_review/INDEPENDENT_REVIEW.md'],
              kind='closed_interval',lower='0',note='Continuous union of seven audited closed pieces; product trial on the baseline piece and fixed q<=2 Ritz vectors on extension pieces. Not a single-product-trial claim.')
    for key,a in d['physical_polynomials'].items():
        if a['center']!='17/2000':continue
        dimension('fully_frustrated_bilayer','0<=epsilon<=171/20000; J=3/10','x'.join(map(str,a['geometry'])),a['full_dimension'],1,
                  a['trial_dimension'],a['trial_dimension'],a['full_action_union'],p,'/physical_polynomials/'+key.replace('~','~0').replace('/','~1'),
                  notes='Fixed rational Ritz vector at epsilon=.0085 used for the final interval pieces; one retained vector. Other pieces use their separately audited vectors.')

    p=R+'root_review/large_seed_bridges/eight_round_scalar_results.json';d=source(p)
    assert d['status'].startswith('PASS independent exact eight-round')
    claim('ordinary_spinhalf_bilayer','g','3/100',p,'/all_integer_L_ge2_gap',
          [R+'root_review/large_seed_bridges/PROOF.md',R+'low_band_review/symmetric_correlated_fast_results.json'],beta='909/100',base=1024,
          note='Independently audited eight-round scalar continuation and all-integer bridge of the frozen small physical seed; retained in data, superseded in main plot by the large-seed certificate.')

    p=R+'large_seed_review/REVIEW_STATUS.json';d=source(p)
    assert d['status'].startswith('PASS independent physical')
    assert d['updated_at_utc']=='2026-10-10T18:09:00Z'
    proof=R+'large_seed_review/REVIEW.md'
    tr=R+'large_seed_review/results/trace_replay.json';trace=source(tr)
    for i,a in enumerate(d['accepted']):
        t=next(t for t in trace if t['g']==a['g'])
        assert a['all_integer_L_ge']==2 and F(a['gap'])==F(t['gap'])
        claim('ordinary_spinhalf_bilayer','g',a['g'],p,f'/accepted/{i}/gap',
              [proof,tr,R+'large_seed_review/results/all_size_bridge_review.json',R+'large_seed_review/results/patch_replay.json',
               R+'large_seed_review/results/ground_replay.json',R+'large_seed_review/results/translation_replay.json'],
              beta=t['beta_initial'],base=a['asymptotic_onset'],note='Sealed angle-based large-seed review. Physical seed family 4x4,8x4,8x8. Optional Temple variant excluded.')
    gr=R+'large_seed_review/results/ground_replay.json';grounds=source(gr)
    tp=R+'large_seed_review/results/translation_replay.json';translations=source(tp)
    pp=R+'large_seed_review/results/patch_replay.json';patches=source(pp)
    for i,a in enumerate(patches):
        ground=next(g for g in grounds if g['g']==a['g'] and g['shape']==a['shape'])
        translated=next(t for t in translations if t['g']==a['g'] and t['shape']==a['shape'])
        dimension('ordinary_spinhalf_bilayer',a['g'],a['shape'],a['full_Hilbert_count'],a['retained_band'],ground['dimension'],None,None,pp,f'/{i}',
                  scope='ground proposal dimension; separate translated-column support fields',depth=1,
                  notes='The retained band has 1+3N states. Ground proposal has 11 or 29 compressed vectors. Translation support is for one spin-1 highest-weight column, not ground support or entire band support.')
        dims[-1]['translated_column_support']=translated['W_support']
        dims[-1]['translated_H_applied_support']=translated['HW_support']
        dims[-1]['translated_band_columns_per_spin_copy']=(a['retained_band']-1)//3
        dims[-1]['additional_evidence_sources']=' | '.join([gr,tp,proof])

    # The separately sealed rank-one sector-Temple numerical audit supersedes the angle points.
    p=R+'temple_variant_review/REVIEW_STATUS.json';d=source(p)
    assert d['status'].startswith('PASS independent exact sector-Temple')
    assert d['prior_manifest_sha256']=='058ded69771bffe4822090fc8f88175592e5170e932173962fd32d02bd1d056d'
    for i,a in enumerate(d['accepted']):
        assert a['all_integer_L_ge']==2
        claim('ordinary_spinhalf_bilayer','g',a['g'],p,f'/accepted/{i}/gap',
              [R+'temple_variant_review/REVIEW.md',R+'temple_variant_review/results/patch_review.json',
               R+'temple_variant_review/results/trace_and_all_size_review.json',R+'large_seed_review/REVIEW_STATUS.json'],
              beta=a['beta_initial'],base=a['asymptotic_L_ge'],
              note='Sealed independent rank-one sector-Temple endpoint, trace, recurrence and all-size audit; inherits identical independently verified physical moments and complete band count.')
    status[:]=[s for s in status if s['model']!='ordinary_spinhalf_bilayer']
    for r in rows:
        r['id'] += '__'+r['primary_source'].replace('/','_').removesuffix('.json')
        r['plotted_in_main_figure']=True
    for r in rows:
        if r['parameter_kind']=='point':
            competitors=[s for s in rows if s['model']==r['model'] and s['parameter_kind']=='point' and s['parameter_exact']==r['parameter_exact']]
            r['plotted_in_main_figure']=F(r['gap_lower_exact'])==max(F(s['gap_lower_exact']) for s in competitors)
    for d in dims:
        n=int(d['seed_geometry'][2:]) if d['seed_geometry'].startswith('M=') else __import__('math').prod(map(int,d['seed_geometry'].split('x')))
        d['dimer_or_rung_count']=n;d['physical_spin_count']=2*n
        for key in ('translated_column_support','translated_H_applied_support','translated_band_columns_per_spin_copy','additional_evidence_sources'):
            d.setdefault(key,None)
