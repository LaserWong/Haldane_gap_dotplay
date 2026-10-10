# Next steps: fix the scalar seed before buying more trace accuracy

## Exact bottleneck in the present startup

The seed needs simultaneous lower bounds on
S(n,beta)=Z_(2n)(beta)/Z_n(beta)^2 and
T(2n,beta)=Z_(2n)(2beta)/Z_(2n)(beta)^2
inside a proved bootstrap basin, for example both >=7/8.

The archived order-10 route first tries to force a large atom in the D2-trivial
spatial list J. Put m_N=sum(lambda in one nontrivial D2 list N) lambda^10 and
v_N>=max|lambda| on that list. Its nontrivial contribution majorant is

 B_N(L)=3 M(m_N,v_N^10,L/10),
 M(m,h,r)=floor(m/h)h^r+(m-floor(m/h)h)^r.

The proposed atom-exclusion bound, including a J contribution, must be <1 to
contradict the MPS lower bound Z_L>1. Thus **B_N(L)<1 is a necessary intermediate
condition for this particular sufficient proof**. It is not a necessary
condition for the physical chain to be gapped.

At beta8 and the archived D124-certified shift a=4.76121, the optimistic
uncertified order-10 data give v_N≈1.085112 and m_N/v_N^10≈1.724225. Therefore
B_N(128)≈105875.8, before the J part or any choice of atom threshold is added.
A separate thermal obstruction within the same estimate is its J cap≈1.111114:
with numerator lower bound only 1, even zero remainder would require
c_J<=(8/7)^(1/(2L)), about 1.000522 at L=128, to certify T(L)>=7/8.

## What is rigorous, and what is only screening?

- Rigorous algebra: if v_N>1 and m_N>=v_N^10, then this majorant satisfies
  B_N(L)>=3v_N^L>3 for every even L>=10. No atom-threshold grid can rescue that bound.
- Exploratory input evidence: all eight cached beta values 6 through 32 satisfy
  those two inequalities after rescaling to a=4.76121. The 64 checked
  shift/beta/length combinations fail. The L9/L10 moments and numerical support
  caps are not certified, so this is not a rigorous obstruction for the true
  moment sequence or for other filters.
- The earlier beta=9/4 thermal-purity upper-bound obstruction is a different
  archived certificate. It must not be extrapolated to colder beta values.

## Least-cost ways to tighten the missing quantities

1. **Scalar-only joint moment screening first.** Use the copied candidate
   moments to optimize a stronger bound on B_N(L), retaining signed odd moments,
   atom multiplicity and multiple-atom/Hankel PSD constraints rather than
   compressing each list to one cap plus one mass. Tiny matrices and scalar
   optimization are cheap. Require an actual winning candidate and perturb its
   moments by prospective trace errors before requesting more physical inputs.
2. **Bound the ratio actually needed.** Explore joint beta/2beta constraints on
   T(L,beta), using the archived exact purity identities and any available
   denominator bounds. Merely lowering the J cap or improving the MPS energy
   is insufficient. Reject a proposed temperature cheaply if a certified
   thermal-purity upper bound already misses the bootstrap basin.
3. **Check what the existing MPS tensor can cheaply certify.** Its total-trace
   lower bound does not automatically locate a J atom. Audit whether the saved
   exact covariance identities permit useful twist-resolved trial-energy/trace
   bounds or a stronger numerator. This is a proposed small contraction task,
   not an existing certificate or permission to infer a spatial-sector atom.
4. **Only then select expensive inputs.** A successful scalar candidate must
   state beta, beta/2beta needs, moment orders, twists and rational error budget.
   The old D2 order-10 route needs I/P; C is needed only for a genuinely useful
   finer decomposition. Improve precision or add higher moments only when a
   sensitivity calculation shows that the resulting inequalities can pass.

No further long computation is proposed now. L10 I/P with only M=0,...,4 still
projects to 293–316 core-hours, before setup/I/O. A finite-input run that does
not close a mathematically viable critical path is not justified by a faster
kernel alone.
