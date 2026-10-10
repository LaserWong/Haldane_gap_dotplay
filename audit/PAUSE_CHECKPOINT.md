# Audit checkpoint: paused at user request

Date: 2026-10-10 16:25 UTC. No audit computations remain running. No further research or monitoring will be started without a new resume request. The prior October13 research schedule is superseded by this pause.

## Completed independent audits

- Extension archive: all59 included hashes match. Recovered original archive: all8464 manifest entries match. Scalar script copies are byte-identical.
- Uploaded dimer theorem: full transfer construction, sequential recursion, all-integer interpolation, analytic seed, exact scalar/logarithmic gap0.055688426272, and small-size bridge checked.
- Uploaded exact examples: cache-free integer heat moments and inertia certificates reproduced; independent angular-momentum enumeration matches all201 moments and both heat-trace enclosures.
- Spin1 one-retained-state dimer g=1/20: exact full residuals, Weyl completeness, Temple bounds, thermal tails and scalar replay independently pass. Gap0.116303868802 covers every integer cell countM>=2 after the checked small-size bridge.
- Ordinary spin-half square bilayer g=.01: all three exact sparse-support residuals and spectral-bin inputs, both-direction physical history kernels, three-purity map, all-integer square interpolation, and L2,3 bridge pass. Gap0.072950533962 covers every integer square sideL>=2. The largest full Hilbert dimension2^32 was not enumerated or diagonalized.
- Spin1 large-D square model D1,g=.01: independent full-support residuals, local PSD comparison, bins, all seed temperatures and recursion pass. Gap0.086452285325 covers every integer squareL>=2. New small-size bridge: a=1/20,b=11/5000 gives gap>=1461/2500 forL2…7. Integer-spin time reversal supplies both directional transfers.
- Original uniform spin1 Appendix A: all nine I/P/C heat kernels atL6,8,10 rebuilt; independent exact L4 column checks and all saved aggregate error intervals pass. D26 MPS matrices and N72,N120 exact GMP contractions freshly rebuilt. The A4 sector/filter/cooling/dominant-mass analytic bridge is independently reconstructed. Exact seed and five-round replay give gap0.005908566393 for all integer periodicL>=1920, using the reviewed all-integer extension. This is a strengthened reproduction, not a new gap discovery; the manuscript PDF remains unavailable.
- New general2D three-purity algebra and all-square interpolation pass. Even-cycle coloring,1D contraction extensionu<=1/40, scalar failure regionW<=1/2, and correlation-aware first-step cancellations/adjacent-swap formulas are analytically checked.
- At ordinary-bilayer g=.03, the all-beta/all-local-comparison obstruction for the DECLARED ground-only numerator plus independent-dimer-bin majorant family passes independent review. All three depth2 ground inputs were also independently reconstructed, including the32-spin full residual support77753. Every interval and infinite-beta tail for xyt/xty/txy orders passes. It covers arbitrary improved ground pivots within the certified intervals; it is NOT a physical gap obstruction or phase boundary. See `independent/majorant_g003_audit.json`.
- Fully frustrated bilayer: the analytic family argument was independently checked. With conserved rung spin and both same-layer/cross-layer couplings combined asJ T_i·T_j, periodic rectangular multigraphs nx,ny>=2 have sharp family-uniform gap min(1,4-12J) and unique rung-singlet ground for0<=J<1/3. The2x2 all-triplet doubled K2,2 sector attains4-12J. At1/3 it becomes ground-degenerate; above1/3 the product is not the2x2 ground. Simple tori with both sides>=3 have exact gap1 for0<=J<=.3 by the refined star/small-occupation bounds. This is a different model from the ordinary bilayer.

## Not independently completed by this auditor before pause

- Full numerical replay of the newly optimized ordinary-bilayer g=.01 bound about.1689210216, improved axis orders, and the g=.02 improved gap candidates. Their cancellation/canonicalization theory is reviewed, but the latest per-node optimized-tail artifacts were only just supplied and were not independently replayed here.
- Complete g=.02 ordinary-bilayer seed replay. Root independently checked its local16x16 relative-form matrix; this auditor has not yet closed every g=.02 physical input and improved scalar record.
- Spin1 bilayer g=.005 and stronger coupling candidates beyond the models above.
- General-dimension bootstrap beyond the independently checked2D theorem.
- Any full reconstruction of the manuscript's Appendix B large physical inputs, a direct audit of the missing manuscript PDF, or uniform spin2/spin3 Heisenberg gap claims.
- Global optimality of positive coupling thresholds, minimal physical seed sizes, or trial dimensions, except the sharp fully-frustrated multigraph-family statement and the explicitly limited g=.03 majorant-family obstruction.

## Main packaging paths

- `audit/AUDIT_REPORT.md`: uploaded baseline and recovered provenance.
- `audit/NEW_RESULT_REVIEWS.md`: reviewed algebraic improvements.
- `audit/BILAYER_PHYSICAL_PROOF.md`: complete ordinary g=.01 bilayer theorem.
- `audit/APPENDIX_A_BRIDGE.md`: completed original-route proof reconstruction and scope.
- `audit/independent/`: independent verifier sources, JSON verdicts, hashes and exact local identities.
- `audit/mps/`: fresh matrix reconstruction, GMP source/binary, exact contractions and timings.
- `audit/reproduction/`: fresh baseline copies, outputs and logs.

The files ending `.time` in reproduction preserve an initial failed attempt to invoke an absent `/usr/bin/time`; the subsequent Python computations succeeded and their logs/results are the actual replay evidence. They are not performance measurements.
