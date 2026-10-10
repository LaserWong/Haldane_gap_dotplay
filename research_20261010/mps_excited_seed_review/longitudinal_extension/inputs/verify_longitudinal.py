#!/usr/bin/env python3
from pathlib import Path
import json
P=Path(__file__).resolve().parent
raw=lambda p:dict(line.strip().split('=') for line in p.read_text().splitlines())
a=raw(P/'contractions_n24.out');b=raw(P.parent/'contractions_n24.out')
assert a==b
for r in json.loads((P/'source_checks.json').read_text())['fixtures']:
 n=r['n'];assert r['norm']==a[f'N1_{n}'] and r['H_numerator']==a[f'H1_{n}'] and r['psi_cross_inner_product']=='0'
d=json.loads((P/'exact_witness_data.json').read_text())
for r in d['rows']:
 n=r['n'];assert r['retained_denominator_span_dimension']==4
 assert r['norm_phi_z']==a[f'N1_{n}'];assert r['H_numerator_phi_z']==a[f'H1_{n}'];assert r['alpha_z']==r['alpha1']
print('PASS: exact longitudinal norm/H, tiny direct vectors, and all24-site source contraction outputs')
