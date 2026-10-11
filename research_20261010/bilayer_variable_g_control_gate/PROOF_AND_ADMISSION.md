# Algebra, coverage and admission

## Two new quantities and fixed-source pencils

Let u=Qψ,w=Qχ,χ=T0ψ,z=T0χ,d=200,h=11. For arbitrary exact g, H′(g)ψ=a u+bχ and H′(g)χ=a w+bz, where a=1−200g/22,b=g/22. G=(m0,m1;m1,m2).

K00=a<ψ,u>+b m1; K01=a<u,χ>+b m2; K11=a<χ,w>+b m3.
J00=a²<u,u>+2ab<u,χ>+b²m2.
J01=a²<u,w>+ab(<u,z>+<χ,w>)+b²m3.
J11=a²<w,w>+2ab<w,z>+b²m4.

UZ=<u,z> and WZ=<w,z> are the only new accumulated fields. All other weighted quantities reconstruct from sector-separated fields: <ψ,u>=Σq q m0q; <u,u>=Σq q²m0q; <u,χ>=Σq q m1q; <u,w>=Σq q²m1q. For χ, include the omittedq8 norm: <χ,w>=Σ(q≤6)q||χq||²+968n8; <w,w>=Σ(q≤6)q²||χq||²+7744n8.

UZ is accumulated overq≤6 as q<ψq,zq>. WZ includes q<χq,zq> onq≤6 plus its q8 contribution8[11<γ,v>+1331(<m,Ecm>+<m,Nm>)]. Hereγ=C†Cm+Km andv is the existing q8 source. The independent algebra alternative is1548800n8+10648d8+4cross6 for that q8 WZ contribution. Noq10 contribution exists becauseχ10=0. Complete physical fixtures explicitly compare both weighted bilinears to full physical Qψ,Qχ,z vectors.

For g=num/den, set A=22den−200num,B=num. Stored K common numerators use A,B and divide by22den; J common numerators divide by(22den)^2. The direct physical fixture builds Hscaled=2den·Q+num·Aoperator; its comparisons multiply K by11 and J by121, which explains the old raw names but does not change the physical denominators. Consumer tests independently restore these denominators and reject halving/quartering them.

## Integer/diagram safety

This extension changes only GMP bilinear accumulators, not the source/image channel type or rule application. Signed int128 source arithmetic remains checked. UZ/WZ products import existing bounded images into GMP and apply sector/prefactor weights there. Bounds are for the fixed accepted witness, not arbitrary coefficients. The independently reviewed whole-pipeline bound table found elementary rulemax1,Kmax3,E/E†max2 and fixed-witness partial-contraction envelope<2^104. That review's manifest is da9d659b68317702eec8db66beaa5ff3b21ffdb623ee3aa6b63663e86834f810. New scalar products are unbounded-size GMP.

## Deterministic coverage and exact finalization

The complete production plan contains vacuum1, fullq2=496, originq4=4495 and originq6=169911. Chunks are1,64,16,64 targets, respectively, yielding2945 disjoint sequence ranges. Target rank=(a·i) modN withq6a65536,q4a1024,q2a127. Each multiplier is coprime to its modulus, so this is a bijection. The metadata plan checks complete range unions without evaluating a full support pass.

Checkpoint schema/job/range/hash checks and exact24-field integer accumulation remain sign-unrestricted. Complete sector unions are mandatory. For large geometry, normalize originq4 by8 and originq6 by16/3; fullq0/q2 use1. Occupied-site translation counting proves the weights with stabilizers, and rule embeddings are not divided by32 again. A partial sample is explicitly rejected by the complete-coverage finalizer.

production_finalize.finalize_job first verifies current pins, locks the job, adopts successful receipt-bound outputs, requires one exact job identity and complete sector coverage, then reads hash-pinned EXPECTED_M012.json. The expected control schema includes T_Q200,T_A11,m0,m1,m2,witness SHA256 and geometry SHA256. It must agree with reviewed accepted57D evidence before launch. After normalization the recomputed G entries must equal those controls. Only then can FULL_MOMENTS.json be written. The control-mismatch path is tested on complete small data. The actual8×4 control file/full comparison remains unperformed because no production is authorized.

## Lifetime, recovery and atomicity

The worker sets PR_SET_PDEATHSIG(SIGKILL) immediately afterfork and checks its expected parentPID, closing the death-before-prctl race. It inherits the same flock file description across exec. Thus a dead controller cannot release the exclusive job lock while its numerical worker remains live. The observed exec-worker death test verifies this intended path. Parent/controller and orphan cleanup use numeric/proc observation, process-group kill, subreaper andwait4. Missing accounting fails closed. Reconciliation compares recordedPID starttime and refuses a still-live matching old worker; stale reservations become abandoned_charged without refund.

Every attempt reserves beforefork, then stores PID/starttime and immutable hashes. Every successful worker output is hashed in its receipt before adoption. Adoption is exclusively locked, verifies the receipt is present unchanged in the ledger, checks all output hashes and24schema, validates deterministic target ranks/ranges, and cross-checks the five moment assemblies. Prepared checksum journals precede atomic completed-chunk publication. Identical duplicates contribute once; conflicting or overlapping ranges fail. Temporary partial data is diagnostic only. Root explicitly authorized the planned killed/resumed tests; unexpected retries remain forbidden without a specific decision.

## Complete21600 admission implementation, not authorization

production_admission.plan defines all2945 exact ranges. Its forecast computes the actual remaining standard reservations, tracks completed ranges and failed charges, rejects already complete/unreconciled ranges, requires named retry authority, and tests the whole remaining CPU and wall forecast before admitting one chunk. production_controller.run wires this forecast, stores it in the prelaunch reservation, and requires an explicit authority file specifying21600/20000 and2026-10-14T00:00:00Z. The authority-file hash is retained perattempt; it is not silently included in the numerical source identity, so a specifically authorized retry can be documented without changing the fixed witness. No such authority/job files exist here.

Standard reservation plan:2655q6×6=15930;281q4×3=843;9lowq/vacuum×3=27, total16800. Controller/finalization reserve1200 plus retry reserve3600 yields21600. Failed attempts reduce the remaining retrybucket and retain their full charge. Full-plan wall forecast is2×remaining reserved CPU+1200seconds, compared to the absolute deadline; this is an admission margin, not a guarantee of scheduler availability. The active90-second gate never invokes the21600profile.

Final24-field-O2 sample predicts1474.551375q6+33.185180q4=1507.736555body seconds. Add147.25startup(.05×2945),10lowq and100controller/filesystem/finalization, then preserve10× empirical allowance:17649.86555seconds. The21600proposal has3950.13445seconds planning headroom. This is less than the earlier22-field headroom and is not a rigorous time bound. Full-cache setup is not assumed; each chunk uses the tested capped lazy path. Actual perchunk timeouts, memory/deadline or accepted-control failures stop and remain charged; no automatic budget expansion.

## Review scope

Producer test success, independent review and final physical certification are separate. The numerical24gate and consumer tests are executed evidence. The production-profile guard is derived from that controller and its full-plan admission arithmetic is metadata-tested; its production execution has not run. Independent reviewer must check those differences and resource accounting before root can authorize production. Any remaining initialization/control gap must be reported, not hidden under this cost proposal. No gap, spectral endpoint, variational eigenvalue or normalized-state claim follows from these fixtures or samples.
