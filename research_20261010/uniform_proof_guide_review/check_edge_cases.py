#!/usr/bin/env python3
"""Cheap exact edge cases for the reviewed explanatory claims."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent;pins={}
def rd(rel):
 raw=(R/rel).read_bytes();pins[rel]=hashlib.sha256(raw).hexdigest();return raw
def js(rel):return json.loads(rd(rel))
def ints(rel):return {k:int(v) for k,v in (line.split('=') for line in rd(rel).decode().splitlines())}
checks=[]
# Recompute the positive own-length 25-site Rayleigh fraction from sealed integers.
i=ints('uniform_direct25_coverage_review/anchor25.out');ray=F(i['H0_25'],i['N0_25'])+25*F(700741,500000)
c=js('uniform_direct25_coverage/certificate.json');assert ray==F(c['shifted_total_Rayleigh'])>0 and 0<F(c['Z25_2beta_lower'])<1
checks.append('positive own-length MPS25 Rayleigh and numerator penalty retained')
wrong=25*F(i['H0_25'],i['N0_25'])+25*F(700741,500000);assert wrong!=ray
checks.append('double counting the total-energy length factor is detected')
assert -1//32==-1 and int(F(-1,32))==0
checks.append('negative coordinate floor is distinct from truncation to zero')
M=js('uniform_second_moment_optimization/certificate.json')['moment_intervals']
for n in [5,7,9,11]:assert F(M['N'][n-4][1])<0
checks.append('all four odd nontrivial-sector upper moments are negative')
for n in [24,26,28,30,32,34]:
 d=js('uniform_smaller_second_initialization/long_certificate.json')
 assert F(d['J'+str(n)]['bound'])+3*F(d['N'+str(n)]['bound'])!=F(d['J'+str(n)]['bound'])+F(d['N'+str(n)]['bound'])
checks.append('dropping nontrivial-sector multiplicity three changes every finite even bound')
# Positive endpoints are not a full-domain nonnegativity certificate.
f=lambda x:(x-F(1,2))**2-F(1,100)
assert f(F(0))>0 and f(F(1))>0 and f(F(1,2))<0
checks.append('an endpoint-only polynomial positivity test is insufficient')
rows=js('uniform_smaller_second_initialization/certificate.json')['rows']
b30=next(r for r in rows if r['n']==30);b34=next(r for r in rows if r['n']==34)
assert F(b30['gap'])<F(31,1250)==F(b34['gap'])
checks.append('the n30 certificate does not provide the stronger n34 gap')
def G(z):return 1-(1-z)**2/(2*z*z)
p0,p1=b34['states'][:2];s,t=F(p0['S']),F(p0['T']);sn,tn=F(p1['S']),F(p1['T'])
assert sn<=G(s*s*t) and tn<=G(t*t*sn)
assert G(t*t*sn)!=G(t*t*s)
# A high-purity fixture makes the old-value mistake strictly too weak.
sf=tf=F(99,100);snf=G(sf*sf*tf);tnf=G(tf*tf*snf)
assert tnf>G(tf*tf*sf)
checks.append('the staggered second update uses the new spatial endpoint, with an exact separating fixture')
assert set(range(2,4))|set(range(4,26))|set(range(26,34))==set(range(2,34))
assert set(range(2,4))|set(range(4,26))|set(range(26,33))!=set(range(2,34))
checks.append('omitting length33 creates a genuine coverage hole')
r=js('uniform_n24_second_coverage_review/results.json')
assert r['certified_lengths']==[24] and F(r['anchor48_shifted_total_Rayleigh'])<0
assert next(v for v in r['rows'] if v['L']==25)['passed'] is False
checks.append('L24 uses MPS48 and the failed L25 parity bound is not an accepted certificate')
out={'status':'PASS','checks':checks,'input_sha256':pins,'physical_contractions_performed':False}
(P/'EDGE_CASE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks)},indent=2))
