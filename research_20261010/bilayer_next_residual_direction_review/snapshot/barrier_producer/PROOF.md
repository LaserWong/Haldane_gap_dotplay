#Cached moment barrier for the generic Krylov fourth-moment upper

##Conclusion

For the saved optimized57D8x4 witness at g=.11, the generic global spectral m4 upper cannot yield a negative two-vector Temple pencil at either selected ground target. The same is true of the stronger upper obtained from the2x2 interval-localizing moment PSD constraint. No physical contraction is used.

Global moment constraints alone leave a high-residual-Rayleigh region where those bounds could work, but that region is impossible for this actual q<=8 residual vector. This is a scoped obstruction to these particular m4 upper bounds and selected targets, not an obstruction to an exact-m4 Krylov calculation. An exact two-atom moment example obeying the stated spectral bounds and cutoff demonstrates that a sharper m4 could succeed.

##Known data and exact threshold

Let psi be the saved normalized57D endpoint vector. Set rho=m1, v=m2−rho²>0, eta=(H'−rho)psi, R=<eta,H'eta>/v. Then m3=rho³+2rho*v+vR. All rho,v,m2,ell0 (current physical ground lower), a=r2(.11), U=32(1+.11)=35.52 and the best ground upper are pinned exact rationals.

For a selected lower target L<a, the two-vector basis(psi,H'psi) has pencil

 P00=p=m2−(a+L)rho+aL>0,
 P01=m3−B, B=(a+L)m2−aLrho,
 P11=m4−(a+L)m3+aL m2.

A negative direction exists iff its determinant is negative, equivalently

 m4 < T(m3)=(a+L)m3−aL m2+(m3−B)²/p.

This is the necessary and sufficient threshold for the chosen two-vector negative-pencil test, assuming the exactm3,m4. Replacingm4 by an upper retains sufficiency but can lose this witness.

##Exact moment PSD interval and fourth-moment bounds

The localizing matrices for H'−ell0 and U−H' on span(1,H') give

 ell0*m2+(m2−ell0*rho)²/(rho−ell0) <= m3
 <= U*m2−(U*rho−m2)²/(U−rho).

In residual-Rayleigh coordinates this is

 Rmin=a+ell0−rho =1.1159999955606057...,
 Rmax=U−v/(U−rho)=35.519974529229486....

The simplification of Rmin uses the exact saved Temple identity ell0=rho−v/(a−rho); it is checked rationally.

The generic bound is M4=(U+ell0)m3−ell0*U*m2. A sharper bound from the PSD localizing matrix of (H'−ell0)(U−H') is

 M4star=M4−b1²/b0,
 b0=(U+ell0)rho−ell0*U−m2>0,
 b1=−m3+(U+ell0)m2−ell0*U*rho.

The ordinary3x3 moment Hankel PSD constraint also gives

 m4 >= m2²+(m3−rho*m2)²/v.

No moment is assumed to equal either upper. The bounds follow from the full spectral interval, not from projected H².

For either upper, D(R)=p*(M4upper−T(m3(R))) is an exact concave quadratic. derive.py saves all rational coefficients. For the generic bound D(Rmin)>0 and D(14.6)>0; for M4star D(Rmin)=0 and D(14.6)>0. Concavity proves D>=0 throughout[Rmin,14.6]. With p>0, both upper pencils are PSD everywhere in that interval, so neither furnishes a negative witness.

Exact72-bisection brackets locate the high roots:

- beta9.4 target: generic R>25.63018194734..., PSD-refined R>25.62347486715....
- beta10 target: generic R>26.19099903820..., PSD-refined R>26.18700391787....

Those large-root regions occur inside the broad global moment interval, so the generic moment data alone does not exclude them. The physical occupation support does.

##Contraction-free occupation bound R<=14.6

The periodic8x4 graph has32 rungs,64 unit-weight unordered edges and degree4. Write A=C+C†+D with C lowering triplet count by2. The input psi hasq<=6, hence eta=(H'−rho)psi has evenq<=8.

On fixedq, the triplet hopping part of D has norm<=4q: in the orthonormal occupation/color basis each ofq triplets can hop to at most4 neighbors, with unit amplitude. The occupied-pair spin1 interaction has norm<=2 on each occupied edge. Since sum_edges P_i P_j<=2Q on a degree4 graph, this part has norm<=4q. Thus ||Dq||<=8q. No bipartite assumption or bosonic replacement is used.

For C:q→q−2, a source occupation/color column has absolute sum<=2q, the maximum number of occupied edges. A target row has at most64 empty edges and3 singlet color components per edge, so its absolute sum<=192. Therefore ||Cq||²<=||Cq||_1||Cq||_infinity<=384q. The same bound follows in the usual magnetic triplet basis, whose singlet-pair coefficients all have magnitude1.

For an arbitrary vector supported onq=0,2,4,6,8, its H' Rayleigh is bounded by a symmetric5x5 occupation-norm matrix with diagonal q(1+4g) and adjacent off-diagonal(g/2)sqrt(384q). At g=.11 use the exact rational overestimates sqrt768<=28,sqrt1536<=40,sqrt2304=48,sqrt3072<=56. Its row-sum bounds are

 q0:1.54; q2:6.62; q4:10.60; q6:14.36; q8:14.60.

Gershgorin (or2uv<=u²+v²) yields R<=73/5=14.6. This is an upper on the COMPRESSED Rayleigh of eta. It must NOT replace the global U in a fourth-moment bound: H'eta reachesq10, and ||H'eta||² is not the square of the q<=8 compression.

##Exact moment example showing the scope of the obstruction

Take R=9/2 and the positive two-vector Gram diag(1,v), with H matrix [[rho,v],[v,vR]]. Its physical characteristic polynomial is(z−rho)(z−R)−v. The saved rational signs place the lower root in[ell0,ground_upper], the upper root in[a,U], and the lower root strictly above both selected targets. The resulting moments satisfy

 m3=−.025588813143692764...,
 m4=.025176731043900002....

For beta9.4, the required threshold is .02577964686874979..., while M4=.14595514397576348... and M4star=.12493547209911732.... For beta10 the threshold is .025422625254784257.... Thus an admissible exactm4 is below both target thresholds although both generic uppers fail badly. This is an abstract scalar moment model, not an assertion about the actual bilayer'sm3/m4 or its gap.

##Decision

Do not build the expensive physicalm3 calculation merely to combine it with the generic global-U or interval-PSD fourth-moment upper for these targets. That specific shortcut is now excluded for the savedpsi. A true Krylov route needs a materially sharper physicalm4 bound or the new exact normal-order contractions. The58D q6-shape fixture remains a simpler next bounded physical probe using the existing commutator; neither route is claimed sufficient.

CPU3,120CPU-second/100MiB exact arithmetic budget; measured derivation is below one second. No local operator contraction, large-support enumeration, optimizer or full ED ran.
