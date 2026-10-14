# Gap workflow agent harness

Read [README.md](README.md), [INPUT.md](INPUT.md), the exact user request, and the latest run checkpoint before acting. Honor the current scope, deadline, and pause state. These instructions do not grant new permissions, start a scheduler, or authorize remote publication.

## Roles and sequence

- Model agent: validate Hamiltonian, normalization, spin, geometry, boundary multiplicity, and sector. Record physical size and full versus working dimensions.
- Resource agent: admit dimensions and conservative memory before basis allocation. Keep timing forecasts explicitly calibrated or unknown. Propose a small bounded pilot instead of silently launching large full ED.
- Spectrum agent: run partial low-energy candidates within the supplied limits. Record trial rank and residuals. Treat solver convergence as numerical evidence only.
- Certificate agent: construct rational input from source coefficients and verify full-working-space spectral counts or supported tail bounds. Start with unknown ground multiplicity; do not require the user to supply g or an exact ground energy. Infer exact degeneracy only from a valid exact certificate, such as one distinct Sturm-counted bottom root or exhaustive rank-two Kramers coverage. Never rationalize a floating Hamiltonian into a purported exact proof.
- Bootstrap agent: identify the actual geometric theorem, normalization, patch overlap constants, and certified seed requirements. Scalar inequality success alone does not establish these hypotheses.
- Independent reviewer: check model construction and certificate artifacts. Label replay of the same algorithm honestly. Distinguish independent numerical checking from independent exact proof verification.
- Reporter: save the result, diagnostics, report and checkpoint. State the strongest warranted finite-size or conditional result. Never inflate it to a uniform-family theorem.

## Multiplicity and scope

Keep the bottom-cluster rank separate from ground multiplicity. Numerical near-degeneracy is not exact degeneracy. If internal equality is unproved, report cluster width and complementary separation, leave the true ground-gap field unknown, and do not call the cluster separation a ground-state excitation gap. A rank-four Kramers-compatible cluster does not establish fourfold degeneracy, and a whole-space cluster has no excitation complement. Record root-count budgets and missing optional dependencies honestly.

Full-model sector inference requires every sector and exact dimension coverage; one sector supports only a sector statement. A finite certificate does not establish a thermodynamic or uniform-family gap. Named analytic-family routes require their particular theorem hypotheses. For quantum Ising, distinguish the scalar bootstrap scope from the all-size bridge and verify pinned reviewed proof sources before accepting the composed physical result. Do not silently substitute an analytic bound for a failed seed search.

## If a target fails

Separate poor trial approximation, unresolved complement/tail completeness, insufficient geometric seed, unsupported theorem, and resource failure. Raise k only to address trial approximation. Raising k does not enlarge the physical seed. Estimate physical seed requirements only from a stated applicable criterion and data. Label a tested sufficient size as sufficient, and a forecast as a forecast. Never infer physical gaplessness or universal impossibility from computational or certificate failure.

For multi-size work, define each model explicitly, plan its Hilbert and working dimensions before calculation, preserve measured calibration, and check the budget at every step. Do not launch an unbounded search for a minimal seed.

## Recovery

Inspect input.json and checkpoint.json. A terminal --resume must verify fingerprints and artifact hashes before reuse. Preserve interrupted artifacts. Use a new directory for a rerun. Do not retry a costly operation without inspecting its prior logs. Save a precise next action and any missing authorization or theorem hypothesis. Ordinary local code and data work must remain within the user's granted scope. Installation, deletion, credentials, permission changes, uploads and remote publication require their separate applicable authorization.
