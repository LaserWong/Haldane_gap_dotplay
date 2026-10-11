# Independent21D split-image fixture

Scope: complete physical H'^2 on the4x4 basis B6,L5,R5,M5, dimension21 in physical dimension4^16=2^32. The8x4 producer sample is checked only for algebraic recombination and remains partial. No full57D matrix or new energy/gap endpoint is accepted here.

## Independent oriented image contractions

Use H'=Q+(g/2)A. R has q4 and M has q6. Their A images are
 R: q2 CR, q4 r4=A44R, q6 r6=C†R;
 M: q4 m4=CM, q6 m6=A66M, q8 C†M.
The new five blocks are r4*r4,r4*m4,r6*r6,r6*m6,m6*m6. Cross blocks retain their left/right orientation. Both are genuinely nonsymmetric on4x4, so replacing them by symmetric parts would be detectable.

The independently accepted reviewer support engine is lifted by a reproducible four-edit source generator. It saves the separate image arrays BEFORE adding r4+m4 and r6+m6, and contracts each required bilinear separately. No producer implementation is included or executed. All455 fixed-origin q4 and3003 q6 supports are traversed, with exact N/4,N/6 factors and divisibility checks. Every one of125 new matrix entries matches the producer. The unchanged checked matrix arithmetic bounds from the complete8x4 reviewer apply; there are more separately stored accumulators, not larger terms per accumulator.

The full old PP,TT,CMCM and signed COMM are also independently reproduced in this small fixture. Exact recombination verifies PP=r4*r4+r4*m4+m4*r4+CMCM and TT=r6*r6+r6*m6+m6*r6+m6*m6. These checks supplement the independent individual-entry verification; they do not substitute for it.

## Complete21x21 polynomial

The reviewer uses pure Python exact arithmetic to reconstruct the physical4x4 weighted graph, pair-orbit basis, pair Gram and physical pair-preserving action independently. Cached independently verified F,S,V,W,X,Y,Z geometry then reconstructs the split Gram and first-moment matrix. Gram rank21 is proved by positive rational pivots. Homogeneous triplet numbers q=(0,2,4,4,6 by blocks) give Q²_ij=q_i q_j G_ij and (QA+AQ)_ij=(q_i+q_j)A_ij exactly.

The complete A images of B,L remain in the split basis. Their explicitly constructed coordinate map W satisfies GW=A[:,B,L], giving every mixed A² row as W*A. Only the R,M bottom blocks need the new contractions:
 A²_RR=S*Gpair^(-1)S+r4*r4+r6*r6;
 A²_RM=r4*m4+r6*m6;
 A²_MM=CMCM+m6*m6+Q8.
Here Q8=CMCM+COMM is the independently accepted complete signed-commutator norm. R's image has no q8 component. M's image does, and none is omitted. Hermitian transpose supplies the M,R block; neither cross matrix is symmetrized.

The resulting coefficients Q,A/2,Q²,(QA+AQ)/2,A²/4 match the producer entry by entry. Tying cR=cM gives an exact embedding of the old16D basis. Compression reproduces independently reconstructed old G and both H coefficients, and all three independently accepted complete H² coefficients. At g=.105, exact elimination verifies J>=0 and the FULL42x42 block Gram [[G,K],[K,J]]>=0, equivalently the unprojected residual Gram J-KG^(-1)K>=0. Complete q8 positivity and each new squared-image block are checked independently. Compression alone would not rule out opposing split-block errors; the independent oriented contractions do.

## Partial8x4 and resource boundary

The frozen8x4 sample visits2248 q4 and2023 q6 supports. Its old accepted sample is separately hash-pinned. Both PP and TT recombinations agree exactly, but no claim is made about unsampled entries or a full57D polynomial. The producer2.99-second full estimate is a timing projection only. A full8x4 pass requires separate authorization and independent complete-entry review.

Compilation used3.49CPU seconds and114.4MiB under the separately authorized512MiB compiler allowance. The complete physical4x4 pass used.545CPU seconds and6MiB under30CPU seconds/100MiB. Pure-Python matrix assembly used.23seconds and11.4MiB, with no NumPy mappings. REPRODUCE.sh validates hashes, regenerates and rebuilds the reviewer source, repeats the complete small physical run and exact assembly, and compares scientific results. No producer, root or remote files changed.
