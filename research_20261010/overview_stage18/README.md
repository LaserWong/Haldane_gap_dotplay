# Stage 18: uniform-chain gap .0214 after complete physical-input verification

The uniform spin-one Heisenberg chain has **a unique ground state and gap at least .0214 at every integer length L≥36**. This result, accepted at the historical checkpoint, uses untwisted periodic boundaries and unit bilinear exchange. The independent review also establishes the physical premises of the weaker .0046 bound on the same scope. The [final physical review](../uniform_second_thermal_full_review/PROOF.md) verifies all 18 thermal inputs and their exact mapping to both previously accepted scalar proofs and the prior 72-site D26 MPS anchor. No minimum-size or below 36 claim follows.

![Local physical completion and theorem comparison](stage18_uniform_physical_completion.png)

[New local theorem records](stage18_local_uniform_certificates.csv), [all 18 thermal cases](stage18_thermal_cases.csv), [exact provenance mapping](../uniform_second_thermal_full_review/provenance_results.json). The scalar proofs themselves are unchanged. The original conditional rows remain byte-identical historical records. Their premises are now discharged by the new review. Historical figures in this overview are labeled accordingly. [Stage17](../overview_stage17/README.md) and every older snapshot remain untouched.

## Physical input reproduction and normalization

At β=49/4, the 18 inputs cover lengths 4–12 with identity and π-twisted seams, including odd lengths. All 2428 saved batch aggregates, independent physical sparse-matrix digests, orbit representatives/multiplicities, exact integer totals and rigorous error intervals pass. This is matrix-polynomial column evaluation with certified errors, not an assumption of full exact diagonalization.

The final L12 integer totals are 1266666171463993322695232916 (I) and 524785463625387865619045258 (P). The independently checked physical enclosures reproduce both the coarse .0046 premises and the tighter 10^-18 rounded signed J/N intervals used by the .0214 proof. Coarse interval containment alone would not suffice for the latter.

The MPS72 input is the previously reconstructed physical state with bond dimension 26. Exact file identity, positive norm, one-bond numerator normalization and negative total shifted Rayleigh quotient match both proofs. No new MPS contraction is claimed. Physical Hilbert spaces for the thermal inputs are 3^4 through 3^12, distinct from bond dimension 26 and the physical 72-site size.

The immutable 2979-file campaign ZIP and its per-entry hashes are verified directly. The sealed producer export is `uniform_second_thermal_campaign_complete`, manifest 17110955acc17821025bab5c1609706273510de6c8c2a31eb7184d693a9b9156. The terminal charge is 27543 of 43200 CPU seconds, including the original 16207 charges. Historical failures, partial review and all previous evidence remain unchanged. No mutable campaign path is used.

The .0214 certified lower bound is approximately 44.6585 times the original first bound (4/105)log(80/79), and 5.6005 times the original asymptotic bound log20/784, on overlapping scopes. Original final theorems cover even L≥60 and even L≥2304 respectively. This new theorem covers every integer L≥36. These are ratios of sufficient lower bounds, not estimates of the physical gap. The original first initialization was 60, and its second initialization was already 36. The later 52 route improves the first dataset without improving every original initialization.

## Bilayer: complete 58D physical moments and finite-seed endpoints

The ordinary bilayer uses unit rung exchange and intralayer exchange g, with the periodic multiedge conventions in [Models and normalization](../MODELS_AND_NORMALIZATION.md). For the 8×4 seed (32 rungs, 64 spins), H′=H+24I=Q+(g/2)A. The finite-seed endpoints below use this shifted convention.

Positive-gap certificates are unchanged: every real g∈[0,.108] has lower bound .004499695659 (86 closed pieces), and every real g∈[0,.10825] has lower bound .000586405978 (88 pieces), for every integer periodic square side L≥2 with a unique ground state. Both nested certificates remain preserved.

The [independent full-row review](../bilayer_complete_residual_direction_58d_review/PROOF.md) contracts all 4495 fixed-origin q4 supports and 169911 q6 supports. All 174 new G/H200/H200² entries and 290 coupling-polynomial entries agree. The checks include 76566 supports where the old M channels vanish but T does not, along with 1019466 translation-anchor checks. Full signed q8 contributions and separate exact N/4,N/6 normalization are retained.

These are complete physical moments within the 58D trial basis, incorporating the accepted 57×57 block. Gram rank is 58. At g=.11 the 116D basis/Hamiltonian-image block Gram is positive semidefinite with rank 87. These checks supplement the physical contractions. They do not replace them. Physical Hilbert dimension of the 8×4 seed is 2^64.

The [separate endpoint review](../bilayer_residual_direction_58d_algebra_review/PROOF.md) accepts unique-global-ground identification and finite 8×4 shifted-ground lower bounds:

| g | Search dimension | Safe downward-rounded lower endpoint |
|---|---:|---:|
| .1085 | 58 | −.299703121631 |
| .11 | 58 | −.308337477991 |

[Exact endpoint records](stage18_ground_endpoint_certificates.csv) also preserve gains over fresh 57D vectors. These are ground-energy endpoints, not gaps or new coupling intervals. Four target pencils are positive definite only within the current 58D/fixed-r2 setting. Producer finite-temperature failures are scoped diagnostics, not independently rerun universal exclusions. Full untruncated even-singlet cutoffs and complete odd-sector counts are distinguished from full-Hilbert second-eigenvalue bounds.

The frontier gap routes at this checkpoint use 21/57 denominator search dimensions and a 43-dimensional numerator search, retaining 49/97/1 states. Earlier routes retain their own dimensions. The new 58D endpoint basis does not retroactively replace those dimensions.

## Engineering scope

The [physical fixture](../bilayer_residual_direction_fixture_review/PROOF.md), [corrected inner gate](../bilayer_residual_direction_production_gate_review/PROOF.md), and [sole-path outer gate](../bilayer_residual_direction_outer_gate_review/PROOF.md) have separate scopes. The outer gate accepts its fixed 46-call path with a nominal 350+10=360 CPU-second reservation and lifecycle/accounting design. It does not guarantee completion or unrelated optimization runtimes.

The 58D endpoint mathematics passes independently. **Producer optimization resource compliance remains UNVERIFIED.** Its [separately sealed clarification](../bilayer_residual_direction_58d_algebra/RESOURCE_CLARIFICATION.md) records a 33.13448-second child CPU report despite a configured 25-second hard limit, incomplete total accounting, and no verified 60 CPU-second total bound. The addendum is preserved, not promoted to engineering PASS. The independent physical-row and endpoint audits have their own measured, bounded runs. No new compiler work or active plans are included.

## Reproduction and integrity

Run `bash research_20261010/overview_stage18/REPRODUCE.sh` from the repository root. It hydrates the [inherited lossless evidence package](../../reproducibility/stage11_exact_evidence/README.md), verifies frozen source seals, the 2979 ZIP entries and prior snapshot bytes, runs exact extraction/corruption guards, and rerenders to a temporary directory for byte comparisons. It launches no thermal kernel, physical full-support pass or endpoint optimization. The checks use CPU8, one numerical thread and a 1GiB address-space cap. Root documents and remote publication are outside this snapshot builder.

[Validation](validation.json), [corruption checks](rejection_guards.json), [render replay](render_reproducibility.json), [visual QA](VISUAL_QA.md), [review seals](ACCEPTED_REVIEW_SEALS.json), [freeze record](FROZEN_STATUS.json), [manifest](MANIFEST_SHA256.json).
