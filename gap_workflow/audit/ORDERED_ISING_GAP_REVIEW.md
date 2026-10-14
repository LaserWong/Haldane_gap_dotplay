# Independent scope and proof review: ordered periodic Ising

Reviewed 2026-10-14 20:10 UTC. No source or theory edits made.

No actual mathematical issue found in theory/ORDERED_ISING_GAP_DEFINITIONS.md.

- The negative single-spin-flip matrix is irreducible, so Perron–Frobenius establishes a unique full-space ground state. Global flip permutes its positive coordinates and therefore has parity +1.
- In the ordered h<J regime, the R zero mode changes its vacuum occupation; both physical sectors retain even quasiparticle number. The NS unpaired pi mode for odd L has positive coefficient and does not alter that conclusion. The positive-direction doubled L=2 convention is compatible with the stated dispersion and vacuum formulas.
- Z_i applied to the even ground is a normalized odd trial state. Conjugation changes only -(1/2)X_i, with energy increment <X_i><=1. Thus delta<=1. Each non-vacuum allowed state has at least two modes, each of energy >=1. The two vacua consequently are the bottom two levels, and Gamma>=1.
- The listed cheapest pair energies use distinct allowed modes, including L=2. Their limits are both 2. Once delta tends to zero, Gamma and E2-E0 both tend to 2.
- The binomial square-root branches are analytic on 1/2<|z|<2. Cauchy bounds on reciprocal contours give the stated M_rho rho^(-|n|). The difference of R and NS discrete sums selects odd Fourier multiples and yields delta=-L sum_(j odd)c_(jL), with the factor of one half from vacuum energies included correctly. Summing both positive and negative odd multiples gives 2 L M_rho rho^-L/(1-rho^-2L). With rho=3/2 and M_rho<4, the displayed exponential upper bound follows.

The note correctly limits the conclusion to periodic finite-volume spectra and their volume-dependent gap definition. It does not identify a near-degenerate doublet with an exactly two-dimensional ground space, nor assert the same result for an infinite-volume symmetry-breaking representation. The h=0 endpoint genuinely has a different exact ground rank and gap index. The registered paramagnetic CLI route is not extended by this research note.

This was an analytic review. The existing independent four-Ritz-pair benchmark remains numerical corroboration, not an exact spectral count or lower bound.
