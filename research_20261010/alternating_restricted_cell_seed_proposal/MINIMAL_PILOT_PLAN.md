# Minimal nonperturbative g=9/10 pilot: design only, not launched

2026-10-11 00:08 EDT / 04:08 UTC.

## Decision now

Do not launch an alternating g=.9 thermal campaign. The tested ten-trace recipe fails even at the easier uniform feasibility point. First resolve one of: a stronger integral-spectrum/model-specific scalar bound, a sufficiently improved trial numerator, or a precise demonstrated need and benefit for an extra cell moment. L14 and L16 are not implicitly approved or presumed affordable.

## Gate A: mathematical and resource readiness, no physical work

1. Independently review the existing restricted-cell construction and its continuous-moment obstruction. Correct any proof issue without importing physical odd-length moments.
2. Select one concrete improvement and a success margin. For example, cell17 at the retained S endpoint closes .005 if T≥.835. Use the exact relation between denominator Q and shifted trial energy; do not insist on the sufficient Q-only target if the numerator improves.
3. If considering cellm7, first derive the needed interval using the shifted Hankel/Schur-complement threshold in ANALYTIC_ASSESSMENT.md. Do not compute L14 merely because it is the next moment. If m8 is actually needed, stop and present that cost separately.
4. Repair and independently test the resource guard before any additional computation. A configured RLIMIT_CPU is insufficient in this environment. Require verified post-exec limits, external CPU accounting for the process group/descendants where supported, aggregate reservations, a conservative stop margin, and immediate stop on failed observation. The present wrapper is diagnostic evidence, not a production guard.

Gate outcome: a reviewed seed recipe that succeeds using the declared inputs at g=1, or an explicit justified replacement. Stop if this is not established.

## Gate B: optional MPS-only exploratory optimization

Only with separate approval after the guard issue is resolved:

- Fix g=9/10 exactly, strong-bond coefficient1 and period-two tensors A^s,B^s with bond dimension26. Initialize from the existing uniform D26 tensor duplicated over a cell; optional symmetry-preserving two-site perturbations remain candidates, not physical evidence.
- Keep the full two-site variational ansatz explicit. No claim that26 is a Hilbert-space or trial-space dimension: one contracted MPS is one vector; two tensors have3 components each, with26×26 auxiliary matrices before gauge/symmetry constraints.
- A bounded exploratory budget could be300 CPU seconds, one worker,256 MiB, wall deadline before the user's2026-10-14 00:00 UTC stop. This is a proposed ceiling, not authorization or a promise of convergence. Save the initial and best tensors, optimizer loss/gradient or convergence diagnostics, seeds, gauge, precision and all timings. Stop at the ceiling if no meaningful gain.
- Rationalize a selected candidate, then prepare a separate contraction budget and proof gate. Exact positive norms and total strong/weak bond energy numerators must be obtained at the chosen own anchor lengths, initially only physical68 for cell17 if Gate A selects it. Do not automatically run60 and64 as well.
- Compare the achieved numerator against the recipe's actual target. An improvement in floating energy is not an exact anchor or a gap certificate. If an available ground-energy lower bound proves the numerator target impossible at fixed Q, stop this route.

This MPS-only step is optional information gathering; it does not authorize subsequent heat traces and should not be represented as proof that the full seed will succeed.

## Gate C: tiny exact heat-kernel validation, not a full campaign

Only if Gates A/B justify a genuine seed candidate:

- Fix ONE temperature and ONE common cell shift for all lengths. A concrete starting candidate at g=.9 is c=(1+g)/2=19/20, beta=(49/4)/c=245/19 and cell shift q=2ca=19a/10. This is merely a conditioned nonperturbative input choice, not reuse of a uniform perturbation bound. The actual alternating Hamiltonian must be used in every matrix.
- Validate both I and the same spatial pi seam at physicalL4 andL6, with an independently generated exact small matrix. At g=.9, one-site translation is not a valid orbit symmetry; only verified period-two/spin symmetries may be used. The pi-seam handling and orbit multiplicities require independent checks.
- Propose a strict300 CPU-second/256-MiB one-worker fixture allowance, separate from MPS work and requiring approval. This cap is a stop rule, not a runtime forecast. Record integer bit widths, remainder bounds, dimensions, nonzeros, actual CPU and peak RSS. If a full tiny case cannot complete within its allocation, stop and report.
- No L8,L10,L12 production until a conservative benchmark projection using the actual period-two kernel fits an approved aggregate budget and deadline. Do not assume the old uniform campaign timing transfers unchanged.

## Gate D: smallest full restricted-input set

If all earlier gates pass and a new campaign is explicitly approved, the original recipe requires exactly ten cases:

    physical lengths4,6,8,10,12 × seams I,P.

The four accepted tiny fixtures can count toward these ten only if all production parameters and independent validation match. This set yields cellm2,...,m6. No physical odd lengths, arbitrary reused uniform traces, or unrequested temperature grid are included.

If the replacement recipe demonstrates that an additional L14 pair is necessary, that is a different cost proposal, not part of this ten-case pilot. PhysicalL14/16 brute-trace costs may be prohibitive: obtain a credible sparse/symmetry-reduced projection and memory plan before permission. Do not extrapolate success from a low-order scalar moment requirement.

## Gate E: certification scope after a successful seed

- Exact character projection, positive support/moment bounds, own-length numerator, positive-window recurrence and tail closure must all be independently checked.
- A cell17 tail only covers M≥17. The finite cells2,...,16 need separate nonperturbative certification at g=.9. The tiny near-g1 Weyl bridge cannot cover eta=(1−g)/(1+g)=1/19. That finite bridge is additional work, not an automatic consequence of the new tail seed.
- Report a seed or tail result at its true scope first. Claim every M≥2 only after the finite bridge is complete. Physical lengths remain L=2M.
- Preserve all old near-uniform and weak-dimer results; no interpolation across the currently unproved intermediate coupling range.

Stopping conditions: any failed mathematical gate, unattainable numerator or moment threshold, absent reviewed resource guard, exceeded allocated resource/deadline, or unmet authorization. No retries or larger lengths are automatic.
