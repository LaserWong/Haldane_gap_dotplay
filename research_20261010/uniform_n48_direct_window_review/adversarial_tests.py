#!/usr/bin/env python3
"""Exact tests of bridge guards, independent of producer implementation."""
from fractions import Fraction as F
from pathlib import Path
import json
P=Path(__file__).resolve().parent
r=json.loads((P/'results.json').read_text());A=F(r['A_lower']);B=F(r['B_lower']);C=F(r['thermal_window_lower'])
tests={}
def rejects(name,fn):
 try:fn()
 except (AssertionError,ValueError,ZeroDivisionError):tests[name]=True;return
 raise AssertionError('failed to reject '+name)
def guard(a,b,c,n,geom,lo,hi):
 assert n==48 and geom==('T(48,21/2)','S(48,21)')
 assert 0<a<=1 and F(1,2)<b<=1 and F(1,2)<c
 assert c*c<=a**4*(2*b-1)
 assert (lo,hi)==(n,2*n)
guard(A,B,C,48,('T(48,21/2)','S(48,21)'),48,96)
rejects('thermal_coordinate_relabel96',lambda:guard(A,B,C,48,('T(96,21/2)','S(48,21)'),48,96))
rejects('uncool_spatial_beta',lambda:guard(A,B,C,48,('T(48,21/2)','S(48,21/2)'),48,96))
rejects('purity_half_boundary',lambda:guard(A,F(1,2),C,48,('T(48,21/2)','S(48,21)'),48,96))
rejects('upward_window_rounding',lambda:guard(A,B,C+F(1,10**12),48,('T(48,21/2)','S(48,21)'),48,96))
rejects('unsupported_L47',lambda:guard(A,B,C,48,('T(48,21/2)','S(48,21)'),47,96))
rejects('unsupported_L97',lambda:guard(A,B,C,48,('T(48,21/2)','S(48,21)'),48,97))
# Necessary unique-positive-leading premise: negative dominant eigenvalue gives positive
# even moments but negative sufficiently large odd moments.
spec=[F(-3,4),F(1,4)];assert sum(x**48 for x in spec)>0 and sum(x**49 for x in spec)<0
tests['negative_leader_even_moments_do_not_imply_odd_identity']=True
# Stronger even estimate w^2 >= 2w-1; endpoint identities of signed interpolation.
for j in range(51,101):
 w=F(j,100);assert w*w>=2*w-1 and w*w-(1-w)**2==2*w-1
 tests['signed_window_endpoint_identities']=True
# Direct-window gap and tail gap must overlap, and weak gap is the composed one.
assert F(r['finite_gap'])>F(r['combined_gap']) and 52<=96
assert r['bootstrap_initialization_remains']==52 and r['new50site_anchor_used'] is False
tests['coverage_overlap_and_unchanged_initialization']=True
(P/'adversarial_results.json').write_text(json.dumps({'status':'PASS','tests':tests,'count':len(tests)},indent=2)+'\n')
print(json.dumps({'status':'PASS','count':len(tests)}))
