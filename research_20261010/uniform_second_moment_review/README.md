Updated 2026-10-10 19:37 EDT (America/New_York) / 23:37 UTC.

The independent review conditionally accepts gap >= .0214 and a unique ground state for every integer L >= 36 in the uniform periodic spin-one Heisenberg chain.

The result assumes all 18 published beta49/4 integer-total/error certificates, which are used to reconstruct tighter scalar intervals. The full set has not been physically rerun locally, so those thermal inputs remain conditional.

REVIEW.md gives the complete independent derivation, provenance and scope. Reproduce the review using only the Python standard library:

    python audit.py
    python adversarial_tests.py

Each script uses CPU2 with limits of 600 CPU seconds and 700 MiB. No thermal computation or producer modification is performed. Inputs and results are sealed. The original-source snapshots retain their Apache-2.0 attribution/license and verified Git blob pins.
