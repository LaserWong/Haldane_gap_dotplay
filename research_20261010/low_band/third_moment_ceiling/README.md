# Existing two-vector numerator feasibility screen

Updated 2026-10-10 15:45 EDT / 19:45 UTC. No new physical state, moment or contraction is computed here.

The exact arithmetic part bounds how much the current span{ψ,(H'−ρ)ψ} can improve its Rayleigh minimum. The floating part is **only an optimistic resource-prioritization screen**, not a gap certificate or a method exclusion.

## Exact gain ceiling

Let v=||(H'−ρ)ψ||², r=(H'−ρ)ψ, and R=<r,H'r>/v. The existing exact q-sector residual masses and pair-creation norm bounds give

    R_low=(1−2g)<r,Qr>/v − cross_upper,
    R_high=(1+2g)<r,Qr>/v + cross_upper,

where `cross_upper` is twice the sum of the certified adjacent-sector square root bounds divided by v. Hence R_low≤R≤R_high. The lower direction follows from the independently reviewed number-preserving lower bound and subtraction of the absolute cross-term upper bounds. It does not assume the residual is an eigenvector or that its interaction expectation is positive.

In the orthonormal basis ψ,r/sqrt(v), H' compresses to

    [[ρ,sqrt(v)],[sqrt(v),R]].

Its smallest eigenvalue increases with R in the Loewner order. With
C=R_low−ρ>0, an upward-rounded root gives

    δ_upper=(sqrt_upper(C²+4v)−C)/2,
    inf_(φ in the two-vector span) Rayleigh(φ) ≥ ρ−δ_upper.

The script verifies `δ_upper*(C+δ_upper)≥v` exactly. This is a ceiling on the possible energy improvement in that fixed two-vector span, not a valid new Rayleigh upper endpoint.

## g=.09 outcome

For the largest 8×8 seed:

- R_low = 4.796306676711337…
- R_high = 7.197862436927804…
- Exactly known Q contribution = 5.997084556819571…
- Maximum possible two-vector gain upper = .005846548475871025…
- Current certified gain = .004001246683620774…

A β=7,…,14 step-.05 floating scan, allowing at most ten joint-aware cycles,
suggests R must be at most about 5.66090505 near β=8.9 for asymptotic scalar
acceptance. Thus an exact third moment would need to resolve a sufficiently
negative interaction contribution. Setting R to its Q contribution alone
would still fail this proposal criterion. Neither attainability nor finite
window success is asserted by this screen. All raw ratios are required to
remain≤1, avoiding the overtly inconsistent optimistic shifts from earlier
diagnostics.

The missing exact contraction and its projected resource cost are described separately in `../third_moment_plan/ASSESSMENT.md`. No such contraction has been started. `screen.py` reads only frozen .09 endpoint/filter data and uses one CPU with a 1 GiB virtual-memory cap.
