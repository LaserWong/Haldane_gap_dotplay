# Independent n28 finite-window coverage review

2026-10-11 02:29UTC /2026-10-10 22:29 America/New_York.

## Accepted conclusion

For the untwisted periodic uniform spin-one Heisenberg Hamiltonian with bilinear coefficient1, the unique-ground-state gap is at least179/10000=.0179 for every integer L≥28. The newly proved finite window is28≤L≤56 at beta49/4. Combining it with the independently accepted .0179 tail L≥30 leaves no uncovered integers. Bootstrap initialization remains30. This review does not accept an n28 bootstrap initialization.

The stronger nested bounds .0245 from32 and .0248 from34 remain available from uniform_smaller_second_initialization_review, manifest54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f. Producer bridge manifest66c710bfc302c3f6a220a3162d933add710bfe51aef6fbcf1e256d6725430b55 is fully verified. All18 thermal inputs retain their independent physical acceptance792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94.

## Physical anchor and exact scalar proof

A fresh entrywise reconstruction of the fixed physical D26 tensors, norm transfer and spin-one two-site insertion again matches the accepted original block matrices. Tiny physical amplitude checks at lengths2 and3 pass. The previously inspected independent sequential GMP engine is reused with externally enforced30CPU-second/100MiB limits. It cannot raise these hard limits. The fresh batch outputs48,52,56 in one sequential run;48 matches the accepted benchmark. The56 norm and TOTAL Hamiltonian numerator exactly match the producer, and H0_56/N0_56+56a<0, a=700741/500000. It is a true56-site trial state, with no reused72-site energy. Its physical Hilbert dimension is3^56; bond dimension26 and one-dimensional trial span are separate quantities.

The52 and48 results are recorded as additional physical anchor outputs only. They do not contribute to the n28 bridge or imply a gap at26 or24. Their separate files are extracted from the fresh independent batch, not producer copies.

The negative56-site shifted Rayleigh quotient gives Z56(b)>1 for all b>0 without assuming ground uniqueness. The refined signed J,N moment intervals, caps and the N28 polynomial majorant are exactly the already accepted inputs. N contributes with multiplicity3. Packing lambda^12 with exponent56/12 forces a J atom above ell, and ell exceeds both the negative-J cap and N modulus cap. The residual J twelfth mass is positive and below ell^12, proving a unique positive leading atom. All fractional powers are independently bounded by exact integer-root inequalities at140 decimal digits.

Writing Q for the upper56-site trace, R=mJ12−ell^12 and B_N28 for the accepted signed N28 moment upper bound, the independent reconstruction proves

    S(28,beta0) ≥ [1+(R^(28/12)+3B_N28)/ell^28]^-2,
    T(56,beta0) ≥ Q^-2.

The saved endpoints are conservative. The labels remain spatial28 and thermal56. The checker does not silently identify T56 with T28.

At K=S²T>1/2 set w=(1+sqrt(2K−1))/2, rho=(1−w)/w, d=T/(1+rho²). The inherited all-integer signed-transfer lemma gives purity C≥(1−rho)min(S sqrt(d),d) at every integer28..56. Its physical trace identity is valid at every length≥4, including odd lengths; no twisted odd chain is substituted. A positive leading eigenvalue is justified by the physical positive odd traces, not assumed for the whole spectrum. The independent lower endpoint is C=.5800209325816545 (display), with exact positive margin

    C−exp[(49/4)(179/10000)](1−C)>0,

approximately.05707406328829727. Exponential enclosure is independently directed. Exact fractions, not the displays, prove both the gap and uniqueness. The accepted30-tail begins inside this window, so their union is every integer≥28.

## Failed continuation and finite scan

The checker reproduces the producer's literal100-digit rounded recurrence, including its use of NEW S in the thermal update. For zero requested gap, the particular n28 attempt fails its round2 saved purity lower bound, C=.4439946414447402<1/2. For gap.0179 it fails already at round1. These endpoints match exactly. A failed lower bound is not an upper bound on physical purity, so neither is an impossibility theorem or minimum-initialization proof. The successful first window is unaffected by later failure.

The floating pilot is recorded as1021 bounded-grid candidates, all reported unsuccessful. This review checks its record count and scope but does not certify floating search calculations as exact results. There is no exclusion over all real cooling temperatures, other moment bounds, adaptive orders, or all possible initializations.

## Reproducibility and resources

The fresh batch used18.1619CPU seconds/11912KiB onCPU5, plus approximately1.2CPU seconds for physical matrix rebuilding. The scalar replay used0.085CPU seconds/14328KiB onCPU4. The resource limits are30CPU seconds/100MiB for the separately authorized physical work,60CPU seconds/256MiB for scalar work. No thermal job or producer code is executed by this review. Seven adversarial scope/corruption checks reject label confusion, a gap in coverage, negative margins, and improper promotion of bounded failures.

Run check_anchors.py, audit_bridge.py and adversarial_tests.py in a disposable copy with the pinned sibling packages. Fresh physical replay additionally uses rebuild_d26.py and limited_run.py48 52 56. All prior producer/reviewer seals remain unchanged. No n26/n24 gap claim belongs to this package.
