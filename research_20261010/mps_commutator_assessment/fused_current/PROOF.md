# Fused range-two current contractions at momentum pi

## Result

The exact n24 pi-only two-vector span improves the trial energy difference
relative to psi24 from0.4910226054728026 to0.4238202243082572. An explicit
integer direction is(-1000000000000,259782703769) in the(v,w) basis below.
The exact Gram-orthogonal second direction has difference3.8268850622358066.
All figures here are decimal displays of saved exact rational numbers.

Replacing the old pi triplet in the reviewed70-state lower trace closes the
previous unresolved beta interval[539/64,339/32]: every beta>=0 is excluded
for the fixed D26 length48 single-Rayleigh numerator and the specified
thermal-first / delayed joint-aware canonical recipes. Adding the second
triplet gives73 states and the same all-beta conclusion. These lower traces
upper-bound what that certificate can attain with any valid denominator
upper traces. The conclusion is neither a physical-gap statement nor a
universal seed-size barrier. It does not exclude other finite-window lemmas,
transport formulas, initialization choices, or other uses of these inputs.
Earlier unresolved windows remain immutable records of weaker screens.

The complete n24 campaign used795.063106 CPU seconds on one core, with
peak273096KiB, within the authorized2400CPU-second /700MiB gate.
Independent review is separate from this producer certificate.

## Scope and state definitions

The target is the same fixed archived D26 state psi24 for the uniform,
periodic, unit-coupling spin-one Heisenberg chain. Define R_j=S_j^+/sqrt2,
M_j=Sz_j,

    A_pi=sum_j (-1)^j R_j,
    J_j=R_j M_(j+1)-M_j R_(j+1),
    v=A_pi psi24,
    w=[H,A_pi]psi24=2 sum_j (-1)^j J_j psi24.

The identity is exact and was verified as an integer local operator in the
sealed tiny assessment. In particular, w is not replaced by(H-<H>)v. The
distinction matters because psi24 has not been assumed to be an H eigenstate.

Only the two-vector pi space is optimized. The necessary displacement data
are collected to form its Gram/H entries; this campaign does not optimize
all momenta or repeat multiple large-n variants.

## Fusing overlapping source words into cells

The local current word tensor is Gamma_st=m_t B_s A_t-m_s A_s B_t, with
B_s=A_(s-1) and B_-1=0. Two-site current words on bra and ket are fused into
one cell whenever they overlap. The nine cells are:

- ordinary one-site cell
- one-site bra raising source
- two-site bra current, ket current, or coincident bra/ket currents
- two-site ket current with the bra raising source on either endpoint
- three-site overlapping currents with either bra-first or ket-first order

At displacement n-1, the cut is rotated to n-1 so the wrapping source becomes
an ordinary cell in cyclic order. Translation invariance of the trace state
justifies this rotation. It introduces no Fourier sign into the fixed-source
correlator. The final staggered sum still uses the original displacement r.

For each cell B, build its physical bra and ket word tensors first. Exact
physical sums then give auxiliary transfer matrices for:

    E_B(identity), Q_B(open internal H),
    E_B(first M/R/L), E_B(last M/R/L).

The largest cell has physical dimension27. These are local construction
matrices, not an expansion of the24-site physical support. Every nonzero
virtual matrix entry is checked against its charge shift. All local entries
are smaller than2^63 in absolute value; the cached engine uses signed64-bit
sparse values and arbitrary-precision GMP accumulated entries.

## Exact Hamiltonian accumulation and the periodic seam

For a prefix of cells retain its ordinary product P and open-H sum Q. Let
T_a denote the product with X_a on its last physical site, and U_a the product
with Y_a on its first physical site, where

    (X_a,Y_a)=(M,M),(R,L),(L,R).

Appending a cell B gives

    P'=P E_B,
    Q'=Q E_B+P Q_B+sum_a T_a E_B(Y_a at first site),
    T_a'=P E_B(X_a at last site),
    U_a'=U_a E_B.

The first two terms in Q' preserve prior bonds and add bonds internal to B;
the third adds exactly the bond crossing the cell boundary. At the final
cell, the periodic seam is

    sum_a Tr[U_a(previous prefix) E_B(X_a at last site)].

Adding it to Tr Q gives the full periodic H form. This explicitly includes
all source/H overlaps and wrapping current paths. The fused engine handles
n>=4; separate direct physical n2 fixtures handle the doubled-bond convention.

The cached version advances a common bra-source prefix once as the ket-current
position moves. Each evaluation copies that exact prefix, inserts the ket
cell, and closes its ordinary suffix. This changes multiplication reuse only.
It is checked byte-for-byte against the uncached engine and independently
against every direct physical C/K entry at n4 and n6.

## Reconstructing the exact two-vector forms

The saved fixed-source correlators are

    C_mix(r)=<R_0 psi,J_r psi>, K_mix(r)=<R_0 psi,H J_r psi>,
    C_jj(r)=<J_0 psi,J_r psi>, K_jj(r)=<J_0 psi,H J_r psi>.

All24 mixed displacements are computed. For the same-source pair, reality,
translation and Hermiticity give C_jj(r)=C_jj(n-r), K_jj(r)=K_jj(n-r), so13
independent displacements suffice. No reflection assumption is used.
With n=24, the forms for(v,w) are

    G00=||v||^2, H00=<v,Hv> from the frozen earlier contraction,
    G01=2n sum_r (-1)^r C_mix(r),
    H01=2n sum_r (-1)^r K_mix(r),
    G11=4n sum_r (-1)^r C_jj(r),
    H11=4n sum_r (-1)^r K_jj(r).

Both off-diagonal entries are real and symmetric. Positive G00 and detG are
checked before any generalized Rayleigh calculation. The quadratic roots of
det(H-lambda G) are enclosed by exact discriminant square-root intervals.
They describe compressed Rayleigh data, not physical eigenvalues.

The lower direction is rounded to an explicit integer coefficient pair u.
The second coefficient pair v_orth=(b,-a), with(a,b)=G u, is exactly
G-orthogonal to u. Their positive norms and exact rational Rayleigh quotients
are checked directly. Thus the trace witnesses do not depend on numerical
orthogonality or a floating generalized eigensolver.

## Exact cross-Gram sum rule

As a separate check, set L=R^dagger. The local identity

    [L_j-L_(j+1),J_j]=-2M_jM_(j+1)-L_jR_(j+1)-R_jL_(j+1)

gives the pi double commutator

    [A_pi^dagger,[H,A_pi]]
      =-2 sum_j [2M_jM_(j+1)+L_jR_(j+1)+R_jL_(j+1)].

The verified finite-n24 singlet implies isotropy, so its expectation is
-8<psi,Hpsi>/3. Reality and spin flip identify the two halves of this double
commutator with the same cross-Gram entry. Consequently3G01=-4<psi,Hpsi>.
The saved integers satisfy this identity exactly. This argument uses H spin
symmetry and the proven trial singlet, not an H-eigenstate assumption.

## Spin components, dimensions, and trace use

The separately certified n24 zero total-raising norm proves psi24 is an
exact singlet. Since total raising commutes with both H and A_pi, it also
annihilates w. Both basis vectors have Sz1 and momentum pi. Every combination
is therefore a highest-weight triplet vector. Normalized total lowering and
global spin flip supply its Sz0 and Sz-1 partners with identical Gram/H forms.
Two G-orthogonal combinations produce two mutually orthogonal triplets.

Replacing the prior pi triplet preserves a70-dimensional retained denominator
span. Retaining both orthogonal optimized pi triplets gives73 states. Other
momenta are taken unchanged from the frozen70-state certificate. The numerator
remains one fixed D26 state at48. The local pi linear search has dimension2;
a safe individual-state MPS bound is156 via the four-channel open current sum
plus two explicit wrapping terms. Those dimensions are not interchangeable.
The normalized lowered current also satisfies Lw=-[H,Z_pi]psi, where
Z_pi=sum(-1)^j Sz_j, because Lpsi=0 and[L,H]=0. Its local commutator is again
a two-term, two-site operator. Thus the same156 bound applies to the lowered
component; global spin flip preserves the bound for the opposite component.

The scalar verifier repeats the exact hot / closed-box / cold necessary test
for these two options. It certifies only the stated fixed-numerator,
thermal-first and delayed joint-aware recipes. No physical gap, physical
gaplessness, exact low eigenvalues, or universal minimum seed is inferred.

## Exact all-beta scalar coverage

Let alpha0 be the ground trial Rayleigh, R the fixed D26 Rayleigh at48,
delta=R-2alpha0>0, and g_i the energy differences of the orthogonal trial
states relative to psi24. Scalar Jensen on each orthonormal direction gives

    Z24(beta)>=exp(-beta alpha0) F(beta),
    F(beta)=1+sum_i m_i exp(-beta g_i).

With numerator L=exp(-2beta R), every valid pair of denominator upper traces
U0>=Z24(beta), U1>=Z24(2beta) obeys

    J=L/U0^4 <= exp(-2beta delta)/F(beta)^4,
    C=L/U1^2 <= exp(-2beta delta)/F(2beta)^2.

This is an upper bound on attainable certificate inputs, not an upper bound
on a true physical purity ratio. Positive gaps are upper-rounded and delta
is lower-rounded to64-bit dyadics; exponentials use160-bit outward intervals.
On each closed box[l,h], the numerator is evaluated at l and denominators at
h. This bounds the entire closed box, including endpoints.

The hot tail[0,1/2] uses Tr H=0 and Z>=3^24, with J<2.582e-17. The cold
tail[80,infinity) uses delta>0 and J<0.206. In both tails J<2/5 and G(2/5)<0.
All318 closed quarter-width boxes cover[1/2,80]. No refinement was needed.
For both retained spans,165 boxes fail the initial first G,104 the initial
second G,25 a continued time-first first G, and24 a continued second G.
At most two possible conversion delays require checking before the
continued upper orbit is nonpositive. The exact per-box histories and
rational signs are stored in pi_scalar_results.json.

Specifically G(x)=1-(1-x)^2/(2x^2), initial a=G(J), b=G(C^2 a), followed by
whole time-first cycles a'=G(a^2 b), b'=G(b^2 a'). At each fixed whole-cycle
delay, the canonical conversion starts S=a sqrt(b), T=K=a^2 b, then
S'=G(max(S^2 T,K)), T'=G(max(T,K)^2 S'); K is discarded after that cycle.
Upward rounding and monotonicity give an optimistic orbit. Every tested
conversion and every surviving whole-cycle delay fails; a finite replay
limit would instead be recorded inconclusive. No arbitrary adaptive
mid-cycle switching or new direct finite-window interpolation is covered.

## Cost authorization and recovery

The initial naive100-monomial route was projected at1,780 CPU seconds and
was not launched under the original600-second gate. The parent subsequently
authorized one pi-only n24 campaign up to2,400 CPU seconds /700MiB, with an
exact checkpoint. The optimized n12 benchmark used59.992 CPU seconds and
216.25MiB. A recorded conservative n24 projection was1,885.1944 CPU seconds
and432.5MiB. Only after that gate passed was the n24 campaign started.

`INPUT_MANIFEST_SHA256.json` freezes all physical computation inputs.
`run_n24_checkpointed.py` saves each complete C/K pair atomically and records
source hashes, attempts, resource use, and completion state. A normal interrupted
run can resume only unchanged inputs and within its remaining CPU budget.
An attempt with unknown CPU use requires a measured recovery decision rather
than an automatic retry. The complete n24 integer records are also published
as n24_exact.out. Independent review must use separate output files.
