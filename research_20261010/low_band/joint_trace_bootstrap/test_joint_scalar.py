"""Exact scalar consistency tests; independent review is a separate package."""
from fractions import Fraction as F
from pathlib import Path
import random,json,sys
sys.dont_write_bytecode=True
import joint_scalar as J


def main():
    rng=random.Random(20261010);updates=windows=0
    for _ in range(200):
        actual=[F(rng.randrange(975,1000),1000) for _ in range(3)]
        lower=[x-F(rng.randrange(1,6),1000) for x in actual]
        actualjoint=J.full_product(actual)
        boundjoint=actualjoint-F(rng.randrange(1,6),1000)
        assert 0<boundjoint<=actualjoint
        old,_=J.canonical_advance(lower,J.full_product(lower))
        improved,_=J.canonical_advance(lower,max(boundjoint,J.full_product(lower)))
        full,_=J.canonical_advance(actual,actualjoint)
        assert all(x<=y<=z for x,y,z in zip(old,improved,full));updates+=1
        original,_=J.interpolate_2d_joint(*lower,J.full_product(lower))
        better,_=J.interpolate_2d_joint(*lower,max(boundjoint,J.full_product(lower)))
        ceiling,_=J.interpolate_2d_joint(*actual,actualjoint)
        assert 0<=original<=better<=ceiling<=1;windows+=1
        # Exact telescoping for three independent positive partition values.
        zs=[F(rng.randrange(1,100),rng.randrange(1,100)) for _ in range(4)]
        ps=[zs[i+1]/zs[i]**2 for i in range(3)]
        assert J.full_product(ps)==zs[3]/zs[0]**8
    result=dict(status='passed_exact_scalar_tests_not_independent_review',
        update_order_cases=updates,joint_window_monotonic_cases=windows,
        telescoping_identity_cases=200)
    Path(__file__).with_name('test_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
