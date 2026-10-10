# Fixed auxiliary ground witnesses for coupling intervals

2026-10-10 15:04 America/New_York (EDT) / 19:04 UTC.
Status: exact export candidates; independent review and interval acceptance
remain pending. The separate ground_moment_pencil freeze is unchanged.

All 21 inverse-moment negative-direction vectors have been exported as fixed
coefficient vectors c in the existing 11/29-dimensional trial spaces. Each file
contains:

- exact Gram norm, with the original common factor 2^N removed;
- affine shifted Rayleigh coefficients R0+R1 g;
- quadratic full second-moment coefficients Q0+Q1 g+Q2 g²;
- quadratic full residual-squared coefficients V0+V1 g+V2 g²;
- the center-coupling cutoff, lower endpoint, complete residual, scalar Temple
  endpoint, and negative polynomial witness check;
- original sharper Rayleigh upper at the center, so the auxiliary lower-bound
  vector need not replace the original variational upper-bound vector.

The vectors do not represent distinct low eigenstates. Every one is an
alternative witness for the same unique ground. They may supply different
upper/lower bounds on that one state; do not sum their heat-trace contributions
or enlarge the retained-state count.

## Exact algebra and center acceptance

The audited basis is independent of g and H'(g)=H'(0)+g V. Hence G is constant,
A(g) is affine, and the complete B(g) is quadratic. `export.py` interpolates
those exact matrix coefficients from the stored .03/.04/.05 inputs and checks
all three matrices, selected basis indices and denominators against every
stored .03,.04,.05,.06,.07,.08,.10 input. No new Hamiltonian action, physical
state expansion or higher moment is computed.

For norm n=c*Gc, let rho(g)=c*A(g)c/n and
variance(g)=c*B(g)c/n-rho(g)^2. At the center, each exported vector obeys

    (rho-a)(rho-l)+variance < 0.

Because variance>=0, this implies l<rho<a and

    rho-variance/(a-rho)>l.

Thus the auxiliary vector's scalar Temple bound is at least the exported
pencil lower endpoint without interval matrix inertia. To use it across a
coupling interval, keep c fixed and re-establish the required uniform sector
count/cutoff and scalar inequalities throughout that interval. The export
itself is not a continuous-coupling certificate.

## Files

`auxiliary_{shape}_g{center}.json`: the 21 fixed-vector scalar exports.
`matrix_polynomial_{shape}.json`: exact full G and matrix A/B polynomial data.
`summary.json`: all exports and source SHA-256 checksums.
`FROZEN_MANIFEST_SHA256.json`: this export's freeze.

Replay from the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python research_20261010/low_band/ground_moment_auxiliary/export.py

Replay overwrites generated files only in this separate export directory.
