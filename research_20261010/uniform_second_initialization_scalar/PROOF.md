# Conditional second-initialization scalar certificate

2026-10-10 23:25 UTC. Producer exact arithmetic; independent review pending. Conclusion: conditional gap>=23/5000 and unique ground state for EVERY integer L>=36. The condition is validity of all18 published beta49/4 thermal intervals. The existing nine independently reconstructed beta21/2 entries do not supply these premises. A separate four-small-case pilot does not discharge the full condition.

## Inputs and published replay

The model is the uniform periodic spin1 Heisenberg chain with unit bilinear exchange and linear shift a=700741/500000. Physical lengths here are at least36, safely above the official all-integer transfer identity floor4. The official initialization, thermal72, trials and assembly TeX are archived verbatim with Apache2.0 license. initialization Git blob a9a4604db87448b4e7d211ef483518b57862f097; thermal72 b9f3c87a4fcfa96a82cdb5d4daf30b6088428037; trials14be92f2308bc6758f3aac628e337a363caead77; assembly495b5810afe35da8d73fbf52ac4bdcc7be1f9f5f.

At beta49/4, the18 physical traces are identity/pi seam at EVERY n4..12, including odd n. The centers and error30e-6 are explicit in certificate.json. Set J_n=(Z_n+3P_n)/4 and N_n=(Z_n-P_n)/4, so Z_n=J_n+3N_n. J and N are ordinary eigenvalue lists counted with integer multiplicity; N repeats three times. The interval error eps=30e-6 is conservative for BOTH transformed lists. Odd moments retain their signs. No cyclic C seam or beta/2beta trace has been invented.

F_J=x^4(7+17x-280x^2-185x^3+1000x^4)^2 and F_N=x^4(12-394x^2+1000x^4)^2 are nonnegative on R. Their summed upper bounds use signed centered combinations plus eps times the absolute coefficient sum. Code reproduces exactly318604.54848175 and48169.880699. Endpoint comparisons at U=1.00139,V=.872 are strictly positive. For the J exterior rays, Q(1+y)=559+2902y+5165y^2+3815y^3+1000y^4 and Q(-1-y)=895+3978y+6275y^2+4185y^3+1000y^4, positive/increasing for y>=0. For N,12-394r^2+1000r^4 is positive atV and derivative4r(1000r^2-197)>0 for r>=V. Multiplication by x^4 preserves ray monotonicity. Thus every J modulus<U and N modulus<V.

The twelfth moments obey J12<=mJ=1.0657205,N12<=mN=.2783155. Let ell=.999 and C(m,h,r)=floor(m/h)*h^r+(m-floor(m/h)*h)^r. Ordinary nonnegative atom packing proves sum t_i^r<=C for r>=1. Define B(k)=3C(mN,V^12,k/12), R(k)=B(k)+(mJ-ell^12)^(k/12), k36,72. Code checks C(mJ,ell^12,6)+B(72)<1. The independently rebuilt72-site D26 Rayleigh anchor in audit/mps/contraction.out has positive norm and exact negative shifted energy (see audit/APPENDIX_A_BRIDGE.md). Hence Z72(beta)>1 at every positive beta. At beta49/4 this forces a J eigenvalue with modulus>ell. Removing one unit atom leaves the stated tail. Consequently S36>=(1+R36/ell^36)^-2 and T72>=(U^72+R72)^-2. The latter uses Z72(2beta)>1 and the beta trace upper bound, with the same physical72-site anchor.

These seeds give S>=.9520842289937825,T>=.8184798319671879. All six published upward10^-7 defect updates are reproduced EXACTLY, including the terminal2304/784 pair. This separately verifies the original scalar chain without asserting new thermal reproduction.

## Stronger continuation and ALL integer windows

The improvement here is high-precision downward purity rounding on10^-80 and additional canonical rounds, not a new moment cap. G(x)=1-(1-x)^2/(2x^2) is increasing for0<x<=1. At base(n,beta), S denotes S(n,beta) and T denotes T(2n,beta). Update Snew=G(S^2T), Tnew=G(T^2 Snew), then double n,beta. Every argument and result is verified positive/legal. There is no geometry relabeling.

At each state use the independently accepted signed all-integer interpolation: K=S^2T>1/2, w=(1+sqrt(2K-1))/2, rho=(1-w)/w, d=T/(1+rho^2), C=(1-rho)*min(S sqrt(d),d). Then T(L,beta)>=C for every integer n<=L<=2n. Directions: lower root gives upper rho; this decreases d,C, so directed endpoints remain conservative. The accepted proof infers a positive dominant spatial eigenvalue from positive physical traces at all sufficiently large odd lengths. No positivity of every eigenvalue is assumed.

Every dyadic window[36*2^j,72*2^j], j0..10, is checked with exp(beta*23/5000)(1-C)<C, which ensures unique physical ground state and gap>=23/5000. All window endpoints, C and positive exact margins are recorded. After ten updates, n=36864,beta=12544 and common defect u≈7.23115e-27. The accepted small-defect theorem applies (u<=.01); the exact inequality5u exp(beta*23/5000)<1 proves the same gap for every integerL>=36864. Earlier windows overlap and cover all integers36..36864 without gaps. An extra[36864,73728] check is retained.

Square roots are enclosed by exact integer-power bisection. Exponentials use positive Taylor degree120 after halving to argument<=1/16, next-term geometric tail, outward grid rounding and repeated squaring. Negative arguments use reciprocal enclosures. All certificate arithmetic is rational/integer; floats are display-only. The inherited all-integer interpolation/closure reviews are SHA-bound. This is no minimum-seed claim and does not claim anything below36.

## Resource/status

Scalar runtime .076CPU seconds,~10MiB RSS, CPU0. No eigensolver, new physical contraction, or imported upstream code execution. Reproduce with python certify.py. This exact conditional result is stronger than the original rounded log20/784 all-even tail but weaker in gap magnitude than the separately accepted.0102 tail from60. It extends prospective small-size coverage; thermal reconstruction and independent scalar review remain separate obligations.
