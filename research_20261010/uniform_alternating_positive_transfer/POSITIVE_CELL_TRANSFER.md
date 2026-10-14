# Positive cell transfer for the alternating spin-one Heisenberg chain

2026-10-11 03:26 UTC. The positive-transfer and finite-window lemmas have independent structural acceptance in uniform_alternating_positive_cell_review (manifest abb8e04fa7478e939d18c831a3a4b201c0ec6baf9b8e3e494b5b867a4347f872). New scalar certificates are documented separately and await their own review. The accepted robustness producer and review packages remain unchanged.

## 1. Scope and model

For integer M>=2 and g>=0, consider the periodic 2M-site spin-one chain

    H_M(g)=sum_(j=1)^M [h_(2j-1,2j)+g h_(2j,2j+1)],
    h_ab=sum_(alpha=1)^3 S_a^alpha S_b^alpha.

Choose the identical Cartesian spin-one basis at every site. Then G_alpha=i S^alpha is real, ||G_alpha||=1, and

    -h_ab=sum_alpha G_alpha^(a) tensor G_alpha^(b).

The same G_alpha occurs on both endpoints. The orientation of a bond changes neither its Hamiltonian nor this factorization. Reality at a SINGLE spin-one site is important here. This proof is not claimed for an arbitrary exchange/time-reversal-invariant cell perturbation v, or for a half-integer single-site representation.

## 2. History measures with coupling carried in the measure

Fix a finite physical inverse temperature tau>0. Let Omega be the disjoint union of the empty history and all ordered lists

    (0<t_1<...<t_k<tau; alpha_1,...,alpha_k in {1,2,3}),  k>=1.

For J>=0 define the measure mu_J by mass one at the empty history and density J^k times Lebesgue measure on each labeled ordered simplex. Its total mass is

    mu_J(Omega)=sum_(k>=0) (3J tau)^k/k! = exp(3J tau).

For J=0, nonempty histories have zero mass and the resulting L2 space is the one-dimensional space supported on the empty history. All measure weights are nonnegative. No analogous positive-measure statement is made here for negative J.

For two histories x,u, merge their event lists in chronological order and put

    k_tau(x,u)=tr_(C^3)[product of the corresponding G_alpha matrices in that chronological order].

Choose either convention that later events multiply on the left or on the right and use it at EVERY site. Both reproduce the same consistently time-ordered exponential. Coincident events between independent nonempty histories form a measure-zero set, so any fixed tie convention is harmless.

The kernel is real, |k_tau(x,u)|<=3, and k_tau(x,u)=k_tau(u,x). The last identity only exchanges the ownership of the same merged events. It does not reverse the chronological product, transpose a noncommuting product, or require the G_alpha matrices to commute.

## 3. Bipartite history operator and Gram kernel

Let H_1=L2(Omega,mu_1) and H_g=L2(Omega,mu_g), considered as complex Hilbert spaces with real kernels. Define

    A_g:H_g -> H_1,
    (A_g f)(x)=integral k_tau(x,u) f(u) dmu_g(u).

Its Hilbert–Schmidt norm is finite, with the following bound.

    ||A_g||_HS^2 = integral |k_tau(x,u)|^2 dmu_1(x)dmu_g(u)
                  <=9 exp[3(1+g)tau].

The adjoint is determined by the two distinct measures and has the following form.

    (A_g* v)(u)=integral overline{k_tau(x,u)} v(x) dmu_1(x).

Consequently C_g=A_g A_g* is a positive TRACE-CLASS operator on H_1, with kernel

    C_g(x,y)=integral k_tau(x,u) k_tau(y,u) dmu_g(u)
            =integral k_tau(x,u) k_tau(u,y) dmu_g(u).              (1)

In particular <v,C_g v>=||A_g* v||^2>=0. This is an actual Gram factorization between two possibly different Hilbert spaces. Positivity follows from this Gram factorization rather than from a general product of self-adjoint operators. The single-site kernel can take either sign. Positivity occurs after contracting the internal bond.

## 4. Physical cell identity, orientation, and time ordering

Regroup physical sites into cells (2j,2j+1), cyclically. The g bond is internal to a cell. The unit bond joining (2j+1,2j+2) is between cells.

Expand the finite-dimensional physical exponential in ordered bond events. Assign history x_j with measure mu_1 to the j-th unit bond and history u_j with measure mu_g to the j-th internal g bond. At the two physical sites of cell j the local trace factors are precisely

    k_tau(x_(j-1),u_j)  and  k_tau(u_j,x_j).

Both local products use forward chronological ordering inherited from the SAME global ordering. Internal history u_j carries the same label and time on its two endpoints. The fact that operators at distinct physical sites commute allows the full trace to factor into these single-site traces. It does not reorder two noncommuting matrices at any one site.

At total event number k, an absolute bound is

    3^(2M) [3M(1+g)tau]^k/k!.

The sum over k converges. Hence regrouping by bond histories, factoring site traces, and integrating the internal histories are justified by absolute convergence. Integrating u_j gives exactly (1), so

    Tr exp[-tau H_M(g)]
      = integral product_(j=1)^M C_g(x_(j-1),x_j) product_j dmu_1(x_j)
      = Tr C_g^M.                                               (2)

For M>=2 the cyclic trace formula follows from standard products of Hilbert–Schmidt kernels, or directly by first expanding A_g A_g* and using Fubini with the displayed bounds. Since C_g is already positive trace class, all its positive integer powers are trace class. The physical M=2 convention retains its two distinct unit intercell bonds, so (2) is exactly the requested four-spin Hamiltonian. No M=1 extension is needed.

An added constant a_g per PHYSICAL site is represented by

    X_g,tau = exp[-2 tau a_g] C_g,
    Tr exp[-tau(H_M(g)+2M a_g I)] = Tr X_g,tau^M.                 (3)

The scalar multiplier is positive, hence X_g,tau remains positive trace class. In the accepted near-uniform normalization, c=(1+g)/2, a_g=c*(700741/500000), and tau=beta/c. Then the per-cell scalar is exp[-2 beta*(700741/500000)], exactly the square of the uniform per-site shift at normalized beta. The physical history measures themselves still use tau and couplings 1,g.

### Consistency limits

At g=1, mu_g=mu_1. The operator A_1 is the real self-adjoint one-site history operator K_tau, so C_1=K_tau^2. With a_g=a this is exactly the shifted uniform one-site transfer squared.

At g=0, H_g is one-dimensional, A_0 f(x)=k_tau(x,empty)f(empty), and C_0 is a nonzero rank-one Gram operator. Its one positive eigenvalue is the single unit-dimer partition function. Consequently (2) gives the partition function of M independent unit dimers, as required.

These checks do not replace the derivation for intermediate g. They help check the measure assignment and physical normalization.

## 5. Positive-spectrum spatial purity at ANY cell base

For every integer n>=2, X_g,tau^n is positive trace class. Therefore

    S(n,tau)=Z_(2n)(tau)/Z_n(tau)^2

is the purity of the normalized spectrum of X_g,tau^n, even when n is odd. It lies in (0,1]. The physical thermal purity

    T(n,tau)=Z_n(2tau)/Z_n(tau)^2

likewise lies in (0,1]. Thus the exact exchange identities and same-direction purity squaring require no even-cell restriction for this model. In particular, accepted uniform physical starts 30,32,34,36 correspond to valid cell starts 15,16,17,18, respectively.

## 6. A stronger all-integer finite window

Fix an integer n>=2 and n<=M<=2n, and write q=M/n in [1,2]. Put

    S=S(n,tau),  T=T(2n,tau).

At inverse temperature 2tau, let Y=X_g,2tau>=0. Nonnegative sequence power monotonicity gives

    Z_M(2tau)=sum_i mu_i^M
             >= [sum_i mu_i^(2n)]^(M/(2n))
             = Z_(2n)(2tau)^(q/2).                              (4)

For example, normalize z_i=mu_i^(2n)/sum_j mu_j^(2n). Then sum_i z_i^(q/2)>=sum_i z_i=1, since q/2<=1. Finite moments and monotone limits justify the countable-spectrum case.

At inverse temperature tau, Hölder interpolation of the NONNEGATIVE spectrum yields

    Z_M(tau) <= Z_n(tau)^(2-q) Z_(2n)(tau)^(q-1).                (5)

Division of (4) by the square of (5), with strictly positive physical traces, proves

    T(M,tau) >= S^(2-q) T^(q/2)
              >= min(S sqrt(T), T).                            (6)

The last expression is the minimum of the endpoint values of the log-linear expression in q. It holds for every integer M in the entire window, at odd or even n and M. Neither a dominant-eigenvalue argument, K=S^2T>1/2, a signed-tail subtraction, nor the factor 1/(1+rho^2) is needed for (6).

Given lower endpoints s<=S,t<=T in (0,1], the rational-root implementation may safely use C=min(s sqrt(t),t). A physical gap D follows on that window whenever C>1/2 and C-exp(tau D)(1-C)>0. Positivity of the transfer alone is not a gap proof. Numerical lower purity information is still necessary.

## 7. Bootstrap and tail closure with unchanged conservative constants

At any integer cell base n>=2, define G(x)=1-(1-x)^2/(2x^2). The exact physical trace identities and probability squaring give the familiar legal-domain updates

    S_new >= G(S^2 T),
    T_new >= G(T^2 S_new),
    (n,tau) -> (2n,2tau).

The newly obtained S_new must be used in the thermal update. A proposed endpoint outside (0,1] is not usable. The positive-window lemma removes an INTERPOLATION gate, not all legal-domain requirements of the update.

For completeness the inherited small-defect constant five remains valid without parity assumptions. If s,t>=1-u and 0<u<=1/100, then 1-s^2t<=3u. Squaring that purity leaves defect at most

    (3u)^2/[2(1-3u)^2] <=5u^2,

because 9/[2(97/100)^2]<5. The new thermal pre-squaring defect is at most 2u+5u^2<=3u, giving the same bound. Thus u_j <= (5u)^(2^j)/5 after j cycles.

On the j-th window, (6) gives C_j >=(1-u_j)^(3/2)>=1-(3/2)u_j. Its largest physical Gibbs weight exceeds 1/2. The second-to-first weight ratio is at most

    (1-C_j)/C_j <= 2u_j <= (2/5)(5u)^(2^j),

where the middle inequality follows from u_j<=.01. Consequently every integer cell M>=n has a unique ground state and gap at least

    log[1/(5u)]/tau.

Therefore the same conservative exact terminal test 5u exp(tau D)<1 is sufficient. If the initial cell n is odd, the proof still holds. Alternatively every later doubled base is even, so only the first finite positive window needs the parity extension.

## 8. Consequences and next numerical scope

The already accepted untwisted finite trace perturbation comparison remains unchanged and reads

    1<=Z_eta,L(beta)/Z_0,L(beta)<=exp[(9/8)(beta r L)^2], |eta|<=r.

A uniform physical seed (L,beta,s0,t0) transfers to cell n=L/2 with

    s>=s0 exp(-2A),  t>=t0 exp(-8A),  A=(9/8)(beta L r)^2.

The positive transfer makes physical starts L30 and L34 newly eligible. L32 and L36 remain eligible. The finite-window lower bound improves to min(s sqrt(t),t). All use the existing physical thermal inputs and their own already accepted MPS anchors. No new physical contraction or thermal data is needed to TEST these improved sufficient conditions.

This analytic note alone asserts no wider numerical interval. CERTIFICATE_PROOF.md and certificate.json give separate new producer-certified intervals, requiring independent numerical composition review before promotion. The previous accepted explicit neighborhoods and their seals remain unchanged.
