"""Analytic true-gapless control; not a general gaplessness decision procedure.

The proof applies only to the explicitly constructed spin-half ferromagnetic
Heisenberg periodic family. Numerical checks are independent finite-size tests,
not the evidence establishing the all-size result. See theory/GAPLESS_CONTROL.md.
"""
from fractions import Fraction
import math

from .model import Model

FAMILY = 'ferromagnetic_spin_half_heisenberg_cycle'


def _coupling(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValueError('J must be an exact rational string or integer')
    try:
        value = Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise ValueError('J must be a positive rational') from None
    if value <= 0:
        raise ValueError('J must be positive')
    return value


def _length(length):
    if isinstance(length, bool) or not isinstance(length, int) or length < 2:
        raise ValueError('L must be an integer at least 2')
    return length


def diagnose_gapless_family(family=FAMILY, J='1'):
    """Return the explicit analytic theorem, with no finite-size computation.

    This function does not infer gaplessness from failed certification, degenerate
    ground states, numerical fitting, or an arbitrary user-supplied Hamiltonian.
    """
    try:
        if family != FAMILY:
            raise ValueError('Unsupported family; no gaplessness conclusion')
        coupling = _coupling(J)
    except (ValueError, TypeError) as exc:
        return {'status': 'INVALID_INPUT', 'physical_gaplessness': False,
                'reason': str(exc)}
    return {
        'status': 'CERTIFIED_GAPLESS_FAMILY',
        'family': FAMILY, 'J': str(coupling),
        'physical_gaplessness': True,
        'scope': 'All integer L >= 2, fixed positive rational J, full Hilbert space',
        'hamiltonian': 'H_L = J sum_i (1/4 - S_i dot S_(i+1))',
        'boundary': 'Periodic positive-direction multigraph; L=2 has two bonds',
        'ground_energy': '0', 'ground_space_dimension': 'L+1',
        'finite_size_gap_positive': True,
        'gap_definition': 'Smallest energy strictly above the entire ground eigenspace',
        'gap_upper_bound': 'J*(1-cos(2*pi/L)) <= 2*pi^2*J/L^2',
        'uniform_gap': '0',
        'proof_kind': 'Analytic projector-kernel and explicit orthogonal magnon proof',
        'proof_reference': 'theory/GAPLESS_CONTROL.md',
        'reason': 'An explicit excited eigenstate has positive energy tending to zero.',
        'general_gaplessness_algorithm': False,
    }


def ferromagnetic_cycle(length, J='1'):
    """Existing builder's unshifted model: add J*L/4 I to obtain H_L."""
    length, coupling = _length(length), _coupling(J)
    return Model.from_dict({
        'name': 'Ferromagnetic gapless control', 'spin': 0.5,
        'geometry': {'type': 'lattice', 'shape': [length], 'periodic': True,
                     'bond_convention': 'positive_direction_multigraph'},
        'terms': [{'type': 'heisenberg', 'J': str(-coupling)}],
    })


def numerical_control_check(length, J='1'):
    """Bounded floating-point check of all sectors, L=2..10 only.

    Reports every eigenvalue via exhaustive Sz blocks (largest block 252),
    numerical ground multiplicity, and magnon residual. No exact-proof status.
    """
    import numpy as np
    length, coupling = _length(length), _coupling(J)
    if length > 10:
        raise ValueError('Numerical control is explicitly limited to L <= 10')
    # Normalize by J before testing, avoiding ill-conditioned tiny/huge scales.
    model = ferromagnetic_cycle(length, '1')
    spectra = []
    for total_m2, dimension in sorted(model.sector_dimensions().items()):
        block = model.hamiltonian(total_m2, matrix_free=False, max_dimension=252)
        matrix = block.toarray() + length/4*np.eye(dimension)
        spectra.extend(np.linalg.eigvalsh(matrix).tolist())
    spectrum = np.sort(spectra)
    tolerance = 1e-10
    sector = model.hamiltonian(length-2, matrix_free=False, max_dimension=10)
    positions = [state.index(0) for state in sector.gapflow_basis.states]
    magnon = np.exp(2j*np.pi*np.asarray(positions)/length)/math.sqrt(length)
    expected = 2*math.sin(math.pi/length)**2
    residual = np.linalg.norm(sector@magnon + (length/4-expected)*magnon)
    positive = spectrum[spectrum > tolerance]
    return {
        'evidence': 'floating_point_check_only', 'L': length, 'J': str(coupling),
        'full_dimension': 2**length, 'covered_dimension': len(spectra),
        'ground_multiplicity': int(np.sum(abs(spectrum) <= tolerance)),
        'minimum_energy_over_J': float(spectrum[0]),
        'gap_over_J': float(positive[0]),
        'magnon_energy_over_J': expected,
        'magnon_residual_over_J': float(residual),
        'magnon_norm': float(np.linalg.norm(magnon)),
        'symmetric_ground_overlap': float(abs(np.sum(magnon)/math.sqrt(length))),
        'quadratic_upper_bound_over_J': 2*math.pi**2/length**2,
    }
