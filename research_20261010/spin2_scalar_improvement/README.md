# Spin-2 scalar startup: bounded improvement and a sharper obstruction

Updated: 2026-10-10 14:31 EDT / 18:31 UTC.

No viable joint spatial/thermal startup was found. No new large heat trace,
physical many-body diagonalization, software installation, or uniform spin-2
gap result is claimed. Do not launch a full L9/L10 campaign on this evidence.

## Useful results

1. **New atom-location lemma.** Global positivity of the physical P/C twisted
   traces, including odd-length trivial-sector positivity, forces the largest
   spatial modulus to occur as a positive trivial-sector atom. The existing
   MPS lower bound and L8 trace upper bound therefore locate such an atom
   without an independent nontrivial-sector mass bound below one. Exact
   rational thresholds at L128,256,512,1024 are 0.971082, 0.985901, 0.993037,
   0.996540. See [proof](POSITIVITY_DOMINANCE.md) and [checks](atom_location.json).
   The full all-length transfer hypotheses and inherited input assumptions are
   explicit. This improvement does not control the next atom or thermal purity.

2. **Exact I/P finite-moment obstruction.** An explicit rational, integer-atom
   spectrum matches all 14 archived I/P boxes at L2..8, lies within proposed
   L9/L10 boxes with radii 6e-6/5e-5, and has positive I/P traces at every L>=2.
   Yet at a=4.76121, beta8 it gives Z128>53.761701 and S(64)≈0.273805238.
   This defeats unconditional N-mass-below-one and numerator-one denominator
   strategies based solely on those boxes. It does not refute a conditional
   J-cutoff argument or a physical gap. **Its integer spectrum is excluded by
   the known C moments; no cross-temperature constraints are imposed.**
   See [proof](IP_WITNESS_PROOF.md) and immutable [audit packet](frozen_ip_witness/).
   [Independent review](../spin2_moment_review/README.md) accepted the narrowed
   I/P interval relaxation. The atom-location lemma is still separately pending.

3. **C-aware PSD screen.** A separate exact-rational positive-measure witness
   passes all 21 I/P/C boxes through order8 plus the proposed I/P orders9/10,
   while retaining bad fixed unit atoms. Its residual weights are noninteger,
   and all-length positivity was not imposed. This is a relaxation diagnostic,
   not a full C-aware counterexample. See [additional notes](C_AND_MPS_NOTES.md).

4. **Existing MPS twist formulas.** Character-weighted contractions of the saved
   exact blocks give a cheap seam-matched trial-state route. A four-second
   floating check finds useful positive-coefficient trivial-sector lower bounds,
   but no new rigorously certified twisted energy. No extra contraction is
   warranted until a scalar ratio proposal shows how it closes the thermal
   step. See [diagnostic data](mps_twist_screen.json).

5. **Error slack.** All eight cached beta rows retain a super-unit atom after
   full signed 4x4 Hankel and 3x3 localizer tests, robustly under coordinatewise
   moment errors of 1e-4. This exact decimal-center algebra remains conditional
   on unverified higher-order inputs. See [checks](robust_hankel.json).

## Next decision and stopping condition

The requested bounded scalar pass is complete. The new leading-atom lemma is
worth independent review, and the rational I/P witness is already under review.
The next scientifically useful step would be a genuinely joint beta/2beta or
C-aware integer/multiplet constraint that supplies thermal concentration, with
an explicit winning sensitivity budget. A new cap grid or a large trace run is
not justified by the current results. No additional physical inputs requested.

## Reproduce the accepted scalar checks

All jobs use at most one numerical thread and impose a 1 GiB address-space cap.
The exact witness verifier needs only the Python standard library. From here:

- python verify_integer_witness.py
- python verify_atom_location.py
- python verify_c_psd.py
- python check_robust_hankel.py

The first command writes the nonfrozen output; do not run it inside the immutable
frozen packet. The LP/nonlinear prototype scripts and their initial seed files
are discovery provenance only. Some intermediate spectra fail uncomputed trace
positivity; only `full_integer_witnesses.json` is the accepted integer witness.

The original extracted tree has no .git metadata. Parent provenance records
source commit 6be889a30f642bde77fb89af75b3a7379615bed1. All new writes in this pass
are contained in this directory; original tensors and finite traces were read
without changes.
