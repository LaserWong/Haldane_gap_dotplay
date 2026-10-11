# Independently accepted smaller uniform initialization

Updated2026-10-11 02:25UTC /2026-10-10 22:25 America/New_York.

Accepted gap and unique ground state for every integer periodic length:

- .0248 for L≥34, initialized at34 with fresh MPS68;
- .0245 for L≥32, initialized at32 with fresh MPS64;
- .0179 for L≥30, initialized at30 with fresh MPS60.

Uniform spin-one Heisenberg chain, bilinear coefficient1, beta0=49/4. All18 thermal inputs are already locally reproduced. These are genuine smaller initialization sizes. No minimum-size or below30 exclusion is claimed.

See PROOF.md, scalar_results.json and anchor_results.json. All26 signed long-moment majorants and every integer window pass independent exact replay. Fresh physical D26 tensors and sequential GMP contractions match all producer anchor integers. Nineteen adversarial fixtures pass.

Reproduce only in a disposable copy with the pinned sibling packages:

    python rebuild_d26.py
    python limited_run.py 48 > benchmark48.out 2> benchmark48.log
    python limited_run.py 60 64 68 > anchors.out 2> anchors.log
    python check_anchors.py
    python audit_scalar.py
    python adversarial_tests.py

Preserve stderr logs for resource checks. Original logged resource totals are40.09CPU seconds for physical work and9.91CPU seconds for scalar replay. The physical engine is hard-capped100MiB/60CPU seconds onCPU5; scalar replay256MiB/60CPU seconds onCPU4. Fresh contractions are unnecessary for checking existing exact outputs. No thermal command is present.
