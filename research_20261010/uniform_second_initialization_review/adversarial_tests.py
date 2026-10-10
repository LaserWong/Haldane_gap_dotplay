#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
import json
P=Path(__file__).resolve().parent;A=P.with_name('uniform_second_initialization_scalar');c=json.loads((A/'certificate.json').read_text());tests={}
def check(x):
 assert len(x['improved_states'])==len(x['all_integer_windows'])==11
 prev=None
 for j,(s,w) in enumerate(zip(x['improved_states'],x['all_integer_windows'])):
  n=36*2**j;b=F(49,4)*2**j;S,T=F(s['S']),F(s['T']);assert s['n']==n and F(s['beta'])==b and (w['from'],w['to'])==(n,2*n) and F(w['beta'])==b and F(w['gap'])==F(23,5000)
  if prev:
   a,t=prev;G=lambda z:1-(1-z)**2/(2*z*z);assert S<=G(a*a*t) and T<=G(t*t*S)
  else:assert S<=F(x['seed']['S']) and T<=F(x['seed']['T72'])
  prev=S,T
 assert x['asymptotic']['from']==36864 and F(x['asymptotic']['beta'])==12544
check(c)
def bad(name,change):
 x=deepcopy(c);change(x)
 try:check(x)
 except AssertionError:tests[name]=True;return
 raise AssertionError(name)
bad('missing_window',lambda x:x['all_integer_windows'].pop(4))
bad('wrong_spatial_base',lambda x:x['improved_states'][0].update(n=72))
bad('wrong_beta',lambda x:x['all_integer_windows'][0].update(beta='49/2'))
bad('window_gap',lambda x:x['all_integer_windows'][4].update({'from':577}))
bad('inflated_spatial_seed',lambda x:x['improved_states'][0].update(S='1'))
bad('inflated_thermal_update',lambda x:x['improved_states'][1].update(T='1'))
bad('inflated_gap_label',lambda x:x['all_integer_windows'][0].update(gap='1/100'))
bad('premature_asymptotic_onset',lambda x:x['asymptotic'].update({'from':18432}))
# Odd moments cannot be replaced with their absolute values in F_J.
J={5:F(2925+3*2960742,4*10**6),7:F(54069+3*1920414,4*10**6)}
N5=F(2925-2960742,4*10**6);assert N5<0
# J filter has odd terms even though F_J is globally nonnegative.
q=[7,17,-280,-185,1000];co=[sum(q[i]*q[k-i] for i in range(5) if 0<=k-i<5) for k in range(9)];assert any(co[k] for k in (1,3,5,7));assert min(co)<0
tests['signed_odd_terms_and_negative_endpoint_coefficients_retained']=True
# Replacing a periodic odd physical identity with even-only positivity is invalid.
assert (-F(3,4))**48+F(1,4)**48>0 and (-F(3,4))**49+F(1,4)**49<0
tests['odd_trace_requires_physical_identity']=True
(P/'adversarial_results.json').write_text(json.dumps({'status':'PASS','count':len(tests),'tests':tests},indent=2)+'\n');print('PASS',len(tests))
