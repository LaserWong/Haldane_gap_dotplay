# Chain certificate audit, 2026-10-10

Independent reconstruction passed for the saved spin-one alternating-chain certificates at $g=0.1,0.125,0.15$.
The short-size bridge at $g=0.15$ is now closed without new diagonalization.

The strongest independently verified bounds are

- $g=0.1$, every integer $M\geq2$, gap at least 0.118954972866
- $g=0.125$, every integer $M\geq2$, gap at least 0.068202652189
- $g=0.15$, every integer $M\geq2$, gap at least 0.017013326349

Here $M$ is the number of two-spin cells, the strong coupling is one, and the boundary is periodic.
Each statement includes uniqueness of the ground state.

Read [the proof](CHAIN_CERTIFICATE_PROOF.md) for the Hamiltonian, whole-spectrum completeness argument, independent audit method, signed-transfer interpolation lemma, and exact all-size bridge.

Run `verify_chain.py` from any working directory to rebuild the audit JSON files and `summary.json`.
Use `PYTHONDONTWRITEBYTECODE=1` and single-thread BLAS as shown in the proof.
The verifier reads the historical trial artifacts without changing them.
The default run checks all saved seed temperatures, including rejected seeds.
No project source module or eigensolver is imported.

`summary.json` records runtimes and resources.
`audit_run.log` is the final replay log.
The four `*_independent_audit.json` files contain full exact local LDL pivots, full-spectrum bin counts, source hashes, scalar checks, and exact rational bridge inputs.

The new all-size statement at $g=0.15$ follows from a finite-window interpolation estimate before the final small-defect bootstrap stage.
At depth four this yields a gap of at least 0.019906846147 for $M=8\ldots16$, while the exact local comparison gives at least 0.065980249445 for $M=2\ldots7$.
Both exceed the existing large-size gap 0.017013326349.

The audit is complete.
Further coupling scans or trial optimization are separate research tasks.
