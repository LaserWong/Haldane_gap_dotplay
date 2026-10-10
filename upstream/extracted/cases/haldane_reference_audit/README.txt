INDEPENDENT READ-THROUGH AND COMPUTATIONAL AUDIT
Source: uploaded paper.pdf, The periodic spin-one Haldane gap, dated September 24, 2026.

This folder is NOT a formal proof certificate for the full manuscript.

Completed computations:
1. Appendix C: independently reconstructed all three 26x26 integer MPS matrices
   from the printed entry rules, built T and O, checked all difference blocks,
   and recomputed both N=72 and N=120 contractions using arbitrary-precision GMP.
   Both printed C.8 energy intervals and the strict variational margins passed.
2. Nine independently rebuilt heat-kernel enclosures, using every physical
   column (not the paper's symmetry representatives or recorded totals):
   Appendix A: n=6, twists I/P/C; Appendix B: n=4,5,6, twists I/P.
3. All 27 scalar trace-enclosure calculations, conditional on the manuscript's
   printed large integer totals. This does NOT independently regenerate all
   27 physical matrix calculations.
4. The scalar inequalities for both initializations and the six-step bootstrap.

Remaining physical heat-kernel computations not independently regenerated:
Appendix A: n=8,10 with all three twists (6 inputs).
Appendix B: n=7,...,12 with twists I/P (12 inputs).
The weaker, still uniform positive gap requires only the first initialization;
its remaining independent matrix recomputations are the six Appendix A inputs.

Run requirements: Python 3, NumPy, SciPy; g++ with GMP development libraries.

Commands:
python build_mps.py
g++ -O3 mps_exact.cpp -lgmpxx -lgmp -o mps_exact
./mps_exact mps_blocks.txt > mps_exact_output.txt
python thermal_small_exact.py
python published_scalar_enclosures.py
python bootstrap_scalar_checks.py

Note: floating-point numbers in terminal output are for display only.
All acceptance tests in these scripts use integer or rational comparisons.
Large intermediate matrix files and executable binaries are omitted from the ZIP.
