# Independent bosonic-tail review

Updated 2026-10-10 14:28 America/New_York (EDT) / 18:28 UTC.

The independent review verified the finite-sector pair-creation lemma, orthonormal physical embedding, period-two edge multiplicities, and all twelve frozen Jacobi tail certificates.

- Full proof and counting argument: [PROOF.md](PROOF.md)
- Exact acceptance summary: [results/summary.json](results/summary.json)
- Exact bin replay: [results/bin_replay.json](results/bin_replay.json)
- Complex and real Fock-sector checks: [results/fock_tests.json](results/fock_tests.json)
- Independent physical-spin checks: [results/physical_tests.json](results/physical_tests.json)
- Reproduction: `bash REPRODUCE.sh`

The input snapshot is fixed by `INPUT_SHA256.json`. No producer Python module is imported and no producer file is edited. The source package is the 18:23 UTC freeze, identified by SHA-256 `4bc8db06b3695b37f01dd12b63eb15476853b5dfe5d5bd772897e6d32d81a08e`.

The audit passed 34 exact Fock-sector checks, 10 exact physical creation-operator checks, and 11,436 positive rational LDL pivots across 12 bin files. Shapes are 4×4, 8×4, 8×8 at g=.03,.04,.05,.06. On 8×8 at g=.06, the certified λ_194(H+48) cutoff is a2=1.368913479949. The old occupancy-only cutoff is approximately 1.058964546252. This improves the whole-space spectral-tail input. A global gap certificate requires the remaining bootstrap argument.

The complete physical Hilbert dimensions are 4^16, 4^32, and 4^64. The number 193 on the largest shape is the number of ordered levels below the first omitted index 194, not the full Hilbert dimension or a newly diagonalized trial space.

The computation took about 38 seconds, used about 87 MiB peak RSS, and was pinned to one CPU with one BLAS thread and a 1.5 GiB address-space limit. Floating diagnostic values are labeled and play no role in exact acceptance. No remote state was changed.

The proposed stable quadratic-boson comparison remains outside this review.
