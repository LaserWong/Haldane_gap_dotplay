# Research checkpoint at the pause

October 10, 2026, 16:25 UTC.
Research and computation were paused at the user's request.
The status recorded below refers to that checkpoint.

## Completed material

- `THEORY.md` contains the two-dimensional three-purity recurrence, the two selfadjoint transfer constructions, interpolation to all integer square sizes, the scope of the GNS limit, analytic bilayer and spin-1 large-D examples, and two obstructions to strip-based inference.
- `three_purity_certificate.py` implements exact rational exponential bounds, recurrence updates, and gap acceptance using only the Python standard library.
- `bilayer_seed_certificate.json` and `spin_one_seed_certificate.json` contain conservative analytic seed certificates.
- `NONPERTURBATIVE_MODELS.md` gives the exact one-dimensional trial space and rigorous direct gap for the fully frustrated bilayer at J=3/10, together with its use in the same three-purity framework.
- `fully_frustrated_bilayer.py`, `fully_frustrated_one_trial_n2.json`, and `fully_frustrated_one_trial_n4.json` provide the exact zero-residual ground-state trial and a binomial tail bound covering the entire omitted spectrum.
- `PRIMARY_LITERATURE.md` compares the checked primary sources for frustration-free and non-frustration-free methods.
- `GENERAL_DIMENSION.md` derives the general d-dimensional extension, which had been submitted for independent review. Its constants are more conservative than the dedicated two-dimensional constants. A package must identify its independent-audit status separately from the reviewed two-dimensional result.
- `toy_checks.py` and `toy_checks.json` provide small-system floating-point diagnostics for the two analytic obstructions. These values are not inputs to the gap proof.

## Conditions needed by the certificates

The three-purity certificate assumes exact real selfadjoint Hilbert–Schmidt thermal transfers in both spatial directions.
Each transfer identity must hold for every integer length at least 2 in that direction.
A periodic direction of length 2 retains repeated periodic bonds and cannot be replaced by a simple graph.

The standard staircase is A=Z(2n,m)/Z(n,m)^2, B=Z(2n,2m)/Z(2n,m)^2, and C=T(2n,2m).
Sequential updates use the newly computed defects.
For a common two-dimensional defect u≤1/500, the bound gap≥log(1/(32u))/β applies to the common-scale rectangles and all integer squares covered by the theorem.
A square seed does not establish the result for every rectangle of arbitrary aspect ratio.

The fully frustrated bilayer H=Q+JΣT_r·T_s differs from the ordinary bilayer.
Each intercell edge in the fully frustrated model contains four equally coupled bonds, including intralayer and crossed bonds.
At J=.3, the actual square-system gap is 1 for L≥3 and .4 for L=2, so its infimum over L≥2 is .4.
The weaker numerical three-purity bound must be reported separately.
Its trial dimension of 1 relies on the exact singlet product state and local conservation laws.
The full excited-state space remains exponentially large.

## Derived proposals awaiting implementation

The following proposals were not executable certificate inputs at this checkpoint.

For noncommuting weak bonds, a matching-color heat-trace bound can be obtained from convexity of logTr exp.
If each color forms a matching on the product-cell graph, then

$$
\log Z(H_0+\sum_cV_c)\le\chi^{-1}\sum_c\log Z(H_0+\chi V_c).
$$

This gives D≤χβ²Σ_e width(v_e)²/8.
The bilayer could further use the exact partition function of a four-spin matching block.
This proposal had not been incorporated into the formal recomputation script or independently audited.

The structure-breaking test uses intralayer coupling J+ε and crossed coupling J.
The derived full vacuum residual squared is (3ε²/4)Σ_unique_edges multiplicity².
It equals 12ε², 18ε², and 24ε² on 2×2, 4×2, and 4×4 geometries, respectively.
An independent comparison with physical matrices was still pending.

The SU(2)-singlet trial space with at most two triplets has dimension 1+binom(N,2).
An ordinary Mz=0 enumeration includes additional basis vectors.
Certification of the full spectrum still requires both a residual bound and a tail bound.

A candidate compressed action had been sent to the low-energy workstream but had not been implemented or independently checked.
Use the unnormalized states |ij>=Σ_a |t_a(i)t_a(j)>, with norm²=3, and write trial=c0|vac>+Σcij|ij>.
For r_ij=(ε/2)m_ij and K=J+ε/2, the proposed projected action is

$$
(Hc)_{\mathrm{vac}}=3\sum r_{ij}c_{ij},
$$

$$
(Hc)_{ij}=r_{ij}c_0+[2-2K m_{ij}]c_{ij}
+\sum_{k\ne i,j}(r_{ik}c_{kj}+r_{jk}c_{ik}).
$$

The three pairing amplitudes in the four-triplet leakage are a_(ij)(kl)=r_ijc_kl+r_klc_ij.
The proposed Gram matrix has diagonal entries 9 and off-diagonal entries 3.
The signs require verification in a consistent Cartesian-triplet phase convention before these expressions can be used for acceptance.

Low-energy certificates and structure-breaking tests in other numerical directories belong to their respective workstreams.
Their in-progress results are not recorded here as accepted results.
