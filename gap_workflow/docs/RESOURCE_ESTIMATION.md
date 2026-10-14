# From a failed pilot to a resource decision

The workflow keeps four sizes separate: the number of physical sites, the full Hilbert dimension, the largest certified symmetry block, and the retained trial rank. An MPS bond dimension, when requested for storage planning, is a fifth quantity. None determines the others without a representation and a model.

## A concrete admission decision

The open spin-half 2 by 2 by 2 XXZ example has full dimension 256. Its exact magnetization sectors have dimensions 1, 8, 28, 56, 70, 56, 28, 8, and 1. An exact block cap of 32 is insufficient for exhaustive inertia coverage. A cap of 70 admits every block. The two example inputs differ only in this explicit budget. The larger cap is sufficient for this implementation, rather than a claim that no other certificate could use a smaller space.

The spin-one 2 by 2 square has full dimension 81 and largest magnetization sector 19. Exhaustive sector coverage fits the default exact cap of 32. Checking only the largest sector would not establish the full-model gap: all sectors are included and their dimensions sum to the full dimension.

## Measured cost and forecasts

The numerical pilots compute four low Ritz pairs for eleven small finite models. A separate exact benchmark uses two proposed low states and exact arithmetic to certify six finite-size bounds. Neither pilot replaces spectral completeness with a residual test. Exact certification covers the omitted states through inertia or a proved analytical tail.

`benchmarks/partial_spectrum_pilots.json` records measured construction, matrix-vector and partial-solve times. `benchmarks/resource_forecasts.json` contains 28 full-space/sector forecasts using the same Python matrix-free backend and an assumed 200 matrix-vector operations. These are estimates for that implementation and machine. A compiled backend, different hardware, or a different convergence rate requires new calibration.

For example, the spin-one 12-site chain has full dimension 531441 and Sz=0 dimension 73789. The current accounting estimates about 0.38 GiB and 0.053 GiB for their respective matrix-free iterative workspaces. The corresponding 200-operation forecasts are about 3234 s and 449 s. These estimates exclude an unproved guarantee of convergence and do not establish a useful bootstrap seed.

The spin-half 3 by 3 by 3 model has full dimension 134217728. Its smallest-|Sz| sector has dimension 20058300. The same Python representation estimates about 126 GiB and 18.8 GiB. This rules out these particular computations under the default 512 MiB budget. It does not rule out a tensor-network, analytical, or more specialized certificate.

## Predicting a seed size

`forecast_seed_size` accepts comparable bootstrap-defect records at distinct physical sizes, their evidence labels, and the applicable threshold. A certified input bound below threshold identifies a tested sufficient scalar seed. Its model-to-seed proof and coverage bridge must also be verified.

With at least three failing pilot sizes, the optional fit uses log(defect)=a+b*size to propose a next even size. The fit is heuristic. It neither proves a minimum nor proves failure at untested sizes. No improving trend gives no finite crossing estimate. Too few data give an explicit missing-data result. Exact threshold comparisons use rational arithmetic. Floating point is used only for the forecast.

## When more resources will not fix the chosen method

The connected ferromagnetic Ising diagnostic proves that near-one thermal purity cannot be reached because the ground space is two-dimensional. The global-width Hoeffding diagnostic separately excludes its original seed construction at specified couplings for every temperature and every larger seed. Both conclusions concern a particular criterion. They redirect the search to a different ground-space or tail bound instead of enlarging the same calculation.

The workflow distinguishes these mathematical obstructions from a timeout, a memory limit, an unsupported operator, an unverified spectral tail, and physical gaplessness. A failure of one route does not establish an impossibility theorem for all routes.
