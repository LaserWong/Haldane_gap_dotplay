#!/usr/bin/env python3
"""Floating proposal stage only; verify.py must check all candidates exactly."""
from pathlib import Path
from fractions import Fraction as F
import json,os,resource
os.sched_setaffinity(0,{0});resource.setrlimit(resource.RLIMIT_AS,(700*1024**2,700*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(600,600))
import numpy as np
from scipy.optimize import root
P=Path(__file__).resolve().parent;d=json.load(open(P.parent/'uniform_transfer_moment_assessment/results.json'));out={}
for name,rr in d['hankel_caps'].items():
 h=rr['x_cap']['display'];m=np.array([sum(a['display'] for a in rr['moment_intervals'][str(j)])/2 for j in (3,4,5)]);a,b,c=m;t=(h*b-c)/(h*a-b);A=(b-t*a)/(h-t);N=int((a-A)/t**3)
 for guess in [.1,.5,.9]:
  fn=lambda z:np.array([z[0]**k+N*z[1]**k+z[2]**k for k in (3,4,5)])-m
  sol=root(fn,[h,t,t*guess],tol=1e-12)
  if sol.success and min(sol.x)>0 and max(sol.x)<=h and max(abs(fn(sol.x)))<1e-12:break
 else:raise RuntimeError(name)
 out[name]={'counts':[1,N,1],'x_rational':[str(F(round(v*10**15),10**15)) for v in sol.x],'floating_residual_display':fn(sol.x).tolist()}
(P/'unit_atom_proposals.json').write_text(json.dumps(out,indent=2)+'\n')
