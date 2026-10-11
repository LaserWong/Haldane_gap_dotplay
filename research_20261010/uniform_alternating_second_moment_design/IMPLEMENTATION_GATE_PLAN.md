# Proposed first B² implementation/fixture gate

2026-10-11 03:46 UTC. DESIGN ONLY. No physical computation was launched. This plan requests a separate bounded fixture gate; the earlier scalar-only allowance is not treated as permission for production contractions.

## Requested first gate

One Python exact-integer process, hard15CPU seconds total and256MiB address space, one allowed CPU affinity, independent60-second wall watchdog, no automatic retry. Its scope is local-operator construction plus tiny fixtures only. No physical32/64 contraction, numerical optimization, new thermal trace, or production H² job.

Using Python for this first gate avoids an unbudgeted compiler child process. Source can be written and inspected before the run. If the fixture process hits any guard, stop and report the incomplete stage with the actual wait4 process-CPU/RSS accounting. Do not increase the cap or switch algorithms without a new decision.

## Exact convention

For real site tensors A_s, use transfer insertion

    E_O=sum_(bra s,ket t) O_(s,t) A_(t_1)...A_(t_k) tensor A_(s_1)...A_(s_k),

or the globally exchanged bra/ket convention already used by the pinned T/E_h builder. The ordering must be fixed and verified against physical amplitudes; local operator Hermiticity does not license swapping h01h12 with h12h01 inside an unfinished derivation.

Build the integer two-spin Heisenberg h in the physical Sz basis, then construct

    U=E_(h²),
    V=E_(h01h12+h12h01).

The Hermitian V avoids relying on an implicit reversal of an overlapping product. With N_L=Tr(T^L), for even L>=4,

    <B_L²> = L/N_L * [Tr(U T^(L−2)) − Tr(V T^(L−3))
      + sum_(r=2)^(L−2) (−1)^r Tr(E_h T^(r−2) E_h T^(L−r−2))].

The three groups are respectively same-bond, the two adjacent-bond orderings, and every disjoint periodic bond pair. There is no uncounted closing-bond term. Multiplication by L occurs exactly once, and N_L is the norm of the same length-L periodic trial.

For the parent's proposed block choice K=[[T,E_h],[0,−T]], let its upper-right block at powerN be R_N. Then

    R_N=sum_(j=0)^(N−1) T^j E_h (−T)^(N−1−j).

At N=L−3, N is odd and N−1 is even, so the coefficient is (−1)^j, exactly the desired disjoint sum with j=r−2. Thus the disjoint term is Tr(R_(L−3) E_h). Intermediate powers must retain the full signed block recursion; replacing their signs by the final odd-N sign would be wrong.

Store blocks rather than the doubled dense matrix. For K^a having diagonal blocks T^a, (−T)^a and upper R_a,

    R_(a+b)=T^a R_b + R_a (−T)^b.

Binary powering therefore requires ordinary T powers and at most two additional block multiplications per composition. At the final oddN it agrees with the alternate diagonal convention [[−T,E_h],[0,T]], but those conventions must not be mixed at intermediate even powers.

The optional later H² formula has +Tr(V T^(L−3)) and the all-positive disjoint convolution. It is not needed for the first fidelity improvement, and is outside this first production scope.

## Fixture matrix

1. Reconstruct A_s from the independently reviewed printed-integer formulas. Rebuild T and E_h and require byte-for-byte equality with pinned audit/mps/mps_blocks.txt before trusting U,V. Reuse no producer output for U,V.
2. Check the9×9 local h: real symmetry, standard eigenvalue polynomial (h+2I)(h+I)(h−I)=0, h² product, and the27×27 adjacent anticommutator. These local checks are small exact arithmetic, not ED.
3. Deterministic small real D=2 tensors with three physical spin-one labels: direct periodic L4 andL6 amplitudes, exact full-space Hpsi andBpsi action, and norms. Compare direct ||Bpsi||² and||Hpsi||² to the overlap-separated formulas and BOTH explicit displacement and binary-convolution evaluations. Include several noncommuting tensor choices to avoid accidental sign cancellations.
4. A physical D26 L4 direct amplitude fixture: compare norm, total first moment and B² against the new insertion formula. Do not silently replace it by only a D=2 fixture. A full D26 L6 fixture is optional only if an explicit remaining-time gate permits it; it is not required to claim the planned gate complete.
5. Check exact <psi,Bpsi>=0 for each one-site-translation-invariant even-ring trial, nonnegative B² and variance, and invariance under moving the chosen staggered origin (B->−B).
6. Adversarially confirm that the fixture suite rejects: missing factorL; double factorL; missing norm division; wrong sign on V; omission/double counting of the closing bond; treating adjacent bonds as disjoint; wrong intermediate block-power sign; and omission of the midpoint/disjoint pair in L4. Log which fixture distinguishes each mutation.

The direct physical full dimensions are81 atL4 and729 atL6. The production D26 bond dimension and retained linear span remain26 and1. No tiny fixture establishes a production32/64 number; it only validates conventions and algorithms.

## Memory plan

The accepted charge-difference sectors have sides1,8,32,80,136,162,136,80,32,8,1. T,E_h,U,V preserve the difference charge because each physical observable preserves total Sz. Generate each sector entrywise, and release temporary two-/three-site tensor products after use. Do not allocate a dense676×676 four-insertion stack or a dense1352×1352 block power.

The first fixture gate uses only local26×26 products, the tiny physical vectors and streamed transfer blocks, comfortably below a256MiB hard cap by design, subject to measured validation.

For a later GMP production kernel, stream one charge block at a time and retain at most a small fixed set of current powers/accumulators. AtL64 a deliberately coarse entry bound from |A_s(i,j)|<=1156 places the relevant integer sizes below roughly2100bits. Even ten162×162 GMP buffers at approximately320bytes/entry are about80MiB, with room for local insertions and allocator overhead under256MiB. This is a conservative design estimate, not a measured peak. The fixture should report allocation dimensions; the later production guard still enforces the memory limit.

## Runtime and next decision

A previous independent D26 T/E_h reconstruction took1.165860534CPU seconds and12032KiB. A previous physical26..33 norm/first-moment batch took7.25026CPU seconds and15824KiB; these are reference costs, not a benchmark for the new two-insertion convolution.

The binary algorithm replaces O(L) separate dense contractions by O(log L) compositions. U/V construction and GMP bit growth remain additional costs. The fixture must report per-stage CPU, operation counts, maximum block side, integer bit lengths and peak RSS before any production projection is accepted.

If all fixtures pass, propose a separately authorized physical64 B²-only pilot, with a hard60CPU-second/256MiB limit, one CPU, wall watchdog and checkpoint after each charge block. Compiler setup, if needed, needs a separately explicit charged cap; it is not silently excluded from the budget. Do not start32 until64 passes and a projected remaining budget is approved. No automatic retry after a guard exit.

The quantitative decision gate is clear: q64=<B64²>/(96²)<=.05 would imply kappa64<=.245218 using ONLY the accepted energy-based fidelity. q32<=.05 subsequently implies kappa32<=.199073. These thresholds make the proposed fixture work worthwhile. If q64 is too large to improve kappa materially, pause rather than starting H² automatically. H² is a separately reviewed optional follow-on if improving fidelity is actually the bottleneck.

## Exact inputs

IMPLEMENTATION_INPUT_SHA256.json lists all exact byte hashes. The principal pins are:

- audit/mps/mps_blocks.txt:26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa
- audit/mps/build_mps.py:693ded40630e851fda40986460b841bcfe3e48cf5ace665997f923ec7737ffdb
- independent D26 rebuild source:4e4e586dddb48b993c7d84186ddce777cfd7a6636e3f7238e28c7ec013b25b1a
- accepted32-containing independent anchor file:70562d55010e46b5fea6aeb10609d846145c263dffe88fc8236cd5f4b8c088b5
- accepted64-containing independent anchor file:217e4ba47ad3544f4f8ce384970cdc501c77a5916a7f5883a86cadeb42df1af2

The accepted uniform review manifests5407745b... and54401c08... and positive-cell robustness reviewe80440ac... are also pinned. Local file paths identify project artifacts, not new authorizations to run their scripts. The existing rebuild scripts have write side effects and must not be executed in their sealed directories.
