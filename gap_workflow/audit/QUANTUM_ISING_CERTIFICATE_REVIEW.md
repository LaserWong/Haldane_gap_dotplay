# Independent review: periodic quantum Ising seeds and gap certificate

Reviewed 2026-10-14. Scope: the Pauli-normalized periodic family
H_L = -J sum_i Z_i Z_(i+1) - h sum_i X_i, with J>=0, real h, and every
integer L>=2. The L=2 positive-direction convention includes two bonds.

## Verdict

**PASS for the exact finite partition enclosures and the reviewed composed
mathematical theorem.** The target J=1, h=3/2, n=16, beta=8 supplies the exact
rational bootstrap lower bound 121183565803/250000000000 = 0.484734263212.
The dedicated bootstrap theorem covers every integer L>=16. The separately
reviewed analytic paramagnetic comparison covers all L>=2, including odd
lengths, with gap>=1. Consequently the weaker bootstrap-derived bound extends
to every integer L>=2 by an explicit small-size bridge. The stronger bound 1
is already available independently from integrability; this is a validation of
the partition-seed/bootstrap route, not a new Ising gap discovery.

This verdict is a mathematical/code review, not proof-assistant verification.
The callable scalar adapter correctly retains VERIFIED_CONDITIONAL and false
physical/uniform flags: its input declarations are not authenticated proofs.
Those conservative API flags must not be confused with the separately reviewed
composition of model, arithmetic, interpolation and bridge in this report.

## Analytic checks

### Parity, normalization and odd lengths

The spin rotation and Jordan-Wigner transform give NS momenta in the physical
even-fermion sector and R momenta in the physical odd sector. Bogoliubov paired
modes preserve parity. For g=|h|, the unpaired zero-mode coefficient is g-J,
while the pi coefficient is g+J. The NS vacuum is even. For g>J the R vacuum is
even and the physical R projection selects odd occupation; for g<J its vacuum
parity reverses and the projection selects even occupation. At g=J the zero
mode makes both projections equal. Odd L moves the pi mode from R to NS and
does not change this reasoning. The g=J=0 limit gives 2^L correctly.

The E/O updates are simultaneous and count each occupation monomial once.
Multiplying by exp(beta sum epsilon/2) restores the vacuum contribution. This
proves the trace formula across both phases without subtractive cancellation.
There are L modes per sector, not only the positive momenta. The L=2 formula
matches the doubled-bond Hamiltonian. No many-body truncation enters a seed.

### Exact enclosure arithmetic

Integer floor/ceiling division in box is outward for either endpoint sign.
Taking all four endpoint products is correct for sign-changing intervals.
The reciprocal endpoints are correctly ordered for either strictly positive
or strictly negative denominators; a denominator containing zero is rejected.
For rational x>=0, isqrt(floor(x D^2)) equals floor(D sqrt(x)); the upper-end
square comparison adds exactly the needed unit. The half-angle cosine
recursion reduces p after exact periodic/reflection reductions, selects the
positive root only for angles in [0,pi/2], and treats endpoints exactly.

For 0<=r<=1/2 the positive Taylor remainder is bounded by twice the next term.
The code's degree loop uses exactly 2*(1/2)^(N+1)/(N+1)!<=1/D. Outward term
recurrence preserves lower partial sums and upper omitted terms. Squaring
nonnegative intervals undoes range reduction; reciprocal handles negative
arguments and monotonicity handles interval arguments. Large exponential
intervals can be broad or underflow to a rational lower endpoint of zero;
that is a precision/resource limitation, not an invalid enclosure.

The rational shift C is identical in all three traces. Both exponents cancel
algebraically in B/A^2 and C_trace/B^2. Choosing a midpoint of a vacuum-density
enclosure is legitimate: the shift need not equal the exact vacuum density.
Dependency loss only widens intervals. Endpoint division supplies rigorous
lower purities. No floating value participates in the proof path.

### Physical transfers and dedicated bootstrap provenance

The bond -J Z tensor Z has a real identical-factor witness with coefficient
J>=0, and onsite -hX is real symmetric. The family is homogeneous, local and
periodic with the specified multiplicities. The exact continuous-time history
construction therefore supplies a selfadjoint Hilbert-Schmidt transfer with
Z_L(beta)=Tr X_beta^L for every integer L>=2; this includes positive odd traces.
See [transfer eligibility](../theory/TRANSFER_ELIGIBILITY.md).

The repository's `seed_size/proofs/DERIVATIONS.md`, Section 2, supplies K=5
contraction (in fact on a larger region); `two_d_theory/THEORY.md`, Sections
2.1 and 4, supplies exact history transfer and signed all-integer 1D
interpolation. These source files were independently read in the restored
checkpoint and its English edition. They are distinct from this workflow's
own `theory/THEORY.md` and should not be confused by basename.

For u<=1/100 the exact first-step coefficient
(3-3u+u^2)^2/[2(1-u)^6] and second-step coefficient
(2+5u)^2/[2(1-(2+5u)u)^2] are both <5. Their monotone upper bounds at 1/100
were checked rationally. Thus u_j<=(5u_0)^(2^j)/5. Signed interpolation uses
the unique dominant absolute transfer eigenvalue, whose sign must be positive
because all sufficiently large odd physical traces are positive. Its tail
bound and Holder interpolation give thermal purity >=1-4u on every integer
n<=L<=2n. The endpoint constants satisfy
3/2+5u+2/(1-2u)<4 and 4/(1-4u)<5. Hence uniqueness and
exp(-beta Delta_L)<=5u hold. Dyadic windows cover every L>=n, with the same
lower gap log(1/(5u_0))/beta_0. This is not merely a dyadic-length claim.
The positive atanh partial series used by log_lower gives a genuine lower
logarithm, including its exact power-of-two range reduction.

### Independent all-size analytic bridge

For g>J, omega(k)=sqrt(g^2+J^2-2gJ cos k) is analytic in a nonzero strip, so
its Fourier series is absolutely convergent. The Laplace representation of
sqrt(x), followed by subtracting the k-independent term, justifies exchanging
the integral and nonconstant Fourier coefficient. The modified-Bessel series
has nonnegative terms, making every nonconstant omega Fourier coefficient
nonpositive. Near zero the integrand is O(t^(|m|-3/2)); at infinity g>J gives
exponential decay. For J=0 those coefficients vanish directly.

Sampling NS versus R gives sum_NS omega - sum_R omega =
-4L sum_(q positive odd) omega_hat(qL)>=0, with the sign and factor four
correct. Therefore E_R,vac>=E_NS,vac. The NS vacuum is physical and all other
NS states cost at least 4(g-J); every physical R state has odd occupation and
costs at least 2(g-J) above its vacuum. The ground is unique and every gap is
at least 2(g-J). This proof includes every integer L>=2 and cannot be carried
to g<J, where the R parity selection changes. It supplies the required early
window bridge without ED or a numerical extrapolation.

## Independent diagnostics and reproducibility

Run from the workflow root:

    OPENBLAS_NUM_THREADS=1 PYTHONPATH=. python audit/check_quantum_ising_certificate_independent.py

Results: [JSON](quantum_ising_certificate_independent_results.json).

- 4 exact rational square-root endpoint tests.
- 4 independent unrounded Taylor/geometric-tail containment tests.
- 1,008 200-digit diagnostics across every allowed dyadic angle, extreme
  exponent inputs, hyperbolic-product target traces/purities, and both shift
  cancellation ratios.
- 224 independently assembled spin-basis trace comparisons for L=2..8,
  eight parameter choices and four temperatures; maximum log Z error
  3.2685e-13.
- 28 ED gap comparisons with the paramagnetic analytic bridge; minimum
  numerical margin -8.89e-15, consistent with binary64 eigensolver roundoff.
- 4 tampered scalar-label/bound rejections, 9 malformed parameter rejections,
  and 4 resource/singular-division rejections.

The production interval module is called to obtain enclosures, but the
200-digit comparator uses the algebraically different hyperbolic product
formula, and ED constructs the spin matrix without the fermion transform.
These numerical comparisons are diagnostics, not exact proof. The proof
review of the enclosure algorithm above is separate from them. The JSON
records SHA256 of reviewed source snapshots to make later changes visible.

## Limits and requested cleanup

1. The interval note initially attributed signed interpolation to
   TRANSFER_ELIGIBILITY.md alone. That attribution must instead include the
   exact Section 4 theorem identified above. The finite enclosure result
   itself is unaffected. The numerical seed note's remaining-proof checklist
   should acknowledge the now-completed interval implementation and review.
2. There is no serialized quantum-seed verifier: mutating stored numerical
   lower bounds cannot be detected by scalar replay alone. A deliberately
   changed valid-in-range lower bound remains only conditional, with physical
   and uniform flags false. Recompute the seed and compare source/artifact
   identity for trusted reuse. Never promote proof-declaration strings into
   verified physical evidence.
3. shifted_partition accepts optional ctx/modes as a trusted internal reuse
   interface and does not authenticate custom mode lists. canonical_seed_interval
   generates its own validated modes and does not expose that injection route.
   Do not present the lower-level custom-mode API as an untrusted-input verifier.
4. Caps bound length, decimal precision and exponent magnitude; they are not a
   complete wall-time/memory admission system for arbitrarily large rational
   strings. This is a callable research backend, not a hardened remote service.
5. Precision failures, failed recurrence admission and resource rejection are
   not exclusions and never prove gaplessness. The exact backend accepts
   dyadic finite seed lengths only; all-integer family coverage comes from
   the reviewed theorem, not from calling it at odd sizes.
