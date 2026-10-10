#!/usr/bin/env python3
"""Independent exact-arithmetic checks for the general-dimensional audit.

No project certificate/transfer/bootstrap routine is imported. All diagnostic
models are finite commuting Hamiltonians. Their partition functions are exact
rational numbers, not floating-point diagonalizations. The analytic proof is
PROOF_REVIEW.md. Finite model checks are implementation tests, not that proof.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations, product
from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def encoded(x):
    x = F(x)
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def f(u):
    assert 0 <= u < 1
    return u * u / (2 * (1 - u) ** 2)


def floor_grid(x, denominator=10**12):
    x = F(x)
    return F((x.numerator * denominator) // x.denominator, denominator)


def matmul(a, b):
    n = len(a)
    bt = list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in bt] for row in a]


def trace_power(a, n):
    assert n >= 0
    m = len(a)
    out = [[int(i == j) for j in range(m)] for i in range(m)]
    while n:
        if n & 1:
            out = matmul(out, a)
        n //= 2
        if n:
            a = matmul(a, a)
    return sum(out[i][i] for i in range(m))


@lru_cache(None)
def chain_z(length, temperature_multiplier, base=2048):
    # H = 2 sum n_i + 2 sum n_i n_{i+1}, beta = multiplier log(base).
    # T = [[1,q],[q,q^4]]. det(T) = q^4-q^2 < 0, hence a signed spectrum.
    b = base ** temperature_multiplier
    scale = b**4
    a = [[scale, b**3], [b**3, 1]]
    return F(trace_power(a, length), scale**length)


@lru_cache(None)
def row_stack_z(node):
    *lengths, multiplier = node
    rows = 1
    for x in lengths[1:]:
        rows *= x
    return chain_z(lengths[0], multiplier) ** rows


@lru_cache(None)
def square_z(node):
    # H = 4 sum n_r + 2 sum_{r,e=x,y} n_r n_{r+e} on periodic tori.
    # Length-2 directions retain both oriented periodic adjacency terms.
    lx, ly, multiplier = node
    if ly > lx:
        lx, ly = ly, lx
    b = 16 ** multiplier
    states = range(1 << ly)
    onsite = [4*s.bit_count() + 2*sum(((s >> y)&1)*((s >> ((y+1)%ly))&1)
                                    for y in range(ly)) for s in states]
    max_exponent = 8 * ly
    scale = b**max_exponent
    a = [[b**(max_exponent - (onsite[s]+onsite[t])//2
              - 2*(s&t).bit_count()) for t in states] for s in states]
    return F(trace_power(a, lx), scale**lx)


def double(node, axis):
    x = list(node)
    x[axis] *= 2
    return tuple(x)


def purity(z, node, axis):
    return z(double(node, axis)) / z(node)**2


def staircase(z, node, axes):
    result = []
    for axis in axes:
        result.append(purity(z, node, axis))
        node = double(node, axis)
    return result


def exact_endpoints():
    v = F(1,100)
    coeff_square = (3-3*v+v*v)**2 / (2*(1-v)**6)
    coeff_interpolation = F(3,2)+5*v+2/(1-2*v)
    inverse_weight_margin = 1-5*v-v*v
    assert coeff_square < 5
    assert coeff_interpolation < 4
    assert inverse_weight_margin > 0
    assert (1-v)**3 > F(1,2)
    records = []
    for d in range(1,21):
        c = 2**(d+1)-1
        fd = 4*8**(d-1)
        kd = max(c*c, 2*fd)
        u = min(F(1,4*kd), F(1,100*8**(d-1)))
        assert f(c*u) <= c*c*u*u <= kd*u*u <= u/4
        assert fd*u <= F(1,25)
        assert fd*u/(1-fd*u) <= kd*u
        assert (1-u)**2*(1-2*u)*(1-4*u) >= 1-8*u
        records.append({"dimension":d,"c":c,"F":fd,"K":kd,"u":encoded(u),
                        "square_coefficient":encoded(f(c*u)/(u*u)),
                        "thermal_error":encoded(fd*u)})
    return {"one_dimensional_v":encoded(v),
            "one_dimensional_square_coefficient":encoded(coeff_square),
            "one_dimensional_interpolation_coefficient":encoded(coeff_interpolation),
            "one_dimensional_inverse_weight_margin":encoded(inverse_weight_margin),
            "universal_squaring_coefficient_upper":encoded(F(72,121)),
            "dimension_endpoint_tests":records,
            "interpolation_polynomial_remainder_coefficients":[0,0,21,-22,8]}


def improvement_endpoints():
    v = F(1,40)
    one_d_square = (3-3*v+v*v)**2 / (2*(1-v)**6)
    one_d_interpolation = F(3,2)+5*v+2/(1-2*v)
    assert one_d_square < 5 and one_d_interpolation < 4
    assert 1-5*v-v*v > 0 and (1-v)**3 > F(1,2)
    u = F(1,200)
    product_loss = 1-(1-u)**7
    k26_coefficient = f(product_loss)/(u*u)
    k26_tail = 20/(1-20*u)
    assert k26_coefficient < 26 and k26_tail < 26 and 26*u < 1
    records = []
    p = F(1)
    for d in range(1,7):
        c = 2**(d+1)-1
        cd = F(1) if d == 1 else F(8)-F(3,2**(d-2))
        if d > 1:
            p *= cd
        fd = 4*p
        umax = 1/(40*p)
        conservative_k = max(c*c, 2*fd)
        exact_coeff = f(1-(1-umax)**c)/(umax*umax)
        tail_coeff = fd/(1-fd*umax)
        maximum_coeff = max(exact_coeff,tail_coeff)
        integer_k = -((-maximum_coeff.numerator)//maximum_coeff.denominator)
        assert c*c*umax <= F(49,200)
        assert conservative_k*umax <= F(49,200)
        assert exact_coeff <= c*c
        assert integer_k <= conservative_k and integer_k*umax < 1
        records.append({"dimension":d,"induction_factor":encoded(cd),
                        "product_P":encoded(p),"purity_loss_F":encoded(fd),
                        "input_domain_U":encoded(umax),
                        "conservative_K":encoded(conservative_k),
                        "exact_contraction_coefficient":encoded(exact_coeff),
                        "exact_gap_extraction_coefficient":encoded(tail_coeff),
                        "valid_integer_K":integer_k})
    return {"one_dimensional_extended_endpoint":encoded(v),
            "one_dimensional_square_coefficient":encoded(one_d_square),
            "one_dimensional_interpolation_coefficient":encoded(one_d_interpolation),
            "one_dimensional_inverse_weight_margin":encoded(1-5*v-v*v),
            "two_dimensional_u":encoded(u),
            "two_dimensional_exact_product_coefficient":encoded(k26_coefficient),
            "two_dimensional_K26_margin":encoded(26-k26_coefficient),
            "two_dimensional_gap_extraction_coefficient":encoded(k26_tail),
            "refined_general_dimension_endpoints":records}


def test_rotations():
    records = []
    for d in (1,2,3):
        k = d+1
        initial = (2,)*d+(1,)
        u = F(1,100*8**(d-1))
        max_bit_length = 0
        cases = 0
        for perm in permutations(range(k)):
            node = initial
            order = list(perm)
            measured = staircase(row_stack_z,node,order)
            assert all(1-u <= x <= 1 for x in measured)
            bounds = [floor_grid(x) for x in measured]
            for step in range(k):
                first = order[0]
                other_node = node
                for axis in order[1:]:
                    other_node = double(other_node,axis)
                corner = row_stack_z(double(other_node,first)) / row_stack_z(node)**(2**k)
                measured = staircase(row_stack_z,node,order)
                telescoped = F(1)
                bounded = F(1)
                for j in range(k):
                    exponent = 2**(k-1-j)
                    telescoped *= measured[j]**exponent
                    bounded *= bounds[j]**exponent
                assert telescoped == corner
                assert purity(row_stack_z,other_node,first) >= corner >= bounded
                new_bound = floor_grid(1-f(1-bounded))
                new_node = double(node,first)
                new_order = order[1:]+order[:1]
                new_values = staircase(row_stack_z,new_node,new_order)
                assert new_values[:-1] == measured[1:]
                assert new_values[-1] >= new_bound
                bounds = bounds[1:]+[new_bound]
                node, order = new_node,new_order
                for value in new_values:
                    max_bit_length = max(max_bit_length,value.numerator.bit_length(),
                                         value.denominator.bit_length())
                cases += 1
            assert node == tuple(2*x for x in initial)
            assert order == list(perm)
            final_values = staircase(row_stack_z,node,order)
            kd = max((2**k-1)**2, 8**d)
            assert all(1-value <= kd*u*u for value in final_values)
        records.append({"dimension":d,"permutations":len(list(permutations(range(k)))),
                        "exact_rotation_steps":cases,"largest_rational_bit_length":max_bit_length,
                        "all_checks_passed":True})
    return records


def direct_square_z(lx, ly, multiplier=1):
    """Independent product-basis enumeration, including length-2 multiplicity."""
    n = lx*ly
    base = 16**multiplier
    max_energy = 8*n
    histogram = {}
    for state in range(1 << n):
        occ = lambda x,y: (state >> ((x % lx)*ly+(y % ly))) & 1
        energy = 4*state.bit_count()
        energy += 2*sum(occ(x,y)*(occ(x+1,y)+occ(x,y+1))
                        for x in range(lx) for y in range(ly))
        histogram[energy] = histogram.get(energy,0)+1
    zz = F(sum(count*base**(max_energy-energy)
               for energy,count in histogram.items()), base**max_energy)
    energies = sorted(histogram)
    assert histogram[energies[0]] == 1 and energies[1]-energies[0] == 4
    return zz, histogram


def test_coupled_square():
    seed = (2,2,1)
    u = F(1,800)
    q = staircase(square_z,seed,(0,1,2))
    assert all(1-u <= x <= 1 for x in q)
    tested = []
    for lx,ly in product(range(2,5),repeat=2):
        actual = purity(square_z,(lx,ly,1),2)
        assert actual >= 1-32*u
        # The specialized 2D bound is also valid for this same model.
        assert actual >= 1-20*u
        tested.append({"shape":[lx,ly],"contains_odd_length":bool(lx%2 or ly%2),
                       "purity_lower_bound":encoded(1-20*u),"passed":True})
    for perm in permutations(range(3)):
        vals = staircase(square_z,seed,perm)
        prod = F(1)
        for i,x in enumerate(vals):
            assert 0 < x <= 1
            prod *= x**(2**(2-i))
        assert prod == square_z((4,4,2))/square_z(seed)**8
    # Explicit transfer entries are strictly positive but the matrix is not PSD.
    # For transverse width 2, use states 00 and 01. The 2x2 principal determinant
    # is q^4*(q^2-1), which is strictly negative.
    qq = F(1,16)
    principal_determinant = qq**4 * (qq**2-1)
    assert principal_determinant < 0
    enumerations = []
    for lx,ly in ((2,2),(2,3),(3,3)):
        direct,histogram = direct_square_z(lx,ly)
        assert direct == square_z((lx,ly,1))
        enumerations.append({"shape":[lx,ly],"full_hilbert_dimension":2**(lx*ly),
                             "ground_degeneracy":histogram[0],"first_excitation_energy":4,
                             "partition_function_matches_transfer":True})
    return {"hamiltonian":"4 sum n_r + 2 sum_{r,e=x,y} n_r n_(r+e)",
            "beta":"log(16)","seed_purities":[encoded(x) for x in q],
            "certified_input_defect":encoded(u),"rectangles":tested,
            "staircase_permutations_tested":6,
            "width_two_transfer_principal_minor":encoded(principal_determinant),
            "exact_periodic_gap":4,"independent_basis_enumeration":enumerations}


def test_all_integer_stacks():
    records = []
    for d in (1,2,3):
        u = F(1,100*8**(d-1))
        fd = 4*8**(d-1)
        seed = (2,)*d+(1,)
        assert all(1-u <= x <= 1 for x in staircase(row_stack_z,seed,range(d+1)))
        count = odd_count = 0
        for lengths in product(range(2,5),repeat=d):
            actual = purity(row_stack_z,lengths+(1,),d)
            assert actual >= 1-fd*u
            count += 1
            odd_count += any(x%2 for x in lengths)
        records.append({"dimension":d,"integer_boxes_tested":count,
                        "boxes_with_odd_side":odd_count,"all_checks_passed":True,
                        "exact_periodic_gap":2})
    return records


def counterexamples():
    a = F(1,16)
    z = lambda n: 1+(-a)**n
    s2,s3,s4 = (z(2*n)/z(n)**2 for n in (2,3,4))
    assert 0 < s2 < 1 < s3 and s4 < s3
    # Ferromagnetic zero-field Ising transfer T_beta=[[2,1/2],[1/2,2]].
    # At beta=log(2), eigenvalues are 5/2 and 3/2.
    # At 2 beta, eigenvalues are 17/4 and 15/4.
    eig1 = (F(5,2),F(3,2))
    eig2 = (F(17,4),F(15,4))
    zz1 = lambda n: sum(x**n for x in eig1)
    zz2 = lambda n: sum(x**n for x in eig2)
    spatial1, spatial2 = zz1(4)/zz1(2)**2, zz2(4)/zz2(2)**2
    thermal_n, thermal_2n = zz2(2)/zz1(2)**2, zz2(4)/zz1(4)**2
    assert spatial2 < spatial1
    assert spatial1*spatial1*thermal_2n == spatial2*thermal_n*thermal_n
    return {"signed_spatial_odd_purity":{"spectrum":[encoded(1),encoded(-a)],
            "S_even_2":encoded(s2),"S_odd_3":encoded(s3),"S_even_4":encoded(s4),
            "all_integer_traces_positive":True},
            "spatial_purity_not_monotone_in_beta_and_naive_permutation_fails":{
            "model":"zero-field ferromagnetic Ising chain H=-sum s_i s_(i+1)",
            "n":2,"beta":"log(2)","S_at_beta":encoded(spatial1),
            "S_at_double_beta":encoded(spatial2),
            "x_then_beta_staircase":[encoded(spatial1),encoded(thermal_2n)],
            "beta_then_x_staircase":[encoded(thermal_n),encoded(spatial2)],
            "naively_swapped_second_value_is_false_lower_bound":True}}


def main():
    started = time.monotonic()
    files = ["two_d_theory/GENERAL_DIMENSION.md","two_d_theory/THEORY.md",
             "audit/NEW_RESULT_REVIEWS.md"]
    result = {"status":"PASS_WITH_EXPLICIT_HYPOTHESES_AND_SCOPE",
              "arithmetic":"Python Fraction and integer matrix products only",
              "input_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},
              "endpoints":exact_endpoints(),
              "improvement_endpoints":improvement_endpoints(),
              "sequential_permutation_tests":test_rotations(),
              "coupled_two_dimensional_commuting_test":test_coupled_square(),
              "all_integer_signed_row_stack_tests":test_all_integer_stacks(),
              "counterexamples_to_unlicensed_extensions":counterexamples()}
    result["runtime_seconds_diagnostic_only"] = round(time.monotonic()-started,3)
    path = OUT/"exact_checks.json"
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"output":str(path),
                      "runtime_seconds":result["runtime_seconds_diagnostic_only"],
                      "rotation_steps":sum(x["exact_rotation_steps"] for x in result["sequential_permutation_tests"]),
                      "coupled_rectangles":len(result["coupled_two_dimensional_commuting_test"]["rectangles"])},indent=2))

if __name__ == "__main__":
    main()
