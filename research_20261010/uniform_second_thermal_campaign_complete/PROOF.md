# Physical-input completion and provenance

## Certified objects

H_n(g) is the periodic uniform spin1 Heisenberg Hamiltonian, coupling1, with physical dimension3^n. g=I or a pi z-axis rotation on the closing bond. The shifted trace is Tr exp[-(49/4)(H_n(g)+n*(700741/500000)I)]. There are18 objects: every n4..12, both seams, including odd lengths. No cyclic seam, beta/2beta trace, or spatial/temporal relabeling is used.

The independently accepted kernel/symmetry/error proof in uniform_second_thermal_kernel_review underlies the campaign. Integer sparse D=32I-3nI-2H yields R=D/32, a self-adjoint contraction because0<=3n/2+H<=5n/2 and n<=12. Matrix entries are generated directly from physical spin transitions. Real integer Poisson-Horner columns approximate F=exp[98(R-I)] using cutoff280,Q2^55, coefficient floors,192 effective nonzero steps but281 charged error steps. Correct negative floor, signed64 partial-sum bounds, signed128 squares/unsigned12864-term accumulations and unrestricted GMP final sums were independently reviewed.

Nonnegative magnetization representatives use dihedral word orbits, doubled for M>0; at M0 global negation enters the orbit. Signed translations restore the pi seam; they preserve exact heat-column norms for all allowed lengths, including odd n. Rounded columns need not be signed-equivariant, so the error proof compares weighted direct sums of exact and rounded representatives. This is why exact representative specification is part of each certificate, not a cosmetic optimization. The reviewer independently reconstructed physical matrix/orbit identities, including odd fixtures.

For each n, d_n=floor(sqrt(3^n))+1 and E_n=281(d_n+1)+1. Weighted full-norm error is bounded by d_n E_n. With W the independently accumulated sum of integer squared column norms times physical multiplicities, r=floor(sqrt W), x=(49/4)n(3/2-a), s=sum_{j=0}^{100}x^j/j!,t=x^100/100!, the exact thermal enclosure is

L=s*max(0,r-d_n E_n)^2/Q^2,
U=(s+t)*(r+1+d_n E_n)^2/Q^2.

The complete records show L>center-30e-6 and U<center+30e-6 for all18 cases. Actual full W totals are independently formed from physical columns; published integers enter only at final comparison. All18 match exactly. No eigensolver, stochastic trace, imported upstream execution or full-spectrum input was used.

## Identity, completeness and independent-review boundary

The strict runner was reviewed separately. Every case binds physical parameters, original wrapper/source/binary/coefficients, complete orbit-code/multiplicity lists and physical sparse-matrix digests. Every checkpoint binds case/sector/range identity, source pins, ordered representatives and exact norm records, weighted sum and canonical payload hash. Complete-case aggregation requires every expected batch once, no duplicate codes or gaps, total physical multiplicity3^n, exact rational endpoint arithmetic, and full payload-digest linkage.

export.py performs a further read-only producer verification of all2428 checkpoints, identity/payload hashes, completeness, exact W, rational intervals and printed equality. It does not substitute for independent review and does not rerun heat columns. Source/kernel/matrix/orbit proof is inherited from accepted review; final campaign-data audit is pending. The entire terminal run directory is SHA256-pinned in CAMPAIGN_STATE_SHA256.json and all final certificates are copied here.

## Preserved failure history and successful repair

The original campaign completed16 cases then failed at a runner-invocation CPU boundary on L12I/P. Both unknown reservations7320 remain fully charged. The partial outcome and independent partial review are immutable historical records; nothing is silently replaced. The authorized extension saved byte-identical original terminal history, retained every original attempt/binding and16207 charge, and appended +21600 authorization for a43200 cap.

The independently accepted repair changes only supervision: at most eight complete batches, internal600 allowance, fixed35-second compute/5-second metadata caps,552 worst-case CPU reservation per L12 invocation. The bounded invocation cannot reach the legacy insufficient-allowance branch. Arithmetic source/kernel and checkpoint pins remain byte-identical. Parent-death/absolute-deadline protections, group cleanup, at most two CPU0/1 worker trees and256MiB tree memory ceiling were retained. Normal terminal whole-tree wait4 permits conservative refunds; no old unknown attempt is refunded. No new failure occurred.

Final state is ALL_CASES_COMPLETE_PRODUCER_REVIEW_REQUIRED, with0 active attempts,27543 charged of43200. All61 old attempts agree exactly with the frozen partial ledger. The fixed06:00UTC campaign deadline was not reached. Terminal state blocks automatic restart.

## Theorem status

These are the missing beta49/4 physical thermal premises used by the official n36/72 initialization and subsequent conditional scalar packages. Final independent acceptance can discharge those premises, but each gap claim still requires its own already reviewed scalar/analytic chain and accepted variational anchor. This producer export itself asserts no newly promoted all-size gap or minimum-seed theorem.
