# Bootstrap adapter contracts

The project combines exact-rational recurrence kernels with model-specific seed constructions. The contracts below separate reusable arithmetic from the mathematical arguments needed for a new Hamiltonian family. The current [gapflow/bootstrap.py](../gapflow/bootstrap.py) implements bounded exact scalar replay in one, two, and general dimension. Its strongest status is `VERIFIED_CONDITIONAL`, because physical model assumptions and all-size coverage require separate evidence.

Legacy paths below refer to the restored research checkpoint and are not bundled in this workflow package. Paths beginning with `gapflow/` refer to this package. Confirm the checkpoint files and their dependency hashes before invoking legacy code.

## Existing code and intended reuse

| Component | Existing entry point | Reusable output | Required gate |
|---|---|---|---|
| One-dimensional scalar replay | `seed_size/code/certified_core.py`, `replay(S,T,n,beta,...)` | Rational trajectory and conditional gap lower bound | Certified staircase inputs and the applicable transfer and interpolation theorem |
| Two-dimensional scalar replay | `two_d_theory/three_purity_certificate.py`, `replay(A,B,C,n,m,beta,...)` | Rational three-coordinate trajectory and conditional square/common-scale-rectangle bound | Exact transfers in both axes, certified inputs, and coverage |
| Conservative analytic 2D seeds | Same file, `analytic_seed(model,g,beta,n,m)` | Physical trace-based seed bounds for two named models | Unit rung bilayer or D=1 spin-one large-D model with nonnegative coupling |
| Sparse-support bilayer seed | `low_energy/bilayer_seed.py`, `seed3(r22,r42,r44,beta)` | Three lower purity bounds from existing ground and tail certificates | Model-specific `dimer_subspace` and `local_relative_bound` prerequisites |
| Stored optimized bilayer tail replay | `seed_size/code/verify_stored_tail_certificates.py`, `verify(row)` | Exact recomputation without rerunning the float optimizer | Complete stored thermal-tail nodes and matching axis-order metadata |
| One-dimensional counted-bin analysis | `seed_size/code/spectral_search.py` and `necessary_windows.py` | Certified trace envelopes and necessary temperature windows | Exact spectrum/bin provenance and multiplicities |
| Model-specific independent checks | `audit/independent/verify_bilayer.py`, `verify_large_d.py`, `verify_baseline.py`, `verify_streamed_heat.py` | Check-specific evidence and logs | Read each script's scope and file dependencies before running |
| General d | `gapflow/bootstrap.py`, based on `two_d_theory/GENERAL_DIMENSION.md` | Exact conditional scalar trajectory | A verified transfer and seed adapter for every axis remains external |

Some legacy scripts write beside their source or overwrite a stored result. Do not run their command-line entry points against immutable evidence. Use a fresh working copy with explicit output paths or an adapter that reads inputs and writes only into its new run directory. Importable functions may be reused after checking import-time side effects.

## Exact data contract

A proposed adapter consumes `model`, `geometry`, `parameter_domain`, `seed_nodes`, `transfer_evidence`, `arithmetic`, `budget`, and `claim_scope`. These describe the end-to-end scientific interface. The implemented scalar sub-interface below is deliberately narrower.

Each node needs its side-length vector, rational beta, energy shift, lower and upper trace bounds, and proof-artifact hashes. Each edge needs its axis label and explicit base node. A ratio lower bound uses the numerator's lower bound and the denominator's upper bound squared. Bounds may be clipped above at one only after the applicable purity theorem is established. A raw lower bound greater than one should first be investigated as a likely normalization or certificate error.

Exact inputs are rational strings. Floating display values never enter acceptance. The adapter must reject absent tail coverage, unresolved model identities, changed periodic multiplicities, or unsupported geometry mappings before assigning a physical certificate status.

The adapter emits the stage artifacts in [AGENTS_WORKFLOW.md](AGENTS_WORKFLOW.md). It records both the native legacy result and its translated workflow status. In particular, `accepted=True` from a scalar function is not translated directly into `CERTIFIED`.

## One spatial dimension

At even n≥2, use the ordered staircase

\[
S=Z(2n,\beta)/Z(n,\beta)^2,\qquad
T=Z(2n,2\beta)/Z(2n,\beta)^2.
\]

The thermal input is at length 2n, not n. Define

\[
G(z)=1-\frac{(1-z)^2}{2z^2}.
\]

The actual sequential update is

\[
S'=G(S^2T),\qquad T'=G(T^2S').
\]

One full cycle sends `(n,beta)` to `(2n,2beta)`. The canceled first joint ratio is `Z(2n,2beta)/Z(n,beta)^4`. A lower bound computed directly for this ratio may be sharper than the product of separate edge lower bounds.

The existing `certified_core.replay` defaults to `max_rounds=40`, `clip=False`, and `small=1/100`. It rounds downward on a 128-bit dyadic grid and uses the contraction constant 5, giving the conditional bound

\[
\Delta\ge\log[1/(5u_*)]/\beta_*.
\]

`seed_size/proofs/DERIVATIONS.md`, Section 2, proves a larger entry region `u≤1/40`. Selecting that region is allowed only when that specific derivation and all associated interpolation inequalities are included in the proof record. Do not choose an arbitrary larger `small` argument merely because the function accepts it.

The legacy message `Invariant scalar failure region S^2 T <= 1/2` is a statement about the supplied scalar tuple. If S and T are lower bounds, their product below the threshold does not prove the exact physical purities are excluded. Translate this outcome to `INCONCLUSIVE` unless independently certified upper bounds establish the relevant method-level exclusion. Even a rigorous method-level exclusion does not establish gaplessness.

The `u=0` branch returns no numerical gap. Treat it separately. An exact rank-one finite-temperature Gibbs state is incompatible with an ordinary nontrivial finite-dimensional finite Hamiltonian, so this branch should trigger a model or input review rather than an invented infinite gap.

## Two spatial dimensions

At even n,m≥2, the canonical staircase is

\[
A=\frac{Z(2n,m;\beta)}{Z(n,m;\beta)^2},\quad
B=\frac{Z(2n,2m;\beta)}{Z(2n,m;\beta)^2},\quad
C=\frac{Z(2n,2m;2\beta)}{Z(2n,2m;\beta)^2}.
\]

The update is

\[
A'=G(A^4B^2C),\quad
B'=G(B^4C^2A'),\quad
C'=G(C^4(A')^2B').
\]

The queue rotates after each individual update. One complete cycle doubles n, m, and beta. `three_purity_certificate.advance` implements this in defects with outward upward rounding. Its `replay` defaults to 32 rounds and 18 decimal digits of rational outward rounding. Acceptance requires the common defect `u≤1/500`. The dedicated two-dimensional theorem uses

\[
u_j\le\frac{(32u_*)^{2^j}}{32},\qquad
\Delta\ge\frac{\log[1/(32u_*)]}{\beta_*}.
\]

The interpolation proof first controls the other-axis spatial purity by `1−5u`, then the physical purity by `1−20u`. Both directions are essential. Odd lengths require the signed-transfer argument, not an assumption that the transfer itself is positive.

For n=m, the accepted scale covers every square side at least n. For unequal n,m, it covers only rectangles in the common-scale boxes stated by the theorem. If recurrence startup increases n and m, the missing earlier finite windows must be closed separately before claiming the original requested lower size cutoff.

Changing coordinate order requires new staircase nodes or certified adjacent exchanges. Do not permute three existing numerical values. `THEORY.md`, Section 10, gives the rational conservative exchange `(a,b) -> (ab,a^2 b)` and explains conversion to canonical order.

### Immediately executable analytic-seed example

With the checkpoint path supplied as `PROJECT`, Python's standard library suffices for the scalar/analytic arithmetic below. Use a fresh `RUN_DIR` that does not contain historical outputs.

```sh
PYTHONDONTWRITEBYTECODE=1 python "$PROJECT/two_d_theory/three_purity_certificate.py" \
  --model bilayer_s_half --g 1/4000 --beta 12 \
  --output "$RUN_DIR/bilayer_analytic_seed.json"
PYTHONDONTWRITEBYTECODE=1 python "$PROJECT/two_d_theory/three_purity_certificate.py" \
  --model square_spin_one_large_D --g 1/6000 --beta 12 \
  --output "$RUN_DIR/large_D_analytic_seed.json"
```

These commands replay seed and scalar arithmetic. They do not run an independent reviewer or automatically verify the full model and smallest-size proof. The archived baseline all-size bounds are 0.151171228506 for the bilayer and 0.152901911246 for the large-D model. The analytic record supplies the L=2,3 Weyl bridge, at least 0.991 for the stated coupling ranges. Preserve those recorded bounds unchanged. A fresh run should report its actual output and explicit bridge verification separately.

The stronger historical ordinary-bilayer point bounds at g=0.09 and g=0.10 are 0.027330086079 and 0.038976038275, respectively. Their low-band and full-residual inputs are different from the conservative analytic seeds above. Do not reproduce these claims by changing only the `--g` argument or by substituting a fully frustrated bilayer spectrum.

## General spatial dimension

Let k=d+1 and let the ordered coordinates be the d spatial lengths followed by inverse temperature. For an ordered list of current staircase lower bounds `q[0:k]`, the next edge uses

\[
z=\prod_{j=0}^{k-1}q_j^{2^{k-1-j}}.
\]

Compute a rigorous lower bound for `G(z)`, discard a nonpositive bound as an inconclusive attempt, and rotate the queue by appending the updated first edge. Repeat k times for a full cycle. All spatial lengths and beta then double together. The product is also the corner ratio `Z(all coordinates doubled)/Z(base)^(2^k)`. Axis labels and basepoints remain part of the data throughout.

The conservative general theorem defines

\[
F_d=4\,8^{d-1},\qquad
K_d=\max\{(2^{d+1}-1)^2,2F_d\}.
\]

For

\[
0<u_*\le\min\{1/(4K_d),1/[100\,8^{d-1}]\},
\]

it gives the conditional bound `log(1/(K_d u_*))/beta_*` on each common-scale integer box. Equal seed sides cover all sufficiently large hypercubes. A separate bridge is still needed for smaller sizes. For d=2, this general route has K=64 and must not replace the sharper dedicated K=32 route in existing certificates. For d=1, it is likewise more conservative than the dedicated K=5 adapter.

The scalar adapter has exact tests reducing its sequential queue to the 1D and 2D formulas, checking coordinate labels and basepoints, checking the general-dimension constants and thresholds, and replaying the two archived analytic baseline bounds. These tests establish implementation checks, not an independent proof of the general-dimension theorem or physical coverage. The general theorem does not supply heat-trace bounds or exact transfer structures for arbitrary user input. Without those model-specific components, return `UNSUPPORTED` or `SCALAR_ACCEPTED_CONDITIONAL` as appropriate.

## Seed and tail adapter requirements

A trace upper bound can combine retained eigenvalue lower endpoints with omitted bins,

\[
Z(\beta)\le\sum_j e^{-\beta\ell_j}+\sum_q m_q e^{-\beta b_q}.
\]

The multiplicities and indices are proof inputs, not estimates. Sector decomposition must restore all physical multiplicities. A small Krylov or symmetry-reduced search dimension is not the dimension of the physical Hilbert space and is not a count of omitted eigenstates.

The bilayer `seed3` function expects certificate records accepted by `local_relative_bound.trace`. Its geometry is specifically 2×2, 4×2, and 4×4 rungs. The adapter cannot replace them with arbitrary geometries by relabeling files. More advanced archived 4×4, 8×4, and 8×8 inputs need their own exact moment and full-residual dependency chain. A saved result without its generator and checker is historical evidence with a replay blocker.

The stored-tail verifier checks rational parameter inequalities, reconstructed thermal-tail bounds, correlated first-step values, and canonical replay fields. It does not automatically reconstruct every earlier trial vector or prove the physical transfer theorem. List its exact scope in the result.

## Adapter acceptance tests

A production wrapper needs tests for the following failure modes before it labels a run certified.

- Odd or length-one seed, nonpositive beta, invalid purity interval, wrong dimensionality
- Length-two edge deduplication, incorrect energy shifts, mismatched model parameters
- Thermal purity attached to the initial rather than staircase-final geometry
- Parallel instead of sequential updates, and naive permutation of axis values
- Unaccounted tail states, sector multiplicity errors, and incomplete residuals
- Floating-point display values accidentally reused as proof inputs
- Passing recurrence but missing an early finite window or smallest-size bridge
- Parameter-grid samples incorrectly labeled as interval coverage
- Exhausted rounds mislabeled as exclusion or gaplessness
- Reused producer flags mislabeled as independent verification
- Missing dependencies, changed hashes, unavailable software, user pause, or exhausted resources

The wrapper should stop at the first unmet certification prerequisite while preserving completed useful stages. It may continue an authorized exploratory branch, but that branch must retain its weaker evidence label.

## Implemented scalar sub-interface

Import `bootstrap_certificate` and `canonical_edges` from `gapflow.bootstrap`. The function `bootstrap_certificate(data)` accepts the following fields.

- `dimension` is a positive integer, capped at 8 by the bounded implementation.
- `lengths` contains one even integer at least two per spatial axis.
- `beta` is a positive rational string or integer.
- `edges` has d+1 entries in canonical order `x1`, ..., `xd`, `beta`. Each entry contains `axis`, `base_lengths`, `base_beta`, and `lower`.
- `model_to_seed_proof` contains `verified: true` and a nonempty `evidence` list. This is an externally reviewed proof declaration, not a trusted proof object. Missing declarations are rejected as `UNSUPPORTED`. Supplied declarations are retained with `proof_declaration_trusted: false`.
- `max_rounds` defaults to 32 and cannot exceed 128.
- `digits` defaults to 18 and lies between 12 and 100.
- `mode` is `dedicated` for d=1 or d=2 by default, and `general` otherwise.

`canonical_edges(lengths, beta, lower)` creates labels for bounds whose proof is already available. It does not certify those bounds. A wrongly labeled or permuted staircase is rejected before replay. The adapter keeps input and output basepoint labels for each full cycle.

Acceptance emits `VERIFIED_CONDITIONAL`, an exact rational gap lower bound, an explicitly conditional common-scale scope, and the required external checks. `uniform_family_claim` and `physical_proof_verified` remain false. Other implemented outcomes are `INVALID_INPUT`, `UNSUPPORTED`, `INCONCLUSIVE`, and `RESOURCE_LIMIT`. These uppercase scalar statuses are distinct from the orchestration layer's status vocabulary.

Run the focused tests from the workflow package root.

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p test_bootstrap.py -v
```

On 2026-10-14, all 11 focused tests passed. The archived analytic seed inputs reproduce both displayed baseline bounds exactly at the stated 12-decimal downward rounding. This run did not independently reverify the physical transfer proofs, omitted-spectrum derivations, or smallest-size bridges.
