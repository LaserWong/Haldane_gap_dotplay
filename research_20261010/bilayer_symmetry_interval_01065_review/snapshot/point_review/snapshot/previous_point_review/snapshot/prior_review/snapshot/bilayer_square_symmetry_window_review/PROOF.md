# Square-isotropic direct-window strengthening

## Scope and statement

Ordinary isotropic bilayer with identical x/y couplings, periodic weighted-edge convention, positive physical partition functions, and the accepted self-adjoint spatial history transfer for every integer transverse circumference≥2. Let n≥2 be even and β>0. At one common square base define actual ratios

A=T(n,n;β), B=Sx(n,n;2β), C=Sy(2n,n;2β).

Take certified lower bounds 0<a≤A, 0<b≤B, 0<c≤C, all≤1. If c>1/2, b>1/2, and s=b² sqrt(2c−1)>1/2, then every integer rectangle n≤L,W≤2n satisfies

T(L,W;β) ≥ a⁴(2b−1) sqrt(2b² sqrt(2c−1)−1).

This is a theorem strengthening the previous exchange-based factor. It is not a numerical g=.11 certificate. No floating search or physical contraction is performed in this review.

## Proof with odd sizes

Coordinate exchange is a unitary equivalence of the isotropic physical Hamiltonians, including weighted parallel edges. Therefore Z(L,W;t)=Z(W,L;t) at the same temperature. In particular Sy(n,n;2β)=B≥b. This replaces only the old missing-edge lower b sqrt(c); it does not change the rectangular edge C.

Use the accepted direct signed-transfer lemma at fixed x=n. It gives T(n,W;β)≥a² sqrt(2b−1). Separately, interpolation in y of the spatial x ratio gives Sx(n,W;2β)≥b² sqrt(2c−1)=s. Its numerator is the y-transfer trace at x=2n and uses purity C; its denominator is at x=n. No square symmetry is asserted at the intermediate rectangle (n,W).

For every fixed W, apply the same direct thermal lemma in x at even base n, using the two preceding lower bounds. Squaring the thermal bound produces a⁴(2b−1), and the second spatial factor is sqrt(2s−1), giving the result.

Odd L and W are covered by the accepted signed-transfer lemma, not positivity of the transfer. At an even base, normalized even powers form a probability distribution. Purity z>1/2 forces a unique largest absolute eigenvalue, positive because all odd physical traces are positive. Writing w(z)=(1+sqrt(2z−1))/2 and r∈[1,2], the odd numerator has lower factor w^r−(1−w)^r≥sqrt(2z−1); the even numerator has lower factor w^r≥sqrt(2z−1). Denominator absolute-spectrum norm monotonicity uses the even base. The all-integer transverse transfer premise remains essential.

All displayed functions are increasing in the certified lower endpoints on the legal domain. Directed downward square-root/arithmetic bounds therefore preserve validity. The stronger factor is at least the old a⁴(2b sqrt(c)−1)sqrt(2s−1) wherever the latter is legal. Numerical evaluation needs exact gates, not a positive floating estimate.

## Integer-resolved optional variant

Let p=L/n, q=W/n and h(z,r,k)=w(z)^r−(1−w(z))^r for odd k, w(z)^r for even k. Set A_W=a^q h(b,q,W), B_W=b^q h(c,q,W). Then

T(L,W;β)≥A_W^p h(B_W,p,L)

whenever B_W>1/2. For squares take p=q. At the actual base keep the stronger original input a if useful. Fractional powers require separately certified enclosures; this review does not implement them. Swapping target L and W is allowed only by the physical coordinate-exchange identity, not by changing the base of a saved edge.

## Exact full-cycle recurrence and labels

Axes are x,y,t; doubling maps D_i commute. P_i(v)=Z(D_i v)/Z(v)^2. A time-first ladder at v=(n,n,β) is

[a,b,c] = [P_t(v),P_x(D_t v),P_y(D_xD_t v)] lower bounds.

The accepted cyclic update appends G(a⁴b²c), where G(z)=1−(1−z)²/(2z²), after rotating the first axis. The appended ratio is P_t(D_xD_yD_t v). Thus the three successive intermediate bases/orders are:

1. (n,n,2β), order xyt, ladder [b,c,r].
2. (2n,n,2β), order ytx, ladder [c,r,s1].
3. (2n,2n,2β), order txy, ladder [r,s1,u].

Here r=G(a⁴b²c), s1=G(b⁴c²r), u=G(c⁴r²s1), rounded down and used only while positive. The final new b=s1 is indeed Sx(2n,2n;4β), while the new c=u is Sy(4n,2n;4β). Therefore the square theorem applies at every complete cycle. The second intermediate base is rectangular and must never receive square-axis identification. The first intermediate square has a canonical xyt ladder, whose middle entry c is still a rectangular edge.

Canonical xyt at (n,n,β) means [Sx(n,n;β),Sy(2n,n;β),T(2n,2n;β)]. Its middle component is not Sx(n,n;2β). Canonical_advance preserves these canonical labels at the doubled base; it does not make its components raw txy. Any exchange transport or componentwise maximum must match exact edge labels before using the theorem.

The symbolic checker verifies all telescoping exponents and rotated labels for eight cycles. This tests geometry, not the numerical validity of any supplied initial ratios.

## Basepoint-aware closure audit

For distinct i,j set a=P_i(v), b=P_j(D_i v), c=P_j(v), d=P_i(D_j v). Exact partition-function cancellation gives d c²=b a². Because all relevant purities are≤1, valid lower updates are d≥ba², c≥a sqrt(b), b≥dc², a≥c sqrt(d). The checker verifies the formal partition exponents on81 plaquettes.

Same-axis squaring is valid for every nonnegative probability sequence w: with p=Σw², the doubled purity is Σw⁴/p². Hölder gives Σw⁴≥p³, hence monotonicity. Also p²−Σw⁴=2Σ_{i<j}w_i²w_j²≤(1−p)²/2, giving the lower G(p). Thermal Gibbs weights are nonnegative; spatial powers are nonnegative because every dyadic spatial base is even. This does not imply spatial purity is monotone in temperature.

Spatial exchange must map both coordinates and direction: P_x(nx,ny;t)=P_y(ny,nx;t), and P_t(nx,ny;t)=P_t(ny,nx;t). The pilot implementation uses exactly this mapping. Its extracted raw keys at cycle j are ((j,j,j),t), ((j,j,j+1),x), ((j+1,j,j+1),y); canonical keys are ((j,j,j),x), ((j+1,j,j),y), ((j+1,j+1,j),t). They have the required common base and temperatures. Taking maxima of valid lower bounds is sound. A floating propagation threshold affects only proposal strength, not a rigorous certificate; exact directed replay is required for every quantitative conclusion.

## Conclusion

Accept the square finite-window lemma and the stated basepoint-aware recurrence/closure rules. This review does not certify a g=.11 gap, initial physical trace values, a successful infinite recurrence, or a global impossibility from failed floating temperatures. A numerical proposal must separately replay exact saved physical inputs, every finite window, the terminal theorem and the short-size bridge.
