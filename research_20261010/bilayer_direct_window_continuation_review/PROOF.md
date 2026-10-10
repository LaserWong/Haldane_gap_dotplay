# Independent acceptance of all 66 closed coupling intervals

Updated 2026-10-10 18:32 EDT / 22:32 UTC.

## Result and scope

For the ordinary periodic spin-one-half square bilayer, unit rung coupling and identical intralayer coupling g, every real g in [0,1/10] and every integer square side L>=2 has a unique finite-volume ground state and spectral gap at least

 4499695659/10^12 = .004499695659.

The positive-neighbor multiedge convention at side two is unchanged. There are no cross-layer inter-rung interactions. This is a stronger uniform bound on the same coupling interval, not a larger interval, a physical gap estimate, an arbitrary-aspect-ratio theorem or an infinite-volume uniqueness statement. No new physical trial vectors or many-body spectral calculations enter this improvement.

## Immutable physical input inheritance

All 66 source interval records match exact hashes in the already accepted independent review manifests. PROVENANCE.json records source name/hash, accepted review, accepted manifest hash and matching frozen-record path. Copies of those manifests and PASS statuses are retained in snapshot. Group counts are16,15,2,16,7,10 from ordinary_interval, interval_extension, interval_joint_extension, interval_range_0085, interval_range_009 and interval_range_010. They cover [0,.07], [.07,.078], [.078,.08], [.08,.085], [.085,.09] and [.09,.10], respectively.

Those reviews certify their trace-ratio lower endpoints, complete omitted-spectrum coverage, local small-size bounds and closed parameter ranges. The new work inherits those facts; it does not claim to have recomputed their physical proof. In particular each saved J1,J2,C0 is a simultaneous bound throughout its specified closed interval, not a point sample. The source records are not read from an unverified current floating scan.

## Initial state and scalar proof

For each source record at beta_initial, read its accepted raw time-first lower triple and canonical lower triple. Independently verify

 a<=G(J1), b<=G(J2*a), c<=G(C0^4*a^2*b),

where G(x)=1-(1-x)^2/(2x^2) on 0<x<=1. The triples are at common spatial base 8 and physical inverse temperature 2beta_initial. Any separately accepted initial joint lower bound is retained. Order conversion yields canonical bounds (a sqrt(b), a^2 b sqrt(c), a^4 b^2 c), all at that same common base. Maxima may combine valid bounds only when their physical edges agree.

Each full raw time-first cycle and each joint-aware canonical cycle uses the independently accepted rotating-ladder recurrence. All three coordinates double together. The exact state ledger is checked at every cycle, including every raw and canonical edge base/endpoint. Saved positive components and joint products are bounded by independently propagated lower endpoints. No thermal or spatial monotonicity of the physical gap is presumed.

At a given state, the direct time-first bound proved in bilayer_direct_window_review/PROOF.md is

 I_direct=a^4(2b sqrt(c)-1)sqrt(2b^2 sqrt(2c-1)-1),

with c>1/2, b sqrt(c)>1/2 and b^2 sqrt(2c-1)>1/2. It covers all integer rectangles in the corresponding doubled box, including both-odd side lengths. When a gate fails it supplies no bound.

The second separately valid option is the inherited canonical joint-aware window. Writing canonical components A,B,C and joint lower K, put

 sx=max(A^2 sqrt(2B-1), sqrt(K)sqrt(2B-1)/B),
 ty=I1(B,C;K), I_canonical=I1(sx,ty;0),

where I1(s,t;k)=(1-r)min(s sqrt(d),d), p=max(s^2 t,k)>1/2, w=(1+sqrt(2p-1))/2, r=(1-w)/w, d=t/(1+r^2). The quotient sqrt(2B-1)/B is monotone on [1/2,1]. This is the already accepted joint-ratio proof, including the two separate inverse-purity gates. Taking the maximum of the two valid thermal lower endpoints is safe. Each saved selected method and both saved candidate purities are checked independently.

For every selected finite window at its actual physical beta, the audit verifies the strict rational witness exp(beta*d_gap)(1-I)<I with I>1/2. This implies a unique finite-volume ground state and gap>=d_gap. The audit does not move a thermal window to a different beta.

At the terminal state, the accepted all-integer canonical theorem applies with 0<u<=1/500. Its sufficient witness exp(beta*d_gap)*32u<1 is checked independently. Its constants are reconfirmed exactly: 49/[2(1-7u0)^2]<32, 32u0<1, 20/(1-20u0)<32 and 5u0<=1/100 at u0=1/500. These ensure contraction and the inherited all-integer interpolation domain.

## Complete size and parameter coverage

Each interval retains its six accepted short-size gaps for L=2,...,7. Their labels, physical rung counts L^2 and edge-square sums 16,18,32,50,72,98 are checked. The minimum short gap is included with every required finite-window gap and the terminal asymptotic gap. A path with a missing window or mismatched next base is rejected. The 66 selected paths have 517 required finite windows in total.

The new per-interval gap equals that minimum and is no smaller than the source record's accepted gap. After checking each path, exact rational comparisons verify consecutive closed endpoints coincide, the first endpoint is 0 and the last 1/10. Taking the minimum of the 66 uniform interval bounds establishes the stated bound on every real g in the union. There is no inference from endpoint gaps or floating coupling monotonicity.

The limiting interval is [169/2000,339/4000]=[.0845,.08475], source interval_range_0085/lowband/interval_007.json. Its asymptotic onset is L=16384 at beta=35840. Its local endpoint information remains inherited from the accepted interval certificate.

## Independent arithmetic and validation

No producer code is executed or imported. independent_point_math.py is a byte-identical, hash-matched copy of the freshly accepted independent point audit. It supplies 544-bit rational directed exponentials and integer-square-root lower bounds. The continuation implementation independently reconstructs canonical interpolation and all state/path checks. Positive Taylor sums use 150 terms and an explicit geometric upper tail, with directed rounding at every multiplication; negative arguments use reciprocal bounds. Floating display values are never used to establish a gap.

Ten adversarial changes are rejected: altered parameter interval, temperature, common base, edge label, missing window, inflated direct purity, inflated canonical purity, wrong terminal size, oversized gap and altered short-size bound. A second clean-directory run matches all substantive results. Per-run caps are CPU 4, 600 CPU seconds and 700MiB address space. The audit takes about 11 seconds and 27MiB RSS. No physical many-body run, network call, producer mutation, root change or GitHub publication occurred.

The frozen continuation producer manifest is 13878cb1b8456ae34e33c1f5e1f2738755bfd1b65afdef7dd0913cb7de6ab961. The new lemma's independent point-review seal is 8e2726b4925b752fed9789dc43b3486229a626e4d7d07b45c1d6b5171d23f8c7. These are separate immutable reviews; no later data was inserted into the point review.
