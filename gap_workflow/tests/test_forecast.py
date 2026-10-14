import unittest
from gapflow.forecast import forecast_seed_size
class ForecastTests(unittest.TestCase):
 def rows(self,us):return [{'linear_size':2*(i+1),'defect_upper':u,'evidence':'floating_estimate'} for i,u in enumerate(us)]
 def test_no_minimum_claim(self):
  r=forecast_seed_size(self.rows([.1,.05,.025]),.001)
  self.assertEqual(r['status'],'HEURISTIC_NEXT_SEED');self.assertFalse(r['minimality_proved']);self.assertIsNone(r['true_minimum_size'])
 def test_failures_are_not_no_go(self):
  r=forecast_seed_size(self.rows([.01,.02,.03]),.001)
  self.assertEqual(r['status'],'NO_IMPROVING_TREND');self.assertEqual(r['model_gapless'],'not established')
 def test_certified_scalar_still_needs_theorem(self):
  rows=self.rows([.1,.01]);rows[-1]['evidence']='certified_bound';r=forecast_seed_size(rows,.02)
  self.assertEqual(r['smallest_tested_sufficient_size'],4);self.assertFalse(r['uniform_gap_proved'])
 def test_decimal_threshold_no_rounding(self):
  from decimal import Decimal
  r=forecast_seed_size([{'linear_size':2,'defect_upper':Decimal('0.100000000000000000000001'),'evidence':'certified_bound'}],Decimal('0.1'))
  self.assertIsNone(r['smallest_tested_sufficient_size'])
  self.assertEqual(r['status'],'INSUFFICIENT_PILOT_DATA')
 def test_low_data(self):self.assertEqual(forecast_seed_size(self.rows([.1,.05]),.001)['status'],'INSUFFICIENT_PILOT_DATA')
 def test_budget(self):self.assertEqual(forecast_seed_size(self.rows([.1,.05,.025]),.001,max_size=8)['status'],'FORECAST_OUTSIDE_SIZE_BUDGET')
if __name__=='__main__':unittest.main()
