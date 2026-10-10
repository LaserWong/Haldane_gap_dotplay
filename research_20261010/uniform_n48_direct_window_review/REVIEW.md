# Independent acceptance: direct 48–96 window

## Accepted result and scope

For the uniform periodic spin-one Heisenberg Hamiltonian with unit bilinear coupling and the same energy normalization as the archived certificates, the spectral gap is at least 53/10000 for every integer 48 ≤ L ≤ 96. Combining the already accepted 19/5000 theorem for every integer L ≥ 52 gives gap at least 19/5000 for every integer L ≥ 48. The ground state is unique throughout these scopes. Bootstrap initialization remains 52. This finite-coverage result is consistent with the separate exclusion of the specified canonical n48/n50 startup recipes.

Acceptance retains the nine archived uniform I/P/C thermal-input interval certification assumptions, the analytic spatial/thermal transfer theorems, and the accepted exact physical MPS48/96 Rayleigh anchors. We have not rerun the archived thermal certifications. Exact contractions alone do not establish the gap. No provisional MPS50 datum, new physical contraction, adaptive startup claim, below48 claim, or minimum-size claim enters this result.

Producer manifest: 720a4243609cf64f451cd138f5297a110ad2b0d79db57994202e0ef300f3b65e. All dependency seals and every producer input digest are checked by independent_check.py; exact pins are in results.json and INPUT_SHA256.json.

## Coordinates and scalar construction

Write Z_L(β)=Tr exp(−β(H_L+aL)), a=700741/500000, S(L,β)=Z_2L(β)/Z_L(β)^2, and T(L,β)=Z_L(2β)/Z_L(β)^2. The direct pair is A=T(48,21/2), B=S(48,21). In particular the thermal input is length48, not the staggered length96 thermal coordinate used in canonical startup.

The accepted negative total shifted Rayleigh value R48 supplies v48 ≤ exp(−(21/2)R48), hence Z48(21) ≥ v48² without any uniqueness assumption. The length48 Hermite/packing moment envelope Q48 bounds Z48(21/2) from above. Thus A ≥ (v48/Q48)². The independent checker compares MPS48 exact norm/energy integers with the separately rebuilt benchmark48; it checks both norm positivity and total, rather than per-bond, Rayleigh conventions.

For B, the base length is26, cooling exponent2, q=48/26=24/13 and p=96/26=48/13. The character multiplicities are1,2,3. At the cooled temperature21, D ≥ z² and E ≥ e² bound total and scalar-sector sums respectively; τ=(D+11E)/12 and τ0=(D+3E)/4 give residual sector constraints inherited from the accepted generalized lemma. W ≤ exp(−21 R96) is a lower bound on the physical length96 trace, using the accepted negative shifted MPS96 Rayleigh value. These are all upper/lower bounds in the required directions.

For a certified leading mass t, the residual q-th or p-th power is bounded above by the convex maximum of x^j+2(y/2)^j+3((D−t−x−y)/3)^j over x,y≥0, x≤τ−t, x+y≤τ0−t. The checker enumerates intersections of active constraints independently. Convexity for j≥1 puts the maximum at vertices; fractional powers use integer-verified rational root brackets. The initial total-power contradiction and all 11 subsequent polygon contradictions are strict. The initial 2t>D establishes uniqueness in modulus and identifies the trivial sector as required by the inherited lemma. At each improvement t_new^p+R_p(t)<W, so the actual leading mass exceeds t_new. Then B ≥ [1+R_q(t)/t^q]^(−2).

The six length26/48 sector envelopes are rebuilt independently. Their Hermite polynomials obey Q(x)−x^k=(h−x)(x−t)²P(x), where P has explicitly checked positive rational coefficients and k=L/2−3. This proves the bound over the full closed support including zero. Positive coefficients select upper moment endpoints, negative coefficients select lower endpoints. The minimum with unit-count packing is a valid upper bound. No independent sector corner is asserted to be a jointly realizable physical spectrum.

The resulting exact conservative bounds are

- A ≥ 782159275175083593289269 / 10^24;
- B ≥ 213232331787153576811891 / (25·10^22);
- C ≥ 256991805584988123566957 / (5·10^23) > 1/2.

## Signed all-integer direct window

Here is the analytical bridge, separately from its numerical inputs. For even n, suppose T(n,β)≥a and S(n,2β)≥b>1/2. Set Y=X_(2β). The normalized weights |μ_i|^n/Z_n(2β) have purity S(n,2β). Their unique largest weight is at least w=(1+sqrt(2b−1))/2>1/2: the purity is at most u²+(1−u)² for largest weight u≥1/2.

The official spatial transfer proposition identifies the untwisted physical trace with Tr X_β^L for every integer L≥4. This is the pinned transfer.tex blob 41e01eee2b9103fd61201931005bd1b079b51cf1, audited in uniform_source_scope_review. It has no staggered odd-cycle twist. Positivity of physical odd traces therefore forces the unique largest-modulus eigenvalue of Y to be positive. Compactness and a finite even moment make the normalized subleading signed tail vanish at sufficiently large odd powers. Positivity without this physical identity would not suffice. We use the source floor4 only; the producer's looser n≥2 wording is unnecessary here.

For p=L/n∈[1,2], the signed numerator obeys
Z_L(2β) ≥ Z_n(2β)^p [w^p−(1−w)^p].
For odd L this follows by bounding the absolute tail power by its total mass to power p; for even L one has the stronger lower bound Z_n(2β)^p w^p. The denominator obeys Z_L(β)≤Z_n(β)^p by the absolute spectral ℓ^p inequality and positivity of the physical trace.

Consequently T(L,β)≥a^p[w^p−(1−w)^p]. For w∈[1/2,1] and 1≤p≤2, the difference w^p−(1−w)^p−(2w−1) is concave in w and vanishes at both endpoints; it is nonnegative. Also a^p≥a². Thus T(L,β)≥a²sqrt(2b−1)=C uniformly for all integer n≤L≤2n. The even-length conclusion also follows without a leading-sign argument from w^p≥w²≥2w−1.

For Gibbs probabilities, purity at least C>1/2 forces a largest probability at least C, hence a unique ground state. The ratio of the next probability to the ground probability is at most (1−C)/C. Therefore exp(βg)(1−C)<C proves gap>g. At β=21/2 and g=53/10000 the independently directed margin is greater than 0.00015367603836256. This establishes the finite window including odd lengths49,51,…,95.

## Composition and verification

The accepted n52 theorem is gap≥19/5000 with unique ground for all integer L≥52. Its overlap with the present finite window is52–96 and 53/10000>19/5000. Their union is every integer L≥48. No extrapolation of the finite window beyond96 is used.

The independent standard-library checker uses rational arithmetic, 40-digit root brackets checked by integer powering, and an 80-term directed exponential with an analytic remainder. It verifies all source/dependency seals, moment identities, anchor signs, polygon constraints, leading forcing steps, final purity, exponential margin, and composition. CPU5 runtime was about0.25CPU seconds, RSS below17MiB under a100MiB hard limit. No heavy contractions were started. Nine adversarial checks reject coordinate relabeling, wrong temperature, the purity boundary, upward purity rounding and unsupported window endpoints; they also exhibit why even moments alone cannot determine the odd leading sign. These tests complement, rather than replace, the analytical argument.
