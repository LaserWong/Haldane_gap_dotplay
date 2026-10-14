"""Finite exact local witnesses for a conditional spatial-transfer theorem.

A passed bond witness is not a thermodynamic gap certificate. Geometry,
translation, onsite structure and every direction still require validation.
"""
from fractions import Fraction as F
from math import isqrt
from .certify import rational, inertia


def _rat(x):
    if isinstance(x,bool):
        raise TypeError('Boolean is not an exact matrix coefficient')
    return rational(x)


def _square(matrix, size, max_dimension):
    if size<1 or size>max_dimension:
        raise ValueError('Exact matrix dimension budget exceeded')
    if hasattr(matrix,'toarray'):
        if matrix.shape!=(size,size):
            raise ValueError('Matrix has incorrect shape')
        matrix=matrix.toarray()
    if len(matrix)!=size or any(len(row)!=size for row in matrix):
        raise ValueError('Matrix has incorrect shape')
    return [[_rat(x) for x in row] for row in matrix]


def _metric_selfadjoint(matrix, weights):
    return all(weights[i]*matrix[i][j]==weights[j]*matrix[j][i]
               for i in range(len(matrix)) for j in range(len(matrix)))


def bond_realignment_certificate(h, local_dimension=None, metric_weights=None,
                                onsite=None, max_dimension=64):
    """Certify -h=sum c*A tensor A in a specified real coefficient basis.

    h is the coefficient matrix, NOT its metric-weighted energy-form matrix.
    metric_weights specify a positive diagonal local metric, default identity.
    Inputs are exact rationals. Output retains explicit global obligations.
    """
    if type(max_dimension) is not int or max_dimension<1:
        raise ValueError('max_dimension must be a positive integer')
    n=h.shape[0] if hasattr(h,'shape') else len(h)
    q=isqrt(n) if local_dimension is None else local_dimension
    if type(q) is not int or q<1 or q*q!=n:
        raise ValueError('Bond dimension must be the square of its local dimension')
    h=_square(h,n,max_dimension)
    weights=[F(1)]*q if metric_weights is None else [_rat(x) for x in metric_weights]
    if len(weights)!=q or any(x<=0 for x in weights):
        raise ValueError('Local diagonal metric must have positive weights')
    pairweights=[a*b for a in weights for b in weights]
    if not _metric_selfadjoint(h,pairweights):
        raise ValueError('Bond must be selfadjoint in the supplied physical metric')
    onsite_verified=False
    if onsite is not None:
        onsite=_square(onsite,q,max_dimension)
        if not _metric_selfadjoint(onsite,weights):
            raise ValueError('Onsite term must be real metric-selfadjoint')
        onsite_verified=True
    r=[[-h[a*q+c][b*q+d] for c in range(q) for d in range(q)]
       for a in range(q) for b in range(q)]
    symmetric=all(r[i][j]==r[j][i] for i in range(n) for j in range(n))
    ri=inertia(r,max_dimension=max_dimension) if symmetric else None
    passed=ri is not None and ri.negative==0
    witness=[]
    if passed:
        residual=[row[:] for row in r]
        while any(x for row in residual for x in row):
            pivot=next((i for i in range(n) if residual[i][i]>0),None)
            if pivot is None:
                raise ArithmeticError('PSD factorization disagrees with exact inertia')
            c=residual[pivot][pivot]
            vec=[residual[i][pivot]/c for i in range(n)]
            witness.append({'coefficient':str(c),'operator':[[str(vec[a*q+b]) for b in range(q)] for a in range(q)]})
            residual=[[residual[i][j]-c*vec[i]*vec[j] for j in range(n)] for i in range(n)]
        reconstructed=[[F(0) for _ in range(n)] for _ in range(n)]
        for term in witness:
            c=F(term['coefficient']);v=[F(x) for row in term['operator'] for x in row]
            reconstructed=[[reconstructed[i][j]+c*v[i]*v[j] for j in range(n)] for i in range(n)]
        if reconstructed!=r:
            raise ArithmeticError('Identical-factor witness failed exact reconstruction')
    diagonal=all(not h[i][j] for i in range(n) for j in range(n) if i!=j)
    classical_swap=diagonal and all(h[a*q+c][a*q+c]==h[c*q+a][c*q+a] for a in range(q) for c in range(q))
    return {'status':'LOCAL_IDENTICAL_FACTOR_WITNESS_VERIFIED' if passed else 'IDENTICAL_FACTOR_ROUTE_INCONCLUSIVE',
            'local_dimension':q,'bond_dimension':n,'metric_weights':[str(x) for x in weights],
            'bond_metric_selfadjoint':True,'onsite_real_metric_selfadjoint_verified':onsite_verified,
            'realignment_symmetric':symmetric,
            'realignment_inertia':None if ri is None else {'negative':ri.negative,'zero':ri.zero,'positive':ri.positive},
            'identical_factor_witness':witness,'witness_reconstruction_verified':passed,
            'classical_diagonal_symmetric_bond':classical_swap,
            'spatial_transfer_family_certified':False,
            'remaining_obligations':['Identical repeated finite-dimensional cells and a homogeneous rectangular nearest-neighbor family',
                'Real metric-selfadjoint onsite term and a verified bond witness in every direction',
                'Periodic positive-direction multigraph convention, side lengths >= 2',
                'Exact model-template matching at every required seed and family size'],
            'theorem_dependency':'Exact continuous-time identical-factor history construction in two_d_theory/THEORY.md Section 2.1',
            'scope':'Finite local structural witness only. Failure does not exclude a classical or different transfer route.'}
