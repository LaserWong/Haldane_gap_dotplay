# Visual quality assurance

Inspection completed 2026-10-10 19:20 UTC / 15:20 EDT.

All three final PNG figures were opened and visually inspected. The dimension PDF was also rendered independently with Poppler and inspected. The main-bound PDF is one unencrypted vector page, with fonts available and no JavaScript.

- Certified bounds: three separate model panels and vertical scales are legible. The chain's close g=.1615/.1625 points have separate label callouts. The ordinary-bilayer bar explicitly reaches .078, while g=.08 is an isolated point. No lines join isolated points. The final legend says “Finite-size bridge with audited inputs”. The older FF evidence distinction remains visible.
- Interval pieces: all 31 closed pieces are shown, including the exact .078 endpoint tick. Segment endpoints remain closed. The whole-union minimum is visually separate. The nonmonotone jump in certificate values near .07 is not connected by a slope and is explicitly qualified as certificate variation.
- Dimensions: full physical counts, original searches, implicit filtered upper dimensions, numerator rank and complete-band count are separate. Inequality symbols, q≤6, existing G/K/J dependence and interval-extension 11/29/≤30 are readable. No MPS bond dimension is inferred. No axis, legend, caption or annotation is clipped.
- Exact table values and plotted selection were checked against the recorded source pointers. Final bitmap and vector renders reproduced byte for byte in a separate temporary directory. Integrity tests reject seven deliberately corrupted data records.

## Inspected PNG hashes

- `certified_bounds.png`: `2eaec9f921496be1262a87042551f4e092f448b0a1f38ab64e557dbd62c57fa9`
- `ordinary_interval_pieces.png`: `ccaf55475034f291f91fabaa664e5c02a9d0a5b5dc402f5d41250b0cd2f5b60a`
- `trial_space_counts.png`: `e23c291e0d54b2daf06747e9de468a78666290cd81e24f0a533536bbff72ae77`

The final render hashes for PNG and PDF are recorded in `render_reproducibility.json`. This inspection checks presentation and consistency, not an additional proof of the underlying theorems.
