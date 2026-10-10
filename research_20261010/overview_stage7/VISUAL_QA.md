# Stage7 visual QA

Inspected all four rendered PNGs on 2026-10-10, 17:14 EDT / 21:14 UTC. The main result plot was inspected again after its label refinement. This is visual inspection of the actual output pixels, not merely a source-code check.

- certified_bounds: all three thermal-bootstrap model panels are visible; new chain points reach .2, the ordinary isolated point reaches .085, and the entire ordinary interval ends at .085 with the exact uniform displayed bound. Marker/interval evidence types and the non-interpolation caveat remain legible. Sparse parameter labels use leader lines where needed; no text is clipped.
- ordinary_interval_pieces: all 49 closed pieces are drawn from exact data. Green ground-only pieces reach .082; the final nine orange pieces use complete smaller odd bands. The whole-union bound is a separate purple bar. The smallest intervals are intentionally short and are individually readable in the exact CSV/table.
- trial_space_counts: physical dimensions 2^32/2^64/2^128, original search 11/29/29, total final trial dimensions 59/125/≤30 and trace/numerator counts 49/97/1 are separate. The largest-patch panel distinguishes rank 1, search 29, filtered bound ≤30 and the separate 193-direction full-band route. Footer explicitly rejects a pipeline-wide maximum of 30. Axis labels, values and legend are not clipped or overlapping.
- aklt_reference_scope: the normalized projector Hamiltonian, periodic L≥5 gap, L≥3 uniqueness, omitted-state count, MPS bond D=2, one state and 81×81 local proof matrix are legible. It is prominently labeled a separately proved finite-size-projector reference, with the current thermal-transfer sufficiency failure stated.

The PNG and PDF pairs are produced from the same Matplotlib figures. Byte-identical rerender checks cover all eight files. Exact CSVs and source-pointer checks remain authoritative for numerical interpretation. No image-generation or edited screenshots are used.
