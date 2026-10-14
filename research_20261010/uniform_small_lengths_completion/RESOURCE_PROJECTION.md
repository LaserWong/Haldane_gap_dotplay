# Resource projection for the short-length completion

The proposed batch constructs own-length MPS anchors 4..23 using the unchanged D26 powers 1/2/4/8/16. A recent length-25 run took 2.05 CPU seconds, and the earlier combined 12/16/20/24 run took 2.33 CPU seconds. The 20 shorter lengths are projected to need 12–20 CPU seconds and less than 35 MiB.

The separately authorized finite-completion calculation has hard limits of 30 CPU seconds and 100 MiB on CPU5. Separate compilation uses CPU2 with limits of 512 MiB and 30 CPU seconds. Each bounded cached-scalar stage uses CPU2 with at most 30 CPU seconds and 256 MiB. No thermal calculation, exact diagonalization, or tensor optimization is included. Execution must wait until the independent length-25 reviewer releases CPU5.
