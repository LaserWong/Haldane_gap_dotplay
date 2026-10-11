# Physical32 B², finite fidelity, and Gibbs effect

2026-10-11 04:14 UTC. Exact producer result; independent review pending.

## Scope and physical normalization

Use the same periodic spin-one D26 translation-invariant MPS and unit-exchange H=sum_j h_j as all accepted uniform-chain anchors. At physical length L=32, define B=sum_odd h_j−sum_even h_j and b=3L/2=48. The Cartesian-bond spectrum is−2,−1,1, so centering every bond by1/2 gives ||B||<=b. Translation invariance makes the trial mean of B zero. The newly contracted observable is B², not H².

All local transfer insertions T,O=E_h,U=E_(h²),V=E_(h01h12+h12h01) come unchanged from uniform_alternating_b2_fixture/b2_blocks.txt, hash1e63ba284062733ec459fd0f2125874b561b407ef7d722897f1923336ff58581. The physical periodic L4/L6 fixture and signed convolution tests are separately frozen. The wrapper includes the unchanged matrix helpers from fixture.cpp, hashafaf61d76e1de0dceae377b0c61923bf3d2facf11f85a3915888a19707ad5214, with its main renamed and never run.

Let K=[[T,O],[0,−T]], and let P29,R29 denote its top diagonal and upper-right blocks at power29. Set P30=P29*T. In each difference-charge block,

    N=Tr(P30*T²), H=32Tr(P30*O),
    B²=32[Tr(P30*U)−Tr(P29*V)+Tr(R29*O)].

Summing over block sides1,8,32,80,136,162,136,80,32,8,1 gives the exact integer norm, total energy and staggered second moment in pilot.out. They are independently summed from the11 checkpoints by certify_scalar.py. Norm and H agree exactly with uniform_gap_0248_all_sizes_review/anchors.out, hash70562d55010e46b5fea6aeb10609d846145c263dffe88fc8236cd5f4b8c088b5. This mandatory comparison passes before accepting the new observable. No3^32 Hilbert vector or dense676×676 transfer is formed.

    q=<B²>/b²=.01507219528810355...,

where the exact rational is recorded in scalar_result.json. It lies in[0,1]. The saved adjacent contributions also reject the correctly named omission mutation B²+32*sum(adjacent), which removes the existing negative adjacent term. The older fixture's bad[4] instead doubles that subtraction; its historical label error does not alter its actual direct equalities or this formula.

## Finite Gibbs bounds and energy-only fidelity

Use beta=49/4 and the common energy shift aL with a=700741/500000. The original accepted physical32 certificate supplies trace upper Q and purity lower C. Let mu=H/N+32a, E_lo=−63/10000, delta=21/100 and w=(1+sqrt(2C−1))/2. The scalar checker reconstructs all these from the original data and proves with outward rational arithmetic

    exp(−beta E_lo)>Q,
    w−exp(beta delta)(1−w)>0.

Thus E0'>=E_lo, the finite32 ground is unique with gap>=delta, and its Gibbs weight is at least w. This is a finite-size gap used only for fidelity, not a new all-size .21 claim. The actual trial shift mu exactly matches the accepted certificate. The spectral inequality yields ground fidelity

    F>=f=1−(mu−E_lo)/delta≈.9753351376444873.

No energy variance or residual assumption is used.

For any effect0<=O<=I, trial expectation q and ground expectation alpha, Cauchy applied separately to sqrt(O) and sqrt(I−O) gives

    sqrt(F)<=sqrt(q alpha)+sqrt((1−q)(1−alpha)).

When f>q, its angle constraint implies alpha<=[sqrt(fq)+sqrt((1−f)(1−q))]²; otherwise use1. Both roots are rounded upward at120 decimal places. Here alpha<=.07678875791653625... . Bounding all excited expectations by1 gives

    kappa32=Tr(rho_uniform B²)/48²
       <=1−w+w alpha<=.13527650801543895...<17/125=.136.

All fractions and strict margins are saved. The rational exponential uses a120-term positive Taylor sum after reducing the argument below1/16 and a geometric remainder, followed by outward squaring; negative arguments use reciprocal endpoints. Square-root endpoints are verified by squaring.

One-site translation makes the actual uniform Gibbs spectral distribution of B symmetric. Golden–Thompson and the pointwise chord bound therefore allow the future seed comparison

    1<=Z_eta,32(beta)/Z_0,32(beta)
      <=1+(17/125)[cosh(48 beta eta)−1].

This package does not perform the all-size perturbed bootstrap or claim a new interval.

## Authorized correction and budget ledger

The historical uniform_alternating_b2_32_companion wrapper used unsafe textual numeric substitution. A requested62→30 replacement accidentally turned the block side162 into130. The identity guard stopped at the central block before any accepted32 result. Its five partial checkpoints, source, logs and FAILURE.json are retained and pinned by INPUT_SHA256.json. Failed physical child charge:2.223153CPU seconds. Failed-wrapper compile charge:8.624353CPU seconds.

Root explicitly authorized the dimension correction and one guarded retry in this new folder, with remaining aggregate numerical allowance27.776847CPU seconds, child<=25, parent reserve1,256MiB CPU4 and90-second external wall watchdog. The new source uses LENGTH=32, CONVOLUTION_POWER=LENGTH−3, BNORM=3*LENGTH/2, and a fixed unchanged block array. WRAPPER_DIFF.txt lists all wrapper changes; WRAPPER_AUDIT.json records the unchanged shared kernel and dimension162. There was no further numerical retry.

Successful child:7.643177 user+.100999 system=7.744176CPU seconds; wall7.827237444seconds; peak25436KiB. Cumulative numerical child charge=9.967329CPU seconds. Conservatively allowing one full CPU second for each of the two parent launchers and one for the scalar gate gives<=12.967329, below the original30-second aggregate. The scalar result itself records its measured small CPU cost.

Corrected compilation:6.933501 user+1.728498 system=8.661999CPU seconds; peak204640KiB. Both compiles total17.286352CPU seconds; adding their two full parent reserves gives<=19.286352, within the original separate30-second compilation allowance. The corrected compile child was capped at18CPU/512MiB. Parent limits are lowered only after fork, avoiding inheritance of a256MiB hard limit into the512MiB compiler.

Production verifies sole CPU4 affinity,25CPU hard limit,256MiB hard address limit, default and unblocked SIGXCPU and parent-death SIGKILL after exec. Its external wall watchdog did not fire. Checkpoint and output paths are exclusive. Reproduction requires a fresh directory and separately authorized physical budget. Previous fixture,64 pilot, accepted structural and interval seals, and root documents remain unchanged.
