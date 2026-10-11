# Coverage, transactions and next production contract

## Exact schema and kernel

The22 fields are the15 signed terms in the frozen whole-pipeline order, followed by m0,m1,m2low,m3low,m4low,n8,cross6. They are serialized as canonical decimal GMP integer strings, never floats. Each chunk preserves its sector, sequence begin/end, full sector size and exact job identity. The numerical kernel is inherited unchanged: only an output sidecar and deterministic chunk path were added. All six complete fixtures pass, and the complete generic4×2 union of independently executed sector chunks equals its uninterrupted22-field result.

## Bijection and normalization

For largeq6,N=169911,a=65536; q4,N=4495,a=1024; q2,N=496,a=127. Target rank is a·i modN. The first two multipliers are powers of2 with odd modulus, so coprime. gcd(127,496)=1. Thus every complete sequence interval union[0,N) enumerates every target rank once. Complete small ranks are checked explicitly; large modular inverses/boundaries and all sampled rank/unrank pairs are checked without a full8×4 support enumeration. Origin supports fixsite0 and rank the remaining q−1 sites among1..31.

Small chunk fixtures use full supports and unit weights. Eventual large production uses fullq0/q2, originq4 weighted8 and originq6 weighted16/3. The occupied-site counting proof is valid with translation stabilizers: N times the origin-containing scalar sum equals q times the full scalar sum. Rule embeddings are already included and must not be divided by32 again. For final production retain sector-separated22 fields until applying the exact GMP/rational weight and checking divisibility/acceptedm0–m2 controls.

## Transaction protocol

Atomic JSON writes use fresh exclusive temporary files, flush+fsync, os.replace, then directoryfsync. Abandoned temporary files do not block future writes or enter summation. The prepared journal records the expected complete-chunk digest before data publication. A post-rename crash can therefore be reconciled from journal+data; a prewrite or partial-write crash contributes nothing until the exact completed payload is recovered. Mutation tests verify the hash and coverage checks.

Commit rejects an existing prepared filename with a conflicting digest. An identical duplicate returns without adding a new contribution. Finalization verifies every file against the prepared digest, verifies job/schema/sector/size, sorts each sector's ranges and demands a contiguous nonoverlapping union from0 toN. It sums all22 components exactly once. Missing/partial/overlapping outputs cannot be complete moments.

The dispatcher locks the job directory, validates fixed inputs and the monotone budget, reserves beforefork and atomically persists that reservation. Charge=controller reserve+sumattempt charges is checked exactly, attempts have positive reservations and charges no smaller than reservations, and duplicate attempt names are rejected. Failed/interrupted attempts remain charged. Runtime never automatically retries unexpected failures. The one deliberate numerical interruption/resume is explicitly authorized and separately charged.

## Observer and termination

Scan numeric/proc entries and parse PPid,pgrp,session,CPU,RSS and thread count from stat. Construct descendants/group members and refuse unexpected children/threads. Missing mandatory live-child accounting or parser/observer exceptions trigger termination. Sum child/descendant CPU and liveRSS; RLIMIT_CPU/AS and singleCPU6 affinity provide secondary controls. PR_SET_CHILD_SUBREAPER plus groupkill and explicitwait4 drain orphan descendants. Receipts record all seen/reapedPIDs and no survivors are accepted. Parent waited-childCPU may conservatively double-count around a reap race; finalwait4 usage is the receipt accounting basis.

The numerical binary is intentionally single-process. General enforcement for arbitrary hostile daemonization is not claimed; independent guard review should assess the exact approved workload. No missing observation is silently treated as zero.

## Measured new-schedule costs

128q6 target bodies:.963076 CPU seconds, projection1278.415674 seconds.32q4 bodies:.237259, projection33.327475. Combined1311.743149 seconds. Isolated worker setup is.012341–.016633 seconds, below the proposed.05 perchunk startup allowance. Four measured sample controller costs are about.0093–.0379seconds each; these are partial controller clocks as noted in README.

Retain the more conservative previous512-target cold-body projection1406.474463 for admission, rather than reduce the envelope from a smaller128-target sample.2945 fresh processes at.05 startup allowance add147.25. Add10 forlowq and100 forcontroller/filesystem/finalization, then multiply by10:16637.24463 CPU seconds. This remains an empirical planning envelope, not a rigorous maximum. The proposed21600 cap has4962.75537seconds headroom. The new sample separately predicts15689.93149 with the same allowances, but is not used to silently lower reservations.

Candidate no-refund reservations:2655q6 chunks×6seconds=15930;281q4×3=843;8q2+vacuum×3=27; total16800. Allocate1200controller/finalization and3600charged retry/repartition reserve, sum21600. Existing integer cap−2 internal numerical deadline means a3-secondworker gets1second compute; the observed q4sample is far below this, but any repartition/guard-margin change requires explicit testing before launch. No cap or deadline is automatically expanded. Retryforecast includes all failed reservations.

Production authorization is still absent. A final reviewed launcher must configure21600 only after rootdecision, preserve one job lock/immutable identities, dispatch exact disjoint ranges, reconcile completion receipts/output hashes, atomically commit22 fields and enforce full coverage before momentassembly. It must use measured/independently reviewed complete controller accounting and leave deadline margin for the independently authorized numerical replay. Fullm0/m1/m2 must match accepted controls. Fullm3/m4 do not alone certify a gap or endpoint.

## Variable-g extension excluded

Withu=Qψ,w=Qχ,a=1−200g/22,b=g/22, H(g)ψ=a u+bχ and H(g)χ=a w+bz. Thus J01=a²<u,w>+ab(<u,z>+<χ,w>)+b²m3 and J11=a²<w,w>+2ab<w,z>+b²m4. Existing sector-separated norms/m1 reconstruct several weighted bilinears, but <u,z> and <w,z> require new accumulation. Theq8 part of<χ,z> is11<γ,v>+1331(<m,Ecm>+<m,Nm>); itsQweighted contribution is8 times that. These images already exist, so an extension is cheap pertarget, but it changes the schema and requires independent full physical/serialization tests. It is not part of this frozen22-field gate; only5seconds remain before itssoft90stop. Request a separate bounded extension rather than silently weaken testing or expand this budget.
