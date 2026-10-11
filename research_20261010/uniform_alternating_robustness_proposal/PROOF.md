# A certified finite-seed neighborhood of the uniform spin-one chain

2026-10-10 23:13 EDT / 2026-10-11 03:13 UTC. Producer exact proof; independent review of the new analytic comparison, cell identification, and scalar composition is required. This package does not amend any accepted result or sealed input.

## 1. Explicit producer conclusions

For each integer cell number M >= 2, put L=2M and

    H_M(g) = sum_(j=1)^M [S_(2j-1) dot S_(2j) + g S_(2j) dot S_(2j+1)],
    S_(2M+1)=S_1,  S_j^2=2.

The designated unit exchange remains one on the first set of bonds, including when g is slightly greater than one. Both following closed intervals have exact outward scalar certificates:

1. For 19999/20001 <= g <= 20001/19999, every M >= 2 has a unique ground state and gap >= 3/200 = 0.015.
2. For 12499/12501 <= g <= 12501/12499, every M >= 2 has a unique ground state and gap >= 1/200 = 0.005.

Approximate intervals are [0.9999000049997500, 1.0001000050002500] and [0.9998400127989761, 1.0001600128010241], respectively. These displays do not define the endpoints. Neither interval is claimed optimal. They are neighborhoods of a nonperturbative reference model, certified by finite-seed perturbation followed by a genuine cell-transfer bootstrap; no infinite-volume gap is inferred by subtracting an extensive operator norm.

## 2. Normalization and the staggered operator

Let h_j = S_j dot S_(j+1) on the periodic even ring and set

    H_0 = sum_j h_j,
    B_L = sum_(j odd) h_j - sum_(j even) h_j,
    c=(1+g)/2,  delta=(1-g)/2,  eta=delta/c=(1-g)/(1+g).

Then H_M(g)=c(H_0+eta B_L). In the present intervals c>0 and

    |eta| <= r,
    1/(1+r) <= c <= 1/(1-r),
    g in [(1-r)/(1+r), (1+r)/(1-r)].

The unshifted two-spin operator h has eigenvalues -2,-1,1. Consequently h+I/2 has norm 3/2. Since there are equally many plus and minus bonds,

    B_L = sum_j (-1)^(j+1)(h_j+I/2),
    ||B_L|| <= 3L/2 =: b_L.

This bound uses no commutation of neighboring bonds. It applies at L=4 as well: all four nearest-neighbor physical bonds are distinct, and these are exactly the two unit and two g bonds of M=2. No M=1 statement is made.

Retain the accepted uniform shift a=700741/500000 per physical site. Define

    Z_eta,L(beta) = Tr exp[-beta(H_0+eta B_L+aL)],
    Z_g,M(tau) = Tr exp[-tau(H_M(g)+c a L)].

At tau=beta/c they are equal. Thus the actual initial inverse temperature is tau_0=(49/4)/c; the normalized inverse temperature remains beta_0=49/4. The scalar shift affects neither physical gaps nor purities.

## 3. Uniform-Gibbs expectation and the exact trace comparison

This section concerns only the untwisted even physical ring. Let U be one-site cyclic translation. It obeys

    U H_0 U* = H_0,   U B_L U* = -B_L.

The uniform Gibbs state rho_0=e^[-beta(H_0+aL)]/Z_0,L(beta) therefore commutes with U. Cyclicity gives Tr(rho_0 B_L)=-Tr(rho_0 B_L)=0. This is an exact finite-volume identity, with no ground-state or trial-state approximation.

The Gibbs variational principle, evaluated in rho_0, gives

    log Z_eta,L(beta) >= log Z_0,L(beta)-beta eta Tr(rho_0 B_L)
                           = log Z_0,L(beta).

Equivalently, trace-exponential convexity and the evenness in eta implied by translation show that eta=0 minimizes the finite trace.

For the upper bound, Golden–Thompson has the following direction:

    Z_eta,L(beta) <= Tr(e^[-beta(H_0+aL)] e^[-beta eta B_L])
                  = Z_0,L(beta) Tr(rho_0 e^[-beta eta B_L]).

No commutation of H_0 and B_L is asserted. If B_L=sum_lambda lambda P_lambda, the numbers p_lambda=Tr(rho_0 P_lambda) are a genuine probability distribution, have mean zero, and are supported in [-b_L,b_L]. Thus Hoeffding's scalar moment-generating-function estimate applies to the spectral measurement of B_L, irrespective of whether rho_0 commutes with B_L.

For completeness, the elementary spectral chord bound already proves the needed estimate. For any real t and lambda in [-b,b], convexity gives

    exp(t lambda) <= cosh(tb)+(lambda/b) sinh(tb).

Taking the mean removes the second term. Finally cosh(x)<=exp(x^2/2), for example by integrating tanh(x)<=x for x>=0 and using evenness. We obtain

    1 <= Z_eta,L(beta)/Z_0,L(beta)
      <= cosh(3 beta eta L/2)
      <= exp[A_L(beta,r)],
    A_L(beta,r) = 9 beta^2 r^2 L^2 / 8,    |eta|<=r.                 (1)

The upper loss is quadratic in the staggered coupling. Its L^2 growth is harmless only at fixed finite input sizes. It is not applied to arbitrary growing lengths to infer a thermodynamic gap.

### Twisted-data boundary

The pi-seam Hamiltonian is not assumed to have ordinary one-site translation symmetry. Neither the zero-expectation claim nor (1)'s lower bound is asserted for that twisted trace. All identity/pi data are used solely in the already accepted UNIFORM seed derivation, before (1) is applied to the untwisted physical ratios. No perturbed twisted moment, sector filter, or cell-moment identification is invented.

For an even twisted ring a coarse two-sided Weyl trace comparison is separately available, because a rotated seam bond has the same local spectrum and hence the same centered norm bound. It is unnecessary here. The uniform odd-length seam data remain inputs to the uniform moment certificate, not odd-length alternating chains.

## 4. Self-adjoint CELL history transfer

A direct construction is required. Writing a product of two self-adjoint one-site transfers would not establish self-adjointness or positivity and is not used.

Group each g bond into a two-spin cell. More explicitly, cell j contains physical sites (2j,2j+1), with the indices periodic; the unit bond joining (2j+1,2j+2) connects adjacent cells. The local cell operator is v=g S_L dot S_R+2ca I and every intercell bond has coefficient one. This is the homogeneous cell model in audit/AUDIT_REPORT.md and chain_audit/CHAIN_CERTIFICATE_PROOF.md.

The exact sufficient hypotheses, all satisfied here, are:

- finite fixed spin s=1 and the same Hermitian v in every cell;
- invariance FvF*=v under exchange of the left and right spins;
- invariance under cell time reversal Theta_1 tensor Theta_1;
- positive unit antiferromagnetic intercell exchange;
- periodic rings with every integer cell number M>=2.

The original width(v)<=.03 restriction was an analytic-SEED condition, not a condition for existence of the history transfer. The accepted chain audit explicitly separates these roles. No small-width restriction is used here.

Cell time reversal squares to +1. In a basis where it is complex conjugation, v is real symmetric and iS_L^alpha and iS_R^alpha are real, norm-bounded matrices. The Duhamel expansion of an intercell bond uses

    -S_R dot S_L = sum_alpha (iS_R^alpha) tensor (iS_L^alpha).

Labeled ordered histories carry a nonnegative finite measure of total mass exp(3 tau) for s=1. A cell kernel is the real trace of chronologically ordered spin insertions interspersed with exp(-Delta t v). Its absolute value is bounded by 9 exp(tau ||v||). Exchanging the two boundary histories is conjugation by F, preserving the chronological order and leaving v fixed. Hence k(x,y)=k(y,x). No reversal of a noncommuting product is needed.

The resulting real symmetric bounded kernel on a finite measure space defines a real self-adjoint Hilbert–Schmidt operator X_g,tau. Absolute convergence of the finite-volume Duhamel series permits grouping histories into cells. The cyclic kernel trace then gives

    Z_g,M(tau)=Tr X_g,tau^M,    every integer M>=2.                 (2)

At M=2 the two intercell unit bonds are distinct physical bonds, exactly as in the requested Hamiltonian. The same operator works for every M. Its spectrum may be signed; neither an entrywise-positive kernel nor a positive-semidefinite transfer is claimed. Positivity of all physical traces, including odd CELL lengths, is what permits the inherited signed-spectrum interpolation to identify a positive dominant transfer eigenvalue.

These are the exchange/time-reversal hypotheses needed for a reflection-compatible cell kernel. No additional, unproved operator reflection-positivity assertion is used.

## 5. The actual finite inputs and trial space

The new scalar seed uses the accepted physical-length n=32 uniform seed at beta_0=49/4, now interpreted as EVEN cell n=16:

    S_0 = Z_0,64(beta_0)/Z_0,32(beta_0)^2 >= s_0,
    T_0 = Z_0,64(2 beta_0)/Z_0,64(beta_0)^2 >= t_0,
    s_0 approximately .9301225504257616,
    t_0 approximately .8419036295805096.

Exact rationals are copied, pinned, and retained in certificate.json. Their source is the n32 row of uniform_smaller_second_initialization/certificate.json, independently accepted by uniform_smaller_second_initialization_review.

The actual newly consumed physical thermal evidence consists of the existing eighteen uniform traces:

- every physical length 4,5,6,7,8,9,10,11,12;
- inverse temperature exactly 49/4;
- both identity I and pi seam P at each length;
- shift a=700741/500000 per physical site.

The accepted signed moments J_k=(I_k+3P_k)/4 and N_k=(I_k-P_k)/4, including signed odd moments and the physical multiplicity J+3N, already imply the n32/n64 trace and dominant-atom bounds. The long moments used by that derivation are certified consequences, not new physical thermal jobs. No physical trace at a different g is computed. No physical thermal trace at 49/2 is newly computed: its lower bound is variational.

The physical trial is the unchanged periodic D26 MPS at exactly 64 physical sites. With the accepted integer contractions N0_64>0 and TOTAL energy numerator H0_64,

    R_64 = H0_64/N0_64+64a < 0,
    R_64 approximately -0.000009283946501609371.

The accepted seed uses this sign to infer both Z_0,64(beta_0)>1 and Z_0,64(2 beta_0)>1. H0_64 is already the total periodic energy numerator; it is not multiplied by 64 again.

Cyclic invariance of the MPS amplitudes gives U psi=psi. On an even ring this independently implies <psi,B_L psi>=0. Hence its alternating-chain shifted Rayleigh quotient is EXACTLY c R_64, and at tau_0=beta_0/c its Jensen numerator lower bounds are unchanged. No approximate SU(2), reflection, or translation assignment is needed.

The linear trial span has dimension ONE; the MPS bond dimension is 26; its norm-transfer matrix dimension is 676; the physical 64-site Hilbert dimension is 3^64. None is identified with the history-transfer rank, which need not be finite. No additional trial vector, optimization, residual calculation, physical contraction, or exact diagonalization is required for this neighborhood.

The finite short-size bridge consumes the already independently accepted all-size uniform gap 31/1250 (seal 5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf). It does not replace the original physical-length-24 parity/MPS48 construction with a nonexistent own24 anchor.

## 6. Finite seed perturbation, then unrestricted bootstrap

Apply (1) only at fixed physical lengths 32 and 64. Numerators have the exact lower comparison Z_eta>=Z_0; each denominator gains at most the factor in (1). Therefore, at cell n=16 and actual tau_0=beta_0/c,

    S_g(16,tau_0) >= s_0 exp[-2 A_32(beta_0,r)],
    T_g(32,tau_0) >= t_0 exp[-2 A_64(beta_0,r)]
                         = t_0 exp[-8 A_32(beta_0,r)].           (3)

All further size growth uses the ACTUAL cell transfer (2) and exact physical trace-ratio identities, not a perturbation bound with a growing prefactor. For canonical state (n,tau,S,T), use

    K=S^2 T,
    G(x)=1-(1-x)^2/(2x^2),
    S_new=G(K),  T_new=G(T^2 S_new),
    (n,tau) -> (2n,2tau).

Every spatial base n is even. All quantities are checked in their legal domains, and the newly updated S is used in T_new. For each preclosure state the accepted all-integer signed window has

    w=(1+sqrt(2K-1))/2,  rho=(1-w)/w,
    d=T/(1+rho^2),
    C=(1-rho) min(S sqrt(d),d).

It gives physical thermal purity >=C for every integer CELL number in [n,2n]. For physical gap target D, the certificate checks

    C-exp(tau_upper D)(1-C)>0,
    tau_upper = 2^j beta_0 (1+r),

which covers all eta in [-r,r] because 1/c=1+eta<=1+r. Exact integer square roots and rational exponential enclosures are directed outward. At common defect u=max(1-S,1-T)<=.01 it verifies

    1-5u exp(tau_upper D)>0.

The inherited small-defect theorem then covers all subsequent integer cell sizes. The finite windows overlap and leave no missing cell integers. The narrow certificate closes at cell n=256 after four updates; the wider certificate closes at cell n=512 after five updates. The exact recorded windows also include the terminal window.

## 7. Separate finite bridge: cell M=2 through 15

For physical lengths L=4,6,...,30 the accepted uniform theorem gives gap >=31/1250 and uniqueness. Weyl at each of these FIXED finite sizes gives

    gap[H_0+eta B_L] >= 31/1250-2|eta| ||B_L||
                       >= 31/1250-3Lr.

Multiplication by c and minimization over this finite range imply

    gap[H_M(g)] >= (31/1250-90r)/(1+r).                          (4)

This lower bound is 203/10000 divided by 20001/20000, approximately .02029898505074746, for r=1/20000. For r=1/12500 it is .01759859211263099. Each is strictly larger than its respective target .015 or .005. Positivity of the finite perturbed gap also proves uniqueness. Equation (4) is not extrapolated beyond the finite bridge.

## 8. Width bottleneck and the unused thermal bridge

The Weyl bridge is NOT the width bottleneck for these certificates. At target D=.015 the bridge alone would permit

    r <= (31/1250-.015)/(90+.015) > .0001088,

whereas the certified narrow radius is .00005. At target .005 it permits r>.0002199, whereas the wider radius is .00008. Thus both have substantial short-size slack; the perturbation-degraded canonical seed and its subsequent windows are the restrictive part of this sufficient recipe.

If a thermal short-size bridge is desired later, the same untwisted comparison gives, for any accepted finite even-L uniform purity C_L,

    T_g(L/2,beta_0/c) >= C_L exp[-2 A_L(beta_0,r)].

This transfers the accepted ratio itself, so its provenance is preserved. In particular the physical-L24 C_L must retain its accepted parity/MPS48 numerator construction; no own24 trial is needed or asserted. Such a bridge is unnecessary for either current result and cannot by itself fix a failed large-cell bootstrap seed.

Preliminary floating proposals are not no-go results. A failed sufficient test at a larger radius would not establish gaplessness, a maximal robust neighborhood, or a requirement to increase the trial space.

## 9. Resource and acceptance boundary

check_scalar.py is a standalone Fraction/integer implementation; it imports no code that runs physical contractions. It sets a 30-process-CPU-second hard limit and 256 MiB address-space hard limit before scalar work. The one accepted run used .05302305 process CPU seconds, .05810865799867315 monotonic wall seconds, and 11136 KiB peak RSS. A preliminary read-only floating proposal used .000543495 process CPU seconds and 8320 KiB RSS. These are far below the requested budget; no additional thermal campaign or physical job was started.

INPUT_SHA256.json binds all consumed proofs/certificates and the accepted review manifests. Existing sealed files, root documentation, and GitHub remain untouched. The conclusions are producer-certified exact scalar consequences of inherited independently accepted premises, pending a new independent review of the analytic comparison and composition. This is not a formal proof-assistant verification and does not claim optimality.

Reproduce with PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python check_scalar.py in a disposable copy preserving the relative dependencies. A replay changes the local result/resource files; do not overwrite a frozen package in place.
