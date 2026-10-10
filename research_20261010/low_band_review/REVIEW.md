# Independent review of the complete low-band method

Review started 2026-10-10 13:20 America/New_York / 17:20 UTC.
Reviewer writes only this directory. The producer files are never modified.

## Scope and result

The original affine-tail certificates for the ordinary spin-1/2 square bilayer at g=3/100 on 2×2, 4×2, and 4×4 periodic rung patches pass independent analytic and exact-arithmetic review. The periodic positive-direction edge multiset is retained, including parallel edges for side length two. The physical Hamiltonian has rung coupling one, straight in-layer coupling g in both directions, and no crossed coupling. Its shifted form is H'=H+3N/4.

The complete retained band dimensions are 13, 25, and 49, respectively, in Hilbert spaces of dimensions 256, 65,536, and 4,294,967,296. No thermodynamic conclusion follows from these finite certificates alone. The original affine-tail three-purity seeds fail the specified recurrence at every saved beta; independent replay reproduces each failure exactly.

The stronger number-sector tail and successful correlated seed are reviewed separately below in NUMBER_AND_BRIDGE_REVIEW.md once their exact checks finish.

## Independent reconstruction

`independent_review.py` imports no producer module. It starts from the physical four-spin matrix 4(S_i,0·S_j,0+S_i,1·S_j,1), transforms with a manually specified integer singlet/triplet matrix, and reconstructs the complete action on every reached basis configuration. It checks the supplied trial support independently by combinatorial enumeration. It rebuilds G, A, B, and E, including all leakage, and compares the exact integers with the saved certificate. The independent local kernel has denominator 400 at g=.03, whereas the producer's separated-layer construction has denominator 800; the audit accounts for this harmless scale difference exactly.

Every Gram matrix, residual PSD bound, local relative-form bound, Ritz endpoint, and Schur-polynomial endpoint is accepted using a separately implemented rational symmetric elimination with Fraction arithmetic. This does not call the producer's fraction-free Bareiss inertia routine. All nine blocks passed.

Runtime: approximately 0.13 s, 10.49 s, and 36.38 s for the three patches, including physical ED diagnostics on the first two. Peak RSS was 304,828 KiB. Each process pins itself to one CPU, uses one BLAS thread, and enforces a one-GiB address-space limit.

## Analytic proof review

Let Q be an orthonormal k-dimensional trial matrix, T=Q*HQ, and R=HQ−QT. Assume λ1≥L0, λ(k+1)≥a, T≤rI with r<a, and R*R≤εI. Min-max gives exactly k eigenvalues below a. For their spectral projector P, the Sylvester equation H_high X−XT=(I−P)R with X=(I−P)Q has the convergent one-sided integral solution. Its operator norm is bounded by ||R||/(a−r). Equal-rank principal angles give ||P(I−QQ*)||=||(I−P)Q||. Thus the orthogonal-complement compression is bounded below by

b = a−(a−L0) min(1, ε/(a−r)^2).

This argument is valid in operator norm, not merely Frobenius norm, because the spectra lie on opposite sides of a single real gap. It does not infer completeness from a small residual.

For rational trial columns W in a positive diagonal metric J, G=W*JW, A=W*JHW, and B=(HW)*J(HW). The directly evaluated residual Gram E=(HW−WD)*J(HW−WD) dominates the true projected residual Gram B−AG^-1A for every coefficient matrix D. Consequently E≤εG gives the needed normalized residual bound.

For t<b, the complement resolvent satisfies (C−t)^-1≤1/(b−t). The true Schur complement is therefore bounded below by the normalized pencil A−tG−E/(b−t). Its negative inertia is an upper bound on the number of full-Hamiltonian eigenvalues below t. The code's denominator-cleared expression (b−t)(A−den·t·G)·eden−den·E is exactly this pencil up to a positive scalar.

## Full-Hilbert counting and symmetry

The exact local inequality sums to H'≥αN_triplet−B, with α>0. The isolated-rung multiplicities are binomial coefficients C(N,q)3^q. There are exactly 1+3N states with q<2, hence λ(2+3N)(H')≥2α−B globally across all symmetry sectors.

The trial blocks contain one state in even parity/M=0, N in odd parity/M=0, and N in odd parity/M=+1 plus their exact global-spin-flipped M=−1 partners. Total magnetization and simultaneous layer exchange commute with H. The four spaces are orthogonal and contain k=1+3N states, all Ritz values below the counted cutoff. Min-max and the global count then leave no room for an omitted low mode, even in sectors never diagonalized. Each represented sector has exactly its claimed low-band dimension. No assumption that a numerical eigenvector has a particular total-spin label is required.

## Heat traces

For beta≥0, each retained eigenvalue interval contributes lower exp(−beta·upper) and upper exp(−beta·lower), with its exact multiplicity. The remaining ordered bins start at q=2 only because full-band completeness was established. The positive polynomial sum of the affine-bin tails has the correct direction of rounding. The rational Taylor remainder used by the producer is valid; `trace_audit.py` independently recomputes it using direct powers and factorials, checks every saved A/B/C input and every recurrence update, and verifies beta=0 gives the full dimensions exactly.

Current saved shapes and temperatures satisfy the required nx,ny≥2 and beta≥0. These preconditions were also suggested as explicit code guards for future reuse.

## Floating diagnostics, not proof

The independent physical-spin ED of the full 2×2 matrix has maximum eigenpair residual 6.1×10^-15; every certified low interval contains the corresponding eigenvalue. Exactly 13 eigenvalues lie below the certified cutoff. Six heat-trace checks, including beta=0, lie between the derived bounds.

The independent 4×2 physical-spin matrices in Sz=0,1,2 have dimensions 12,870, 11,440, and 8,008. Maximum checked eigenpair residual is 2.3×10^-14. The nine retained Sz=0 modes and eight Sz=1 modes fit their intervals. The sampled Sz=2 spectrum starts above the global cutoff. Completeness remains established analytically rather than by these samples.

`complement_diagnostic.py` directly reconstructs the complete 2×2 trial space in the physical basis. Its complement minimum is 1.8813806778 versus certified b=1.6720520123. Its actual principal-angle square is 1.3896×10^-6 versus certified 5.4197×10^-5. These are implementation diagnostics only.

## Reproduction

From the repository root, run in sequence:

    python research_20261010/low_band_review/independent_review.py
    python research_20261010/low_band_review/complement_diagnostic.py
    python research_20261010/low_band_review/trace_audit.py

Results are in independent_results.json, complement_diagnostic.json, and trace_results.json. Reviewed input hashes are recorded in reviewed_input_manifest.json. Production certificates remain unchanged.
