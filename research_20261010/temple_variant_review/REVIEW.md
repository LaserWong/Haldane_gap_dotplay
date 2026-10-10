# Independent review of the direct-sector Temple improvement

Updated 2026-10-10 14:12 America/New_York (EDT) / 18:12 UTC.

## Accepted result

The ordinary spin-1/2 square bilayer, with vertical coupling 1, both straight in-layer couplings equal to g, no crossed exchanges, and the established periodic multiedge convention, has the following independently verified sufficient gap bounds for **every integer square side L>=2**:

| g | Gap lower endpoint | Direct asymptotic onset |
|---|---:|---:|
| .03 | .282017228092 | L>=8 |
| .04 | .180632156388 | L>=8 |
| .05 | .104475599844 | L>=16 |

The missing smaller sizes are covered by the previously independently accepted local and finite-window inequalities. Their gap bounds exceed these new endpoints. Unique finite-volume ground states follow. No actual-gap equality, infinite-volume uniqueness, or formal proof-assistant verification is claimed.

## What is inherited and what is new

The sealed `../large_seed_review/` independently reconstructed all physical ground moments, complete translated triplet moments, spin/translation multiplicities, number-sector bins, and the complete count of 1+3N states below a2. Its manifest SHA-256 is:

058ded69771bffe4822090fc8f88175592e5170e932173962fd32d02bd1d056d

That directory has not been edited. Each new patch's declared physical source hash is checked against the exact frozen input used by that review. Every unchanged model, size, spectral bin, and multiplicity field is compared with the accepted angle-based patch. The new producer freeze `TRANSLATION_AND_MOMENTS_FREEZE_1807.json` contains 91 files; its bytes and all 19 moment-bound files are preserved here.

This variant changes only the scalar lower eigenvalue bounds and the resulting trace/recurrence calculation. No new Hamiltonian application, trial vector, Hilbert-space truncation, or low-state completeness assumption is introduced.

## Why rank-one Temple applies to every retained state

The independently counted global band and exact invariant sectors show that each represented ground or momentum/spin sector contains exactly one eigenvalue below a=a2. All other eigenvalues in that sector are at least a. Its normalized trial has theta<a and full residual square r²>=0.

For the lowest sector eigenvalue lambda, the operator (H-lambda)(H-a) is positive semidefinite: it vanishes on the lowest state, and both factors are nonnegative on every other eigenstate. Taking the trial expectation gives

r²+theta²-(lambda+a)theta+lambda a >= 0,

hence

lambda >= theta-r²/(a-theta).

The argument also permits an omitted eigenvalue exactly equal to a. The unique full ground is in the even singlet sector, so the stronger cutoff a2 applies to its second sector eigenvalue even though the full Hamiltonian has triplet levels below a2.

This direct scalar formula is the k=1 specialization of the independently reviewed inverse-moment lemma. It does not use an approximate complement bound or an angle estimate.

## Independent exact acceptance

`audit_temple.py` imports only earlier independent audit helpers, not producer code. It checks all nine patches:

- The exact rational ground Temple endpoint and unchanged upper endpoint
- Every algebraic endpoint theta-r²/(a2-theta) in Q(sqrt(2))
- Every outward rational lower endpoint and exact Temple margin
- The positive denominator a2-theta, nonnegative residual square, and lower-branch direction
- Full band dimensions, spin multiplicities, source hashes, and inherited complete number bins
- That every new lower endpoint improves its already accepted angle-based counterpart

The complete-band trace and all positive number-sector tail terms are recomputed with the separate 384-bit, 90-term directed exponential construction from the sealed independent audit. This differs from the producer's 256-bit, 70-term code. All J1,J2,C ratios, first-cycle fractions, rounded recurrence updates, final sizes/temperatures, and gap endpoints agree exactly. A direct exponential inequality additionally certifies every logarithmic gap endpoint.

## Reusing the finite-size bridge correctly

An independently proved gap on a finite-size window remains valid regardless of the inverse temperature chosen for a different asymptotic certificate. Thus the old windows can be retained even though the newly optimized beta changes at g=.04 and g=.05.

The reviewed local bounds for L=2,3 are at least .64,.52,.40. The base side-4 finite-window bounds are .337867884900,.264039251376,.188350474715. For g=.05, the reviewed side-8 window has bound .169897925769. All strictly exceed the new target gaps.

The verifier checks these exact comparisons and confirms complete coverage of every integer 2<=L<the new asymptotic onset. No unjustified reuse of a seed temperature or staircase side occurs.

## Files and scope

- `REVIEW_STATUS.json`: machine-readable acceptance and final all-size values
- `results/patch_review.json`: nine exact sector-endpoint checks
- `results/trace_and_all_size_review.json`: three independent trace/recurrence/all-size checks
- `INPUT_SHA256.json` and `snapshot/`: immutable moment-variant inputs
- `PRODUCER_FREEZE_1807.json`: supplied producer provenance
- `audit_temple.py`: independent replay

Run `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python audit_temple.py` from this directory. It checks the adjacent sealed large review by hash, imposes one-CPU affinity and at most one GiB address space through its independent helper, and writes only this variant review. No remote state is changed.

The general k>1 inverse-moment theorem is analytically accepted in the sealed large review. This numerical audit concerns its rank-one sector specialization; the producer's 72 internal multilevel tests are preserved but are not mislabeled as an independent numerical audit of every general-purpose implementation path.
