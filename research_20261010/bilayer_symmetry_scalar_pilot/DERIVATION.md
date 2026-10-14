# Square symmetry in the bilayer purity recurrence

2026-10-11 00:28 UTC / 2026-10-10 20:28 EDT.

This derivation concerns the accepted physical inputs for the ordinary bilayer at g=.11. Rung exchange is 1, the x and y intralayer exchanges are equal, and periodic multiedges follow the existing convention. The bounded scalar pilot includes no physical matrix contraction or spectrum calculation.

## Square-base symmetry

For a square base (n,n,beta), isotropy gives Z(L,W;t)=Z(W,L;t). In the time-first staircase a=T(n,n;beta), b=Sx(n,n;2beta), c=Sy(2n,n;2beta), the missing Sy(n,n;2beta) equals b exactly. Consequently the already reviewed direct signed-transfer finite-window argument yields

T(L,W;beta) >= a^4 (2b-1) sqrt(2 b^2 sqrt(2c-1)-1)

for every integer n<=L,W<=2n, when c>1/2, b>1/2, and b^2 sqrt(2c-1)>1/2. This follows by replacing the conservative bound d=b sqrt(c) in that argument by the exact symmetry equality d=b. No time/space interchange or spatial-temperature monotonicity is used.

The integer-resolved variant on square targets L=W is also valid. For p=L/n and w(z)=(1+sqrt(2z-1))/2, define h(z,p,L)=w(z)^p-(1-w(z))^p at odd L and h(z,p,L)=w(z)^p at even L. Then A_L=a^p h(b,p,L), B_L=b^p h(c,p,L), and

T(L,L;beta) >= A_L^p h(B_L,p,L)

whenever B_L>1/2. The actual base L=n can retain its stronger thermal input a. Integer-resolved powers are proposal-only unless separately enclosed in exact arithmetic.

## Coupled updates at a common base point

At an even spatial base v, write P_i(v)=Z(D_i v)/Z(v)^2. All three axes give purities in [0,1]. For a square plaquette set a=P_i(v), b=P_j(D_i v), c=P_j(v), d=P_i(D_j v). The exact identity d c^2=b a^2 implies the four monotone lower-bound updates below.

 d >= b a^2, c >= a sqrt(b), b >= d c^2, a >= c sqrt(d).

Same-axis squaring gives P_i(D_i v)>=G(P_i(v)), with G(p)=1-(1-p)^2/(2p^2). Same-axis purity monotonicity also gives P_i(D_i v)>=P_i(v). For spatial axes, every base length is even. Thermal purity is monotone in inverse temperature, but no analogous monotonicity of spatial purity with temperature is used.

Finally spatial coordinate exchange identifies P_x(nx,ny;t)=P_y(ny,nx;t) and P_t(nx,ny;t)=P_t(ny,nx;t). Taking a maximum of valid lower bounds remains valid. Applying these rules on a bounded coordinate lattice is sound, though it is not claimed complete or optimal. The lattice coordinates below are powers of two relative to the common post-cycle (8,8,2beta) base. Missing inputs begin at zero and never authorize physical conclusions by themselves.

All floating propagation is diagnostic only. A positive all-size proposal requires a fresh directed rational replay from exact physical trace bounds and exact finite-window/gap witnesses. A failed bounded closure is not an all-method no-go.

## Stronger complete square cycle

The independently checked recurrence is

 a'=G(a^4 b^2 c), b'=G(a' c^2), c'=G(c^4 a'^2 b').

For the middle step, spatial reflection identifies Sx(n,2n;2beta)=c_actual. Time exchange then gives Sx(n,2n;4beta)=T(2n,2n;2beta)c_actual^2/T(n,2n;2beta)^2 >= a' c^2. Squaring in x gives the displayed b'. The final ordinary y update uses the correctly based sequence (c,a',b'). Every update requires its stated positivity conditions. This compact recurrence agrees with the bounded general closure through the first updated square. At later cycles the closure can retain additional stronger bounds. Neither actual-input path reaches a small-defect seed in this pilot.

The independent square-window proof has seal 890e942c8a7e37cbefc5b8de52f40f8d61cbfefe76e03f8a71f9dec8d66648cc. The complete-cycle proof has seal 21577fcf285cc7e53c6c4acdbdfa1086f1b7dd88f6f30c4e87e0ebf5f0ac5e83.
