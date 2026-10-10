# Stage10 visual QA

Reviewed 2026-10-10 18:03 America/New_York (EDT) / 22:03 UTC.

All six PNG figures and all six PDFs (independently rasterized with Poppler) were visually inspected. Titles, axis labels, legends, plotted endpoints, annotations and footnotes remain readable and inside their canvases, without overlap or clipping.

- certified_bounds: g=.10 appears at .038976038275; the uniform bar reaches .10 with bound .001945771244. Chain points end at .225; no .25 gap or excluded-branch point appears. Separate model scales and no-interpolation caveat are explicit.
- ordinary_interval_pieces: all 66 closed pieces, new [.09,.10] coverage, and whole-union minimum are visible. Ground-only versus odd-band colors retain their stated meaning.
- trial_space_counts: physical dimensions 2^32/2^64/2^128, ground searches 11/43/43, total trial counts 59/139/43, and retained counts 49/97/1 are distinct and legible. The largest numerator remains one term; 43 is its search dimension.
- aklt_reference_scope: separate projector proof, L>=5 gap and L>=3 uniqueness are explicit.
- recipe_upper_caps: fixed-recipe caps are explicitly separated from physical-purity and gap bounds.
- mps_recipe_windows: historical core and accepted longitudinal/momentum screens remain necessary-condition windows only, without current-operator results or successful-startup claims.

The 12 PNG/PDF files also pass byte-identical rerendering in a separate temporary directory, recorded in render_reproducibility.json. Rasterized PDF QA files were temporary and are not scientific sources. Exact source checks, all 212 preserved stage9 rows, all 56 preserved old pieces, decimal floors and 56 deliberate corruption rejections pass. These checks do not constitute a new physical-proof audit.
