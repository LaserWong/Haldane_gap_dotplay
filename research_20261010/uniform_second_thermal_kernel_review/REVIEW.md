# Independent second-temperature thermal kernel gate

## Verdict

ACCEPTED: the frozen real I/P column kernel for integer lengths4 through12, its exact arithmetic/error analysis and tiny odd/even fixtures. NOT ACCEPTED as a campaign runner: run_pilot.py trusts existing checkpoint files. A new strict resumable orchestration layer needs separate review before a full campaign. No full18-case validation or physical gap theorem is certified by this kernel gate.

Frozen producer manifest0b5ffdc303cd506a2946308c3ce33e7327e38eac6dae9a92413937fe735f0185. Source SHA2565d496b80611e7c68f0ebbf027d686ecff1192a5b77864e2b931ebf2850051d51. The independently rebuilt binary is recorded in kernel_comparison.json. The producer manifest was fully verified before copying/compiling. Only one explicitly authorized producer-kernel invocation was made, on L5/P/M0. No imported Python code was executed.

## Model and arithmetic

The basis words have spin weights−1,0,1. The sparse matrix is D=32I−3nI−2H. Its diagonal32−3n−2Σw_iw_(i+1), ordinary hopping−2, and P-seam hopping+2 agree with the physical spin-one Hamiltonian and official thermal72.tex, Git blob b9f3c87a4fcfa96a82cdb5d4daf30b6088428037. I denotes the untwisted physical chain; P is a π-rotated closing bond. There is no staggered transformation or odd-cycle assumption.

The inherited energy enclosure0≤3n/2+H≤5n/2 makes R=D/32 a contraction for4≤n≤12. Thus F=exp[98(R−I)] is the half-temperature shifted heat operator atβ49/4. The full thermal trace is exp[(49/4)n(3/2−a)]||F||_F², a=700741/500000.

The exact rational Poisson weights proportional98^j/j!, j0..280, are floored after scaling by Q=2^55. Their last nonzero integer coefficient is191. Removing only the initial zero integer steps preserves the exact integer output. Truncation plus renormalization contributes operator error less than2^-84<1/Q. The error estimate still charges281 steps, not192.

At every Horner suffix, the ideal vector has norm≤Q. Coordinate floor error per step has Euclidean norm<sqrt(d); coefficient error<1. Hence the computed vector differs by at most281(sqrt(d)+1). Including exponential approximation gives E_n=281(d_n+1)+1 with d_n=floor(sqrt(3^n))+1≤730. Every coordinate is bounded by Q+281(730+1)<2Q. The sparse absolute row sum is at most |32−3n|+6n≤76. Therefore every product and partial sum is strictly bounded by76·2Q=5476377146882523136<2^63−1. Post-division addition is also safe. This is an inductive proof: exactness of the next operation follows from the current bound, then the norm error proves the next bound.

floor32 implements mathematical floor for negative values; its negation/add31 cannot overflow on the preceding bound. Signed128 products of real coordinates satisfy0≤u²<(2Q)². Chunks of64 squares sum below2^118<2^128, and GMP accumulates all chunks and externally weighted norms without fixed-width overflow. C is rejected before entry into retained unreachable complex branches. Stale inherited comments mentioning173 steps/Eisenstein coordinates are superseded by this real281-step proof; they are not relied upon.

## Orbits and Frobenius interpretation

The kernel uses nonnegative total magnetization only. For positive M it enumerates dihedral word orbits and assigns twice their set cardinality, accounting for−M. At M=0 it adds global digit negation to the orbit and uses its cardinality once. Lexicographic minima and set cardinalities correctly handle stabilizers. Total multiplicity is3^n.

Reversal preserves the closing seam. Global spin negation preserves the real Hamiltonian. A cyclic shift of a P chain moves the seam but a diagonal π gauge on the intervening arc restores it. The resulting signed permutation commutes with H, including odd n. Our fresh L4/L5 matrix checks explicitly verify these identities on every entry. Consequently exact exponential columns have equal norms along these orbits.

Rounding need not commute with a signed permutation. The proof does not assume that it does: repeat the selected exact/computed representative columns by their physical multiplicities, then apply the triangle inequality to these abstract direct sums. It gives |sqrt(W)−Q||F||_F|≤sqrt(3^n)E_n<d_nE_n. Integer square roots and a degree100 positive Taylor sum plus its bounded remainder give rational enclosing thermal intervals. This explains why the producer's retained exploratory negative-M representative convention can yield different rounded totals without invalidating the physical error bound; it is excluded from the printed-total matching claim.

## Independent fixtures and resources

independent_fixtures.py builds matrices from physical bond rules in fresh standard-library Python. It independently constructs orbit closures and computes every representative column for full L4/L5, both seams. All four totals exactly equal the official printed W values. All26 available L4 pilot records match individually. OddL5 totals are9095379218684502088743241789 (I) and9205948219074287936685289758037 (P). Symmetry, signed rotation, reversal, multiplicity and negative-floor tests pass. Runtime about0.35CPU seconds.

kernel_compare.py verifies the full frozen producer manifest, copies its reviewed source and coefficients into this directory, rebuilds under hard256MiB/120CPU-second limits onCPU5, and makes the sole authorized kernel invocation L5/P/M0. All6 records match the independent fixtures. Compile plus run used about2.33CPU seconds and peak144164KiB. Exact hashes are in kernel_comparison.json. No large trace contraction was launched.

## Campaign orchestration requirements

An acceptable new runner must bind the frozen source, executable, coefficient list and algorithm/representative convention. On resume it must validate case, twist, magnetization, batch range, source/binary/coefficient hashes, exact expected code/multiplicity sequence, nonnegative arbitrary-size norms, counts and absence of duplicates/holes. A complete-case aggregator must cover every nonnegative-M representative exactly once, check total multiplicity3^n, and reject partial traces. Writes should be atomic; unvalidated existing files must never become acceptance evidence. Requested integer ranges must be bounded to avoid start+count overflow. A checksum alone authenticates stored content, not computation, so proof relies on the authorized audited kernel and input binding. The pilot wrapper fails these requirements and is expressly excluded.
