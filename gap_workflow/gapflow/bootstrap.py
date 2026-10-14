"""Exact scalar staircase replay. Never establishes a model's uniform gap by itself.

Proof-reference fields are declarations requiring external review, not trusted proof
objects. Canonical basepoint checks prevent relabeling or permuting staircase edges.
"""
from fractions import Fraction as F


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise ValueError('Exact scalar inputs must be integers or rational strings')
    return F(value)


def down(value, digits=18):
    scale = 10 ** digits
    return F(value.numerator * scale // value.denominator, scale)


def log_lower(value, terms=80):
    """Positive atanh partial sums, with exact range reduction."""
    value = rational(value)
    if value <= 1:
        raise ValueError('Positive logarithm requires an argument greater than one')
    power = 0
    while value >= 2:
        value /= 2
        power += 1
    def unit(x):
        z = (x - 1) / (x + 1)
        return 2 * sum((z ** (2*j+1) / (2*j+1) for j in range(terms)), F(0))
    return power * unit(F(2)) + unit(value)


def canonical_edges(lengths, beta, lower):
    """Build explicitly labeled canonical edges for already certified bounds."""
    lengths = list(lengths)
    beta = rational(beta)
    axes = [f'x{i+1}' for i in range(len(lengths))] + ['beta']
    if len(lower) != len(axes):
        raise ValueError('Wrong number of staircase bounds')
    edges = []
    for axis, bound in zip(axes, lower):
        edges.append(dict(axis=axis, base_lengths=list(lengths),
                          base_beta=str(beta), lower=str(rational(bound))))
        if axis == 'beta':
            beta *= 2
        else:
            lengths[axes.index(axis)] *= 2
    return edges


def cycle(lower, digits=18):
    """One exact outward-rounded sequential queue cycle for k coordinates."""
    queue = [rational(q) for q in lower]
    steps = []
    for _ in range(len(queue)):
        z = F(1)
        for j, q in enumerate(queue):
            z *= q ** (2 ** (len(queue)-1-j))
        if not 0 < z <= 1:
            return None, steps
        new = down(1 - (1-z)**2 / (2*z*z), digits)
        steps.append({'joint_lower': str(z), 'updated_lower': str(new)})
        if new <= 0:
            return None, steps
        queue = queue[1:] + [new]
    return queue, steps


def bootstrap_certificate(data):
    """Replay declared certified inputs, returning conditional scalar evidence only.

    Input fields: dimension, lengths, beta, edges, model_to_seed_proof,
    max_rounds (default 32), digits (default 18), mode (dedicated or general).
    Each edge contains axis, base_lengths, base_beta and lower.
    """
    result = {'status': 'INVALID_INPUT', 'uniform_family_claim': False,
              'physical_proof_verified': False,
              'claim': 'No physical model gap is certified by this scalar adapter.',
              'model_gapless': 'not established', 'updates': []}
    try:
        if not isinstance(data, dict):
            raise ValueError('bootstrap must be an object')
        d = data['dimension']
        if isinstance(d, bool) or not isinstance(d, int) or d < 1:
            raise ValueError('dimension must be a positive integer')
        if d > 8:
            result.update(status='RESOURCE_LIMIT', reason='Scalar dimension cap is 8')
            return result
        lengths = data['lengths']
        if not isinstance(lengths, list) or len(lengths) != d or any(
                isinstance(n, bool) or not isinstance(n, int) or n < 2 or n % 2 for n in lengths):
            raise ValueError('Every spatial seed length must be an even integer >=2')
        lengths = list(lengths)
        beta = rational(data['beta'])
        if beta <= 0:
            raise ValueError('beta must be positive')
        rounds = data.get('max_rounds', 32)
        digits = data.get('digits', 18)
        if isinstance(rounds, bool) or not isinstance(rounds, int) or not 0 <= rounds <= 128:
            raise ValueError('max_rounds must be an integer from 0 to 128')
        if isinstance(digits, bool) or not isinstance(digits, int) or not 12 <= digits <= 100:
            raise ValueError('digits must be an integer from 12 to 100')
        mode = data.get('mode', 'dedicated' if d <= 2 else 'general')
        if mode not in {'dedicated', 'general'} or mode == 'dedicated' and d > 2:
            raise ValueError('Dedicated adapters exist only for d=1 and d=2')
        edges = data['edges']
        if not isinstance(edges, list) or len(edges) != d+1:
            raise ValueError('Exactly d+1 labeled staircase edges are required')
        lower = [rational(edge['lower']) for edge in edges]
        if any(not 0 < q <= 1 for q in lower):
            raise ValueError('Purity lower bounds must lie in (0,1]')
        expected = canonical_edges(lengths, beta, lower)
        for edge, wanted in zip(edges, expected):
            if (edge.get('axis') != wanted['axis'] or
                    edge.get('base_lengths') != wanted['base_lengths'] or
                    rational(edge['base_beta']) != rational(wanted['base_beta'])):
                raise ValueError('Noncanonical or permuted staircase basepoint. Supply newly certified canonical edges')
        proof = data.get('model_to_seed_proof')
        if (not isinstance(proof, dict) or proof.get('verified') is not True or
                not isinstance(proof.get('evidence'), list) or not proof['evidence'] or
                any(not isinstance(p, str) or not p.strip() for p in proof['evidence'])):
            result.update(status='UNSUPPORTED', reason='Missing model-to-seed proof declaration and evidence references')
            return result
        result['proof_declaration'] = proof
        result['proof_declaration_trusted'] = False
        result['required_external_checks'] = ['model-to-seed proof and artifact identity',
            'exact transfer in every spatial direction', 'complete omitted-spectrum bounds',
            'signed all-integer interpolation', 'all early windows and smallest-size bridge',
            'independent physical and arithmetic verification']
        if mode == 'dedicated':
            K, threshold = (5, F(1,100)) if d == 1 else (32, F(1,500))
        else:
            factor = 4 * 8 ** (d-1)
            K = max((2 ** (d+1)-1)**2, 2*factor)
            threshold = min(F(1,4*K), F(1,100*8**(d-1)))
        result.update(mode=mode, dimension=d, contraction_constant=K,
                      entry_threshold=str(threshold), arithmetic='exact rational outward rounding')
        lower = [down(q, digits) for q in lower]
        for j in range(rounds+1):
            u = max(1-q for q in lower)
            if u == 0:
                result.update(status='INCONCLUSIVE', reason='Exact rank-one inputs require separate physical treatment')
                return result
            if u <= threshold:
                gap = down(log_lower(1/(K*u))/beta, 12)
                result.update(status='VERIFIED_CONDITIONAL', rounds=j, lengths=lengths,
                    beta=str(beta), edges=canonical_edges(lengths,beta,lower), u=str(u),
                    gap_lower=str(gap), gap_lower_display=float(gap),
                    claim='Scalar inequalities pass conditional on separately verified physical and coverage assumptions.',
                    reason='Exact sequential recurrence entered its proved contraction region',
                    scope={'type':'common_scale_integer_boxes', 'base_lengths':lengths,
                           'hypercubes_all_L_ge_seed': len(set(lengths)) == 1,
                           'arbitrary_aspect_ratios':False, 'small_size_bridge_verified':False})
                return result
            if j == rounds:
                result.update(status='RESOURCE_LIMIT', reason='Maximum replay rounds reached. This is not an exclusion')
                return result
            new, steps = cycle(lower,digits)
            record = {'round':j+1, 'input_edges':canonical_edges(lengths,beta,lower), 'steps':steps}
            result['updates'].append(record)
            if new is None:
                result.update(status='INCONCLUSIVE', reason='A supplied scalar lower bound left the positive purity domain')
                return result
            lower = new
            lengths = [2*n for n in lengths]
            beta *= 2
            record['output_edges'] = canonical_edges(lengths,beta,lower)
        raise RuntimeError('Unreachable replay state')
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as exc:
        result.update(status='INVALID_INPUT', reason=str(exc))
        return result
