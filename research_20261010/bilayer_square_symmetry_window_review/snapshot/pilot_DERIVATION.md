# Spatial symmetry and scalar closure: derivation before the bounded pilot

2026-10-11 00:28 UTC / 2026-10-10 20:28 EDT.

Only the accepted ordinary bilayer at g=.11 is considered. Unit rung exchange, equal x/y intralayer exchanges, and the periodic multiedge convention are unchanged. No physical matrix contraction or spectrum calculation is authorized in this pilot.

## Square-base symmetry

For square base (n,n,beta), isotropy gives Z(L,W;t)=Z(W,L;t). In the time-first staircase a=T(n,n;beta), b=Sx(n,n;2beta), c=Sy(2n,n;2beta), the missing Sy(n,n;2beta) equals b exactly. Consequently the already reviewed direct signed-transfer finite-window argument yields

T(L,W;beta) >= a^4 (2b-1) sqrt(2 b^2 sqrt(2c-1)-1)

for every integer n<=L,W<=2n, when c>1/2, b>1/2, and b^2 sqrt(2c-1)>1/2. This follows by replacing the conservative bound d=b sqrt(c) in that argument by the exact symmetry equality d=b. No time/space interchange or spatial-temperature monotonicity is used.

The integer-resolved variant on square targets L=W is also valid. For p=L/n and w(z)=(1+sqrt(2z-1))/2, define h(z,p,L)=w(z)^p-(1-w(z))^p at odd L and h(z,p,L)=w(z)^p at even L. Then A_L=a^p h(b,p,L), B_L=b^p h(c,p,L), and

T(L,L;beta) >= A_L^p h(B_L,p,L)

whenever B_L>1/2. The actual base L=n can retain its stronger thermal input a. Integer-resolved powers are proposal-only unless separately enclosed in exact arithmetic.

## Basepoint-aware closure

At an even spatial base v, write P_i(v)=Z(D_i v)/Z(v)^2. All three axes give purities in [0,1]. For a square plaquette set a=P_i(v), b=P_j(D_i v), c=P_j(v), d=P_i(D_j v). The exact identity d c^2=b a^2 implies four monotone lower-bound updates:

 d >= b a^2, c >= a sqrt(b), b >= d c^2, a >= c sqrt(d).

Same-axis squaring gives P_i(D_i v)>=G(P_i(v)), with G(p)=1-(1-p)^2/(2p^2). Same-axis purity monotonicity also gives P_i(D_i v)>=P_i(v); for space, every base length is even. Thermal purity is monotone in inverse temperature, but no analogous monotonicity of spatial purity with temperature is used.

Finally spatial coordinate exchange identifies P_x(nx,ny;t)=P_y(ny,nx;t) and P_t(nx,ny;t)=P_t(ny,nx;t). Taking a maximum of valid lower bounds remains valid. Applying these rules on a bounded coordinate lattice is sound, though it is not claimed complete or optimal. The lattice coordinates below are powers of two relative to the common post-cycle (8,8,2beta) base. Missing inputs begin at zero and never authorize physical conclusions by themselves.

All floating propagation is diagnostic only. A positive all-size proposal requires a fresh directed rational replay from exact physical trace bounds and exact finite-window/gap witnesses. A failed bounded closure is not an all-method no-go.
