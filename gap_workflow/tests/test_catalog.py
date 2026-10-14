import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from gapflow.catalog import match_catalog,inspect_catalog_artifacts


def spec(L=4):
    return {'spin':1,'geometry':{'type':'lattice','shape':[L],'periodic':True},
            'terms':[{'type':'heisenberg','J':1}]}


class CatalogTests(unittest.TestCase):
    def test_exact_match_and_size_two(self):
        for L in (2,3,34):
            r=match_catalog(spec(L))
            self.assertEqual(r['status'],'HISTORICAL_CERTIFICATE_MATCH')
            self.assertEqual(r['historical_claim']['gap_lower'],'31/1250')
            self.assertFalse(r['freshly_independently_replayed'])
            self.assertFalse(r['computed_finite_bound_overridden'])

    def test_wrong_models(self):
        bad=[]
        a=spec();a['spin']=0.5;bad.append(a)
        a=spec();a['geometry']['periodic']=False;bad.append(a)
        a=spec(2);a['geometry']['bond_convention']='simple_graph';bad.append(a)
        a=spec();a['terms'][0]['J']='2';bad.append(a)
        a=spec();a['terms'].append({'type':'onsite_d','D':'1/100'});bad.append(a)
        a=spec();a['terms'].append({'type':'field_z','h':'0'});bad.append(a)
        a=spec();a['terms'][0]['sites']=[0,1];bad.append(a)
        for model in bad:
            self.assertEqual(match_catalog(model)['status'],'NO_CATALOG_MATCH')

    def test_no_near_unit_rounding(self):
        a=spec();a['terms'][0]['J']='100000000000000000001/100000000000000000000'
        self.assertEqual(match_catalog(a)['status'],'NO_CATALOG_MATCH')

    def test_input_not_mutated(self):
        a=spec();original=copy.deepcopy(a)
        match_catalog(a)
        self.assertEqual(a,original)

    def test_available_raw_snapshot(self):
        root=Path(__file__).resolve().parents[1]/'catalog_sources'
        r=match_catalog(spec(),root)
        check=r['artifact_inspection']
        self.assertEqual(check['status'],'ARTIFACTS_UNAVAILABLE')
        self.assertGreaterEqual(check['verified_count'],6)
        self.assertGreater(check['missing_count'],0)
        self.assertEqual(check['mismatched'],[])
        self.assertFalse(check['documentation_hashes_checked'])

    def test_raw_tamper_and_changed_prose(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'raw.json').write_text('{}\n');(p/'README.md').write_text('Rewritten prose')
            c={'raw_dependencies_sha256':{'raw.json':hashlib.sha256(b'{}\n').hexdigest()},'identity_scope':'test'}
            self.assertEqual(inspect_catalog_artifacts(p,c)['status'],'LISTED_RAW_IDENTITIES_VERIFIED')
            (p/'raw.json').write_text('{"changed":true}')
            self.assertEqual(inspect_catalog_artifacts(p,c)['status'],'RAW_IDENTITY_MISMATCH')

    def test_reject_dependency_escape(self):
        with tempfile.TemporaryDirectory() as d:
            c={'raw_dependencies_sha256':{'../outside':'0'*64},'identity_scope':'test'}
            self.assertEqual(len(inspect_catalog_artifacts(d,c)['unreadable']),1)

if __name__=='__main__':unittest.main()
