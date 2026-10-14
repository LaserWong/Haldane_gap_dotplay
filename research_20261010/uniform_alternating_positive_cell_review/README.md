# Accepted structural lemma for the positive cell

For spin one and every finite coupling g >= 0, the two-site alternating Heisenberg cell-history transfer is positive and trace class. Its exact factorization is A_g A_g*, where A_g maps L²(mu_g) to L²(mu_1). PROOF.md explicitly defines both positive raw history measures and the corresponding adjoint.

For every integer base n >= 2, including odd n, the window n <= M <= 2n obeys T(M,beta) >= min(S(n,beta) sqrt(T(2n,beta)), T(2n,beta)). This interpolation requires neither a dominant-atom threshold nor a signed-tail penalty. Recurrence legality and numerical gap checks are still required.

The structural proof leaves earlier frozen certificates unchanged and does not itself establish a new numerical interval. A uniform-chain bound based on these cells covers even physical lengths. Odd physical lengths require a separate proof. The all-physical-length .0248 theorem is unchanged.

The companion check uses only abstract exact sequence arithmetic. It covers 2,145 windows, including 1,170 odd-base cases. No physical matrix construction, contraction or thermal calculation was performed. Reproduce the check in a disposable copy with `python check_lemmas.py`.
