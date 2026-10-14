import json
import math
from decimal import Decimal
import unittest
import tempfile
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
from gapflow.model import Model
from gapflow.resources import plan_resources, sweep_resources, summarize_seed_evidence


def chain(n=2,spin=0.5,periodic=False,convention='positive_direction_multigraph'):
    return Model.from_dict({'spin':spin,'geometry':{'type':'lattice','shape':[n],'periodic':periodic,'bond_convention':convention},'terms':[{'type':'heisenberg','J':1}]})


class TestModel(unittest.TestCase):
    def test_half_dimer(self):
        m=chain()
        h=m.hamiltonian(matrix_free=False).toarray()
        np.testing.assert_allclose(np.linalg.eigvalsh(h),[-.75,.25,.25,.25])
        exact=m.exact_hamiltonian()
        self.assertEqual(exact[1][2],Fraction(1,2))
        self.assertEqual(exact[1][1],Fraction(-1,4))
        np.testing.assert_allclose(np.asarray(exact,dtype=float),h)

    def test_periodic_normalization(self):
        m=chain(spin=1,periodic=True)
        simple=chain(spin=1,periodic=True,convention='simple_graph')
        self.assertEqual(len(m.edges),2)
        self.assertEqual(len(simple.edges),1)
        np.testing.assert_allclose(m.hamiltonian(matrix_free=False).toarray(),2*simple.hamiltonian(matrix_free=False).toarray())
        ev=np.linalg.eigvalsh(m.hamiltonian(matrix_free=False).toarray())
        self.assertAlmostEqual(ev[1]-ev[0],2)
        np.testing.assert_allclose(np.array(m.exact_hamiltonian(),dtype=float),m.hamiltonian(matrix_free=False).toarray(),atol=1e-14)

    def test_three_dimensional_cube(self):
        m=Model.from_dict({'spin':.5,'geometry':{'type':'lattice','shape':[2,2,2]},'terms':[{'type':'xxz','Jxy':1,'Jz':.7}]})
        self.assertEqual(len(m.edges),12)
        self.assertEqual(m.hilbert_dimension,256)
        self.assertEqual(m.dimension(0),70)

    def test_matrix_free_and_sector(self):
        m=chain(5)
        full=m.hamiltonian(matrix_free=False).toarray()
        v=np.arange(32)+1j*np.arange(32)[::-1]
        np.testing.assert_allclose(m.hamiltonian()@v,full@v)
        np.testing.assert_allclose(full,full.T)
        sector=m.hamiltonian(total_m2=1,matrix_free=False).toarray()
        full_index={s:i for i,s in enumerate(m.basis().states)}
        rows=[full_index[s] for s in m.basis(1).states]
        np.testing.assert_allclose(sector,full[np.ix_(rows,rows)])
        self.assertEqual(sum(m.sector_dimensions().values()),32)

    def test_huge_counts_without_basis(self):
        m=chain(100)
        self.assertEqual(m.hilbert_dimension,2**100)
        self.assertEqual(m.dimension(0),math.comb(100,50))
        self.assertEqual(len(m.basis(100)),1)
        with self.assertRaises(MemoryError):m.basis()

    def test_graph_mixed_spins_and_diagonal(self):
        m=Model.from_dict({'spins':[.5,1], 'geometry':{'type':'graph','n_sites':2,'edges':[[0,1]],'positions':[[0,0,0],[1,2,3]]},'terms':[{'type':'onsite_d','D':'1/3'},{'type':'field_z','h':'-0.2','sites':[0]}]})
        self.assertEqual(m.hilbert_dimension,6)
        np.testing.assert_allclose(np.array(m.exact_hamiltonian(),dtype=float),m.hamiltonian(matrix_free=False).toarray())
        bad=Model.from_dict({'spins':[.5,1],'geometry':{'type':'graph','n_sites':2,'edges':[[0,1]]},'terms':[{'type':'heisenberg','J':1}]})
        with self.assertRaises(ValueError):bad.exact_hamiltonian()

    def test_arbitrary_spin_exact_pencil(self):
        for spins in ([.5,1],[1.5,2],[2,2],[.5,1,1.5]):
            model=Model.from_dict({'spins':spins,'geometry':{'type':'graph','n_sites':len(spins),'edges':[[i,i+1] for i in range(len(spins)-1)]},'terms':[{'type':'xxz','Jxy':'2/3','Jz':'-3/7'},{'type':'onsite_d','D':'1/11'},{'type':'field_z','h':'2/13'}]})
            for sector in (None,min(model.sector_dimensions(),key=abs)):
                a,w=model.exact_pencil(total_m2=sector)
                self.assertTrue(all(v>0 and isinstance(v,int) for v in w))
                self.assertEqual(a,[list(r) for r in zip(*a)])
                af=np.asarray(a,dtype=float)
                normal=model.hamiltonian(total_m2=sector,matrix_free=False).toarray()
                np.testing.assert_allclose(af/np.sqrt(np.outer(w,w)),normal,atol=1e-14)
                np.testing.assert_allclose(eigvalsh(af,np.diag(w)),np.linalg.eigvalsh(normal),atol=1e-13)

    def test_pencil_matches_existing_exact_backend(self):
        for spin in (.5,1):
            model=chain(3,spin=spin)
            a,w=model.exact_pencil()
            exact=model.exact_hamiltonian()
            np.testing.assert_allclose(np.array(a,dtype=float)/np.sqrt(np.outer(w,w)),np.array(exact,dtype=float),atol=1e-14)
        with self.assertRaises(MemoryError):chain(4,spin=2).exact_pencil(max_dimension=64)

    def test_real_spin_products_against_pauli_kron(self):
        x=np.array([[0,1],[1,0]],dtype=float)/2
        z=np.diag([-.5,.5])
        identity=np.eye(2)
        def kron(factors):
            out=np.array([[1.]])
            for factor in factors: out=np.kron(out,factor)
            return out
        terms=[{'type':'spin_product','coefficient':'-4','factors':[{'site':0,'operator':'z'},{'site':1,'operator':'z'}]},
               {'type':'spin_product','coefficient':'-2/3','factors':[{'site':2,'operator':'x'}]},
               {'type':'spin_product','coefficient':'8','factors':[{'site':0,'operator':'z'},{'site':1,'operator':'x'},{'site':2,'operator':'z'}]}]
        m=Model.from_dict({'spin':.5,'geometry':{'type':'graph','n_sites':3,'edges':[]},'terms':terms})
        expected=-4*kron([z,z,identity])-2/3*kron([identity,identity,x])+8*kron([z,x,z])
        np.testing.assert_allclose(m.hamiltonian(matrix_free=False).toarray(),expected)
        np.testing.assert_allclose(m.hamiltonian()@np.arange(8),expected@np.arange(8))
        np.testing.assert_allclose(np.array(m.exact_hamiltonian(),dtype=float),expected)
        a,w=m.exact_pencil()
        np.testing.assert_allclose(np.array(a,dtype=float)/np.sqrt(np.outer(w,w)),expected)
        self.assertFalse(m.preserves_total_sz)
        for call in (lambda:m.basis(1),lambda:m.hamiltonian(1),lambda:m.exact_pencil(1),lambda:plan_resources(m,total_m2=1)):
            with self.assertRaises(ValueError):call()

    def test_mixed_spin_product_pencil(self):
        m=Model.from_dict({'spins':[1,1.5],'geometry':{'type':'graph','n_sites':2,'edges':[]},'terms':[{'type':'spin_product','coefficient':'3/7','factors':[{'site':0,'operator':'x'},{'site':1,'operator':'z'}]},{'type':'spin_product','coefficient':'2','factors':[]}]})
        x=np.array([[0,1,0],[1,0,1],[0,1,0]],dtype=float)/np.sqrt(2)
        z=np.diag([-1.5,-.5,.5,1.5])
        expected=3/7*np.kron(x,z)+2*np.eye(12)
        a,w=m.exact_pencil()
        self.assertEqual(a,[list(r) for r in zip(*a)])
        np.testing.assert_allclose(np.array(a,dtype=float)/np.sqrt(np.outer(w,w)),expected,atol=1e-14)
        np.testing.assert_allclose(m.hamiltonian(matrix_free=False).toarray(),expected,atol=1e-14)
        with self.assertRaises(ValueError):m.exact_hamiltonian()

    def test_spin_product_rejects_unsupported_and_duplicate(self):
        base={'spin':.5,'geometry':{'type':'graph','n_sites':2,'edges':[]}}
        for factors in ([{'site':0,'operator':'y'}],[{'site':0,'operator':'x'},{'site':0,'operator':'z'}],[{'site':2,'operator':'x'}]):
            with self.assertRaises(ValueError):Model.from_dict(dict(base,terms=[{'type':'spin_product','coefficient':1,'factors':factors}]))
        diagonal=Model.from_dict(dict(base,terms=[{'type':'spin_product','coefficient':1,'factors':[{'site':0,'operator':'z'},{'site':1,'operator':'z'}]}]))
        self.assertTrue(diagonal.preserves_total_sz)
        self.assertEqual(diagonal.dimension(0),2)

    def test_spin_quantization_uses_exact_input(self):
        for invalid in (Decimal('0.50000000000000000001'), Decimal('0.49999999999999999999'), Decimal('1.000000000000000000001'), Decimal('NaN'), Decimal('Infinity'), Fraction(100000000000000000001,200000000000000000000)):
            with self.subTest(spin=invalid):
                with self.assertRaises(ValueError): chain(spin=invalid)
        self.assertEqual(chain(spin=Decimal('0.50000000000000000000')).spins2,(1,1))
        self.assertEqual(chain(spin=Fraction(3,2)).spins2,(3,3))

    def test_explicit_edges_and_terms(self):
        m=Model.from_dict({'spin':.5,'geometry':{'type':'graph','n_sites':3,'edges':[[0,1],[0,1],[1,2]]},'terms':[{'type':'heisenberg','sites':[0,2],'J':'2/3'}]})
        self.assertEqual(len(m.edges),3)
        self.assertEqual(len(m.terms),1)
        self.assertEqual(m.terms[0][3],Fraction(2,3))

    def test_fail_closed(self):
        base={'spin':.5,'geometry':{'type':'lattice','shape':[2]},'terms':[]}
        for term in ({'type':'biquadratic','J':1},{'type':'heisenberg','J':1,'Dx':2},{'type':'heisenberg'},{'type':'field_x','h':1}):
            with self.assertRaises(ValueError):Model.from_dict(dict(base,terms=[term]))
        with self.assertRaises(ValueError):chain(1,periodic=True)
        with self.assertRaises(ValueError):chain(spin=.3)
        with self.assertRaises(ValueError):chain().basis(1)
        with self.assertRaises(ValueError):Model.from_dict(dict(base,typo=True))


class TestResources(unittest.TestCase):
    def test_estimates_and_dimensions(self):
        m=chain(10)
        p=plan_resources(m,total_m2=0,trial_rank=5,mps_bond=3,memory_budget_bytes=10**9)
        self.assertEqual(p['full_hilbert_dimension'],1024)
        self.assertEqual(p['computational_dimension'],252)
        self.assertEqual(p['linear_trial_rank'],5)
        self.assertEqual(p['mps_bond_dimension'],3)
        self.assertEqual(p['bytes']['real_vector'],252*8)
        self.assertTrue(p['admits_matrix_free'])
        self.assertIsNone(p['timing']['matrix_free_seconds'])
        self.assertGreater(p['bytes']['dense_matrix'],p['bytes']['trial_vectors'])

    def test_budget_and_calibration(self):
        m=chain(4)
        p=plan_resources(m,trial_rank=2,memory_budget_bytes=1)
        self.assertFalse(p['admits_dense']);self.assertFalse(p['admits_matrix_free'])
        p=plan_resources(m,trial_rank=2,memory_budget_bytes=10**8,time_budget_seconds=1)
        self.assertIsNone(p['admits_matrix_free'])
        p=plan_resources(m,trial_rank=2,memory_budget_bytes=10**8,time_budget_seconds=1,calibration={'dimension':16,'expanded_term_count':3,'matvec_seconds':.0001,'dense_eigh_seconds':.002})
        self.assertAlmostEqual(p['timing']['matrix_free_seconds'],.02)
        self.assertTrue(p['admits_matrix_free'])
        self.assertFalse(p['timing']['rigorous_bound'])

    def test_sweeps_do_not_invent_minimum(self):
        self.assertEqual(len(sweep_resources([chain(2),chain(3)],trial_rank=2)),2)
        report=summarize_seed_evidence([{'physical_size':4,'hilbert_dimension':16,'certificate_status':'failed'},{'physical_size':6,'hilbert_dimension':64,'certificate_status':'certified'}])
        self.assertEqual(report['smallest_verified_sufficient_tested_seed']['physical_size'],6)
        self.assertIsNone(report['minimum_sufficient_seed'])
        no=summarize_seed_evidence([{'physical_size':4,'hilbert_dimension':16,'certificate_status':'failed'}])
        self.assertIsNone(no['smallest_verified_sufficient_tested_seed'])

    def test_all_examples_parse(self):
        from gapflow.workflow import load_request, budget_values, compute
        family_statuses={
            'graph_state_projector':'certified_uniform_family',
            'quantum_ising_chain':'certified_uniform_family',
            'pinned_ferromagnetic_ising':'certified_uniform_family',
            'ferromagnetic_heisenberg_chain':'certified_gapless_family',
            'ferromagnetic_spin_half_heisenberg_cycle':'certified_gapless_family',
        }
        for path in (Path(__file__).resolve().parents[1]/'examples').glob('*.json'):
            with self.subTest(example=path.name):
                request=load_request(path.read_text())
                spec=request.get('model',request)
                if 'family' in spec:
                    self.assertIn(spec['family'],family_statuses,'Unregistered specialized example family')
                    request['budget']=budget_values(request.get('budget',{}))
                    with tempfile.TemporaryDirectory() as tmp:
                        result=compute(request,Path(tmp))
                        self.assertEqual(result['status'],family_statuses[spec['family']])
                else:
                    m=Model.from_dict(spec)
                    self.assertGreater(m.hilbert_dimension,0)

if __name__=='__main__':unittest.main()
