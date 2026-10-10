# Nonperturbative MPS seeds: exact scope and bounded tests

Updated 2026-10-10 15:37 EDT / 19:37 UTC.

**Producer assessment and exact checks, awaiting a separate independent review.**
No root files or frozen inputs were changed. This shared snapshot has no `.git`
metadata. The original Haldane manuscript PDF is absent and was not read.

## Main conclusions

1. The largest-numerator-only **two-direction** ordering is mathematically
   available for the original uniform spin-1 and integer-spin-2 Heisenberg
   chains. It uses their physical spatial and inverse-temperature directions.
   I/P/C are boundary rotations, not those directions. This is an alternative
   untwisted space/time initialization, not a drop-in replacement for the
   original I/P/C moment-filter inputs. The reduction does not turn one MPS
   vector into a complete upper heat-trace certificate.
2. A new exact, inexpensive test rules out the specified one-D26-Rayleigh
   recipe at smaller seeds n=6 and n=8 **for every beta>0**, even if the
   denominator traces were supplied exactly. This is a limitation of these
   small seeds, this fixed numerator and this scalar recipe. It is not a
   limitation of all small MPS representations or all bootstrap methods.
3. A genuinely entangled, noncommuting AKLT parent provides a positive bounded
   example of a tiny MPS plus certified entire omitted spectrum: D=2, one
   retained vector, a four-site rational positivity test, and gap >=1/10 for
   every periodic L>=5. Its omitted state count is exactly 3^L-1. No large
   many-body spectrum or numerical Ritz assumption is used.
4. That AKLT example is **not** a new application of the current thermal
   spatial-transfer bootstrap: the existing same-real-factor sufficient
   condition fails, as an exact negative realignment witness demonstrates.
   Another thermal transfer proof or replacement spatial inequality would be
   needed. The AKLT MPS norm transfer is not a substitute for such a proof.

## 1. Three different notions of smallness

For a fixed periodic MPS psi(s_1,...,s_L)=Tr(A_s1 ... A_sL):

- D is the virtual matrix size. D does not count physical vectors or physical
  low eigenvalues. The family of D-bond MPS is generally nonlinear.
- Retaining that particular vector supplies one Rayleigh contribution to a
  heat-trace lower bound. Its linear span has dimension one.
- A linear variational search space of dimension k, a retained collection of
  r orthogonal trial vectors, and an MPS bond dimension D are independent
  quantities. None determines a complete low-band multiplicity by itself.
- An explicit product-basis expansion can have exponentially many entries
  despite D and the span dimension being fixed.

The archived uniform spin-1 witness has D=26. Its norm contraction has an
auxiliary 26^2=676-dimensional matrix (largest symmetry block 162), not a
676-dimensional physical trial space. At length 120 the full Hilbert dimension
is 3^120, while the witness's span is one-dimensional. The original route
already uses this single large entangled state rather than a full length-120
spectrum. It additionally needs the complete physical heat inputs at lengths
6,8,10 and the transfer/moment analysis.

The supported archived bound remains 0.005908566393 only for L>=1920, under
its inherited finite-input and analytic hypotheses. The original replay's JSON
labels its primary scope even; the later independently reconstructed bridge
explicitly incorporates signed-transfer interpolation to all integer L>=1920.
Neither statement fills the L<1920 range here. We do not improve that bound.

The analogous spin-2 witness has D=124 and one retained vector. The reviewed
finite witness lengths 128,256,512,1024 and positive leading spatial atom do
not constitute a uniform-gap certificate.

## 2. Precise transfer of the reduced-input ordering

For either uniform integer-spin Heisenberg model, use a consistently shifted
partition function Z_L(t)=Tr exp[-t(H_L+aL)]. The archived history construction
in `audit/APPENDIX_A_BRIDGE.md` and the integer-spin extension in
`../spin2_positivity_review/README.md` give a real self-adjoint Hilbert-Schmidt
operator X_t with Z_L(t)=Tr X_t^L for every integer L>=2. X_t need not be
positive. Fix an **even** n for the starting staircase. Then

    P_x(n,t) = Z_(2n)(t)/Z_n(t)^2 <= 1,
    P_t(n,t) = Z_n(2t)/Z_n(t)^2 <= 1.

The first inequality uses nonnegative weights lambda(X_t)^n; the second uses
positive Boltzmann weights. This is why arbitrary odd starting n cannot be
silently substituted, even though later signed-spectrum interpolation can
cover odd lengths.

For a time-then-space staircase at (n,beta), put

    J = Z_(2n)(2 beta)/Z_n(beta)^4,
    C = Z_(2n)(2 beta)/Z_n(2 beta)^2.

If rho_(2n) is the Rayleigh quotient of any normalized physical state, then
L=exp[-2 beta rho_(2n)] is a rigorous numerator lower bound (with the same
shift convention). With complete upper bounds U0>=Z_n(beta), U1>=Z_n(2 beta),

    J >= L/U0^4,       C >= L/U1^2.

Let G(z)=1-(1-z)^2/(2z^2). The ordered cycle gives

    a=G(J_lower),      b=G(C_lower^2 a).

These lower-bound P_t(2n,2 beta) and P_x(2n,4 beta), respectively. They are an
ordered staircase, not two purities at the same unlabelled point. Provided
all reused values are positive, conversion to canonical space,time at
(2n,2 beta) yields

    S=a sqrt(b),       T=a^2 b.

The inherited canonical cycle is S'=G(S^2 T), T'=G(T^2 S'). Its subsequent
all-integer interpolation assumptions and short-length bridge obligations are
unchanged. One may instead continue the time-first cyclic order before a
later conversion; our n=6/8 test below screens that fixed continuation too.

### What happens to I/P/C?

I (untwisted), P (pi seam rotation), C (2pi/3 seam rotation) label three
physical finite-volume Hamiltonians. Their character combinations give the
A4 spatial transfer sectors, conventionally called I,O,N in the spin-1 proof.
In particular, the letter C for a seam trace should not be confused with the
ratio C defined above. Neither the twists nor those representation sectors
are axes that can be permuted with beta.

Only untwisted traces are needed in the displayed two-direction formula.
Twisted traces may still be indispensable for **deriving useful upper bounds**
on the untwisted denominators through sector filters. The new ordering does
not delete their role in the old proof by relabelling them.

In particular, the original spin-1 cap proof bounds positive square filters
such as sum lambda^6(-2+10 lambda^2)^2, which contains a positive coefficient
of the tenth sector moment. That step needs the corresponding **upper**
moment/trace control. A single physical MPS gives a lower bound on an
untwisted partition function, not the missing upper tenth moment or separate
upper twisted/sector moments. No analogous reversal of inequality has been
proved. Therefore the new theorem alone does not justify deleting the
length-10 I/P/C computations from that existing proof. For spin-2 the same
warning applies to prospective high-order I/P/C moment filters. One must
actually build and certify the alternative two-temperature denominator
contract above, or prove a new sector-filter inequality.

### Exact remaining input

The bottleneck is a sufficiently sharp certified U0 and U1 at the **same
smaller physical size n**, at beta and 2 beta. A trace at beta is not a trace
at 2 beta. Ordinary cooling does give Z_n(2 beta)<=Z_n(beta)^2, but may be far
too loose. No ground Rayleigh value alone supplies either upper trace.
One needs full spectral counting/tails, direct validated heat traces, or
another rigorous trace-upper method. To start a cycle, at minimum J_lower
must exceed sqrt(2)-1 and C_lower^2 G(J_lower) must exceed sqrt(2)-1; successful
later recursion is a further condition.

For spin-2, the current D124 anchor supplies a lower numerator only at its
certified lengths; one cannot reinterpret the length-8 heat trace as a
length-64 denominator. Even-length moment extrapolation and cooling are legal
but are not currently a successful startup. A positive maximal-modulus atom
without a uniqueness/separation estimate supplies no missing heat tail.
The existing I/P moment counterexample retains its limited relaxation scope;
it is not a counterexample to every possible use of a full MPS numerator.

## 3. New exact uniform spin-1 startup exclusion

`mps_small.cpp` freshly contracts the archived exact D26 blocks at 12,16,20.
It inherits the independently audited identification of those blocks with the
physical MPS norm and Heisenberg insertion; their hashes and the builder hash
are checked against the original archive manifest. No 12-, 16-, or 20-site spectrum
is formed. Its length-12 and -16 energy/site results are respectively

    -1.4057922234620184...,
    -1.4029235124705046....

Their exact integer numerator/denominator pairs are in `mps_small.out`.
At n=6 and n=8, two small fixed integer vectors give exact Rayleigh quotients
alpha_n. They were proposed with a sparse one-eigenvector search but their
verification uses only integer Hamiltonian action; no numerical eigenvalue is
a premise. Their explicit S^z=0 support sizes are 141 and 1107. They are used
to demonstrate a denominator obstruction, not to certify a complete spectrum.

Write R=rho_(2n) for the unshifted total D26 energy and

    delta=R-2 alpha_n > 0.

Since Tr H_n=0 and the physical dimension is 3^n, trace Jensen and the trial
variational bound give

    Z_n(beta; a=0) >= 3^n,
    Z_n(beta; a=0) >= exp(-beta alpha_n).

For the *one-Rayleigh lower numerator* exp(-2 beta R), any valid denominator
upper estimates therefore produce

    J_lower <= min[exp(-2 beta R)/3^(4n), exp(-2 beta delta)],
    C_lower <= exp(-2 beta delta).

These ratios are unchanged by an extensive energy shift. Note the direction:
we upper-bound what this particular lower-bound recipe could possibly
certify, using lower bounds on the true denominators. We are not upper-bounding
the physical ratio with a variational lower numerator.

The exact comparisons are:

- n=6: delta=0.365339682084205... . Splitting beta at 3/4 bounds J_lower
  respectively by 0.345613249291... and 0.578099359332..., hence J_lower<29/50.
- n=8: delta=0.227135956266657... . Splitting beta at 31/40 gives upper
  bounds 0.695523744433... and 0.703237411515..., hence J_lower<71/100.

The verifier uses rational Taylor upper/lower exponential bounds. Decimal
numbers above are only displays. Monotonicity of G allows an optimistic
canonical replay with these J bounds and C=1. Even these optimistic replays
produce a nonpositive update (first spatial update for n=6, fifth spatial
update for n=8), without ever entering the accepted small-defect region.

For the fixed continued time-first order a stronger joint test works:

- If beta<=1/2, the dimension/Jensen term gives J_lower<2/5, so G(J_lower)<0.
- If beta>=1/2, the exact comparison exp(-delta)<4/5 gives C_lower<4/5.
  Use the respective global J bound together with C=4/5. The resulting
  optimistic time-first staircase fails after one further cycle for n=6 and
  after two for n=8. Delaying conversion while keeping that order cannot help.

This rules out these specific seeds with this particular one-D26-Rayleigh
numerator and the stated scalar updates, independently of denominator
certification precision. It does **not** rule out multiple numerator trial
directions, a better MPS at the large size, larger n, sharp normalized-squaring
updates, another spatial inequality, or adaptive changes of order/geometry.

For comparison, at the archived beta=21/2, use the exact n=6/8 untwisted upper
traces and legal cooling for 2 beta. The resulting lower J=C values are only
0.000462743350338... and 0.008284536832150..., respectively. They fail the
very first G test. This is a concrete two-temperature screen, not a claim
that the archived beta trace was already computed at twice beta.

## 4. AKLT: a genuinely entangled reference with an entire-spectrum certificate

Use the spin-one Cartesian basis and the normalization

    H_L^AKLT = sum_j h_(j,j+1),
    h=P_(total spin 2)=[(S dot S)^2+3(S dot S)+2I]/6.

Equivalently h=(I+F)/2-|Omega><Omega|/3, where F swaps the two sites and
Omega=|xx>+|yy>+|zz>. The neighboring h's do not commute. The periodic ground
vector has matrices A_x=sigma_x, A_y=sigma_y, A_z=sigma_z, so D=2. This is not a
small-coupling expansion around a product Hamiltonian.

The verifier checks h^2=h, rank(h)=5, the two-site Pauli MPS span of dimension
4, and its annihilation by h. Products of length two span all 2x2 matrices,
so the injectivity length is two. It also checks the length-three MPS rank 4,
annihilation by h12+h23, and exact nullity 4 of that Hamiltonian. Thus the
needed two-body intersection property Int(2,3) holds. The normal-MPS parent
intersection theorem then gives the unique periodic ground state for L>=3.

The exact premise used here is: a normal MPS of injectivity length L0 with
an ell-site parent satisfying Int(ell,l) for l>=L0+1 has a unique periodic
parent ground state for N>=max(L0+ell-1,l). For this example L0=ell=2,l=3.
A primary modern account with the AKLT check is Schuch, Molnar and
Perez-Garcia, *Simple Hamiltonians for Matrix Product State models*, p.2 and
Eq.(3), [arXiv:2503.10767v2](https://arxiv.org/pdf/2503.10767).

### Gap without a large-system eigensolver

On the **open four-site** chain, exact rational elimination proves

    (H_4^open)^2 - (2/5) H_4^open >= 0,
    dim ker H_4^open = 4.

The complete local dimension is 81; Cartesian occupation-parity blocks have
maximum dimension 21. Every rational nonnegative elimination pivot is saved.
Thus the smallest nonzero open four-site energy is >=2/5. This is a full
local operator inequality, not a Ritz estimate.

Knabe's finite-size criterion, stated as Theorem 1 in Gosset and Mozgunov,
*Local gap threshold for frustration-free spin systems*, assumes a
translation-invariant nearest-neighbor **projector** Hamiltonian, a nonempty
zero-energy ground space, open local size n>2, and periodic size m>n. It gives

    gap(H_m^periodic) >= ((n-1)/(n-2)) [gap(H_n^open)-1/(n-1)].

With n=4 this is gap >=(3/2)(2/5-1/3)=1/10 for every periodic m>=5. See
[Theorem 1, p.5](https://arxiv.org/pdf/1512.00088). All its hypotheses are
explicitly met; we do not apply this frustration-free theorem to the uniform
Heisenberg Hamiltonian.

### Certified omitted spectrum and heat traces

The unique exact state has energy zero. There are exactly 3^L-1 omitted
physical eigenstates, counted with multiplicity, and every one has energy
>=1/10 for L>=5. Hence

    1 <= Z_L(beta) <= 1+(3^L-1) exp(-beta/10).

No uncounted low state remains. This very coarse count is enough for a
finite demonstration:

- L=8, beta=160: certified tail <0.000761603; dimension 6561, omitted count 6560.
- L=16, beta=240: certified tail <0.001742971; dimension 43,046,721,
  omitted count 43,046,720.

Both upper traces are strictly below 1.01. The verifier bounds exponentials
using exp(-x)<=(1+x/4096)^(-4096), entirely in rational arithmetic.
These two rows are separate trace demonstrations, not an asserted beta/2beta
bootstrap staircase.

At both lengths, D=2, retained states=1, and linear trial span=1. The exact norm
is 3^L+3(-1)^L. An explicit Cartesian expansion still has
[3^L+3(-1)^L]/4 nonzero coefficients: 1641 at L=8 and 10,761,681 at L=16.
The four-site full local check is a separate 81-dimensional calculation.
The small MPS ground representation did not make all physical excited states
disappear; the operator inequality and counting theorem controlled them.

## 5. Why this AKLT result is not yet a thermal-bootstrap extension

The existing history proof requires, in a suitable real structure,

    -h = sum_alpha c_alpha A_alpha tensor A_alpha,
    c_alpha>=0, A_alpha real,

up to scalar/onsite pieces. Its realignment matrix must therefore be positive
semidefinite. In the Cartesian real structure for AKLT, set
Q=diag(1,-1,0). The verifier calculates exactly

    sum_(a,b,c,d) [-h_(ac,bd)] Q_(ab) Q_(cd) = -1/3.

An additive identity shift contributes a multiple of (Tr Q)^2=0 and cannot
repair this negative direction. Equivalently, the coefficient on the
traceless symmetric/quadrupolar matrices is -1/6. Orthogonal changes of this
real Cartesian basis preserve the obstruction.

This is a failure of the **currently used sufficient construction**, not a
proof that no other self-adjoint thermal transfer or spatial-purity inequality
could exist. The 4x4 MPS norm transfer with eigenvalues 3,-1,-1,-1 describes
this single state's norm; it is not X_beta with Tr X_beta^L=Z_L(beta).
Using it as the thermal transfer would discard the whole excited spectrum.

Nor does the AKLT count directly transfer to the bilinear Heisenberg model.
On a bond, S dot S >=3P2-2I, giving only

    H_Heis+aL >=3H_AKLT-(2-a)L.

This legal comparison yields a catastrophically extensive trace prefactor at
a=1.401482. The AKLT trial's asymptotic Heisenberg energy/site is -4/3, well
above the -1.401482 anchor threshold. A quantitative comparison sharp enough
around the actual target ground energy, including certified counts for its
orthogonal complement, is still missing. Phase intuition or small MPS residuals
cannot substitute for that inequality.

## 6. Recommended next bounded step

For the original uniform chains, prioritize a larger denominator seed with a
sharp certified trace upper bound, or a more correlated use of the archived
spatial moments that avoids their crude absolute upper endpoints. The exact
n=6/8 result discourages spending effort merely improving their denominator
precision within this one-vector recipe. A larger orthogonal numerator trial
collection is a genuinely different option and must be labelled as such.

For an entangled-reference extension, the AKLT local certificate supplies a
clean reference gap and count at tiny cost. The next question is the missing
thermal spatial-transfer condition or a replacement recursion, followed by
quantitative target-Hamiltonian comparison. No full spin-2 heat campaign was
started, and no generic nonperturbative uniform-Heisenberg theorem is claimed.

## Reproduction and provenance

Run `./REPRODUCE.sh`. It compiles and reruns the small GMP contractions, then
runs two exact verifiers. Fixed integer trial vectors are bundled; generating
new floating proposals with `prepare_small_trials.py` is unnecessary for
replay. Limits are one permitted CPU and 1 GiB address space. Recorded runs:
7.7 s/15 MiB for the MPS contractions, about 23 s/11 MiB for the full exact
uniform screen, and about 3.2 s/47 MiB for AKLT. Timings are machine-dependent.

`uniform_screen.json` records all exact Rayleigh ratios, scalar comparisons,
optimistic failures and consumed source hashes. `aklt_certificate.json`
records the exact local positivity pivots, counts and thermal examples.
`MANIFEST_SHA256.json` seals this new assessment's files. Existing physical
input generation, the D26 tensor/block identification, general transfer and
interpolation proofs remain inherited premises as stated above. These new
producer checks require independent review before promotion to root status.
