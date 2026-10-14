# Exact coupling evaluation without new physical support

Updated 2026-10-10 15:19 EDT / 19:19 UTC. This is a new g=.09 candidate package, pending independent physical replay.

## Translated trial family and normalization

Fix a geometry and its rational orthogonal rung basis once and for all. Its positive diagonal physical metric is independent of g. Write the shifted ordinary-bilayer Hamiltonian as

    H'(g)=Q+gV.

The existing literal one-triplet trial family is

    w_r(g) = (I−C_create(g)/2)|t+_r>,

where C_create(g) is the part of gV raising triplet number by two. In particular
C_create(g)=g C_create(1), so w_r(g) is affine in g. Translation operators and
the physical inner product do not depend on g. Therefore the displacement
moments, as identities for this explicit family, have degrees

    <w_0(g),w_r(g)>                  degree ≤2,
    <w_0(g),H'(g)w_r(g)>             degree ≤3,
    <H'(g)w_0(g),H'(g)w_r(g)>        degree ≤4.

This degree statement follows from the operator/vector definitions, not from observing a fit at finitely many values.

The earlier integer producer uses, for g=p/q in lowest terms,

    d=4q,  T=d H'(g),  W_r=2d w_r(g).

Consequently its stored displacement arrays obey exactly

    G_stored = 4d² G_physical,
    A_stored = 4d³ A_physical,
    B_stored = 4d⁴ B_physical.

The metric, including its geometry-dependent common factor, is unchanged across couplings. Each audited source is first divided by its own indicated factor before interpolation. This explicitly removes the coupling-dependent integer denominator. Interpolating the unnormalized integer arrays would be incorrect.

## Reconstruction and checks

`build_inputs.py` uses exact rational Lagrange evaluation, separately for every displacement and each of G,A,B. It uses degree+1 distinct audited couplings to determine the polynomial, then verifies every remaining audited coupling exactly. The available points are .03,.04,.05,.06,.07,.08,.10. Thus G has four, A three, and B two extra checkpoints per displacement. Across the three geometries there are 1,008 extra-point exact equalities. These checks support the implementation. The explicit degree proof above supplies the identity.

At g=.09, d=400. Evaluation is multiplied by the appropriate 4d^power factor, and every resulting entry is checked to be an integer before the existing exact Q(sqrt(2)) Fourier certificate is applied. No new W, HW, H²W, or leaked physical support is constructed. The trial family is g-dependent exactly as written above. It is not replaced by a fixed-coefficient vector from a nearby coupling.

## Ground and full-space inputs

The g-independent ground basis consists of vacuum/pair orbit vectors B and the
q=4 vectors L=A42 B. Existing audited geometric contractions F,S,V,W give its
entire G/K/J at .09, retaining complete q≤6 leakage in J. Only an 11×11 or
29×29 dense coefficient proposal is solved and rounded. The rational vector
is then evaluated exactly. No high-q physical support is materialized.

The independently reviewed quadratic-boson comparison supplies complete ordered bins with its oscillator multiplicities. All three ground trials satisfy rho<a 1, and the complete translated triplet band lies below a 2. Thus the established spectral-completeness argument applies before the full ground inverse-moment pencil is used. The separate reviewed variational filter gives an improved even-trial Rayleigh upper bound using original G/K/J and geometry. No residual for the filtered vector is asserted.

All of these are exact checks in the generating calculation at a new coupling. Their saved values still require independent point-specific replay before a new physical claim is promoted. The scalar searches here produce no successful .09 certificate.
