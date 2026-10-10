# Stage8 visual QA

Inspected all five PNG figures at readable display resolution and independently rasterized all five vector PDFs with Poppler. The final upper-cap y-axis label was shortened before the last render to keep it comfortably inside the canvas.

- `certified_bounds`: ordinary-bilayer isolated .09 point and the full [0,.09] interval are clearly separate. Chain points remain isolated. Three model panels have separately labeled scientific axes. No recipe failure is plotted at zero gap.
- `ordinary_interval_pieces`: all 56 exact closed pieces are represented; green ground-only and orange smaller-odd-band regimes are distinct, with the purple whole-union bound. Narrow pieces remain visible as short segments with endpoints. The source CSV retains all exact endpoints.
- `trial_space_counts`: full dimensions 2^32/2^64/2^128, used searches 11/29/43, total trial spaces 59/125/43 and retained trace/numerator counts 49/97/1 are separated. The exact 43-dimensional enlarged search is not confused with one retained state or an MPS bond dimension.
- `recipe_upper_caps`: dedicated upper-envelope axis and explicit captions prevent confusing recipe J-lower caps with physical-purity upper bounds or gap lower bounds. No minimum seed inference is drawn.
- `aklt_reference_scope`: simple scientific axes replace the earlier text-only panel. The bound begins at periodic L=5 and explicitly continues to all larger integer sizes; it is distinguished from thermal bootstrap.

Titles, axis labels, legends, captions and numeric annotations are legible, without overlaps or clipping. White backgrounds, restrained colors and ordinary scientific axes are used. PNG/PDF byte-identical independent rerender results are recorded separately in `render_reproducibility.json`.
