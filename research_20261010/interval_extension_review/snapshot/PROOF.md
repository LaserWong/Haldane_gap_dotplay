# A continuous ordinary-bilayer extension with one filtered numerator

Updated 2026-10-10 15:14 America/New_York (EDT, UTC−4) / 19:14 UTC.
Status: exact producer candidate, independent interval audit pending.

## 1. Result and model

Fifteen adjoining closed intervals cover 7/100 ≤ g ≤ 39/500. The exact
candidate gives a unique ground state and

    gap(H_L(g)) ≥ 2006633957/1000000000000 = 0.002006633957

for every integer square side L≥2 on this extension. Combining with the sealed,
independently reviewed ordinary_interval / ordinary_interval_review result gives
31 closed intervals covering 0≤g≤39/500=.078 and the unchanged uniform bound

    gap(H_L(g)) ≥ 486442811/250000000000 = 0.001945771244.

The model has spin 1/2 on two square layers, unit AF rung coupling, equal
nonnegative straight intralayer couplings g, no crossed exchanges, and positive
direction periodic bonds counted with multiplicity, including side two. All
energy statements use the physical Hamiltonian unless a prime indicates
H′=H+3N/4, where N is the number of rungs.

The main patches have 16,32,64 rungs and full physical dimensions 4^16,4^32,4^64
(the largest is 2^128). Original linear trial dimensions are 11,29,29. Each
smaller denominator retains one identified ground level. The numerator uses
one normalized filtered trial contribution. No excited-state trial family is
used or counted, and alternative ground witnesses are never added as distinct
levels. These are not MPS bond dimensions.

## 2. Exact inherited physical inputs

Use the audited g-independent vacuum/pair/A42-pair basis. Its columns have
triplet numbers q=0,2,4 and spin zero. With the common factor 2^N removed, write

    G=W*W/2^N,
    A(g)=W*H′(g)W/2^N=A0+g A1,
    B(g)=W*H′(g)^2 W/2^N=B0+g B1+g² B2.

B is the full physical second moment, including q=6 leakage; it is not
A G^−1 A. No higher moments or new Hamiltonian contractions are needed.
The polynomial degree bounds follow from H′(g)=Q+gV and the fixed basis.
`validate_sources.py` reconstructs these coefficients exactly at g=.03,.04,.05,
then verifies every G/A/B against all seven available saved coupling files
(.03,.04,.05,.06,.07,.08,.10) for all three geometries. It additionally checks
A0=QG and B0=Q²G in their explicit q-coordinate blocks. The original matrices
and the physical derivation remain inherited inputs from large_seed_review.

On each interval two smaller coefficient vectors are taken from the fixed
auxiliary exports centered at .07 or .08. The inverse-moment procedure that
proposed them is not an assumption of the present certificate: any nonzero
coefficient vectors in the audited basis may be used. Their Rayleigh and full
residual polynomials are reconstructed here. The largest fixed base vector is
proposed by a 29×29 generalized eigensolver at the interval midpoint and rounded
to integers. Only the exact embedded integer vector matters. Saved replay has
no eigensolver calls.

For each vector c, n=c*Gc>0, and

    rho(g)=c*A(g)c/n=rho0+rho1 g,
    v(g)=c*B(g)c/n−rho(g)²=v0+v1 g+v2 g².

Exact checks v0≥0, v2≥0, 4v0v2≥v1² verify the two-operator covariance is positive
semidefinite. The maximum of v on [a,b] is its endpoint maximum. The exact
minimum checks both endpoints and the vertex −v1/(2v2) when inside [a,b].

## 3. A uniform filter with a fixed base vector and fixed t

Let ψ be the normalized largest base vector, rho its Rayleigh energy, and
r(g)=(H′(g)−rho(g))ψ. Then <ψ,r>=0 and ||r||²=v(g). For fixed rational t≥0,

    φ_g=(ψ−t r(g))/sqrt(1+t²v(g))

is normalized. Suppose <r,H′r>≤Rmax v uniformly. Then, with
C(g)=Rmax−rho(g),

    <φ_g,H′φ_g> ≤ rho(g)+v(g)(−2t+C(g)t²)/(1+t²v(g)).

To bound Rmax uniformly, use the reviewed even-q≤6 Jacobi upper comparison.
For q=0,2,4,6 its diagonal is d_q=(1+2g)q, and its squared off-diagonal is

    b_q(g)=(floor(q/2)+1)(3g²/4)S + 4g² floor((q+1)²/4),
    S=sum_e w_e²=128 for the 8×8 patch.

The local number-preserving upper bound and bosonic pair bound were
independently verified in variational_filter_review. For nonnegative g all
these entries are nondecreasing. For x_q=||P_q r||, the comparison form at any
g≤b is at most its value at b. A rational Rmax with strictly positive LDL
pivots of Rmax I−Jplus(b) therefore bounds the required compression for every
g in the interval. Its positive exact pivots are saved. Potential q=8 parts
of H′r are orthogonal to r and do not contribute to <r,H′r>.

Let

    Cmax=Rmax−min(rho(a),rho(b))>0,
    vmin=min_[a,b] v(g)≥0,
    t=1/Cmax,
    d=vmin Cmax/(Cmax²+vmin).

Then C(g)≤Cmax and −2t+C(g)t²≤−1/Cmax. Crucially, the whole function
v/(1+t²v) is increasing for v≥0. Consequently

    <φ_g,H′φ_g> ≤ rho(g)−d

throughout the closed interval. This step does not bound a negative numerator
and its normalization denominator in incompatible directions. Both endpoints
and the exact quadratic minimum enter a single increasing fraction. Our saved
intervals have vmin>0, so d>0. If vmin=0, the formula safely yields d=0.

No residual certificate for φ_g is asserted. It remains an even spin-zero
vector supported at q≤6. Pointwise its filter plane has dimension at most two;
adjoining r(g) to the old 29-dimensional space gives dimension at most 30.
The same bound holds for the entire interval family: Q maps the original
q=0,2,4 basis space into itself, and r(g) lies in that space plus span{Vψ}.
There remains exactly one numerator trial contribution.

This stronger variant requires the previously available largest full H²
matrix. It is not the earlier first-moment-only variant. Existing G/A/B alone
are sufficient; the optional sharper F/S/V/W residual expectation filter is
not used here.

## 4. Auxiliary Temple lower endpoints and full tails

For each smaller patch the reviewed quadratic-boson reference is

    E_b(g)+q delta(g)=C(2g−1)+(C+q)sqrt(1−4g),
    C=3N/8, delta=sqrt(1−4g).

Total triplet parity is invariant under the physical Hamiltonian, hard-core
compression, mode rotation, and squeezing. The reviewed parity argument gives
lowest odd energy ≥E_b+delta and second even energy ≥E_b+2delta. For each
fixed even auxiliary trial, the code verifies uniformly

    m1=min_[a,b](E_b+delta−rho)>0,
    m2=min_[a,b](E_b+2delta−rho)>0.

These functions are concave, so directed lower endpoint evaluations suffice.
This identifies the unique physical ground below the odd sector and applies
rank-one Temple in the even sector:

    rho(g)−w ≤ λ0(H′(g)) ≤ rho(g),
    w=vmax/m2.

No filtered residual is used in this denominator bound. The auxiliary vector
is a witness for the same ground as any other variational ground vector.

For all q=1,…,N let mq be the endpoint lower bound for
E_b+q delta−rho. Ordered min-max and the finite reference count give

    exp(beta rho(g)) Z′_N(beta,g)
      ≤ exp(beta w)+sum_(q=1)^N binom(3N+q−1,q) exp(−beta mq)
      =: U_N(beta).

The sum through N has enough reference entries because binom(4N,N)≥4^N.
The multiplicities are bosonic reference counts, not physical triplet-shell
counts. No claim that the squeezed physical subspace has q≤N is made. The
single q=0 reference entry is replaced by the improved ground bound, and all
remaining terms are nonnegative. Directed rational exponential enclosures
are inherited from the reviewed scalar implementation.

## 5. Correlation, recursion, and all integer sizes

Let the three affine normalizers be auxiliary rhoS, auxiliary rhoT, and the
filtered upper rhoM=rho_base−d. Spectral Jensen provides
Z′_64(2beta,g)≥exp(−2beta rhoM(g)). The following combinations are evaluated
as shared-g affine functions, then minimized at the interval endpoints:

    h1=8rhoS−2rhoM,
    h2=16rhoS−4rhoM,
    h0=4rhoT−2rhoM.

The extensive −3N/4 shifts cancel identically. Independently bounding total
extensive energies before cancellation would not be the certificate used here.
The directed lower ratios are

    J1=exp(beta min h1)/U_16(beta)^8,
    J2=exp(beta min h2)/U_16(2beta)^8,
    C0=exp(beta min h0)/U_32(2beta)^2.

The implementation rejects ratios outside (0,1]; it does not clip them.
With F(z)=1−(1−z)²/(2z²), the reviewed time/x/y route and transport give

    a=F(J1), b=F(J2 a), c=F(C0^4 a² b),
    A=a sqrt(b), B=a² b sqrt(c), C=a^4 b² c

at the canonical base (8,8,2beta). All purities are rounded downward and
checked positive. The reviewed three-purity recurrence, signed-transfer
finite-window interpolation, and positivity hypotheses are inherited unchanged.
Their monotonicity makes the uniform interval inputs sufficient pointwise for
every g in the interval.

The output has 81 explicitly checked finite windows and 90 L=2,…,7 rows. The
worst asymptotic starting side is 1024; every smaller integer L≥8 is covered
by the saved windows. Short sizes use their exact periodic edge-square sums
16,18,32,50,72,98 and the decreasing comparison E_b+delta at the upper endpoint,
with the singlet-product ground upper 0. This invokes monotonicity of the
comparison, not monotonicity of the unknown physical gap. The final bound for
each interval is the minimum of all required windows, the asymptotic bound,
and the short-size bound. The union ledger checks exact adjoining endpoints.

## 6. Exact partition and reproducibility

The extension endpoints, in order, are

    7/100, 71/1000, 9/125, 73/1000, 147/2000, 37/500,
    149/2000, 299/4000, 3/40, 19/250, 153/2000, 77/1000,
    31/400, 311/4000, 623/8000, 39/500.

Each pair of consecutive endpoints is a closed interval. `coverage_summary.json`
contains exact temperatures and gaps; `coverage/` contains all fixed vectors,
polynomials, filter pivots, margins, traces, recursion states, and bridges.
`replay_result.json` records the certified union with the sealed earlier
0≤g≤.07 package; the older producer freeze is checked byte for byte.

Run `bash research_20261010/interval_extension/REPRODUCE.sh` from the repository
root. This checks dependency hashes, reconstructs all physical polynomial
inputs, tests exact filter algebra and fixtures, and replays saved vectors.
The complete producer scan took approximately 30 seconds at a peak RSS of
51,008 KiB, with one-CPU affinity, all numeric thread counts one, and a 1 GiB
address-space cap. No production physical vector or full spectrum was built.
The optional proposal regeneration changes only this new folder.

At g=.08 the present ground-only finite-tail route did not start in the bounded
beta=5,…,30 step .05 proposal search, even when substituting the sharper point
filter. This is not an all-temperature exclusion or a physical no-gap claim.
The separately studied .08 discrete combination uses stronger triplet inputs;
its success does not fill the remaining continuous interval [.078,.08].
