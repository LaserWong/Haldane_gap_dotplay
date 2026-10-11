# Accepted near-uniform alternating-chain review

Independent review accepts a unique periodic ground state for all integer cell counts M >= 2, with unit exchange on the designated first bond family:

- g in [19999/20001, 20001/19999]: gap >= .015.
- g in [12499/12501, 12501/12499]: gap >= .005.

PROOF.md reconstructs the untwisted quadratic finite-trace comparison, the direct real symmetric two-spin-cell history kernel, exact normalized/physical temperature conversion, every odd/even cell window and the finite Weyl bridge. It uses no product-of-self-adjoint-transfers shortcut or extensive infinite-volume perturbation argument.

The independent directed checker accepted all scalar claims and rejected 18 adversarial corruptions in .04745 CPU seconds and 11.6 MiB. The accepted uniform physical thermal/MPS evidence is inherited and pinned, not recomputed here. Producer seal: 836816261bc679b35d03e13e35141e3f7224fbbf56224ee4d428dc41b653cebd.

Reproduce with `python audit.py` in a disposable copy. No physical calculations, root-document changes or remote writes are performed. Exact results, limitations, source pins and measured resources are retained.
