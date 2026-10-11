# B² local-insertion and small-chain fixture gate

2026-10-11 03:56 UTC. Producer fixture PASS; independent physical review pending. This is not a physical32/64 contraction or a new robustness certificate. Existing interval/structural seals are unchanged.

## Authorized work and result

The parent authorized an aggregate15CPU-second/256MiB fixture gate on CPU4, with external wall watchdog and independent wait4 accounting; compilation was separately allowed30CPU seconds/512MiB. The first numerical run passed without a failed retry.

The program rebuilds the exact D26 matrices from the independently reviewed integer parameters, reconstructs T and E_h and checks EVERY entry against audit/mps/mps_blocks.txt. It then constructs the full physical local insertions U=E_(h²) and V=E_(h01h12+h12h01). No local physical sector is omitted: the operators are9×9 and27×27 respectively. The two-site h polynomial and all local Hermiticity checks pass.

The local h preserves physical Sz. Its square and adjacent anticommutator therefore preserve total physical Sz. Together with the exact A_s virtual charge selection rule, this proves all four insertions preserve the charge difference, so the eleven inherited blocks are complete, not a trial-space restriction. Their dimensions are1,8,32,80,136,162,136,80,32,8,1.

## Formula and periodic overlaps

For every even physical L>=4, with N_L=Tr(T^L),

    <B_L²> = L/N_L [Tr(U T^(L−2)) − Tr(V T^(L−3))
      + sum_(r=2)^(L−2)(−1)^r Tr(E_h T^(r−2) E_h T^(L−r−2))].

The L identical rows of the bond-pair sum account for one same bond, two adjacent bonds, and all disjoint bonds, including the periodic closing bond. The Hermitian V combines both adjacent product orders. Thus the formula is valid without a reflection assumption. The norm and total-energy conventions match the original periodic D26 contraction.

For K=[[T,E_h],[0,−T]], its upper-right block at N=L−3 is

    R_N=sum_(j=0)^(N−1) T^j E_h (−T)^(N−1−j).

Since N is odd, this is exactly the alternating disjoint sum, with j=r−2. The multiplication rule R_(a+b)=T^a R_b+R_a(−T)^b is used with all intermediate signs retained. The off-diagonal block is not treated as a power of a self-adjoint physical transfer.

## Direct physical checks

The direct route constructs complete periodic MPS amplitudes, applies the full physical H and B in the3^L product basis with the closing bond present, and evaluates norms of Hpsi andBpsi. It does not use transfer insertions for those reference values. The transfer route is independently assembled from T,E_h,U,V and the binary/displacement convolution.

Exact D26 results:

- L4, dimension81: N=22975205960525898253776; H=-137851234864097615402880; H² numerator=827107409184585692417280; B² numerator=153212296859239674163968.
- L6, dimension729: N=795377896228728091610809845163632; H=-6854013196214322159921037103475264; H² numerator=59063502830735621473823858042361600; B² numerator=6842697357336864112242332867653632.

Every listed integer agrees between the two methods. The staggered mean is exactly zero at both lengths. A separate deterministic noncommuting real D2 tensor family passes the same full L4/L6 comparisons; its exact integers are in fixture.out. Full physical variances are nonnegative.

Twenty-six abstract block tests compare signed block recurrences with powers of the literal doubled block matrix for N=0,...,12 and both signs. These include even intermediate N and directly test the dangerous sign convention. The physical L6 case also compares the binary alternating result with an explicit displacement sum.

Six physical mutations are detected: extra L, omitted L, omitted norm division, wrong adjacent sign, omitted adjacent term, and omitted disjoint term. This records the actual six tests, not the eight initially suggested design mutations. The direct full physical checks independently include closing bonds, but a separate deliberate closing-bond-omission mutation was not run.

## Saved output and exact pins

b2_blocks.txt has SHA256 1e63ba284062733ec459fd0f2125874b561b407ef7d722897f1923336ff58581 and size2,781,490bytes. It begins with11, then for each sorted charge block contains charge and side, followed in order by the four integer matrices T,E_h,U,V. It is a complete local-insertion input, not a length64 result.

Principal input pins:

- Original T/E_h blocks:26da12458538967b97cb037059440d652d64593bf2044d7f5c99760444d683aa
- Independent D26 rebuild source:4e4e586dddb48b993c7d84186ddce777cfd7a6636e3f7238e28c7ec013b25b1a
- Accepted independent32-containing anchors:70562d55010e46b5fea6aeb10609d846145c263dffe88fc8236cd5f4b8c088b5
- Accepted independent64-containing anchors:217e4ba47ad3544f4f8ce384970cdc501c77a5916a7f5883a86cadeb42df1af2

All exact file paths/hashes are in INPUT_SHA256.json. The generator source is fixture.cpp; it contains no32/64 execution path.

## Observed resources and guards

Compilation: independent wait4 user4.681408CPU seconds plus system1.273614=5.955022 total, peak174632KiB, wall6.02847seconds. It was below the separately approved30CPU-second/512MiB cap.

Fixture: independent wait4 user2.447024CPU seconds plus system.186390=2.633414 total, peak22288KiB, wall2.65474498seconds. No watchdog fired; exit0. The child hard CPU limit was14seconds and parent hard limit1second, leaving an aggregate15second ceiling. Both child and launcher were bounded to256MiB, and the child post-exec verified sole CPU4 affinity, default/unblocked SIGXCPU and parent-death SIGKILL. The launcher uses process-group cleanup and refuses a prior attempt's output paths, preventing automatic retry.

The separate scalar resource projection cost.162310988CPU seconds/12416KiB. With the fixture launcher's maximum1CPU-second reservation, the fixture plus projection is conservatively charged4CPU seconds, below the authorized15. No32/64 physical contraction occurred.

## Proposed separate64-site B² pilot

The new local-block row-norm bounds certify ||T||_infinity<2^21 across every block. Thus ||T^64||_infinity<2^1344. The convolution bound gives ||R61||_infinity<2^1305. These are local-data bounds, not execution of those powers.

A left-to-right binary implementation needs at most27 dense products for the combined T/R61 block recursion and2 further products to obtain T62/T64 for the energy, norm and local-overlap traces: at most29 products per charge block. Stream one charge block at a time. Do not allocate the dense676×676 or1352×1352 matrices. Target at most ten live162×162 GMP buffers; the verified bit bounds give a comfortable sub100MiB design estimate, still guarded by256MiB.

The existing ordinary D26 anchor costs and this fixture suggest20–40CPU seconds for a64-site B²-only pilot, but that is a projection, not a benchmark guarantee. The proposed next cap is aggregate60CPU seconds/256MiB on CPU4, child59seconds plus parent1second, external180-second wall watchdog, checkpoint per charge block and no automatic retry. Compilation would require its own explicitly charged cap. No production authorization is inferred from this document.

At L64 first reproduce the accepted N0 and total H0 exactly, then form q64=B²/(N0*96²). Only this q is new. The established scalar design gives a useful target q64<=.05; q64 up to.1 can still materially improve the trace bound. Do not start L32 or H² production until the64 result, measured cost and remaining scope are reviewed. The retained trial remains one D26 vector.
