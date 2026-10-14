"""Independent exact checks and archived analytic baseline regression values."""
import copy
from fractions import Fraction as F
import unittest
from gapflow.bootstrap import bootstrap_certificate, canonical_edges, cycle, down


def request(d, q, beta='12', lengths=None):
    lengths = lengths or [2]*d
    return dict(dimension=d,lengths=lengths,beta=beta,
                edges=canonical_edges(lengths,beta,q),
                model_to_seed_proof={'verified':True,'evidence':['historical analytic derivation requiring external review']})


class BootstrapTests(unittest.TestCase):
    def test_archived_bilayer_baseline(self):
        # two_d_theory/bilayer_seed_certificate.json, not float display fields.
        q=['999424165856154089/1000000000000000000',
           '997698652170741851/1000000000000000000',
           '990242081527557809/1000000000000000000']
        out=bootstrap_certificate(request(2,q))
        self.assertEqual(out['status'],'VERIFIED_CONDITIONAL')
        self.assertEqual(out['gap_lower'],str(F('0.151171228506')))
        self.assertEqual(out['lengths'],[4,4])
        self.assertEqual(out['beta'],'24')
        self.assertFalse(out['uniform_family_claim'])
        self.assertFalse(out['physical_proof_verified'])
        self.assertFalse(out['proof_declaration_trusted'])

    def test_archived_large_d_baseline(self):
        q=['999424165856154089/1000000000000000000',
           '997698652170741851/1000000000000000000',
           '990436793921877631/1000000000000000000']
        out=bootstrap_certificate(request(2,q))
        self.assertEqual(out['gap_lower'],str(F('0.152901911246')))

    def test_one_dimensional_sequential_formula(self):
        s,t=F(9,10),F(19,20)
        def G(x): return 1-(1-x)**2/(2*x*x)
        ss=down(G(s*s*t))
        tt=down(G(t*t*ss))
        actual,_=cycle([s,t])
        self.assertEqual(actual,[ss,tt])
        self.assertNotEqual(tt,down(G(t*t*s)))

    def test_two_dimensional_sequential_formula(self):
        a,b,c=F(99,100),F(98,100),F(97,100)
        def G(x):return down(1-(1-x)**2/(2*x*x))
        aa=G(a**4*b**2*c)
        bb=G(b**4*c**2*aa)
        cc=G(c**4*aa**2*bb)
        self.assertEqual(cycle([a,b,c])[0],[aa,bb,cc])

    def test_bad_permutation_and_wrong_basepoint(self):
        r=request(2,['999/1000']*3)
        r['edges'][0],r['edges'][1]=r['edges'][1],r['edges'][0]
        self.assertEqual(bootstrap_certificate(r)['status'],'INVALID_INPUT')
        r=request(2,['999/1000']*3)
        r['edges'][2]['base_lengths']=[2,2]
        self.assertEqual(bootstrap_certificate(r)['status'],'INVALID_INPUT')

    def test_missing_proof(self):
        r=request(1,['999/1000']*2)
        del r['model_to_seed_proof']
        self.assertEqual(bootstrap_certificate(r)['status'],'UNSUPPORTED')

    def test_general_d(self):
        out=bootstrap_certificate(request(3,['999999/1000000']*4))
        self.assertEqual(out['status'],'VERIFIED_CONDITIONAL')
        self.assertEqual(out['contraction_constant'],512)
        self.assertEqual(out['entry_threshold'],'1/6400')

    def test_general_two_d_does_not_claim_sharper_constant(self):
        r=request(2,['99999/100000']*3)
        r['mode']='general'
        self.assertEqual(bootstrap_certificate(r)['contraction_constant'],64)

    def test_nonacceptance_is_not_gaplessness(self):
        r=request(1,['1/2','1/2'])
        out=bootstrap_certificate(r)
        self.assertEqual(out['status'],'INCONCLUSIVE')
        self.assertEqual(out['model_gapless'],'not established')
        r=request(1,['9/10','9/10'])
        r['max_rounds']=0
        self.assertEqual(bootstrap_certificate(r)['status'],'RESOURCE_LIMIT')

    def test_bad_exact_input(self):
        r=request(1,['9/10','9/10'])
        r['edges'][0]['lower']=0.9
        self.assertEqual(bootstrap_certificate(r)['status'],'INVALID_INPUT')
        r=request(1,['9/10','9/10'])
        r['lengths']=[3]
        self.assertEqual(bootstrap_certificate(r)['status'],'INVALID_INPUT')

    def test_output_staircase_after_growth(self):
        q=['999424165856154089/1000000000000000000',
           '997698652170741851/1000000000000000000',
           '990242081527557809/1000000000000000000']
        out=bootstrap_certificate(request(2,q))
        self.assertEqual([e['base_lengths'] for e in out['edges']],[[4,4],[8,4],[8,8]])
        self.assertEqual([e['base_beta'] for e in out['edges']],['24']*3)

if __name__=='__main__':
    unittest.main()
