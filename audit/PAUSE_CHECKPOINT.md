# Audit results at the October 10 pause

This record describes the October 10, 2026 pause.
The project resumed on October 14, 2026, at 17:36:22 UTC.
The current repository README and AGENTS.md determine the authorized work.
The completed checks and pending tasks below retain their status at the earlier pause.

Date: 2026-10-10 16:25 UTC. No audit computations were running at the pause. Further research and monitoring required a new resumption request, and the pause superseded the earlier October 13 research schedule.

## Completed independent audits

- Extension archive: all 59 included hashes match. Recovered original archive: all 8464 manifest entries match. Scalar script copies are byte-identical.
- Uploaded dimer theorem: full transfer construction, sequential recursion, all-integer interpolation, analytic seed, exact scalar/logarithmic gap 0.055688426272, and small-size bridge checked.
- Uploaded exact examples: cache-free integer heat moments and inertia certificates reproduced. Independent angular-momentum enumeration matches all 201 moments and both heat-trace enclosures.
- Spin-1 one-retained-state dimer g=1/20: exact full residuals, Weyl completeness, Temple bounds, thermal tails and scalar replay independently pass. The gap 0.116303868802 covers every integer cell count M>=2 after the checked small-size bridge.
- Ordinary spin-1/2 square bilayer g=.01: all three exact sparse-support residuals and spectral-bin inputs, both-direction physical history kernels, three-purity map, all-integer square interpolation, and L = 2, 3 bridge pass. The gap 0.072950533962 covers every integer square side L>=2. The largest full Hilbert dimension 2^32 was not enumerated or diagonalized.
- Spin-1 large-D square model D = 1, g = .01: independent full-support residuals, local PSD comparison, bins, all seed temperatures and recursion pass. The gap 0.086452285325 covers every integer square L>=2. New small-size bridge: a=1/20,b=11/5000 gives gap>=1461/2500 for L = 2,…,7. Integer-spin time reversal supplies both directional transfers.
- Original uniform spin-1 Appendix A: all nine I/P/C heat kernels at L = 6, 8, 10 rebuilt. Independent exact L4 column checks and all saved aggregate error intervals pass. D = 26 MPS matrices and N = 72 and N = 120 exact GMP contractions freshly rebuilt. The A4 sector/filter/cooling/dominant-mass analytic bridge is independently reconstructed. Exact seed and five-round replay give gap 0.005908566393 for all integer periodic L>=1920, using the reviewed all-integer extension. This is a strengthened reproduction, not a new gap discovery. The manuscript PDF remains unavailable.
- New general two-dimensional three-purity algebra and all-square interpolation pass. Even-cycle coloring, one-dimensional contraction extension u<=1/40, scalar failure region W<=1/2, and correlation-aware first-step cancellations/adjacent-swap formulas are analytically checked.
- At ordinary-bilayer g=.03, the all-beta/all-local-comparison obstruction for the specified ground-only numerator plus independent-dimer-bin majorant family passes independent review. All three depth 2 ground inputs were also independently reconstructed, including the 32-spin full residual support 77753. Every interval and infinite-beta tail for xyt/xty/txy orders passes. It covers arbitrary improved ground pivots within the certified intervals. It is not a physical gap obstruction or phase boundary. See `independent/majorant_g003_audit.json`.
- Fully frustrated bilayer: the analytic family argument was independently checked. With conserved rung spin and both same-layer/cross-layer couplings combined as J T_i·T_j, periodic rectangular multigraphs nx,ny>=2 have sharp family-uniform gap min(1,4-12J) and unique rung-singlet ground for 0<=J<1/3. The 2x2 all-triplet doubled K2,2 sector attains 4-12J. At 1/3 it becomes ground-degenerate. Above 1/3 the product is not the 2x2 ground. Simple tori with both sides>=3 have exact gap 1 for 0<=J<=.3 by the refined star/small-occupation bounds. This is a different model from the ordinary bilayer.

## Not independently completed by this auditor before pause

- Full numerical replay of the newly optimized ordinary-bilayer g=.01 bound about .1689210216, improved axis orders, and the g=.02 improved gap candidates. Their cancellation/canonicalization theory is reviewed, but the latest per-node optimized-tail artifacts were only just supplied and were not independently replayed here.
- Complete g=.02 ordinary-bilayer seed replay. An independent check verified its local 16x16 relative-form matrix. This auditor has not yet closed every g=.02 physical input and improved scalar record.
- Spin-1 bilayer g=.005 and stronger coupling candidates beyond the models above.
- General-dimension bootstrap beyond the independently checked two-dimensional theorem.
- Any full reconstruction of the manuscript's Appendix B large physical inputs, a direct audit of the missing manuscript PDF, or uniform spin-2/spin-3 Heisenberg gap claims.
- Global optimality of positive coupling thresholds, minimal physical seed sizes, or trial dimensions, except the sharp fully-frustrated multigraph-family statement and the explicitly limited g=.03 majorant-family obstruction.

## Supporting files

- `audit/AUDIT_REPORT.md`: uploaded baseline and recovered provenance.
- `audit/NEW_RESULT_REVIEWS.md`: reviewed algebraic improvements.
- `audit/BILAYER_PHYSICAL_PROOF.md`: complete ordinary g=.01 bilayer theorem.
- `audit/APPENDIX_A_BRIDGE.md`: completed original-route proof reconstruction and scope.
- `audit/independent/`: independent verifier sources, JSON verdicts, hashes and exact local identities.
- `audit/mps/`: fresh matrix reconstruction, GMP source/binary, exact contractions and timings.
- `audit/reproduction/`: fresh baseline copies, outputs and logs.

The files ending `.time` in reproduction preserve an initial failed attempt to invoke an absent `/usr/bin/time`. The subsequent Python computations succeeded and their logs/results are the actual replay evidence. They are not performance measurements.
