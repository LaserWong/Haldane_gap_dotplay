# Restricted positive-cell seeds

Updated 2026-10-11 00:05 EDT (America/New_York, UTC−4) / 2026-10-11 04:05 UTC.

The tested construction fails for cell seeds 15, 16 and 17 even at g=1. No alternating-chain pilot at g=.9 was launched. The failure applies to this choice of moments, support bounds and majorant. It does not rule out other uses of the available information or establish physical gaplessness.

The resource review recorded **NOT ACCEPTED**. Actual child CPU across all six launches was 30.397826 seconds, exceeding the authorized 30 seconds by .397826 seconds. Including the recorded .05-second supervisor reserve per launch, the charged total is 30.697826 seconds. The final configured 8-second RLIMIT_CPU was not enforced as expected. The process completed with 10.791353 actual CPU seconds. No subsequent scientific computation was performed. The overrun remains part of the record. The mathematical outputs are producer checks awaiting independent review, and the run did not meet its resource requirements.

- [Mathematical construction and exact scoped failure](PROOF.md)
- [Joint-moment, additional-constraint and numerator assessment](ANALYTIC_ASSESSMENT.md)
- [Minimal gated pilot, design only](MINIMAL_PILOT_PLAN.md)
- [Sources and reproduction](SOURCES.md)
- [Resource record and enforcement limitations](RESOURCE_REPORT.md)

The input uses physical even lengths 4,6,8,10,12, I/P spatial seams, beta=49/4. These are cell moments 2,3,4,5,6. It never uses physical odd lengths as cell moments. Existing exact MPS anchors have physical lengths 60/64/68, one trial vector and bond dimension 26. The full physical Hilbert dimensions remain 3^60,3^64,3^68.

The exact producer endpoints are displayed below in decimal form.

| Cell seed | Physical seed | Anchor length | S lower | T lower | Failure |
|---|---:|---:|---:|---:|---|
|15|30|60|.9086198577303725|.8268667138441227|Third spatial update nonpositive|
|16|32|64|.9297410616944342|.8169477965324805|Third thermal update nonpositive|
|17|34|68|.9461546175250289|.8069743583783997|Third thermal update nonpositive|

A conditional calculation shows that retaining the cell17 S endpoint and replacing T by .835 would certify a .005 gap after four doublings. The target T value was not achieved. With the unchanged MPS68 numerator this requires a trace upper bound Q34≤1.0944628815077482, against the present 1.1133056350335735. A better trial numerator is a separate possible route, detailed in the assessment.

The work added this proposal without changing existing sealed packages or remote state. The exported working tree had no accessible .git metadata, so its branch and commit identity were not established. Root README and status updates were outside this proposal.
