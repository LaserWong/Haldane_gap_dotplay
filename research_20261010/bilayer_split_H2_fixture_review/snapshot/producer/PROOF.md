# Split R/M complete-H² fixture and bounded sample

Producer fixture passes; independent split-matrix review pending. No full8x4 split pass is present.

The exact even-singlet trial has21 columns on4x4 (physical Hilbert dimension4^16=2^32) and would have57 on8x4 (physical Hilbert dimension4^32=2^64). These trial dimensions are distinct from physical Hilbert dimensions. Splitting U=R+M into independent R/M coefficients preserves maximum trialq6 and maximum imageq8.

Five new coupling-independent blocks are emitted by the same local matching-action infrastructure as the accepted full43D matrix engine: R4R4=(D4R)*(D4R), R4CM=(D4R)*CM, R6R6=(C†R)*(C†R), R6M6=(C†R)*D6M, M6M6=(D6M)*D6M. Cross matrices retain their orientations and are not symmetrized. Accepted CMCM and signed COMM are reused unchanged, giving Q8=CMCM+COMM in the M,M block only. The R image has no q8 component.

For both the full4x4 fixture and the deterministic8x4 sample, exact recombination reproduces accepted PP and TT entry by entry. The complete4x4 construction also reproduces every G,K,H² entry under the embedding cR=cM. Its Gram is positive definite, dimension21. The21x21 complete J and the42x42 block Gram [[G,K],[K,J]] are PSD, verifying a full unprojected residual Gram. All mixed blocks are built from the exact H(B,L) coordinate map in the split basis. Its q2 RR term is D2=S*Gpair^-1S, q4/q6 terms are retained individually, and q8 is the accepted signed-commutator result.

The emitted full4x4 polynomial stores Q,(A/2),Q²,(QA+AQ)/2,A²/4 matrices. Algebraic coefficient extraction atg=±1 invokes no stability inference at those values. A physical check atg=.105 reproduces the whole compressed accepted polynomial and the unprojected residual positivity. Recombination and PSD are necessary cross-checks, not substitutes for independent verification of individual split cross entries.

All4495/169911 q4/q6 supports would be needed for a full8x4 pass. The sample visits2248q4 and2023q6 and cannot certify unsampled entries. Measured support times were.0774089s for full4x4 and.194684s for sampled8x4, peak7680KiB. Phase-scaled full8x4 projection2.985818958s is only a resource estimate. Proposed full-pass cap40CPU seconds/100MiB; this package does not grant or assume its authorization.

The local int32 guards and checked int128 accumulation from the accepted engine are preserved. Matching Gram factors are<=27 and the inherited coarse accumulator bound remains below2^106 after translation rescaling. No signed commutator term is dropped, no q8 support enumeration or full ED is performed.
