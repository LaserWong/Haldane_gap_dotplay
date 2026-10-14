# Independent reviews of project improvements

This document records the review of results derived after the uploaded baseline. It is separate from the original archive and does not alter its certificates.

## 1. Verified single-state certificate for the spin-1 dimer chain

The model has M periodic two-spin cells with spin-1 sites, inter-cell Heisenberg coupling 1, and intra-cell coupling g=1/20. Width W=1. Ground-only inputs use M=2 and 4 (physical Hilbert dimensions 81 and 6561), at beta = 10. Exactly one approximate vector is retained per Hamiltonian. Its dyadic integer coefficients are part of the certificate.

Verified lower purities: S>=0.930080341751, T>=0.946623580846. Two sequential rounds reach n*=8 cells, beta*=40, u=954102123/500000000000. The certified gap is **0.116303868802**.

The independent checker `independent/verify_ground_only.py` does not import the certificate generator's matrix, residual, exponential, or bootstrap routines and does not call an eigensolver. It reconstructs matrix-vector products from the graph and product-spin basis, verifies both exact Rayleigh quotients and squared residuals, reproduces both Temple intervals, and reconstructs all six recorded temperatures with rational exponential intervals. Full results and input SHA256 values are in `independent/certificate_s1_W1_g1d20_k0_audit.json`.

Completeness is genuinely full-space: H0 has unique ground E00=-2M and next energy E00+1. The perturbation lower bound is V>=-2Mg. Thus ordered Weyl gives lambda1(H)>=E00+1-2Mg. Every weak edge connects distinct strong dimers, so the dimer-product trial has energy E00. For M=2,4 the second-energy lower bound is strictly above E00, proving uniqueness and identifying the one state below it independently of the numerical sector. For the exactly rounded trial vector, Temple yields rho-residual^2/(lambda1_lower-rho)<=E0<=rho. The sector residual equals the full residual because total magnetization is conserved.

For all omitted states, ordered Weyl gives lambda_j(H)>=lambda_j(H0)+Vmin, j>=1. Summing their exponentials gives the certified tail $e^{-\beta(E_{00}+V_{\min}-E_{0,\mathrm{upper}})}[z_s(\beta)^M-1]$. This uses all unperturbed dimer multiplicities and does not guess a density of states.

The same product trial plus Weyl gives Delta_M>=1-M/10>=0.3 for 2<=M<=7. The already-audited all-integer interpolation applies for M>=8. Therefore the stated weaker gap covers **every integer M>=2**, with unique periodic ground state. It is stronger than the original width 0.03 analytic example for this particular spin-1 coupling, but does not certify a uniform Heisenberg chain.

## 2. Verified two-dimensional recursion and square-size interpolation

Let Z(a,b,t) be a torus partition function. Assume exact, real self-adjoint Hilbert–Schmidt directional transfer operators for each fixed transverse integer size and temperature, with trace identities for **all** propagated integer lengths>=2, in both x and y. Let n,m be even, and define

A=Z(2n,m,beta)/Z(n,m,beta)^2,
B=Z(2n,2m,beta)/Z(2n,m,beta)^2,
C=Z(2n,2m,2beta)/Z(2n,2m,beta)^2.

Using only directional/thermal purity<=1, the pre-square x purity is at least A^4 B^2 C. After squaring its density, let A'=1-f(1-A^4 B^2 C). The pre-square y purity is at least B^4 C^2 A', giving B'=1-f(1-B^4 C^2 A'). Finally the pre-square thermal purity is at least C^4 (A')^2 B', giving C'=1-f(1-C^4(A')^2B'). Here f(u)=u^2/[2(1-u)^2]. All dimensions and temperature double after a full cycle.

If all initial defects<=u<=0.01, the first coefficient f(7u)/u^2 is less than 28.33. The next two sequential estimates, using a'<=32u^2 and b'<=32u^2, have coefficient bounds less than 22.76 and 13.62. Hence u'<=32u^2. Alternatively, each intermediate new defect<=u and the uniform exponent-sum 7 argument suffices at each stage.

For arbitrary integers n<=L<=2n and m<=W<=2m, assume u<=1/500. The y transfer at fixed x=2n has leading normalized m-th power weight>=B>=1-u and absolute tail ratio<=u/(1-u). Its dominant eigenvalue is positive because all odd physical traces are positive. For a=W/m in [1,2], this gives

Z(2n,W,beta)>=Z(2n,m,beta)^a (1-u)^a [1-u/(1-u)].

Absolute-spectrum l^p monotonicity gives Z(n,W,beta)<=Z(n,m,beta)^a. Consequently

Sx(n,W,beta)>=(1-u)^3(1-2u)>=1-5u.

Apply the audited one-dimensional interpolation in y to (B,C), giving T(2n,W,beta)>=1-4u. Apply it in x at that fixed W, with common defect 5u<=0.01: T(L,W,beta)>=1-20u. Therefore the physical ground is unique and exp(-beta Delta)<=20u/(1-20u)<=32u.

The recursion gives u_j<=(32u_*)^(2^j)/32. For a square seed n*=m*, every integer square side L>=n* belongs to one common dyadic interval. Thus the conditional uniform all-square gap is log[1/(32u_*)]/beta*. A rectangular seed similarly covers same-scale boxes with bounded aspect ratio. **A single square seed has not proved all arbitrary aspect ratios.** The analytic transfer construction and a certified seed for a concrete genuinely two-dimensional model remain separate requirements.

## 3. Verified perturbation bound for even cycles

For the original disjoint-cell perturbations v_i, all v_i commute mutually. Their joint spectral projectors define a classical probability law under the unperturbed strong-dimer Gibbs state, even though V need not commute with H0. For even M, split cells into even/odd colors. Within each color, cells touch disjoint strong dimers, so their reduced state is a tensor product of maximally mixed cell states.

Cauchy–Schwarz between the two color factors, followed by Hoeffding for each centered cell, gives

log Z_M-log Z_M^(0) <= M beta^2 w^2/4.

This equals the old M^2 beta^2 w^2/8 bound at M=2 and halves it at M=4. It is valid for the even seed lengths needed here. It is not a blanket replacement for overlapping noncommuting perturbations on an arbitrary two-dimensional lattice.

## 4. Verified enlargement of the C=5 contraction domain

The same C=5 recursion and all-integer one-dimensional interpolation remain valid for 0<=u<=1/40. The exact first-step coefficient is

f[1-(1-u)^3]/u^2=(3-3u+u^2)^2/[2(1-u)^6].

It increases on this interval: differentiating (3-3u+u^2)/(1-u)^3 leaves numerator 6-4u+u^2>0. Its endpoint value is below 5. The thermal coefficient bound from 2u+5u^2, the tail-weight proof requiring u<1/8, and the interpolation checks 3/2+5u+2/(1-2u)<4 and 4/(1-4u)<5 also hold at 1/40. This is an extended acceptance theorem. The frozen scalar script's 0.01 threshold is unchanged.

## 5. Verified exclusion region for the scalar method

Write G(x)=1-(1-x)^2/(2x^2) and W=S^2T. Then G(x)-x=(1-x)(2x-1)(x+1)/(2x^2)<=0 for 0<x<=1/2. If W<=1/2, either the first step is nonpositive and fails or S'=G(W)<=W<=S. The second argument T^2S'<=WT^2<=W<=1/2, so either it fails or T'<=T. Thus W cannot increase or reach the small-defect basin. This excludes this scalar scheme whenever a rigorous W upper bound is<=1/2. It does not show the physical system is gapless.

## 6. Verified three-site spectral bound for streamed heat traces

For spin-1, a three-site path h12+h23=S2·(S1+S3) has minimum-3 by angular-momentum addition. Any two rotationally twisted bonds form a tree and can be independently gauged to untwisted interactions. Summing translated three-site paths gives H>=-3L/2 for periodic L>=3, including physical rotational twists. Each bond also obeys h<=1, so H<=L. Consequently P=(16-3L/2-H)/16 has spectrum in[1-5L/32,1], contained in[-1,1] for 3<=L<=12. The L=2 doubled-bond convention must be excluded from this cluster proof.

For Eisenstein coefficients a+b omega with a,b in [-1,0], |a+b omega|^2=a^2-ab+b^2<=1. Thus simultaneous unit-floor errors in those two integer coefficients have complex physical magnitude at most 1. A monomial-unitary symmetry reconstruction preserves each representative column error norm without requiring the quantizer itself to commute with the symmetry. The complete streamed Horner error certificate remains pending its precise implementation.
