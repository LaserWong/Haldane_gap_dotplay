# n=8 exclusion for the spin-1 Heisenberg heat-trace bootstrap

This directory certifies that length 8 cannot start the heat-trace bootstrap recursion for the periodic spin-1 Heisenberg chain, conditional on the assumptions below. The Hamiltonian is the periodic sum of nearest-neighbor dot products

$$
H_L=\sum_{i=1}^{L}\mathbf S_i\cdot\mathbf S_{i+1},
$$

with $\mathbf S_{L+1}=\mathbf S_1$, unit antiferromagnetic exchange, spin 1, and full Hilbert-space dimension $3^L$. There is no biquadratic term, field, or single-ion anisotropy. The per-site shift is the rational $a=700741/500000$. The shifted heat traces are $Z_L(b)=\operatorname{Tr}\exp(-b(H_L+aL))$.

## What the certificate proves

Two rigorous upper bounds hold in arb ball arithmetic.

1. $Z_{12}(49/4)\le 1.90055706559<1.900577$, with margin at least $1.99\times 10^{-5}$.
2. $\sup_{b\ge 0} Z_{12}(2b)^{4/3}/Z_8(b)^4\le 0.10040<1/2$.

Together these bounds exclude size $n=8$ as a starting length of the heat-trace bootstrap recursion. The exclusion is conditional on the transfer-operator and moment-inequality assumptions recorded in [CERTIFICATE_SUMMARY.txt](CERTIFICATE_SUMMARY.txt). A uniform spectral gap, and the status of every other seed size, remain separate claims.

The saved check counts 176571 distinct length-12 enclosures. Symmetry multiplicities bring the total to $531441=3^{12}$, the full Hilbert-space dimension at $L=12$. The length-8 side contributes $6561=3^8$ enclosures, the full Hilbert-space dimension at $L=8$. Both counts are eigenvalue multiplicities of symmetry blocks of $H_L$.

## Method

Each magnetization and crystal-momentum block is built with arb entries. An untrusted LAPACK eigensolver supplies a trial eigenbasis. That basis and the block matrix are rounded to dyadic rationals. The departure from orthonormality and the residual are then exact integer products. The products use plain IEEE double matrix multiplication on limbs small enough that every partial sum is an integer below $2^{53}$. Ostrowski and Weyl convert those residuals into one enclosure per eigenvalue of the block. The largest stored radius is about $6\times 10^{-7}$.

Momentum $k$ and $L-k$ are entrywise complex conjugates, so they share a spectrum. Magnetization $S^z$ and $-S^z$ are related by a spin flip. Only a fundamental set of blocks is diagonalized, and the omitted partners are counted by these multiplicities. The two fully polarized states $S^z=\pm 12$ have energy 12 exactly. The ratio bound bins energies outward at width $1/200$, covers $b\in[0,64]$ by 2142 arb intervals, and bounds the tail $b\ge 64$ by a negative linear exponent.

`enclose8.py`, `enclose12.py`, and `enclose12_fix.py` produced the saved enclosures. Four blocks returned a non-finite value because flint's `x**2` on a ball that straddles zero yields nan. Those blocks were recomputed with a product and stored in `fix12.json`. `verify.py` overrides the four blocks from that file and checks that every enclosure is finite. Replaying `verify.py` does not rebuild the blocks.

## Assumptions

The numerical inequalities are machine-checked from the saved enclosures. The passage from those inequalities to an exclusion of the recursion start still depends on conditions that this package does not re-prove.

- The transfer-operator and moment-inequality condition stated in `CERTIFICATE_SUMMARY.txt` must apply to these shifted traces. That condition is assumed, not re-derived here.
- The sector and Bloch-basis construction must be correct. The verifier supports that code with three exact checks. The length-12 multiplicity equals $3^{12}$. The multiplicity-weighted block traces contain $0$, which is $\operatorname{Tr} H$. The multiplicity-weighted squared Frobenius norms contain $8503056$, which is $\operatorname{Tr} H^2$. The length-8 file likewise matches dimension $3^8$, trace $0$, and its exact squared-Frobenius value.
- The conjugation multiplicity $k\leftrightarrow L-k$ and the spin-flip multiplicity $S^z\leftrightarrow -S^z$ are mathematical identifications. The verifier checks that the computed fundamental set of blocks is complete. It does not re-derive the symmetry.
- Exact integer products assume IEEE double arithmetic with no Strassen multiplication and no fast-math contraction. `selftest.py` compares the limb products with Python integers on a fixed random sample.
- python-flint and its arb implementation must be correct. The run recorded here uses python-flint 0.9.0.

## Requirements and how to run

Install `python-flint==0.9.0` and `numpy`. From this directory run

```sh
python verify.py
```

The check takes about 5 seconds. A successful run reprints a $Z_{12}(49/4)$ upper endpoint near $1.900557066$, a supremum at most about $0.100397$, and the multiplicities $531441$ and $6561$. The archived console record is `verify_output.txt`.

`python selftest.py` is optional and needs SciPy as well as NumPy. It checks the integer matrix products and does not recompute the heat traces. Rebuilding `enclosures8.json` and `enclosures12.json` is a separate long run. The recorded length-12 enclosure took on the order of 90 minutes on one CPU and is not required to verify the saved certificate.
