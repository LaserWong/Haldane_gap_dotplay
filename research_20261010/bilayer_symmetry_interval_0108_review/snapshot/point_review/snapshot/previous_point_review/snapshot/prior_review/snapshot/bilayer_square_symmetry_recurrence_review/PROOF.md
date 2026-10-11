# Stronger square-preserving recurrence

This is an additional exact theorem after the independently sealed square-window review. It has the same physical assumptions and raw txy input labels at (n,n,β): a≤T(n,n;β), b≤Sx(n,n;2β), c≤Sy(2n,n;2β). Every input lies in(0,1], and n is even. Define G(z)=1−(1−z)²/(2z²).

Provided all three new bounds are positive, a valid raw txy ladder at the doubled square (2n,2n,2β) is

a′=G(a⁴b²c),
b′=G(a′c²),
c′=G(c⁴a′²b′).

All operations may be rounded downward. Arguments must be positive, and every lower bound must retain its exact basepoint and temperature.

## First edge

The accepted full cyclic bootstrap update gives a′≤T(2n,2n;2β). This is the same first step as the previously accepted plain recurrence; no new symmetry inference is needed here.

## Improved second edge

Reflect the old rectangular c edge correctly:

Sy(2n,n;2β)=Sx(n,2n;2β).

Let τ=2β. Write C=Sx(n,2n;τ), A=T(2n,2n;τ), E=T(n,2n;τ), D=Sx(n,2n;2τ). Exact partition cancellation gives

D E²=A C².

Since E≤1 is a physical thermal purity, D≥A C²≥a′c². This identity changes both the spatial rectangle and direction through the physical reflection. It never asserts Sx(2n,n;τ)=Sy(2n,n;τ).

At temperature2τ and transverse width2n, the x transfer has even base exponent n. Same-axis squaring of its nonnegative normalized n-th eigenvalue powers gives

Sx(2n,2n;2τ)≥G(D)≥G(a′c²)=b′.

G is increasing on(0,1]. This is exactly the desired new raw middle edge Sx(2n,2n;4β). The old plain argument b⁴c²a′ is weaker by its extra factor b⁴≤1; therefore the new b′ is at least as strong on the positive domain.

## Third edge and iteration

At intermediate base (2n,n,2β), the valid ytx ladder is [c,a′,b′], with edges Sy(2n,n;2β), T(2n,2n;2β), Sx(2n,2n;4β). Applying the accepted cyclic update yields c′≤Sy(4n,2n;4β). Thus [a′,b′,c′] has the full raw txy labels at (2n,2n,2β), and the construction repeats without relabeling a fixed rectangle.

The stronger square direct-window factor from the prior review applies to each input or output ladder whenever its separate gates hold. Passing a recurrence positivity gate does not itself prove the finite-window purity exceeds1/2 or produce an all-size gap.

## Verification and scope

The exact checker verifies partition exponents for the reflected time-exchange plaquette, the same-axis source/target labels, the third cyclic step and eight complete doubled cycles. Rational fixtures verify the stronger b′ and c′ dominate their plain counterparts. The predecessor window proof and seal are pinned. There is no floating search, physical input replay or numericalg=.11 certificate in this package. Quantitative claims still require directed physical trace replay, every short/finite window and the terminal theorem.
