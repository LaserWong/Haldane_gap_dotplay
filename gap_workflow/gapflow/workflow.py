"""Auditable, bounded orchestration. No remote actions, general bootstrap claim, or large dense ED."""
from __future__ import annotations
import hashlib
from dataclasses import asdict, is_dataclass
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction


def write_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False, default=lambda x: asdict(x) if is_dataclass(x) else str(x)) + '\n')
    temporary.replace(path)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def load_request(text):
    """Preserve source coefficient decimal lexemes; normalize only solver budgets/spins."""
    raw = json.loads(text, parse_float=Decimal)
    def normalize(value, path=()):
        if isinstance(value, dict):
            return {k: normalize(v, path+(k,)) for k,v in value.items()}
        if isinstance(value, list):
            return [normalize(v, path+(str(i),)) for i,v in enumerate(value)]
        if isinstance(value, Decimal):
            if path and path[0] == 'budget':
                return float(value)
            if 'spin' in path or 'spins' in path:
                if not value.is_finite() or (2*Fraction(str(value))).denominator != 1:
                    raise ValueError('spin must be an exact positive integer or half-integer')
                exact_spin = Fraction(str(value))
                if exact_spin.denominator == 1:
                    return exact_spin.numerator
                numeric_spin = float(value)
                if not math.isfinite(numeric_spin) or Fraction(numeric_spin) != exact_spin:
                    raise ValueError('half-integer spin is not exactly representable by the supported numerical backend')
                return numeric_spin
            return str(value)
        return value
    return normalize(raw)


def execution_provenance():
    import importlib.metadata
    import platform
    package = Path(__file__).resolve().parent
    sources = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(package.glob('*.py'))}
    versions = {}
    for name in ('numpy', 'scipy', 'sympy'):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = 'not installed'
    review_paths = globals().get('QUANTUM_ISING_REVIEWED_SHA256', {})
    review_sources = {name:hashlib.sha256((package.parent/name).read_bytes()).hexdigest()
                      if (package.parent/name).exists() else None for name in review_paths}
    return {'code_sha256':digest(sources), 'source_sha256':sources,
            'reviewed_physical_source_sha256':review_sources,
            'dependencies':versions, 'python':sys.version, 'platform':platform.platform()}


def budget_values(raw):
    defaults = dict(max_dimension=4096, memory_mb=512, wall_seconds=30,
                    trial_rank=6, exact_max_dimension=32, max_iterations=1000,
                    tolerance=1e-9)
    if not isinstance(raw, dict) or set(raw) - set(defaults):
        raise ValueError('budget must be an object with documented keys only')
    result = {**defaults, **raw}
    for key, value in result.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f'budget.{key} must be a positive finite number')
        if key not in {'wall_seconds', 'tolerance'} and not isinstance(value, int):
            raise ValueError(f'budget.{key} must be an integer')
    if result['memory_mb'] < 128:
        raise ValueError('memory_mb must be >=128 to admit the Python scientific runtime')
    if result['exact_max_dimension'] > 128:
        raise ValueError('exact_max_dimension cannot exceed the conservative hard ceiling of 128')
    return result


def finish(out, result):
    if (out/'catalog.json').exists():
        result.setdefault('historical_catalog', json.loads((out/'catalog.json').read_text()))
    result.setdefault('claim', 'No certified gap conclusion.')
    result.setdefault('uniform_family_claim', False)
    result.setdefault('model_gapless', 'not established')
    result['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    result['artifacts'] = sorted(p.name for p in out.iterdir() if p.is_file() and not p.name.endswith('.tmp'))
    write_json(out / 'results.json', result)
    write_json(out / 'checkpoint.json', {'schema_version': 1, 'input_sha256': result.get('input_sha256'),
               'state': 'terminal', 'status': result['status'], 'execution_provenance':result.get('execution_provenance'), 'resume_policy': 'Verify input and artifact hashes; terminal runs are reused, never silently rerun.',
               'artifact_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()
                                   if p.is_file() and p.name not in {'checkpoint.json', 'report.md'} and not p.name.endswith('.tmp')}})
    (out / 'report.md').write_text('# Gap workflow report\n\n'
        + f"Status: {result['status']}\n\n{result['claim']}\n\n"
        + f"Reason: {result.get('reason', 'See stage artifacts.')}\n\n"
        + ('This family conclusion uses the registered analytic proof recorded in the certificate.\n\n' if result.get('uniform_family_claim')
           else 'Scope: the specified finite Hamiltonian and selected sector, if any. Numerical candidates alone do not certify spectral completeness.\n\n')
        + '## Diagnostics\n\n' + json.dumps(result.get('diagnostics', {}), indent=2) + '\n')
    return result


def run(input_path, output_dir, resume=False):
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()) and not resume:
        raise ValueError('Output directory is not empty; use --resume or a new output directory')
    try:
        if Path(input_path).stat().st_size > 1_000_000:
            raise ValueError('Input exceeds 1 MB safety limit')
        request = load_request(Path(input_path).read_text())
        if not isinstance(request, dict) or set(request) - {'model', 'budget', 'solver', 'certificate', 'bootstrap'}:
            raise ValueError('Input must contain only model, budget, solver, certificate, bootstrap')
        if 'model' not in request:
            raise ValueError('Missing model')
        budget = budget_values(request.get('budget', {}))
        request['budget'] = budget
        fingerprint = digest(request)
    except (OSError, ValueError, TypeError) as exc:
        if any(out.iterdir()):
            raise ValueError('Invalid input; existing output left unchanged: ' + str(exc)) from exc
        return finish(out, {'status': 'invalid_input', 'reason': str(exc)})
    provenance = execution_provenance()
    checkpoint = out / 'checkpoint.json'
    if any(out.iterdir()):
        if resume and checkpoint.exists():
            saved = json.loads(checkpoint.read_text())
            if saved.get('execution_provenance') != provenance:
                raise ValueError('Resume code or environment provenance differs; choose a new output directory for fresh computation')
            if saved.get('input_sha256') != fingerprint:
                raise ValueError('Resume input differs from checkpoint; choose a new output directory')
            for name, sha in saved.get('artifact_sha256', {}).items():
                if not (out/name).exists() or hashlib.sha256((out/name).read_bytes()).hexdigest() != sha:
                    raise ValueError(f'Resume artifact hash mismatch: {name}')
            if saved.get('state') == 'terminal' and (out/'results.json').exists():
                return json.loads((out/'results.json').read_text())
            raise ValueError('Interrupted run requires a new output directory; retain old checkpoint for diagnosis')
        raise ValueError('Output directory is not empty; use --resume or a new output directory')
    write_json(out/'input.json', request)
    write_json(checkpoint, {'state': 'running', 'input_sha256': fingerprint, 'stage': 'validate', 'execution_provenance':provenance})
    env = dict(os.environ)
    env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    package_root = str(Path(__file__).resolve().parent.parent)
    env['PYTHONPATH'] = package_root + os.pathsep + env.get('PYTHONPATH', '')
    def limits():
        import resource
        cap = budget['memory_mb'] * 1024**2
        resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
        cpu = max(1, math.ceil(budget['wall_seconds']))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu+1))
    response = out/'worker_result.json'
    started = time.monotonic()
    try:
        with (out/'worker.log').open('w') as log:
            proc = subprocess.run([sys.executable, '-m', 'gapflow', '--internal-worker', str(out/'input.json'), str(response)],
                                  env=env, stdout=log, stderr=subprocess.STDOUT,
                                  timeout=budget['wall_seconds'], preexec_fn=limits if os.name == 'posix' else None)
        if response.exists():
            result = json.loads(response.read_text())
        else:
            result = {'status': 'resource_limit' if proc.returncode < 0 else 'worker_failed',
                      'reason': f'Worker ended with code {proc.returncode}; inspect worker.log',
                      'diagnostics': {'failure_class': 'resource_or_runtime_failure', 'gaplessness': 'not established'}}
    except subprocess.TimeoutExpired:
        result = {'status': 'resource_limit', 'reason': 'Hard wall-time budget reached; worker terminated',
                  'diagnostics': {'failure_class': 'resource_infeasible_for_this_run', 'minimal_seed_size': 'unknown'}}
    observed_provenance = execution_provenance()
    if observed_provenance != provenance:
        result['unaccepted_status'] = result.get('status')
        result['status'] = 'source_or_environment_changed'
        result['claim'] = 'Artifacts preserved, but no certificate accepted because code or environment changed during execution.'
        result['reason'] = 'Rerun in a fresh output directory after source and dependencies are stable.'
        result['uniform_family_claim'] = False
        result['observed_end_provenance'] = observed_provenance
    if checkpoint.exists():
        result['last_recorded_stage'] = json.loads(checkpoint.read_text()).get('stage')
    result.update(input_sha256=fingerprint, execution_provenance=provenance, elapsed_seconds=time.monotonic()-started,
                  memory_enforcement='OS address-space hard limit' if os.name == 'posix' else 'estimates only')
    return finish(out, result)


def worker(request_path, response_path):
    request = json.loads(request_path.read_text())
    out = response_path.parent
    try:
        result = compute(request, out)
    except MemoryError:
        result = {'status': 'resource_limit', 'reason': 'Memory allocation exceeded hard address-space budget'}
    except (ValueError, TypeError, KeyError, NotImplementedError) as exc:
        result = {'status': 'invalid_or_unsupported_input', 'reason': str(exc)}
    except Exception as exc:
        import traceback
        traceback.print_exc()
        result = {'status': 'worker_failed', 'reason': f'{type(exc).__name__}: {exc}'}
    write_json(response_path, result)


def record_stage(request, out, stage):
    previous = json.loads((out/'checkpoint.json').read_text()) if (out/'checkpoint.json').exists() else {}
    write_json(out/'checkpoint.json', {'state':'running', 'input_sha256':digest(request), 'stage':stage,
                                     'execution_provenance':previous.get('execution_provenance')})


def compute(request, out):
    record_stage(request, out, 'validate_model')
    if isinstance(request.get('model'), dict) and request['model'].get('family') == 'graph_state_projector':
        return compute_stabilizer(request, out)
    if isinstance(request.get('model'), dict) and request['model'].get('family') == 'pinned_ferromagnetic_ising':
        return compute_pinned_ising(request, out)
    if isinstance(request.get('model'), dict) and request['model'].get('family') in {'ferromagnetic_heisenberg_chain','ferromagnetic_spin_half_heisenberg_cycle'}:
        return compute_gapless(request,out)
    if isinstance(request.get('model'), dict) and request['model'].get('family') == 'quantum_ising_chain':
        return compute_quantum_ising(request,out)
    import numpy as np
    from scipy.sparse.linalg import eigsh, ArpackNoConvergence
    from .model import Model
    from .resources import plan_resources
    from . import certify
    from fractions import Fraction
    model = Model.from_dict(request['model'])
    from .catalog import match_catalog
    write_json(out/'catalog.json',match_catalog(model,repository_root=Path(__file__).resolve().parent.parent))
    budget = request['budget']
    solver = request.get('solver', {})
    if not isinstance(solver, dict) or set(solver) - {'total_m2'}:
        raise ValueError('solver supports only total_m2')
    sector = solver.get('total_m2')
    if sector is None and model.terms and all(s == 1 for s in model.spins2) and all(t[0]=='exchange' and t[3]==0 and t[4]<0 for t in model.terms):
        obstruction = compute_ising(request, model, out)
        if obstruction is not None:
            return obstruction
    dimension = model.dimension(sector)
    summary = model.summary()
    write_json(out/'model.json', summary)
    record_stage(request, out, 'resource_planning')
    plan = plan_resources(model, total_m2=sector, trial_rank=min(budget['trial_rank'], max(1, dimension)),
                          krylov_vectors=max(2, min(dimension, max(20, 2*min(budget['trial_rank'], max(1,dimension-1))+1))),
                          memory_budget_bytes=budget['memory_mb']*1024**2,
                          max_basis_dimension=budget['max_dimension'])
    sector_dimensions = model.sector_dimensions() if model.preserves_total_sz and sector is None else None
    if sector_dimensions:
        plan['exact_required_block_dimension'] = max(sector_dimensions.values())
        plan['exact_sector_dimensions'] = sector_dimensions
        plan['exact_sector_partition_admitted'] = max(sector_dimensions.values()) <= budget['exact_max_dimension']
    plan['hard_wall_seconds'] = budget['wall_seconds']
    plan['runtime_admission'] = 'bounded pilot; completion time is not forecast'
    write_json(out/'resources.json', plan)
    diagnostic = {'physical_seed_sites': model.n_sites, 'full_hilbert_dimension': model.hilbert_dimension,
                  'working_dimension': dimension, 'ground_multiplicity_assumption':None, 'requested_trial_rank': budget['trial_rank'],
                  'minimal_seed_size': 'unknown: requires an applicable geometric criterion and certified multi-size data',
                  'time_forecast': 'uncalibrated; no guaranteed completion-time estimate',
                  'geometric_seed_failure': 'not evaluated: general bootstrap adapter unavailable',
                  'tail_completeness': 'not yet certified',
                  'next_experiments': [
                      'Fix a proved geometry-specific bootstrap threshold before forecasting a sufficient physical seed size.',
                      'For each explicitly specified larger model, run resource planning before allocating a basis.',
                      'Compare increasing trial ranks at fixed physical size to separate trial error from geometric seed failure.',
                      'Calibrate matvec time on an admitted small pilot; time extrapolation remains heuristic.',
                      'Call a passing size sufficient, never minimal unless all smaller admissible sizes are excluded.']}
    if sector_dimensions:
        diagnostic['exact_required_block_dimension'] = max(sector_dimensions.values())
        diagnostic['all_sector_coverage_required'] = True
        if dimension > budget['exact_max_dimension'] and max(sector_dimensions.values()) > budget['exact_max_dimension']:
            diagnostic['exact_budget_recommendation'] = {'current_exact_cap':budget['exact_max_dimension'],
                'required_exact_block_cap':max(sector_dimensions.values()), 'automatic_increase':False,
                'meaning':'Largest complete Sz block; all blocks must be certified before a full-model claim'}
    if dimension > budget['max_dimension'] or not plan.get('admits_matrix_free', False):
        diagnostic['failure_class'] = 'resource_infeasible_for_this_run'
        return {'status': 'resource_limit', 'reason': 'Working dimension or estimated memory exceeds admitted budget', 'diagnostics': diagnostic}
    if dimension < 2:
        return {'status': 'insufficient_evidence', 'reason': 'Selected space has fewer than two states; no excitation gap can be inferred', 'diagnostics': diagnostic}
    k = min(budget['trial_rank'], dimension-1)
    record_stage(request, out, 'partial_spectrum')
    H = model.hamiltonian(total_m2=sector, matrix_free=True, max_dimension=budget['max_dimension'])
    try:
        values, vectors = eigsh(H, k=k, which='SA', tol=budget['tolerance'],
                                maxiter=budget['max_iterations'], v0=np.random.default_rng(0).normal(size=dimension))
        converged = True
    except ArpackNoConvergence as exc:
        values, vectors = exc.eigenvalues, exc.eigenvectors
        converged = False
    order = np.argsort(values)
    values, vectors = values[order], vectors[:, order]
    residuals = [float(np.linalg.norm(H @ vectors[:,i]-values[i]*vectors[:,i])) for i in range(len(values))]
    candidate = {'evidence': 'floating_point_partial_spectrum_only', 'converged': converged,
                 'trial_rank_actual': len(values), 'eigenvalues': values.tolist(), 'residual_norms': residuals,
                 'complete_tail': False, 'sector': sector, 'ground_degeneracy': 'unknown; not supplied or assumed'}
    write_json(out/'candidate.json', candidate)
    diagnostic['trial_approximation'] = 'converged numerical candidate' if converged else 'iteration limit; partial candidates only'
    result = {'status': 'candidate_only', 'claim': 'Floating-point finite-size candidates only; no certified gap.', 'diagnostics': diagnostic}
    record_stage(request, out, 'exact_certificate_and_validation')
    certificate = {'status': 'unsupported', 'reason': 'Exact rational construction unavailable or exact dimension budget exceeded'}
    validation = {'status': 'not_run', 'reason': 'No exact certificate to validate'}
    if dimension <= budget['exact_max_dimension'] and hasattr(model, 'exact_hamiltonian'):
        try:
            metric = None
            try:
                exact = model.exact_hamiltonian(total_m2=sector, max_dimension=budget['exact_max_dimension'])
            except (NotImplementedError, ValueError):
                exact, metric = model.exact_pencil(total_m2=sector, max_dimension=budget['exact_max_dimension'])
            if metric is None:
                ground_certificate = lambda e,g: certify.certify_gap(exact,e,g,max_dimension=budget['exact_max_dimension'])
                vector_certificate = lambda v,t: certify.certify_gap_from_vector(exact,v,t,max_dimension=budget['exact_max_dimension'])
            else:
                ground_certificate = lambda e,g: certify.certify_pencil_gap(exact,metric,e,g,max_dimension=budget['exact_max_dimension'])
                vector_certificate = lambda v,t: certify.certify_pencil_gap_from_vector(exact,metric,v,t,max_dimension=budget['exact_max_dimension'])
            proposed = request.get('certificate', {})
            if not isinstance(proposed, dict) or set(proposed)-{'ground_energy','gap_lower_bound'}:
                raise ValueError('certificate supports ground_energy and gap_lower_bound')
            ground = proposed.get('ground_energy')
            gap = proposed.get('gap_lower_bound')
            if ground is None and len(values):
                ground = str(Fraction(float(values[0])).limit_denominator(10000))
            if gap is None and len(values):
                higher = [v for v in values if v-values[0] > max(1e-7, 10*budget['tolerance'])]
                if higher:
                    gap = str(Fraction(float((higher[0]-values[0])*0.9)).limit_denominator(10000))
            if ground is not None and gap is not None:
                certificate = ground_certificate(ground,gap)
                replay_ok = bool(certificate['certified'] and ground_certificate(ground,gap) == certificate)
                if not certificate['certified'] and len(values) > 1 and not proposed:
                    # Rationalizing a vector is allowed: its Rayleigh quotient is
                    # recomputed exactly on the original rational Hamiltonian.
                    threshold = str(Fraction(float(values[0]+0.9*(values[1]-values[0]))).limit_denominator(10000))
                    physical = vectors[:,0] if metric is None else vectors[:,0] / np.sqrt(np.asarray(metric,dtype=float))
                    trial = [str(Fraction(float(x)).limit_denominator(100000)) for x in physical]
                    certificate = vector_certificate(trial,threshold)
                    replayed = vector_certificate(trial,threshold)
                    replay_ok = bool(certificate['certified'] and replayed == certificate)
                exact_float = np.asarray(exact, dtype=float)
                if metric is not None:
                    weights = np.sqrt(np.asarray(metric,dtype=float))
                    exact_float = exact_float / weights[:,None] / weights[None,:]
                maximum_error = max(float(np.max(np.abs(H @ np.eye(dimension)[:,j] - exact_float[:,j]))) for j in range(dimension))
                validation = {'valid': bool(replay_ok and maximum_error < 1e-12),
                              'exact_replay': bool(replay_ok), 'independent_exact_implementation': False,
                              'independent_model_representation_check': 'float matrix-free columns versus rational construction',
                              'maximum_matrix_entry_error': maximum_error,
                              'limitation': 'Independent representation crosscheck is numerical; exact verifier replays the same inertia implementation.'}
                certificate['status'] = 'certified' if certificate['certified'] else 'not_certified'
            else:
                certificate = {'status': 'insufficient_evidence', 'reason': 'Need rational ground_energy and positive gap_lower_bound proposals'}
        except (NotImplementedError, TypeError, ValueError) as exc:
            certificate = {'status': 'unsupported_or_failed', 'reason': str(exc)}
    if dimension > budget['exact_max_dimension'] and sector_dimensions and max(sector_dimensions.values()) <= budget['exact_max_dimension']:
        record_stage(request, out, 'complete_sector_partition_certificate')
        certificate, validation = certify_sector_partition(request, model, values, vectors, H)
        diagnostic['exact_backend'] = 'complete Sz-sector partition'
    if not certificate.get('certified') and not request.get('certificate') and len(values)>1:
        exact_admitted = dimension <= budget['exact_max_dimension'] or (sector_dimensions and max(sector_dimensions.values()) <= budget['exact_max_dimension'])
        if exact_admitted:
            record_stage(request,out,'unknown_degeneracy_low_band')
            low_band, low_validation = certify_unknown_low_band(request,model,sector,values)
            write_json(out/'low_band.json',low_band)
            if low_band.get('certified'):
                certificate,validation = low_band,low_validation
    write_json(out/'certificate.json', certificate)
    write_json(out/'validation.json', validation)
    record_stage(request, out, 'bootstrap_admission')
    bootstrap = {'status': 'criterion_unsupported', 'uniform_family_claim': False,
                 'reason': 'No general geometric bootstrap adapter is registered. Finite-size certification alone is insufficient.',
                 'admission_requires': ['Hamiltonian normalization and local interaction hypotheses', 'boundary and patch geometry',
                                       'proved overlap constants and finite-size threshold', 'certified seed bounds at every required size',
                                       'independently checked theorem hypotheses'],
                 'minimal_seed_physical_size': None, 'minimal_trial_dimension': None,
                 'forecast_is_not_proof': True}
    if request.get('bootstrap') is not None:
        from .bootstrap import bootstrap_certificate
        bootstrap['scalar_adapter_result'] = bootstrap_certificate(request['bootstrap'])
    write_json(out/'bootstrap.json', bootstrap)
    diagnostic['bootstrap'] = bootstrap
    if certificate.get('status') == 'certified' and validation.get('valid') is True:
        result['status'] = 'certified_finite_size'
        result['claim'] = f"Exact finite-size gap lower bound {certificate.get('gap_lower_bound', '?')} in {'the full space' if sector is None else 'the selected magnetization sector only'}. No uniform-family conclusion."
        diagnostic['tail_completeness'] = 'exact full-working-matrix inertia certificate'
    elif certificate.get('status') == 'certified_cluster' and validation.get('valid') is True:
        result['status'] = 'certified_low_energy_cluster'
        cluster_scope = 'the full finite Hilbert space' if sector is None else 'the selected magnetization sector only'
        result['claim'] = f"Certified low-energy cluster in {cluster_scope}: rank {certificate['low_band_rank']}, width at most {certificate['low_band_width_upper']}, separation at least {certificate['gap_above_cluster_lower']}. Ground multiplicity remains unknown."
        diagnostic['failure_class'] = 'ground_multiplicity_unresolved'
        diagnostic['tail_completeness'] = 'exact cluster separation; internal splittings unresolved'
    else:
        diagnostic['failure_class'] = 'tail_completeness_or_exact_certificate_unresolved'
    diagnostic['ground_multiplicity'] = certificate.get('ground_multiplicity')
    diagnostic['ground_multiplicity_source'] = 'inferred by exact certificate' if certificate.get('ground_multiplicity') is not None else 'unknown'
    result['reason'] = bootstrap['reason']
    result['certificate_status'] = certificate.get('status')
    result['validation_status'] = validation
    return result


def compute_stabilizer(request, out):
    """Specific proved family with an analytic low-energy/tail backend."""
    from fractions import Fraction
    from .stabilizer import find_thermal_seed, certify_target, projector_spectrum
    spec = request['model']
    if set(spec)-{'family', 'shape', 'h', 'target_gap', 'max_power', 'name'}:
        raise ValueError('Unsupported graph_state_projector model key')
    if request.get('solver') or request.get('certificate') or request.get('bootstrap'):
        raise ValueError('Graph-state analytic backend does not accept solver/certificate/bootstrap overrides')
    shape = spec.get('shape', [2])
    if not isinstance(shape, list) or not 1 <= len(shape) <= 6 or any(isinstance(x,bool) or not isinstance(x,int) or x<2 or x%2 for x in shape):
        raise ValueError('Graph-state shape requires 1..6 even integer lengths >=2')
    h = Fraction(spec.get('h', '1'))
    target = Fraction(spec.get('target_gap', str(h/2)))
    power = spec.get('max_power', 24)
    if isinstance(power,bool) or not isinstance(power,int) or not 1 <= power <= 100:
        raise ValueError('max_power must be an integer in [1,100]')
    record_stage(request, out, 'analytic_thermal_seed_and_bootstrap')
    result = find_thermal_seed(shape, target, h, power)
    write_json(out/'model.json', {'family':'graph_state_projector', 'shape':shape, 'h':str(h),
               'hamiltonian':'h/2 sum_i (I - X_i product_{j adjacent to i} Z_j)',
               'normalization':'unit projector coefficient h', 'scope':'finite simple graphs; rectangular periodic bootstrap family'})
    write_json(out/'resources.json', {'backend':'analytic binomial spectrum and rational scalar bootstrap',
               'basis_allocated':False, 'numerical_eigenpairs':0, 'working_trial_rank':1,
               'max_dimension_applies_to':'allocated finite matrices, none in this analytic backend',
               'wall_seconds':request['budget']['wall_seconds'], 'memory_mb':request['budget']['memory_mb']})
    write_json(out/'bootstrap.json', result)
    if 'seed' not in result:
        return {'status':'insufficient_evidence', 'reason':'No thermal seed met the target in the tested rational q grid',
                'claim':f'Analytic family gap is {h}; requested bootstrap target not certified by this grid.',
                'diagnostics':{'failure_class':'seed_search_inconclusive', 'minimal_seed_size':'not established'}}
    seed, cert = result['seed'], result['certificate']
    replay = certify_target(seed,target)
    # Distinct direct combinatorial small-graph checks of multiplicities/gap;
    # family-wide proof is algebraic CZ unitary equivalence documented in theory.
    checks = [sum(m for _,m in projector_spectrum(n,h)) == 2**n and projector_spectrum(n,h)[1][0] == h for n in range(1,9)]
    validation = {'exact_replay':replay == cert, 'combinatorial_checks_n_1_to_8':all(checks),
                  'proof_source':'theory/STABILIZER_BENCHMARK.md',
                  'limitation':'Code replay and finite tests complement, but do not replace, the documented algebraic proof.'}
    write_json(out/'candidate.json', {'evidence':'analytic_unitary_equivalence', 'trial_rank':1,
              'numerically_computed_eigenpairs':0, 'ground_energy':'0', 'first_excitation':str(h),
              'tail':'exact binomial multiplicities'})
    write_json(out/'certificate.json',cert)
    write_json(out/'validation.json',validation)
    verified = cert['target_verified'] and validation['exact_replay'] and all(checks)
    return {'status':'certified_uniform_family' if verified else 'insufficient_evidence',
            'claim':f'Graph-state projector family: exact analytic gap {h}; thermal-bootstrap lower bound {target} verified.' if verified else 'Validation failed.',
            'uniform_family_claim':bool(verified), 'reason':'Specific proved commuting-projector benchmark only; no extension to general spin models.',
            'diagnostics':{'physical_seed_shape':shape, 'seed_sites':seed['seed_volume'],
                           'temporal_seed_sites':seed['temporal_seed_volume'],
                           'full_hilbert_dimension':seed['full_hilbert_dimension'], 'trial_rank':1,
                           'trial_rank_kind':'analytically retained exact ground state',
                           'minimal_seed_size':'sufficient tested shape; minimality not established',
                           'numerical_low_energy_states_computed':0}}


def compute_ising(request, model, out):
    from .ising import diagnose_ising_obstruction
    edges = [(t[1], t[2], -t[4]) for t in model.terms]
    # The graph diagnostic uses polynomial graph storage, never a Hilbert basis.
    if model.n_sites > request['budget']['max_dimension']:
        return {'status':'resource_limit','reason':'Ising graph-node budget exceeded before minimum-cut allocation'}
    record_stage(request, out, 'analytic_ising_method_obstruction')
    try:
        diagnosis = diagnose_ising_obstruction(model.n_sites, edges)
    except ValueError as exc:
        if 'connected graph' in str(exc):
            return None
        raise
    replay = diagnose_ising_obstruction(model.n_sites, edges)
    validation = {'exact_replay':replay == diagnosis, 'independent_min_cut_check':'not run beyond 12 graph nodes'}
    if model.n_sites <= 12:
        cuts = [sum((w for i,j,w in edges if bool(mask & (1<<i)) != bool(mask & (1<<j))), Fraction(0))
                for mask in range(1, 1 << (model.n_sites-1))]
        validation['independent_min_cut_check'] = min(cuts) == Fraction(diagnosis['weighted_min_cut'])
    write_json(out/'model.json',model.summary())
    write_json(out/'resources.json',{'backend':'exact graph minimum cut and analytic Ising spectrum identity',
              'basis_allocated':False,'numerically_computed_eigenpairs':0,
              'full_hilbert_dimension':model.hilbert_dimension,'graph_nodes':model.n_sites,
              'graph_algorithm_cost':'O(n^3) rational operations; bit complexity additional'})
    write_json(out/'candidate.json',{'evidence':'analytic Ising cut identity', 'ground_degeneracy':2,
              'numerically_computed_eigenpairs':0})
    write_json(out/'certificate.json',diagnosis)
    write_json(out/'validation.json',validation)
    write_json(out/'bootstrap.json',{'status':'METHOD_OBSTRUCTION', 'purity_upper_bound':'1/2',
              'entry_impossible_for_threshold':'greater than 1/2', 'scope':'near-one thermal-purity criterion for this connected finite Ising model',
              'recommended_action':diagnosis['recommended_action'], 'uniform_family_claim':False})
    return {'status':'certified_finite_size','claim':f"Exact Ising gap above the two-dimensional ground space is {diagnosis['gap_above_ground_space']}. Near-one thermal-purity bootstrap is obstructed.",
            'reason':diagnosis['recommended_action'],'model_gapless':False,'uniform_family_claim':False,
            'diagnostics':{'failure_class':'rigorous_method_specific_obstruction', 'ground_degeneracy':2,
                           'failed_assumption':'unique_ground_state', 'U1_symmetry_present':True,
                           'cause':'degenerate_Gibbs_ground_state_mixture',
                           'physical_seed_sites':model.n_sites, 'full_hilbert_dimension':model.hilbert_dimension,
                           'minimum_seed_for_near_one_purity':'none within this degenerate family: purity never exceeds 1/2',
                           'trial_rank_remedy':False, 'larger_seed_remedy':False, 'lower_temperature_remedy':False,
                           'general_gap_proof_impossible':False}}


def certify_sector_partition(request, model, values, vectors, full_operator):
    import numpy as np
    from .sectors import certify_sectors_gap, certify_sectors_gap_from_vector
    budget = request['budget']
    cap = budget['exact_max_dimension']
    proposed = request.get('certificate', {})
    if not isinstance(proposed, dict) or set(proposed)-{'ground_energy','gap_lower_bound'}:
        raise ValueError('certificate supports ground_energy and gap_lower_bound')
    if len(values) < 2 and not {'ground_energy','gap_lower_bound'} <= set(proposed):
        return {'status':'insufficient_evidence','reason':'Need two numerical levels or explicit exact proposals'}, {'valid':False}
    ground = proposed.get('ground_energy', str(Fraction(float(values[0])).limit_denominator(10000))) if len(values) else proposed['ground_energy']
    higher = [v for v in values if v-values[0] > max(1e-7,10*budget['tolerance'])] if len(values) else []
    gap = proposed.get('gap_lower_bound', str(Fraction(float(0.9*(higher[0]-values[0]))).limit_denominator(10000)) if higher else None)
    if gap is None:
        return {'status':'insufficient_evidence','reason':'No proposed positive excitation gap'}, {'valid':False}
    def exact_ground():
        return certify_sectors_gap(model,ground,gap,max_sector_dimension=cap)
    certificate = exact_ground()
    replay_fn = exact_ground
    if not certificate.get('certified') and not proposed and len(values)>1:
        dims = model.sector_dimensions()
        states = full_operator.gapflow_basis.states
        index = {state:i for i,state in enumerate(states)}
        sector_indices = {m:[index[state] for state in model.basis(total_m2=m,max_dimension=cap).states] for m in dims}
        chosen = max(dims, key=lambda m:float(np.linalg.norm(vectors[sector_indices[m],0])))
        _, weights = model.exact_pencil(total_m2=chosen,max_dimension=cap)
        trial = vectors[sector_indices[chosen],0] / np.sqrt(np.asarray(weights,dtype=float))
        trial = [str(Fraction(float(x)).limit_denominator(100000)) for x in trial]
        threshold = str(Fraction(float(values[0]+0.9*(values[1]-values[0]))).limit_denominator(10000))
        def exact_vector():
            return certify_sectors_gap_from_vector(model,chosen,trial,threshold,max_sector_dimension=cap)
        certificate = exact_vector()
        replay_fn = exact_vector
    replayed = replay_fn() if certificate.get('certified') else {}
    stable = lambda c: {key:value for key,value in c.items() if key != 'elapsed_seconds'}
    replay_ok = certificate.get('certified',False) and stable(replayed) == stable(certificate)
    maximum_error = 0.0
    for m, dim in model.sector_dimensions().items():
        A, W = model.exact_pencil(total_m2=m,max_dimension=cap)
        weights = np.sqrt(np.asarray(W,dtype=float))
        exact_float = np.asarray(A,dtype=float) / weights[:,None] / weights[None,:]
        H = model.hamiltonian(total_m2=m,matrix_free=True,max_dimension=cap)
        for j in range(dim):
            unit = np.zeros(dim); unit[j] = 1
            maximum_error = max(maximum_error,float(np.max(np.abs(H@unit-exact_float[:,j]))))
    validation = {'valid':bool(replay_ok and maximum_error<1e-12 and certificate.get('coverage_complete')),
                  'exact_replay':bool(replay_ok), 'independent_exact_implementation':False,
                  'coverage_complete':certificate.get('coverage_complete',False),
                  'independent_model_representation_check':'Every Sz block: float matrix-free columns versus rational weighted pencil',
                  'maximum_matrix_entry_error':maximum_error}
    certificate['status'] = 'certified' if certificate.get('certified') else 'not_certified'
    return certificate,validation


def compute_pinned_ising(request, out):
    """Registered classical family with a proved comparison bound and transfer."""
    from .classical_seed import find_thermal_seed, certify_target
    spec = request['model']
    if set(spec)-{'family','shape','J','h','target_gap','max_power','name'}:
        raise ValueError('Unsupported pinned_ferromagnetic_ising model key')
    if request.get('solver') or request.get('certificate') or request.get('bootstrap'):
        raise ValueError('Pinned-Ising analytic backend does not accept solver/certificate/bootstrap overrides')
    shape = spec.get('shape',[2])
    if not isinstance(shape,list) or not shape or any(type(x) is not int or x<2 or x%2 for x in shape):
        raise ValueError('Pinned-Ising shape requires even integer lengths >=2')
    if any(isinstance(spec.get(key),bool) for key in ('J','h','target_gap')):
        raise ValueError('J, h and target_gap require rational numbers, not booleans')
    J, h = Fraction(spec.get('J','1')), Fraction(spec.get('h','1'))
    target = Fraction(spec.get('target_gap',str(h/2)))
    power = spec.get('max_power',24)
    if type(power) is not int or not 1<=power<=100:
        raise ValueError('max_power must be an integer in [1,100]')
    record_stage(request,out,'analytic_pinned_ising_seed_and_bootstrap')
    result = find_thermal_seed(shape,target,J,h,power)
    write_json(out/'model.json',{'family':'pinned_ferromagnetic_ising','shape':shape,'J':str(J),'h':str(h),
               'hamiltonian':'J/2 sum_edges (1-Z_i Z_j) + h/2 sum_i (1-Z_i)',
               'normalization':'Z eigenvalues +/-1; positive_direction_multigraph',
               'parameter_range':'J>=0 and h>0; no weak-coupling requirement'})
    write_json(out/'resources.json',{'backend':'analytic counted comparison and rational thermal bootstrap',
               'basis_allocated':False,'numerically_computed_eigenpairs':0,'working_trial_rank':1,
               'wall_seconds':request['budget']['wall_seconds'],'memory_mb':request['budget']['memory_mb']})
    write_json(out/'bootstrap.json',result)
    if 'seed' not in result:
        return {'status':'insufficient_evidence','claim':f'Analytic family gap is at least {h}; requested thermal-bootstrap target not established on the tested grid.',
                'reason':'No sufficient seed in the bounded rational q search',
                'diagnostics':{'failure_class':'seed_search_inconclusive','physical_gap_is_claimed_exact':False}}
    seed,certificate = result['seed'],result['certificate']
    replay = certify_target(seed,target)
    validation = {'valid':bool(certificate['target_verified'] and replay==certificate),
                  'exact_replay':replay==certificate,'independent_exact_implementation':False,
                  'proof_source':'theory/TRANSFER_ELIGIBILITY.md',
                  'model_to_seed_identity':'E(configuration)>=h*number_of_flipped_spins, giving Z<= (1+q)^N',
                  'limitation':'Replay checks rational arithmetic; the family conclusion also uses the documented analytic comparison and classical transfer proof.'}
    write_json(out/'candidate.json',{'evidence':'analytic counted spectral comparison','trial_rank':1,
               'numerically_computed_eigenpairs':0,'ground_energy':'0','ground_multiplicity':1,
               'analytic_gap_lower_bound':str(h),'physical_gap_is_claimed_exact':False,
               'tail_status':seed['tail_status']})
    write_json(out/'certificate.json',certificate)
    write_json(out/'validation.json',validation)
    passed = validation['valid']
    return {'status':'certified_uniform_family' if passed else 'insufficient_evidence',
            'claim':f'Pinned ferromagnetic Ising family: analytic gap at least {h}; thermal-bootstrap lower bound {target} verified.' if passed else 'Exact seed validation failed.',
            'reason':'Nonnegative ferromagnetic bonds and positive pinning field; comparison bound valid beyond weak coupling.',
            'uniform_family_claim':bool(passed),'model_gapless':False,
            'diagnostics':{'physical_seed_shape':shape,'seed_sites':seed['seed_volume'],
                           'temporal_seed_sites':seed['temporal_seed_volume'],
                           'full_hilbert_dimension_log2':seed['full_hilbert_dimension_log2'],
                           'trial_rank':1,'trial_rank_kind':'analytically retained ground state',
                           'numerical_low_energy_states_computed':0,'analytic_gap_lower_bound':str(h),
                           'physical_gap_is_claimed_exact':False,'weak_coupling_assumption':False,
                           'minimal_seed_size':'sufficient tested shape; minimality not established'}}


def compute_gapless(request,out):
    from .gapless import diagnose_gapless_family, FAMILY
    spec=request['model']
    if set(spec)-{'family','J','name'}:
        raise ValueError('Ferromagnetic Heisenberg family accepts family, J and name only')
    if request.get('solver') or request.get('certificate') or request.get('bootstrap'):
        raise ValueError('Gapless family theorem does not accept finite solver/certificate/bootstrap overrides')
    record_stage(request,out,'analytic_gapless_family_proof')
    diagnosis=diagnose_gapless_family(FAMILY,spec.get('J','1'))
    if diagnosis['status']!='CERTIFIED_GAPLESS_FAMILY':
        return {'status':'invalid_input','reason':diagnosis.get('reason','Unsupported gapless family input')}
    replay=diagnose_gapless_family(FAMILY,spec.get('J','1'))
    write_json(out/'model.json',{'family':FAMILY,'registered_alias':spec['family'],'J':diagnosis['J'],
              'hamiltonian':diagnosis['hamiltonian'],'boundary':diagnosis['boundary']})
    write_json(out/'resources.json',{'backend':'analytic projector-kernel and explicit magnon identity',
              'basis_allocated':False,'numerically_computed_eigenpairs':0,
              'wall_seconds':request['budget']['wall_seconds'],'memory_mb':request['budget']['memory_mb']})
    write_json(out/'candidate.json',{'evidence':'explicit analytic excited magnon state',
              'excitation_energy':diagnosis['gap_upper_bound'],'ground_space_dimension':'L+1',
              'numerically_computed_eigenpairs':0})
    write_json(out/'certificate.json',diagnosis)
    write_json(out/'validation.json',{'valid':replay==diagnosis,'analytic_metadata_replay':True,
              'proof_source':diagnosis['proof_reference'],'independent_exact_implementation':False})
    write_json(out/'bootstrap.json',{'status':'RIGOROUS_UNIFORM_POSITIVE_GAP_IMPOSSIBLE',
              'uniform_gap':'0','physical_gaplessness':True,'finite_size_gap_positive':True,
              'reason':'An explicit excited eigenstate has energy tending to zero as L grows.'})
    return {'status':'certified_gapless_family','claim':'Periodic spin-half ferromagnetic Heisenberg family: uniform gap is zero; every finite ring has a positive gap above its full ground space.',
            'reason':diagnosis['reason'],'uniform_family_claim':True,'model_gapless':True,
            'physical_gaplessness':True,'diagnostics':{'uniform_gap':'0','finite_size_gap_positive':True,
              'ground_space_dimension':'L+1','gap_upper_bound':diagnosis['gap_upper_bound'],
              'failure_class':'rigorous_physical_uniform_gaplessness',
              'positive_uniform_target_possible':False,'general_gaplessness_algorithm':False}}


def certify_unknown_low_band(request,model,sector,values):
    """Propose a cluster numerically, then certify it without assuming its rank."""
    import numpy as np
    from .low_band import certify_low_band, certify_sector_low_band
    cap = request['budget']['exact_max_dimension']
    dimension = model.dimension(sector)
    scale = max(1.0,abs(float(values[0])))
    margin = max(1e-6,100*request['budget']['tolerance']*scale)
    split = next((i for i in range(1,len(values)) if values[i]-values[0]>8*margin),None)
    if split is None:
        return {'certified':False,'status':'insufficient_cluster_proposal',
                'reason':'Partial spectrum does not exhibit a separated low cluster within the current trial rank'}, {'valid':False}
    lower = str(Fraction(float(values[0]-2*margin)).limit_denominator(10**9))
    upper = str(Fraction(float(values[split-1]+2*margin)).limit_denominator(10**9))
    threshold = str(Fraction(float((values[split-1]+values[split])/2)).limit_denominator(10**9))
    import importlib.util
    has_sympy = importlib.util.find_spec('sympy') is not None
    infer = dimension <= 16 and has_sympy
    use_partition = sector is None and model.preserves_total_sz and dimension > 16
    if dimension <= cap and not use_partition:
        A,W = model.exact_pencil(total_m2=sector,max_dimension=cap)
        replay_fn = lambda: certify_low_band(A,lower,upper,threshold,Wdiag=W,max_dimension=cap,
                                             infer_multiplicity=infer,distinct_root_max_dimension=16)
        blocks = {sector:dimension}
    elif sector is None and model.preserves_total_sz:
        replay_fn = lambda: certify_sector_low_band(model,lower,upper,threshold,max_sector_dimension=cap,
                                                    infer_multiplicity=True,distinct_root_max_dimension=16 if has_sympy else 1)
        blocks = model.sector_dimensions()
    else:
        return {'certified':False,'status':'unsupported','reason':'Exact low-band coverage unavailable'}, {'valid':False}
    certificate = replay_fn()
    replayed = replay_fn() if certificate.get('certified') else {}
    stable = lambda c: {key:value for key,value in c.items() if key!='elapsed_seconds'}
    replay_ok = bool(certificate.get('certified') and stable(replayed)==stable(certificate))
    maximum_error = 0.0
    for m,dim in blocks.items():
        A,W = model.exact_pencil(total_m2=m,max_dimension=cap)
        weights = np.sqrt(np.asarray(W,dtype=float))
        rational_representation = np.asarray(A,dtype=float)/weights[:,None]/weights[None,:]
        H = model.hamiltonian(total_m2=m,matrix_free=True,max_dimension=cap)
        for j in range(dim):
            unit=np.zeros(dim);unit[j]=1
            maximum_error=max(maximum_error,float(np.max(np.abs(H@unit-rational_representation[:,j]))))
    validation={'valid':bool(replay_ok and maximum_error<1e-12),'exact_replay':replay_ok,
                'independent_exact_implementation':False,'maximum_matrix_entry_error':maximum_error,
                'independent_model_representation_check':'Every covered block: numerical operator versus exact weighted pencil',
                'ground_multiplicity_assumed':False}
    certificate['source_status']=certificate.get('status')
    if certificate.get('certified'):
        if certificate.get('true_ground_gap_lower') is not None and certificate.get('ground_multiplicity') is not None:
            certificate['status']='certified'
            certificate['gap_lower_bound']=certificate['true_ground_gap_lower']
        else:
            certificate['status']='certified_cluster'
    return certificate,validation


# This switch records independent physical-composition review, not user input.
QUANTUM_ISING_PHYSICAL_AUDIT_CLEARED = True
QUANTUM_ISING_REVIEWED_SHA256 = {'gapflow/quantum_ising_interval.py': 'ab88cb3b0c66f5e6ae0d7b7d80a049566df5532a11f749bf125182c538508558', 'gapflow/bootstrap.py': '4547563b245b0417f126721806dfd60679cbaebe048735f4574fae2b78ec872d', 'theory/QUANTUM_ISING_SEEDS.md': '42a0724cea8a6f1b4409c69c709b1d596098da596cf0a6aa2ac4dc3b2d340209', 'theory/QUANTUM_ISING_INTERVAL.md': '6f0ba52a47d25bcbef43ccef48abf19af1af0f906e30454726881422cb5bac3a', 'theory/TRANSFER_ELIGIBILITY.md': '06ea50e49f6e775a415e2cfd79aa95b94fc0fd450f0f0025fb896329fa986369', 'audit/QUANTUM_ISING_CERTIFICATE_REVIEW.md': '0e9c4d584cb72129edb689dcdfde034b5bf7b4e29a73fa5cde859af7d4555428'}


def compute_quantum_ising(request,out):
    from .quantum_ising_interval import canonical_seed_interval
    spec=request['model']
    root=Path(__file__).resolve().parent.parent
    observed={name:hashlib.sha256((root/name).read_bytes()).hexdigest() if (root/name).exists() else None
              for name in QUANTUM_ISING_REVIEWED_SHA256}
    changed=[name for name in observed if observed[name]!=QUANTUM_ISING_REVIEWED_SHA256[name]]
    write_json(out/'physical_review_sources.json',{'expected_sha256':QUANTUM_ISING_REVIEWED_SHA256,
               'observed_sha256':observed,'matched':not changed,'changed_or_missing':changed})
    if changed:
        return {'status':'proof_source_mismatch','claim':'No physical certificate accepted: reviewed proof sources changed or are missing.',
                'reason':'Independent review must be reconciled with the current source artifacts.',
                'diagnostics':{'changed_or_missing_review_sources':changed}}
    if set(spec)-{'family','J','h','n','beta','digits','name','bond_convention'}:
        raise ValueError('Quantum Ising accepts J, h, optional n, beta, digits, name and bond_convention')
    if request.get('solver') or request.get('certificate') or request.get('bootstrap'):
        raise ValueError('Quantum-Ising family backend does not accept finite solver/certificate/bootstrap overrides')
    if spec.get('bond_convention','positive_direction_multigraph')!='positive_direction_multigraph':
        raise ValueError('Quantum Ising requires periodic positive_direction_multigraph bonds')
    if 'J' not in spec or 'h' not in spec or any(isinstance(spec.get(key),bool) for key in ('J','h','beta')):
        raise ValueError('Exact rational J and h are required; booleans are not parameters')
    J,h=Fraction(spec['J']),Fraction(spec['h'])
    if not h>J>=0:
        raise ValueError('Registered Quantum-Ising family requires h>J>=0')
    digits=spec.get('digits',50)
    if type(digits) is not int or not 20<=digits<=100:
        raise ValueError('digits must be an integer in [20,100]')
    ns=[spec['n']] if 'n' in spec else [2,4,8,16,32,64]
    if any(type(n) is not int or n<2 or n>64 or n & (n-1) for n in ns):
        raise ValueError('n must be a dyadic integer in [2,64]')
    betas=[Fraction(spec['beta'])] if 'beta' in spec else list(map(Fraction,[1,2,4,8,16]))
    if any(b<=0 for b in betas):
        raise ValueError('beta must be positive')
    bridge=2*(h-J)
    write_json(out/'model.json',{'family':'quantum_ising_chain','J':str(J),'h':str(h),
              'hamiltonian':'H_L=-J sum_i Z_i Z_(i+1)-h sum_i X_i',
              'normalization':'Pauli X/Z eigenvalues +/-1; periodic positive_direction_multigraph, doubled L=2 bond',
              'parameter_range':'h>J>=0','ground_multiplicity_input':None})
    write_json(out/'resources.json',{'backend':'Exact rational single-particle mode and partition enclosures',
              'planned_seed_sizes':ns,'planned_betas':list(map(str,betas)),'precision_digits':digits,
              'maximum_seed_sizes':len(ns)*len(betas),'many_body_basis_allocated':False,
              'many_body_eigenpairs_computed':0,'hard_wall_seconds':request['budget']['wall_seconds'],
              'hard_memory_mb':request['budget']['memory_mb']})
    trials=[]
    accepted=None
    for n in ns:
        for beta in betas:
            record_stage(request,out,f'quantum_ising_seed_n{n}_beta{beta}')
            trial={'n':n,'beta':str(beta),'state':'in_progress',
                   'physical_largest_seed_sites':2*n,'physical_hilbert_dimension':str(2**(2*n)),
                   'distinct_single_particle_modes_enclosed':6*n,'single_particle_mode_visits_partition':10*n,
                   'many_body_eigenpairs_computed':0}
            trials.append(trial)
            write_json(out/'seed_trials.json',trials)
            started=time.monotonic()
            try:
                seed=canonical_seed_interval(n,beta,J,h,digits=digits)
            except (ValueError,ZeroDivisionError,OverflowError) as exc:
                trial.update(state='interval_seed_failed',reason=str(exc),elapsed_seconds=time.monotonic()-started)
                write_json(out/'seed_trials.json',trials)
                continue
            replay=seed['bootstrap']
            label=f'seed_{len(trials):03d}.json'
            write_json(out/label,seed)
            positive=replay.get('status')=='VERIFIED_CONDITIONAL' and Fraction(replay.get('gap_lower','0'))>0
            trial.update(state='positive_conditional_replay' if positive else 'no_positive_replay',
                         elapsed_seconds=time.monotonic()-started,artifact=label,
                         bootstrap_status=replay.get('status'),gap_lower=replay.get('gap_lower'),
                         accepted_scalar_scope=replay.get('scope'),purity_intervals=seed['purity_intervals'])
            write_json(out/'seed_trials.json',trials)
            if positive:
                accepted=seed
                break
        if accepted is not None:
            break
    write_json(out/'candidate.json',{'evidence':'Exact rational partition enclosures from complete parity formulas',
              'many_body_eigenpairs_computed':0,'tested_seed_count':len(trials),
              'smallest_seed_claim':'first positive result in the stated tested order, not a global minimum',
              'ground_multiplicity_input':None,'analytic_bridge_lower_bound_proposed':str(bridge)})
    if accepted is None:
        write_json(out/'bootstrap.json',{'status':'INCONCLUSIVE_WITHIN_TESTED_GRID','trials':trials,
                  'uniform_family_claim':False})
        return {'status':'insufficient_evidence','claim':'No positive thermal-bootstrap certificate found in the bounded tested grid.',
                'reason':'Analytic bridge evidence is recorded separately from bootstrap success.',
                'diagnostics':{'analytic_bridge_gap_lower_bound':str(bridge),'tested_seed_count':len(trials),
                               'physical_audit_cleared':QUANTUM_ISING_PHYSICAL_AUDIT_CLEARED,
                               'failure_class':'seed_search_inconclusive','global_minimum_seed':'not established'}}
    replay=accepted['bootstrap']
    composed=min(Fraction(replay['gap_lower']),bridge)
    proof={'physical_audit_cleared':QUANTUM_ISING_PHYSICAL_AUDIT_CLEARED,
           'reviewed_source_sha256':QUANTUM_ISING_REVIEWED_SHA256,
           'partition_evidence':'EXACT_RATIONAL_PARTITION_SEED_ENCLOSURES',
           'scalar_bootstrap_gap_lower_bound':replay['gap_lower'],
           'scalar_accepted_scope':replay.get('scope'),
           'analytic_all_finite_sizes_bridge_gap_lower_bound':str(bridge),
           'composed_uniform_gap_lower_bound':str(composed),
           'composition_rule':'minimum of scalar replay lower bound and analytic all-L>=2 bridge',
           'bridge_scope':'all integer L>=2; covers all sizes outside the accepted scalar bootstrap scope',
           'ground_multiplicity':1,'ground_multiplicity_source':'derived from the paramagnetic parity/Fourier proof; not supplied',
           'proof_sources':['theory/QUANTUM_ISING_SEEDS.md','theory/QUANTUM_ISING_INTERVAL.md','theory/TRANSFER_ELIGIBILITY.md'],
           'uniform_family_claim':QUANTUM_ISING_PHYSICAL_AUDIT_CLEARED,
           'status':'CERTIFIED_UNIFORM_FAMILY' if QUANTUM_ISING_PHYSICAL_AUDIT_CLEARED else 'CONDITIONAL_PHYSICAL_REVIEW_PENDING'}
    write_json(out/'certificate.json',proof)
    write_json(out/'bootstrap.json',accepted)
    write_json(out/'validation.json',{'valid':QUANTUM_ISING_PHYSICAL_AUDIT_CLEARED,
              'physical_composition_audit':'cleared' if QUANTUM_ISING_PHYSICAL_AUDIT_CLEARED else 'pending',
              'arithmetic':'Exact rational outward intervals and scalar replay',
              'many_body_eigenpairs_computed':0})
    cleared=QUANTUM_ISING_PHYSICAL_AUDIT_CLEARED
    return {'status':'certified_uniform_family' if cleared else 'conditional_bootstrap_certificate',
            'claim':f'Periodic quantum Ising family: uniform gap at least {composed}.' if cleared else f'Exact interval seeds give conditional scalar gap bound {replay["gap_lower"]}; physical composition review is pending.',
            'reason':'Finite-size bridge composed with accepted scalar-bootstrap scope.' if cleared else 'The positive scalar result is not promoted to a physical uniform-family certificate before independent review.',
            'uniform_family_claim':cleared,'diagnostics':{'seed_n':accepted['n'],'beta':accepted['beta'],
              'physical_largest_seed_sites':2*accepted['n'],'physical_hilbert_dimension':str(2**(2*accepted['n'])),
              'single_particle_modes_enclosed':accepted['distinct_single_particle_modes_enclosed'],
              'many_body_eigenpairs_computed':0,'tested_seed_count':len(trials),
              'minimal_seed_size':'first positive tested pair only; global minimality unknown',
              'accepted_scalar_scope':replay.get('scope'),'proposed_composed_lower_bound':str(composed),
              'analytic_bridge_gap_lower_bound':str(bridge),'ground_multiplicity_assumption':None}}
