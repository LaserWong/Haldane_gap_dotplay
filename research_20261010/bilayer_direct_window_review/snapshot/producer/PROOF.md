# Direct time-first two-dimensional finite windows

2026-10-10 22:25 UTC / 18:25 America/New_York. Producer candidate awaiting independent review. Existing physical inputs only. No prior sealed files, project-root files, or remote state are changed.

## Exact statement and geometry

Assume positive physical partition functions and the previously accepted self-adjoint Hilbert–Schmidt spatial history transfers in each direction for every fixed transverse integer circumference >=2 and temperature. The ordinary bilayer satisfies these premises by bilayer_audit/PROOF.md, section4. Fix even n,m>=2 and beta>0. Define the actual time-first staircase

 a_actual = Z(n,m;2beta)/Z(n,m;beta)^2,
 b_actual = Z(2n,m;2beta)/Z(n,m;2beta)^2,
 c_actual = Z(2n,2m;2beta)/Z(2n,m;2beta)^2.

Let a,b,c in (0,1] be respective lower bounds. Set

 d=b sqrt(c), s=b^2 sqrt(2c-1).

If c>1/2, d>1/2 and s>1/2, then every integer rectangle n<=L<=2n, m<=W<=2m obeys

 T(L,W;beta) >= a^4 (2d-1) sqrt(2s-1).

All spatial inputs in this formula are at 2beta; the output thermal ratio is at beta. The second spatial edge is based at (2n,m), not (n,m). The three scalars cannot be relabeled from a canonical xyt ladder without valid transport.

## Proof

For an even base length k and a self-adjoint spatial transfer Y at temperature2beta, the normalized eigenvalues of Y^k are a nonnegative probability sequence. Purity >=z>1/2 bounds the largest weight below by w(z)=(1+sqrt(2z-1))/2. Its associated eigenvalue is unique in absolute value and positive, since otherwise sufficiently large odd physical traces would be negative. For r=M/k in[1,2], signed tail control gives a numerator factor

 h(z,r,M)=w(z)^r-(1-w(z))^r if M is odd,
 h(z,r,M)=w(z)^r if M is even.

Absolute-spectrum norm monotonicity at the even base controls the denominator, including odd target lengths. This is the accepted one-dimensional direct time-first lemma. The uniform inequality h>=sqrt(2z-1) follows from concavity in w of w^r-(1-w)^r-(2w-1), whose endpoint values vanish. No positivity of the transfer itself or odd-base purity is assumed.

First obtain a missing transverse spatial ratio D=Sy(n,m;2beta). Write E=Sx(n,2m;2beta). Both base exponents m and n are even, so D,E<=1. Exact spatial exchange gives b_actual^2 c_actual=D^2 E. Hence D>=b sqrt(c)=d.

At fixed x=n, apply the direct one-dimensional thermal lemma in y to a and D>=d. This gives T(n,W;beta)>=a^2 sqrt(2d-1).

Separately, apply the same signed-transfer power argument to the spatial ratio Sx(n,W;2beta). Its numerator is a y-transfer trace at x=2n with purity c; its denominator is the square of the y-transfer trace at x=n. With q=W/m, norm monotonicity gives

 Sx(n,W;2beta)>=b^q h(c,q,W)>=b^2 sqrt(2c-1)=s.

Finally fix each integer W, including odd W, and apply the direct one-dimensional thermal lemma in x at even base n. The premises hold at this transverse width by the all-integer transverse transfer theorem. Squaring the previous thermal bound and multiplying by sqrt(2s-1) proves the displayed result. All functions used are increasing in their certified lower endpoints on the stated domain, so downward rounding is valid.

An unused stronger integer-resolved statement follows from q=W/m, p=L/n:

 A_W=a^q h(d,q,W), B_W=b^q h(c,q,W),
 T(L,W;beta)>=A_W^p h(B_W,p,L), when B_W>1/2.

The uniform statement is used for the numerical certificate; no fractional-power implementation is needed.

## Saved physical inputs and exact scalar composition

Model: ordinary spin-half bilayer, rung coupling1, straight intralayer g=1/10, periodic multiedges. Use the accepted three inputs in bilayer_complete_residual_8x4/scalar/input_{4x4,8x4,8x8}.json. Denominator retained counts49/97, search dimensions11/43; numerator retains one43D-search Rayleigh vector. Largest physical dimension2^128. No new physical contraction, diagonalization, trial-state search or cutoff estimate is made.

The inherited initial txy thermal-trace calculation and coupled raw/canonical updates are unchanged. At initial beta187/20, the first common state is n=m=8 and physical beta187/10. Each full cycle doubles n,m,beta. Raw txy edges are transported to canonical xyt with the accepted exchange lemma, and the componentwise maximum of valid canonical bounds is used. The complete joint ratio is retained, always at the same common physical base.

The new finite-window formula checks [8,16], [16,32], [32,64], [64,128], [128,256], [256,512], and [512,1024]. At n=m=1024, beta11968/5, the established canonical small-common-defect theorem applies. Its exact witness is exp(beta*gap)*32u<1 with u=max canonical defect and 0<u<=1/500. The previously accepted short-size bound covers L2,...,7 and exceeds0.3. Therefore every integer square L>=2 has a unique finite-volume ground and

 gap >= 55580714827/10^12 = .055807148827.

This improves the accepted g=.10 point lower bound .038976038275, conditional on independent acceptance of this new lemma/composition. It does not extend the coupling range or change the accepted whole[0,.10] bound .001945771244.

## Arithmetic, reproduction, and limits

scan.py is bounded floating proposal search, beta6..20 by.05, at most7 states. Near-one floating cancellation overestimated some terminal scores; only replay.py results are used. replay.py encloses square roots by integer-square checks at120 decimals, rounds recurrence results downward at120 decimals, and verifies each proposed gap with the inherited rational192-bit exponential upper bound. Initial thermal traces retain the inherited exact rounding. The displayed gap is accepted by exact inequalities, not floating logs.

replay.json records nine exact checks (three temperatures and three terminal lengths); candidate.json selects the largest verified minimum. REPRODUCE.sh verifies file/dependency seals and reruns those nine paths to replay_check.json, leaving sealed results unchanged, then compares every non-timing result. CPU3, one library thread, <=600CPU seconds and700MiB address space per job. The complete exact replay takes about3 seconds and below30MiB. No claim of an all-temperature optimum or a frontier obstruction is made.
