# Finite staggered second moments improve the robustness radius

2026-10-11 04:18 UTC. Producer exact-arithmetic result, pending independent review of the newly contracted observables and the composed interval certificates. No new thermal trace or physical contraction is performed in this package.

## 1. Statement and physical units

Let h_j=S_j dot S_(j+1) be the unit spin-one exchange with bond spectrum−2,−1,1, including periodic bond multiplicity. At physical length L=2M, M an integer at least2, define

    H_M(g)=sum_j [h_(2j−1)+g h_(2j)],
    H0=sum_j h_j, B=sum_odd h_j−sum_even h_j,
    c=(1+g)/2, eta=(1−g)/(1+g), H_M(g)=c(H0+eta B).

For each row in README.md and certificate.json, the claimed finite-volume ground state is unique and the physical-unit gap is at least D throughout the closed interval |eta|<=r, equivalently g in[(1−r)/(1+r),(1+r)/(1−r)]. The designated bond remains one. All physical lengths are even; there is no alternating odd-physical-ring conclusion.

The four exact (r,D) pairs are

    (6/112525,1/50), (49/450075,3/200),
    (37/225025,1/100), (99/450025,1/200).

The prior accepted positive-cell and eight interval certificates remain valid and immutable. These new wider intervals are producer results until the independent review is complete.

## 2. Finite trace comparison with a Gibbs second moment

For even L, centering h_j by1/2 does not change the alternating sum and gives ||B_L||<=b_L=3L/2. Let rho0=exp(−beta0 H0)/Z0, beta0=49/4. One-site translation fixes H0 and reverses B, so Tr(rho0 B)=0 and the spectral measurement of B in rho0 is symmetric.

The Gibbs variational principle, or convexity of log partition function with zero derivative at eta0, gives

    Z_eta(beta0)>=Z0(beta0).

Golden–Thompson has the opposite, upper-bound role:

    Z_eta/Z0<=Tr[rho0 exp(−beta0 eta B)]
             =Tr[rho0 cosh(beta0 eta B)].

For |x|<=b, positivity of the even power series shows that(cosh(tx)−1)/x² is nondecreasing in |x|, with its value at zero defined by continuity. Thus

    cosh(tx)−1<=(x²/b²)[cosh(tb)−1].

For a certified kappa_L>=Tr(rho0 B_L²)/b_L² and |eta|<=r,

    1<=Z_eta,L(beta0)/Z0,L(beta0)<=F_L(r),
    F_L(r)=1+kappa_L[cosh(beta0 b_L r)−1].                 (1)

Energy shifts cancel from the ratio. This argument is only for the actual untwisted uniform Gibbs state. No translation-zero or second-moment assertion is made for a twisted trace.

The physical32 and64 producer packages rigorously derive, pending independent review,

    kappa32<=17/125=.136, kappa64<=157/1000=.157.

They use exact D26 B² contractions, mandatory exact N/H agreement with accepted anchors, accepted finite uniform trace/purity bounds, and energy-only fidelity. For completeness: if E0>=E_lo, gap>=delta and trial mean mu, then ground fidelity F>=f=1−(mu−E_lo)/delta. For O=B²/b² and trial q, the effect inequality gives alpha_ground<=[sqrt(fq)+sqrt((1−f)(1−q))]² when f>q. If the Gibbs ground weight is at least w, kappa<=1−w+w alpha. No assertion equates the MPS with the actual ground state, and no H² or residual estimate is used. The exact derivations and data are frozen under producer seals eccb1dcb...d9b75 and26d1977c...3570.

## 3. Seed transport, actual temperature, and unchanged physical inputs

Use only the accepted physical32 uniform seed, hence cell16, from uniform_smaller_second_initialization/certificate.json. Its certified lower endpoints are S0≈.9301225504257616 and T0≈.8419036295805096, with its own physical64 periodic D26 MPS anchor. The latter has negative shifted total Rayleigh quotient R64≈−.000009283946501609371. H0_64/N0_64 is already total energy; it is not multiplied by64 again.

The accepted uniform seed uses all18 uniform physical thermal inputs at beta0, lengths4..12 with I and P seams, and per-site shift a=700741/500000. These thermal sources and their signed-transfer moment consequences stay unchanged. Twists are only inputs to that existing uniform certificate, not targets of comparison(1).

The trial is fixed by one-site translation, so its B expectation is exactly zero. Choose actual physical inverse temperature tau0=beta0/c and physical shift a_g=ca. The perturbed shifted trial mean is cR64, so its variational Boltzmann numerator at tau0 or2tau0 is unchanged. The uniform untwisted Z64 numerator is also bounded below by(1). Consequently the actual perturbed cell endpoints satisfy

    S>=S0/F32(r)², T>=T0/F64(r)².                         (2)

All perturbation losses in(2) concern finite seed patches only. The subsequent spatial/thermal recursion belongs to the actual alternating model. No extensive norm is subtracted from a thermodynamic gap.

## 4. Positive cell operator and all-integer windows

The independently accepted positive-cell proof uses nonnegative bond-history measures mu1,mug and the real symmetric one-site chronological kernel k. The operator A_g:L²(mug)->L²(mu1) is Hilbert–Schmidt and the cell transfer is A_g A_g*, hence positive trace class. It is not an unjustified product of two self-adjoint operators on one Hilbert space. Its appropriately shifted Mth trace is the physical alternating partition function for every integer M>=2 and g>=0. Every g here is positive.

At cell base n and actual tau, let s,t be lower bounds on spatial purity S(n,tau) and physical thermal purity T(2n,tau). For n<=M<=2n, positivity gives

    Z_M(2tau)>=Z_(2n)(2tau)^(M/(2n)),
    Z_M(tau)<=Z_n(tau)^(2−M/n) Z_(2n)(tau)^(M/n−1).

After cancellation,

    T(M,tau)>=s^(2−M/n)t^(M/(2n))>=min(s sqrt(t),t)=C.    (3)

Every integer cell size in each window is included. C>1/2 forces a unique largest Gibbs eigenvalue and, since the largest weight is at least its purity, the excited-to-ground ratio is at most(1−C)/C. The directed inequality C−exp(tau_upper D)(1−C)>0 therefore proves a gap greater than D for that window.

Sequential updates remain

    G(x)=1−(1−x)²/(2x²),
    s_new=G(s²t), t_new=G(t² s_new),
    (n,beta)->(2n,2beta).

Each actual tau=beta/c has upper bound beta(1+r), because1/c=1+eta. The newly obtained s is used in the second update, all inputs and usable outputs are checked in(0,1], and every saved window margin is strictly positive.

At a common defect u=max(1−s,1−t)<=.01, the next defects are at most5u²: the pre-squaring defect is at most3u and9/[2(.97)²]<5. The same holds for the thermal update since2u+5u²<=3u. Thus future defects satisfy u_j<=(5u)^(2^j)/5. Equation(3) yields C_j>=1−3u_j/2, and(1−C_j)/C_j<=2u_j. Therefore the exact terminal test

    5u exp[beta(1+r)D]<1

closes every subsequent integer-cell window. The four rows close at cell256,256,512,512 after5,5,6,6 checked windows respectively. All22 finite-window margins and all four terminal margins are exact positive rationals in certificate.json.

## 5. Finite cells and the active bottleneck

Cell sizes2..15, physical lengths4,6,...,30, retain the existing accepted uniform all-size gap delta0=31/1250. Weyl and||B_L||<=3L/2 give only on this finite prefix

    gap(H_M(g))>=c(delta0−3L|eta|)
               >=(delta0−90r)/(1+r).                     (4)

The numerator is positive in every row. Solving(4)>=D gives exactly

    r<=(delta0−D)/(90+D).

Each chosen radius equals this upper endpoint, so the finite bridge margin is exactly zero at the coarsened worst case, and the guaranteed gap is still at least the strictly positive D. The inequality is closed and proves uniqueness. The infinite bootstrap windows all have strict slack. Thus these widths are maximal for this particular unchanged bridge, not optimal intervals for the actual model or for all available finite data.

The physical24 parity/MPS48 provenance is untouched: this bridge uses the already accepted all-size .0248 theorem rather than inventing a new physical24 own-anchor certificate. A future scalar-only finite-prefix improvement could use stronger accepted length-specific purities, but it is outside this package.

## 6. Exact checks, source preservation and resource accounting

All arithmetic uses rational endpoints on a160-place decimal grid. Square-root bounds are checked by integer squaring. Exponentials use140 positive Taylor terms after reducing the argument below1/16, a geometric bound for the next-term tail, and outward repeated squaring. Negative exponentials use reciprocal endpoints. Cosh upper endpoints average the two exponential upper endpoints. The grid rounds down s,t,C and up trace-loss factors and gap exponentials.

The first planned candidate for every target was the exact finite-bridge limit. All four passed, so no search rejection, fallback or retry occurred. The script also defines a bounded rational search for rejected sufficient candidates; that branch was not used. No new physical state, thermal trace, contraction, matrix moment or eigensolver is computed. There is one retained linear trial vector with MPS bond dimension26; the physical anchor Hilbert dimension is3^64.

The guard is separately named and has child hard limits28CPU seconds/256MiB, CPU4, a90-second wall watchdog and active process-CPU polling with kill threshold27seconds. The parent has a one-second CPU reserve, keeping hard aggregate accounting below the authorized30. Postexec checks verify hard limits, sole affinity, default/unblocked SIGXCPU and parent-death SIGKILL. Independent wait4 reports .452154CPU seconds and15268KiB; parent measured .006521998CPU seconds;26 active polls; wall .540158496seconds. No watchdog fired.

Eleven source manifests are pinned, and all members are verified when represented by simple filename/hash maps. Their exact hashes and additionally read inputs are saved in INPUT_SHA256.json. This includes the old structural/interval packages and both new observable producer packages. All old seals, failed32 history, root documents and remote state remain unchanged. Reproduction should use a disposable copy because output/resource paths are exclusive. This is an exact-arithmetic mathematical certificate, not a formal proof-assistant result.
