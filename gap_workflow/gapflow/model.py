"""Finite spin models. Energies use hbar=1, S^2=s(s+1), no hidden shifts.

JSON schema v1: {"spin": 0.5, "geometry": {"type": "lattice", "shape": [4],
"periodic": false}, "terms": [{"type": "heisenberg", "J": 1}]}. Alternatively
use geometry={"type":"graph","n_sites":3,"edges":[[0,1],[1,2]]}, and
"spins": [0.5,1,0.5]. Real spin-product terms are supported; sector restriction requires total-Sz conservation.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import LinearOperator


def _keys(value, allowed, where):
    if not isinstance(value, dict):
        raise ValueError(f"{where} must be an object")
    unknown = set(value) - set(allowed)
    if unknown:
        raise ValueError(f"Unsupported {where} keys: {sorted(unknown)}")


def _integer(x, label, minimum=None):
    if isinstance(x, bool) or not isinstance(x, (int, np.integer)):
        raise ValueError(f"{label} must be an integer")
    x = int(x)
    if minimum is not None and x < minimum:
        raise ValueError(f"{label} must be >= {minimum}")
    return x


def _real(x, label):
    if isinstance(x, bool) or not isinstance(x, (int, float, Decimal, np.integer, np.floating)):
        raise ValueError(f"{label} must be a finite real number")
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(f"{label} must be finite")
    return x


def _coefficient(x, label):
    """Exact rational coefficient; decimal numbers denote their decimal spelling.

    from_json preserves JSON decimal lexemes with Decimal. For Python float
    inputs, the caller's repr(x) is the intended decimal coefficient. Prefer
    integer or rational string input when exact provenance matters.
    """
    if isinstance(x, bool) or not isinstance(x, (int, float, str, Decimal, Fraction, np.integer, np.floating)):
        raise ValueError(f'{label} must be a real rational number')
    try:
        result = Fraction(str(x))
        if not math.isfinite(float(result)): raise ValueError()
        return result
    except (ValueError, ZeroDivisionError, OverflowError):
        raise ValueError(f'{label} must be a finite rational number') from None


def _spin2(x):
    # Validate before any floating conversion: a near-half Decimal must not
    # round onto the allowed half-integer grid.
    if isinstance(x, bool) or not isinstance(x, (int, float, Decimal, Fraction, np.integer, np.floating)):
        raise ValueError('spin must be a positive integer or half-integer number')
    try:
        y = 2 * Fraction(str(x))
    except (ValueError, ZeroDivisionError, OverflowError):
        raise ValueError('spin must be a finite positive integer or half-integer') from None
    if y < 1 or y.denominator != 1:
        raise ValueError('spin must be a positive integer or half-integer')
    return y.numerator


def _sites(raw, n, label, length=None):
    if not isinstance(raw, (list, tuple)):
        raise ValueError(f'{label} must be a list')
    vals = tuple(_integer(v, label, 0) for v in raw)
    if any(v >= n for v in vals):
        raise ValueError(f'{label} site index outside [0,{n})')
    if length is not None and len(vals) != length:
        raise ValueError(f'{label} requires {length} sites')
    if len(set(vals)) != len(vals):
        raise ValueError(f'{label} requires distinct sites')
    return vals


@dataclass(frozen=True)
class Basis:
    """Computational basis encoded as local digit tuples, m_i=digit_i-s_i."""
    states: tuple
    total_m2: int | None
    local_dimensions: tuple

    @property
    def dimension(self):
        return len(self.states)

    def __len__(self):
        return len(self.states)


@dataclass(frozen=True)
class Model:
    name: str
    spins2: tuple
    edges: tuple
    terms: tuple
    geometry: dict

    @classmethod
    def from_json(cls, path):
        return cls.from_dict(json.loads(Path(path).read_text(), parse_float=Decimal))

    @classmethod
    def from_dict(cls, spec):
        _keys(spec, {'schema_version', 'name', 'spin', 'spins', 'geometry', 'terms', 'description'}, 'model')
        if spec.get('schema_version', 1) != 1:
            raise ValueError('Only schema_version=1 is supported')
        g = spec.get('geometry')
        _keys(g, {'type', 'n_sites', 'edges', 'positions', 'shape', 'periodic', 'bond_convention'}, 'geometry')
        kind = g.get('type')
        if kind == 'graph':
            _keys(g, {'type', 'n_sites', 'edges', 'positions'}, 'graph geometry')
            n = _integer(g.get('n_sites'), 'n_sites', 1)
            edges = tuple(_sites(e, n, 'edge', 2) for e in g.get('edges', []))
            if 'positions' in g:
                pos = np.asarray(g['positions'], dtype=float)
                if pos.ndim != 2 or pos.shape[0] != n or pos.shape[1] < 1 or not np.isfinite(pos).all():
                    raise ValueError('positions must be finite n_sites by spatial_dimension coordinates')
            geometry = dict(g)
            geometry['bond_convention'] = 'explicit_multigraph'
        elif kind == 'lattice':
            _keys(g, {'type', 'shape', 'periodic', 'bond_convention'}, 'lattice geometry')
            shape = tuple(_integer(x, 'shape entry', 1) for x in g.get('shape', []))
            if not shape:
                raise ValueError('lattice shape must be nonempty')
            n = math.prod(shape)
            periodic = g.get('periodic', False)
            if isinstance(periodic, bool):
                periodic = (periodic,) * len(shape)
            if not isinstance(periodic, (list, tuple)) or len(periodic) != len(shape) or any(type(p) is not bool for p in periodic):
                raise ValueError('periodic must be bool or one bool per spatial direction')
            convention = g.get('bond_convention', 'positive_direction_multigraph')
            if convention not in ('positive_direction_multigraph', 'simple_graph'):
                raise ValueError('Unsupported bond_convention')
            if any(p and l == 1 for p, l in zip(periodic, shape)):
                raise ValueError('Periodic length-one directions create self-bonds; remove the direction or use open boundaries')
            strides = [math.prod(shape[i+1:]) for i in range(len(shape))]
            edges = []
            for coord in itertools.product(*(range(l) for l in shape)):
                i = sum(c * st for c, st in zip(coord, strides))
                for axis, l in enumerate(shape):
                    if coord[axis] + 1 < l:
                        edges.append((i, i + strides[axis]))
                    elif periodic[axis]:
                        edges.append((i, i - (l-1)*strides[axis]))
            if convention == 'simple_graph':
                edges = sorted(set(tuple(sorted(e)) for e in edges))
            edges = tuple(edges)
            geometry = {'type': kind, 'shape': list(shape), 'periodic': list(periodic), 'bond_convention': convention}
        else:
            raise ValueError(f'Unsupported geometry type: {kind!r}')
        if 'spins' in spec and 'spin' in spec:
            raise ValueError('Specify spin or spins, not both')
        if 'spins' in spec:
            if len(spec['spins']) != n:
                raise ValueError('spins length must equal n_sites')
            spins2 = tuple(_spin2(s) for s in spec['spins'])
        elif 'spin' in spec:
            spins2 = (_spin2(spec['spin']),) * n
        else:
            raise ValueError('Specify spin or spins')
        terms = []
        raw_terms = spec.get('terms')
        if not isinstance(raw_terms, list):
            raise ValueError('terms must be a list (empty list gives zero Hamiltonian)')
        for raw in raw_terms:
            _keys(raw, {'type','sites','J','Jxy','Jz','D','h','coefficient','factors'}, 'term')
            t = raw.get('type')
            if t in ('heisenberg', 'xxz'):
                _keys(raw, {'type','sites','J'} if t == 'heisenberg' else {'type','sites','Jxy','Jz'}, t)
                pairs = (_sites(raw['sites'], n, t, 2),) if 'sites' in raw else edges
                if t == 'heisenberg':
                    if 'J' not in raw: raise ValueError('heisenberg requires J')
                    jxy = jz = _coefficient(raw['J'], 'J')
                else:
                    if 'Jxy' not in raw or 'Jz' not in raw: raise ValueError('xxz requires Jxy and Jz')
                    jxy, jz = _coefficient(raw['Jxy'], 'Jxy'), _coefficient(raw['Jz'], 'Jz')
                terms.extend(('exchange', i, j, jxy, jz) for i,j in pairs)
            elif t in ('onsite_d', 'field_z'):
                param = 'D' if t == 'onsite_d' else 'h'
                _keys(raw, {'type','sites',param}, t)
                if param not in raw: raise ValueError(f'{t} requires {param}')
                sites = _sites(raw['sites'], n, t) if 'sites' in raw else range(n)
                terms.extend((t, i, _coefficient(raw[param], param)) for i in sites)
            elif t == 'spin_product':
                _keys(raw, {'type','coefficient','factors'}, t)
                if 'coefficient' not in raw or not isinstance(raw.get('factors'), list):
                    raise ValueError('spin_product requires coefficient and factors list')
                factors = []
                for factor in raw['factors']:
                    _keys(factor, {'site','operator'}, 'spin_product factor')
                    site = _sites([factor.get('site')], n, 'factor site', 1)[0]
                    operator = factor.get('operator')
                    if operator not in ('x','z'):
                        raise ValueError('spin_product supports only real x/z operators; y and arbitrary matrices are unsupported')
                    factors.append((site,operator))
                if len({i for i,_ in factors}) != len(factors):
                    raise ValueError('spin_product factors must act on distinct sites')
                terms.append(('spin_product', _coefficient(raw['coefficient'],'coefficient'), tuple(factors)))
            else:
                raise ValueError(f'Unsupported interaction type: {t!r}; supported: heisenberg, xxz, onsite_d, field_z, spin_product')
        return cls(str(spec.get('name', 'unnamed')), spins2, edges, tuple(terms), geometry)

    @property
    def n_sites(self): return len(self.spins2)
    @property
    def spins(self): return tuple(s/2 for s in self.spins2)
    @property
    def local_dimensions(self): return tuple(s+1 for s in self.spins2)
    @property
    def hilbert_dimension(self): return math.prod(self.local_dimensions)

    @property
    def preserves_total_sz(self):
        return not any(t[0] == 'spin_product' and t[1] and any(op == 'x' for _,op in t[2]) for t in self.terms)

    def sector_dimensions(self):
        """Exact integer DP counts; never builds the Hilbert basis."""
        counts = {0: 1}
        for s in self.spins2:
            nxt = Counter()
            for q, count in counts.items():
                for m2 in range(-s, s+1, 2): nxt[q+m2] += count
            counts = dict(nxt)
        return counts

    def dimension(self, total_m2=None):
        if total_m2 is None: return self.hilbert_dimension
        if not self.preserves_total_sz:
            raise ValueError('total_m2 sectors are invalid: model does not preserve total Sz')
        return self.sector_dimensions().get(_integer(total_m2, 'total_m2'), 0)

    def basis(self, total_m2=None, max_dimension=2_000_000):
        dim = self.dimension(total_m2)
        if dim > max_dimension:
            raise MemoryError(f'Basis dimension {dim} exceeds explicit basis limit {max_dimension}')
        if not dim: raise ValueError('Requested magnetization sector is empty')
        dims = self.local_dimensions
        if total_m2 is None:
            states = tuple(itertools.product(*(range(d) for d in dims)))
        else:
            # Prune branches, so a tiny sector never scans the full Hilbert space.
            states_list = []
            remaining = [sum(self.spins2[k:]) for k in range(self.n_sites+1)]
            def visit(prefix, q):
                k = len(prefix)
                if k == self.n_sites:
                    if q == total_m2: states_list.append(tuple(prefix))
                    return
                for digit in range(dims[k]):
                    qn = q + 2*digit-self.spins2[k]
                    if abs(total_m2-qn) <= remaining[k+1]: visit(prefix+[digit], qn)
            visit([], 0)
            states = tuple(states_list)
        return Basis(states, total_m2, dims)

    def hamiltonian(self, total_m2=None, matrix_free=True, max_dimension=2_000_000):
        basis = self.basis(total_m2, max_dimension=max_dimension)
        states, d = basis.states, len(basis)
        index = {state: i for i, state in enumerate(states)}
        spins = self.spins
        def transitions(state):
            diagonal = 0.0
            for term in self.terms:
                if term[0] == 'exchange':
                    _, i, j, jxy, jz = term
                    mi, mj = state[i]-spins[i], state[j]-spins[j]
                    diagonal += jz * mi * mj
                    if jxy:
                        for sign in (-1, 1):
                            a, b = state[i]+sign, state[j]-sign
                            if 0 <= a <= self.spins2[i] and 0 <= b <= self.spins2[j]:
                                amp = 0.5*jxy*math.sqrt((spins[i]*(spins[i]+1)-mi*(mi+sign))*(spins[j]*(spins[j]+1)-mj*(mj-sign)))
                                new = list(state); new[i], new[j] = a,b
                                yield index[tuple(new)], amp
                elif term[0] == 'onsite_d':
                    _, i, value = term; diagonal += value*(state[i]-spins[i])**2
                elif term[0] == 'field_z':
                    _, i, value = term; diagonal += value*(state[i]-spins[i])
                elif term[0] == 'spin_product':
                    _, coefficient, factors = term
                    paths = [(list(state),float(coefficient))]
                    for i,operator in factors:
                        nxt = []
                        for current,amplitude in paths:
                            mi = state[i]-spins[i]
                            if operator == 'z':
                                nxt.append((current,amplitude*mi))
                            else:
                                for sign in (-1,1):
                                    p = state[i]+sign
                                    if 0 <= p <= self.spins2[i]:
                                        new = current.copy(); new[i] = p
                                        nxt.append((new,amplitude*0.5*math.sqrt(spins[i]*(spins[i]+1)-mi*(mi+sign))))
                        paths = nxt
                    for current,amplitude in paths:
                        if amplitude: yield index[tuple(current)],amplitude
            if diagonal: yield index[state], diagonal
        def matvec(x):
            x = np.asarray(x).reshape(d)
            y = np.zeros(d, dtype=np.result_type(x.dtype, np.float64))
            for col, state in enumerate(states):
                for row, value in transitions(state): y[row] += value*x[col]
            return y
        if matrix_free:
            op = LinearOperator((d,d), matvec=matvec, rmatvec=matvec, dtype=np.float64)
        else:
            rows, cols, values = [], [], []
            for col, state in enumerate(states):
                for row, value in transitions(state): rows.append(row); cols.append(col); values.append(value)
            op = coo_matrix((values, (rows, cols)), shape=(d,d), dtype=np.float64).tocsr()
            op.sum_duplicates(); op.eliminate_zeros()
        # Provenance available without a second basis enumeration.
        op.gapflow_basis = basis
        op.gapflow_model = self
        return op

    def exact_pencil(self, total_m2=None, max_dimension=64):
        """Exact rational (A,Wdiag) with physical spectrum A v = E W v.

        In the local divided-power basis |p>=(S+)^p/p!|-s>, the norm is
        binom(2s,p), and ladder coefficients are integers. If Htilde is the
        Hamiltonian in this basis, A=W Htilde is symmetric rational and W is
        strictly positive diagonal. Thus inertia(A-tW) equals inertia(H-tI)
        in the normalized physical basis. This supports arbitrary positive
        half-integer/integer spins, including mixed spins, without radicals.
        """
        basis = self.basis(total_m2, max_dimension=max_dimension)
        index = {state:i for i,state in enumerate(basis.states)}
        weights = [math.prod(math.comb(s,p) for s,p in zip(self.spins2,state))
                   for state in basis.states]
        out = [[Fraction(0) for _ in basis.states] for _ in basis.states]
        for col,state in enumerate(basis.states):
            m = [Fraction(2*p-s,2) for p,s in zip(state,self.spins2)]
            for term in self.terms:
                if term[0] == 'exchange':
                    _,i,j,jxy,jz = term
                    out[col][col] += weights[col]*jz*m[i]*m[j]
                    for sign in (-1,1):
                        pi,pj = state[i],state[j]
                        a,b = pi+sign,pj-sign
                        if jxy and 0 <= a <= self.spins2[i] and 0 <= b <= self.spins2[j]:
                            if sign == 1:
                                ladder = (pi+1)*(self.spins2[j]-pj+1)
                            else:
                                ladder = (self.spins2[i]-pi+1)*(pj+1)
                            new = list(state); new[i],new[j] = a,b
                            row = index[tuple(new)]
                            out[row][col] += weights[row]*jxy*Fraction(ladder,2)
                elif term[0] == 'onsite_d':
                    _,i,c = term; out[col][col] += weights[col]*c*m[i]*m[i]
                elif term[0] == 'field_z':
                    _,i,c = term; out[col][col] += weights[col]*c*m[i]
                elif term[0] == 'spin_product':
                    _,coefficient,factors = term
                    paths = [(list(state),coefficient)]
                    for i,operator in factors:
                        nxt = []
                        for current,amplitude in paths:
                            if operator == 'z':
                                nxt.append((current,amplitude*m[i]))
                            else:
                                for sign in (-1,1):
                                    p = state[i]+sign
                                    if 0 <= p <= self.spins2[i]:
                                        new = current.copy(); new[i] = p
                                        ladder = state[i]+1 if sign == 1 else self.spins2[i]-state[i]+1
                                        nxt.append((new,amplitude*Fraction(ladder,2)))
                        paths = nxt
                    for current,amplitude in paths:
                        row = index[tuple(current)]
                        out[row][col] += weights[row]*amplitude
        return out, weights

    def exact_hamiltonian(self, total_m2=None, max_dimension=64):
        """Return a Fraction matrix from rational model coefficients, never floats.

        Supported exchange representations: all sites spin-1/2, or all spin-1.
        General mixed/higher-spin ladder matrix elements require algebraic
        arithmetic not supplied here and explicitly fail closed.
        """
        has_exchange = any(t[0] == 'exchange' and t[3] != 0 for t in self.terms)
        if has_exchange and not (all(s == 1 for s in self.spins2) or all(s == 2 for s in self.spins2)):
            raise ValueError('Exact exchange matrix currently supports uniform spin-1/2 or spin-1 only; use algebraic arithmetic for other spins')
        if any(t[0] == 'spin_product' and t[1] and any(op == 'x' and self.spins2[i] != 1 for i,op in t[2]) for t in self.terms):
            raise ValueError('Normalized exact x-product matrix may contain radicals; use exact_pencil')
        basis = self.basis(total_m2, max_dimension=max_dimension)
        index = {state:i for i,state in enumerate(basis.states)}
        out = [[Fraction(0) for _ in basis.states] for _ in basis.states]
        for col,state in enumerate(basis.states):
            m = [Fraction(2*d-s,2) for d,s in zip(state,self.spins2)]
            for term in self.terms:
                if term[0] == 'exchange':
                    _,i,j,jxy,jz = term
                    out[col][col] += jz*m[i]*m[j]
                    for sign in (-1,1):
                        a,b = state[i]+sign,state[j]-sign
                        if jxy and 0 <= a <= self.spins2[i] and 0 <= b <= self.spins2[j]:
                            # Ladder product is exactly 1 (spin half) or 2 (spin one).
                            amplitude = jxy * Fraction(self.spins2[i],2)
                            new = list(state); new[i],new[j] = a,b
                            out[index[tuple(new)]][col] += amplitude
                elif term[0] == 'onsite_d':
                    _,i,c = term; out[col][col] += c*m[i]*m[i]
                elif term[0] == 'field_z':
                    _,i,c = term; out[col][col] += c*m[i]
                elif term[0] == 'spin_product':
                    _,coefficient,factors = term
                    current = list(state)
                    amplitude = coefficient
                    for i,operator in factors:
                        if operator == 'z': amplitude *= m[i]
                        else:
                            current[i] = 1-state[i]
                            amplitude *= Fraction(1,2)
                    if amplitude: out[index[tuple(current)]][col] += amplitude
        return out

    def summary(self):
        return {'name':self.name, 'n_sites':self.n_sites, 'spins':list(self.spins),
                'local_dimensions':list(self.local_dimensions), 'hilbert_dimension':self.hilbert_dimension,
                'geometry':self.geometry, 'preserves_total_sz':self.preserves_total_sz, 'edge_count':len(self.edges), 'expanded_term_count':len(self.terms),
                'normalization':'hbar=1; S^2=s(s+1); exchange=Jxy*(SxSx+SySy)+Jz*SzSz; field_z=+h*Sz; onsite_d=D*Sz^2; no energy shift'}


def build_hamiltonian(spec_or_model, total_m2=None, matrix_free=True, **kwargs):
    model = spec_or_model if isinstance(spec_or_model, Model) else Model.from_dict(spec_or_model)
    return model.hamiltonian(total_m2=total_m2, matrix_free=matrix_free, **kwargs)
