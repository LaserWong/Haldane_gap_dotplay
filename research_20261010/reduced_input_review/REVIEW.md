# Independent audit: largest-seed first moments suffice

Updated 2026-10-10 14:49 America/New_York (EDT) / 18:49 UTC.

## Verdict

**PASS.** The largest 8×8-rung patch needs only a positive-norm trial and its
Rayleigh quotient for the time–x–y bootstrap. Its H-squared moments, full
residual, energy lower bounds, number bins, spectral cutoff, and low-band
completeness are unnecessary. This is both a mathematical dependency reduction
and a tested file-level reduction, rather than reading comprehensive data and
then ignoring its higher-moment fields.

The following exact lower bounds hold for the ordinary spin-1/2 square bilayer,
unit rung exchange, equal straight intralayer exchanges g, no crossed exchange,
and every integer periodic square side L≥2. The finite-volume ground state is
unique. Positive-direction edge multiplicities, including side-two parallel
edges, are retained.

| g | Initial beta | One largest trial | 193 largest trial directions |
|---|---:|---:|---:|
| 3/100 | 259/20 | 0.318085338503 | 0.318085460990 |
| 1/25 | 47/4 | 0.235117533454 | 0.235117964607 |
| 1/20 | 199/20 | 0.171818025695 | 0.171822115684 |
| 3/50 | 203/20 | 0.103485296797 | 0.103487228301 |

These are sufficient gap certificates, not gap estimates, optimal coupling
thresholds, arbitrary-aspect-ratio results, or infinite-volume uniqueness
statements. All acceptance uses exact rational or Q(sqrt(2)) arithmetic and
analytic inequalities; this is not proof-assistant verification.

Each row compares the two numerator choices at identical beta and with identical
smaller-patch quadratic upper traces. The largest loss from dropping 192 trial
directions is exactly 0.000004089989, at g=.05. The reduced input requirement
itself is a cost reduction; any improvement over older certificates also uses
the separately reviewed denominator bounds and choice of staircase.

The 193 directions in the last column are orthogonal **trial directions**.
Their being the complete physical low band is neither asserted nor needed by
this reduced proof. The largest patch still has 128 physical spins and full
Hilbert dimension 2^128. The one retained trial is optimized in a 29-dimensional
linear space. The largest patch that still needs a complete upper-trace
certificate is 8×4 rungs, with 64 physical spins and Hilbert dimension 2^64.

## 1. Exact correlated ratios and their basepoints

Let Z(nx,ny;b)=Tr exp[-b H(nx,ny)] and v=(n,n,beta), n even. Let D_t double beta
and D_x,D_y double their spatial coordinates. Define

    v0=(n,n,beta), v1=(n,n,2beta),
    v2=(2n,n,2beta), v3=(2n,2n,2beta),
    q1=Z(v1)/Z(v0)^2, q2=Z(v2)/Z(v1)^2, q3=Z(v3)/Z(v2)^2.

The transfer hypotheses previously proved for this model give each purity in
(0,1]. No spatial length is identified with physical temperature. Formal
partition-function cancellation, keeping every basepoint, gives

    J1=q1^4 q2^2 q3=Z(v3)/Z(v0)^8,
    J2=q2^4 q3^2=Z(v3)^2/Z(v1)^8,
    C0=q3=Z(v3)/Z(v2)^2.

Thus the needed physical inputs are precisely a lower bound L≤Z(v3) and three
upper bounds Z(v0)≤U0, Z(v1)≤U1, Z(v2)≤U2. The safe inputs are L/U0^8,
L^2/U1^8 and L/U2^2. There is **no largest-patch upper trace**. In particular,
no trace at (8,8;beta) is needed for n=4.

Let G(z)=1-(1-z)^2/(2z^2). Its derivative (1-z)/z^3 is nonnegative on (0,1].
The established sequential squaring inequalities therefore give

    a=G(J1), b=G(J2 a), c=G(C0^4 a^2 b),

using downward-rounded lower bounds at every step and requiring each new
bound to be positive. After three updates these bound the t,x,y staircase
at v3: P_t(v3), P_x(D_t v3), P_y(D_x D_t v3), respectively.

For adjacent directions i,j at a base w, put a=P_i(w), b=P_j(D_i w),
c=P_j(w), e=P_i(D_j w). Exact cancellation gives e c^2=b a^2. Since c,e≤1,
the swapped lower pair is (a sqrt(b), a^2 b). Swapping t,x then t,y gives

    A=a sqrt(b), B=a^2 b sqrt(c), C=a^4 b^2 c.

This is the canonical x,y,t staircase at the unchanged base v3. Only this
canonical triple is passed to the canonical recursion and interpolation.
`audit_dataflow.py` rechecks all six formal orders, 12 adjacent swaps, 18
rotations, and the precise largest-numerator-only dependency graph. Its ledger
is `results/path_ledger.json`.

For numerical stability the code shifts each Hamiltonian separately. If
Z_i(b)=exp(-b e_i) Q_i(b), it explicitly restores

    exp(-2beta e64+8beta e16),
    exp(-4beta e64+16beta e16),
    exp(-2beta e64+4beta e32)

in J1, J2, C0, respectively. Trial shifts are not assumed extensive.

## 2. Finite-trial Peierls/Jensen lower bound

Let H be any finite-dimensional self-adjoint Hamiltonian and tau>0. For any
normalized psi, the spectral theorem and scalar convexity give

    exp[-tau <psi,H psi>] ≤ <psi,exp(-tau H) psi>.

If psi_1,...,psi_k are orthonormal, their projection P satisfies 0≤P≤I. Since
exp(-tau H) is positive,

    sum_i exp[-tau <psi_i,H psi_i>]
      ≤ Tr[P exp(-tau H)] ≤ Tr exp(-tau H).

Omitted vectors contribute positively; their number and energies need no
bound for this inequality. Small residuals, eigenvector status and low-band
completeness are not hypotheses. A verified upper endpoint for a Rayleigh
quotient can replace the exact quotient because exp(-tau x) decreases in x.

For a nonnormalized single trial psi=Wc, use

    G=W*W, K=W*H W,
    rho=(c* K c)/(c* G c), c*G c>0.

Only the Gram and first-Hamiltonian moment enter. Common positive Gram scaling
factors cancel. The ground-only numerator in the code is exp(-2beta rho), or
exactly 1 after shifting H by rho.

For a full-column-rank, nonorthogonal W, let B=G^(-1/2) K G^(-1/2). If U
diagonalizes B, then V=W G^(-1/2) U is an orthonormal family with Rayleigh
quotients the eigenvalues theta_i of B. Therefore

    sum_i exp(-tau theta_i) ≤ Tr exp(-tau H).

Generalized Ritz upper enclosures also suffice. If G is singular, first remove
dependent columns or work on its positive support with the corresponding rank;
zero-norm directions cannot be counted. Summing exponentials of individual raw
Rayleigh quotients for arbitrary nonorthogonal columns is generally invalid.
For example, counting the same normalized vector twice would double its
contribution. Orthogonalization, Gram normalization, or an equivalent frame
weighting is essential.

## 3. Independent physical input generation without higher moments

The comprehensive historical ground code formed G, K and J=<Hpsi,Hpsi>, using
geometric arrays F,S,V,W and four- and six-triplet contractions. The minimal
ground input keeps only G, K and integer coefficients. We independently
reconstruct it, without reading those comprehensive largest-patch files:

- Rebuild the periodic graph and pair-orbit classification.
- Enumerate all C(64,4)=635,376 four-site subsets with the independently reviewed
  exact matching identities, computing F and S only.
- Do not enumerate any six-site subset and do not compute V or W.
- Form G=diag(D,F) and K with blocks D C, h E, h E*, 4 den F+h S.
- Select independent columns by exact rational Schur elimination and verify all
  29×29 G/K entries, all selected indices, the norm, and the Rayleigh quotient.

Here den=4 denominator(g), h=2 numerator(g), E is F with a zero vacuum row, and
D contains the exact vacuum/pair-orbit Gram weights. The historical common
factor 2^64 cancels. The matching-action/Gram identities are those already
proved independently in `large_seed_review`; the local spin kernel is rebuilt
again directly in the present optional-triplet audit.

`rebuild_fs_only.cpp` has no q6 loop or V/W accumulator. Per-subset coefficients
are checked to obey |l|≤2, |r|≤128. Every Gram factor is at most 9 and there
are nine matching pairs, so each accumulated |S_ij| is at most
635376×9×9×2×128<2^34; F is smaller. Signed 64-bit accumulation cannot overflow.
On this 8×8 graph, the exhaustive F/S stage took about two seconds on one CPU in this environment;
that timing is diagnostic, not a complexity theorem. Its loop size is
C(N,4), with bounded-degree graph actions and 14 pair-orbit components
for this graph (the compiled storage supports at most 20). No 2^128 matrix is formed.

For the optional 193 directions, the independent four-spin physical kernel
rebuilds the highest-weight one-triplet generator W and verifies S+W=0, total
magnetization one and odd triplet parity. The 373-configuration generator is
translated exactly. Its 64 translated supports have a union of 23,488 basis
configurations. To compute G/A only, the audit forms P_support H W; that
restricted image has 1,873 nonzero configurations. It does not form full H W
(the old full image had 67,755 configurations), square H, or calculate a
residual. Discarding outputs outside the union is exact for these matrix
elements because every trial bra is supported inside it; it would not be a
valid residual calculation, and none is claimed.

Every displacement Gram/first-moment entry agrees with the minimal export.
The symbols are evaluated independently as pairs in Q(sqrt(2)); all 64 Gram
symbols are strictly positive, and all upward rational Rayleigh endpoints are
checked exactly. Distinct momenta are orthogonal after Gram normalization.
SU(2) gives three mutually orthogonal magnetic copies with equal mean energy.
The even-parity ground trial is orthogonal to every odd-parity triplet trial.
These facts justify exactly 1+3×64 trial contributions, without any claim
about the number of physical eigenvalues below a cutoff.

## 4. Real read boundary, not unused fields

The producer's historical `export_minimal.py` did read comprehensive files to
extract existing first moments. That historical preparation is not presented
as having avoided their original computation. The new `replay_minimal.py`
reads only explicitly whitelisted largest G/K and optional G/A files, never
dereferencing their historical-source strings.

`test_read_boundary.py` copies the declared numerical inputs to an isolated
tree and runs the frozen producer consumer there. It places invalid-JSON poison
at the historical comprehensive largest paths and representative largest
Temple/number-bin paths. A Python audit hook rejects any JSON open outside the
strict per-case allowed set. In ground-only mode the optional G/A file is also
physically absent. All eight runs produce exactly the frozen output records:

- ground-only: nine numeric files, comprising two smaller trace records, one
  largest G/K record, and six short-size records;
- 193 directions: the same nine plus one largest G/A record.

The supplied G/K and G/A schemas contain no H², residual, spectral cutoff,
number-bin, lower-eigenvalue, complement, or completeness field. Historical
metadata are just source names/hashes and are never dereferenced. Every
actual JSON read equals the declared allowed set. `results/read_boundary.json`
records the complete per-case evidence. The independent acceptance auditor
imports no producer module; the separate isolation test deliberately executes
the producer solely to verify its claimed data access and output equality.

## 5. Smaller upper traces and all integer sizes

The eight 4×4/8×4 quadratic-boson upper-trace records are unchanged bytes from
`tail_comparison_review`, which independently verified their complete physical
low-band count, all Temple endpoints and positive omitted-tail sums. Oscillator
shell multiplicities are kept distinct from physical triplet-shell counts.
The trace upper formulas are valid for every beta>0. These smaller full upper
certificates remain required; Jensen alone does not supply them.

The scalar audit uses an independent 90-term Taylor enclosure reduced to
|x|≤1/8 and directed 384-bit squaring. Every 16-decimal correlated ratio,
first-cycle lower bound, 18-decimal transported triple, defect update and final
gap equals the producer record. Square roots use exact integer-square-root
witnesses. The reported gap d is checked by exp(beta_accepted d) 32u<1,
independently of floating logarithms.

For g=.03,.04 the accepted canonical onset is L=8. For g=.05,.06 it is L=16;
the exact signed-transfer window from the initial canonical triple covers
all integer rectangles in [8,16]^2, hence the missing squares. We independently
recompute every saved window, including optional extra windows, and verify
its direct exponential gap inequality. No interpolation theorem is changed.

For L=2,...,7 we inherit the independently accepted g_m=.06 number-compression
LDL certificates. They are valid at every 0≤g≤g_m: for x_q=||psi_q||≥0,

    <psi,K(g)psi> ≥ sum_q(1-2g_m)q x_q²
                    -2 sum_q g_m c_q x_q x_(q+2)
                  = x* J(g_m) x.

Both parities of Q≥1 are included. The product trial has shifted Rayleigh
quotient zero, so lambda_1(K(g))≤0 and the certified lambda_2 lower bound is a
gap lower bound. Their common minimum 36490836267/62500000000 is greater than
all eight targets. This argument concerns the comparison form and does not
assume monotonicity of the physical gap. The short sizes, necessary finite
window, and canonical asymptotic theorem cover every integer L≥2.

## 6. Provenance and reproduction

The producer freeze is `low_band/reduced_input/FROZEN_MANIFEST_1842.json`,
SHA-256 `8d8cce2d1ed1a30ad57f96d9b0e9accb3ec2d4c18dd77702d991aa4e8fbac1d6`.
Its 21 files are preserved under `snapshot/`, together with the needed smaller
inputs. `INPUT_SHA256.json` checks every frozen byte.

The inherited small-patch trace review manifest is
`28a3fd81c41fa5dc0b8da7b3ac427c7283659177ed9d30c098ae4f6b45609327`.
The inherited alternative-order/short-size and physical matching-identity
review manifests and relevant input hashes are also pinned in `INHERITED_REVIEWS.json`. Acceptance verifies these
seals and the exact needed input hashes, without opening historical largest
comprehensive numerical data.

Run `REPRODUCE.sh`. It pins execution to one CPU, limits virtual memory to
1 GiB, sets BLAS/OpenMP threads to one, rebuilds F/S-only geometry, checks the
formal dataflow, independently accepts all eight candidates, and reruns the
isolated consumer tests. It writes only this review's generated outputs.
No producer file, prior review, repository index, or remote state is changed.
