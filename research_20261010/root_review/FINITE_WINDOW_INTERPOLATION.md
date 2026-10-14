# Sharp finite-window signed-transfer interpolation

10 October 2026, 13:30 EDT / 17:30 UTC. The interpolation lemma transfers purity bounds to every integer size in a finite window, including odd lengths. Its proof is independent of the physical seed generator, and the low-band reviewer reconstructed both interpolation steps independently. Applying it to a new seed still requires verification of that seed.

## 1. One spatial direction

Assume an exact real self-adjoint Hilbert–Schmidt representation $Z_L(\beta)=\operatorname{Tr}X_\beta^L$ for every integer $L\ge2$, with strictly positive physical partition functions. Let $n$ be even. Suppose

$$
S(n,\beta)\ge S>0,\quad T(2n,\beta)\ge T>0,\quad p=S^2T>\frac12,
$$

where $S,T\le1$. Define

$$
w=\frac{1+\sqrt{2p-1}}{2},\quad r=\frac{1-w}{w},\quad D=\frac{T}{1+r^2},
$$

$$
I(S,T)=(1-r)\min\{S\sqrt D,D\}.
$$

Then every integer $n\le L\le2n$ obeys $T(L,\beta)\ge I(S,T)$.

The exact exchange identity and $T(n,\beta)\le1$ imply $S(n,2\beta)\ge S^2T=p$. Since $n$ is even, the normalized spectrum of $X_{2\beta}^n$ is a probability distribution. Its largest weight exceeds one half, and the inverse purity inequality bounds it below by $w$. Its unique largest-modulus underlying transfer eigenvalue must be positive. Otherwise all sufficiently large odd traces would be negative, contrary to positive partition functions.

Writing this eigenvalue as $\mu_0>0$ gives

$$
\sum_{j>0}\left|\frac{\mu_j}{\mu_0}\right|^n\le r<1.
$$

At power $2n$ the relative tail is at most $r^2$, so $\mu_0^{2n}\ge Z_{2n}(2\beta)/(1+r^2)$. At every integer $L\ge n$, the absolute relative tail is at most $r^{L/n}\le r$. For $t=L/(2n)\in[1/2,1]$ this yields

$$
Z_L(2\beta)\ge\left[\frac{Z_{2n}(2\beta)}{1+r^2}\right]^t(1-r).
$$

Absolute-spectrum Hölder interpolation, whose endpoint powers $n,2n$ are even, gives

$$
Z_L(\beta)\le Z_n(\beta)^{2-2t}Z_{2n}(\beta)^{2t-1}.
$$

Consequently

$$
T(L,\beta)\ge(1-r)S^{2-2t}D^t.
$$

The logarithm of the last two factors is affine in $t$. Their minimum over the entire interval is the minimum of the two endpoint values $S\sqrt D$ and $D$. This proves the lemma, including odd $L$ and signed transfer spectra.

All expressions used for the lower bound are monotone increasing in the supplied lower endpoints $S,T$. In particular, increasing $p$ increases $w$, decreases $r$, and increases $D$ and both candidate products. Downward rational input enclosures are therefore safe.

## 2. Two spatial directions

Use the canonical staircase

$$
A=\frac{Z(2n,m;\beta)}{Z(n,m;\beta)^2},\quad B=\frac{Z(2n,2m;\beta)}{Z(2n,m;\beta)^2},\quad C=T(2n,2m;\beta),
$$

with even $n,m\ge2$. In the formulas below the same letters may denote certified lower bounds. Assume $B>1/2$ and that both successive calls to $I$ have their required argument $S^2T>1/2$.

Define

$$
S_* = A^2\sqrt{2B-1},\quad T_* = I(B,C),\quad C_* = I(S_*,T_*).
$$

Then every integer rectangle $n\le L\le2n$, $m\le W\le2m$ satisfies $T(L,W;\beta)\ge C_*$.

To prove the spatial input, fix $x=2n$ and consider its transverse transfer at temperature $\beta$. Let $w_B=(1+\sqrt{2B-1})/2$ and $r_B=(1-w_B)/w_B$. The inverse-purity bound and positivity of odd physical traces again identify a positive unique dominant eigenvalue. For $s=W/m\in[1,2]$, its signed-tail estimate and absolute-spectrum norm monotonicity at fixed $x=n$ give

$$
S_x(n,W;\beta)\ge(Aw_B)^s\bigl(1-r_B^s\bigr)
=(Aw_B)^s-[A(1-w_B)]^s.
$$

For $0<d<c<1$, $c^s-d^s$ has at most one interior stationary point, which is a maximum. The sign of its derivative changes, if at all, from positive to negative because $(d/c)^s$ decreases strictly. The endpoint or constant cases follow directly. Here the two endpoint values are $A(2w_B-1)$ and $A^2(2w_B-1)$, so the minimum is the latter because $0<A\le1$. Thus $S_x(n,W;\beta)\ge S_*$.

The one-dimensional lemma applied in the transverse direction gives $T(2n,W;\beta)\ge I(B,C)=T_*$. Applying it in the longitudinal direction at this fixed integer $W$ proves the claimed two-dimensional bound.

## 3. Finite-window gap and completeness

If $C_*>1/2$, the largest Gibbs weight is at least $C_*$. Thus the finite-volume ground state is unique and

$$
e^{-\beta\Delta}\le\frac{1-C_*}{C_*},\qquad
\Delta\ge\frac1\beta\log\frac{C_*}{1-C_*}.
$$

The bound is valid on a finite integer rectangle of lengths at a fixed inverse temperature. It uses neither a limiting extrapolation nor a small-common-defect threshold. Several consecutive bootstrap states therefore provide overlapping finite windows before asymptotic acceptance.

## 4. Exact implementation and application

`finite_window_2d.py` uses 40-decimal downward square-root bounds verified by integer squares, exact rational arithmetic, and a separate 192-bit exponential enclosure with 70 Taylor terms and a geometric remainder. Floating logarithms propose gap endpoints only. The final assertion is the rational inequality $\exp(\beta\Delta)(1-C_*)<C_*$. The program explicitly rejects calls without the required inverse-purity margin.

For the ordinary bilayer at $g=0.03$, the new producer's initial inverse temperature $911/100$ supplies its first canonical state at $n=m=4$, $\beta=911/50$. Exact interpolation of its consecutive states gives the following lower bounds on the missing windows.

| Side interval | Gap lower bound |
| --- | --- |
| 4–8 | 0.037563294252 |
| 8–16 | 0.020705261190 |
| 16–32 | 0.012659323312 |
| 32–64 | 0.008963000173 |
| 64–128 | 0.007302383534 |
| 128–256 | 0.006491372977 |

Each exceeds the producer's asymptotic candidate 0.004333053946 for all $L\ge256$. The singlet-product trial and full-space Weyl lower bound give $\Delta_L\ge1-3gL^2\ge0.19$ for $L=2,3$, with the same periodic multiplicity convention. Therefore these scalar bridge calculations extend that candidate to every integer $L\ge2$, conditional on independent verification of its physical low-band and spectral-tail inputs.

Reproduce the calculation with

```sh
python research_20261010/root_review/finite_window_2d.py \
  research_20261010/low_band/refined_correlated_number_g003.json
```

The resulting JSON includes exact fractions for every square-root enclosure, intermediate purity, gap and source hash. These bridge checks are not a substitute for the independent physical-seed audit.
