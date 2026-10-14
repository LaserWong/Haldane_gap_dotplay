# Version 24 variable-coupling and control tests

2026-10-11 03:46 UTC / 2026-10-10 23:46 EDT. Frozen producer evidence for independent review. No production job, complete 8×4 support contraction/cache or new gap claim exists.

## Results

Six complete physical fixtures (localized, symmetrized and generic sources on 4×2/5×2) pass. Each checks all prior 15 signed terms/m0–m4 plus two new weighted bilinears, and compares the complete fixed-source 2×2 G,K(g),J(g) at five exact couplings:0,1/10,11/100,3/25,1/4. These are 30 physical pencil comparisons, with ψ and χ=T0ψ fixed while g changes. A separate consumer reconstructs all 30 from serialized sector data and rejects 60 factor-of-two/four denominator mutations.

The complete generic 4×2 fixture also equals the sum of four independently run sector chunks in all 24 fields. Controller-death injection observed the numerical worker after exec, proved the inherited lock excluded another controller, killed the controller, and observed parent-death SIGKILL terminate its worker. The supervisor reaped both. Its 3-second reservation remained charged and became abandoned_charged on recovery. The explicitly authorized resumed range had a separate 3-second charge and passed exact 24 comparison.

Strict adoption verifies every worker output digest against the exit-time receipt, verifies that receipt against the ledger, checks fixed input/executable/schema/range/rank identities and reconstructs all five chunk moments from 24 fields before commit. Corruption of old low-sector fields and each new weighted field is rejected. Duplicate identical commits count once. Conflicting/overlapping/missing/truncated/version 22 data fail. All signed integers remain allowed.

Final-O2 explicit-denominator smoke fixture passes. Its 24 values equal the earlier-O1 source fixture. Final-O2 cold sample:64q6 targets 0..63 and 16q4 targets 0..15 in the dispersed schedule. Body times .555416 and .118123 CPU seconds. No warm pass. Their whole-body mean projection is 1507.736555 seconds. This is sampled timing, not completed moments or a rigorous bound.

Gate charge 74/90 CPU seconds (soft 75), including 10 reserved controller/metadata seconds. Guarded child wait4 CPU 22.368805, plus .079964 from the external controller-death supervisor. Recorded controller CPU 2.790681736. Serialized test metadata CPU .148216191 and metadata child wait4 .057065. Maximum numerical/guard RSS 56,500 KiB. See SUMMARY.json and receipts for exact scope. Compilation separately 512 MiB/CPU 6. Compiler CPU was not recorded by wait4 and is not included in these runtime totals.

## Explicit schema and pencil units

The schema is `bilayer-moment24-v1`.
Fields 0–21 retain the original 22 fields in their original order.
Field 22 is UZ=<Qψ,z>, and field 23 is WZ=<Qχ,z>, with χ=T0ψ,z=T0χ,T0=200Q+11A,A=C+C†+D.
Every checkpoint carries its schema.
A 22-field record or a version 22 name is rejected.
Sector records remain separate until the correct weights are applied.

The final source and consumer use K_numerators/J_numerators with explicit physical_K_denominator/physical_J_denominator or K_denominator/J_denominator. For g=num/den the denominators are 22·den and (22·den)^2. G has denominator 1. Do not divide these common numerators only by 11 or 121. The initial-O1 fixture files retain historical keys K_scaled_11/J_scaled_121. *_physical_pencils_v1.json exports bind their raw SHA256 and give the unambiguous denominator fields. These historical files are not silently rewritten.

The consumer operates on unnormalized fixed-source matrices. It does not normalize the basis, diagonalize a pencil, find roots, or claim a spectral bound.

## Key files

- whole.cpp, whole: final-O2 numerical source/executable.
- whole_pre_denominator.cpp / whole_pre_denominator: original-O1 source/binary used for all six full fixtures and the controller-death/recovery run. DENOMINATOR_ONLY_SOURCE.diff records the output-only source change. whole_O1_denominator preserves the intervening-O1 build. Input-pin epochs are separately retained. Receipts are not rebound.
- controller.py: bounded 90/75 dispatcher, parent-death+inherited-lock lifetime control, numeric/proc guard/subreaper, strict digest adoption, atomic checkpoints and 24-field coverage finalization.
- controller_pre_commit_lock.py: previous controller revision used for the initial fixture/control runs, preserved for receipt provenance. Final controller adds exclusive locking around adoption. No numerical identities are silently changed.
- production_admission.py:2945-chunk exact coverage plan and complete remaining-reservation/retry/deadline forecast, tested with synthetic ledgers.
- production_controller.py / build_production_controller.py: separate generated production-profile entrypoint wiring the actual nonzero complete plan forecast before every reservation. It requires an explicit authority file, hash-pinned inputs/expected controls and job directory. None has been created. Its numerical launch path has not run. It shares the gate's guard/lifetime/adoption implementation, with allocation and full-plan wiring differences visible in the generator.
- production_finalize.py: mandatory complete coverage and accepted m0/m1/m2 control comparison before writing FULL_MOMENTS.json. Actual accepted 57-dimensional controls must still be supplied from reviewed evidence and pinned before any production launch.
- pencil24.py: exact consumer with explicit denominators.
- *_TESTS.json, CONTROLLER_DEATH_TEST.json, committed/, recovery/, mutations/: retained positive/negative evidence.
- BUDGET_LEDGER.json and runs/*/receipt.json: no-refund charges, input/output hashes, CPU/wall/RSS and failure history.

Use fresh isolated copies for review. PYTHONDONTWRITEBYTECODE=1 prevents irrelevant cache writes. Build final whole.cpp directly, not a historical generator. g++ -O2 -std=c++17 whole.cpp -lgmpxx -lgmp -o whole. Reviewer must initialize its own pinned identities and separately authorized ledger, never mutate this frozen gate. Numerical workers and their guard launches were CPU 6/single-threaded. Standalone metadata/serialization scripts were serial but not separately affinity-pinned. Their measured costs are covered by the 10-second controller reserve. No claim is made that those metadata helpers ran on CPU 6.

## Remaining admission limits

Independent review must pass before requesting 21600-second production authority. The production-profile entrypoint has static/metadata admission tests but no production numerical run. Actual expected 57-dimensional m0/m1/m2 input controls, authority, output directory and pin file are deliberately absent. Per-chunk assembly alone is not the physical full-control check. Numerical processing must never proceed on a partial coverage union.

Parent-death tests cover the intended single-process numerical binary. No claim of general hostile-daemon containment is made. The fsync/rename tests exercise process crashes, not physical power loss. A controller CPU outlier 1.6776 seconds occurred in the first generic 4 receipt. Report it rather than erase it. Recorded controller clocks omit some interpreter/final-write work, hence the explicit controller reserve and independent accounting review remain necessary. The producer does not declare this package independently approved or production ready merely because component tests pass.
