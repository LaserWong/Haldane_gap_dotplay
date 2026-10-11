# Smaller second-input bootstrap initialization

2026-10-10 22:21 EDT / 2026-10-11 02:21 UTC. Exact producer certificates; independent physical/scalar review pending.

## Scope and source attribution

Uniform periodic spin-one Heisenberg chain, unit bilinear coupling, shift a=700741/500000, beta0=49/4. The original paper's self-adjoint history-transfer identity is valid at every integer physical length L>=4, and the paper already had an n36 second initialization. No claim that the first-input n52 was a global minimum is made. This package uses all eighteen identity/pi seam inputs at lengths4..12, now physically independently validated by uniform_second_thermal_full_review (manifest792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94), and the accepted signed-sector intervals/support filters from uniform_second_moment_optimization and its separate review. Original theorem, transfer construction and physical tensor attribution remain in those unchanged source packages.

The improvement here is genuinely a smaller canonical initialization, not merely a direct-window extension of a larger initialization. Every case uses its own physical2n-site MPS anchor. No72-site quotient is reused at60,64 or68. No new thermal campaign, ED, tensor optimization, rank truncation or larger bond dimension is used.

## Signed long moments

The accepted multiplicity-space spectra are J and N, with full trace J+3N. Their signed moments4..12 and four independently accepted support caps are retained exactly. Odd moments are never replaced by unsigned moments. Every spectral occurrence has unit mass, and finite transfer rank is not assumed.

For each proposed even length k, certify_long.py builds a rational degree-eight polynomial p and proves p(x)-x^(k-4)>=0 on the whole signed support interval. It transforms exactly to Bernstein coefficients and recursively bisects by exact de Casteljau arithmetic. Nonnegative coefficients on all leaves prove interval nonnegativity. The floating LP and scalar minimization only propose coefficients and an added rational constant; they do not certify the inequality. Multiplying by x^4 and summing gives m_k<=sum_j p_j m_(4+j), choosing the upper moment endpoint for a nonnegative coefficient and lower endpoint for a negative coefficient. Thus signed cancellation is rigorously enclosed. Every bound, coefficient and Bernstein subdivision depth is saved in long_certificate.json.

For arbitrary rational r>=1, packing nonnegative y_i<=h with total mass<=m yields sum y_i^r<=floor(m/h)h^r+(m-floor(m/h)h)^r. This follows by convex mass packing and monotone convergence for infinite lists. Apply y=lambda^12 and r=k/12. The checker takes the minimum of this exact outward packing bound and the polynomial bound whenever available. Length60 uses packing alone;64 and68 may use both. Long-sector certificates at16..36 also permit comparison but are not all consumed in the final claims.

## Fresh anchors and dominant eigenvalue

contract_ground.cpp uses the previously validated fixed D26 blocks in audit/mps/mps_blocks.txt and exactly contracts N0_L=Tr(T^L), H0_L=L Tr(T^(L-2)O). The total shifted quotient is R_L=H0_L/N0_L+aL. Positive norm and R_L<0 are checked as exact integer/rational inequalities for L60,64,68. A physical MPS is one trial state of bond dimension26, whereas the full Hilbert-space dimension is3^L. The script does not mistake D26 for the Hilbert dimension or transfer rank.

Jensen/variational positivity gives Z_(2n)(beta0)>1 and Z_(2n)(2beta0)>1, without assuming ground uniqueness. For a rational ell below1, the checker proves

    pack(mJ12,ell^12,2n/12)+3 upper(N_(2n)) < 1.

Therefore some J eigenvalue has modulus>ell. Since ell exceeds the accepted negative-J support cap, this eigenvalue is positive. Remove one copy; its residual J twelfth moment is at most mJ12-ell^12. Convexity bounds the remaining J n-th absolute mass by (mJ12-ell^12)^(n/12). Add3 upper(N_n) to obtain tail R_n. A second equal leading atom is excluded by the same residual-mass inequality; no fabricated multiplicity or realization of a relaxed measure is required.

The canonical seed endpoints are

    S(n,beta0) >= [1+R_n/ell^n]^-2,
    T(2n,beta0) >= Q_(2n)^-2,

where Q_(2n) is the certified full trace upper bound. The thermal endpoint uses the OWN2n-site anchor at doubled temperature. Cooling ratio is1: the zero-additional-cooling endpoint already succeeds, so a larger finite beta search or direct-time-first workaround is unnecessary for the requested positive result. No optimal-temperature claim is made.

## All integer windows and closure

At canonical state(n,beta,S,T), K=S^2T, update sequentially S'=G(K), T'=G(T^2S'), then double n and beta, where G(x)=1-(1-x)^2/(2x^2). All arguments/output endpoints are legal and rounded downward.

For every state prior to accepted closure, use the inherited independently reviewed signed all-integer interpolation:

    w=(1+sqrt(2K-1))/2, rho=(1-w)/w,
    d=T/(1+rho^2), C=(1-rho) min(S sqrt(d),d).

K>1/2 is checked. The exact C is a lower purity bound for every integer L in[n,2n], including odd L. At the requested gap g the checker proves C-exp(beta*g)(1-C)>0. The windows overlap without missing integers. The terminal small-defect theorem applies when u=max(1-S,1-T)<=.01 and1-5u exp(beta*g)>0. Every seed, state, window and terminal margin is in certificate.json. The supported conclusion includes unique ground state.

Roots are enclosed by exact integer bisection with explicit power checks. Exponentials use a positive Taylor polynomial, geometric next-term remainder, outward rounding and repeated squaring. All acceptance arithmetic is rational; decimal displays are not premises. The gap search is a finite1e-4 grid and is not a proof of the best possible gap, minimum seed or all-method failure at any smaller size. No n28 test was authorized or run.

## Resource and reproducibility

Cached algebra uses CPU2, hard120CPU-second/256MiB limits per process, and one BLAS/OpenMP/HiGHS thread. A first LP launch aborted because HiGHS attempted its default threaded startup under the cap; it produced no accepted candidate. Explicit threads=1 then completed safely. An early long-check launch before candidate creation returned missing-file, without accepted output. Search2.04CPU seconds; long exact check18.12CPU seconds. The final continuation resource measurement is in certificate.json. Preliminary replays remain covered by the bounded scalar work; no large physical job was started.

Anchors64/68 used15.912CPU seconds/33900KiB. The separately authorized60 anchor used8.96001CPU seconds/33408KiB. Total24.87201CPU seconds; both ran CPU5 with100MiB hard memory cap and60CPU-second hard process cap. An independent reviewer is separately reconstructing physical tensors/contractions rather than trusting output matching alone.

Reproduce scalar bounds with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python certify_long.py, then python certify.py. search.py is optional proposal generation. Fresh contraction replay requires compiling contract_ground.cpp with g++ -O2 -lgmpxx -lgmp, then running under taskset -c5 against the exact pinned block input at lengths64,68 and separately60. Original sealed packages, root documentation and GitHub are untouched. INPUT_SHA256.json pins consumed inputs; MANIFEST_SHA256.json and SEAL.json freeze this new isolated package.
