"""Exact positive-gap / degenerate-ground-space obstruction benchmark.

H = -sum_(i,j) J_ij Sz_i Sz_j, Sz=+/-1/2, J_ij>0.
No Hilbert basis is allocated by the minimum-cut diagnostic. Float weights
are deliberately rejected: supply integer, Fraction, or rational strings.
"""
from fractions import Fraction


def _graph(n_sites, edges):
    if type(n_sites) is not int or n_sites < 2:
        raise ValueError('n_sites must be an integer >= 2')
    adjacency = [dict() for _ in range(n_sites)]
    normalized = []
    for edge in edges:
        if not isinstance(edge, (list, tuple)) or len(edge) != 3:
            raise ValueError('Each weighted edge must be (i, j, J)')
        i, j, weight = edge
        if (type(i) is not int or type(j) is not int or
                not 0 <= i < n_sites or not 0 <= j < n_sites or i == j):
            raise ValueError('Edges require two distinct valid integer sites')
        if isinstance(weight, bool) or not isinstance(weight, (int, str, Fraction)):
            raise ValueError('Weights must be exact integers, Fractions or rational strings')
        try:
            weight = Fraction(weight)
        except (ValueError, ZeroDivisionError):
            raise ValueError('Invalid rational edge weight') from None
        if weight <= 0:
            raise ValueError('Every edge weight must be positive')
        normalized.append((i, j, weight))
        adjacency[i][j] = adjacency[i].get(j, Fraction(0)) + weight
        adjacency[j][i] = adjacency[j].get(i, Fraction(0)) + weight
    reached = {0}
    pending = [0]
    while pending:
        for j in adjacency[pending.pop()]:
            if j not in reached:
                reached.add(j)
                pending.append(j)
    if len(reached) != n_sites:
        raise ValueError('A connected graph is required; disconnected ground degeneracy differs')
    return tuple(normalized), adjacency


def weighted_min_cut(n_sites, edges):
    """Return (exact cut weight, one side) by deterministic Stoer-Wagner.

    Parallel undirected edges add, including reversed repetitions. Uses
    O(n^3) Fraction arithmetic operations and O(n^2+m) storage; rational
    bit complexity is additional. Intended for small/moderate finite graphs.
    """
    _, adjacency = _graph(n_sites, edges)
    active = list(range(n_sites))
    groups = {i: {i} for i in active}
    best, best_side = None, None
    while len(active) > 1:
        used = set()
        weights = {i: Fraction(0) for i in active}
        previous = None
        for step in range(len(active)):
            vertex = max((i for i in active if i not in used),
                         key=lambda i: (weights[i], -i))
            if step == len(active) - 1:
                if best is None or weights[vertex] < best:
                    best = weights[vertex]
                    best_side = tuple(sorted(groups[vertex]))
                # Contract the last two vertices of this maximum-adjacency phase.
                for other in active:
                    if other not in (previous, vertex):
                        value = (adjacency[previous].get(other, Fraction(0)) +
                                 adjacency[vertex].get(other, Fraction(0)))
                        if value:
                            adjacency[previous][other] = value
                            adjacency[other][previous] = value
                        adjacency[other].pop(vertex, None)
                adjacency[previous].pop(vertex, None)
                groups[previous].update(groups[vertex])
                active.remove(vertex)
                break
            used.add(vertex)
            for other in active:
                if other not in used:
                    weights[other] += adjacency[vertex].get(other, Fraction(0))
            previous = vertex
    return best, best_side


def diagnose_ising_obstruction(n_sites, edges, purity_threshold=Fraction(99, 100)):
    """Certify this finite graph's gap and impossibility of near-one purity.

    The spectral gap means energy above the entire ground eigenspace, not
    E_1-E_0 with eigenvalues counted with multiplicity (which is zero).
    Threshold is the desired lower bound T >= purity_threshold.
    """
    normalized, _ = _graph(n_sites, edges)
    if isinstance(purity_threshold, bool) or not isinstance(purity_threshold, (int, str, Fraction)):
        raise ValueError('purity_threshold must be exact rational')
    threshold = Fraction(purity_threshold)
    if not 0 < threshold <= 1:
        raise ValueError('purity_threshold must lie in (0,1]')
    cut, side = weighted_min_cut(n_sites, normalized)
    impossible = threshold > Fraction(1, 2)
    return {
        'status': 'VERIFIED_METHOD_OBSTRUCTION' if impossible else 'THRESHOLD_NOT_EXCLUDED',
        'n_sites': n_sites, 'full_hilbert_dimension_log2': n_sites,
        'normalization': 'H=-sum J_ij Sz_i Sz_j; Sz eigenvalues +/-1/2',
        'ground_energy': str(-sum((w for _, _, w in normalized), Fraction(0)) / 4),
        'ground_degeneracy': 2,
        'obstruction_origin':'Exact two-fold ground degeneracy prevents near-one Gibbs purity',
        'total_Sz_conserved':True, 'U1_symmetry_present':True,
        'global_spin_flip_Z2':True,
        'failed_assumption':'Unique ground state required by the near-one purity criterion',
        'weighted_min_cut': str(cut),
        'min_cut_side': list(side), 'gap_above_ground_space': str(cut / 2),
        'thermal_purity_upper_bound': '1/2', 'zero_temperature_purity_limit': '1/2',
        'purity_threshold': str(threshold), 'entry_impossible': impossible,
        'scope': 'This connected finite weighted graph; no uniform-family cut bound asserted',
        'model_gapless': False, 'uniform_family_claim': False,
        'recommended_action': ('Change to a ground-space-aware criterion; increasing seed size, beta or trial rank cannot remove this obstruction'
                               if impossible else 'This upper bound alone does not exclude the supplied threshold'),
        'algorithm': 'Exact rational Stoer-Wagner; analytic Ising cut identity',
    }
