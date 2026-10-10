# Direct time-first windows: a relaxed-path necessary screen

## Result and scope

For every separately checked even denominator size n=6,8,...,24, the fixed
archived D26 single-Rayleigh numerator at2n cannot close the specified
G-based scalar route at any beta>=0, even if every short and intermediate
integer-size bridge is granted for free. This is a new scalar-only statement
about the route with improved windows, separate from the earlier frozen
canonical-window exclusions. No seed-size monotonicity is used.

For n24 both70- and73-state lower traces from the pi-current extension give
this result. The test takes0.25CPU seconds and performs no physical
contraction. Physical input review and new-lemma review remain separate.
The result bounds attainable certificate endpoints, not true physical
purities; a nonpositive endpoint blocks this certifier, not a physical
continuation. It is not a physical-gap or universal minimum-size statement.

The covered routes use the existing time-first G startup, any fixed number
of whole time-first cycles, then the accepted joint-aware canonical route
or the inherited same-base small-defect closure. No arbitrary adaptive
mid-cycle switching, different recursion, stronger initialization or new
asymptotic closure is covered.

## Physical indexing and the candidate window

Let the initial denominator size be n and initial inverse temperature beta0.
The existing G startup returns a lower endpoint a for T(2n,2beta0) and b for
S(2n,4beta0). Its actual time-first base is therefore(2n,2beta0). After k
additional full cycles the base is(2^(k+1)n,2^(k+1)beta0).

At a general actual base(N,B), with a<=T(N,B), b<=S(N,2B), the proposed
and independently analytically checked direct signed-transfer window gives

    T(M,B)>=a^2 sqrt(2b-1), N<=M<=2N,

under the stated self-adjoint history-transfer assumptions, N even,
0<a<=1 and1/2<b<=1. To certify a positive finite-window gap, its lower
endpoint must be strictly greater than1/2. Every preceding window must pass
at its own actual B; beta and spatial size must never be relabeled.

The bounded floating diagnostic finds that the optimistic n24 first-window
quantity reaches about0.629535 near beta0=10.825. This is only a necessary
upper-envelope diagnostic: it does not certify any physical window or gap.
It shows why failing the older interpolation is not sufficient to reject
the new window route.

## Relaxation that avoids rejecting a stronger bridge

For the exact screen, assume all finite windows pass, including every short
size before startup, every direct window, and every potentially stronger
length-resolved or old/new maximum window. This enlarges the set of possible
certificate paths. Hence a failure after this relaxation cannot be repaired
solely by improving those window lemmas.

Let Jbar,Cbar be certified upper bounds on the attainable startup lower
endpoints, derived from the fixed numerator and trial lower denominator
traces. Since G(x)=1-(1-x)^2/(2x^2) is increasing on(0,1], upward arithmetic
propagates the optimistic endpoints

    abar=G(Jbar), bbar=G(Cbar^2 abar).

Nonpositive outputs exclude the route immediately. At each positive pair,
let Pbar=abar^2 bbar. Same-base transport gives canonical S>=sqrt(P),T>=P.
Its common defect is u=1-P because0<P<=sqrt(P)<=1. Therefore the accepted
u<=1/100 closure requires P>=99/100. If Pbar<99/100, that closure is impossible
with any weaker certified endpoints.

At every possible whole-cycle delay, also test the already accepted
joint-aware canonical continuation, with initial S=abar sqrt(bbar),
T=K=abar^2 bbar, then

    S'=G(max(S^2 T,K)), T'=G(max(T,K)^2 S'),

and discard K after that first cycle. Every such optimistic canonical route
fails a nonpositive update before entering the accepted target region.
Continue the time-first path itself by

    abar'=G(abar^2 bbar), bbar'=G(bbar^2 abar').

In every covered beta box it also becomes nonpositive after finitely many
steps. Thus there are only finitely many possible delays, and each has been
excluded. The32-step implementation cap never establishes failure: if
reached it would explicitly return inconclusive. No cap is reached here.

The direct-window upper square abar^4(2bbar-1) is recorded diagnostically.
It is never used to exclude a box: a stronger integer-resolved bridge could
succeed where the uniform direct bound fails. Granting all bridges avoids
that issue entirely.

## Exact inherited beta coverage

The verifier uses frozen exact J/C upper envelopes over closed beta boxes,
not point samples or regenerated floating estimates. It checks contiguous
box endpoints and matching hot/cold tails.

- n6 and8: the archived global J cap and late C cap cover beta>=1/2;
  the hot interval[0,1/2] fails the first G.
- n10 and12: inherited all-beta J caps already fail the first G.
- n14,16,18,20,22: the sealed three-state envelopes and exact hot/cold tails.
- n24: separate70/73-state pi-current envelopes,318 closed boxes[1/2,80]
  with exact hot and cold tails.

All rational upper bounds and complete replay histories are in
exact_results.json, along with dependency hashes. Directed exponentials are
inherited from those exact input certificates; this replay uses their saved
rational endpoints and160-bit upward arithmetic. Its claims depend on those
physical/scalar input certificates being valid.

For n24, every positive optimistic history has P<674059/1000000, and no
path reaches a positive whole-cycle base beyond96. The recorded actual beta
multiplier is4 at base96, not an unchanged temperature. A subsequent
nonpositive bound excludes later whole-cycle delays of this certifier.

## Reproduction

In a fresh copy preserving the research directory layout, run

    taskset -c 2 python3 bounded_scan.py
    taskset -c 2 python3 verify_relaxed_paths.py

The first file is deliberately labeled floating diagnostic. Only the second
produces the exact relaxed-path result. Both write local outputs, so do not
run them inside a frozen tree. Dependencies and their hashes are explicit.
