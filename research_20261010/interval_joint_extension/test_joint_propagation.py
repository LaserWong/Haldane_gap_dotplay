"""Supplementary exact monotonicity checks; not a substitute for the joint proof."""
from certify_joint_extension import *
from itertools import product

def main():
 checked=0;window=0
 for vals in product((F(49,50),F(99,100),F(1)),repeat=3):
  actual=list(vals);high,args=JS.canonical_advance(actual,JS.full_product(actual),True,digits=18)
  assert high is not None
  for scale in (F(99,100),F(999,1000),F(1)):
   lo=[x*scale for x in actual]
   for kscale in (F(99,100),F(999,1000),F(1)):
    joint=JS.full_product(actual)*kscale
    got,z=JS.canonical_advance(lo,joint,True,digits=18)
    if got is not None:assert all(x<=y for x,y in zip(got,high));checked+=1
    w,_=JS.interpolate_2d_joint(*lo,joint);wactual,_=JS.interpolate_2d_joint(*actual,JS.full_product(actual))
    assert w<=wactual;window+=1
 # Exact product identity for symbolic ladder partition values represented by
 # arbitrary positive rationals: the labels, rather than numerical coincidence,
 # determine the common final-to-initial quotient.
 ladder_tests=0
 for v in product((F(1),F(2),F(3)),repeat=4):
  p=[v[i+1]/v[i]**2 for i in range(3)]
  assert JS.full_product(p)==v[3]/v[0]**8;ladder_tests+=1
 out=dict(status='PASS producer joint scalar diagnostics',canonical_monotonicity_cases=checked,joint_window_monotonicity_cases=window,exact_trace_identity_cases=ladder_tests,warning='Analytic joint lemma remains an independently reviewed dependency, not established by finite tests.')
 (HERE/'joint_test_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
