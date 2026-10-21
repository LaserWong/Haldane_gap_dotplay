"""Optional seed-size forecasts from measured bootstrap defects.

These forecasts guide the next computation. They never establish a minimal
seed, a gap, or impossibility. Samples must belong to the same model, shape
family, temperature/rank optimization protocol and certificate criterion.
"""
import math
import json
from copy import deepcopy
from fractions import Fraction
import numpy as np


_PROVENANCE_FIELDS = (
    'model_family', 'geometry_family', 'temperature_protocol',
    'trial_rank_protocol', 'certificate_criterion',
)


def _json_signature(value):
    """Compare declared settings without Python's True == 1 coercion."""
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise ValueError('Provenance settings require string keys')
        for item in value.values():
            _json_signature(item)
    elif isinstance(value, list):
        for item in value:
            _json_signature(item)
    elif value is not None and not isinstance(value, (str, int, float, bool)):
        raise ValueError('Provenance settings must contain finite JSON values')
    try:
        return json.dumps(value, sort_keys=True, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError('Provenance settings must contain finite JSON values') from exc


def _sample_compatibility(samples, threshold):
    """Check supplied declarations, without revalidating their source artifacts."""
    missing = []
    observed = {}
    for sample in samples:
        n = sample['linear_size']
        provenance = sample['provenance']
        if provenance is None:
            missing.append({'linear_size': n, 'field': 'provenance'})
            continue
        if not isinstance(provenance, dict):
            raise ValueError('provenance must be an object or absent')
        if provenance.keys() - set(_PROVENANCE_FIELDS):
            raise ValueError('Unknown provenance fields')
        for field in _PROVENANCE_FIELDS:
            descriptor = provenance.get(field)
            if descriptor is None:
                missing.append({'linear_size': n, 'field': field})
                continue
            if not isinstance(descriptor, dict):
                raise ValueError(f'{field} must be an object')
            required = {'id', 'settings'}
            if field == 'certificate_criterion':
                required.add('threshold')
            if descriptor.keys() - required:
                raise ValueError(f'Unknown {field} fields. Put parameters in settings')
            for key in sorted(required):
                path = f'{field}.{key}'
                value = descriptor.get(key)
                if value is None:
                    missing.append({'linear_size': n, 'field': path})
                    continue
                if key == 'id':
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(f'{path} must be a nonempty string')
                elif key == 'settings':
                    if not isinstance(value, dict):
                        raise ValueError(f'{path} must be an object')
                else:
                    try:
                        value = Fraction(str(value))
                    except (ValueError, ZeroDivisionError) as exc:
                        raise ValueError(f'{path} must be rational and lie in (0,1)') from exc
                    if not 0 < value < 1:
                        raise ValueError(f'{path} must be rational and lie in (0,1)')
                    value = descriptor[key] = str(value)
                observed.setdefault(path, []).append((n, _json_signature(value)))

    conflicts = []
    for field, values in sorted(observed.items()):
        if len({value for n, value in values}) > 1:
            conflicts.append({'field': field, 'linear_sizes': [n for n, value in values]})
    threshold_field = 'certificate_criterion.threshold'
    wrong_threshold = [n for n, value in observed.get(threshold_field, [])
                       if value != _json_signature(str(threshold))]
    if wrong_threshold:
        conflicts.append({'field': threshold_field, 'linear_sizes': wrong_threshold,
                          'requested_threshold': str(threshold)})
    return {
        'status': 'incompatible' if conflicts else 'unverified' if missing else 'verified',
        'scope': 'declared_metadata_only',
        'source_artifacts_reverified': False,
        'missing_metadata': missing,
        'conflicts': conflicts,
    }


def forecast_seed_size(records, threshold, max_size=None):
    """Forecast only for matching per-record provenance and an exact threshold.

    Each provenance descriptor has an immutable definition id and a settings
    object. The certificate descriptor also binds the threshold. Missing legacy
    metadata blocks forecasting. See docs/RESOURCE_ESTIMATION.md for the schema.
    """
    if not isinstance(records,list) or not records:
        raise ValueError('Nonempty defect records required')
    threshold_exact=Fraction(str(threshold))
    threshold=float(threshold_exact)
    if not 0<threshold_exact<1 or not math.isfinite(threshold):
        raise ValueError('threshold must be finite and lie in (0,1)')
    if max_size is not None and (isinstance(max_size,bool) or not isinstance(max_size,int) or max_size<2):
        raise ValueError('max_size must be an integer >=2')
    rows=[]
    samples=[]
    for row in records:
        if not isinstance(row,dict) or not {'linear_size','defect_upper'} <= row.keys():
            raise ValueError('Every sample requires linear_size and defect_upper')
        n=row['linear_size'];u_exact=Fraction(str(row['defect_upper']));u=float(u_exact)
        if isinstance(n,bool) or not isinstance(n,int) or n<2:
            raise ValueError('linear_size must be an integer >=2')
        if not 0<u_exact<=1 or not math.isfinite(u) or u==0:
            raise ValueError('defect_upper must lie in (0,1]')
        if row.get('evidence') not in ('certified_bound','floating_estimate'):
            raise ValueError('Every sample requires an explicit evidence label')
        rows.append((n,u_exact,row['evidence']))
        samples.append({'linear_size':n,'defect_upper':str(u_exact),'evidence':row['evidence'],
                        'defect_at_or_below_threshold':u_exact<=threshold_exact,
                        'provenance':deepcopy(row.get('provenance'))})
    if len({x[0] for x in rows})!=len(rows):raise ValueError('Duplicate linear sizes')
    rows.sort()
    samples.sort(key=lambda sample: sample['linear_size'])
    compatibility = _sample_compatibility(samples, threshold_exact)
    base={'smallest_tested_sufficient_size':None,
          'true_minimum_size':None,'minimality_proved':False,'uniform_gap_proved':False,
          'model_gapless':'not established','assumption':'Supplied provenance accurately describes each sample and its complete computation protocol.',
          'prediction_is_certified':False,'input_bound_certification_reverified':False,
          'threshold':str(threshold_exact),'sample_compatibility':compatibility,'samples':samples}
    if compatibility['status'] != 'verified':
        incompatible = compatibility['status'] == 'incompatible'
        return dict(base, status='INCOMPATIBLE_SAMPLES' if incompatible else 'UNVERIFIED_SAMPLE_COMPATIBILITY',
                    prediction=None,
                    reason='Conflicting sample provenance or requested threshold. Separate the data before forecasting.' if incompatible else
                           'Sample provenance is incomplete. Recover the missing source information before forecasting.')
    successful=[n for n,u,e in rows if e=='certified_bound' and u<=threshold_exact]
    if successful:
        return dict(base,status='TESTED_SUFFICIENT_SCALAR_SEED',prediction=None,
                    smallest_tested_sufficient_size=min(successful),
                    reason='Threshold reached by a certified scalar bound. Model-transfer hypotheses and finite-size bridge still require verification.')
    if len(rows)<3:
        return dict(base,status='INSUFFICIENT_PILOT_DATA',prediction=None,
                    reason='At least three distinct pilot sizes are required for this empirical forecast.')
    x=np.array([n for n,u,e in rows],dtype=float);y=np.log([float(u) for n,u,e in rows])
    slope,intercept=np.polyfit(x,y,1);fit=intercept+slope*x
    rms=float(np.sqrt(np.mean((fit-y)**2)))
    if slope>=0:
        return dict(base,status='NO_IMPROVING_TREND',prediction=None,log_defect_slope=float(slope),
                    reason='This fit provides no finite crossing estimate. It does not prove that a larger seed or another criterion cannot work.')
    crossing=float((math.log(threshold)-intercept)/slope)
    # Give a conservative next even test size, not a guaranteed sufficient size.
    next_even=max(2*math.ceil(crossing/2),2*math.ceil((x[-1]+1)/2))
    beyond=max_size is not None and next_even>max_size
    return dict(base,status='FORECAST_OUTSIDE_SIZE_BUDGET' if beyond else 'HEURISTIC_NEXT_SEED',
                prediction={'candidate_even_linear_size':next_even,'continuous_crossing':crossing,
                            'log_defect_slope':float(slope),'log_residual_rms':rms,
                            'fit_model':'log(u)=a+b*n','largest_observed_size':int(x[-1]),
                            'extrapolation_ratio':next_even/x[-1]},
                reason='Heuristic extrapolation only. Recompute and certify the proposed seed before accepting any bound.')
