# Certified seed-size and adaptive-bootstrap optimization

The results recorded here on October 10, 2026 concern seed size, temperature, update order, and limitations of the certification method. The physical transfer constructions and all-integer interpolation are in `../two_d_theory`. Independently certified low-energy records come from `../low_energy` and `../two_d_numerics`.

## Main conclusions

1. **True fixed-seed exclusions.** Uniform spin-1, spin-2, and spin-3 Heisenberg chains with bootstrap seed length n=2 are excluded at every temperature for the stated sequential purity recursion. Exact analytic L=2/L=4 spectra reduce the proof to rational polynomial positivity. Certified maximum W intervals are approximately [0.01267351988, 0.012674], [0.00209720572, 0.002098], and [0.00069432820, 0.000695]. The method's invariant failure threshold is W≤1/2, stronger than merely requiring first-step positivity W>sqrt(2)−1.
2. **Rigorous resource-planning obstruction.** For the spin-1/2 square AF bilayer at g=0.03 and the present 2×2/4×2/4×4 seed geometry, no beta, no local comparison parameter a, and no one of the three inequivalent x/y/time staircase orders can rescue the implemented ground-only numerator plus independent ordered-dimer-bin tail recipe. This remains true after allowing arbitrarily sharp ground refinement inside the existing depth-2 ground intervals. It is not a physical phase boundary or an impossibility for better seed inputs.
3. **Useful optimizations without new spectra.** Cancel common heat traces before interval evaluation. Optimize beta and the local thermal-tail parameter a. Rebuild the appropriate ratios for every legitimate staircase order. For the spin-1/2 bilayer g=0.01 this produces a certified square-gap bound 0.1689210216 for L≥4. At g=0.02 gives 0.0573084578 for L≥16. These enhanced numbers do not automatically cover smaller squares.
4. **Analytic dimer improvement.** Two-color dependency factorization improves the even-cell heat-trace error from beta² M² w²/8 to beta² M w²/4. At local perturbation width w=0.03, beta=6.4, ordinary rational replay already gives 0.1535504099 for every cell number M≥2 after a Weyl patch. Correlation-aware replay improves the certified all-M bound on the tested grid to 0.1667512861. At w=0.04, correlation-aware replay gives 0.0968387421 after its verified finite-size patch. A near-threshold scalar seed at w=0.047846 is certified, but its much larger starting length is not bridged to all small M.
5. **Entry constants.** The old coefficient 5 and all-integer one-dimensional interpolation remain valid for common defect u≤1/40, not only u≤0.01. This is a separately proved extension. The uploaded scalar code was not edited.

## Keep m, n, and L0 separate

- `m_moment_order` is the actual highest numerical input moment, when moments are used. It is null for purely analytic/local spectral calculations here.
- n is the bootstrap seed length (the cell count for a dimer chain or one side length for a square model).
- L0 is the first length covered by the eventual uniform gap theorem. It can substantially exceed n after transient iterations.
- Analytic dimer seed traces refer to 4- and 8-spin chains, but the actual spectral input is a two-spin dimer and the local perturbation width. An eight-site numerical spectrum or eighth moment is not computed.
- Uniform n=2 exclusion says nothing about whether fourth/eighth moments can certify much larger n using filtering.
- Low-energy bilayer records refer to full physical sizes up to 32 spins, but retain one certified ground vector and counted analytic excitation bins, not a full 4^16 spectrum.

## Model names and scopes

- `square_af_bilayer_spin_half_unit_rung`: two spin-1/2 layers with unit antiferromagnetic rung coupling and positive antiferromagnetic intralayer couplings g in both directions. Length-two periodic directions retain the two neighbor terms.
- `square_af_bilayer_unit_rung_s_one_*`: two spin-1 layers with the same graph/normalization. This is distinct from large-D.
- `single_layer_spin_one_large_D_square`: one spin-1 layer, H=sum (Sz)^2 + g sum_edges S_i·S_j, D=1.
- `dimer` statements refer to a one-dimensional alternating chain with general disjoint-cell perturbation of spectral width w.

The current single-layer large-D grid succeeds at g=0.015 with correlated x→y→time replay, giving approximately 0.0187550008 for L≥32. A grid failure at g=0.02 is not an exclusion certificate. Spin-one bilayer g=0.005 succeeds, while the tested spin-1 bilayer g=0.01 grid does not. Neither observation concerns the single-layer large-D model.

## Files

- `proofs/DERIVATIONS.md`: complete elementary derivations and careful obstruction scope.
- `code/certified_core.py`: rational Taylor intervals, dyadic outward rounding, scalar replay.
- `code/exact_n2_exclusion.py`: exact analytic spectra and Bernstein positivity.
- `code/spectral_search.py`: interface for certified counted energy bins, interval heat traces, derivative envelopes, all-beta exclusions and seed proposals.
- `code/necessary_windows.py`: rigorous thermal-lower-beta / spatial-upper-beta overlap tests.
- `code/asymmetric_basin.py`: independently certified accepted/rejected boundary brackets. Lower-trajectory failure is never misreported as a proof of exclusion.
- `code/colored_dimer.py`, `code/correlated_seeds.py`: analytic dimer and cancelled-ratio certification.
- `code/axis_order_search.py`: rebuilt staircase ratios and certified adjacent-swap conversion to the audited canonical order.
- `code/optimize_bilayer_tail.py`: certified beta-dependent analytic local comparison.
- `code/majorant_ceiling.py`: all-beta/all-a optimistic-envelope obstruction for the declared majorant family.
- `code/scan_large_d_orders.py`: separate single-layer large-D optimization.
- `code/test_certificates.py`: exact arithmetic regression suite.

Run with `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python code/test_certificates.py`. The initial eight-test suite passed in approximately 1.8 seconds with peak RSS approximately 61 MiB. Floating-point optimization only proposes rational candidates. Accepted comparisons, exponential enclosures, square roots, and emitted gaps are rational/outward-certified. Analytic proofs are human-audited, not proof-assistant formalized.

## Priority for the next expensive calculation

At spin-1/2 bilayer g=0.03, ground precision alone is now provably insufficient within the current recipe. Spend effort on improved low-excitation counting/tails, a Schur-complement comparison, cluster comparisons, or a changed seed geometry. In particular, projecting onto the rung vacuum plus all one-triplet states gives a 1+3N dimensional full-spin subspace. Its orthogonal complement starts at two unperturbed excitations. Exact compressed and off-diagonal Gram matrices can potentially improve the first spectral bin by a Schur-complement inertia argument. This is a proposed next calculation, not yet a completed certificate here.
