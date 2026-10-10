# Independent review of the ordinary-bilayer continuous-coupling certificate

Updated 2026-10-10 14:58 America/New_York (EDT, UTC−4) / 18:58 UTC.

## Verdict and scope

The frozen certificate passes independent exact-arithmetic and analytical review:

\[
\Delta_L(g)\ge \frac{486442811}{250000000000}=0.001945771244,
\qquad 0\le g\le 0.07,\quad L\in\mathbb Z,\ L\ge2.
\]

Every indicated finite periodic square has a unique ground state. The model is the ordinary spin-1/2 square bilayer: unit vertical exchange, equal straight intralayer exchange g in both layers and both directions, and no crossed bonds. Positive-direction periodic edges are counted with multiplicity, including the two parallel bonds in a direction of length two. The Hamiltonian is not the completely frustrated bilayer.

This is a simultaneous uniform statement on the entire closed coupling interval, not interpolation between sampled spectral gaps. At g=0 the exact gap is one. The certified constant is a sufficient lower bound, not an estimate of the physical gap or a phase boundary. No claim concerning all aspect ratios or uniqueness of all infinite-volume ground states is made. This review is not proof-assistant formalization.

The seed patches are 4×4, 8×4 and 8×8 rungs, with 32, 64 and 128 physical spins. Their full Hilbert dimensions are 2^32, 2^64 and 2^128. Their fixed ground-trial search spaces have dimensions 11, 29 and 29. Each denominator trace retains exactly one ground eigenvalue. The largest numerator uses exactly one Rayleigh trial vector, and does not require a largest-patch residual, second moment, spectral cutoff, excited band, or band completeness. None of these dimensions is an MPS bond dimension.

## 1. Frozen evidence and independence

The producer's 29-file freeze has SHA-256

`bf38883ef54e3bf0e5d80e1abcac8b9a21355106382d546d27cb413b3734c8c3`.

The original manifest is preserved as `PRODUCER_FREEZE.json`; every file in it is copied byte-for-byte to `snapshot/` and checked. `INPUT_SHA256.json` binds all local snapshots and the three inherited geometry inputs.

The audit verifies every entry of five sealed independent reviews, totaling 354 files:

- `large_seed_review`: 163 files, manifest `058ded69771bffe4822090fc8f88175592e5170e932173962fd32d02bd1d056d`
- `reduced_input_review`: 63 files, manifest `e5970d2303f65be0b69354417012aaf4925bf2920664d4890fb1e1e6cf2ff7d4`
- `quadratic_boson_review`: 36 files, manifest `0d9034b05db6968aa6647a010c8e832edf510f74fc8bbf601e22b44008b205bb`
- `alternative_order_review`: 61 files, manifest `025cdba0e315df7f148fe35a6831e04d7d87b61b03f3635fc7c876ad30d53469`
- `bosonic_tail_review`: 31 files, manifest `5ba82f60b9127d6bbf82b8ad7ad3af489edfb3661e40c6cc7eebc3eef7834f40`

The new program imports no producer module and no prior auditor implementation. It uses Python integer/Fraction arithmetic and object-array matrix products; there is no eigensolver. It independently constructs the periodic graph, pair orbits, Gram matrix, first moments and full second moments from the independently audited coupling-independent geometry. Existing transfer, quadratic-comparison, and finite-window theorems are inherited by explicit attribution, not presented as new proofs.

The shared working tree is an extracted snapshot without local Git metadata. Neither a commit nor publication is inferred from these filesystem writes. Root README/status integration belongs to the parent task.

## 2. Physical polynomial reconstruction

Write H′(g)=H(g)+3N/4=Q+gV. In the fixed physical trial basis W, G=W*W is independent of g, K(g)=W*H′(g)W is affine, and J(g)=W*H′(g)^2W is quadratic. The removed common metric factor is exactly 2^N. The basis consists of the vacuum, invariant two-triplet pair orbits, and the fixed four-triplet columns A42 applied to pair orbits; all are even under total triplet parity.

The auditor rebuilds graph edges and pair orbits rather than trusting saved adjacency or orbit labels. Previously independently reconstructed F/S/V/W contractions are reused by verified hash for 4×4 and 8×4. For 8×8, the numerical assembly reads only the separate minimal F/S geometry. Its routine returns before forming any second moment or consulting V/W.

For a general rational formal parameter g, the physical first-moment block is assembled directly from the vacuum creation, pair hopping, pair interaction and four-triplet blocks. Complete H′ images are combined in the second moment, including the q=6 contribution through W. This is a full residual calculation; J is never replaced by K G^−1 K or by a projection of H′ onto the trial space.

Exact evaluations at formal g=0,1,−1 recover the coefficients of the independently assembled known-degree polynomials. These evaluations are algebraic devices, not spectral-comparison claims at unstable g. The fixed-basis identity H′=Q+gV establishes the degrees for every g. Every coefficient equals the producer model. Exact Schur elimination also reproduces all selected independent columns and establishes the positive Gram metric.

The producer extracted its model using audited g=.03,.04,.05 anchors and separately checked later saved matrices. Our reconstruction does not rely on acceptance of any producer g=.07,.08,.10 certificate or on those interpolation checks.

For every one of the 48 saved integer coefficient vectors c, the audit recomputes

\[
\nu=c^*Gc>0,\qquad \rho(g)=\frac{c^*K(g)c}{\nu}.
\]

For the 32 denominator trials it recomputes the three coefficients of

\[
r^2(g)=\frac{c^*J(g)c}{\nu}-\rho(g)^2=v_0+v_1g+v_2g^2.
\]

All coefficients agree exactly. It verifies v0≥0, v2≥0 and 4v0v2≥v1². In particular this residual square is convex; its maximum on a closed interval is at an endpoint. The two-operator covariance matrix positivity is also checked, rather than assuming that rounded proposed residual coefficients define a nonnegative polynomial.

## 3. Parity-refined Temple bound

The inherited physical comparison embeds the entire 4^N-dimensional spin Hilbert space isometrically into the Fock space of D=3N modes, with P the at-most-one-boson-per-rung projection. It proves

\[
H'\ge PLP,\quad L=\alpha Q+B+B^*,\quad \alpha=1-2g,
\]

where Kpair=(g/2)A⊗Jcolor and B=(1/2)Σ(Kpair)uv a*u a*v. Weighted graph degree four gives ||Kpair||=2g. For 0≤g<1/4 the finite-mode oscillator is stable. Its diagonalization has positive frequencies ωj≥δ=√(1−4g) and vacuum energy at least

\[
E_b=-\frac{v}{\alpha+\delta},\qquad v=\frac{3g^2}{4}\sum_e w_e^2.
\]

The inherited proof treats self-adjoint form closure, complete oscillator spectrum and restricted form-domain min–max. These facts permit comparison at every ordered physical index.

The added parity argument is valid for the following reasons.

1. The exact two-rung physical exchange changes triplet count only by 0 or ±2. The audit independently rebuilds that 16×16 exchange from four physical spin-half sites and verifies every nonzero entry has even count change. Thus Π=(−1)^Q commutes with H′. It also commutes with P and L.
2. The orthogonal bosonic mode rotation is number-preserving and therefore commutes with Π.
3. In oscillator coordinates Π acts by joint coordinate inversion f(x)↦f(−x). Each positive coordinate dilation used in the stable Bogoliubov diagonalization commutes with this inversion. Their product therefore preserves parity. The transformed even sector is precisely the even reference-number sector, rather than an unidentified invariant subspace.
4. Restricting the form-domain min–max principle to the even sector gives λ2,even(H′)≥Eb+2δ. In the full space λ2(H′)≥Eb+δ. The first odd reference energy is Eb+δ, while the second even reference energy is Eb+2δ.

Each even trial has ρ(g)<Eb(g)+δ(g), uniformly as checked below. Since its Rayleigh energy is below the full second-eigenvalue lower bound, the full ground is unique, is in the even sector, and is identified by this trial. Applying rank-one Temple within that invariant even sector, with the full residual and cutoff Eb+2δ, gives

\[
\rho(g)-\frac{r^2(g)}{E_b(g)+2\delta(g)-\rho(g)}
\le\lambda_1(H'(g))\le\rho(g).
\]

This step neither needs nor assumes a complete one-triplet low band. It would be invalid to use the even second-level cutoff without first proving parity preservation through the Bogoliubov transformation; that obligation is explicitly discharged here.

## 4. Continuous endpoint bounds

Let S=Σe we² and C=3S/16. Rationalization, including the continuous value at g=0, gives

\[
E_b+q\delta=C(2g-1)+(C+q)\sqrt{1-4g}.
\]

The main seed graphs have S=2N. The second derivative after subtracting the affine ρ is

\[
\frac{d^2}{dg^2}[E_b+q\delta-\rho]
=-\frac{4(C+q)}{(1-4g)^{3/2}}<0.
\]

A concave function on [a,b] is at least the lesser endpoint value. At each endpoint, the auditor independently verifies the 60-decimal downward square root by integer-square inequalities. Since C+q>0, substitution is in the correct lower-bound direction. Hence the saved mq are valid uniform lower bounds for Eb+qδ−ρ, q=1,…,N. The exact minima are reproduced.

Both m1 and m2 are positive for every denominator patch and interval. Across all intervals the smallest identification margin exceeds .832669798231 and the smallest even Temple denominator exceeds 1.681197935655. With Vmax the larger residual endpoint value, w=Vmax/m2 bounds the Temple width uniformly, so λ1(H′(g))≥ρ(g)−w.

There is no assumption that the physical gap itself is monotone in g.

## 5. Correct full-space trace counting

The equal-frequency reference shell has bosonic multiplicity

\[
d_q=\binom{3N+q-1}{q}.
\]

These are not the hard-core physical shell multiplicities binom(N,q)3^q. After improving the single physical ground level by Temple, all remaining physical indices are still bounded by the ordered reference list beginning at q=1. Moreover

\[
\sum_{q=0}^N d_q=\binom{4N}{N}\ge4^N.
\]

One justification of the last inequality is the injection of the original hard-core basis into original boson sectors q≤N. No statement that the Bogoliubov-transformed physical subspace lies in transformed sectors q≤N is made. Only the dimension of the sorted reference list is relevant. Including all entries through shell N overcounts the needed tail by positive terms and is safe.

Therefore for every g in the interval,

\[
e^{\beta\rho(g)}Z'_N(\beta,g)
\le e^{\beta w}+\sum_{q=1}^N d_q e^{-\beta m_q}=U_N(\beta).
\]

The audit checks every multiplicity, complete count, q=1 starting point, and single retained level. No omitted excited level is silently removed. The largest patch requires only the Rayleigh/Jensen lower bound Z′M(2β,g)≥exp[−2βρM(g)]. It need not have an independently identified ground state for that use.

The independent exponential enclosure uses 112 Taylor terms, reduction to absolute argument at most 1/16, a geometric positive remainder, and 512-bit directed arithmetic in every term and squaring. Negative arguments use reciprocal interval bounds. This differs from the producer's 70-term, 256-bit routine. Each saved ground, tail and trace upper bound encloses the independently computed tighter upper bound. The final 18-decimal ratio endpoints agree exactly.

## 6. Shared-parameter energy cancellation and t–x–y transport

Let S,T,M denote the 16-, 32-, 64-rung patches. The relevant exponents are

\[
h_1=8\rho_S-2\rho_M,\quad h_2=16\rho_S-4\rho_M,
\quad h_0=4\rho_T-2\rho_M.
\]

All are affine in the same g. Their uniform minima are computed as joint endpoint values. The physical −3N/4 energy shifts cancel identically in each combination; the audit checks these cancellations. Independent worst-case bounds on the extensive energies are not substituted.

At initial base (4,4,β), the t–x–y path visits (4,4,2β), (8,4,2β), (8,8,2β). The trace bounds give

\[
J_1\ge e^{\beta\min h_1}/U_S(\beta)^8,
\quad J_2\ge e^{\beta\min h_2}/U_S(2\beta)^8,
\quad C_0\ge e^{\beta\min h_0}/U_T(2\beta)^2.
\]

The inherited purification algebra uses G(z)=1−(1−z)²/(2z²) and produces at common post-cycle base (8,8,2β)

\[
a=G(J_1),\quad b=G(J_2a),\quad c=G(C_0^4a^2b),
\]

with directed rounding. All three are checked in (0,1]. G is increasing there, so lower endpoints are valid inputs.

For adjacent directions, exact partition-function cancellation gives ec²=ba². Since both swapped purities are at most one, the lower pair (a,b) transports to (a√b,a²b). Swapping t past x and then y therefore gives the canonical x–y–t lower triple

\[
(A,B,C)=(a\sqrt b,\ a^2b\sqrt c,\ a^4b^2c).
\]

The base remains (8,8,2β). The audit reconstructs all directed square roots and all transported entries. No spatial length is identified with inverse temperature.

## 7. Canonical recurrence and every integer size

The canonical sequential update rotates the triple after replacing the first purity by a downward bound G(A⁴B²C). The next update uses the already updated entry. The audit exactly reproduces every saved update, base size and temperature, not a simultaneous-update approximation. There are 30 complete three-direction rounds across the 16 interval certificates.

At the accepted common defect u≤1/500, the inherited signed-transfer theorem gives every integer square side at least n a unique ground state and gap at least log[1/(32u)]/βaccepted. Every saved rational gap d is accepted by the independent exact inequality

\[
e^{\beta_{\rm accepted}d}\,32u<1.
\]

No floating logarithm enters acceptance. Endpoint constants for the quadratic contraction and two successive integer-size interpolation steps are checked again with exact fractions.

Before that asymptotic onset, the auditor independently reconstructs all 46 saved signed-transfer finite-window witnesses, including inverse-purity dominant weights, signed-tail ratios, both one-dimensional interpolation calls and the final lower thermal purity C*. Every window gap d is accepted by exp(βd)(1−C*)<C*. The required windows cover consecutive boxes [8·2^j,16·2^j], including odd integer side lengths.

For L=2,…,7, it independently constructs the periodic graph and computes the exact edge-square sums 16,18,32,50,72,98. The singlet product has H′ Rayleigh energy zero. The global comparison λ2(H′)≥Eb+δ and

\[
\frac{d}{dg}(E_b+\delta)
=2C-\frac{2(C+1)}{\sqrt{1-4g}}<0
\]

show that the upper coupling endpoint supplies a uniform short-size gap lower bound. All 96 short-size rows pass, including length-two parallel multiplicities. At g=.07 their minimum exceeds .637732662587.

The weakest interval is [11/160,7/100]=[.06875,.07]. Its accepted asymptotic side is 1024. Seven required finite windows start at 8,16,32,64,128,256,512; their minimum is .002703641449, above the final uniform bound. An extra [1024,2048] window is checked but is not needed. Thus short sizes, finite windows, and the asymptotic theorem leave no unproved integer size.

Finally, the 16 closed rational intervals meet exactly, start at 0 and end at 7/100. The audit checks every endpoint equality and takes the minimum of each interval's verified all-size gap. This establishes the simultaneous coupling-and-size claim in the verdict.

## 8. Reproduction and outputs

Run `bash REPRODUCE.sh`. The script verifies frozen provenance, rebuilds physical polynomial matrices, replays every interval and bridge, and writes only this separate review directory. It pins one CPU, sets BLAS/OpenMP threads to one and caps address space at 1 GiB, below the requested 1.5 GiB. The full acceptance run takes about nine seconds and about 25 MiB RSS in this environment. Timings are diagnostic only.

- `results/SUMMARY.json`: accepted uniform claim and all 16 detailed interval outcomes
- `results/matrix_reconstruction.json`: Gram, first-moment and complete second-moment equality checks
- `results/local_parity.json`: independently rebuilt physical exchange parity test
- `audit_interval.py`: independent acceptance implementation
- `test_rejection_guards.py`: eleven in-memory corrupted certificates, each rejected, covering incorrect normalization, residuals, Temple cutoff, tail counting, energy correlation, transport, size coverage and gap inflation
- `PRODUCER_FREEZE.json`, `INPUT_SHA256.json`, `INHERITED_REVIEWS.json`: exact provenance
- `MANIFEST_SHA256.json`: this completed review's seal

The analysis and all physical-input roles are explicit. The only inherited dependencies are the already independently reviewed geometry and general transfer/comparison/interpolation theorems; the new polynomial, parity, continuous-interval and numerical acceptance obligations are discharged here.
