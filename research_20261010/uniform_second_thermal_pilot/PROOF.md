# Independent beta49/4 thermal pilot (producer, review pending)

2026-10-10 23:24 UTC. No full thermal campaign authorized or run.

## Model and exact arithmetic
Periodic uniform spin1 Heisenberg, coupling1, physical dimension3^n, shift a=700741/500000. I is no seam; P is a pi rotation about z on the closing bond. There is no C input. Every integer4<=n<=12 is allowed, including odd n. In a fixed magnetization block D=32I-3nI-2H has diagonal32-3n-2 sum w[i-1]w[i] and off-diagonal-2, changed to+2 on the P seam. The positive operator 3n/2+H lies in[0,5n/2], so R=D/32 has spectrum in[-7/8,1] and norm<=1.

F=exp(98(R-I)); Z=exp[(49/4)n(3/2-a)] ||F||_F^2. Rational conditioned Poisson coefficients p_j proportional98^j/j!, j0..280; Q=2^55 and c_j=floor(Qp_j). Exact integer generation checks last nonzero c is191. Truncation and renormalization error<2^-84<1/Q. Each Horner step X=floor(DX/32)+c_j e_r uses mathematical floor for negative integers. The implementation omits only initial zero integer steps, but the error proof charges281 steps.

For block dimension d, each ideal suffix has norm<=Q, and accumulated rounding error<=281(sqrt(d)+1). Using d_n=floor(sqrt(3^n))+1 and E_n=281(d_n+1)+1 gives ||X-QF e_r||<=E_n. d_n<=730; thus every coordinate<2Q. Absolute row sum<=|32-3n|+6n<=76. Every signed multiplication and partial sum is bounded by76*2Q=5476377146882523136<2^63-1; division/addition bounded by76*2Q/32+Q<2^63-1. This is an induction using contraction error after each exact operation. Squares use signed128, sums of64 squares use unsigned128 (<64*(2Q)^2=2^118), then GMP for unrestricted accumulation. No growing rational denominator occurs in vectors.

Stale inherited comments mentioning173 or Eisenstein arithmetic are NOT this proof. C is rejected. The bound implemented for component size is2Q. A future source version should clean the comments and rebind hashes.

## Orbits and odd lengths
The final kernel computes M>=0. For M>0, representatives are lexicographic minima of dihedral word orbits with weight twice orbit size. For M=0, digit negation is included and there is no extra factor. Signed translations restore the pi seam; reversal and global negation are exact symmetries of physical column norms. No bipartite/even-length gauge is assumed. check_symmetries.py independently checks all sparse entries, signed translation, reflection, negation, and exhaustive code/multiplicity coverage for n4,5,6, both seams. All pass. Their orbit multiplicities sum to3^n.

Rounded columns need not obey signed covariance. Repeat each exact/computed representative column by its physical multiplicity; the exact repeated Frobenius norm equals the full heat Frobenius norm. Triangle inequality gives |sqrt(W)-Q||F||_F|<=d_n E_n. Apply rational Taylor degree100 enclosure for exp(x), x<15, and integer square root to obtain each thermal interval. All four full small cases match published W exactly and satisfy center+/-30e-6.

The first attempted negative-magnetization convention is retained under initial_negative_convention. Its P6 total differs from the published convention because representative choices may involve signed shifts and floor is not sign-equivariant. This is an expected convention dependence, NOT agreement evidence. Only final nonnegative-M results are advertised as published-total matches.

## Checkpoints and gate
The pilot completed fresh in this directory. Each JSON records case, start/count, exact code/multiplicity/norm records, source and coefficient hashes, CPU/RSS. However run_pilot.py's resume path trusts existing JSON and is NOT APPROVED as a campaign runner. Before any long campaign, a NEW runner must validate source/binary/coefficient hashes, complete expected orbit identities/multiplicities, case and batch parameters, record counts, duplicate/holes, nonnegative exact integers and atomic output integrity. A partial L12 batch is not a trace certificate. No full campaign is launched here.

## Provenance/license
stream_second.cpp adapts the already locally reviewed heat_trace/stream_horner.cpp; check_symmetries.py adapts heat_trace/validate_symmetries.py. Matrix/coefficient/error specification was inspected in official thermal72.tex, Git blob b9f3c87a4fcfa96a82cdb5d4daf30b6088428037. No upstream Python was executed. Official sectors.jsonl is retained solely for planning, Git blob99ab264a4e8156fad86a6693055e31ed98451aa8. It is external measured evidence, not a local rerun. Upstream openai/math Apache2.0 license is retained as LICENSE.upstream. Its content and manuscript snapshots appear in the sibling scalar package. SHA256 bindings are in INPUT_SHA256.json.
