"""Explicit additions from independently sealed review snapshots."""
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
    # Retain every independently accepted order/tail combination, while plotting only the best per coupling.
    p=R+'tail_comparison_review/REVIEW_STATUS.json';sealed=source(p)
    assert sealed['status']=='passed_independent_exact_recombination_review'
    accepted_path=R+'tail_comparison_review/results/accepted_certificates.json';accepted=source(accepted_path)
    assert len(accepted)==35
    evidence=[p,R+'tail_comparison_review/REVIEW.md',R+'tail_comparison_review/results/summary.json',
              R+'tail_comparison_review/results/path_ledger.json',R+'tail_comparison_review/results/patch_review.json',
              R+'tail_comparison_review/results/small_sizes.json']
    for i,a in enumerate(accepted):
        assert a['independent_exact_arithmetic']
        row=claim('ordinary_spinhalf_bilayer','g',a['g'],accepted_path,f'/{i}/all_integer_L_ge2_gap',evidence,
                  beta=a['beta_initial'],base=a['asymptotic_onset'],
                  note='Independently audited same-physical-input tail/order recombination; all-size bridge included. The '+a['order']+' order is transported exactly to the canonical spatial/thermal staircase. Physical and oscillator counts are not pointwise merged.')
        row['tail_variant']=a['variant'];row['bootstrap_order']=a['order']
    import csv
    comparisons={}
    for filename,output in [('same_order_comparison.json','tail_order_comparison.csv'),('fixed_order_fixed_beta_gains.json','fixed_order_tail_gains.csv')]:
        comparison_path=R+'tail_comparison_review/results/'+filename
        comparison_rows=source(comparison_path)
        enriched=[dict(a,evidence_source=comparison_path,evidence_sha256=sources[comparison_path],evidence_json_pointer=f'/{i}') for i,a in enumerate(comparison_rows)]
        comparisons[filename]=enriched
        with (api['HERE']/output).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for a in enriched for k in a)))
            writer.writeheader();writer.writerows(enriched)
    api['RECOMBINATION_COMPARISONS']=comparisons
    comparison_path=R+'tail_comparison_review/results/same_order_comparison.json'
    status.append(dict(model='ordinary_spinhalf_bilayer',parameter_exact='3/50',status='original_tail_xyt_grid_no_success',gap_lower_exact=None,
                       evidence_source=comparison_path,evidence_sha256=sources[comparison_path],
                       scope='Original physical-number tail in xyt order only: no accepted proposal on the tested grid. Other orders and tails certify this same coupling; no all-beta exclusion or physical gaplessness claim.'))
    patch_path=R+'tail_comparison_review/results/patch_review.json';patches=source(patch_path)
    for i,a in enumerate(patches):
        if a['variant']=='quadratic' and a['g']=='3/50':
            dimension('ordinary_spinhalf_bilayer',a['g'],a['shape'],a['full_hilbert_dimension'],a['retained_full_band_dimension'],
                      a['linear_ground_trial_dimension'],None,None,patch_path,f'/{i}',scope='compressed ground proposal; complete retained band',depth=1,
                      notes='Same 4x4/8x4/8x8 geometry family. Full physical count, ground proposal and retained band are audited; per-column support is not separately extracted in this row. Oscillator reference overcount is not the physical Hilbert dimension.')
            dims[-1]['translated_band_columns_per_spin_copy']=(a['retained_full_band_dimension']-1)//3
    for r in rows:
        r['id'] += '__'+r['primary_source'].replace('/','_').removesuffix('.json')+'__'+r['primary_json_pointer'].replace('/','_')
        r.setdefault('tail_variant',None);r.setdefault('bootstrap_order',None)
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
