"""Conservative planning estimates, not allocation or runtime guarantees.

Exact integer dimensions are separated from floating-point timing extrapolation.
The current matrix-free backend stores Python basis tuples plus a lookup dict;
it is NOT a tensor-network backend or an O(N)-storage implicit bitstring backend.
"""
from __future__ import annotations
import math
from .model import Model, _integer, _real


def plan_resources(model, total_m2=None, trial_rank=8, mps_bond=None,
                   krylov_vectors=24, memory_budget_bytes=None,
                   time_budget_seconds=None, calibration=None,
                   expected_matvecs=200, max_basis_dimension=2_000_000):
    if not isinstance(model, Model): model = Model.from_dict(model)
    rank = _integer(trial_rank, 'trial_rank', 1)
    krylov = _integer(krylov_vectors, 'krylov_vectors', 2)
    calls = _integer(expected_matvecs, 'expected_matvecs', 1)
    limit = _integer(max_basis_dimension, 'max_basis_dimension', 1)
    dimension = model.dimension(total_m2)
    if not dimension: raise ValueError('Requested magnetization sector is empty')
    if rank > dimension: raise ValueError('trial_rank exceeds selected computational dimension')
    if mps_bond is not None: mps_bond = _integer(mps_bond, 'mps_bond', 1)
    if memory_budget_bytes is not None: memory_budget_bytes = _integer(memory_budget_bytes,'memory_budget_bytes',1)
    if time_budget_seconds is not None:
        time_budget_seconds = _real(time_budget_seconds, 'time_budget_seconds')
        if time_budget_seconds <= 0: raise ValueError('time_budget_seconds must be positive')
    n, d = model.n_sites, dimension
    exchanges = sum(t[0] == 'exchange' and t[3] != 0 for t in model.terms)
    transitions_per_column = 1 + 2*exchanges + sum(2**sum(op == 'x' for _,op in t[2]) for t in model.terms if t[0] == 'spin_product' and t[1])
    nnz_bound = min(d*d, d*transitions_per_column)
    # Accounting assumptions are intentionally explicit and generous. Python
    # object sizes differ by interpreter; this is an estimate, never a limit.
    basis = d*(256+16*n)
    vector = 8*d
    trial = 8*d*rank
    projected = 8*rank*rank
    dense_matrix = 8*d*d
    dense_peak = basis + 4*dense_matrix + trial + 8*vector
    sparse_csr = 16*nnz_bound + 8*(d+1)
    # COO builder currently uses Python lists before converting to CSR.
    sparse_construction = basis + 128*d*transitions_per_column + sparse_csr
    iterative_workspace = basis + (krylov+8)*vector + 2*trial + 4*projected
    matrix_free_peak = iterative_workspace
    sparse_peak = max(sparse_construction, iterative_workspace+sparse_csr)
    mps_storage = None
    if mps_bond is not None:
        # Upper bound on open-boundary tensor entries for a selected ordering,
        # not the rank of a linear variational subspace or a guarantee of accuracy.
        bonds = [1] + [min(mps_bond,math.prod(model.local_dimensions[:i]),math.prod(model.local_dimensions[i:])) for i in range(1,n)] + [1]
        mps_storage = 8*sum(bonds[i]*di*bonds[i+1] for i,di in enumerate(model.local_dimensions))
    timings = {'status':'uncalibrated', 'matrix_free_seconds':None, 'dense_seconds':None,
               'expected_matvecs':calls, 'rigorous_bound':False}
    if calibration is not None:
        if not isinstance(calibration, dict): raise ValueError('calibration must be an object')
        allowed = {'dimension','expanded_term_count','matvec_seconds','dense_eigh_seconds','provenance'}
        if set(calibration)-allowed: raise ValueError('Unsupported calibration keys')
        ref_dim = _integer(calibration.get('dimension'), 'calibration dimension', 1)
        if 'matvec_seconds' in calibration:
            secs = _real(calibration['matvec_seconds'], 'matvec_seconds')
            if secs <= 0: raise ValueError('matvec_seconds must be positive')
            ref_terms = _integer(calibration.get('expanded_term_count'), 'calibration expanded_term_count', 1)
            timings['matrix_free_seconds'] = secs * (d/ref_dim) * (max(1,len(model.terms))/ref_terms) * calls
        if 'dense_eigh_seconds' in calibration:
            secs = _real(calibration['dense_eigh_seconds'], 'dense_eigh_seconds')
            if secs <= 0: raise ValueError('dense_eigh_seconds must be positive')
            timings['dense_seconds'] = secs * (d/ref_dim)**3
        timings['status'] = 'heuristic_calibrated_extrapolation'
        timings['calibration'] = calibration
    def admit(peak, runtime):
        if d > limit: return False
        if memory_budget_bytes is None: return None
        if peak > memory_budget_bytes: return False
        if time_budget_seconds is None: return True
        if runtime is None: return None
        return runtime <= time_budget_seconds
    return {
        'model':model.summary(),
        'full_hilbert_dimension':model.hilbert_dimension,
        'symmetry_sector':None if total_m2 is None else {'total_m2':total_m2,'dimension':d},
        'computational_dimension':d, 'linear_trial_rank':rank, 'mps_bond_dimension':mps_bond,
        'bytes':{'real_vector':vector, 'trial_vectors':trial, 'projected_trial_matrix':projected,
                 'python_basis_and_lookup_estimate':basis, 'dense_matrix':dense_matrix,
                 'dense_eigensolve_peak_estimate':dense_peak, 'sparse_csr_upper_estimate':sparse_csr,
                 'sparse_construction_peak_estimate':sparse_construction,
                 'sparse_iterative_peak_estimate':sparse_peak,
                 'matrix_free_iterative_peak_estimate':matrix_free_peak,
                 'mps_tensor_storage_estimate':mps_storage},
        'sparse_nnz_upper_bound':nnz_bound,
        'timing':timings,
        'budget':{'memory_bytes':memory_budget_bytes,'time_seconds':time_budget_seconds,'max_basis_dimension':limit},
        'admits_dense':admit(dense_peak,timings['dense_seconds']),
        'admits_matrix_free':admit(matrix_free_peak,timings['matrix_free_seconds']),
        # Dense/sparse timing cannot be interchanged with Python matrix-free timing.
        'admits_sparse':admit(sparse_peak,None),
        'assumptions':[
            'Dimensions and byte arithmetic are exact integers; memory overheads are estimates, not certified peaks.',
            'float64 real arithmetic, 8-byte vectors and 8-byte sparse indices; complex arithmetic is not supported by the model schema.',
            'Dense peak assumes four dense matrices, basis, trial vectors, and eight work vectors; LAPACK/workspace overhead can vary.',
            'Matrix-free implementation retains Python tuple basis and dict; estimated 256+16*N bytes per state.',
            'Sparse construction budgets 128 bytes per candidate entry for Python lists, then CSR; duplicates are combined.',
            'Iterative workspace includes krylov_vectors+8 full vectors, two trial blocks, and four projected matrices.',
            'MPS estimate counts only open-boundary tensors, not optimization workspace; no MPS solver is implemented.',
            'Timing extrapolation assumes comparable hardware/backend and linear matvec or cubic dense scaling; convergence and allocation time are not guaranteed.',
            'Admission null means missing memory or calibrated timing information; admission true is only an estimate, not enforcement.',
            'Sector dimensions do not imply a gap in the full Hilbert space; omitted sectors require independent bounds.'
        ]}


def sweep_resources(model_specs, **planner_options):
    """Plan a supplied finite sequence of models without allocating their bases.

    This cannot infer a minimum theorem seed from a size-resource relation.
    Pass actual per-size mathematical certificate outcomes to summarize_seed_evidence.
    """
    return [plan_resources(spec, **planner_options) for spec in model_specs]


def summarize_seed_evidence(records):
    """Summarize tested physical sizes without turning failed certificates into no-go results.

    Each record: {'physical_size': positive int, 'hilbert_dimension': int,
    'certificate_status': 'certified'|'failed'|'unverified'|'not_tested', ...}.
    Caller is responsible for verification and for an explicitly fixed model family,
    bootstrap criterion, boundary convention, and normalization across records.
    """
    checked = []
    for record in records:
        size = _integer(record.get('physical_size'), 'physical_size', 1)
        dim = _integer(record.get('hilbert_dimension'), 'hilbert_dimension', 1)
        status = record.get('certificate_status')
        if status not in ('certified','failed','unverified','not_tested'):
            raise ValueError('Unknown certificate_status')
        checked.append(dict(record,physical_size=size,hilbert_dimension=dim))
    successes = sorted((r for r in checked if r['certificate_status']=='certified'),key=lambda r:r['physical_size'])
    return {'smallest_verified_sufficient_tested_seed':successes[0] if successes else None,
            'minimum_sufficient_seed':None,
            'minimum_status':'not_established',
            'records':checked,
            'conclusion':('A successful tested seed gives a sufficient size, not a proof of minimality.' if successes else 'No certified sufficient size is available from these records; no finite minimum estimate is justified.'),
            'caution':'Failure of a partial-spectrum bootstrap can reflect weak bounds or missing states, not a physically gapless model. Resource growth and monotone fits do not certify a seed threshold.'}
