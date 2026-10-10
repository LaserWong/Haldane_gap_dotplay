# Stage12 visual, scope and reproducibility QA

Reviewed 2026-10-10 18:48 America/New_York (EDT) / 22:48 UTC.

All11 figures /22 PNG-PDF exports are covered. Five changed/new PNGs were inspected directly; their PDFs were rasterized independently with Poppler and inspected. Six unchanged figure pairs are byte-identical to visually checked stage11. All titles, labels, annotations, legends and footnotes are readable without clipping or overlap.

- certified_bounds shows the improved .10 and five frontier points through .102, plus one current whole-union bar at .004499695659. Historical alternative rows remain in the data; weaker same-parameter points/union bars are not visually duplicated.
- ordinary_interval_pieces displays the current74-piece cover of [0,.102], exact closed endpoints and correct whole-union minimum. The66 stage11 pieces are preserved separately and are not mixed into a false148-piece cover.
- bilayer_frontier separates six point certificates from the independently proved [.10,.102] interval. The crowded .10/.1001 labels are vertically separated. Six-decimal point labels are rounded downward, explicitly stated; exact12-place values remain in data.
- uniform_gap_frontier includes the new .0038 for every integer L>=52, including odd lengths, and preserves the weaker .0025/L>=54 alternative in gray. No result below52 or minimum-seed claim is displayed.
- uniform_theorem_comparison clearly labels original even-length scopes and new all-integer scopes. Approximation signs distinguish original logarithmic bounds; ratios compare certified sufficient bounds, not physical gaps.
- trial_space_counts, aklt_reference_scope, recipe_upper_caps, mps_recipe_windows, chain_window_refinement and accepted_recipe_scope are byte-identical to stage11 and retain their prior visual QA.

All22 files rerender byte-identically in a separate temporary directory. All44 review/provenance manifests and2,846 sealed source-file hashes pass; all228 stage11 M/L>=2 rows, finite-range record, three previous uniform large-size records and66 old pieces remain unchanged. The102 deliberate corruptions are rejected, including interval holes, wrong fractions, frontier metadata drift, unproved domain promotion, n52 size relabeling, original-theorem scope and ratio overclaims. All43 relative README links resolve.

The inherited final transport map independently restores all18 evidence paths/nine contents into an empty temporary root, preserving original raw hashes, sizes, modes and idempotence. No producer/review raw bytes, original-source snapshots, licenses, previous snapshots or root/GitHub files are changed.

These checks establish source integrity, precise extraction scope and presentation quality; they do not repeat the expensive physical proof audits.
