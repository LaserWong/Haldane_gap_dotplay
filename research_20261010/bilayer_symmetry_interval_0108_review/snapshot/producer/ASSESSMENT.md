# Closed [.1065,.108] candidate, frozen

Updated 2026-10-11 01:00 UTC / 2026-10-10 21:00 EDT.

The ordinary isotropic spin-half bilayer, H′=Q+gA/2 with unit rung exchange and accepted periodic multiedges, has a new exact uniform candidate gap ≥ 21317927/4000000000 = .005329481750 for every real g in [213/2000,27/250]=[.1065,.108] and every integer square side L≥2, with unique full-Hilbert ground, pending independent review.

Four closed pieces, all using beta0=19/2:

- [213/2000,429/4000] = [0.1065,0.10725]: gap 0.009211598071; asymptotic theorem starts at L=256.
- [429/4000,861/8000] = [0.10725,0.107625]: gap 0.008251155962; asymptotic theorem starts at L=256.
- [861/8000,69/640] = [0.107625,0.1078125]: gap 0.006729933145; asymptotic theorem starts at L=256.
- [69/640,27/250] = [0.1078125,0.108]: gap 0.005329481750; asymptotic theorem starts at L=512.

All pieces use the same frozen .108 selected Temple-pencil vectors in21D/57D and energy vector in43D. The retained counts remain49/97/1; the full largest Hilbert space is2^128. Fixed complete variance quadratics are certified positive semidefinite; convexity controls their endpoint maxima. Reference-minus-affine-mean concavity controls uniform global-ground and full even-sector cutoff margins. Fixed odd Gram positivity, exact Q(sqrt2) complete-variance convexity, distinct momentum counts, cutoff margins and all omitted tails are retained. No gap-monotonicity assumption or point interpolation is used. See DERIVATION.md.

All correlated affine energy combinations are enclosed before exponentiation. Directed384-bit exponential bounds,60-decimal rational round-down, integer-square-root enclosures and exact exponential gap witnesses certify every finite window and terminal theorem uniformly on its piece. The previously accepted short theorem on[0,.15] supplies .050426624396 for every L=2,...,7. The finite windows plus terminal theorem cover every integer L≥8, including odd sides.

The initial coarser replay used two pieces with gap .002849073270. Its outputs are retained as initial_* history. The final replay additionally subdivides successful pieces whose rigorous gap is below the prior .004499695659 whole-range bound. It yields four pieces and the stronger .005329481750 extension bound. These subdivisions reduce uniform enclosure loss, without replacing failed/weak intervals by interpolation. result.json and checkpoint.json are the final four-piece deliverables; initial_* is not the final certificate.

Joining this candidate with the independently accepted82-piece[0,.1065] cover would give86 closed pieces on[0,.108] with unchanged uniform gap .004499695659, but only after independent acceptance of the new rational vectors and interval replay. proposed_join.json is explicitly provisional. No coupling above.108 has been tested.

The initial and final interval computations used approximately1.91+5.14=7.05CPU seconds total, under16MiB peak RSS, onCPU2 with one BLAS thread, within the separately authorized120CPU-second/256MiB allocation. No physical support contraction, eigensolver, new rational-vector optimization, predecessor/root edit or GitHub write occurred. Direct dependencies and source seals are pinned in INPUT_SHA256.json. The point sweep seal is9cfcc6ca5332fa4ed2724f16f49554efd5c5de535b736f1dffcbc94d7dde2475. Reproduce produce.py in a fresh sibling directory; do not overwrite this frozen package. This lane is stopped pending independent review and further authorization.
