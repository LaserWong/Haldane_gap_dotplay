# Bounded second-thermal pilot

Four completed producer physical inputs: L4/L6 I/P at beta49/4, exact published integer matches. Independent review pending. One partial L12 I,M0 batch: four representatives,2.62507 CPU seconds including setup,1.66846 kernel seconds,47868KiB peak RSS. Dimension73789,904333 sparse entries,1728 representatives in this block. Limits120CPU seconds/256MiB per child,CPU0; compile512MiB. C++17/GMP are already installed; no BLAS/eigensolver needed. Effective192 Horner steps; error charges281.

Host planning estimate: 11595 representatives per L12 seam. Official recorded dimensions imply116959400064 coordinate-steps per seam; measured batch uses4*73789*192. Scaling kernel work gives about3443seconds/seam before row-density adjustments, plus smaller sizes and checkpoint setup. Budget2–3 CPU hours for this scalar-column implementation, conservatively up to6 aggregate CPU hours, subject to further sector observations. This is an estimate, not measured completion time. Two one-core/256MiB workers would fit512MiB aggregate kernel budget; no launch authorized. Batch16 nominally~7seconds kernel in M0, plus~1second setup, but case/sector variation must be timed. Store checkpoints per16 representatives with unique deterministic case/M/start/count IDs.

Remaining full case list: lengths5,7,8,9,10,11,12, each I/P (14 cases). L4/L6 cases require independent audit before reuse. The completed four L12 representative records can only be reused after strict provenance and orbit checks. All18 original published intervals remain inherited premises until independent replay/review is completed.

Full physical coverage per case must sum3^n; use all magnetizations0..n and exhaustive dihedral/negation orbit lists. Expected per-seam representative totals from official evidence: n4=13,n5=22,n6=52,n7=106,n8=266,n9=630,n10=1652,n11=4270,n12=11595. Those external counts should be independently regenerated, not trusted as proof.

See PROOF.md. Important gate: current pilot resume path is intentionally not accepted as the future campaign runner. Freeze preserves this limitation; implement strict resume separately. No full campaign run.
