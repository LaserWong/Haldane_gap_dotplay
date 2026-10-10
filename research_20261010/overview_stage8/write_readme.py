#!/usr/bin/env python3
import sys;sys.dont_write_bytecode=True
from common import *
from datetime import datetime
from zoneinfo import ZoneInfo
assert not (HERE/'MANIFEST_SHA256.json').exists()
x=json.loads((HERE/'overview_data.json').read_text());endpoint=format(float(F(x['ordinary_interval_endpoint'])),'.8g')
pieces=sorted([r for r in x['claims'] if r.get('certificate_route') in x['ordinary_interval_piece_routes']],key=lambda r:F(r['parameter_lower_exact']))
newpieces=[r for r in pieces if r['snapshot_stage']=='stage8']
pt='\n'.join('| '+format(float(F(r['parameter_exact'])),'.8g')+' | '+r['gap_lower_decimal_down_12']+' |' for r in sorted(x['claims'],key=lambda r:F(r['parameter_exact'])) if r['model']=='ordinary_spinhalf_bilayer' and r['parameter_kind']=='point' and r['plotted_in_main_figure'])
nt='\n'.join('| '+str(r['parameter_lower_exact'])+' | '+str(r['parameter_exact'])+' | '+r['gap_lower_decimal_down_12']+' |' for r in newpieces)
interval=('The independently sealed [new interval review](../interval_range_009_review/REVIEW.md) adds seven exact adjacent closed pieces on **[0.085,0.09]**, uniformly bounded below by **0.005788366954**. Together with all 49 earlier pieces, the whole **[0,0.09]** has the unchanged bound **0.001945771244**. Each piece uses checked denominator residual/complete-tail inputs and finite-window/short-size certification; it is not interpolation between isolated points. The fixed largest numerator is selected in exact dimension 43; smaller denominator totals are 59/125, retaining 49/97 states.\n\n| Exact lower g | Exact upper g | Uniform gap lower bound |\n|---:|---:|---:|\n'+nt if x['interval_range_009_included'] else 'The [0.085,0.09] proposal was unsealed at this cutoff and is excluded. The inherited whole [0,0.085] certificate remains accepted.')
excited=x.get('excited_witness_readme','The excited-MPS witness review was unsealed at this cutoff and is excluded from accepted results. No n14/16/20 exclusion or n24 warm-window claim is inferred here.')
now=datetime.now(ZoneInfo('America/New_York')).strftime('%Y-%m-%d %H:%M EDT (UTC−4)')
text=f'''# Certified results and dimension accounting: stage8

Updated {now} / {datetime.now(ZoneInfo('UTC')).strftime('%H:%M UTC')}. Exact extraction: {x['generated_utc']}.

This immutable snapshot extends [stage7](../overview_stage7/README.md), leaving its files unchanged and retaining **all 198 prior positive certificate rows** and their alternatives. Only pinned independently sealed PASS results enter new accepted claims. Source verification and figure extraction do not constitute a fresh spectral-proof audit.

## Strongest accepted results

- **Ordinary square bilayer, every real 0≤g≤{endpoint}, every integer L≥2: gap ≥0.001945771244.** The exact cover has {len(pieces)} adjacent closed pieces. The isolated g=0.09 certificate is stronger: **0.027330086079**; its two-vector alternative gives **0.001111944974**.
- **Alternating spin-1 chain, isolated g=0.2, every integer M≥2: gap ≥0.043446395688.** No continuous chain interval is inferred.
- **Separate AKLT projector reference, periodic L≥5: gap ≥1/10**, with one D=2 MPS ground state. It is a finite-size projector proof, not a thermal-bootstrap success.
- Uniform-Heisenberg D26 and synchronous mixed-cube results below are **recipe obstructions, not gap bounds or physical-purity upper bounds**. No all-method minimum seed is known from these results.

![Accepted gap certificates](certified_bounds.png)

[Vector PDF](certified_bounds.pdf) · [All {len(x['claims'])} exact positive certificate rows](certified_bounds.csv) · [Full provenance/data](overview_data.json) · [All prior method alternatives and history](../overview_stage7/README.md)

## Model and scope conventions

The alternating spin-1 chain has strong exchange one and weak exchange g, with M two-spin cells. The ordinary spin-1/2 square bilayer has rung exchange one and straight intralayer exchange g in both layers/directions, with no crossed exchange. The near-fully-frustrated bilayer is separate: J=0.3, straight J+ε and crossed J. The uniform spin-one Heisenberg chain below instead has unit exchange on every microscopic bond. See [Hamiltonians and normalization](../MODELS_AND_NORMALIZATION.md).

Thermal certificate families use periodic boundaries with positive-direction periodic multiedges retained at size two. Chain results cover integer M≥2; bilayer results cover integer square sides L≥2. Positive bounds certify a unique finite-volume ground state, not infinite-volume uniqueness or arbitrary rectangles. All displayed gap decimals are rounded downward to 12 places; exact fractions and JSON pointers are retained. Bounds are sufficient certificates, not estimated physical gaps, optimal thresholds or phase boundaries. Isolated points need not be monotone and imply no interpolation.

## Third moment and g=0.09

The [independent third-moment review](../third_moment_review/REVIEW.md) verifies full original-trial H³ information, base moment M5, exact enlarged G/A matrices, Gram ranks, and both all-integer scalar certificates. At g=0.09, the enlarged search gives **0.027330086079**, while a separate two-vector numerator gives **0.001111944974**. Both remain in the data.

| Rung patch | Spins | Full Hilbert dimension | Checked enlarged rank | Search used by accepted pipeline | Total used trial dimension | Retained trace/numerator terms |
|---|---:|---:|---:|---:|---:|---:|
| 4×4 | 32 | 2^32 | 16 | 11 ground | 59 = 11+48 | 49 denominator states |
| 8×4 | 64 | 2^64 | 43 | 29 ground | 125 = 29+96 | 97 denominator states |
| 8×8 | 128 | 2^128 | 43 | 43 enlarged | 43 | 1 numerator contribution |

The smaller enlarged 16/43 searches are checked but are not substituted into denominator certificates. Their complete omitted-state bounds remain inherited and unchanged. The largest new 43-dimensional exact search is distinct from the earlier ≤30 filtered span and from a one-state numerator trace. No new filtered-state residual, base M6, denominator lower bound, full many-body diagonalization, or MPS bond dimension follows from these counts.

![Dimension accounting](trial_space_counts.png)

[Vector PDF](trial_space_counts.pdf) · [Exact dimension records](trial_dimensions.csv)

| Isolated bilayer g | Strongest accepted gap |
|---:|---:|
{pt}

## Continuous interval

{interval}

The original [0,0.07] cover has 16 pieces; [0.07,0.078] adds 15; [0.078,0.08] adds two; [0.08,0.082] adds seven; [0.082,0.085] adds nine. Ground-only denominator coverage reaches g=0.082. After that, smaller complete odd bands supply 49/97 trace states. No largest-patch odd band enters this interval pipeline. The old [0,0.085] proof uses no new H³; new .09 inputs are a separate extension.

![Exact closed interval cover](ordinary_interval_pieces.png)

[Vector PDF](ordinary_interval_pieces.pdf) · [All exact pieces](ordinary_interval_pieces.csv)

## Uniform spin-one Heisenberg: fixed D26 recipe

The [sealed independent review](../uniform_seed_size_review/REVIEW.md) accepts the [diagnostics](../uniform_seed_size_diagnostics/README.md) at denominator microscopic lengths n=6,8,10,12. The numerator is exactly one Rayleigh contribution from the archived D26 MPS at length 2n. Any valid upper denominator traces, including exact traces, remain subject to these recipe obstructions.

| Denominator n | Full dimension 3^n | Numerator full dimension 3^(2n) | Strict recipe J_lower upper cap | Accepted obstruction |
|---:|---:|---:|---:|---|
| 6 | 729 | 531441 | 29/50 | All legal completed time-first delays then specified canonical conversion |
| 8 | 6561 | 43046721 | 71/100 | Same specified delayed-conversion family |
| 10 | 59049 | 3486784401 | 3/25 | First G update; four orthogonal denominator witnesses |
| 12 | 531441 | 282429536481 | 19/100 | First G update; four orthogonal denominator witnesses |

The bounds hold for all beta≥0. At n6, only delay 0 is legal; at n8, delays 0 and 1 are legal; each converted cycle fails. A two-witness construction already gives J_lower<3/10 at n10/12. These are upper envelopes on attainable **certified lower inputs**, not upper bounds on the true physical purity. D=26, one numerator contribution, four denominator witnesses, and physical dimensions count different things. No exclusion of richer numerators, other MPS, arbitrary adaptive switching, new later-base information or other inequalities is implied. Untested n2/n4 and all-method seed minima are outside scope.

![Recipe upper caps, not gap bounds](recipe_upper_caps.png)

[Vector PDF](recipe_upper_caps.pdf) · [Typed exact upper-envelope rows](recipe_upper_envelopes.csv)

### Excited-MPS witnesses

{excited}

## Small ordinary-bilayer seeds: synchronous mixed-cube obstruction

The [independent acceptance](../joint_small_seed_review/ACCEPTANCE.json) and [proof](../joint_small_seed_review/PROOF.md) cover isolated g=0.04 and 0.05 for seeds 2×2/4×2/4×4 and their coordinate-swapped mirror, for every finite beta≥0 including the unbounded cold ray. All six synchronous complete-cube routes, positive partial outputs, compatible same-base maxima, oriented-square root/product closure, and full-joint retention have no positive repeated-cycle or 499/500 small-defect onset within the defined algorithm.

The review checks 644 records, 5,778 sealed quotient upper comparisons and 520 partial-support patterns. This does not cover fresh trace injections, asynchronous other-base updates, stronger simultaneous optimizers, new inequalities or geometries, all methods, physical gaplessness or a phase boundary. It supplies no new positive gap row. The larger-seed g=.04/.05 positive certificates coexist without contradiction. See [all scoped statuses](unplotted_status.csv); none is plotted as a zero gap.

## Preserved references and alternatives

All 207 counted/joint chain candidate paths, historical fixed-order obstructions, earlier ordinary-bilayer ground/filter/combined alternatives, continuous near-frustrated interval proofs, and the AKLT projector reference remain unchanged in source and retained in the data. The historical stage7 unreviewed-.09 status is annotated as superseded, not silently used as a current rejection. [Chain paths](chain_candidate_routes.csv) · [Combined comparisons](combined_route_comparison.csv) · [Selected failures](combined_selected_failures.csv).

![Separate AKLT reference](aklt_reference_scope.png)

AKLT means H=ΣP₂ with coefficient one. Its periodic uniqueness starts at L=3, the stated gap at L=5; L=2 has four ground states. The convention B+B²/3+2I/3=2P₂ doubles the gap. The current thermal-transfer sufficiency failure is not universal transfer impossibility.

## Verification and reproduction

Run `bash REPRODUCE.sh`. It verifies all source hashes and pinned review manifests, the exact gap and upper-envelope pointers, all preserved alternatives, dimensions, closed-cover adjacency, and uniform minimum; it runs corruption rejection tests and rerenders all ten PNG/PDF files byte-for-byte in a temporary directory. It does not repeat expensive physical proof audits. The manifest covers scripts, data, documents, figures and QA. One CPU, 1 GiB address-space cap, BLAS/OpenMP one thread. No root documents, GitHub state or prior sealed files were edited.
'''
(HERE/'README.md').write_text(text)
(HERE/'PROVENANCE.md').write_text('''# Stage8 provenance boundary

All inherited stage7 sources and files are checked without mutation. Every one of its 198 certificate rows remains with identical exact gap, parameter, scope and primary source. Plot selection alone may change when a stronger point or wider union is added. All 207 chain candidate paths and comparison CSVs are preserved.

`ACCEPTED_REVIEW_SEALS.json` is an explicit allowlist of immutable manifests. New gap rows require a PASS review source contained in those manifests. Candidate producer values alone never authorize promotion. New recipe upper envelopes are separately typed and have null gap values. Prior stage7 unreviewed-.09 status is historical and superseded.

Exact values are read from primary source JSON pointers, and all decimal gap displays are rounded down. Full accepted manifests are checked, not merely their existence. No proof is inferred from a successful plot. The archived commit metadata is inherited project context, not a verified checkout identity; this extracted tree has no Git metadata.

The .09 enlarged search has exact rank 43 and one retained numerator in full dimension 2^128. Smaller checked enlarged ranks 16/43 are not substituted into denominator certificates: used ground ranks 11/29, total trial spaces 59/125, retained trace states 49/97. The fixed-D26 all-beta exclusions and synchronous mixed-cube no-go are recipe-specific and cannot become gap bounds or universal seed minima.
''')
