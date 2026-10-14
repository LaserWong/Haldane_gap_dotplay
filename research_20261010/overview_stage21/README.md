# Stage 21 research overview

Stage21 strengthens the near-uniform alternating-chain intervals using independently accepted staggered-second-moment data. It adds eight closed-interval certificates while preserving every Stage20 scientific field and CSV. The engineering tests and producer-only failures below retain their limited historical scope. This reader edition reports no new physical or thermal campaign, and the original sealed snapshot remains unchanged.

## Stronger accepted near-uniform intervals

For the periodic alternating spin-one Hamiltonian

    H_M(g) = Σ_j [S_(2j−1)·S_(2j) + g S_(2j)·S_(2j+1)],

with the designated first bond coefficient one, each entire closed interval below has a unique finite-volume ground state and the stated physical-unit gap, for every integer cell count M ≥ 2. Physical length is L = 2M and the full Hilbert dimension is 3^(2M).

| Closed coupling interval | Certified gap lower bound | Exact η radius |
| --- | --- | --- |
| [9998709/10001291, 10001291/9998709] | .020 | 1291/10000000 |
| [1249773/1250227, 1250227/1249773] | .015 | 227/1250000 |
| [9997841/10002159, 10002159/9997841] | .010 | 2159/10000000 |
| [156213/156287, 156287/156213] | .005 | 37/156250 |

Here η=(1−g)/(1+g), and a radius r corresponds exactly to [(1−r)/(1+r),(1+r)/(1−r)]. The [final independent proof](../uniform_alternating_second_moment_finite_bridge_review/PROOF.md), [exact dataset](stage21_finite_intervals.csv), and [frontier figure](stage21_second_moment_frontier.png) distinguish these sufficient neighborhoods from optimal widths, actual gaps or phase boundaries. Odd cell counts are covered. Odd physical rings are not asserted by this alternating-cell result.

The proof checks 39 complete integer-cell windows, 56 finite bridges (14 physical lengths for each row), four infinite-tail closures, and all 400-place directed scalar updates using independent 1600-bit enclosures. Cell 16 contains 32 physical sites. Its physical-64 MPS anchor has bond dimension 26 and a one-dimensional retained trial span. These three dimensions are not interchangeable.

Normalized β0=49/4 corresponds to physical inverse temperature β/c with c=(1+g)/2. Every subsequent doubled temperature and finite bridge retains that scaling. The linear physical shift is c·700741/500000 per site. The anchor energy numerator is already total periodic energy, so no extra physical-length factor is introduced.

The missing cells 2…15 are covered by separately inherited finite purities at physical lengths 4,6,…,30. The finite-gap perturbation is [δ_L−3Lr]/(1+r), checked both through exact rational δ_L and directly from its Gibbs ground-weight inequality. Every finite bridge has a strict margin beyond the target. Physical 24 is the weakest finite bridge but still supplies approximately .10369/.09991/.09743/.09593, respectively. Its accepted input is the parity-resolved certificate with physical 48 MPS anchor. There is no own-length MPS24 contraction.

The four terminal cell bases are 8192,4096,8192,8192, with 10,9,10,10 explicit windows. The later purity defects remain nonzero directed rational bounds. Rounding them to one is rejected. The 32 producer search candidates and 15 rejected candidates remain historical producer data. The independent review replays the four final certificates, not the candidate search. No maximal-radius claim follows.

## Independently accepted physical B² input

The [observable review](../uniform_alternating_b2_fixture_review/PROOF.md) reconstructs all D26 local transfer insertions, checks complete physical L4/L6 fixtures and two D2 families, and independently contracts all eleven exact charge blocks at physical lengths 32 and 64. For the actual uniform Gibbs state at β=49/4 it proves

    κ32 = Tr[ρ32 B32²/(48²)] ≤ 17/125 = .136,
    κ64 = Tr[ρ64 B64²/(96²)] ≤ 157/1000 = .157.

These are Gibbs observable bounds obtained from trial data plus a finite-volume fidelity/effect argument. They are not an identification of the trial MPS with the ground or Gibbs state. The physical Hilbert dimensions are 3^32 and 3^64, while the full norm-transfer dimension is 676 and MPS bond dimension is 26. All eleven virtual charge sectors are retained. There is no physical spectral truncation or finite thermal-transfer rank assumption. See [observable scope data](stage21_observables.csv).

Translation symmetry, Golden–Thompson, and the scalar second-moment cosh bound give the finite trace factors F_L=1+κ_L[cosh(β·3Lr/2)−1]. The inherited uniform seed endpoints transport as S0/F32² and T0/F64². Existing positive-cell trace-class interpolation then controls every integer cell in each doubled window. No H² production at 32/64 is claimed.

The fixture originally described as an adjacent omission actually doubled the subtraction. The independent review tests a true omission separately. An initial length-32 producer wrapper changed 162 to 130, was stopped and preserved, and an explicitly authorized corrected retry passed. The old files and their audit trail were not silently rewritten.

## Earlier second-moment intervals preserved

The [first scalar review](../uniform_alternating_second_moment_robustness_review/PROOF.md) independently accepted the four earlier all-size closed intervals below.

| Closed coupling interval | Certified gap lower bound |
| --- | --- |
| [112519/112531, 112531/112519] | .020 |
| [225013/225062, 225062/225013] | .015 |
| [112494/112531, 112531/112494] | .010 |
| [224963/225062, 225062/224963] | .005 |

The [earlier exact dataset](stage21_first_intervals.csv) retains all 22 bootstrap windows and all previous scope. This route uses the coarser uniform .0248 theorem for its finite Weyl bridge. Its chosen radii make the bridge margin exactly zero at the target, which is valid for a closed gap≥D claim with D>0. Its infinite-bootstrap margins remain strictly positive. These records are not replaced by the later, stronger finite-purity bridge.

## Preserved baseline results

The [frozen Stage20 overview](../overview_stage20/README.md) remains byte-for-byte unchanged. The preserved results include the following.

- Uniform periodic unit-exchange spin-one chain: unique finite-volume ground state and gap≥.0248 for every integer physical L≥2. The strongest tail starts at 34. Smallest separately successful genuine initialization remains 30 at .0179. Full-size coverage from 2 does not establish initialization 2 or a minimum seed.
- Ordinary square bilayer: 86 closed pieces cover [0,.108] with gap≥.004499695659. A cover of 88 pieces covers [0,.10825] with gap≥.000586405978, every integer square side L≥2. Both nested results remain.
- Near-uniform alternating-chain Stage20 intervals remain separately preserved, including odd cell 15/17 starts. No coupling connection to the earlier weak-dimer g≤.225 results is established here.
- Original first/second theorem comparisons, all 18 accepted thermal cases, complete finite uniform prefixes, and every prior failure/resource caveat remain in the inherited exact data.

No new uniform-chain gap value or bilayer gap is claimed in Stage21. Finite-volume uniqueness is not a proof of uniqueness of all infinite-volume ground states.

## Synthetic checkpoint tests

The [first incremental-control review](../bilayer_incremental_control_first_review/FINDING.md) independently passes a fresh 2945-record synthetic metadata assembly with complete signed 24 accumulator agreement, one-uncommitted restart/adoption, and a fully committed restart. These are synthetic records, not physical moments, and cannot enter a physical namespace.

That immutable source fails the production gate because committed startup does not bind the payload digest to attempt.output_sha256. Its physical memory partition and dispatcher were not run under that first seal. The earlier six complete small m0–m4 fixtures, bounded physical samples and partial22 hardening finding remain limited to their original scopes. Full 8×4 moments are not computed, there is no new endpoint or gap, and full production is not authorized. The later corrected source has a separate final component acceptance below. That later result does not rewrite this first failed seal.

## Corrected controls and the 24-field calculation

The [final component review](../bilayer_variable_g_control_review/FINAL_REVIEW.md) accepts all 24 fields on six independently spin-derived dense small fixtures, 30 exact variable-g 2×2 pencils, corrected incremental-control behavior, and one actual 8×4 fixed-witness vacuum target. Physical K/J denominators are 22·g_den and its square. The final control report passes 26 checks, including exact receipt/digest binding, namespace separation, stale-run/retry accounting, partial-coverage rejection and cleanup after planned faults.

The separately sealed producer revised 64/64/128 MiB virtual-address-space profile and bounded integration evidence were inspected. The original 32/64/160 MiB producer failure is retained, even though the lean independent vacuum wrapper passed. Combined RSS must include the future outer observer. Sampled RSS is not a proof against all polling overshoot or arbitrary ENOMEM. One committed vacuum target and a labelled small-fixture finalizer mock are not a complete 8×4 moment sweep.

The production launch remains blocked on the following two concrete prerequisites.

1. A hash-pinned, externally bounded and accounted launch guard covering the production entrypoint from process start, including imports, startup, process-tree CPU/RSS, deadline and cleanup.
2. Independently verified accepted-57D fixed-witness m0/m1/m2 controls with exact physical normalization and source provenance.

A separate production resource authorization and fixed job identity are still absent. No full 8×4 m3/m4 or new gap is accepted. The nominal 21,600-second plan is a planning budget, not permission or a completion guarantee. The final component review excludes its large 2,945-record raw synthetic scratch directory. Source/generator pins, benchmark results, selected mutation evidence and receipts are sealed. This does not claim a full raw synthetic inventory seal.

Three no-refund review ledgers close at 90/90, 8/8 and 8/8 CPU seconds. Both reviewer-check failures remain recorded. The first was a generic-vacuum comparison mismatch, and the second was an analytic reference omitting D hopping. The final corrected gate includes the hopping terms and passes. The first 25 seconds of compile/fixture reservations did not separately meter the external review parent, which remains disclosed. Later parent receipts do not repair that historical omission. See [component scope](stage21_component_scope.csv). Active outer-launch work is excluded from this snapshot.

## Producer-only restricted-cell failure

The [restricted-cell producer proposal](../alternating_restricted_cell_seed_proposal/README.md) has no independent acceptance. Tested cell 15/16/17 constructions do not close this bootstrap recipe. The separate counterfactual thermal target .835 is unachieved and remains a conditional design target, not a physical certificate or a necessary threshold. No g=.9 seed, smaller successful initialization, new gap or universal no-go result is supplied.

Its resource status remains NOT_ACCEPTED. Measured child CPU 30.397826 seconds and charged CPU 30.697826 seconds, including reserves, exceeded the 30-second authorization. Scientific computation was stopped. This record is preserved in [unaccepted findings](stage21_unaccepted_findings.csv). Inclusion in an overview is not independent scientific or resource acceptance.

## Resource history and reproduction

The observable checks and both interval audits together conservatively charge 24.081720854/30 review CPU seconds, including three full 2-second sealing reserves. Separate compilation attempts, including the preserved pre-exec failure, total 16.872037073/30 seconds. The final interval review itself records 2.586350 child plus .157467666 launcher CPU seconds, CPU 5, 256 MiB, external watchdogs, post-exec guards, and no remaining descendants.

The corrected producer finite-bridge attempt used 18.508296 child plus .315004 launcher CPU seconds. Its cumulative gate, including the preliminary failed proposal, records 22.904749356/30 seconds, or 25.530375 with the conservative full-parent charge. The preliminary floating selection failure and the one authorized exact-bisection correction remain separate immutable packages. Older direct25 and 58D resource caveats are not erased.

[Provenance](PROVENANCE.md), [dependency pinset](STAGE21_DEPENDENCIES.json), exact source hashes, complete accepted manifests and all inherited CSV bytes are checked before rendering. The reproduction script hydrates the prior lossless 18-path evidence transport and verifies that every PNG/PDF reproduces byte-for-byte. It runs no producer physical campaign.

The parent-reported last verified remote main before this snapshot is 47a0c919d8c32f65e564ff7a5453a6eca3efd60c at 2026-10-11 03:52:34 UTC. This overview writer does not modify root files or publish remotely. The research cutoff recorded for this historical snapshot was 2026-10-14 00:00 UTC / 2026-10-13 20:00 America/New_York (EDT). Current work follows the latest project status and user instructions.
