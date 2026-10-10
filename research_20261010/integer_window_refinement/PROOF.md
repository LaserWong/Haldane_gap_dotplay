# Integer-resolved and direct time-first signed-transfer windows

Updated 2026-10-10 18:11 EDT / 22:11 UTC. Research-only producer package; independent new-lemma review is separate. No predecessor, root-file, or remote edits.

## Hypotheses and basepoints

Use the previously independently established self-adjoint history transfer X_beta with Z_M(beta)=Tr X_beta^M for every integer M>=2, positive physical partition functions, and finite even moments. Fix an even integer n>=2 and beta>0. Let

- A=T(n,beta)=Z_n(2beta)/Z_n(beta)^2;
- B=S(n,2beta)=Z_2n(2beta)/Z_n(2beta)^2;
- S=S(n,beta), T=T(2n,beta), so A^2 B=S^2 T.

All these base lengths are even; A,B,S,T are in (0,1]. No spatial-purity assertion at an odd base is made.

Suppose A>=a>0 and B>=b>1/2. Put w=(1+sqrt(2b-1))/2 and q=M/n. Then for each integer n<=M<=2n,

    T(M,beta) >= a^q [w^q-(1-w)^q]           (M odd),
    T(M,beta) >= (a w)^q                     (M even).

Exact endpoint lower bounds A>=a at M=n and T>=a^2 b at M=2n may be used in addition.

### Proof, including the sign

The normalized eigenvalues of Y^n, Y=X_(2beta), form a nonnegative probability sequence with purity B>=b>1/2. Its largest weight w0 is unique and w0>1/2. Since B<=w0^2+(1-w0)^2, w0>=w. The associated eigenvalue mu0 of Y is uniquely maximal in absolute value. It is positive: a negative mu0 would make sufficiently large odd traces negative, contrary to the positive physical Z_M(2beta). The remaining relative eigenvalues satisfy sum_{j>0}|mu_j/mu0|^n=(1-w0)/w0. For q>=1, the power-sum inequality sum z_j^q <=(sum z_j)^q gives

    Z_M(2beta) >= Z_n(2beta)^q [w0^q-(1-w0)^q]

at odd M. At even M the tail is nonnegative and the bracket can be replaced by w0^q. Both expressions increase with w0.

Independently, Schatten power monotonicity gives

    Z_M(beta) <= Tr |X_beta|^M <= Z_n(beta)^(M/n).

Only the EVEN base n is used to replace its absolute trace by Z_n(beta); the target can be odd. Divide the numerator bound by the square of this denominator bound, and use A>=a. This proves the result without purity monotonicity in physical M or positivity of X_beta.

### Uniform simplification

For 1<=q<=2 and 1/2<=w<=1, define

    F(w)=w^q-(1-w)^q-(2w-1).

F(1/2)=F(1)=0 and, in the open interval,

    F''(w)=q(q-1)[w^(q-2)-(1-w)^(q-2)]<=0.

Thus F>=0. Since a^q>=a^2, the new uniform bound is

    T(M,beta) >= a^2 sqrt(2b-1),   n<=M<=2n, all integers.

The even-M bound is stronger than the signed expression. This proof is concavity in w, not an unproved concavity assertion in q.

## Canonical length-resolved refinement and the separate joint observation

For comparison with the existing canonical window, suppose S>=s,T>=t,S^2T>=K. Put p=max(s^2t,K)>1/2, w_p=(1+sqrt(2p-1))/2, r=(1-w_p)/w_p, and D=t/(1+r^2). The exchange identity and A<=1 give B>=p, hence the same signed tail control.

Because mu0^(2n)>=Z_2n(2beta)/(1+r^2), the original even-endpoint Holder denominator interpolation, with its exponent retained, gives

    T(M,beta) >= S^(2-q) [T/(1+r^2)]^(q/2) h_M,
    h_M=1-r^q for odd M, and h_M=1 for even M.

In particular use s^(2-q) D^(q/2) h_M rather than minimizing over all real q at once. The exponent is genuinely M/n, derived from transfer eigenvalue powers; no odd-base even-power positivity was assumed.

Retaining the joint product Q=S^2T>=K yields another valid lower bound (t'=max(t,K)):

    h_M K^(1-q/2) (t')^(q-1)/(1+r^2)^(q/2).

Take the maximum with the separate-component result. At q=1, this contains precisely S sqrt(D)>=sqrt(K/(1+r^2)). In the old uniform canonical rule with s=sqrt(P),t=K=P, the min D branch dominated, so the latter isolated observation cannot fix that rule. The direct time-first lemma instead retains the much stronger actual a,b before this lossy transport.

## Saved-input replay at g=1/4

The physical inputs are the already independently reviewed rank195 M4 counted denominator and saved two-vector M8 Rayleigh numerator. No physical spectrum or trial vector is computed here. At initial beta=942/125=7.536, the inherited time-first initialization gives

    J=lower Z8(2beta)/Z4(beta)^4,
    C=lower Z8(2beta)/Z4(2beta)^2,
    a=G(J)=.9116781571718575...,
    b=G(C^2 a)=.7123613406463991...,
    G(x)=1-(1-x)^2/(2x^2).

These a,b belong to (n=8, physical beta=2*initial beta=1884/125), not to the original base or temperature. Their joint P=a^2b=.5920841591623008... fails the old transported uniform gate, but the new uniform purity exceeds .542. Integer-resolved purity lower endpoints for M9,...,15 are approximately

    .60053171, .70134366, .59727604, .65330660,
    .58027573, .60855975, .55562299.

Both endpoints are bounded separately. `replay.py` encloses all exponentials and fractional powers rationally at 128 dyadic bits and verifies a shared gap 1/100 without logarithms, by exp(beta_window/100)<C/(1-C).

The initial [4,8] window uses A>=sqrt(J) and B>=C. The first assertion follows from the EXACT identity J_actual=A^2B and B<=1, not from an assumed sign of the variational energy shift. Its uniform lower bound J sqrt(2C-1) also passes gap1/100. The inherited local form at g1/4 gives positive direct M2,M3 gaps, with M3>.01568. Thus the new lemma plus inherited exact inputs gives a finite-size bridge gap>=1/100 for every integer 2<=M<=16, subject to independent new-lemma review.

This is NOT an all-size .25 certificate. At the displayed beta the next unchanged time-first recursion gives a_next=.76267458..., argument b^2 a_next=.38702583..., b_next<0. The bounded saved-input scan beta=2,...,30 by .01, with up to seven subsequent time and seven canonical rounds, finds no complete path. A finer startup diagnostic beta=.001,...,12 by .001 finds a largest next-spatial argument about .39274376, below the G-positivity threshold sqrt(2)-1. These finite scans do not prove any all-temperature exclusion.

A separate diagnostic replaces only the numerator with the unreviewed exact rational 17D block candidate supplied by the parent. It still finds no path on the same beta grid. This candidate test is clearly separated from the saved-input-only exact replay and does not certify its physical input.

## Improved complete saved-input scalar paths

Using sealed rank67 inputs for the three already accepted couplings, direct time-first windows, and canonical conversion only when useful, `replay_paths.py` verifies:

| g | Initial beta | Extra time cycles from n8 | Asymptotic onset | New uniform gap lower bound |
|---|---:|---:|---:|---:|
| .21 | 8.19 | 4 | 128 | .107424972 |
| .22 | 8.10 | 4 | 128 | .071581253 |
| .225 | 8.25 | 5 | 256 | .051807500 |

Every intervening [n,2n] integer window is checked, as are [4,8], M2,M3, and the established terminal small-defect exponential witness. These are exact directed-arithmetic scalar certificates over inherited physical premises, pending independent review of this new lemma and composition. No new coupling is certified.

The bounded floating scan proposes temperatures and paths only. In particular floating cancellation in a near-one terminal purity can overstate the final gap. The exact replay recomputes the defect rationally and checks each final rational gap directly. The final .225 gap was lowered accordingly.

## Toy checks, resources, and reproduction

`replay.py` first checks 1,088 exact rational inequalities for two-state classical ring transfers X=[[u,v],[v,u]], u,v in1,...,8 and n2,4,8. The doubled-temperature transfer has entries squared, so its spectrum is (u^2+v^2,u^2-v^2). There are476 tests with a negative subleading transfer eigenvalue. These are toy partition functions, not new spin-chain physical spectra. Exact calculations verify the actual target purity against the rigorously rounded proposed lower bound.

Run, from this directory:

    python replay.py
    python diagnostic.py
    python scan_paths.py
    python replay_paths.py
    python scan_candidate.py

Each script pins to CPU7 when available and limits address space to1GiB through replay.py. Individual saved-input jobs take seconds and approximately11MiB. `replay.json`, `path_scan.json`, and `replay_paths.json` distinguish exact checks from bounded floating diagnostics. Input hashes and final artifact manifest are recorded separately.
