# Hamiltonians and normalization

The strong antiferromagnetic exchange is the unit of energy in both models. The parameter g is the weak-to-strong exchange ratio. All reported gaps are unchanged by the constant shifts used in the computation.

## Ordinary spin-1/2 square bilayer

Each layer has L × L sites, with periodic boundaries. Let r=(x,y), let ell=1,2 label the layers, and let e_x,e_y be the positive lattice unit vectors. Each spin is S_(r,ell)=sigma_(r,ell)/2, so S²=3/4.

$$
H_L=\sum_{\mathbf r}\mathbf S_{\mathbf r,1}\cdot\mathbf S_{\mathbf r,2}
+g\sum_{\mathbf r}\sum_{\mu=x,y}
\left(\mathbf S_{\mathbf r,1}\cdot\mathbf S_{\mathbf r+\mathbf e_\mu,1}
+\mathbf S_{\mathbf r,2}\cdot\mathbf S_{\mathbf r+\mathbf e_\mu,2}\right).
$$

There are 2L² physical spins and L² vertical rungs. The rung exchange is 1. Both layers have nearest-neighbor intralayer exchange g. There are no crossed interlayer bonds and no magnetic field.

The positive-direction sum specifies the finite-size convention. At L=2, the two oriented steps around a periodic direction yield two parallel bonds between the same pair. At L≥3 it agrees with counting each ordinary undirected nearest-neighbor bond once. Rectangular seed patches use the same convention in each direction. The accepted all-size statements concern square tori with every integer L≥2, not arbitrary aspect ratios.

The product of rung singlets has energy expectation −3L²/4. Computations often use

$$
H'_L=H_L+\frac{3L^2}{4}\,\mathbb I.
$$

At g=0 this product is the unique ground state and its gap is 1. At positive g it remains a reference state, not an asserted exact ground state. The term ordinary bilayer distinguishes this Hamiltonian from the separately studied fully frustrated model with crossed bonds.

## Spin-1 alternating Heisenberg chain

There are M two-site cells and 2M physical spin-1 sites. Each spin satisfies S²=2. The periodic convention is S_(2M+1)=S_1, with M≥2.

$$
H_M=\sum_{j=1}^{M}\left(
\mathbf S_{2j-1}\cdot\mathbf S_{2j}
+g\,\mathbf S_{2j}\cdot\mathbf S_{2j+1}\right).
$$

The strong bonds have exchange 1 and the alternating weak bonds have exchange g. There is no biquadratic term, single-ion anisotropy or magnetic field. A strong spin-1 dimer has total-spin 0, 1, 2 energies −2,−1,1. After shifting by 2, these become 0,1,3 with multiplicities 1, 3, 5. In particular, a quintet has excitation weight 3. It must not be counted as a unit-energy triplet.

The reference singlet product has energy expectation −2M. The shifted Hamiltonian is

$$
H'_M=H_M+2M\,\mathbb I.
$$

At g=0, the product is the unique ground state with gap 1. The g=1 Hamiltonian is the uniform spin-1 Heisenberg chain. Certificates at g=.2 establish the alternating-chain result at that parameter and do not establish the uniform-chain result. The archived uniform-chain proof has its own inputs, assumptions and size range.

## Meaning of the reported bounds

A stated lower bound is a sufficient certified bound for the explicitly specified model, coupling, boundary convention and size range. It is not the actual gap, a critical coupling or the largest coupling the method could certify. Different successful recipes can produce nonmonotone sequences of lower bounds as g changes. Proof and independent-review links in the repository README specify each certificate's scope.
