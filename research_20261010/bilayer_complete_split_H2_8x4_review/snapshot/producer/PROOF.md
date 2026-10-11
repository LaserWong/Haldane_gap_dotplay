# Complete57D split8x4 second-moment matrix

Producer full matrix complete; independent full split-matrix review pending. No endpoint or all-size claim is made by this package.

One authorized full support pass uses the frozen split engine from bilayer_split_H2_fixture:4495 fixed-origin q4 and169911 fixed-origin q6 supports, without M-zero filtering. It took2.65946seconds onCPU3 and7680KiB peak RSS under40CPU seconds/100MiB. No duplicate full producer pass was run.

The basis is B15,L14,R14,M14, dimension57; the physical Hilbert space is4^32=2^64. Its exact Gram is positive definite. Maximum trial occupancy isq6 and complete image occupancyq8. Five new split-image blocks retain both nonsymmetric cross orientations. Existing independently accepted CMCM and signed COMM supply the unchanged q8 M,M norm; it is not omitted or replaced by a bosonic commutator.

assemble.py constructs the full57x57 G,K,H² coupling polynomial, including exact q2 RR norm D2, all separate q4/q6 terms and complete q8. Every mixed H² block follows the exact H(B,L) coordinate map. Setting cR=cM reproduces every accepted43D Gram, first-moment and complete second-moment coefficient exactly. Split sums reproduce accepted PP and TT. Full114x114 Gram [[G,K],[K,J]] is PSD at physicalg=.105, certifying consistency with an unprojected residual Gram. These checks do not substitute for independent verification of every split entry.

The stored coefficients are G, H(g)=Q+g(A/2), J(g)=Q²+g(QA+AQ)/2+g²A²/4. Extraction at formalg=±1 is algebra only; stability and spectral cutoffs must be checked separately at every physical coupling. The code and exact resource/overflow reasoning are pinned to the independently reviewed fixture lineage.

Reproduction after authorization: compile the pinned matrix_split.cpp with g++ -O2 -std=c++17 -lgmpxx -lgmp; invoke it with the pinned geometry_8x4.txt and a fresh output path, with no sampling argument, under taskset-c3/40CPU seconds/100MiB; compare all matrix entries and support counts, excluding resource fields. Run assemble.py with a fresh output directory and compare the complete polynomial and checks. Keep existing frozen files unchanged.
