#!/usr/bin/env python3
"""Write explanatory tables directly from the already frozen selection."""
from common import *
d=json.loads((HERE/'overview_data.json').read_text());rows=d['claims'];ext=d['interval_extension_included'];combined=d['combined_review_included']
end='0.078' if ext else '0.07';pieces=31 if ext else 16

def table(model):
    out=['| Parameter | Certified gap lower bound |','|---:|---:|']
    selected=sorted([r for r in rows if r['model']==model and r['parameter_kind']=='point' and r['plotted_in_main_figure']],key=lambda r:F(r['parameter_exact']))
    out.extend(f"| {float(F(r['parameter_exact'])):g} | {r['gap_lower_decimal_down_12']} |" for r in selected)
    return '\n'.join(out)

def ground_table():
    out=['| g | 193-direction numerator | One filtered numerator trial |','|---:|---:|---:|']
    for g in ['3/100','1/25','1/20','3/50','7/100','2/25']:
        vals=[]
        for route in ['combined_full_band','combined_ground_only']:
            rs=[r for r in rows if r['parameter_exact']==g and r.get('certificate_route')==route]
            vals.append(max(rs,key=lambda r:F(r['gap_lower_exact']))['gap_lower_decimal_down_12'])
        out.append(f"| {float(F(g)):g} | {vals[0]} | {vals[1]} |")
    return '\n'.join(out)

def interval_table():
    out=['| Closed g interval | Uniform gap lower bound |','|---|---:|']
    rs=sorted([r for r in rows if r.get('certificate_route') in ['uniform_interval_piece','filtered_interval_extension_piece']],key=lambda r:F(r['parameter_lower_exact']))
    for r in rs:out.append(f"| [{float(F(r['parameter_lower_exact'])):g}, {float(F(r['parameter_exact'])):g}] | {r['gap_lower_decimal_down_12']} |")
    return '\n'.join(out)
text=f'''# Certified results and dimension accounting: stage6

Snapshot generated **{d['generated_utc']}**. This new folder preserves the [earlier sealed overview](../overview/README.md) unchanged and adds only independently sealed reviews. It is an exact-data extraction and static visualization, not a new spectral audit or eigensolver run.

![Certified parameter points and intervals](certified_bounds.png)

[Vector PDF](certified_bounds.pdf) · [All exact certificate rows](certified_bounds.csv) · [Latest isolated points](latest_point_bounds.csv) · [Complete data and source hashes](overview_data.json)

## Model, normalization, and scope

The alternating spin-1 chain has unit strong-bond exchange and weak exchange g. Both spin-1/2 bilayers have unit rung exchange. The ordinary square bilayer has straight intralayer exchange g in both directions and layers, without crossed bonds. The near-fully-frustrated model instead has fixed J=0.3, straight exchanges J+ε and crossed exchanges J.

All boundary conditions are periodic. Positive-direction bond multiplicities are retained at side or cell count two. Chain certificates cover **every integer two-spin cell count M≥2**. Both square-bilayer certificate families cover **every integer square side L≥2**. Each positive bound includes a unique finite-volume ground state. Arbitrary rectangles and infinite-volume uniqueness are not inferred, except for the explicitly identified analytic FF reference theorem.

Every displayed decimal is rounded down to 12 decimal places. Exact fractions, initial temperatures, recurrence onset sizes, primary JSON pointers, source hashes, and evidence links are in the CSV/JSON. A dot certifies its individual parameter. A horizontal bar certifies the entire interval. The bounds are sufficient lower bounds, not estimates of the physical gap, an optimal parameter threshold, or a phase boundary. Changes of certificate construction can produce nonmonotone displayed bounds. No monotonicity of the physical gap is claimed.

## Alternating spin-1 chain

{table('alternating_spin1_chain')}

The new [temperature-first independent review](../chain_temperature_review/REVIEW.md) certifies g=0.1615, 0.1625, and 0.175 with bounds **0.039815121561, 0.037716426713, and 0.006791087005**. Its largest M=8 patch uses only an exact Rayleigh quotient of one numerator trial. The original coordinate search still has **43,294 dimensions** in a full space of **9^8=43,046,721** states. One numerator trial does not mean a one-dimensional search, an identified eigenstate, or a largest-patch residual certificate.

The earlier [ground-only/dimer-tail recipe obstructions](../chain_frontier_review/FRONTIER_PROOF.md) at those same couplings remain valid for that specific different update recipe. They are retained as scoped method statements in [unplotted_status.csv](unplotted_status.csv). They do not exclude the new temperature-first route and do not establish physical gaplessness. The g=0.2 failed finite proposal grid remains unplotted and is not an all-temperature theorem.

## Ordinary square bilayer

{table('ordinary_spinhalf_bilayer')}

The strongest plotted isolated points are selected from all accepted routes in this snapshot. Older accepted routes remain in the full data, including the separately [reviewed g=0.07 frontier bound](../bilayer_frontier_review/REVIEW.md) **0.024790852531**, the [ground inverse-moment certificates](../ground_moment_review/REVIEW.md), and the [largest-seed first-moment reduction](../reduced_input_review/REVIEW.md). The g=0.01 and 0.02 points preserve their existing certificates. Their relative heights are not a physical-gap trend.
'''
if combined:
    text+='''
### Independently accepted filtered-numerator combination

The [combined independent review](../combined_ground_review/REVIEW.md) certifies all thermal ratios, spatial/temperature-order transport, asymptotic recurrences, finite interpolation windows, and the short sizes L=2 through 7. The data retain all **30 accepted full-band alternatives and 11 accepted largest-ground-only alternatives**, rather than only the largest value at each coupling.

'''+ground_table()+'''

The table compares accepted combined routes. Full-band and rank-one comparisons at each selected parameter preserve the temperatures recorded in the audit. A 193-direction numerator uses orthogonal trial contributions and the independently certified smaller-patch upper traces. A rank-one largest numerator uses just the filtered ground trial. Neither choice changes the largest physical Hilbert space, **2^128**.

The [route comparison CSV](combined_route_comparison.csv) also preserves the original, ground-pencil-only, filter-only and combined alternatives. Their temperatures were selected individually. Their differences cannot all be attributed to one isolated ingredient at a common temperature. [Selected recipe failures](combined_selected_failures.csv) remain failures of those proposals and are never plotted as zero physical gaps.

The largest filtered numerator uses the existing **G/K/J full second-moment information**. Its small rank does not make this the earlier G/K-only largest-input route. No new H³ or H⁴ moments, complete diagonalization, or filtered-state residual certificate are claimed.
'''
text+=f'''
### Genuine continuous coupling coverage

For **every 0≤g≤{end}** and **every integer L≥2**, the certified uniform gap is

**Δ ≥ 0.001945771244**.

The original [continuous interval review](../ordinary_interval_review/REVIEW.md) establishes 16 adjacent closed pieces on [0,0.07]. On those pieces, the two denominator patches retain one certified ground level each, and the largest 8×8 numerator has rank one and uses **G/K only**. The three original searches have dimensions **11/29/29**.
'''
if ext:
    text+='''
The separately [reviewed continuous extension](../interval_extension_review/REVIEW.md) adds **15 closed pieces on [0.07,0.078]**, with extension-wide bound **0.002006633957**. Their exact union with the original interval has **31 pieces** and preserves the smaller bound **0.001945771244** over [0,0.078]. This statement is derived from interval certificates, not interpolation between the g=0.07 and 0.08 dots.

Only the largest numerator is filtered in this extension. Its working dimensions are **11/29/≤30**, with largest filtered support at triplet number **q≤6**. It consumes the existing largest-seed full second moment G/K/J and computes no new H³/H⁴ moment. This is a different input contract from the first-moment-only baseline interval. The isolated g=0.08 result does not extend the proved continuum from 0.078 to 0.08.
'''
text+=f'''
![All certified ordinary-bilayer closed pieces](ordinary_interval_pieces.png)

[Vector PDF](ordinary_interval_pieces.pdf) · [Every exact closed piece](ordinary_interval_pieces.csv)

{interval_table()}

The horizontal green pieces show their own uniform lower bounds. The purple segment shows the uniform minimum on their entire union. The piecewise bounds need not vary monotonically, since distinct verified constructions are used. The common endpoints are checked as exact rational numbers.

## Near fully frustrated bilayer

The new ordinary-bilayer certificates do not change this separate model. All FF entries are inherited from the earlier sealed overview with their original evidence status.

{table('fully_frustrated_bilayer')}

The independently reviewed ε intervals [0,0.004], [0,0.0045], [0,0.00475], [0,0.0085], and [0,0.00855] have uniform bounds 0.024046763298, 0.014475263367, 0.008090283176, 0.001703099464, and 0.000768515509. The first three use one product vector. The two widest intervals use the [fixed-vector piecewise extension](../epsilon_interval_review/INDEPENDENT_REVIEW.md), not one product state throughout. The ε=0.008 and 0.0085 point markers preserve the more limited evidence label of a supplemental scalar size bridge on independently audited physical inputs.

At ε=0, the [analytic reference theorem](../../two_d_theory/NONPERTURBATIVE_MODELS.md) gives gap at least 2/5 for all periodic rectangles nx,ny≥2 at J=0.3. The stronger actual square gap 1 for L≥3 is not plotted, because it has a different size range.

## Dimensions count different objects

![Physical, search, filtered and numerator dimensions](trial_space_counts.png)

[Vector PDF](trial_space_counts.pdf) · [{len(d['dimensions'])} exact seed and route records](trial_dimensions.csv)

| Physical geometry | Spins | Full Hilbert dimension | Original ground search | Ground search plus one residual direction |
|---|---:|---:|---:|---:|
| 4×4 rungs | 32 | 2^32 = 4,294,967,296 | 11 | ≤12 |
| 8×4 rungs | 64 | 2^64 = 18,446,744,073,709,551,616 | 29 | ≤30 |
| 8×8 rungs | 128 | 2^128 = 340,282,366,920,938,463,463,374,607,431,768,211,456 | 29 | ≤30 |

The original trial lies at q≤4. The residual-direction filtered trial lies at q≤6 and adds at most one implicit direction to its original search. The **≤12/≤30/≤30** entries are upper bounds, not proven exact enlarged dimensions or a newly optimized coordinate basis. These general point-filter dimensions account for filtering each patch. In the strongest time–x–y ratio, the smaller-patch filtered upper expectations cancel from the denominator normalization, so only the largest filtered numerator is needed. The local plane spanned by one chosen trial and its residual has dimension at most two. It does not replace the original search with a two-dimensional global search. One final numerator vector likewise does not make the search one-dimensional.

The [independent filter review](../variational_filter_review/REVIEW.md) verifies these energy-upper-bound and dimension statements. It does not itself prove a complete gap certificate, filtered-state residual, eigenvalue isolation, or low-band completeness. The combined and interval extension reviews separately supply the remaining gap-proof obligations.

A complete-band route can retain **49/97/193 states** on the three patches, including one ground level and 3N triplet levels. In the earlier reduced route, the optional 193 largest vectors are orthogonal numerator trial directions and need not be identified as a complete eigenband. At the largest patch, the old translated triplet generator has 373 configurations and its full H-action has 67,755 configurations. These are per-column support counts, not search dimensions, band dimensions, or the full physical Hilbert dimension.

The first-moment-only reduced route moves the largest required full upper-trace certification to **8×4 rungs**, even though its largest physical numerator patch remains 8×8. Filtering can improve the rank-one numerator using already available second moments, but then that largest numerator no longer has the G/K-only input contract.

The chain and FF dimension records remain available alongside these bilayer records. Unrecorded support or retained-state counts are null, never zero. No dimension in this overview is an MPS bond dimension.

## Provenance, replay, and frozen deliverables

This snapshot contains **{len(d['claims'])} exact certificate rows**, **{len(d['dimensions'])} dimension records**, **{len(d['sources'])} direct source hashes**, and **{len(d['review_seals'])} verified review manifests**. All original 62 certificate rows remain in the data. [Provenance](PROVENANCE.md) lists accepted manifest hashes. The main figure chooses the strongest accepted isolated certificate per parameter, not an inferred optimal certificate among all possible constructions.

From the repository root:

```sh
bash research_20261010/overview_stage6/REPRODUCE.sh
```

Replay first verifies the stage6 manifest, every selected source SHA-256, all selected independent review manifests, every exact primary-gap JSON pointer, decimal downward rounding, full Hilbert counts, all {pieces} exact adjacent closed pieces, and the uniform interval minimum. It renders the three figures to a temporary directory, compares all six PNG/PDF files byte for byte with the frozen outputs, and verifies the frozen manifest again. It writes no replacement into this overview, the earlier overview, or the review folders.

The plotter pins itself to one allowed CPU, sets single-thread numerical-library variables, and caps address space at **1 GiB**. Python 3.12 and Matplotlib 3.10.8 were used. This is an integrity and extraction replay of existing independently reviewed results. It does not rerun each mathematical proof, full physical audit, or eigensolver. Those reviews retain their own reproduction scripts.

To deliberately re-extract a later snapshot, review `build_snapshot.py` and the selected seal status first. Its accepted-review selection is explicit and pinned in `ACCEPTED_REVIEW_SEALS.json`, not an automatic promotion rule. This stage was built with `python research_20261010/overview_stage6/build_snapshot.py{' --include-combined' if combined else ''}{' --include-interval-extension' if ext else ''}`. Re-extraction changes the frozen snapshot and requires renewed visual QA and a new manifest. Do not silently refresh the previous snapshot.

[Validation record](validation.json), [visual inspection](VISUAL_QA.md), [render reproducibility](render_reproducibility.json), and [SHA-256 manifest](MANIFEST_SHA256.json) describe the checks actually performed. The materialized tree has no `.git` metadata. The reported project commit is not asserted to be a locally verified checkout identity. No root README or status file, previous overview file, or remote repository was modified by this task.
'''
(HERE/'README.md').write_text(text)
prov=['# Stage6 accepted review provenance','',f"Snapshot {d['generated_utc']}.",'','Each listed manifest was checked entry by entry before inclusion. `overview_data.json` records the exact SHA-256 of every directly referenced source. This verifies integrity and association with sealed reviews, not a new independent proof audit.','','| Review directory | Manifest SHA-256 | Verified files |','|---|---|---:|']
for s in d['review_seals']:prov.append(f"| [{s['directory'].split('/')[-1]}](../{s['directory'].split('/')[-1]}/README.md) | `{s['sha256']}` | {s['verified_files']} |")
prov+=['',f"Previous sealed overview data SHA-256: `{d['previous_overview_sha256']}`.",'','All prior overview artifacts were left unchanged. The stage6 manifest excludes itself and Python bytecode caches to avoid circular checksums and machine-local cache state.']
(HERE/'PROVENANCE.md').write_text('\n'.join(prov)+'\n')
