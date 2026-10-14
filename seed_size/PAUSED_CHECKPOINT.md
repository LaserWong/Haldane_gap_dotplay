# Results at the October 10 pause

This record describes the October 10, 2026 pause.
The project resumed on October 14, 2026, at 17:36:22 UTC.
The current repository README and AGENTS.md determine the authorized work.
The completed checks and pending tasks below retain their status at the earlier pause.

Paused on explicit user request at 2026-10-10 16:25 UTC. No background process remained running in this calculation at the pause. The pause required a new user instruction before research or scans could resume.

## Saved files

- `README.md`: results, model distinctions, length conventions, reproduction entrypoints.
- `proofs/DERIVATIONS.md`: detailed proofs, necessary-window reasoning, and exact scope of the majorant-family obstruction.
- `results/uniform_n2_all_beta.json`: exact analytic-spectrum Bernstein certificates for uniform spin 1, 2, 3 at fixed n=2.
- `results/necessary_temperature_windows.json`: rigorous incompatible thermal/spatial beta windows.
- `results/asymmetric_basin.json`: outward-certified two-purity basin boundary brackets.
- `results/colored_dimer_certificates.json`, `results/correlated_seed_results.json`: analytic dimer improvements and finite-size patch status.
- `results/optimized_bilayer_tail_results.json`: optimized spin-1/2 bilayer certificates, with actual beta/2beta local parameters at every node and complete ground-certificate snapshots.
- `results/stored_tail_replay_validation.json`: six optimized bilayer certificates independently replayed without rerunning a floating-point minimizer. All pass.
- `results/bilayer_majorant_ceiling.json`: all-beta/all-local-a obstruction at g=.03, also allowing zero ground width and every refined ground pivot within current certified intervals. This is a ground-only-numerator / independent-bin-tail recipe obstruction, not a physical phase boundary or all-method fixed-size exclusion.
- `results/single_layer_large_D_order_results.json`: optimization of the single-layer spin-1 large-D model, which is distinct from the spin-1 bilayer.
- `results/extended_bilayer_order_results.json`: spin-1 bilayer and spin-1/2 depth-2 scans. Grid failures are not exclusions.
- `results/validation.json`: eight exact-arithmetic regression tests passed with approximately 61 MiB peak RSS.

## Audit status

The independent review covered the W≤1/2 invariant failure region, the two-color dimer Hoeffding improvement, the one-dimensional entry extension u≤1/40, exact correlation cancellations, valid adjacent staircase swaps, the analytic optimum of the bilayer local first-bin bound, and the optimistic ground-refinement envelope. Full proof-assistant formalization is not claimed.

The optimized-tail artifact omission noted during audit was fixed: actual a,b,alpha,B,Q bounds at all used beta/2beta nodes are now persisted, and all six accepted optimized records replay without floating-point optimization.

All saved 2D certificates use the audited common-defect entry u≤1/500. A possible u≤1/200 extension was only proposed moments before the pause. It was not applied, proved, or included in any saved result.

Enhanced 2D gaps retain their L≥L0 scopes. No unrecorded finite-square bridge is claimed. At g=.01 the latest optimized value is approximately .1689210216 for L≥4. At g=.02 it is .0573084578 for L≥16.

## Tasks recorded for a later resumption

1. Read this checkpoint, README, and DERIVATIONS before rerunning anything.
2. Verify any updated physical-input records against saved snapshots. Keep model IDs explicit.
3. Prioritize excited-state/tail improvements at spin-1/2 bilayer g=.03. More ground digits alone cannot rescue the declared current recipe.
4. The requested g=.025/.0225/.0275 coupling-frontier records were put on hold and were not scheduled for automatic generation.
5. Pending proposals: Schur-complement low-excitation comparison, stronger cluster bins, finite-square bridges, and the unverified u≤1/200 two-dimensional entry extension.
