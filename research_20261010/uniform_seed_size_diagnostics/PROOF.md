# Uniform spin-one minimum-seed diagnostics

Updated 10 October 2026, 17:08 America/New_York (EDT) / 21:08 UTC.
Producer exact certificate; independent review remains pending.

## Result and its deliberately limited scope

For the uniform, periodic, unit-coupling spin-one Heisenberg chain,

    H_n = sum_(j=0)^(n-1) S_j · S_(j+1 mod n),

all inverse temperatures beta >= 0 are excluded for the explicitly specified
one-D26-Rayleigh thermal-first scalar recipe at denominator sizes
n = 6, 8, 10, 12. This is not a claim that the physical gap vanishes, that
small MPS descriptions are impossible, or that every bootstrap recipe fails.
It does not establish an absolute minimal seed or certify n=14. Only the
listed sizes, numerator witness and recursions are covered.

The n=6/8 conclusion is re-established using the accepted joint-aware conversion;
it is not inherited from the obsolete product-only conversion argument.
For n=10/12, a lower denominator trace from four orthogonal rational trial
states proves failure of the very first scalar update. Even two of those
states suffice, with a weaker but still obstructive bound.

| Denominator n | Numerator length | Denominator witnesses | Exact global upper cap on attainable J lower bound | Failure |
|---|---:|---:|---:|---|
| 6 | 12 | 1 | 29/50 | Every legal delayed joint-aware conversion fails |
| 8 | 16 | 1 | 71/100 | Every legal delayed joint-aware conversion fails |
| 10 | 20 | 4 (2 already suffice) | 3/25 | First G is negative |
| 12 | 24 | 4 (2 already suffice) | 19/100 | First G is negative |

The cap for two states at either n=10 or n=12 is 3/10. These caps are rigorous
convenient endpoints, not numerical optima.

## 1. Fixed numerator and inherited premises

Write Z_n(beta)=Tr exp(-beta H_n), with no energy shift. An extensive shift
cancels out of every ratio below. Let R_n be the exact Rayleigh quotient of
the archived D=26 periodic MPS at length 2n. This recipe fixes its lower
numerator as

    L(beta) = exp(-2 beta R_n).

It does not replace L by the true large-system trace or by several states.
For arbitrary valid upper denominator certificates U0 >= Z_n(beta) and
U1 >= Z_n(2 beta), set

    J_lo = L/U0^4,       C_lo = L/U1^2,
    G(x) = 1 - (1-x)^2/(2x^2),
    a = G(J_lo),         b = G(C_lo^2 a).

The positive pair a,b is a time-first ladder at (2n,2 beta). A nonpositive
update cannot be reused. The inherited transfer identification and G
purification theorem, including their even-base conditions, remain premises.
The present result is in fact an obstruction to this numerical recipe
regardless of whether those inherited premises are applied elsewhere.

The archived exact block file and builder identification are hash-checked.
Fresh integer GMP contractions at lengths 12,16,20,24 use

    R_n = 2n Tr(T^(2n-2) O) / Tr(T^(2n)).

All repeated 12/16/20 numerator and denominator integers agree exactly with
the frozen previous assessment. Length 24 is new. The identification of T
and O with the physical MPS norm and bond insertion is inherited from the
archived audited construction; the original manuscript PDF is not present
and has not been read. This does not introduce a physical 676-state trial
space: the norm transfer has auxiliary dimension 26^2=676, largest archived
block 162; the physical numerator contains one fixed state.

Exact rational R_n values are in mps_lengths.out and
uniform_seed_size_diagnostics.json. Decimal displays are:

| n | R_n, total numerator-chain energy |
|---:|---:|
| 6 | -16.869506681544223... |
| 8 | -22.446776199528074... |
| 10 | -28.040250648164623... |
| 12 | -33.640539741732766... |

## 2. What the lower denominator witnesses actually prove

For mutually orthonormal vectors v_i with alpha_i=<v_i,H_n v_i>, scalar
convexity applied to the spectral measure of each v_i gives

    Z_n(beta) >= sum_i exp(-beta alpha_i).

No v_i is asserted to be an exact eigenvector. Integer vectors are normalized
only conceptually; the exact ratios divide the integer quadratic form by the
integer norm square. Orthogonality is checked before this trace inequality
is used. It cannot be inferred from distinct rounded Ritz values.

Every bond has trace zero, so Tr H_n=0 and, with D=3^n,

    Z_n(beta) >= D.

There is also a complementary-subspace Jensen refinement. Complete the r
trial vectors to an orthonormal basis. The sum of all remaining diagonal
energies is -sum_i alpha_i. Therefore

    Z_n(beta) >= sum_i exp(-beta alpha_i)
                + (D-r) exp(beta sum_i alpha_i/(D-r)).

The verifier records exact lower estimates from this refinement at six
sample temperatures. The exclusion needs only the simpler trial sum and
ordinary Tr H_n=0 bound, so does not depend on those sample temperatures.

Let alpha_0 be the first trial energy and define

    delta = R_n - 2 alpha_0 > 0,
    g_i = alpha_i-alpha_0 > 0,  i>0.

For this fixed lower numerator and any valid upper denominators,

    J_lo <= exp(-2 beta delta)/(1+sum_(i>0)exp(-beta g_i))^4,
    C_lo <= exp(-2 beta delta)/(1+sum_(i>0)exp(-2 beta g_i))^2.

These are upper bounds on what the specified certification inputs can
achieve. They are not upper bounds on the true physical ratios obtained by
substituting a lower numerator into a quotient.

## 3. Exact physical vectors and Hamiltonian actions

For n=6/8 the frozen integer Sz=0 vectors are rechecked, including their full
Hamiltonian actions. For n=10/12, only two new sparse extremal-vector proposals
are made at each size, separately in Sz=0 and Sz=1. Each call asks for k=1,
never a full spectrum, and has a hard 300-CPU-second cap, one pinned CPU and
1 GiB address-space cap. Floating energies are proposal metadata only.

Round to integers and project the Sz=0 proposal to translation eigenvalue +1
and the Sz=1 proposal to translation eigenvalue -1. The projection is a finite
integer sum of translated coefficients. Generate two more integer vectors by
spin flip (Sz=-1), and by total lowering divided by sqrt(2) (Sz=0). The latter
scalar is irrelevant after normalization. The four vectors are orthogonal:
separate Sz sectors are disjoint, and the two Sz=0 vectors have opposite exact
translation eigenvalues. Their cross inner product is also checked as the
integer zero. A nonzero norm is checked for every vector.

The rounded vectors are not assumed to have exact total spin one or zero.
In particular, the lowered vector's Rayleigh energy is recomputed and is not
silently copied from its parent.

The physical basis uses base-three digits 0,1,2 for m=-1,0,1. For each bond,
H has diagonal m_j m_(j+1) and coefficient 1 on each allowed transition
(m_j,m_(j+1))->(m_j+/-1,m_(j+1)-/+1). The coefficient is exactly one because
(1/2)sqrt(2)sqrt(2)=1. The verifier independently reconstructs the entire
integer H-applied vector, not just its returning support. It checks integer
range bounds before using int64 action buffers; all norms and quadratic-form
sums use arbitrary-precision Python integers.

| n | Witness | Nonzero trial support | Full H-action support |
|---:|---|---:|---:|
| 6 | Archived Sz=0 | 141 | 141 |
| 8 | Archived Sz=0 | 1,107 | 1,107 |
| 10 | Sz=0, momentum 0 | 8,953 | 8,953 |
| 10 | Sz=1, momentum pi | 8,350 | 8,350 |
| 10 | Sz=-1, spin flip | 8,350 | 8,350 |
| 10 | Sz=0, lowered momentum pi | 8,502 | 8,662 |
| 12 | Sz=0, momentum 0 | 73,693 | 73,765 |
| 12 | Sz=1, momentum pi | 69,504 | 69,576 |
| 12 | Sz=-1, spin flip | 69,504 | 69,576 |
| 12 | Sz=0, lowered momentum pi | 71,512 | 72,628 |

The full n=10/n=12 Sz=0 block dimensions are 8,953/73,789; the Sz=1 dimensions
are 8,350/69,576. The full physical Hilbert dimensions are 59,049/531,441.
The denominator trial span is four-dimensional, while two explicitly saved
coefficient vectors generate it using the stated symmetries. Neither number
is the MPS bond dimension. The largest numerator physical dimension is
3^24=282,429,536,481; that physical matrix and its explicit MPS coefficient
support are never formed.

The exact energies and norms are in exact_trial_data.json. Useful displays:

| n | alpha_0 | First Sz=1 energy | delta |
|---:|---:|---:|---:|
| 10 | -14.094129954931903... | -13.569322004518533... | 0.14800926169918177... |
| 12 | -16.86955613946792... | -16.385359669556212... | 0.09857253720308078... |

## 4. n=6/8 with the new joint-aware conversion

First reconstruct the previous global J caps using exact inequalities:

- n=6: split beta at 3/4, yielding J_lo<29/50.
- n=8: split beta at 31/40, yielding J_lo<71/100.

Below each split use exp(-2 beta R_n)/3^(4n), increasing with beta; above
it use exp(-2 beta delta), decreasing with beta.

If beta<=1/2, trace Jensen directly gives J_lo<2/5, and G(2/5)=-1/8.
If beta>=1/2, C_lo<=exp(-delta)<4/5. The joint-aware test therefore uses the
optimistic upper pair

    a_bar=G(J_cap),     b_bar=G((4/5)^2 a_bar),

with safe upward rounding. This stronger joint envelope is essential; an
old product-only obstruction is not transferred automatically.

For a positive time-first pair a,b at its current base, the accepted conversion
has component lower endpoints s=a sqrt(b), t=a^2 b and a separate joint lower
endpoint K=a^2 b. The first canonical cycle is

    s_new=G(max(s^2 t,K)),
    t_new=G(max(t,K)^2 s_new).

The old K is then discarded at the new base; later cycles use their new
component product. We bound this exact recipe above, not below, using
monotonicity of G and an upward square-root enclosure. A negative upper
endpoint proves failure of every less optimistic input.

The exact finite failure witnesses are:

- n=6, no extra time-first cycle: first canonical spatial update is negative.
  Continuing time-first instead already fails on its next first direction.
- n=8, no extra time-first cycle: first canonical thermal update is negative.
- n=8, one extra positive time-first cycle: first canonical spatial update is
  negative. The following time-first cycle fails before another conversion.

Every legal fixed time-first delay has thus been checked. At every preceding
positive state at least one upper component is below 99/100, so none has
already reached the accepted common small-defect region. This scope does not
cover arbitrary adaptive switching with new inequalities or independently
propagated information at later bases.

## 5. n=10/12 exact hot/box/cold covering

For beta in [0,1/2], use

    J_lo <= exp(-R_n)/3^(4n).

For beta>=10, use J_lo<=exp(-20 delta). For the warm range, use the 38 closed
boxes [i/4,(i+1)/4], i=2,...,39. On a box [l,h], positivity of delta and g_i
proves

    J_lo <= exp(-2l delta)/(1+sum_(i>0)exp(-h g_i))^4.

The exact verifier encloses the numerator exponential upward and each
positive denominator exponential downward. These boxes join without gaps
and cover [1/2,10]. Every hot, warm and cold bound is strictly below 3/25 for
n=10, or 19/100 for n=12. The largest warm-box bounds, displayed only, are
0.1138414784449191 and 0.1801389902342928 respectively.

Both G(3/25) and G(19/100) are negative. Thus no later conversion, including
the new joint-aware one, is even reached. Repeating the same covering with
only alpha_0 and the Sz=1 witness gives J_lo<3/10 for both n values.
This two-state version also fails the initial G and needs no spin-flip or
lowering premise. Four states are retained in the stronger recorded estimate.

The all-temperature conclusion is a finite rational certificate covering an
unbounded beta interval, not a bounded numerical scan. The small positive
delta is a finite-size/numerator mismatch, and the low excited witnesses
supply a warm-temperature denominator obstruction. Neither is a proof of a
physical gap upper or lower bound.

## 6. Directed arithmetic and reproduction

exp_i first reduces nonnegative rational x to x<=1/16, uses Taylor terms
through degree 40, and bounds the remaining positive series by

    next_term/(1-x/42).

It rounds both endpoints outward to a 160-bit dyadic grid, squares outward
back to the original argument, and handles negative x by outward reciprocal
intervals. Rational comparisons, not displayed decimals, establish every
margin. Square roots used in n=6/8 transport are upper-enclosed using integer
square roots and checked by exact squaring.

Run bash REPRODUCE.sh. It verifies INPUT_MANIFEST_SHA256.json, compiles the
small GMP contraction, recomputes all four MPS Rayleigh quotients, then runs
exact physical-vector and scalar verifiers. No eigensolver is imported in
this replay. Python, NumPy, a C++ compiler and GMP development libraries are
required. propose_trials.py is optional provenance, never a verification
prerequisite. Its saved compressed JSON files contain every integer
coefficient; derived vectors have unambiguous exact constructions.

Replay rewrites local result files and resource metadata. Preserve a sealed
copy before replay if byte-for-byte timing metadata matters. All writes stay
inside this new directory. No frozen source, root index or GitHub item is
edited. This extracted workspace has no Git metadata.

Observed proposal peaks were at most 87,444 KiB. The exact trial verifier
used about 42 MiB and approximately one CPU second; the scalar covering used
about 12 MiB and approximately three CPU seconds. The contraction resources
are recorded separately in mps_resources.json. Every proposal was under the
hard 300-CPU-second cap; one n=10 proposal had a longer wall-clock scheduling
delay, which is not being reported as CPU time.

## 7. Next-size estimate, not a new computation

No n>=14 support has been generated. next_size_cost_estimate.json contains
an analytic n=14 estimate from trinomial coefficient counts: Sz=0/Sz=1 have
616,227/585,690 basis states and at most 8,644,667/8,179,822 stored CSR entries.
Float64/int32 CSR storage is about 101/96 MiB and 20 Lanczos vectors add about
94/89 MiB. Temporary COO arrays and mapping buffers may bring the peak to
350-650 MiB. A preliminary 15-120 CPU-second range is an estimate, not a
resource guarantee or authorization to extend this task. The same hard
one-CPU, 1-GiB, 300-CPU-second limits would still be required.

Whether n=14 passes any useful recipe, whether better numerator witnesses
help, and how to obtain the required upper denominator traces are open.
These lower-trace diagnostics deliberately avoid spending on that upper-tail
certification until the fixed numerator/seed pair survives a necessary test.
