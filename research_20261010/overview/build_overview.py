#!/usr/bin/env python3
"""Extract a deliberately frozen claim selection; do not run research or eigensolvers."""
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
R = 'research_20261010/'
SOURCES = {}
ROWS = []
DIMS = []
STATUS = []


def source(path):
    data = (ROOT / path).read_bytes()
    SOURCES[path] = hashlib.sha256(data).hexdigest()
    return json.loads(data) if path.endswith('.json') else data.decode()


def ptr(doc, pointer):
    for token in pointer.strip('/').split('/') if pointer else []:
        token = token.replace('~1','/').replace('~0','~')
        doc = doc[int(token)] if isinstance(doc, list) else doc[token]
    return doc


def floor12(value):
    f = F(value)
    n = f.numerator * 10**12 // f.denominator
    return f'{n // 10**12}.{n % 10**12:012d}'


def claim(model, parameter, value, primary, pointer, evidence, status='independent_review_passed',
          kind='point', lower=None, beta=None, base=None, note=''):
    d = source(primary)
    gap = str(F(ptr(d, pointer)))
    files = list(dict.fromkeys([primary] + evidence))
    for f in files:
        source(f)
    row = dict(id=f'{model}_{kind}_{value}', model=model, parameter=parameter,
               parameter_exact=str(F(value)), parameter_lower_exact=str(F(lower)) if lower is not None else None,
               parameter_decimal=float(F(value)), parameter_kind=kind,
               fixed_J_exact='3/10' if model=='fully_frustrated_bilayer' else None,
               unit_coupling='strong bond = 1' if model=='alternating_spin1_chain' else 'rung = 1',
               gap_lower_exact=gap, gap_lower_decimal_down_12=floor12(gap),
               size_variable='M (two-spin cells)' if model=='alternating_spin1_chain' else 'L (square side)',
               integer_size_min=2, unique_finite_volume_ground_state=True,
               boundary='periodic; positive-direction adjacency multiplicities retained at size 2',
               evidence_status=status, initial_beta_exact=beta, asymptotic_base_size=base,
               primary_source=primary, primary_json_pointer=pointer,
               primary_sha256=SOURCES[primary], evidence_sources=files, notes=note)
    ROWS.append(row)
    return row


def dimension(model, coupling, geometry, full, retained, proposal, expanded, reached, path, pointer,
              scope='ground trial', depth=None, notes=''):
    source(path)
    DIMS.append(dict(model=model, parameter_exact=coupling, seed_geometry=geometry,
                     full_Hilbert_dimension=full, retained_low_band_count=retained,
                     proposal_basis_dimension=proposal, expanded_vector_support=expanded,
                     full_H_applied_support=reached, MPS_bond_dimension=None,
                     support_scope=scope, support_depth=depth, evidence_source=path,
                     evidence_json_pointer=pointer, evidence_sha256=SOURCES[path], notes=notes))


def build():
    p='audit/independent/certificate_s1_W1_g1d20_k0_audit.json'
    claim('alternating_spin1_chain','g','1/20',p,'/seeds/2/gap_lower',
          ['audit/PROOF.md'] if (ROOT/'audit/PROOF.md').exists() else ['README_先读.md'],
          beta='10',note='Historical independently reviewed baseline; M=2 and M=4 finite seed patches.')
    q='low_energy/certificate_s1_W1_g1d20_k0.json';d=source(q)
    for i,g in enumerate(d['ground_certificates']):
        dimension('alternating_spin1_chain','1/20',f"M={g['M']}",g['full_dimension'],1,
                  g['ritz_sector_dimension'],None,None,q,f'/ground_certificates/{i}',
                  notes='Proposal dimension is the full Sz=0 sector; nonzero support was not separately recorded here.')

    for tag,g,depth in [('g1d10_n4_depth2','1/10',2),('g1d8_n4_depth3','1/8',3),('g3d20_n4_depth4','3/20',4)]:
        p=R+f'chain_audit/chain_sparse_s1_{tag}_independent_audit.json';d=source(p);b=d['all_size_bridge']
        claim('alternating_spin1_chain','g',g,p,'/all_size_bridge/uniform_gap_lower',
              [R+'chain_audit/CHAIN_CERTIFICATE_PROOF.md'],beta=b['best_seed_beta'],base=b['bootstrap_from'])
        for i,a in enumerate(d['ground_checks']):
            dimension('alternating_spin1_chain',g,f"M={a['N_dimers']}",a['full_dimension'],a['retained_states'],
                      a['trial_dimension'],a['trial_dimension'],a['full_Hv_support'],p,f'/ground_checks/{i}',depth=depth,
                      notes='Selected coordinate-space size; expanded support is the coordinate basis size, not a count of nonzero coefficients.')

    for tag,g in [('g4d25','4/25'),('g161d1000','161/1000'),('g129d800','129/800')]:
        p=R+f'chain_frontier_review/chain_sparse_s1_{tag}_n4_depth4_independent_review.json';d=source(p);b=d['bridges']['best']
        claim('alternating_spin1_chain','g',g,p,'/bridges/best/all_M_ge2_gap',
              [R+'chain_frontier_review/FRONTIER_PROOF.md'],beta=b['beta'],base=b['asymptotic_from'])
        for i,a in enumerate(d['grounds']):
            dimension('alternating_spin1_chain',g,f"M={a['N_dimers']}",a['full_dimension'],a['retained_states'],a['trial_dimension'],
                      a['trial_dimension'],a['full_Hv_support'],p,f'/grounds/{i}',depth=4,
                      notes='Selected coordinate-space size; expanded support is the coordinate basis size.')
        a=d['bridges'].get('short_M7_ground_check')
        if a:
            dimension('alternating_spin1_chain',g,'M=7',a['full_dimension'],1,a['trial_dimension'],a['trial_dimension'],
                      a['full_Hv_support'],p,'/bridges/short_M7_ground_check',scope='short-size bridge ground trial',depth=2)

    p=R+'bilayer_audit/optimized_bilayer_audit.json';d=source(p)
    for g,key in [('1/100','g001'),('1/50','g002')]:
        claim('ordinary_spinhalf_bilayer','g',g,p,f'/bridges/{key}/all_integer_squares_ge_2_gap',[R+'bilayer_audit/PROOF.md'])
    for i,a in enumerate(d['ground_checks']):
        dimension('ordinary_spinhalf_bilayer',a['g'],'x'.join(map(str,a['shape'])),a['full_Hilbert_dimension'],a['retained_states'],
                  a['linear_trial_dimension'],a['linear_trial_dimension'],a['full_H_applied_union_support'],p,f'/ground_checks/{i}',
                  notes='q<=2, Sz=0 coordinate proposal; one vector retained.')

    p=R+'low_band_review/symmetric_finite_window_results.json'
    claim('ordinary_spinhalf_bilayer','g','3/100',p,'/files/0/records/0/all_integer_gap_lower',
          [R+'low_band_review/REVIEW.md',R+'low_band_review/NUMBER_AND_BRIDGE_REVIEW.md',
           R+'low_band_review/SYMMETRY_VARIANT_REVIEW.md',R+'low_band_review/symmetric_ground_results.json',
           R+'low_band_review/symmetric_correlated_fast_results.json',R+'low_band/symmetric_correlated_beta909d100_FINAL.json'],
          beta='909/100',base=128,note='Frozen independently reviewed seed. Later scalar continuations are excluded.')
    p=R+'low_band_review/symmetric_ground_results.json';d=source(p)
    for i,a in enumerate(d['records']):
        x,y=map(int,a['shape'].split('x'));N=x*y
        dimension('ordinary_spinhalf_bilayer','3/100',a['shape'],4**N,1+3*N,a['linear_dimension'],a['expanded_support'],
                  a['full_reached_support'],p,f'/records/{i}',scope='proposal/support are ground-only; retained count is entire band',depth=1,
                  notes='Retained band = ground plus 3N excited states. The 11-dimensional ground proposal is not the 49-dimensional band.')

    p=R+'nonperturbative_audit/ff_seed_J3d10_eps1d200_depth0_audit.json';d=source(p)
    claim('fully_frustrated_bilayer','epsilon','1/200',p,'/best_all_sizes/all_integer_L_ge2_gap',
          [R+'nonperturbative_audit/BASELINE_PROOF.md'],beta=d['best_all_sizes']['beta'],base=d['best_all_sizes']['bootstrap_n'])
    for i,a in enumerate(d['ground_checks']):
        dimension('fully_frustrated_bilayer','epsilon=1/200; J=3/10','x'.join(map(str,a['geometry'])),a['full_dimension'],1,
                  a['trial_dimension'],a['trial_dimension'],a['reached_dimension'],p,f'/ground_checks/{i}',
                  notes='q<=2, Sz=0 coordinate proposal; one vector retained.')
    p=R+'nonperturbative_audit/epsilon_scan_summary.json';d=source(p)
    for eps,tag in [('3/500','3d500'),('3/400','3d400')]:
        i=next(i for i,a in enumerate(d) if a['epsilon']==eps);b=d[i]['best_all_sizes']
        claim('fully_frustrated_bilayer','epsilon',eps,p,f'/{i}/best_all_sizes/all_sizes_gap',
              [R+f'nonperturbative_audit/ff_eps{tag}_selected_seeds_audit.json',R+'nonperturbative_audit/EPSILON_FRONTIER.md'],
              beta=b['beta'],base=b['n'])
    p=R+'root_review/ff_frontier_finite_windows.json';d=source(p)
    for i,a in enumerate(d):
        eps=a['epsilon'];tag=eps.replace('/','d')
        claim('fully_frustrated_bilayer','epsilon',eps,p,f'/{i}/best/all_integer_L_ge2_gap',
              [R+'root_review/FF_FRONTIER_BRIDGE.md',R+'root_review/FINITE_WINDOW_INTERPOLATION.md',
               R+f'nonperturbative_audit/ff_eps{tag}_selected_seeds_audit.json'],
              status='root_scalar_bridge_on_independently_audited_physical_inputs',
              beta=a['best']['initial_beta'],base=a['best']['original_asymptotic_n'],
              note='New all-L root scalar bridge; a separate complete bridge replay is not claimed by this overview.')
    p=R+'nonperturbative_audit/vacuum_interval_certificates.json';d=source(p)
    for i,a in enumerate(d):
        if not a.get('best_uniform_all_sizes_gap'):continue
        claim('fully_frustrated_bilayer','epsilon',a['epsilon_interval'][1],p,f'/{i}/best_uniform_all_sizes_gap',
              [R+'nonperturbative_audit/INTERVAL_INDEPENDENT_REVIEW.md',R+'nonperturbative_audit/EPSILON_FRONTIER.md'],
              kind='closed_interval',lower=a['epsilon_interval'][0],beta=a['best_beta'],base=a['best_n'],
              note='A single product trial; affine endpoint PSD and full residual establish every epsilon in this interval.')
        if a['epsilon_interval'][1]=='19/4000':
            for j,c in enumerate(a['ground_checks']):
                dimension('fully_frustrated_bilayer','0<=epsilon<=19/4000; J=3/10','x'.join(map(str,c['geometry'])),c['full_dimension'],1,1,1,
                          c['reached_dimension_at_nonzero_epsilon'],p,f'/{i}/ground_checks/{j}',
                          notes='One product vector; reached support is for nonzero epsilon. At epsilon=0 the shifted residual is zero.')

    # Method failures are separate records, with no numerical gap assigned.
    for tag,g in [('chain_sparse_s1_g323d2000_n4_depth5','323/2000'),('chain_sparse_s1_g13d80_n4_depth4','13/80'),('g7d40','7/40')]:
        p=R+f'chain_frontier_review/{tag}_obstruction_independent_review.json';d=source(p)
        assert d['status'].startswith('PASS')
        STATUS.append(dict(model='alternating_spin1_chain',parameter_exact=g,status='independently_reviewed_recipe_obstruction',
                           gap_lower_exact=None,evidence_source=p,evidence_sha256=SOURCES[p],
                           scope='Every beta>0 and valid local comparison in the specified ground-only numerator/dimer-bin tail/G-recursion recipe; no physical gaplessness or monotone threshold claim.'))
    p=R+'nonperturbative_audit/epsilon_scan_summary.json';d=source(p)
    for a in d:
        if a['epsilon'] in ['9/1000','1/100','1/80','3/200','1/50']:
            STATUS.append(dict(model='fully_frustrated_bilayer',parameter_exact=a['epsilon'],status='tested_grid_no_success',
                               gap_lower_exact=None,evidence_source=p,evidence_sha256=SOURCES[p],
                               scope='Only recorded q<=2 trial, tail and beta=12:0.5:120 proposal grid plus selected exact checks; not a no-go theorem.'))
    p=R+'low_band/scalar_refinement/symmetric_beta909d100_eight_rounds.json';source(p)
    STATUS.append(dict(model='ordinary_spinhalf_bilayer',parameter_exact='3/100',status='later_scalar_refinement_pending',
                       gap_lower_exact=None,evidence_source=p,evidence_sha256=SOURCES[p],
                       scope='Candidate scalar bound 11205710127059/1000000000000000 = 0.011205710127059 for L>=1024; outside the frozen beta=909/100 independent review, with all-size bridge not yet promoted; not plotted.'))
    p=R+'low_band_review/README.md';source(p)
    STATUS.append(dict(model='ordinary_spinhalf_bilayer',parameter_exact='1/25;1/20',status='stronger_coupling_work_outside_completed_review',
                       gap_lower_exact=None,evidence_source=p,evidence_sha256=SOURCES[p],
                       scope='g=.04/.05 frontier work and any grid failures are outside this reviewed snapshot; no zero-gap values are assigned.'))
    p='two_d_theory/NONPERTURBATIVE_MODELS.md';source(p)
    # Document-only analytic anchor: explicitly separated from executable certificate rows.
    analytic=dict(model='fully_frustrated_bilayer',J_exact='3/10',epsilon_exact='0',gap_lower_exact='2/5',
                  scope='all periodic rectangles nx,ny>=2',status='analytic_reference_theorem',source=p,source_sha256=SOURCES[p],
                  note='The family theorem is min(1,4-12J) for 0<=J<1/3. At J=.3, square L>=3 has actual gap 1. Neither value is inferred from perturbation scans.')
    from extend_overview import add_extensions
    add_extensions(globals())
    out=dict(schema_version=2,claim_selection='2026-10-10 14:12 EDT / 18:12 UTC',
             source_commit_reported_by_project='6be889a30f642bde77fb89af75b3a7379615bed1',
             git_checkout_verified=False,root_note='Materialized tree has no .git metadata; provenance is by file hash.',
             claims=ROWS,dimensions=DIMS,unplotted_status=STATUS,analytic_reference=analytic,sources=SOURCES)
    (HERE/'overview_data.json').write_text(json.dumps(out,indent=2)+'\n')
    for name,rows in [('certified_bounds.csv',ROWS),('trial_dimensions.csv',DIMS),('unplotted_status.csv',STATUS)]:
        with (HERE/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for row in rows for k in row)));w.writeheader()
            for row in rows:
                w.writerow({k:' | '.join(v) if isinstance(v,list) else v for k,v in row.items()})
    print(f'Extracted {len(ROWS)} certified claim rows, {len(DIMS)} seed-dimension rows, {len(STATUS)} unplotted status rows; {len(SOURCES)} source hashes.')


if __name__=='__main__':
    build()
