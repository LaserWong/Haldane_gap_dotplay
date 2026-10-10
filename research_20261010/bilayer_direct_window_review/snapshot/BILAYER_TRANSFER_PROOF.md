# Independent optimized ordinary-bilayer audit and complete square-size bridge

Date: 2026-10-10 13:20 America/New_York (EDT, UTC−4) / 17:20 UTC.

## 1. Result and scope

For two spin-1/2 degrees of freedom at each site of the square torus, set

\[
H_L=\sum_r\mathbf S_{r,0}\cdot\mathbf S_{r,1}
+g\sum_{r,\ell=0,1}\bigl(\mathbf S_{r,\ell}\cdot\mathbf S_{r+e_x,\ell}
+\mathbf S_{r,\ell}\cdot\mathbf S_{r+e_y,\ell}\bigr).
\]

The rung coupling is one and \(\hbar=1\). Both intralayer directions have the same positive coupling \(g\). There are **no cross-layer inter-rung interactions**. Positive-neighbor terms are retained with multiplicity: at side length two, the same unordered edge occurs twice. Every integer \(L\ge2\) has a unique ground state and the following rigorous lower bounds:

- \(g=1/100:\quad\Delta_L\ge0.168921021674\).
- \(g=1/50:\quad\Delta_L\ge0.057308457817\).

These are exact-certificate conclusions, rounded downward to twelve decimal places. They are not floating estimates of the actual gaps and are not claims about a physical phase boundary or globally optimal certificate. They improve the status of the archived candidates by independently checking their physical inputs and optimized scalar arithmetic and, for \(g=1/50\), closing the previously missing sizes below sixteen.

The theorem concerns square tori. The interpolation also proves the same stated finite-scale bounds for rectangles whose sides lie in the same specified dyadic interval. It does not certify every arbitrary aspect ratio.

## 2. What was independently recomputed

The executable `verify_optimized_bilayer.py` imports no generating project code or prior audit module. It performs no eigensolve and no floating optimization.

1. Rebuild the physical sixteen-dimensional two-rung Hamiltonian symbolically and compare its exact characteristic polynomial with the claimed local spectrum.
2. Rebuild the exact time-reversal-real rung basis and all six real antisymmetric spin factors, including their norms.
3. Rebuild the six exact trial-vector matrix products from the graph and the integer coefficients in the NPZ files. Include the complete support reached by applying the full Hamiltonian.
4. Recompute exact Rayleigh quotients, full residual norms, full-space second-level bounds, and Temple intervals.
5. Check that all embedded ground snapshots equal the separately saved ground JSON files, and that each of the twenty-four stored thermal-tail nodes uses the correct snapshot, geometry, temperature and coupling.
6. Check every selected local comparison parameter and every saved tail and shifted-trace upper bound. Independent exponential intervals use 220-bit outward rounding and 48 Taylor terms, rather than the generating code's 128 bits and 32 terms.
7. Recompute all six rational scalar paths, including the correlation cancellations, legitimate staircase-order conversions, and every recorded update. Check each final gap directly through a rational exponential inequality, without using the generator's logarithm routine.
8. Check the finite-size bridges and all endpoint constants in the extended interpolation argument below.

The six ground inputs have shapes \(2\times2\), \(4\times2\), \(4\times4\), at each of the two couplings. Their physical-spin counts are 8, 16, 32; complete Hilbert dimensions are 256, 65,536, 4,294,967,296; linear trial dimensions are 23, 93, 377. Their complete Hamiltonian-applied union supports have dimensions 58, 1,301, 21,345. Exactly one approximate ground vector is retained in each case. No MPS bond dimension is involved in these sparse-vector certificates.

`optimized_bilayer_audit.json` records the exact inputs, hashes, six ground checks, twenty-four tail-node checks, all scalar stages, finite-size certificates, and resource usage. The run used about 70 MiB peak RSS and approximately five seconds on the recorded environment, with one BLAS thread and at most two CPUs.

## 3. Exact local comparison and complete omitted spectrum

Put \(h_i=\mathbf S_{i,0}\cdot\mathbf S_{i,1}+3/4\), the rung-triplet projector, and \(v_{ij}=\mathbf S_{i,0}\cdot\mathbf S_{j,0}+\mathbf S_{i,1}\cdot\mathbf S_{j,1}\). Direct physical-basis characteristic-polynomial calculation gives the spectrum of \(a(h_i+h_j)+gv_{ij}\):

\[
2a+g/2\;(5),\quad2a-g/2\;(3),\quad a+g/2\;(3),\quad a-g/2\;(3),
\]
\[
a-g/2\pm\sqrt{a^2-ag+g^2}\;(1\text{ each}).
\]

For \(a\ge g/2\ge0\), all eigenvalues except the minus-root value are nonnegative. Thus the exact rational conditions

\[
b\ge0,\quad b+a-g/2\ge0,\quad (b+a-g/2)^2\ge a^2-ag+g^2
\]

imply \(gv_{ij}+a(h_i+h_j)+bI\ge0\). There are \(2N\) inter-rung edges, counting multiplicity, and each rung has degree four. Hence, with \(E_{00}=-3N/4\),

\[
H-E_{00}\ge\alpha\sum_i h_i-BI,
\qquad \alpha=1-4a>0,\quad B=2Nb.
\]

Ordered min–max therefore bounds every energy, including all omitted states, by the corresponding independent-rung bin \(E_{00}+\alpha k-B\), of multiplicity \(\binom Nk3^k\). This is a full-Hilbert-space statement and does not assume the numerical magnetization sector contains every low-energy state.

For the seed ground intervals, either this comparison or the elementary bound \(V\ge-3gN\) supplies a second-eigenvalue lower bound \(E_1^-\). The singlet product has energy \(E_{00}<E_1^-\), establishing a unique full-space ground below that threshold. Each exact Rayleigh quotient \(\rho<E_1^-\) and full residual \(\epsilon^2\) then give

\[
\ell=\rho-\frac{\epsilon^2}{E_1^--\rho}\le E_0\le U=\rho.
\]

The basis used for the sparse multiplication is unnormalised with exact rung weights \((2,1,2,1)\); all norms and matrix elements use this metric. The residual includes states outside the trial space.

At every saved thermal node, with its individually chosen \(a,b\), the shifted trace \(Q=e^{\beta U}\operatorname{Tr}e^{-\beta H}\) satisfies

\[
1\le Q\le e^{\beta(U-\ell)}
+e^{\beta(B+U-E_{00})}\left[(1+3e^{-\beta\alpha})^N-1\right].
\]

The numerator bound \(Q\ge1\) uses \(E_0\le U\). The upper bound sums the entire omitted spectrum via its bin multiplicities. Separate choices of \(a\) at \(\beta\) and \(2\beta\) are legitimate because each node independently bounds its physical trace.

## 4. Exact physical transfer in both directions

In the physical rung basis \((dd,du,ud,uu)\), the following columns, all divided by \(\sqrt2\), form an orthonormal basis:

\[
(0,1,-1,0)^T,\ (0,i,i,0)^T,\ (1,0,0,1)^T,\ (i,0,0,-i)^T.
\]

The two-spin time reversal is complex conjugation in this basis. The rung Hamiltonian is \(\operatorname{diag}(-3/4,1/4,1/4,1/4)\), and every layer spin is \(S_\ell^\alpha=iA_\ell^\alpha\) with \(A\) real antisymmetric and \(A^TA=I/4\). The audit verifies these identities symbolically.

Consequently \(-g\sum_{\ell,\alpha}S_\ell^\alpha\otimes S_\ell^\alpha=g\sum A_\ell^\alpha\otimes A_\ell^\alpha\). For any transverse integer circumference \(W\ge2\), group one column of \(W\) rungs. Its internal Hamiltonian is real symmetric. Across columns there are \(6W\) identical-endpoint event factors \(2A\), each of norm one and with nonnegative intensity \(g/4\).

The continuous-time bond-history measure has finite mass \(e^{3\beta gW/2}\). Merge the left and right histories chronologically, interspersing their local factors with column imaginary-time evolution, and take the column trace. Swapping the two histories does not change the merged operator string, except on the zero-measure simultaneous-event set. The resulting kernel is real symmetric. Its absolute value is at most \(4^W e^{\beta\|V_W\|}\), where \(\|V_W\|\le3W/4+3gW/2\). Thus it is Hilbert–Schmidt.

The absolutely convergent Duhamel expansion yields

\[
Z(M,W;\beta)=\operatorname{Tr}X_{W,\beta}^M\qquad(M\ge2\text{ any integer}).
\]

The same argument with axes interchanged establishes the second direction for the identical Hamiltonian and multiplicity convention. The transfer operator need not be positive semidefinite or have a pointwise-positive kernel. Its even powers are positive, and its odd physical traces are strictly positive. A unique largest-absolute-value transfer eigenvalue must therefore be positive: a negative one would eventually make odd traces negative. This supplies the sign needed for odd-size interpolation. No Trotter limit is used as an unverified numerical approximation.

## 5. Scalar paths and accepted asymptotic bounds

For a staircase through the commuting doubling axes \(x,y,t\), let its three purity lower bounds be \(A,B,C\). The exact exchange identity and purity squaring give

\[
G(z)=1-\frac{(1-z)^2}{2z^2},\qquad
A'=G(A^4B^2C),\quad B'=G(B^4C^2A'),\quad C'=G(C^4(A')^2B').
\]

Every implemented operation is rounded downward. For a staircase of four partition functions \(Z_0,\ldots,Z_3\), the first two arguments are evaluated after exact cancellation:

\[
J_1=Z_3/Z_0^8,\quad J_2=Z_3^2/Z_1^8,
\]

so that \(A_1=G(J_1)\), \(B_1=G(J_2A_1)\), and \(C_1=G(C^4A_1^2B_1)\). All ground-pivot exponential factors are combined before bounding. This avoids counting the same intermediate-trace uncertainty twice.

All three inequivalent axis orders \(xyt,xty,txy\) were reconstructed from their actual geometrical/temperature nodes. They were not obtained by relabeling three fixed input numbers. An adjacent pair of staircase bounds \((a,b)\) can be reversed using the lower bounds \((ab,a^2b)\), as follows from the exchange identity and purity at most one. The checked saved records use these rational conversions to the canonical \(xyt\) order.

For \(u\le1/100\), a full cycle contracts the common defect by \(u'\le32u^2\), since \(49/[2(1-7u)^2]<32\) and \(32u^2\le u\). Combined with the all-integer interpolation, accepted canonical seeds give \(\Delta\ge\log(1/(32u))/\beta\).

The strongest accepted records are:

- \(g=1/100\), order \(xyt\), initial \(\beta=45/4\), final \(n=4,\beta=45/2\), \(u\approx0.0006985813721572771\), exact certified gap
  \(57480845078162907233072210178152997545/340282366920938463463374607431768211456\).
- \(g=1/50\), order \(xyt\), initial \(\beta=49/4\), final \(n=16,\beta=98\), \(u\approx0.0001136979975699853\), exact certified gap
  \(19501057670622863144185293551966373475/340282366920938463463374607431768211456\).

The alternative-order large-size gaps also pass: approximately 0.147457300837 and 0.143673119374 at \(g=.01\), and 0.0210684474247 and 0.0289692549806 at \(g=.02\). Their stored entry sides are respectively 8, 8, 64 and 64. No assertion of global optimality of the temperature grid or axis choice is made.

## 6. Finite all-integer interpolation at the needed larger domain

The archived one-dimensional proof remains valid up to common defect \(v=1/40\). Here are the exact checks needed to use that fact independently.

Given spatial purity \(S(n,\beta)\ge1-v\) and thermal purity \(T(2n,\beta)\ge1-v\), with even \(n\), the exchange identity gives \(S(n,2\beta)\ge(1-v)^3\). The purity inverse bound implies a unique dominant transfer weight greater than \(1-2v\), because

\[
(1-v)^3-(1-4v+8v^2)=v(1-5v-v^2)>0.
\]

The squared spatial defect is at most \(5v^2\): the coefficient

\[
\frac{(3-3v+v^2)^2}{2(1-v)^6}
\]

increases on this interval and has endpoint \(17529408800/3518743761<5\). For its monotonicity, the derivative of \((3-3v+v^2)/(1-v)^3\) has numerator \(6-4v+v^2>0\).

For any integer \(n\le L\le2n\), signed-tail control at \(2\beta\), absolute-spectrum Hölder interpolation at \(\beta\), and the positive dominant eigenvalue then give a thermal-purity loss bounded by

\[
\tfrac32v+5v^2+\frac{2v}{1-2v}\le4v.
\]

Indeed \(3/2+5v+2/(1-2v)\) increases, and its value at \(1/40\) is \(567/152<4\). All factors used in the interpolation are positive throughout the interval. Thus \(T(L,\beta)\ge1-4v\), including odd \(L\).

Now let the three canonical two-dimensional defects be at most \(u\le1/200\), and take integers \(n\le L,W\le2n\). The signed y-transfer tail and absolute-spectrum norm monotonicity give

\[
S_x(n,W;\beta)\ge(1-u)^3(1-2u)\ge1-5u.
\]

The polynomial slack in the last inequality is \(u^2(9-7u+2u^2)\ge0\). The one-dimensional lemma in y gives \(T(2n,W;\beta)\ge1-4u\). Its second application, now in x with \(v=5u\le1/40\), yields

\[
T(L,W;\beta)\ge1-20u.
\]

This is valid for all integers in the finite square of dimensions, not just the even or dyadic ones. Since \(1-20u>1/2\), the Gibbs maximum weight is greater than one half and the physical ground state is unique. Moreover

\[
e^{-\beta\Delta_{L,W}}\le\frac{20u}{1-20u}.
\]

The coarser bound \(20u/(1-20u)\le32u\), together with the unchanged contraction, also extends the complete asymptotic two-dimensional entry theorem to \(u\le1/200\). For the missing finite bridge below, retaining the sharper ratio gives the better number needed to match the later asymptotic gap.

## 7. Explicit short-size bridges

### Coupling \(g=1/100\)

The independent-rung product trial and the full-space Weyl bound give \(\Delta_L\ge1-3gL^2\). At \(L=2,3\), this is at least \(73/100\), exceeding the optimized gap. The accepted seed and all-integer interpolation cover every \(L\ge4\).

### Coupling \(g=1/50\): sides two through seven

Take one rational local comparison \(a=1/20\), \(b=9/2500\). It passes the exact squared-root inequality in Section 3. Then \(\alpha=4/5\) and, for every \(N=L^2\le49\),

\[
\Delta_L\ge1-4a-2Nb\ge\frac{559}{1250}=0.4472.
\]

Here the singlet product gives \(E_0\le E_{00}\) and min–max gives \(E_1\ge E_{00}+\alpha-2Nb\); their strict separation proves uniqueness. This argument uses the full spectrum and applies equally to odd sizes and the doubled length-two bonds.

### Coupling \(g=1/50\): sides eight through sixteen

The saved intermediate canonical scalar state has base side \(n=8\), \(\beta=49\), and common defect

\[
u_8=\frac{824510061961837007512221169432696865}{340282366920938463463374607431768211456}
\approx0.0024230173000806842<1/200.
\]

Section 6 therefore applies for every integer \(8\le L,W\le16\). Its Gibbs-weight ratio is at most

\[
r=\frac{4122550309809185037561105847163484325}{80948041420425430828282546010778568539}.
\]

The independent rational exponential enclosure verifies

\[
e^{49(0.060761949098)}r<1.
\]

Consequently every square with \(8\le L\le16\) has \(\Delta_L\ge0.060761949098\), strictly above the exact accepted later gap. This bridge uses a certified intermediate thermal state and not a new many-body diagonalization.

The accepted \(n=16,\beta=98\) seed covers all integers \(L\ge16\) with the exact optimized gap of Section 5. Combining the three ranges proves the all-integer \(L\ge2\) result stated in Section 1.

## 8. Reproduction and remaining limits

From the repository root run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python research_20261010/bilayer_audit/verify_optimized_bilayer.py
```

Only `research_20261010/bilayer_audit/optimized_bilayer_audit.json` is written. The script sets a two-GiB address-space cap and at-most-two-CPU affinity itself. Python 3.12, NumPy and SymPy suffice; SciPy is not used.

The original input files remain unchanged. This audit retains the archived candidates' exact integer vectors and checks their consequences independently; it does not assert an independently discovered optimal variational vector. No proof-assistant formalization, infinite-volume ground-state uniqueness theorem, stronger-coupling extrapolation, or uniform Heisenberg-model result is claimed. The ordinary bilayer remains distinct from the separately studied fully frustrated bilayer.
