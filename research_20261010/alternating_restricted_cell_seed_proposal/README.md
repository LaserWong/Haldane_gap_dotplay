# Restricted positive-cell seed feasibility and nonperturbative pilot design

Updated 2026-10-11 00:05 EDT (America/New_York, UTC−4) / 2026-10-11 04:05 UTC.

**Outcome: the tested restricted-data recipe does not close cell seeds 15, 16 or 17, even at g=1. No alternating g=.9 pilot was launched.** This is a scoped obstruction to the present moment/support/majorant construction, not a no-go for the available information, a claim of gaplessness, or a theorem that another seed construction cannot work.

**Resource verdict: NOT ACCEPTED.** Actual child CPU across all six launches was 30.397826 seconds, exceeding the authorized 30 seconds by .397826 seconds. Including the recorded .05-second supervisor reserve per launch, the charged total is 30.697826 seconds. The final configured 8-second RLIMIT_CPU was not enforced as expected: the process completed with 10.791353 actual CPU seconds. No subsequent scientific computation was performed. This historical violation remains part of the package; the mathematical outputs are producer checks requiring independent review, not accepted resource-compliant certificates.

- [Mathematical construction and exact scoped failure](PROOF.md)
- [Joint-moment, additional-constraint and numerator assessment](ANALYTIC_ASSESSMENT.md)
- [Minimal gated pilot, design only](MINIMAL_PILOT_PLAN.md)
- [Sources and reproduction](SOURCES.md)
- [Resource record and enforcement limitations](RESOURCE_REPORT.md)

The input uses physical even lengths 4,6,8,10,12, I/P spatial seams, beta=49/4; these are cell moments 2,3,4,5,6. It never uses physical odd lengths as cell moments. Existing exact MPS anchors have physical lengths60/64/68, one trial vector and bond dimension26. The full physical Hilbert dimensions remain3^60,3^64,3^68.

Final exact producer endpoints, decimal displays:

| Cell seed | Physical seed | Anchor length | S lower | T lower | Failure |
|---|---:|---:|---:|---:|---|
|15|30|60|.9086198577303725|.8268667138441227|Third spatial update nonpositive|
|16|32|64|.9297410616944342|.8169477965324805|Third thermal update nonpositive|
|17|34|68|.9461546175250289|.8069743583783997|Third thermal update nonpositive|

A **counterfactual sufficient target**, not achieved data: retaining the cell17 S endpoint while replacing T by .835 closes a .005 gap after four doublings. With the unchanged MPS68 numerator this requires a trace upper bound Q34≤1.0944628815077482, against the present1.1133056350335735. A better trial numerator is a separate possible route, detailed in the assessment.

All files here are new. Existing sealed packages and remote state are unchanged. The working tree is an exported repository without accessible .git metadata, so no branch or commit identity is inferred from git. The parent owns any root README/status update.
