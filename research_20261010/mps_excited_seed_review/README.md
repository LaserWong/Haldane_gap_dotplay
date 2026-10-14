# Independent review of compact excited-MPS witnesses

The three-state physical witnesses and exclusions for the specified scalar method passed independent review.
`REVIEW.md` gives the proof and limitations, and `CLAIM_VERDICTS.json` summarizes the conclusions.
`SEAL.json` and `MANIFEST_SHA256.json` preserve their provenance.

- At n = 14, 16, and 20, the specified single-Rayleigh numerator method with delayed conversion using joint ratios fails for every β≥0.
- At n = 24, the necessary-condition test leaves [13/2,45/4] unresolved. This interval is not a feasibility certificate.
- The full physical spaces have dimensions 3^n and 3^(2n). The retained denominator span has dimension three, and the MPS bond dimensions are 26/52/52. No physical-basis expansion is performed above n = 6.
- Independent exact source contractions through 24 and ground-state contractions through 48 match every generated integer. No many-body eigensolver is used.

The seal covers only this three-state core.
Any later review of a longitudinal extension has a separate scope and seal.
