# A complete route to the uniform periodic spin-one gap

Evidence checkpoint: 2026-10-11 02:56 UTC. This guide explains an accepted finite-volume theorem and its exact computational dependencies. The exposition and its lightweight consistency check are new. They are not a replacement for the independent physical and scalar reviews cited below.

## 1. The theorem, before the machinery

Let each site carry the self-adjoint spin-one representation, with

\[
 [S^\alpha,S^\beta]=i\sum_\gamma\varepsilon_{\alpha\beta\gamma}S^\gamma,
 \qquad (S^x)^2+(S^y)^2+(S^z)^2=2I_3.
\]

For every integer \(L\ge2\), work on the full physical space
\(\mathcal H_L=(\mathbb C^3)^{\otimes L}\) and use the Hamiltonian

\[
 H_L=\sum_{j=0}^{L-1}\mathbf S_j\cdot\mathbf S_{j+1},
 \qquad \mathbf S_L=\mathbf S_0.
 \tag{1}
\]

The bilinear coupling is exactly one. The boundary is periodic and untwisted. There is no biquadratic interaction, anisotropy or magnetic field. At \(L=2\), the sum in Eq. (1) contains two terms on the same pair, so \(H_2=2\mathbf S_0\cdot\mathbf S_1\).

**Accepted finite-volume theorem.** The ground energy of \(H_L\) has multiplicity one and the next distinct energy satisfies

\[
 \gamma_L=E_1(L)-E_0(L)\ge\delta,
 \qquad \delta=\frac{31}{1250}=0.0248,
 \qquad\text{for every integer }L\ge2.
 \tag{2}
\]

The final composition is independently accepted in [A, Sections 1–4]. Its review manifest is

`5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf`.

The coverage is

\[
 \{2,3\}\ \cup\ \{4,\ldots,25\}\ \cup\ \{26,\ldots,33\}
 \ \cup\ \{L\in\mathbb Z:L\ge34\}.
 \tag{3}
\]

The last piece uses a canonical bootstrap initialized at \(n=34\), with a physical trial state at \(2n=68\). The smallest separately certified canonical initialization is \(n=30\), at the weaker bound \(0.0179\). Neither fact makes the initialization for Eq. (2) equal to 30 or 2. No minimal initialization, optimal lower bound, or exact physical gap is claimed.

Equation (2) implies a positive lower bound on the finite-volume gap liminf. It does not by itself identify all infinite-volume ground states or prove their uniqueness. The theorem concerns finite periodic Hamiltonians in precisely the normalization of Eq. (1).

### 中文摘要

在单位双线性交换的无扭转周期 spin-1 Heisenberg 链上，已独立验收所有整数 \(L\ge2\) 的唯一基态与统一能隙下界 \(0.0248\)。证明由 \(L=2,3\) 的角动量代数、\(4\le L\le33\) 的有限尺寸证书和从 \(n=34\) 启动的无限尺寸 bootstrap 拼接而成。另有 \(n=30\) 启动的 \(0.0179\) 证书，但不能把全尺寸覆盖起点 2 或较弱启动点 30 当成 \(0.0248\) 的启动点。以下推导区分原论文框架、精确算术、向外舍入、独立复核与浮点候选，不把试探态维数当成完整物理空间维数。

## 2. The two traces and the central proof idea

Set

\[
 a=\frac{700741}{500000},\qquad
 H'_L=H_L+aLI,\qquad
 Z_L(\beta)=\operatorname{Tr}_{\mathcal H_L}e^{-\beta H'_L},
 \qquad \beta>0.
 \tag{4}
\]

This is the ordinary, unnormalized trace over all \(3^L\) physical states. The shift changes every energy by the same amount and leaves \(\gamma_L\) unchanged.

The normalized Gibbs state and its physical purity are

\[
 \rho_L(\beta)=\frac{e^{-\beta H'_L}}{Z_L(\beta)},\qquad
 T(L,\beta)=\operatorname{Tr}\rho_L(\beta)^2
 =\frac{Z_L(2\beta)}{Z_L(\beta)^2}.
 \tag{5}
\]

The second description uses a compact self-adjoint *spatial* transfer operator \(X_\beta\). For every integer \(L\ge4\), the original source proves

\[
 Z_L(\beta)=\operatorname{Tr}X_\beta^L
 =\sum_i\lambda_i(\beta)^L.
 \tag{6}
\]

Its eigenvalues \(\lambda_i\) are real and may be negative. They are not energy eigenvalues of \(H_L\). For even \(n\ge4\), define the spatial purity

\[
 S(n,\beta)=\frac{Z_{2n}(\beta)}{Z_n(\beta)^2}
 =\sum_i\left(\frac{|\lambda_i(\beta)|^n}{Z_n(\beta)}\right)^2.
 \tag{7}
\]

Thus both \(S\) and \(T\) are purities, but they square different distributions. The bootstrap exploits their exact algebraic relationship. A finite set of certified traces and one physical trial state first bound \(S(n,\beta)\) and \(T(2n,\beta)\). Alternating spatial and thermal squaring makes their defects shrink quadratically. A separate interpolation argument fills every integer length between successive doubled sizes. Finite certificates cover the lengths below the bootstrap onset.

A one-dimensional trial span only supplies a lower bound on the numerator of Eq. (5). The denominator bounds the full thermal trace. This second ingredient is what controls states outside the trial span. A good trial energy or a small residual alone would not prove Eq. (2).

## 3. Why a purity bound proves both uniqueness and a gap

Let \(p_0\ge p_1\ge\cdots\ge0\) be the normalized Gibbs weights, counted with physical multiplicity. Suppose

\[
 \sum_j p_j^2\ge C>\frac12.
\]

Since \(\sum_jp_j^2\le p_0\sum_jp_j=p_0\), we have \(p_0\ge C>1/2\). The largest weight cannot occur twice. Therefore the physical ground state is unique, without having been assumed unique in constructing \(C\). Moreover

\[
 e^{-\beta\gamma_L}=\frac{p_1}{p_0}
 \le\frac{1-p_0}{p_0}\le\frac{1-C}{C}.
 \tag{8}
\]

It is sufficient to verify the directed inequality

\[
 C-e^{\beta\delta}(1-C)>0.
 \tag{9}
\]

The certificates verify Eq. (9) with an upper enclosure for the exponential and a lower enclosure for \(C\). Their strict margins imply a gap strictly greater than the target whenever this lemma is used. Equation (2) records the conservative non-strict rational endpoint. The analytic gaps at 2 and 3 also exceed that endpoint.

## 4. The physical spatial-transfer identity, including odd lengths

This is inherited from the original framework [O2], with its scope checked in [S]. It is useful to spell out why parity does not change the physical Hamiltonian.

In a Cartesian spin basis, let \(G_\alpha=iS^\alpha\). Each \(G_\alpha\) is real and has operator norm one, and

\[
 -\mathbf S\cdot\mathbf S=\sum_\alpha G_\alpha\otimes G_\alpha.
 \tag{10}
\]

A bond history is an ordered list of event times in \((0,\beta)\), each carrying one of three labels \(\alpha\). Include an empty history of mass one. Lebesgue measure on every labeled time simplex gives a finite measure \(\mu_\beta\) of total mass

\[
 \sum_{k\ge0}\frac{3^k\beta^k}{k!}=e^{3\beta}.
\]

For two histories \(x,y\), merge their events in time order and take the trace of the resulting product of the \(3\times3\) matrices \(G_\alpha\). Call this real kernel \(k_\beta(x,y)\). Its absolute value is at most 3. Interchanging the histories does not change the merged chronological list, so \(k_\beta(x,y)=k_\beta(y,x)\). No reversal of a noncommuting chronological product is used.

The associated integral operator \(K_\beta\) on \(L^2(\mu_\beta)\) is real, self-adjoint and Hilbert–Schmidt. Set

\[
 X_\beta=e^{-a\beta}K_\beta.
\]

It is compact and has a countable real spectrum with \(\sum_i|\lambda_i|^k<\infty\) for every integer \(k\ge2\). A product-of-Hilbert–Schmidt trace formula expresses \(\operatorname{Tr}K_\beta^L\) as a cyclic integral of kernels. Expanding the physical exponential in ordered bond events gives that same integral. At total degree \(k\), the sum of absolute traced contributions is at most \(3^L(3L\beta)^k/k!\), so regrouping histories is justified by absolute convergence. Equation (6) follows after inserting the scalar shift.

The same construction gives a real unitary history representation \(U_g\) for proper signed Cartesian rotations, commuting with \(X_\beta\), and

\[
 Z_L(\beta,g)=\operatorname{Tr}(X_\beta^L U_g),\qquad L\ge4.
 \tag{11}
\]

Here \(H_L(g)\) rotates only the closing bond on its site-0 factor,

\[
 H_L(g)=\sum_{j=0}^{L-2}h_{j,j+1}
 +\sum_\alpha S_{L-1}^\alpha(gS^\alpha g^{-1})_0,
 \qquad h=\sum_\alpha S^\alpha\otimes S^\alpha,
\]

and \(Z_L(\beta,g)=\operatorname{Tr}e^{-\beta(H_L(g)+aLI)}\). These physical partition functions are positive. The identity case is the untwisted chain at odd as well as even length. Equation (10) is an onsite choice of basis, not a staggered transformation. It leaves no extra twist on odd rings.

Only the even powers in Eq. (7) are probabilities. Equation (6) itself holds for every integer \(L\ge4\). The guide does not extend the source proposition to \(L=2,3\). Those lengths are treated directly in Section 12.

## 5. Eighteen finite thermal inputs, with full-space error control

The second-input route uses \(\beta_0=49/4\), each length \(4\le L\le12\), and two closing-bond rotations, the identity \(I\) and a \(\pi\) rotation \(P\). These are two seams at the same temperature. They are not two temperatures.

### 5.1 Integer columns approximate a physical matrix exponential

In the weight basis \(s\in\{-1,0,1\}\), a Heisenberg bond has diagonal \(st\) and permitted opposite-unit-step coefficients one. Total magnetization is conserved. In each magnetization block define

\[
 D_L=32I-3LI-2H_L(g),\qquad R_L^{\rm heat}=D_L/32.
 \tag{12}
\]

The diagonal is \(32-3L-2\sum_js_{j-1}s_j\). Each hopping entry is \(-2\), except for \(+2\) on the \(P\) seam. The source energy bound

\[
 -\frac{3L}{2}I\le H_L(g)\le LI
 \tag{13}
\]

makes \(R_L^{\rm heat}\) a self-adjoint contraction for \(4\le L\le12\). The upper bound uses the two-spin eigenvalues \(-2,-1,1\). For the lower bound, the open three-site inequality \(h_{12}+h_{23}\ge-3I\) follows from an absolute weighted-row bound using weights 4, 3, 2, 2 for the word patterns \(aaa\), \(aab/abb\), \(aba\), \(abc\). Every weighted row sum is at most three times its weight. Seam-crossing open triads are unitarily equivalent to ordinary triads. Summing all triad inequalities counts each bond twice and proves Eq. (13) [O1].

With \(Q=2^{55}\), the desired half-temperature operator is

\[
 F_L=\exp\left[-\frac{\beta_0}{2}
       \left(\frac{3L}{2}I+H_L(g)\right)\right]
 =\exp[98(R_L^{\rm heat}-I)].
\]

Consequently

\[
 Z_L(\beta_0,g)=e^{x_L}\|F_L\|_F^2,
 \qquad x_L=\beta_0L(3/2-a).
 \tag{14}
\]

Conditioned Poisson weights \(p_j\), proportional to \(98^j/j!\) for \(0\le j\le280\), are rational. Truncation and renormalization have operator error less than \(2^{-84}<Q^{-1}\). For a selected basis column \(e_r\), the integer Horner procedure starts with zero and applies

\[
 X\leftarrow\left\lfloor D_LX/32\right\rfloor
          +\lfloor Qp_j\rfloor e_r,
 \qquad j=280,279,\ldots,0.
 \tag{15}
\]

The vector floor means mathematical floor, including at negative entries. It does not mean truncation towards zero. Although the integer coefficients above degree 191 vanish, the error proof charges all 281 rational steps.

Put

\[
 d_L=\lfloor\sqrt{3^L}\rfloor+1,\quad
 E_L=281(d_L+1)+1,\quad \mathcal E_L=d_LE_L.
\]

Contraction of \(R_L^{\rm heat}\), coordinate rounding and the coefficient error give \(\|X-QF_Le_r\|_2\le E_L\). The integer kernel's row absolute sum is at most 76 and every intermediate coordinate has magnitude less than \(2Q\). Thus sparse products and partial sums are bounded by \(76\cdot2Q<2^{63}-1\). The square and aggregate stages use independently checked exact wide-integer/GMP accumulation [P].

### 5.2 Symmetry reduction does not omit physical states

Selected columns represent cyclic, reflection and spin-negation orbits. At positive total magnetization the multiplicity includes the negative partner. At zero magnetization, negation is included in the orbit itself and is not counted twice. Stabilizers are handled by actual orbit cardinalities. For the \(P\) seam, translation is accompanied by a diagonal \(\pi\)-gauge on an arc, restoring the seam. This works on odd rings too.

For representative multiplicities \(\nu_r\), the coverage check is

\[
 \sum_r\nu_r=3^L,\qquad
 W_{L,g}=\sum_r\nu_r\|X_r\|_2^2\in\mathbb Z_{\ge0}.
\]

The rounded columns need not respect the signed translation symmetry. Instead, compare direct sums that repeat each computed representative and its exact counterpart \(\nu_r\) times. The triangle inequality then proves

\[
 \left|\sqrt{W_{L,g}}-Q\|F_L\|_F\right|<\mathcal E_L.
 \tag{16}
\]

### 5.3 Exact rational trace intervals

Let \(r=\lfloor\sqrt{W_{L,g}}\rfloor\),
\(s=\sum_{j=0}^{100}x_L^j/j!\), and \(t=x_L^{100}/100!\).
Because \(0<x_L<15\), the omitted exponential tail is at most \(15t/86<t\). Hence

\[
 \underline Z_{L,g}=
 \frac{s\max(0,r-\mathcal E_L)^2}{2^{110}},\qquad
 \overline Z_{L,g}=
 \frac{(s+t)(r+1+\mathcal E_L)^2}{2^{110}}
 \tag{17}
\]

are rigorous endpoints. The refined inputs round the lower endpoint down and the upper endpoint up to the \(10^{-18}\) grid. Merely using the original center \(\pm30\times10^{-6}\) table would not reproduce the improved proof.

All 18 physical inputs have been independently accepted [P]. That review independently reconstructs physical matrices and orbit coverage, checks all 2,428 checkpoints and exact integer aggregates, and maps Eq. (17) to the refined moment intervals. Matching a published integer alone is not its physical proof. The historical conditional labels in [M] and [B] remain unchanged, but their thermal premises were explicitly discharged by [P]. This guide does not run a new heat-trace campaign.

## 6. Signed sectors and finite moments

Use the rotation group \(D_2=\{I,P_x,P_y,P_z\}\). Its character projections commute with \(X_{\beta_0}\). The cyclic rotation permutes the three nontrivial character spaces, making their transfer spectra identical. Let \(J_k\) be the moment on the invariant space and \(N_k\) that on one nontrivial space. Then

\[
 J_k=\frac{Z_k(\beta_0,I)+3Z_k(\beta_0,P)}4,
 \qquad
 N_k=\frac{Z_k(\beta_0,I)-Z_k(\beta_0,P)}4,
 \qquad Z_k=J_k+3N_k.
 \tag{18}
\]

Both \(J\) and \(N\) are actual countable eigenvalue lists. Each eigenvalue occurrence has unit multiplicity within its list, while the full transfer contains three copies of \(N\). The invariant list \(J\) is not assumed one-dimensional. It contains the original finer sectors \(I+2O\).

Every moment in Eq. (18) is \(\sum_i\lambda_i^k\), not \(\sum_i|\lambda_i|^k\) and not a moment of \(\lambda_i^2\). In particular, all four odd \(N_k\) intervals for \(k=5,7,9,11\) are strictly negative. Subtraction reverses endpoints,

\[
 \underline N_k=(\underline Z_{k,I}-\overline Z_{k,P})/4,
 \qquad
 \overline N_k=(\overline Z_{k,I}-\underline Z_{k,P})/4.
 \tag{19}
\]

For any coefficients \(c_k\), a conservative upper bound on \(\sum_kc_kM_k\) is

\[
 \sum_{c_k\ge0}c_k\overline M_k+
 \sum_{c_k<0}c_k\underline M_k.
 \tag{20}
\]

The intervals can be used simultaneously even though they arise from shared physical traces. Enlarging the feasible data to an interval box is conservative. It does not assert that all adverse endpoints are jointly attainable or that sector data are independent.

### 6.1 Whole-ray support exclusion

For a degree-four rational polynomial \(q\), the filter
\(F(x)=x^4q(x)^2\) is nonnegative. Its sum over one sector is a combination of moments 4 through 12. If the interval upper sum is \(B\), every eigenvalue occurrence \(\lambda\) obeys \(F(\lambda)\le B\).

For each of the positive and negative rays in each sector, [M] supplies a rational \(q\) and a rational radius \(r\). The exact checks are

\[
 r^4q(\pm r)^2>B
\]

and positivity of all coefficients of \(q(\pm(r+y))\) as a polynomial in \(y\ge0\). This proves that the filter stays above \(B\) throughout the entire exterior ray. An endpoint check alone would not do so.

The resulting open supports are

\[
 -0.6501774659<\lambda_J<1.0013390453,
 \qquad
 -0.8710299903<\lambda_N<0.7502278231.
 \tag{21}
\]

These terminating decimals are exact rational cap values, not rounded estimates. The four exact filters are in `EXACT_DATA.json` under `filters`.

The unit-atom interpretation is essential. One can also write the necessary condition
\(H-t^4v(t)v(t)^T\succeq0\), where \(H_{ij}=M_{4+i+j}\) and \(v(t)=(1,t,\ldots,t^4)^T\). Removing an eigenvalue occurrence removes unit mass. Arbitrary fractional masses do not justify the same exclusion. The actual accepted proof uses direct rational filters, not a numerically inverted moment matrix. Method-specific midpoint nonexclusion tests do not establish physical realizability or global optimality.

### 6.2 Certified long-moment majorants

For a desired order \(k\), take an exact rational polynomial \(p\) of degree eight and prove

\[
 p(x)-x^{k-4}\ge0\quad\text{on the entire closed support interval}.
 \tag{22}
\]

Multiplying by \(x^4\ge0\) proves \(x^4p(x)\ge x^k\), including at zero and for negative \(x\). This avoids division by \(x\) and preserves the sign of an odd target power.

The proof of Eq. (22) is exact Bernstein arithmetic. After mapping the full interval to \([0,1]\), write the complete polynomial, including the target term, in the Bernstein basis of its full degree. Nonnegative Bernstein coefficients certify nonnegativity. When a coefficient is negative, subdivide the interval by exact midpoint de Casteljau arithmetic. Every terminal leaf must have all coefficients nonnegative. A grid of sampled values or a floating extremum search is insufficient.

Summing Eq. (22) gives an upper bound using Eq. (20). Absolute convergence follows from bounded support and finite fourth/twelfth moments. For intermediate powers, \(|x|^j\le |x|^4+|x|^{12}\) for \(4\le j\le12\). Higher powers are bounded by a constant times \(|x|^{12}\).

The n30/32/34 package verifies 26 even-sector majorants, including orders 24, 26, 28, 30, 32, 34, 64 and 68 [I]. The finite-prefix package additionally verifies 14 majorants at orders 13, 14, 15, 17, 19, 21 and 23 [F]. Negative odd \(N\)-upper bounds remain negative. All coefficients and their exact upper sums are retained in `EXACT_DATA.json`.

### 6.3 Capped-mass bounds

For \(m\ge0\) and \(h>0\), a finite or countable family \(0\le y_i\le h\), \(\sum_i y_i\le m\), and exponent \(r\ge1\), define

\[
 \mathcal C(m,h,r)=qh^r+(m-qh)^r,\qquad q=\lfloor m/h\rfloor.
 \tag{23}
\]

Then \(\sum_i y_i^r\le\mathcal C(m,h,r)\). For a finite family, moving mass from a smaller unsaturated coordinate to a larger one increases the convex power sum until all but one coordinate are 0 or \(h\). The expression is nondecreasing in total mass. Taking finite-subfamily limits proves the countable case. Without individual caps, \(\sum_i y_i^r\le m^r\).

Apply Eq. (23) to \(y_i=|\lambda_i|^{12}\). The exact twelfth-moment upper bounds are

\[
 m_J=\frac{66606415448354239}{62500000000000000},\qquad
 m_N=\frac{556584262998464971}{2000000000000000000}.
 \tag{24}
\]

With \(U=1.0013390453\) and \(V=0.8710299903\), an even \(k\ge12\) has the valid bounds \(\mathcal C(m_J,U^{12},k/12)\) and \(\mathcal C(m_N,V^{12},k/12)\). Take the smaller of a packing bound and a proved polynomial bound when both are available. Denote the resulting sector bounds by \(B_J(k),B_N(k)\), and put

\[
 Q_k=B_J(k)+3B_N(k)\ge Z_k(\beta_0).
 \tag{25}
\]

No spectral-rank cutoff is used.

## 7. What the MPS contributes, and what it does not

Use the fixed real integer matrices \(A_{-1},A_0,A_1\in M_{26}(\mathbb R)\) from the original trial construction [O5]. For each required physical length \(L\), define

\[
 \psi_L(s_0,\ldots,s_{L-1})
 =\operatorname{Tr}(A_{s_0}\cdots A_{s_{L-1}}).
 \tag{26}
\]

The same tensor can define different physical states at different lengths. Each length must use its own contraction. Define the finite MPS norm-transfer matrix and insertion

\[
 \mathcal A=\sum_s A_s\otimes A_s,\qquad
 \mathcal O=\sum_{s,t,u,v}h_{st,uv}
          (A_sA_t)\otimes(A_uA_v).
\]

The real-amplitude contractions are

\[
 N_L=\operatorname{Tr}\mathcal A^L=\|\psi_L\|^2,
 \qquad U_L=\operatorname{Tr}(\mathcal A^{L-2}\mathcal O),
 \qquad H_L^{\rm num}=L U_L.
 \tag{27}
\]

The last factor \(L\) is required because \(U_L\) is a single-bond insertion. Some archived files use `U72` for this single-bond value. The newer `H0_L` files already contain \(H_L^{\rm num}\), the total energy numerator. Their shifted Rayleigh quotient is

\[
 \mathcal R_L=\frac{H_L^{\rm num}}{N_L}+aL
 =L\left(\frac{U_L}{N_L}+a\right),\qquad N_L>0.
 \tag{28}
\]

It must not be multiplied by \(L\) a second time.

For the normalized trial, spectral Jensen gives

\[
 Z_L(2\beta)\ge
 \langle\widehat\psi_L,e^{-2\beta H'_L}\widehat\psi_L\rangle
 \ge e^{-2\beta\mathcal R_L}.
 \tag{29}
\]

Equivalently, use the variational inequality \(E'_0(L)\le\mathcal R_L\). No prior uniqueness is needed. If \(\mathcal R_L<0\), then \(Z_L(b)>1\) at every \(b>0\). If \(\mathcal R_L>0\), Eq. (29) still holds, but its right side is less than one and that penalty must be retained. The odd length 25 is an important example.

There are three distinct sizes here.

- The physical Hilbert-space dimension is \(3^L\).
- The retained linear trial span has dimension one.
- The MPS bond dimension is \(D=26\), and \(\mathcal A\) has matrix dimension \(D^2=676\).

Neither 26 nor 676 is a rank bound on the physical thermal transfer \(X_\beta\). The proof never substitutes \(\mathcal A\) for \(X_\beta\).

The accepted reviews reconstruct the fixed tensor entries and physical bond insertion independently, verify the charge-difference blocks, check tiny direct amplitudes and use exact sequential integer contractions distinct from the producer's binary-power implementation. The original tensor design is credited to [O5]. The later length-specific exact contractions are verification inputs, not new tensor optimization.

## 8. The actual n34 initialization for the stronger theorem

At \(n=34\), the independently rebuilt 68-site contraction has \(N_{68}>0\) and \(\mathcal R_{68}<0\). Its displayed shifted total trial value is about \(-8.32217861\times10^{-6}\). The exact fraction, not its decimal display, supplies \(Z_{68}(b)>1\) [I].

Take the exact rational

\[
 \ell=\frac{9999962631}{10^{10}}.
\]

The certificate checks

\[
 \mathcal C(m_J,\ell^{12},68/12)+3B_N(68)<1.
 \tag{30}
\]

If every \(J\) eigenvalue had modulus at most \(\ell\), Eq. (30) would contradict \(Z_{68}(\beta_0)>1\). Thus there is an occurrence \(\lambda_0\) in \(J\) with \(|\lambda_0|>\ell\). The negative \(J\) support cap is less than \(\ell\), so \(\lambda_0>0\). Also \(\ell>V\), so this occurrence dominates all \(N\) eigenvalues.

After removing it, the residual twelfth mass of \(J\) is at most

\[
 r_J=m_J-\ell^{12},\qquad 0<r_J<\ell^{12}.
\]

This last inequality rules out a second \(J\) occurrence of modulus greater than or equal to \(\ell\). Let

\[
 A_{34}=r_J^{34/12}+3B_N(34).
\]

Retaining the dominant numerator \(\lambda_0^{68}\) in the spatial purity and bounding its denominator gives

\[
 S(34,\beta_0)\ge
 \left(1+\frac{A_{34}}{\ell^{34}}\right)^{-2},\qquad
 T(68,\beta_0)\ge Q_{68}^{-2}.
 \tag{31}
\]

The second bound uses Eq. (29) in its weaker form \(Z_{68}(2\beta_0)>1\). All powers and rounding directions in Eq. (31) are certified by integer-root enclosures. The accepted saved lower endpoints have decimal displays

\[
 S_0\simeq0.9464711505468461,
 \qquad T_0\simeq0.8332246829370601.
 \tag{32}
\]

The exact forcing margin in Eq. (30) is positive, about \(4.38714\times10^{-9}\). It is checked rationally. The full fractions for \(\ell,A_{34},Q_{68},S_0,T_0\), the trial quotient and every later state are in `EXACT_DATA.json` under `bootstrap_rows`.

The same accepted package gives distinct chains

| Canonical base \(n\) | Physical anchor \(2n\) | Initial temperature | Certified tail gap | Tail begins |
|---:|---:|---:|---:|---:|
| 30 | 60 | \(49/4\) | \(179/10000=0.0179\) | every integer \(L\ge30\) |
| 32 | 64 | \(49/4\) | \(49/2000=0.0245\) | every integer \(L\ge32\) |
| 34 | 68 | \(49/4\) | \(31/1250=0.0248\) | every integer \(L\ge34\) |

Only the final row supplies the infinite tail of Eq. (2).

## 9. Deriving the staggered purification recurrence

First consider any probability distribution \((p_i)\) with purity \(z=\sum_i p_i^2\). Squaring and renormalizing gives \(\widetilde p_i=p_i^2/z\). Then

\[
 1-\sum_i\widetilde p_i^2
 =\frac{2\sum_{i<j}p_i^2p_j^2}{z^2}
 \le\frac{(1-z)^2}{2z^2},
\]

because \(1-z=2\sum_{i<j}p_ip_j\). Define

\[
 G(z)=1-\frac{(1-z)^2}{2z^2},\qquad 0<z\le1.
 \tag{33}
\]

It is increasing on this interval. Spatial squaring proves \(S(2n,\beta)\ge G(S(n,\beta))\) for even \(n\), while physical squaring proves \(T(L,2\beta)\ge G(T(L,\beta))\).

The exact exchange identity follows directly from the four traces,

\[
 S(n,2\beta)T(n,\beta)^2
 =T(2n,\beta)S(n,\beta)^2.
 \tag{34}
\]

Suppose the current certified state consists of lower bounds

\[
 s\le S(n,\beta),\qquad t\le T(2n,\beta).
\]

Since \(T(n,\beta)\le1\), Eq. (34) gives \(S(n,2\beta)\ge s^2t\). Spatial squaring gives the next bound

\[
 s'\le G(s^2t)\le S(2n,2\beta).
\]

Using Eq. (34) at length \(2n\), with \(S(2n,\beta)\le1\), yields
\(T(4n,\beta)\ge t^2s'\). Thermal squaring then gives

\[
 \boxed{s'=G(s^2t),\qquad t'=G(t^2s')},
 \qquad (n,\beta)\longmapsto(2n,2\beta),
 \tag{35}
\]

where practical certificates round each new lower endpoint downward. The second update uses the **new** spatial endpoint. At the new coordinate, \(t'\) bounds \(T(4n,2\beta)\). The pair is always \(S(n,\beta),T(2n,\beta)\), never \(S(n,\beta),T(n,\beta)\). Every actual recurrence argument and saved output lies in its checked positive domain [I, M].

## 10. Filling every integer window, including odd lengths

Fix a certified state \((n,\beta,s,t)\) with even \(n\), and let

\[
 K=s^2t>\frac12,\qquad
 w=\frac{1+\sqrt{2K-1}}2,\qquad
 \rho=\frac{1-w}{w},\qquad d=\frac{t}{1+\rho^2}.
 \tag{36}
\]

By Eq. (34), the probability distribution of normalized \(n\)-th powers of \(X_{2\beta}\) has purity at least \(K\). Its largest weight \(p\) obeys \(p\ge K>1/2\). Also
\(K\le\sum_i p_i^2\le p^2+(1-p)^2\), so \(p\ge w\). There is a unique largest-modulus transfer eigenvalue \(\mu_0\), and

\[
 \sum_{i\ne0}\left|\frac{\mu_i}{\mu_0}\right|^n\le\rho<1.
 \tag{37}
\]

### 10.1 The leading eigenvalue has positive sign

If \(\mu_0<0\), the signed dominant term in every sufficiently large odd moment would be negative. The relative absolute tail tends to zero by dominated convergence applied to the summable sequence in Eq. (37). Equation (6) identifies those odd moments with positive physical Gibbs traces. This is a contradiction. Thus \(\mu_0>0\). Subleading eigenvalues can still be negative. No entrywise positivity of the kernel or positivity of its whole spectrum is assumed.

### 10.2 Numerator and denominator estimates

Let \(n\le L\le2n\) be any integer and put \(\alpha=L/(2n)\in[1/2,1]\). From Eq. (37), the relative absolute tail at \(L\) is at most \(\rho\) and at \(2n\) at most \(\rho^2\). Hence

\[
 Z_L(2\beta)\ge
 \left(\frac{Z_{2n}(2\beta)}{1+\rho^2}\right)^\alpha(1-\rho).
 \tag{38}
\]

At temperature \(\beta\), absolute-spectrum Hölder interpolation between the even exponents \(n\) and \(2n\) gives

\[
 0<Z_L(\beta)\le\sum_i|\lambda_i|^L
 \le Z_n(\beta)^{2-2\alpha}
       Z_{2n}(\beta)^{2\alpha-1}.
 \tag{39}
\]

Dividing Eq. (38) by the square of Eq. (39), and using the definitions of the purities, proves

\[
 T(L,\beta)\ge(1-\rho)s^{2-2\alpha}d^\alpha
 \ge C(s,t),
 \qquad
 C(s,t)=(1-\rho)\min\{s\sqrt d,d\}.
 \tag{40}
\]

The last step uses affine dependence of the logarithm on \(\alpha\), so its minimum is at an endpoint. A lower square-root enclosure in Eq. (36) increases \(\rho\) and decreases \(d\) and \(C\), preserving safety. Equation (40) requires no monotonicity of the physical gap or purity in length.

For n34, the saved windows are \([34\cdot2^j,68\cdot2^j]\), \(j=0,\ldots,9\), at \(\beta_j=(49/4)2^j\). Every saved lower purity satisfies Eq. (9) at \(\delta=31/1250\). The smallest displayed strict window margin is about \(0.08703\). Neighboring windows share endpoints, so there are no parity gaps or missing integer lengths.

## 11. Why finitely many iterations cover infinitely many lengths

Let \(u=\max\{1-s,1-t\}\), and suppose \(0<u\le1/100\). The first update in Eq. (35) obeys

\[
 1-s'\le
 \frac{u^2(3-3u+u^2)^2}{2(1-u)^6}<5u^2.
\]

Using \(s'\ge1-5u^2\) in the second update gives

\[
 1-t'\le
 \frac{u^2(2+5u)^2}{2(1-2u-5u^2)^2}\le5u^2.
 \tag{41}
\]

These inequalities use elementary rational bounds on the stated interval. For example, the first coefficient is at most \(9/[2(99/100)^6]<5\), and the second is bounded by its endpoint expression at \(u=1/100\).

For the integer-window bound, \(K\ge(1-u)^3\ge1-3u\). The inequalities

\[
 \sqrt{2K-1}\ge1-\tfrac72u,\qquad
 \rho\le\tfrac95u,\qquad
 d\ge1-\tfrac{26}{25}u
\]

hold for \(u\le1/100\). Since \(\sqrt d\ge d\), Eq. (40) implies

\[
 C\ge(1-9u/5)(1-51u/25)\ge1-4u,
 \qquad \frac{1-C}{C}\le5u.
 \tag{42}
\]

For the n34 route, the accepted terminal state is

\[
 n_*=17408,\quad \beta_*=6272,\quad
 u_*\simeq3.8272784677\times10^{-69},\quad
 5u_*e^{\beta_*\delta}<1.
 \tag{43}
\]

The last inequality is checked with exact rational endpoints and an upper exponential. Iterating Eq. (41) gives

\[
 u_j\le\frac{(5u_*)^{2^j}}5,\qquad
 \beta_j=2^j\beta_*.
\]

Therefore

\[
 5u_j e^{\beta_j\delta}
 \le\left(5u_*e^{\beta_*\delta}\right)^{2^j}<1
\]

for all \(j\ge0\). Equations (8) and (42) prove the same gap on every later integer window. This is an analytic infinite continuation. It does not continue fixed-precision rounding until it hits a floor. Combining it with Section 10 proves the tail for every integer \(L\ge34\).

## 12. Completing the finite prefix without changing the initialization

### 12.1 Exact volumes 2 and 3

At length 2,

\[
 H_2=2\mathbf S_0\cdot\mathbf S_1=\mathbf S_{\rm tot}^2-4I.
\]

The total spins \(j=0,1,2\) occur once, with energies \(-4,-2,2\) and dimensions 1, 3, 5. Thus the ground singlet is unique and the gap is 2.

At length 3,

\[
 H_3=(\mathbf S_{\rm tot}^2-6I)/2.
\]

Successive spin-one coupling gives representation multiplicities \(m_0=1,m_1=3,m_2=2,m_3=1\). The dimensions sum to \(1+9+10+7=27\). The energies are \(-3,-2,0,3\), so the ground singlet is unique and the gap is 1. The threefold *representation multiplicity* at total spin one must not be assigned to the singlet. Neither argument uses Eq. (6) below its source-verified range [F].

### 12.2 Direct certificates at lengths 4 through 23

Each length has its own exact D26 norm and total energy numerator [F]. For \(4\le L\le12\), use the physical *identity-seam* upper endpoint from Eq. (17), not the \(P\)-seam value. For \(13\le L\le23\), use the signed polynomial or packing upper bounds described in Section 6. Let the resulting full positive trace upper bound be \(Q_L\). Then

\[
 T(L,\beta_0)\ge
 \frac{\exp(-2\beta_0\mathcal R_L)}{Q_L^2}.
 \tag{44}
\]

At odd orders, the signed polynomial bound can be better than a bound on the absolute moment. In particular, negative odd \(N\) upper bounds are retained when forming \(J+3N\). Positive shifted trial energies at some odd lengths are also retained inside the exponential. Every displayed or saved purity is rounded downward.

### 12.3 The isolated length 24

The accepted 24-site purity was obtained differently [E24]. A negative shifted 48-site trial energy supplies the canonical seed values \(s\le S(24,\beta_0)\), \(t\le T(48,\beta_0)\), but this does not establish a successful n24 infinite bootstrap.

In the window proof, an even target length has a nonnegative numerator tail. At \(L=n=24\), Eq. (38) can omit \(1-\rho\). Hence

\[
 T(24,\beta_0)\ge s\sqrt{t/(1+\rho^2)}.
 \tag{45}
\]

The saved exact lower purity is about \(0.6813771416499027\). This is an individual finite-size certificate. A previous parity-window attempt at 25 failed to certify a purity above one half. That failure was a limitation of that bound, not an upper bound on the physical purity or evidence for gaplessness.

### 12.4 Direct odd length 25 and lengths 26 through 33

For odd \(L\ge5\), real transfer eigenvalues and Cauchy–Schwarz give

\[
 0<Z_L(\beta_0)\le\sum_i|\lambda_i|^L
 \le\sqrt{Z_{L-1}(\beta_0)Z_{L+1}(\beta_0)}.
 \tag{46}
\]

The neighboring exponents are even. Both traces in the last expression therefore retain their physical meaning despite signed subleading eigenvalues. With certified even upper traces,

\[
 T(L,\beta_0)\ge
 \frac{\exp(-2\beta_0\mathcal R_L)}{Q_{L-1}Q_{L+1}}.
 \tag{47}
\]

At 25, the own-length shifted trial energy is positive, about \(0.0042115764\), so the numerator bound is below one. Retaining it gives a purity lower bound about \(0.7059136372\) [E25]. Replacing it by one would be an invalid improvement.

At each of 26 through 33, [A] independently rebuilds the own-length norm and total energy integers. Even lengths use Eq. (44), and odd lengths use Eq. (47). The saved purity lower endpoints have the following decimal displays.

| Length | Purity lower endpoint, display |
|---:|---:|
| 26 | 0.8692559860 |
| 27 | 0.7567727545 |
| 28 | 0.8737925526 |
| 29 | 0.7949222602 |
| 30 | 0.8779999921 |
| 31 | 0.8228656865 |
| 32 | 0.8813220598 |
| 33 | 0.8428024167 |

The relevant denominator inputs are the exact even traces at 24, 26, 28, 30, 32 and 34, with the full \(J+3N\) multiplicity. No neighboring-length trial quotient is substituted for an odd numerator.

### 12.5 Why the old finite purities prove the larger gap

The earlier finite certificates often stated \(0.0023\). That label alone would not prove \(0.0248\). The stronger review retrieves the exact saved \(C_L\) at every length 4 through 25, checks its equality to the accepted earlier endpoint, and re-evaluates Eq. (9) with

\[
 \beta_0\delta=\frac{1519}{5000}.
\]

All 22 inequalities pass. The weakest cached purity is at 24. Its stronger-gap margin is about \(0.24964\). The eight new lengths 26 through 33 also pass. Combining them with the analytic 2/3 gaps and the n34 tail proves Eq. (2), with exactly the union in Eq. (3).

## 13. What is exact, what is enclosed, and what is only a proposal

**Exact mathematical identities.** These include the physical Hamiltonian, representation and sector decompositions, the history-transfer trace identity, MPS contraction identities, Jensen, purity-to-gap implication, purification recurrence, Hölder/Cauchy–Schwarz inequalities and the analytic infinite continuation.

**Exact finite arithmetic.** Integer matrix entries, orbit multiplicities, accumulated heat-column totals, MPS norm/energy contractions, rational polynomial coefficients, Bernstein subdivision and fraction comparisons are exact. Their scientific relevance still depends on correct physical construction, coverage and implementation bounds. A digest match alone establishes byte identity, not the physical interpretation.

**Directed rational enclosures.** Physical exponential approximation errors, integer square-root brackets, rational-power bounds, Taylor-exponential bounds and saved lower purities have explicit directions. For example, an upper denominator and a lower numerator give a lower purity. A negative exponent is handled by reciprocating a positive-exponent upper bound when that direction is needed. Enclosures are verified by integer or rational inequalities.

**Floating proposals and displays.** Optimization can suggest polynomial coefficients, caps, trial parameters, target gaps or candidate initialization sizes. Acceptance rationalizes and verifies the resulting proposal over its full required domain. Decimal displays, a failed grid search, or a near-zero residual neither prove the theorem nor establish optimality or impossibility. The source MPS tensor is fixed in this proof, not reoptimized here.

**Independent acceptance.** The relevant reviews use separately implemented scalar arithmetic and physical reconstruction where stated. The final physical campaign review checks all finite heat inputs. Later packages reuse those accepted inputs without claiming another physical rerun. This guide replays only selected scalar/data consistency checks. It must not be described as another independent full physical validation.

A separate execution-history issue remains explicit. The length-25 review mathematically accepted its exact output, but did not accept its reported 15-second resource compliance. It logged 25.9614 process CPU seconds and lacked sufficient post-exec measurements to explain the discrepancy. The cause remains unresolved [E25]. The later 26–33 guarded run has consistent independent timers and limits [A]. That does not retroactively resolve the earlier anomaly. Mathematical validity and resource-policy compliance are separate verdicts.

A further, separate event occurred while checking this guide. Its first scalar consistency replay reported 30.21035921 process CPU seconds against a declared 30-second CPU limit. The original script and output remain unchanged under `history/`, and strict measured 30-second compliance is not accepted. The cause was not diagnosed. No physical computation occurred. A subsequent replay uses a stated 60-second limit and a shorter rigorously bounded Taylor sum. This guide-specific record neither alters nor reopens the independently accepted physical theorem.

## 14. Comparison with the original paper and fair attribution

The original public source is *The periodic spin-one Haldane gap*, in the September 24, 2026 directory of `openai/math`. Its [introduction](https://github.com/openai/math/blob/main/preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/build/introduction.tex) states unique ground states and

\[
 \gamma_L>\frac4{105}\log\frac{80}{79}
 \simeq0.0004791917031184807
 \quad\text{for even }L\ge60,
 \tag{48}
\]

and

\[
 \gamma_L>\frac{\log20}{784}
 \simeq0.0038210870836147844
 \quad\text{for even }L\ge2304.
 \tag{49}
\]

These are the original comparators [O3, S]. The later archived \(0.005908566393\) result is an independently strengthened reproduction and is not the original theorem.

On their respective common even-length scopes, the new constant has exact ratio expressions

\[
 \frac{31/1250}{(4/105)\log(80/79)}
 =\frac{651}{1000\log(80/79)}
 \simeq51.7538176028648,
\]

\[
 \frac{31/1250}{\log(20)/784}
 =\frac{12152}{625\log20}
 \simeq6.49029960775952.
 \tag{50}
\]

These are ratios of **proved lower bounds**, not ratios of actual physical gaps. The exact ratios involve logarithms. Their decimal approximations are checked by rational logarithm enclosures in the guide's self-check.

The original framework already contains the self-adjoint spatial-history transfer construction, symmetry sectors, finite thermal certification, fixed D26 trial state, alternating purity bootstrap and two initialization routes. In particular, its stronger second route starts with \(S(36,49/4)\) and \(T(72,49/4)\), then takes six updates to the stated \((2304,784)\) theorem. It is incorrect to credit this project with inventing the n36 second initialization or to compare a new second-input initialization only against the first route's n60.

The original [thermal appendix](https://github.com/openai/math/blob/main/preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/build/thermal72.tex) already certifies a matrix-polynomial approximation to the physical exponential with explicit rounding and truncation errors. It does not require full exact diagonalization of the \(3^L\) physical Hamiltonian. The later work's contribution is not the removal of an ED premise that the source never had.

The improvements represented by the accepted dependencies are more specific.

1. The second-input physical thermal calculations have been reproduced and independently mapped to their refined rational intervals.
2. Signed moment support filters and whole-interval polynomial majorants yield stronger usable trace bounds.
3. Own-length exact MPS contractions enable separately certified n34, n32 and n30 starts.
4. The signed-spectrum interpolation proves every integer window, extending the original theorem's even-length scope using the original all-integer transfer identity.
5. Direct finite purities and exact low-volume algebra complete every \(L\ge2\), at the stronger common constant.

These are rigorous strengthening and verification results within the inherited framework. They are not a new discovery of the Haldane-gap framework, a proof of the actual gap value, or a minimum-seed theorem. The guide makes no further novelty claim.

## 15. Dependency map and reproduction boundary

The shortest logical chain is

1. **Physical meaning:** [O1, O2, S] establish Eq. (6), the seams and signs for every integer \(L\ge4\).
2. **Finite thermal inputs:** [P] establishes all 18 physical trace enclosures and their refined signed-moment mapping.
3. **Moment bounds:** [M] certifies support filters. [I] and [F] certify the relevant full-domain long-moment majorants.
4. **Physical trial inputs:** [O5] defines the tensor. [I], [F], [E25] and [A] independently verify the required length-specific contractions. [E24] pins its independently verified 48-site input.
5. **Unbounded tail:** [I] combines the n34 seed, exact staggered updates, every integer window and the analytic closure.
6. **Finite prefix:** [F], [E24], [E25] and [A] supply every length 2 through 33. [A] explicitly rechecks the stronger gap inequality rather than merely relabeling weaker conclusions.
7. **Final theorem:** [A] checks the union and accepts Eq. (2).

`DEPENDENCY_MAP.md` gives the concrete paths and manifest identities. `SOURCE_PINS.json` records the SHA-256 of every file consumed to build this guide, source Git-blob identities, and the accepted review-manifest pins. `EXACT_DATA.json` preserves the finite data used in the explanation, with original path/field provenance.

Run `python selfcheck.py` from this new directory for a bounded standard-library consistency check. It checks source identity, original-source blob hashes, exact scope/coverage, physical-to-signed moment endpoint mapping, the accepted finite purities at the stronger gap, the n34 recurrence/window/closure, and the numerical comparison. It does not execute producer scientific modules, contract a physical MPS, generate heat columns, optimize tensors or publish anything. Its output is `SELF_CHECK.json` only in this directory. Replaying an older review should be done in a disposable copy, since many archived checkers write their result files beside themselves.

### Source and evidence key

- **[O1]** Original `model.tex`, locally preserved at `../uniform_source_scope_review/sources/model.tex`. Energy normalization, seams and energy bound.
- **[O2]** Original `transfer.tex`, at `../uniform_source_scope_review/sources/transfer.tex`. Spatial-transfer proposition and sector lemma.
- **[O3]** Original `introduction.tex`, at `../uniform_source_scope_review/sources/introduction.tex`. The stated original gap theorem.
- **[O4]** Original `initialization.tex` and `thermal72.tex`, at `../uniform_second_moment_review/sources/`. Original n36 second initialization and physical matrix-polynomial trace certification.
- **[O5]** Original `trials.tex`, at `../uniform_second_moment_review/sources/trials.tex`. Fixed D26 tensor and physical norm/energy identities.
- **[S]** [Original-source scope reconciliation](../uniform_source_scope_review/SOURCE_SCOPE.md). Pins the original physical identity for all integers \(L\ge4\), while retaining the original gap theorem's even-length scope.
- **[B]** [Original second-input scalar review](../uniform_second_initialization_review/REVIEW.md). Original n36 route and its initially conditional scalar replay.
- **[P]** [Complete independent physical thermal review](../uniform_second_thermal_full_review/PROOF.md), plus `provenance_results.json`. Discharges all 18 thermal premises of the refined scalar proof.
- **[M]** [Independent signed-moment review](../uniform_second_moment_review/REVIEW.md), plus the pinned `../uniform_second_moment_optimization/certificate.json`. Signed supports and majorants, initially conditional on physical inputs subsequently accepted by [P].
- **[I]** [Independent smaller second-input initialization review](../uniform_smaller_second_initialization_review/PROOF.md), plus `scalar_results.json` and its pinned producer `certificate.json`. The n30/32/34 chains.
- **[F]** [Independent small-length completion](../uniform_small_lengths_completion_review/PROOF.md), plus `results.json`. Exact volumes 2/3 and direct lengths 4–23.
- **[E24]** [Isolated 24-site review](../uniform_n24_second_coverage_review/PROOF.md). Its exact purity and the distinction from a successful n24 bootstrap.
- **[E25]** [Direct 25-site review](../uniform_direct25_coverage_review/PROOF.md). Positive trial energy, odd Cauchy–Schwarz denominator and separate resource anomaly.
- **[A]** [Final all-size 0.0248 review](../uniform_gap_0248_all_sizes_review/PROOF.md), plus `results.json`. Own-length 26–33 verification, stronger recheck at 4–25, final composition and accepted scope.

The original source snapshots are unchanged and retain their upstream Apache-2.0 license and attribution in the cited source directories and `../uniform_source_license_supplement/`. The present guide is a new explanatory derivation. It does not claim authorship of those sources or silently modify a previously sealed proof.
