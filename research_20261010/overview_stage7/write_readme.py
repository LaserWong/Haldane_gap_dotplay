#!/usr/bin/env python3
import sys; sys.dont_write_bytecode=True
from common import *
assert not (HERE/'MANIFEST_SHA256.json').exists(), 'Frozen snapshot: create a new stage instead'
x=json.loads((HERE/'overview_data.json').read_text())
def points(model):
 return '\n'.join('| '+format(float(F(r['parameter_exact'])),'.8g')+' | '+r['gap_lower_decimal_down_12']+' |' for r in sorted(x['claims'],key=lambda a:F(a['parameter_exact'])) if r['model']==model and r['parameter_kind']=='point' and r['plotted_in_main_figure'])
pieces=sorted([r for r in x['claims'] if r.get('certificate_route') in x['ordinary_interval_piece_routes']],key=lambda r:F(r['parameter_lower_exact']))
interval_table='\n'.join('| ['+format(float(F(r['parameter_lower_exact'])),'.8g')+', '+format(float(F(r['parameter_exact'])),'.8g')+'] | '+r['gap_lower_decimal_down_12']+' | '+('complete smaller odd bands' if F(r['parameter_lower_exact'])>=F('41/500') else 'ground-only')+' |' for r in pieces)
readme=f'''# Certified results and dimension accounting: stage7

Updated 2026-10-10 17:12 EDT (America/New_York, UTC−4) / 21:12 UTC. Extraction timestamp: **{x['generated_utc']}**.

This new immutable snapshot extends [stage6](../overview_stage6/README.md), preserving every prior file and accepted alternative. It extracts independently sealed results and redraws static figures. It does not perform new spectral research or re-audit each mathematical proof.

## Current certified results

- **Ordinary square bilayer: every real 0≤g≤0.085, every integer L≥2, gap ≥0.001945771244.** The exact cover has 49 adjacent closed pieces. The isolated g=0.085 certificate is stronger, **0.027887084487**, and remains a separate claim.
- **Alternating spin-1 chain: isolated g=0.2, every integer M≥2, gap ≥0.043446395688.** The new counted-band route also certifies g=0.18, 0.185, 0.19 and 0.195. No continuous chain interval is inferred.
- **Separate AKLT projector reference: periodic L≥5, gap ≥1/10**, with one D=2 MPS ground state. This uses a finite-size projector criterion; it is not a thermal-bootstrap success.
- The new third-moment 43-dimensional g=0.09 proposal is unreviewed and excluded from all certified figures. This snapshot is frozen without waiting for that work.

![Thermal-bootstrap certificate families](certified_bounds.png)

[Vector PDF](certified_bounds.pdf) · [All exact thermal certificate rows](certified_bounds.csv) · [Strongest isolated points](latest_point_bounds.csv) · [Full exact data and provenance](overview_data.json)

## Models, normalization and size scope

The alternating spin-1 chain has unit strong-bond exchange and weak exchange g; M counts two-spin cells. The ordinary spin-1/2 square bilayer has unit rung exchange and straight intralayer exchange g in both directions and layers, with no crossed bonds. The near-fully-frustrated bilayer is a different model: fixed J=0.3, straight exchange J+ε and crossed exchange J.

These three thermal-bootstrap families use periodic boundary conditions and retain positive-direction bond multiplicities at side/cell count two. Positive chain bounds cover every integer M≥2; positive square-bilayer bounds cover every integer L≥2. Each certifies a unique finite-volume ground state. No arbitrary-rectangle or infinite-volume-uniqueness conclusion is inferred, apart from the explicitly scoped analytic fully-frustrated reference below.

AKLT instead means the spin-1 projector Hamiltonian H=ΣP₂ with coefficient one. Its periodic uniqueness starts at L=3, and its stated gap starts at L=5. Periodic L=2 has four ground states and is excluded. The convention B+B²/3+2I/3=2P₂ would double the numerical gap.

Every displayed gap decimal is rounded down to 12 places. Exact fractions, primary JSON pointers, source hashes, temperatures and asymptotic onsets are retained. A dot certifies only its parameter; a bar certifies an entire interval. Bounds are sufficient certificates, not estimated physical gaps, optimal thresholds or phase boundaries. Different constructions can give nonmonotone bounds.

## Alternating spin-1 chain

| Isolated g | Strongest accepted gap lower bound |
|---:|---:|
{points('alternating_spin1_chain')}

The [joint-ratio general lemma](../joint_ratio_review/GENERAL_LEMMA.md) is independently sealed separately from its physical applications. The [chain application](../joint_ratio_review/CHAIN_REVIEW.md) gives g=0.175/0.18/0.181/0.182 with gaps 0.026579108896/0.013222512347/0.009728769181/0.005940278341. All four remain in the exact data even where superseded.

The [counted low-band review](../chain_low_band_review/README.md) gives the strongest new five points:

| g | Gap | Initial β | Asymptotic onset M |
|---:|---:|---:|---:|
| 0.18 | 0.112949677804 | 11.2 | 64 |
| 0.185 | 0.096048414952 | 11.45 | 64 |
| 0.19 | 0.078956697835 | 11.75 | 64 |
| 0.195 | 0.061526095375 | 12.2 | 128 |
| 0.2 | 0.043446395688 | 12.75 | 128 |

Each full-size bound is limited by the finite window [8,16]. The M=4 denominator uses a 13-dimensional comparison P and 6,548-dimensional complement Q in physical dimension 6,561. Its complete trace count comprises one independently identified ground term, triplet-reference multiplicities 3/6/3 and 6,548 remaining terms. It does not assume that thirteen physical eigenvalues lie below the complement cutoff; at g=0.2 that assumption would fail.

The 13 bare comparison columns, their shifted-H union support 172, unshifted-H/trial-plus-action union 173, and residual union 160 are different counts. The existing ground search has 1,099 configurations and full-H action support 1,107. The largest M=8 numerator is one state selected from an independently checked **two-vector first-moment combination on 43,294 configurations**, in full dimension 9⁸=43,046,721. This current two-vector span is distinct from the earlier 43,294-coordinate search and is not an MPS bond dimension.

All **207 newly reviewed candidate paths** are retained in [chain_candidate_routes.csv](chain_candidate_routes.csv), with exact all-size bounds and derivations. Old order-specific obstructions and failed finite grids remain in [unplotted_status.csv](unplotted_status.csv). In particular, the old g=0.2 grid failure is superseded by the counted-band success; it was never an all-temperature or physical-gaplessness result.

## Ordinary spin-1/2 square bilayer

| Isolated g | Strongest accepted gap lower bound |
|---:|---:|
{points('ordinary_spinhalf_bilayer')}

The [polynomial frontier review](../bilayer_polynomial_frontier_review/README.md) certifies the isolated g=0.085 result using β=177/20, eight further txy cycles and onset L=2048, with every preceding finite window and L=2,…,7 checked. Its accepted .09 physical inputs alone establish no .09 all-size gap.

All previous 30 full-band and 11 largest-ground-only combined alternatives remain available in the exact data and unchanged [combined_route_comparison.csv](combined_route_comparison.csv). The original ground-pencil-only, filter-only and combined routes use individually selected temperatures; their differences are not controlled single-ingredient comparisons. [Selected failures](combined_selected_failures.csv) stay scoped to their proposals. The [stage6 explanation](../overview_stage6/README.md) retains the older route details.

### Entire interval through g=0.085

For **every real 0≤g≤0.085 and every integer L≥2**, Δ≥**0.001945771244**, with a unique finite-volume ground state.

The accepted chain of continuous proofs is:

| Contribution | Closed pieces | Extension-wide bound |
|---|---:|---:|
| Original [0,0.07] | 16 | 0.001945771244 |
| Filtered [0.07,0.078] | 15 | 0.002006633957 |
| Joint-aware [0.078,0.08] | 2 | 0.008215303694 |
| Ground-only [0.08,0.082] | 7 | 0.005978179134 |
| Smaller complete odd bands [0.082,0.085] | 9 | 0.003365750386 |

The [joint interval review](../interval_joint_review/REVIEW.md) completes the entire [0,0.08]. The [new range review](../interval_range_0085_review/REVIEW.md) adds sixteen pieces on [0.08,0.085], whose minimum is 0.003365750386. The union of all 49 pieces retains the earlier minimum 0.001945771244. Shared endpoints are checked exactly; no interpolation between isolated g points is used.

Ground-only denominator coverage reaches **g=0.082**. On the final nine pieces, the 4×4 and 8×4 denominator traces retain **49 and 97 states**, and their ground-search-plus-odd spaces have dimensions **59 and 125**. The 8×8 numerator throughout uses **one filtered contribution**, in dimension **≤30**, with full physical Hilbert dimension **2¹²⁸**. No largest-patch odd input enters this interval proof. Existing complete G/K/J moments through H² are used; no H³/H⁴ is claimed.

![Every exact closed piece](ordinary_interval_pieces.png)

[Vector PDF](ordinary_interval_pieces.pdf) · [Exact piece CSV](ordinary_interval_pieces.csv)

| Closed g interval | Uniform gap | Denominator regime |
|---|---:|---|
{interval_table}

Green segments are ground-only denominator certificates; orange segments use complete smaller odd bands. Each segment has its own sufficient bound. The purple bar is the uniform minimum on the entire union. The original [0,0.07] numerator was G/K-only; the filtered later route consumes existing full second moments and has a different input contract.

## Dimensions count different objects

![Full Hilbert, denominator and numerator counts](trial_space_counts.png)

[Vector PDF](trial_space_counts.pdf) · [{len(x['dimensions'])} exact dimension records](trial_dimensions.csv)

| Patch | Physical spins | Full Hilbert dimension | Ground search | Final total trial space | Final trace states / contributions |
|---|---:|---:|---:|---:|---:|
| 4×4 rungs | 32 | 2³² | 11 | 11+48=59 | 49 denominator states |
| 8×4 rungs | 64 | 2⁶⁴ | 29 | 29+96=125 | 97 denominator states |
| 8×8 rungs | 128 | 2¹²⁸ | 29 | ≤30 | 1 numerator contribution |

These final-regime rows apply to [0.082,0.085]. Through 0.082, the working spaces are 11/29/≤30 with one denominator ground level each. The largest numerator bound ≤30 is **not the maximum search/trial dimension across the full .085 pipeline**. The 59/125 spaces combine all ground search directions with the smaller odd spaces; the actual fixed ground/odd witnesses span 49/97 directions.

The largest filtered trial adds at most one implicit residual direction to the 29-dimensional search. The local plane formed by a chosen trial and residual has dimension at most two; neither that plane nor one final numerator vector turns the original search into a two- or one-dimensional search. Original ground support has q≤4 and filtered support q≤6.

A separate complete-band route retains 49/97/193 states. The largest 193-direction numerator is unnecessary for the rank-one continuous proof. Its old triplet generator support 373 and full H-action support 67,755 are per-column support counts, not search or band dimensions. The earlier first-moment-only reduction moves the largest required upper-trace certification to 8×4 while keeping an 8×8 physical numerator. These distinctions remain in the inherited records. Missing counts remain null, never zero.

## Separate nonperturbative AKLT reference and scoped exclusions

![Separately proved AKLT projector reference](aklt_reference_scope.png)

[Vector PDF](aklt_reference_scope.pdf) · [Exact reference record](reference_certificates.csv) · [Independent review](../nonperturbative_mps_review/REVIEW.md)

For the normalized projector Hamiltonian H=ΣP₂, an exact four-site **81×81** local proof matrix (largest symmetry block 21) and periodic bond counting prove Δ≥1/10 for every L≥5. The entangled Pauli **MPS bond dimension is D=2**, its retained span contains **one state**, and the physical space has dimension **3ᴸ**. Exactly **3ᴸ−1** omitted states are bounded above the gap. These dimensions describe different objects.

This is a separately proved **finite-size projector criterion** reference. The current same-real-factor thermal-transfer sufficient construction fails: its Cartesian realignment has the exact witness −1/3. That scoped obstruction does not invalidate the projector certificate and does not prove universal thermal-transfer impossibility. The MPS norm transfer does not equal a complete thermal transfer. No quantitative gap transfer to the bilinear Heisenberg model is asserted.

The same review independently checks fixed **D26** uniform-spin-1 seed exclusions at denominator n=6/8 and numerator L=12/16 for the specified one-Rayleigh and G-update recipes, including one-off canonical conversion after completed positive time-first cycles. These are recipe-specific all-temperature exclusions, not an exclusion of all MPS states, richer numerators, larger seeds or arbitrary adaptive schemes. The old uniform-spin-1 bound and spin-2 D124 certificates remain inherited background, not newly re-certified successes here.

## Near fully frustrated bilayer and preserved alternatives

No new FF result is introduced. Its separate Hamiltonian and evidence labels remain unchanged.

| Isolated ε | Accepted gap lower bound |
|---:|---:|
{points('fully_frustrated_bilayer')}

The reviewed intervals [0,0.004], [0,0.0045], [0,0.00475], [0,0.0085], [0,0.00855] retain bounds 0.024046763298, 0.014475263367, 0.008090283176, 0.001703099464, 0.000768515509. The first three use one product vector; the widest two use piecewise fixed vectors. The ε=0.008/0.0085 point markers retain their supplemental scalar-bridge status. At ε=0 the analytic reference gives gap≥2/5 for periodic rectangles nx,ny≥2 at J=0.3; the stronger square gap 1 for L≥3 has a different scope and is not substituted.

The unchanged [tail/order comparison](tail_order_comparison.csv) and [fixed-order gains](fixed_order_tail_gains.csv) preserve previous alternatives. Prior spin-2, small-seed and fixed-subspace exclusions are retained with their original limitations in the data and stage6 documentation.

## Provenance and reproduction

This stage contains **{len(x['claims'])} thermal certificate rows**, **{len(x['dimensions'])} dimension records**, **207 additional exact chain path alternatives**, **1 separate AKLT reference**, **{len(x['sources'])} direct source hashes** and **{len(x['review_seals'])} selected manifests**. All 164 stage6 certificate rows and 80 stage6 dimension records are retained. The 17 manifest checks cover 1,486 entries, including overlaps among inherited seals. Source identity is pinned in [ACCEPTED_REVIEW_SEALS.json](ACCEPTED_REVIEW_SEALS.json) and [PROVENANCE.md](PROVENANCE.md).

From the project root:

```sh
bash research_20261010/overview_stage7/REPRODUCE.sh
```

Replay verifies the frozen snapshot, source hashes, selected seals, all primary exact fractions, downward rounding, every interval endpoint, the uniform minimum, all 207 new path alternatives, preserved stage6 artifacts and dimension distinctions. It tests deliberately corrupted inputs, redraws all four figures into a temporary directory and compares **all eight PNG/PDF files byte for byte**, then rechecks the manifest. It leaves stage7, stage6 and all source reviews unchanged. This replay checks integrity and extraction; each mathematical review has its own separate reproduction script, some of which change timing-bearing files and should be run in a disposable copy.

Processes are pinned to one CPU and capped at **1 GiB address space**, with numerical libraries single-threaded. Python 3.12 / Matplotlib 3.10.8 were used. [Validation](validation.json), [corruption guards](rejection_guards.json), [visual QA](VISUAL_QA.md) and [render reproducibility](render_reproducibility.json) record the checks actually performed.

The project commit reported by the parent is **00593ba445c26b1da625c9afe618e85a2550f70e**. The extracted tree has no Git metadata, so this is context rather than a locally verified checkout identity. No root README/status file or GitHub resource was written. Once frozen, writer entry points refuse in-place regeneration; later findings require a new overview stage.
'''
(HERE/'README.md').write_text(readme)
provenance='# Stage7 provenance and source contract\n\n'
provenance+='This is a newly created static extraction. All earlier files remain unchanged. The inherited stage6 manifest and every selected source manifest were verified before extraction and again during replay. Manifest entry totals include overlaps.\n\n'
provenance+='| Selected manifest | SHA-256 | Entries checked |\n|---|---|---:|\n'
for s in x['review_seals']:provenance+=f"| [{s['manifest']}](../../{s['manifest'].removeprefix('research_20261010/')}) | {s['sha256']} | {s['verified_files']} |\n"
# Use local paths from this directory rather than the project-root-oriented display path.
provenance=provenance.replace('](../../','](../')
provenance+='\n## Extraction boundaries\n\n- Thermal claims preserve primary JSON numeric pointers and exact fractions. The AKLT theorem is a separately typed reference, whose exact rational gap and size range are read from the accepted claim conditions and supported by the full independent proof.\n- The 54 joint-chain paths use min(path M≥8 bound, accepted M=2…7 minimum). The 153 counted-chain paths read their accepted all-M≥2 bound directly. Every derivation is replayed.\n- New continuous claims consist of two joint-aware pieces and sixteen range-extension pieces, joining all 31 stage6 pieces. Duplicate whole-union and regime summaries are not counted as additional pieces.\n- Only the newest [0,.085] ordinary-bilayer union is drawn in the main figure; earlier accepted union rows remain in the data. All isolated points select the largest exact accepted value at that parameter.\n- The final [.082,.085] denominator trial dimensions 59/125 are distinct from retained trace counts 49/97 and the largest filtered numerator bound ≤30.\n- The g=.09 third-moment 43D proposal is intentionally excluded. Existing physical .09 input acceptance and failed grids do not authorize a .09 gap marker.\n- The reported project main commit is 00593ba445c26b1da625c9afe618e85a2550f70e; no local Git identity is asserted.\n\nAll CSVs use exact fraction strings and retain provenance fields. Source paths are project-root-relative. The four historical comparison CSVs are byte-identical to stage6.\n'
(HERE/'PROVENANCE.md').write_text(provenance)
print('Wrote README and provenance')
