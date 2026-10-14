# Independently accepted smaller uniform initialization

Updated 2026-10-11 02:25 UTC /2026-10-10 22:25 America/New_York.

The following gaps and a unique ground state are accepted for every integer periodic length in the specified range.

- .0248 for L≥34, initialized at 34 with fresh MPS68.
- .0245 for L≥32, initialized at 32 with fresh MPS64.
- .0179 for L≥30, initialized at 30 with fresh MPS60.

Uniform spin-one Heisenberg chain, bilinear coefficient 1, beta0=49/4. All 18 thermal inputs are already locally reproduced. These are genuine smaller initialization sizes. No minimum-size claim or exclusion below 30 is made.

See PROOF.md, scalar_results.json and anchor_results.json. All 26 signed long-moment majorants and every integer window pass independent exact replay. Fresh physical D26 tensors and sequential GMP contractions match all producer anchor integers. Nineteen adversarial fixtures pass.

Reproduce only in a disposable copy with the pinned sibling packages, using the following commands.

    python rebuild_d26.py
    python limited_run.py 48 > benchmark48.out 2> benchmark48.log
    python limited_run.py 60 64 68 > anchors.out 2> anchors.log
    python check_anchors.py
    python audit_scalar.py
    python adversarial_tests.py

Preserve stderr logs for resource checks. Original logged resource totals are 40.09 CPU seconds for physical work and 9.91 CPU seconds for scalar replay. The physical engine is hard-capped 100 MiB/60 CPU seconds on CPU 5. Scalar replay is capped at 256 MiB and 60 CPU seconds on CPU 4. Fresh contractions are unnecessary for checking existing exact outputs. No thermal command is present.
