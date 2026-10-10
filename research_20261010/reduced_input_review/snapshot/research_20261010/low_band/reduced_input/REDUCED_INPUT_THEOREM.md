# A largest-seed Rayleigh bound is enough for the t,x,y route

2026-10-10 14:41 America/New_York / 18:41 UTC.

This theorem is independent of the particular spectral-tail method used on the
two smaller seeds. The current numerical records use the independently reviewed
quadratic-boson reference on 4x4 and 8x4. The complete earlier full-band proofs
remain unchanged. New reduced-input numerical records require their own review.

## 1. Exactly which partition-function bounds are needed

Let v=(n,n,beta), with even n, and use the ordered time,x,y staircase. The three
initial edges are

    q1 = Z(n,n;2beta)/Z(n,n;beta)^2,
    q2 = Z(2n,n;2beta)/Z(n,n;2beta)^2,
    q3 = Z(2n,2n;2beta)/Z(2n,n;2beta)^2.

The correlated first-cycle inputs are exactly

    J1 = q1^4 q2^2 q3
       = Z(2n,2n;2beta) / Z(n,n;beta)^8,
    J2 = q2^4 q3^2
       = Z(2n,2n;2beta)^2 / Z(n,n;2beta)^8,
    C0 = q3
       = Z(2n,2n;2beta) / Z(2n,n;2beta)^2.

Consequently it is sufficient to know only

    L <= Z(2n,2n;2beta),
    Z(n,n;beta) <= U0,
    Z(n,n;2beta) <= U1,
    Z(2n,n;2beta) <= U2.

Then J1>=L/U0^8, J2>=L^2/U1^8 and C0>=L/U2^2. The largest seed never appears in a
denominator. Its complete spectrum, spectral count, lower energy estimates,
residuals, and squared-Hamiltonian moments are absent from these requirements.

Writing G(z)=1-(1-z)^2/(2z^2), the sequential cycle gives the lower bounds

    a=G(J1), b=G(J2 a), c=G(C0^4 a^2 b).

These are a time,x,y staircase at (2n,2n,2beta). Exact adjacent swaps produce
canonical spatial,spatial,thermal lower bounds

    A=a sqrt(b), B=a^2 b sqrt(c), C=a^4 b^2 c

at that same basepoint. Only after this transport is the canonical all-integer
bootstrap/interpolation theorem applied. Each intermediate purity lower bound
must be positive before it is reused.

## 2. One Rayleigh quotient supplies the largest lower trace

Let H_max be the finite-dimensional Hamiltonian on the largest seed, and let
psi be any normalized trial vector. It need not be a certified ground state, a
Ritz eigenvector, or part of a complete low band. For tau>0, spectral Jensen
convexity gives

    exp[-tau <psi,H_max psi>]
       <= <psi,exp(-tau H_max) psi>
       <= Tr exp(-tau H_max).

Thus L=exp(-2beta rho), with rho=<psi,H_max psi>, is sufficient for Section1.
For an integer coefficient vector c in a nonorthogonal trial basis W, only

    G=W*W, A=W*H_max W, rho=(c*A c)/(c*G c)

are needed. The denominator must be positive. No W*H_max^2 W, residual, or
external lower spectrum is involved. The word "ground" in a filename describes
the optimization target, not a hypothesis of this lower-trace theorem.

## 3. Optional improvement from several trial directions

For any orthonormal collection psi_1,...,psi_k, the same argument gives

    sum_i exp[-tau <psi_i,H_max psi_i>]
      <= sum_i <psi_i,exp(-tau H_max) psi_i>
      <= Tr exp(-tau H_max).

For a full-rank nonorthogonal W, form G=W*W>0 and A=W*H_max W. Diagonalizing the
finite compression G^(-1/2) A G^(-1/2) gives an orthonormal collection in ran W
with Rayleigh quotients theta_i. Hence

    sum_i exp(-tau theta_i) <= Tr exp(-tau H_max).

Verified upper enclosures for theta_i only decrease this lower bound. There is
no assumption that these Ritz values account for every low eigenvalue. The
ordinary variational min-max principle gives another proof of the same finite
trace lower bound, without any external eigenvalue count.

The optional 193-direction variant uses one even-parity spin-singlet trial plus
64 odd-parity spin-one translation directions and their three exact SU(2) spin
copies. Their Gram and first moments are block-circulant, so the theta_i are
computed from G/A Fourier symbols in Q(sqrt(2)). Its largest input contains no B
or H^2 symbol. The 193 directions are orthogonal trial directions after Gram
normalization, not assumed exact eigenstates or a certified complete low band.

## 4. Actual minimal consumer and historical extraction

`export_minimal.py` is a one-time historical extraction from comprehensive,
previously audited artifacts. It writes eight new largest-seed files containing
only ground G/K/coefficients or optional translated G/A data. This preparation
step is distinguished from the reduced certificate consumer.

`replay_minimal.py` consumes those minimal files directly. Its ground_only mode
never opens the optional largest translated file. Neither mode opens a largest
full-band certificate, number-sector file, squared-Hamiltonian matrix, or
residual record. Each input schema has an explicit allowed-field check, and
each numerical file actually read is recorded with its SHA-256. Historical
source hashes are provenance strings; the consumer does not dereference them.

The only upper-trace inputs are the 4x4 and 8x4 quadratic-tail certificates. The
largest physical seed is still 8x8, but the maximum seed requiring full residual
and complete-tail certification is now 8x4. The ground_only largest numerator
has trace rank one, formed from a 29-dimensional symmetry/Krylov trial basis.
These ranks and linear trial dimensions are different quantities.

The reviewer additionally rebuilt the largest ground's needed F/S geometry
without computing V/W residual geometry or entering the q6 loop. Thus the
reduction can be realized in physical input generation, not merely by omitting
fields after a larger computation.

## 5. Numerical comparison protocol

For each g=.03,.04,.05,.06, use the same inverse temperature selected in the
accepted 193-direction quadratic-tail txy record. Evaluate both numerator
choices with directed exact arithmetic, transport both to the canonical
staircase, and replay all finite-window and short-size bridges. No new
optimization or changed denominator can explain a difference between the two
reported bounds. The final records are separated by ground_only and trial193.

## 6. Shared short-size comparison and output

For every g<=gm=.06, the same gm comparison matrix is a valid lower form on a
fixed physical number compression. Indeed, with x_q=||psi_q||>=0 and
||C_+(g)|_q||<=g c_q, one has

    <psi,H'(g)psi>
      >= sum_q (1-2gm)q x_q^2 - 2 sum_q gm c_q x_q x_(q+2)
       = x^T J(gm) x >= lambda_min(J(gm)) ||psi||^2.

Both parity chains of Q>=1 are included. Their already certified gm endpoints
therefore give the same lambda_2 lower bound at every smaller g. The singlet
product has shifted Rayleigh quotient zero at every g, so lambda_1<=0 and the
positive short-size gap follows. This argument does not assume monotonicity of
the physical gap. An equivalent proof observes that the minimum of the
negative-off-diagonal scalar Jacobi form can be taken on nonnegative vectors.

The exact reduced-input candidate comparison is:

| g | one-vector largest numerator | 193-direction largest numerator |
|---|---:|---:|
| .03 | .318085338503 | .318085460990 |
| .04 | .235117533454 | .235117964607 |
| .05 | .171818025695 | .171822115684 |
| .06 | .103485296797 | .103487228301 |

Every entry includes all integer square sides L>=2. Independent numerical
review is pending at this freeze. The greatest absolute loss from retaining
only one largest-seed Rayleigh term is .000004089989. This says nothing about
whether a single Rayleigh term would suffice in the denominator traces: those
still require complete upper-trace certificates on the smaller patches.
