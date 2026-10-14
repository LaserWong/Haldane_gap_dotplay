"""Optional seed-size forecasts from measured bootstrap defects.

These forecasts guide the next computation. They never establish a minimal
seed, a gap, or impossibility. Samples must belong to the same model, shape
family, temperature/rank optimization protocol and certificate criterion.
"""
import math
from fractions import Fraction
import numpy as np


def forecast_seed_size(records, threshold, max_size=None):
    if not isinstance(records,list) or not records:
        raise ValueError('Nonempty defect records required')
    threshold_exact=Fraction(str(threshold))
    threshold=float(threshold_exact)
    if not 0<threshold_exact<1 or not math.isfinite(threshold):
        raise ValueError('threshold must be finite and lie in (0,1)')
    rows=[]
    for row in records:
        n=row['linear_size'];u_exact=Fraction(str(row['defect_upper']));u=float(u_exact)
        if isinstance(n,bool) or not isinstance(n,int) or n<2:
            raise ValueError('linear_size must be an integer >=2')
        if not 0<u_exact<=1 or not math.isfinite(u) or u==0:
            raise ValueError('defect_upper must lie in (0,1]')
        if row.get('evidence') not in {'certified_bound','floating_estimate'}:
            raise ValueError('Every sample requires an explicit evidence label')
        rows.append((n,u_exact,row['evidence']))
    if len({x[0] for x in rows})!=len(rows):raise ValueError('Duplicate linear sizes')
    rows.sort();successful=[n for n,u,e in rows if e=='certified_bound' and u<=threshold_exact]
    base={'smallest_tested_sufficient_size':min(successful) if successful else None,
          'true_minimum_size':None,'minimality_proved':False,'uniform_gap_proved':False,
          'model_gapless':'not established','assumption':'Comparable optimized bootstrap defects for the same family and criterion.',
          'prediction_is_certified':False,'input_bound_certification_reverified':False,'samples':[{'linear_size':n,'defect_upper':str(u),'evidence':e} for n,u,e in rows]}
    if successful:
        return dict(base,status='TESTED_SUFFICIENT_SCALAR_SEED',prediction=None,
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
    if max_size is not None and (isinstance(max_size,bool) or not isinstance(max_size,int) or max_size<2):
        raise ValueError('max_size must be an integer >=2')
    beyond=max_size is not None and next_even>max_size
    return dict(base,status='FORECAST_OUTSIDE_SIZE_BUDGET' if beyond else 'HEURISTIC_NEXT_SEED',
                prediction={'candidate_even_linear_size':next_even,'continuous_crossing':crossing,
                            'log_defect_slope':float(slope),'log_residual_rms':rms,
                            'fit_model':'log(u)=a+b*n','largest_observed_size':int(x[-1]),
                            'extrapolation_ratio':next_even/x[-1]},
                reason='Heuristic extrapolation only. Recompute and certify the proposed seed before accepting any bound.')
