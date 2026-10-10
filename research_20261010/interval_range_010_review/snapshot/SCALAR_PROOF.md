# Directed scalar and all-integer certificate

Updated 2026-10-10 17:56 America/New_York (EDT) / 21:56 UTC.
Status: exact producer certificate pending independent interval review.

Ten adjoining closed intervals cover [9/100,1/10]. On this extension every
integer square side L>=2 has a unique finite-volume ground state and gap at
least 2190412273/250000000000 = .008761649092. Joining the immutable and
independently reviewed [0,.09] package yields 66 closed intervals covering
[0,.10] with uniform bound 486442811/250000000000 = .001945771244.

For each interval the physical proof gives upper normalized denominator
traces U16(beta), U16(2beta), U32(2beta), including ground, odd bands, and full
omitted-state tails. Jensen gives the one-state numerator lower trace.
Affine energies are minimized at the same coupling endpoints:

J1: 8rho16-2rho64; J2: 16rho16-4rho64; C0: 4rho32-2rho64.

The initial directed lower ratios are respectively exp(beta E_J1)/U16(beta)^8,
exp(beta E_J2)/U16(2beta)^8, exp(beta E_C0)/U32(2beta)^2. Their physical trace
numerators are Z64(2beta), Z64(4beta), Z64(2beta). Constant shifts cancel.
All exponentials are rational outward enclosures. Floating calculations only
select witnesses and an initial beta on the finite grid [5,30] step 1/20.

The inherited reviewed joint scalar lemma transports the temperature-first
order txy to canonical xyt, retains the same-base joint full product, and
advances each route. Every state is explicitly labeled by its physical base
(n,n,beta), its canonical and permuted edge bases and endpoints, and its
joint-product physical base. These labels and all exact scalar values replay
without eigensolvers. Reordering paths never transports a joint product to
another base without the inherited valid recursion.

The saved 46 finite-window rows cover integer sides consecutively from L=8
through the small-defect bootstrap. Each row indicates whether it contributes
to the final minimum; the final row is redundant with the analytic tail.
All earlier necessary windows are included even when their bound is weaker
than the asymptotic estimate. The largest analytic-tail starting size is 256.
Sixty short-size checks separately cover L=2,...,7 for each coupling interval.
L=2 uses edge-square sum 16; L=3,...,7 use 2L^2. Positivity of the explicit
q1 reference minus the vacuum Rayleigh bound proves uniqueness and the gap
there. Endpoint evaluation uses the explicit reference's decreasing derivative
for g>=0, not monotonicity of the physical gap. Every accepted final gap is
the minimum of all needed windows, the analytic tail, and these short sizes.

A preliminary [.0999,.1] interval succeeds at beta=47/5 with gap .038032028638.
All ten width-.001 intervals succeed without subdivision at the requested
minimum .002. The adaptive bisection branch remains available for unsuccessful
proposal intervals. No finite search is interpreted as a method-wide failure.

replay.py recomputes all saved intervals from fixed vectors with eigensolvers
forbidden. It checks 30 numerator matrix endpoint/center evaluations, coupling
coverage, same-base labels, every finite window, short-size multiplicities,
retained counts and the unchanged predecessor seal. Eleven deliberate
corruptions are rejected, including complete residual, even-sector cutoff,
global ground margin, wrong joint base, coefficients, energies, trace bounds,
short multiedges, finite windows and retained counts. This producer replay
is distinct from independent review.
