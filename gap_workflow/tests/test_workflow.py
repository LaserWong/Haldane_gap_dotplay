"""Independent CLI integration regressions: observable outputs and evidence scope."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

class WorkflowCLITests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='gapflow-cli-test-')
        self.base=Path(self.tmp.name)
    def tearDown(self):
        self.tmp.cleanup()
    def invoke(self, request, name='case', resume=False, raw=False):
        inp=self.base/(name+'.json');out=self.base/name
        if request is not None:
            inp.write_text(request if raw else json.dumps(request))
        env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
        cmd=[sys.executable,'-m','gapflow',str(inp),'--output',str(out)]
        if resume:cmd.append('--resume')
        process=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,timeout=20)
        result=json.loads((out/'results.json').read_text()) if (out/'results.json').exists() else None
        return process,result,out
    @staticmethod
    def dimer(spins=None):
        model={'geometry':{'type':'graph','n_sites':2,'edges':[[0,1]]},'terms':[{'type':'heisenberg','J':1}]}
        model.update({'spin':0.5} if spins is None else {'spins':spins})
        return {'model':model,'certificate':{'ground_energy':'-3/4','gap_lower_bound':'1'}}
    def test_dimer_full_finite_gap(self):
        p,r,out=self.invoke(self.dimer())
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(r['status'],'certified_finite_size')
        self.assertFalse(r['uniform_family_claim'])
        self.assertIn('full space',r['claim'])
        c=json.loads((out/'certificate.json').read_text())
        self.assertTrue(c['certified']);self.assertEqual(c['gap_lower_bound'],'1')
        v=json.loads((out/'validation.json').read_text())
        self.assertTrue(v['valid']);self.assertFalse(v['independent_exact_implementation'])
    def test_decimal_lexeme_false_certificate_regression(self):
        raw='{"model":{"spin":0.5,"geometry":{"type":"graph","n_sites":1,"edges":[]},"terms":[{"type":"field_z","h":0.99999999999999999999}]},"certificate":{"ground_energy":"-1/2","gap_lower_bound":"1"}}'
        p,r,out=self.invoke(raw,raw=True)
        self.assertNotEqual(p.returncode,0)
        self.assertEqual(r['status'],'candidate_only')
        self.assertFalse(json.loads((out/'certificate.json').read_text())['certified'])
        self.assertEqual(json.loads((out/'input.json').read_text())['model']['terms'][0]['h'],'0.99999999999999999999')
    def test_bad_spin_decimal_rejected(self):
        raw='{"model":{"spin":0.50000000000000000001,"geometry":{"type":"graph","n_sites":1,"edges":[]},"terms":[]}}'
        p,r,out=self.invoke(raw,raw=True)
        self.assertEqual(r['status'],'invalid_input');self.assertNotEqual(p.returncode,0)
    def test_graph_state_uniform_exact(self):
        p,r,out=self.invoke({'model':{'family':'graph_state_projector','shape':[2,2],'h':'1','target_gap':'1/2'}})
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(r['status'],'certified_uniform_family');self.assertTrue(r['uniform_family_claim'])
        c=json.loads((out/'certificate.json').read_text());self.assertTrue(c['target_verified'])
        self.assertEqual(c['full_family_gap_exact'],'1')
        self.assertFalse(json.loads((out/'resources.json').read_text())['basis_allocated'])
    def test_matching_resume_reuses_terminal_result(self):
        p,r,out=self.invoke(self.dimer());before=(out/'results.json').read_bytes()
        p2,r2,_=self.invoke(None,resume=True)
        self.assertEqual(p2.returncode,0,p2.stderr);self.assertEqual(r,r2)
        self.assertEqual((out/'results.json').read_bytes(),before)
    def test_tampered_artifact_resume_rejected(self):
        p,r,out=self.invoke(self.dimer());result_before=(out/'results.json').read_bytes()
        path=out/'certificate.json';path.write_text(path.read_text()+'\n')
        p2,_,_=self.invoke(None,resume=True)
        self.assertNotEqual(p2.returncode,0);self.assertIn('hash mismatch',p2.stdout+p2.stderr)
        self.assertEqual((out/'results.json').read_bytes(),result_before)
    def test_hard_wall_timeout_is_not_gaplessness(self):
        q=self.dimer();q['budget']={'wall_seconds':0.000001}
        p,r,out=self.invoke(q)
        self.assertNotEqual(p.returncode,0);self.assertEqual(r['status'],'resource_limit')
        self.assertEqual(r['model_gapless'],'not established');self.assertFalse(r['uniform_family_claim'])
        self.assertIn('wall-time',r['reason'])
    def test_dimension_resource_admission_blocks_allocation(self):
        q=self.dimer();q['budget']={'max_dimension':2}
        p,r,out=self.invoke(q)
        self.assertEqual(r['status'],'resource_limit');self.assertFalse((out/'candidate.json').exists())
        self.assertEqual(r['model_gapless'],'not established')
    def test_sector_scope_does_not_become_full_gap(self):
        q=self.dimer();q['model']['terms'].append({'type':'field_z','h':2})
        # M=0 eigenvalues are -3/4,1/4. The full-space ground is -7/4,
        # so the certified sector ground is deliberately not the physical ground.
        q['solver']={'total_m2':0}
        p,r,out=self.invoke(q)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(r['status'],'certified_finite_size')
        self.assertIn('selected magnetization sector only',r['claim']);self.assertNotIn('in the full space',r['claim'])
        self.assertFalse(r['uniform_family_claim'])
        self.assertEqual(json.loads((out/'candidate.json').read_text())['sector'],0)
    def test_mixed_spin_generalized_pencil(self):
        q=self.dimer([0.5,1]);q['certificate']={'ground_energy':'-1','gap_lower_bound':'3/2'}
        p,r,out=self.invoke(q)
        self.assertEqual(p.returncode,0,p.stderr+'\n'+json.dumps(r))
        self.assertEqual(r['status'],'certified_finite_size')
        c=json.loads((out/'certificate.json').read_text())
        self.assertTrue(c['certified']);self.assertEqual(c['ground_multiplicity'],2)
        self.assertEqual(c['gap_lower_bound'],'3/2');self.assertIn('pencil',c['evidence'])
        self.assertFalse(r['uniform_family_claim'])

    def test_ising_obstruction_is_not_gaplessness(self):
        q=self.dimer();q.pop('certificate')
        q['model']['terms']=[{'type':'xxz','Jxy':0,'Jz':-1}]
        p,r,out=self.invoke(q)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(r['status'],'certified_finite_size')
        self.assertFalse(r['model_gapless']);self.assertFalse(r['uniform_family_claim'])
        c=json.loads((out/'certificate.json').read_text())
        self.assertEqual(c['ground_degeneracy'],2);self.assertEqual(c['gap_above_ground_space'],'1/2')
        self.assertEqual(c['thermal_purity_upper_bound'],'1/2')
        self.assertEqual(r['diagnostics']['failure_class'],'rigorous_method_specific_obstruction')
        self.assertFalse(json.loads((out/'resources.json').read_text())['basis_allocated'])
    def test_transverse_model_rejects_magnetization_sector(self):
        q=self.dimer();q['model']['terms']=[{'type':'spin_product','coefficient':1,'factors':[{'site':0,'operator':'x'}]}]
        q['solver']={'total_m2':0}
        p,r,out=self.invoke(q)
        self.assertNotEqual(p.returncode,0);self.assertEqual(r['status'],'invalid_or_unsupported_input')
        self.assertIn('does not preserve total Sz',r['reason']);self.assertFalse(r['uniform_family_claim'])

    def test_changed_code_provenance_refuses_resume(self):
        p,r,out=self.invoke(self.dimer());before=(out/'results.json').read_bytes()
        path=out/'checkpoint.json';checkpoint=json.loads(path.read_text())
        checkpoint['execution_provenance']['code_sha256']='0'*64
        path.write_text(json.dumps(checkpoint))
        p2,_,_=self.invoke(None,resume=True)
        self.assertNotEqual(p2.returncode,0);self.assertIn('provenance differs',p2.stdout+p2.stderr)
        self.assertEqual((out/'results.json').read_bytes(),before)
    def test_complete_sector_partition_covers_full_model(self):
        q=json.loads((ROOT/'examples'/'square_large_d.json').read_text())
        p,r,out=self.invoke(q)
        self.assertEqual(p.returncode,0,p.stderr+str(r));self.assertEqual(r['status'],'certified_finite_size')
        c=json.loads((out/'certificate.json').read_text());v=json.loads((out/'validation.json').read_text())
        self.assertTrue(c['coverage_complete']);self.assertTrue(v['coverage_complete'])
        self.assertIn('full space',r['claim']);self.assertFalse(r['uniform_family_claim'])

    def test_pinned_ising_registered_uniform_lower_bound(self):
        p,r,out=self.invoke({'model':{'family':'pinned_ferromagnetic_ising','shape':[2,2],'J':'100','h':'2','target_gap':'1'}})
        self.assertEqual(p.returncode,0,p.stderr+str(r));self.assertEqual(r['status'],'certified_uniform_family')
        self.assertTrue(r['uniform_family_claim']);self.assertFalse(r['model_gapless'])
        c=json.loads((out/'certificate.json').read_text())
        self.assertTrue(c['target_verified']);self.assertEqual(c['analytic_gap_lower_bound'],'2')
        self.assertFalse(c['physical_gap_is_claimed_exact']);self.assertIn('at least 2',r['claim'])
        self.assertFalse(json.loads((out/'resources.json').read_text())['basis_allocated'])
    def test_pinned_search_budget_does_not_claim_success(self):
        p,r,out=self.invoke({'model':{'family':'pinned_ferromagnetic_ising','shape':[2,2],'max_power':1}})
        self.assertNotEqual(p.returncode,0);self.assertEqual(r['status'],'insufficient_evidence')
        self.assertFalse(r['uniform_family_claim']);self.assertEqual(r['model_gapless'],'not established')
        self.assertEqual(len(json.loads((out/'bootstrap.json').read_text())['search']),1)
        p,r,out=self.invoke({'model':{'family':'pinned_ferromagnetic_ising','shape':[2],'max_power':101}},name='invalidpower')
        self.assertNotEqual(p.returncode,0);self.assertEqual(r['status'],'invalid_or_unsupported_input')
    def test_registered_gapless_is_family_not_finite_gaplessness(self):
        p,r,out=self.invoke({'model':{'family':'ferromagnetic_heisenberg_chain','J':'2/3'}})
        self.assertEqual(p.returncode,0,p.stderr+str(r));self.assertEqual(r['status'],'certified_gapless_family')
        self.assertTrue(r['physical_gaplessness']);self.assertTrue(r['uniform_family_claim'])
        self.assertTrue(r['diagnostics']['finite_size_gap_positive'])
        c=json.loads((out/'certificate.json').read_text())
        self.assertEqual(c['ground_space_dimension'],'L+1');self.assertEqual(c['J'],'2/3')
        self.assertIn('full Hilbert space',c['scope']);self.assertFalse(c['general_gaplessness_algorithm'])
        self.assertFalse(json.loads((out/'resources.json').read_text())['basis_allocated'])
    def test_gapless_bad_parameters_and_overrides_rejected(self):
        for i,model in enumerate([{'family':'ferromagnetic_heisenberg_chain','J':'-1'},
                                  {'family':'ferromagnetic_heisenberg_chain','J':1,'h':1}]):
            p,r,out=self.invoke({'model':model},name='badgapless'+str(i))
            self.assertNotEqual(p.returncode,0);self.assertFalse(r['uniform_family_claim'])
            self.assertNotEqual(r['model_gapless'],True)
        p,r,out=self.invoke({'model':{'family':'ferromagnetic_heisenberg_chain'},'solver':{'total_m2':0}},name='badsector')
        self.assertNotEqual(p.returncode,0);self.assertFalse(r['uniform_family_claim'])

    def test_unknown_ground_multiplicity_inferred_without_input(self):
        q=json.loads((ROOT/'examples'/'unknown_degeneracy_chain.json').read_text())
        self.assertNotIn('certificate',q)
        p,r,out=self.invoke(q)
        self.assertEqual(p.returncode,0,p.stderr+str(r));self.assertEqual(r['status'],'certified_finite_size')
        c=json.loads((out/'certificate.json').read_text())
        self.assertEqual(c['true_ground_multiplicity'],2)
        self.assertEqual(c['distinct_ground_cluster_roots'],1)
        self.assertIsNotNone(c['true_ground_gap_lower'])
        self.assertFalse(json.loads((out/'validation.json').read_text())['ground_multiplicity_assumed'])
    def test_tiny_split_cluster_does_not_become_true_ground_gap(self):
        q=json.loads((ROOT/'examples'/'unknown_degeneracy_chain.json').read_text())
        q['model']['terms'].append({'type':'field_z','h':'1/10000000000'})
        p,r,out=self.invoke(q)
        self.assertEqual(r['status'],'certified_low_energy_cluster',p.stderr+str(r))
        c=json.loads((out/'certificate.json').read_text())
        self.assertEqual(c['low_band_rank'],2);self.assertEqual(c['distinct_ground_cluster_roots'],2)
        self.assertIsNone(c['true_ground_multiplicity']);self.assertIsNone(c['true_ground_gap_lower'])
        self.assertIn('Ground multiplicity remains unknown',r['claim']);self.assertFalse(r['uniform_family_claim'])

if __name__=='__main__':unittest.main()
