# Measured pilots and resource forecasts

Eleven noncommuting finite spin models were tested with four low Ritz pairs per model. No full spectrum is required by these pilots. The spectra are floating-point diagnostics and do not certify a thermodynamic gap. The first spacing can vanish because of a ground multiplet.

The runs used periodic positive-direction multigraph bonds. Length-two directions retain parallel bonds. A single measured matrix-vector operation calibrates each forecast, so timings are approximate. The forecasts assume 200 operations. Solver iteration counts, overheads, and convergence can differ.

| Pilot | Full dimension | Partial solve (s) | Largest residual |
| --- | ---: | ---: | ---: |
| spin0.5_chain_4 | 16 | 0.0031965 | 8.15e-16 |
| spin0.5_chain_6 | 64 | 0.027807 | 4.57e-15 |
| spin0.5_chain_8 | 256 | 0.22886 | 1.04e-14 |
| spin0.5_chain_10 | 1024 | 1.3953 | 3.07e-11 |
| spin1_chain_2 | 9 | 0.00070447 | 2.44e-15 |
| spin1_chain_4 | 81 | 0.027854 | 5.27e-15 |
| spin1_chain_6 | 729 | 0.69922 | 7.91e-13 |
| half_lattice_2x2 | 16 | 0.00488 | 1.48e-15 |
| half_lattice_2x3 | 64 | 0.03744 | 4.22e-15 |
| half_lattice_3x3 | 512 | 1.2179 | 3.91e-11 |
| half_lattice_2x2x2 | 256 | 0.43125 | 7.1e-10 |

The resource forecast file compares full-space and fixed-magnetization calculations at larger sizes. A smaller symmetry sector needs independent coverage of omitted sectors before any full-model gap claim. The Python matrix-free implementation stores a basis and lookup table, so its memory is still exponential. These forecasts do not identify the minimum physical bootstrap seed.

For comparison, the graph-state benchmark uses an exact combinatorial tail and zero computed eigenpairs. Its retained ground-state rank is one. This illustrates why a Hilbert-space dimension alone cannot predict the difficulty of a proof.
