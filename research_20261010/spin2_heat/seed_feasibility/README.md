# Should complete L9/L10 traces be funded for the current spin-2 route?

**The recommendation is not to launch a full campaign for the archived startup route yet.**
The faster finite-trace algorithm is useful infrastructure, but a scalar
acceptance path is missing even when the current unverified high-order moments
are optimistically treated as exact. This is a method-specific, exploratory
screen. It is not a proof that another filter cannot work, or that the chain
is gapless. No Hamiltonian diagonalization was performed here.

## Original target and available evidence

The archived route uses H_L=sum S_j.S_(j+1), spin 2, unit coupling and periodic
seam twists I/P/C. Its spatial and thermal purities are
S(n,beta)=Z_(2n)(beta)/Z_n(beta)^2 and
T(N,beta)=Z_N(2beta)/Z_N(beta)^2.
A convenient sufficient startup is S(n,beta),T(2n,beta)>=7/8. The original
0.99 condition is stronger. The improved asymmetric scalar basin still needs
thermal purity near 0.8 even with almost perfect spatial purity. Spatial
purity by itself does not imply a physical gap.

The current complete archived finite inputs stop at order 8. Their spectral
validation has documented arithmetic assumptions. L9 and L10 I/P moments in
`exploratory_moment_inputs.json` come from incomplete Ritz lists. They are not
trace certificates, and their errors are not enclosed. No L10 C Ritz input is
included in that original order-10 screen.

The later D124 MPS certificate claims E0(N)<-4.76121 N for
N=128,256,512,1024, yielding Z_N(beta;a=4.76121)>1. Its archived exact tensor
and Arb contraction workflow is distinct from this scalar screen. No new large
MPS contraction or tensor audit is asserted here. The D180 energy
-4.761235250999516 is only an infinite-chain floating candidate.

## Updated cheap screen

An energy-shift change rescales every order-k moment by
exp[-beta(a_new-a_old)k], and every homogeneous support cap by
exp[-beta(a_new-a_old)]. This permits a transparent scalar update without
recomputing a spectrum or trusting a new root finder.

At the certified a=4.76121, beta 8, the optimistic tenth-order caps are
J = 1.1111141471 and N = 1.0851120293.
The old cap-based nontrivial-sector mass bound is
B_N(N)=3 M(m_N, v_N^10, N/10),
M(m,h,r)=floor(m/h)h^r+(m-floor(m/h)h)^r.
The leading-atom exclusion step requires its total mass upper bound to be <1.
Here B_N(128) alone is about 105875.8, regardless of the leading-atom threshold.

More generally, every saved beta in {6,8,10,12,16,20,24,32} has v_N>1 and
m_N/v_N^10>1, even after shifting to a=4.76121. Conditional on those candidate
values, the same cap majorant is at least 3 v_N^N>3 at every even N>=10. Thus this
specific exclusion test cannot succeed at any leading-atom threshold. This
conditional analytic observation is stronger than only missing a point on an
ell grid, but the input moments and caps remain exploratory.

At beta 6 the N=128 obstruction is still about 90.3. The tested D180 sensitivity
shift does not fix it. All 64 combinations (two shifts, eight betas, four trial lengths)
fail the exclusion step. This is not a no-go result for stronger joint moment
constraints, improved atom-removal filters, or a direct thermal-purity ratio.

For a second perspective, using only the MPS numerator lower bound 1 and a
single J cap c in the denominator would need
c<=(8/7)^(1/(2N)) even with zero remainder to prove T(N)>=7/8.
At N=128 the required cap is roughly 1.000522, far below 1.111114. Better MPS
energy alone at the current precision does not close this margin.

## Evidence needed before a full computation

1. Produce a scalar certificate proposal that succeeds with optimistic complete
   inputs, specifying beta, maximum moment, normalization, and the exact target
   trace errors. The present method has no successful candidate to certify.
2. If high-order moments remain useful for that different proposal, identify
   which of I/P/C and beta/2beta inputs it actually needs. The archived D2 order 10
   filter uses I/P only. A finer I/O decomposition needs C as well.
3. Reconstruct complete high-order traces, including low-M blocks and certified
   omitted-sector tails. A high-magnetization bound cannot replace missing
   low-energy eigenvalue counts within low-M blocks.
4. Propagate rational trace intervals through the Hankel/filter and root-count
   proof. Optimistic floating support caps are not certified caps.
5. Independently verify all MPS energy and analytic transfer assumptions at the
   selected lengths and show the simultaneous spatial/thermal bootstrap basin
   inequalities. Neither a faster heat trace nor a better trial energy alone
   proves a uniform spin-2 gap.

## Reproduce

Run `python screen_seed.py` in this directory. It reads the copied eight cached
candidate moment rows, performs only scalar rescaling and mass arithmetic,
and writes `seed_screen.json`. `PROVENANCE.json` records source archive paths
and hashes. The copied archived README, scalar findings and MPS summary make
the interpretation and missing pieces inspectable without the original sibling
workspace. No cached moment value is promoted to a rigorous input.
