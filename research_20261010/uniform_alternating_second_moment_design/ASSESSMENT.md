# Variance-weighted finite-trace comparison: design assessment

2026-10-11 03:43 UTC. Design-only proposal. The scalar separation checks consume already accepted inputs; no new physical B^2 or H^2 contraction has been performed. No wider robustness interval is asserted here.

## 1. Main finding

The proposed second-moment chord bound is correct and can materially reduce the finite trace loss. A first useful test needs only the two observables <B_32^2> and <B_64^2> in the unchanged D26 trials. New H^2/energy-variance contractions are optional rather than a prerequisite: the existing finite thermal purities certify much stronger gaps at these two finite lengths than the global .0248 bound, making an energy-only fidelity estimate useful.

Directed scalar checks from frozen data give:

| Physical length | Shifted trial mean mu | Ground energy lower E_lo | Finite gap delta | Gibbs ground weight lower gamma | Energy-only infidelity upper epsilon |
|---|---|---|---|---|---|
| 32 | -.0011203789053423393 | -.0063 | .21 | .9366474892930138 | .02466486235551267 |
| 64 | -.000009283946501609371 | -.0071 | .19 | .9134631964156602 | .03731955817630732 |

These are scoped finite-volume statements at beta0=49/4, not a replacement for the global gap. Decimal entries except the chosen rational E_lo and delta are displays of the exact saved fractions/checks.

If future certified normalized D26 expectations q_L=<B_L^2>_psi/(3L/2)^2 satisfy q_32,q_64<=.05, then the rigorous bounds below give

    kappa_32 <= .199072718,
    kappa_64 <= .245217685.

Thus the small-radius quadratic trace loss would be at most approximately one quarter of the previous worst-case loss, suggesting roughly twice the radius for a comparable seed loss. This radius estimate is a design heuristic, not a new certified interval. Exact bootstrap replay is still required.

## 2. Spectral second-moment chord

Keep B_L=sum_odd h_j-sum_even h_j, b_L=3L/2, and rho_0 the UNTWiSTED uniform Gibbs state. One-site translation fixes rho_0 and sends B_L to -B_L. Thus the probability measure p_lambda=Tr(rho_0 P_lambda(B_L)) is symmetric under lambda -> -lambda, even though rho_0 need not commute with B_L. Consequently

    Tr(rho_0 exp(t B_L)) = Tr(rho_0 cosh(t B_L)).

For |x|<=b and real t,

    cosh(tx)-1 <= (x^2/b^2)[cosh(tb)-1].

Indeed (cosh(tx)-1)/x^2=sum_(k>=1) t^(2k)x^(2k-2)/(2k)! is nondecreasing in |x|; its x=0 limit is t^2/2. Functional calculus and the symmetric probability measure give

    Tr(rho_0 exp(t B_L)) <= 1+kappa_L[cosh(tb_L)-1],
    kappa_L=Tr(rho_0 B_L^2)/b_L^2 in [0,1].

Golden–Thompson therefore refines the accepted finite trace comparison to

    1 <= Z_eta,L(beta)/Z_0,L(beta)
      <= 1+kappa_L[cosh(beta eta b_L)-1].                        (1)

The lower bound and all twist restrictions are unchanged. Neither kappa nor the symmetry claim is asserted for a pi-seam Gibbs state. Equation (1) is used only at the finite seed lengths.

If kappa_L<=k_L is certified, use F_L(r)=1+k_L[cosh(beta0 r b_L)-1]. For the existing physical n32 seed,

    S_g >= S_0/F_32(r)^2,
    T_g >= T_0/F_64(r)^2.

The actual inverse temperature remains beta0/c. Subsequent positive-cell bootstrap is unchanged. No physical trace at a new g or beta is needed.

## 3. Thermal ground-weight lower bound

Let C_L be an accepted physical Gibbs-purity lower bound greater than1/2. The unique largest Gibbs weight p0 obeys

    p0 >= gamma_L=(1+sqrt(2C_L-1))/2.

Proof: purity<=p0 first gives p0>1/2; and purity<=p0^2+(1-p0)^2 gives the sharper displayed root. It follows that

    gap_L >= beta0^(-1) log[gamma_L/(1-gamma_L)].

check_saved_separation.py takes C_32 from the accepted own-length direct physical32 row, and C_64 from the accepted T64 endpoint of the n32 seed. It proves the more conservative rational finite gaps .21 and .19 by checking gamma-exp(beta0 delta)(1-gamma)>0. No logarithm approximation certifies these gaps.

These finite gaps are stronger than .0248 but apply only at the two lengths required for the proposed new contractions.

## 4. Ground energy lower bounds and the separation test

All energies in this section use H'=H+aL, a=700741/500000. With the accepted upper trace Z_L(beta0)<=Q_L,

    E0' >= -log(Q_L)/beta0.

For a proposed rational E_lo, it is sufficient to verify

    lower_exp(-beta0 E_lo) >= Q_L.

The saved exact checks accept E_lo=-.0063 at32 and -.0071 at64. If mu=<psi,H'psi>, define e=mu-E_lo. The requested separation with the global gap is already positive:

    .0248-e_32 = .01962037890534234...,
    .0248-e_64 = .01770928394650161....

Thus the original variance/residual proposal is not blocked by an unidentified spectral separation. Using the stronger finite gaps improves the denominators further:

    delta_32-e_32 = .20482037890534234...,
    delta_64-e_64 = .18290928394650161....

The source mean energies are total shifted Rayleigh quotients, not per-bond energies. The norm/energy data at32 and64 are already accepted and are not recomputed here.

## 5. Fidelity inequalities, with and without new H^2

Let |0> be the unique normalized ground state and f=|<0,psi>|^2. The spectral gap implies

    mu-E0' >= (1-f) delta.

Therefore an ENERGY-ONLY certified infidelity upper endpoint is

    1-f <= epsilon_E = (mu-E_lo)/delta.                         (2)

This gives the values in the opening table using only frozen inputs.

If a complete physical energy variance is newly certified,

    sigma^2=<psi,H^2 psi>-<psi,H psi>^2
           =||(H-mu_unshifted)psi||^2,

then every excited eigenvalue is at least E_lo+delta, so with d=E_lo+delta-mu>0,

    sigma^2 >= (1-f)d^2,
    1-f <= epsilon_V = sigma^2/d^2.                            (3)

Take epsilon=min(1,epsilon_E,epsilon_V) if (3) is available. The variance must be the full-space residual norm, including all Hpsi components; a projected trial-space variance is invalid. Constant shifts cancel from sigma^2.

The relatively large finite d values make variance potentially effective, but its numerical value has not been computed. A small MPS Rayleigh quotient alone is not a variance certificate.

## 6. From trial B^2 to the ground and Gibbs B^2

Set O=B_L^2/b_L^2, so0<=O<=I, and q=<psi,Opsi>. After aligning a phase, write

    |0>=sqrt(f)|psi>+sqrt(1-f)|chi>,  <psi,chi>=0.

The triangle inequality after O^(1/2) gives

    sqrt(<0,O0>) <= sqrt(f q)+sqrt((1-f)<chi,Ochi>)
                   <= sqrt(q)+sqrt(epsilon).

Thus an easily certified ground upper endpoint is

    alpha <= min(1,(sqrt(q)+sqrt(epsilon))^2).                 (4)

The pure-state trace-distance estimate also gives alpha<=q+sqrt(epsilon); taking the smaller valid endpoint is allowed. More refined binary-measurement fidelity inequalities are optional; they are not needed for the present design thresholds.

Decompose the uniform Gibbs state into its ground contribution p0|0><0| and the positive excited remainder. Since0<=O<=I and p0>=gamma,

    kappa=Tr(rho_0 O) <= (1-p0)+p0 alpha
                       <= (1-gamma)+gamma alpha.              (5)

This establishes the parent's proposed form with a rigorously identified gamma, rather than silently treating a trial state as the exact ground state.

With energy-only epsilon, the sufficient q thresholds for kappa<=1/4 are

    q_32 <= .08372241632023175...,
    q_64 <= .05282677781035461....

These are downward-directed exact thresholds, not expectations about the missing contractions. The simpler joint target q_32,q_64<=1/20 is safely inside both. For comparison, q<=.1 would yield kappa_32<=.273155 and kappa_64<=.323580; even that would substantially improve the worst-case trace bound. q<=.25 gives .467718 and .525458, still better than1 but a less compelling gain.

## 7. Exact physical contractions that would be needed

The first proposed physical gate needs ONLY N_L, the existing first moment H_L, and a new B_L^2 numerator at L32 and64. N_L/H_L are consistency checks against already accepted integers. No D increase, variational optimization, new thermal matrix or extra retained trial state is required.

Let T be the accepted D26 norm-transfer matrix, O_h the accepted two-site bond insertion, and N_L=Tr(T^L). Introduce exact local insertions

- O_(h^2), supported on two physical sites;
- O_(h_12 h_23), supported on three physical sites, with the product in that order.

The D26 tensors and the Heisenberg matrix are real. Translation and reality imply <h_0 h_r>=<h_0 h_(L-r)> without requiring reflection invariance of the MPS. Overlapping bonds are treated separately, not as disjoint two-site insertions. Put

    A0=Tr(T^(L-2) O_(h^2)),
    A1=Tr(T^(L-3) O_(h_12 h_23)),
    D_z=sum_(k=0)^(L-4) z^k Tr(T^k O_h T^(L-4-k) O_h), z=+1 or-1.

Then, for even L>=4,

    <psi,H^2 psi>_unnormalized = L(A0+2A1+D_(+1)),
    <psi,B^2 psi>_unnormalized = L(A0-2A1+D_(-1)).               (6)

The minus sign on the two adjacent-bond terms in B^2 is essential. Every periodic ordered pair is counted, including the closing bond. Divide by N_L; subtract the square of the accepted TOTAL unshifted mean for sigma^2.

The first B^2-only gate needs the z=-1 sum. The optional H^2 variance requires z=+1 as well and can reuse the same powers and local insertions.

A compact exact evaluation can avoid one dense matrix product per displacement. Define

    F_N(z)=sum_(k=0)^(N-1) z^k T^k O_h T^(N-1-k).

It is the upper-right block of [[zT,O_h],[0,T]]^N and obeys

    F_(a+b)(z)=(zT)^a F_b(z)+F_a(z) T^b.

Thus binary-power recurrences compute F_(L-3)(z), with D_z=Tr(F_(L-3)(z) O_h). The existing eleven charge-difference blocks, largest side162, remain available: h^2 and the adjacent product preserve total magnetization. There is no need to form a676-dimensional physical Hamiltonian, a3^L vector, or a larger linear trial basis. The doubled transfer block is an algorithmic representation and should be evaluated using its block formula rather than allocated densely.

## 8. Proposed bounded gate, not an authorization to run it

A physical pilot is justified because the scalar conditions above show a material possible gain while retaining one D26 trial. Recommended sequence:

1. Independently derive the two local insertion matrices and verify equation(6) on tiny periodic L4/L6 fixtures; check the alternating signs, overlap ordering and full-space variance. This is a separate physical-code validation step, not part of the already used scalar budget.
2. Reproduce the accepted norm and first moment exactly at physical64, then compute only its B^2 numerator. Physical64 is the more restrictive q threshold and the more heavily weighted thermal seed loss, so test it first.
3. If q64 is sufficiently small and measured cost is acceptable, compute the32-site counterpart using shared powers. If q64 fails to improve kappa materially, stop before a larger batch.
4. Only if energy-only fidelity is the limiting factor and the extra cost is justified, add the z=+1 H^2 sum to improve epsilon through(3).

A reasonable request for the FIRST physical gate is one process with a hard60CPU-second/256MiB limit, explicit one-thread affinity, an independent wall watchdog, no automatic retry and per-block checkpoints; the precise wall cap should be selected from current executor performance. This is a proposed cap, not a claim that a production contraction has been benchmarked or will fit. Tiny-fixture cost should be separately measured and charged. No such run was started or authorized by this assessment.

Any resulting q, sigma^2, kappa, radius and new gap must receive independent physical/scalar review before promotion. A failed pilot would limit this sufficient design, not prove that the true staggered susceptibility is large or that no robust neighborhood exists.

## 9. Artifacts and current resource boundary

check_saved_separation.py, separation_results.json and INPUT_SHA256.json preserve the exact saved-input scalar checks and hypothetical thresholds. That check used .006987984 process CPU seconds and10240KiB peak RSS, with5CPU-second/256MiB hard limits. It did not form any physical matrix or run any contraction. Existing accepted positive-transfer and robustness packages remain unchanged.
