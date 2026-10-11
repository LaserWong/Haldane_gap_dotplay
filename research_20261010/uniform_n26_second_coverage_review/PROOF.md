# Independent parity-resolved prefix review

2026-10-11 02:32UTC /2026-10-10 22:32 America/New_York.

## Verdict

ACCEPTED: the untwisted periodic uniform spin-one Heisenberg Hamiltonian with unit bilinear exchange has a unique ground state and gap≥23/10000=.0023 for every integer L≥26. The new work certifies exactly L26 and27 at beta49/4. It joins the independently accepted .0179 tail from28. Bootstrap initialization remains30; no26-site initialization or minimum-size theorem is claimed.

The nested stronger bounds remain .0179 forL≥28, .0245 forL≥32 and .0248 forL≥34. Producer manifestc723bca65e315ad2c2d296a9b0cc6cf51dc67240749bd06ee812b49ec8a9e609 and all inherited review seals pass. No new physical contraction or thermal computation is performed in this package.

## Physical anchor and canonical inputs

The52-site D26 anchor was freshly rebuilt from physical tensors and independently contracted by the sequential GMP engine in uniform_n28_second_initialization_review, manifest e22c642a814744fed23e45e799b58be4d31da7c4e1b341e2d4c39b95bb474ead. Its separate anchor52.out matches every producer integer. Positive norm and H0_52/N0_52+52a<0 are checked exactly, where H0 is TOTAL energy and a=700741/500000. This supplies Z52(b)>1 for every b>0 without a uniqueness premise. Bond dimension26 is not physical Hilbert dimension3^52 or a thermal-rank cutoff.

All18 beta49/4 physical thermal intervals retain acceptance792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94. Their signed J,N moments and support caps are unchanged. The N26 global signed polynomial upper bound was independently proved in core review54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f. The checker matches that exact coefficient-derived bound and retains multiplicity3.

Packing twelfth absolute masses with exponent52/12, together with the negative physical anchor, forces a positive unique dominant J atom above ell=.9999543523. Its negative-support and N-cap exclusions, residual mass and exact forcing margin are checked. Fractional residual exponent26/12 gives conservative spatial S(26,beta0)≥.848048256921175, while the full52 trace upper bound gives thermal T(52,beta0)≥.8662555116602277. These decimal displays are not proof inputs; exact rational endpoints are reconstructed with140-digit outward power bounds. The two seed coordinates are not relabeled as an unstaggered pair.

## Independent derivation of the length/parity refinement

Let n be even and let S≤Z_(2n)(beta)/Z_n(beta)^2, T≤Z_(2n)(2beta)/Z_(2n)(beta)^2. The exact exchange identity and physical thermal purity T(n,beta)≤1 imply spatial purity S(n,2beta)≥K=S²T. Here K>1/2. The normalized absolute n-th powers of the real doubled-temperature transfer eigenvalues form a probability distribution. Its purity≥K forces a unique largest weight at least

    w=(1+sqrt(2K−1))/2, rho=(1−w)/w<1.

The unique largest-modulus transfer eigenvalue mu0 is positive: otherwise its odd powers dominate all sufficiently large odd traces with a negative sign, contradicting positive physical partition functions. The official all-integer physical trace identity is valid for L≥4. The older abstract lemma's stated range≥2 is not needed here.

The relative n-th absolute tail is at most rho. For p=L/n≥1, convex mass concentration bounds its relative L-th absolute tail by rho^p. At2n its tail is at most rho², so

    mu0^(2n) ≥ Z_(2n)(2beta)/(1+rho²).

For EVEN integer L, the numerator Z_L(2beta) is at least mu0^L because every subleading L-th power is nonnegative. For ODD L it is at least mu0^L(1−rho^p). No positivity of individual subleading transfer eigenvalues is assumed.

For n≤L≤2n, absolute-spectrum Hölder gives

    Z_L(beta) ≤ Z_n(beta)^(2−p) Z_(2n)(beta)^(p−1).

For odd L the first comparison is Z_L≤sum|lambda|^L; positivity of the physical trace permits division and squaring. Endpoint powers n and2n are even, so their absolute and physical traces agree. Substitution into Z_L(2beta)/Z_L(beta)^2 yields, with D=T/(1+rho²),

    T(L,beta) ≥ S^(2−p) D^(p/2)                  for even L,
    T(L,beta) ≥ S^(2−p) D^(p/2)(1−rho^p)        for odd L.

All factors are nonnegative and monotone in their supplied lower endpoints S,T: increasing K decreases rho and increases D. Thus conservative input rounding is safe. This formula keeps the actual p and parity, rather than minimizing over an unnecessary whole interval.

## Exact checks and composition

At26, p=1 and no tail penalty is needed. At27, p=27/26 and the factor1−rho^(27/26) is essential. The checker obtains exact certified lower purities whose displays are .747990627911218 and .5070738839110758. Positive powers of S,D are bounded downward; rho^p is bounded upward before subtraction. Every root bound is verified by integer powers. The exact check at each length is

    C−exp[(49/4)(23/10000)](1−C)>0.

The tight27-site margin exceeds.000062074. Purity>1/2 proves the ground state is unique, and the exponential ratio inequality proves the stated gap. The finite set{26,27} joined to all integers≥28 has no missing lengths. The .0179 tail may be weakened to.0023 without changing its scope. This argument makes no assumption about monotonicity of physical gaps in L.

## Preserved failure and limits

The original simplified constant over all26..52 is approximately.495981255822436<1/2. Its exact100-digit computation is independently reproduced. It therefore fails to certify that entire window by that one constant; it does not bound actual physical purity from above and does not rule out individual lengths. The positive prefix result is consistent with that failure. No universal temperature, recipe, initialization or physical-gap obstruction follows.

Six adversarial tests reject dropping the odd tail factor, assigning even parity to27, confusing coverage26 with initialization26, treating a failed lower bound as a no-gap result, substituting a per-bond anchor, and omitting length27. The standard-library scalar replay consumes.163CPU seconds and14.8MiB onCPU4 under60CPU seconds/256MiB. Producer code is read, never imported or executed. Input digests and exact margins are archived. All prior seals remain unchanged.
