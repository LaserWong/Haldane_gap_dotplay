import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import unittest,json,sys,resource,time
from pathlib import Path
from fractions import Fraction as Q
from certified_core import exp_bounds,G,replay
from exact_n2_exclusion import certify_upper,polynomials
from asymmetric_basin import classify
from spectral_search import exact_n2_pair
from necessary_windows import window
from optimize_bilayer_tail import sqrt_bounds,qfunc
from majorant_ceiling import delta_upper,upper_first_state,exclude_family
from axis_order_search import ordered_bilayer,canonicalize,ROOT,OUT

class Tests(unittest.TestCase):
 def test_exponential_enclosures(self):
  sys.path.insert(0,str(ROOT/'original/Haldane_extensions/code'))
  from analytic_certificates import exp_bounds as reference
  for x in [Q(-100),Q(-17,3),Q(-1),Q(-1,8),Q(0),Q(1,8),Q(1),Q(17,3),Q(100)]:
   lo,hi=exp_bounds(x);rl,rh=reference(x)
   self.assertLessEqual(lo,rl);self.assertGreaterEqual(hi,rh)
 def test_G_invariant(self):
  for k in range(1,100):
   x=Q(k,100)
   self.assertEqual(G(x)-x,(1-x)*(2*x-1)*(x+1)/(2*x*x))
  self.assertEqual(classify(Q(3,4),1)[0],'excluded')
  self.assertEqual(classify(1,Q(79,100))[0],'excluded')
 def test_small_defect_extension(self):
  u=Q(1,40)
  self.assertLess((3-3*u+u*u)**2/(2*(1-u)**6),5)
  self.assertLess((2+5*u)**2/(2*(1-(2+5*u)*u)**2),5)
  self.assertLess(Q(3,2)+5*u+2/(1-2*u),4)
  self.assertLess(4/(1-4*u),5)
 def test_polynomial_all_beta(self):
  for t,u in [(2,Q('0.012674')),(4,Q('0.002098')),(6,Q('0.000695'))]:
   r=certify_upper(t,u);self.assertTrue(r['all_beta_excluded_for_legacy_recursion'])
   leaves=sorted((Q(x['x_lo']),Q(x['x_hi'])) for x in r['leaves'])
   self.assertEqual(leaves[0][0],0);self.assertEqual(leaves[-1][1],1)
   for a,b in zip(leaves[:-1],leaves[1:]):self.assertEqual(a[1],b[0])
 def test_spectral_interval_and_windows(self):
  for t in [2,4,6]:
   pair=exact_n2_pair(t)
   self.assertTrue(pair.exclude_all_beta()['excluded'])
   self.assertTrue(window(pair,bits=12)['excluded'])
   lo,hi=pair.a.mean_gap(0,0)
   mean=sum((l*c for l,h,c in pair.a.bins),Q(0))/pair.a.dimension
   self.assertLessEqual(lo,mean);self.assertGreaterEqual(hi,mean)
 def test_sqrt(self):
  for x in [Q(0),Q(2),Q(9,4),Q(17,31)]:
   l,h=sqrt_bounds(x);self.assertLessEqual(l*l,x);self.assertGreaterEqual(h*h,x)
 def test_optimistic_majorant(self):
  paths=[ROOT/'low_energy'/f'bilayer_s1d2_{x}x{y}_g1d50_k1d50_q2_ground.json' for x,y in [(2,2),(4,2),(4,4)]]
  recs=[json.loads(p.read_text()) for p in paths]
  for beta in [Q(8),Q(12),Q(16)]:
   for rec in recs:
    floor=1+3*rec['N_dimers']*exp_bounds(-beta*delta_upper(rec))[0]
    self.assertLessEqual(floor,qfunc(rec,beta))
   for order in ['xyt','xty','txy']:
    actual=ordered_bilayer(recs,beta,order,qfunc=qfunc)
    if actual.get('correlated_first_step'):
     optimistic=upper_first_state(recs,order,beta,beta)
     self.assertIsNotNone(optimistic)
     for a,b in zip(actual['correlated_first_step'],optimistic):self.assertLessEqual(Q(a),b)
 def test_strict_majorant_family_obstruction(self):
  recs=[json.loads((ROOT/'low_energy'/f'bilayer_s1d2_{x}x{y}_g3d100_depth2_ground.json').read_text()) for x,y in [(2,2),(4,2),(4,4)]]
  for order in ['xyt','xty','txy']:
   self.assertTrue(exclude_family(recs,order)['majorant_family_excluded'])

if __name__=='__main__':
 t=time.monotonic();suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
 r=unittest.TextTestRunner(verbosity=2).run(suite)
 result={'passed':r.wasSuccessful(),'tests_run':r.testsRun,'seconds':time.monotonic()-t,
         'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'blas_threads':1,
         'scope':'Exact arithmetic regression tests; analytic theorems are separately written/audited, not proof-assistant formalized'}
 (OUT/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
 sys.exit(0 if r.wasSuccessful() else 1)
