# Accepted positive-cell structural lemma

For spin one and every finite coupling g >= 0, the two-site alternating Heisenberg cell-history transfer is positive trace class. The exact factorization is A_g A_g*, where A_g maps L²(mu_g) to L²(mu_1); the two positive raw history measures and the correct adjoint are explicit in PROOF.md.

For every integer base n >= 2, including odd n, the window n <= M <= 2n obeys T(M,beta) >= min(S(n,beta) sqrt(T(2n,beta)), T(2n,beta)). The interpolation needs no dominant-atom threshold or signed-tail penalty. Recurrence legality and numerical gap checks still apply.

This new structural proof does not alter earlier frozen certificates or establish a new numerical interval by itself. A uniform-chain bound using these cells covers even physical lengths unless odd physical lengths are proved separately. The all-physical-length .0248 theorem is unchanged.

The companion check performs only abstract exact sequence arithmetic: 2,145 windows, including 1,170 odd-base cases. No physical matrices, contractions or thermal calculation were run. Reproduce in a disposable copy with `python check_lemmas.py`.
