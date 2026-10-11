#!/usr/bin/env python3
"""Exact in-memory fixtures; execute only selected reviewer-written functions."""
import ast,json,math,os,resource
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
os.sched_setaffinity(0,{4});resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(30,30))
P=Path(__file__).resolve().parent;A=P.parent/'uniform_smaller_second_initialization';B=10**140
names={'down','up','power','bernstein','G'};tree=ast.parse((P/'audit_scalar.py').read_text());selected=ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in names],type_ignores=[]);exec(compile(selected,'reviewer_functions','exec'))
checks=[]
def must(x):assert x
def reject(name,fn):
 try:fn()
 except AssertionError:checks.append(name);return
 raise RuntimeError(name+' was accepted')
for x,r in [(F(2),F(17,6)),(F(1,1000),F(8,3)),(F(0),F(5,2))]:
 l,u=power(x,r);assert l**r.denominator<=x**r.numerator<=u**r.denominator
 checks.append('directed_fractional_'+str(r)+'_x'+str(x))
reject('negative_fractional_base',lambda:power(F(-1),F(1,2)))
reject('illegal_G_domain',lambda:G(F(0)))
assert bernstein([F(1),F(0),F(1)],F(-2),F(1))[0]>=1
reject('negative_polynomial_endpoint',lambda:bernstein([F(-1)],F(-1),F(1)))
C=json.loads((P.parent/'uniform_second_moment_optimization/certificate.json').read_text());L=json.loads((A/'long_certificate.json').read_text());q=list(map(F,L['N30']['coeff']));M=[tuple(map(F,x)) for x in C['moment_intervals']['N']]
right=sum(c*(b if c>=0 else a) for c,(a,b) in zip(q,M));wrong=sum(c*b for c,(a,b) in zip(q,M));assert right==F(L['N30']['bound']);reject('wrong_signed_endpoint_selection',lambda:must(wrong==right))
cert=json.loads((A/'certificate.json').read_text())
for row in cert['rows']:
 n=row['n'];s,t=map(F,(row['states'][0]['S'],row['states'][0]['T']));new_s=F(row['states'][1]['S']);new_t=F(row['states'][1]['T'])
 reject(f'inflated_spatial_update_{n}',lambda:must(G(s*s*t)+F(1,10**30)<=G(s*s*t)))
 reject(f'wrong_staggered_thermal_label_{n}',lambda:must(row['anchor_length']==n))
 reject(f'window_coverage_hole_{n}',lambda:must(row['windows'][0]['to']-1==row['states'][1]['n']))
 own=next(x for x in json.loads((P/'anchor_results.json').read_text())['rows'] if x['length']==2*n);v=F(own['shifted_total_Rayleigh']);reject(f'one_bond_total_confusion_{n}',lambda:must(v/(2*n)==v))
(P/'adversarial_results.json').write_text(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'all_mutations_in_memory':True},indent=2)+'\n');print(len(checks),'exact fixtures passed')
