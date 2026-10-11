#!/usr/bin/env python3
"""Cheap exact sequence checks only; no physical matrices or contractions."""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,resource,time,os
resource.setrlimit(resource.RLIMIT_CPU,(30,30))
resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
start=time.process_time();wall=time.monotonic();p=Path(__file__).resolve().parent
spectra=[tuple(F(i,3) for i in seq) for length in range(1,5) for seq in itertools.combinations_with_replacement(range(4),length) if any(seq)]
checks=0;odd=0
for x in spectra:
 # Independent positive numerator spectra; these are abstract sequence tests.
 y=tuple((v+F(1,5))/(i+2) for i,v in enumerate(reversed(x)))
 def z(a,m):return sum(v**m for v in a)
 for n in range(2,8):
  S=z(x,2*n)/z(x,n)**2;T=z(y,2*n)/z(x,2*n)**2
  for m in range(n,2*n+1):
   assert z(y,m)**(2*n)>=z(y,2*n)**m
   assert z(x,m)**n<=z(x,n)**(2*n-m)*z(x,2*n)**(m-n)
   actual=z(y,m)/z(x,m)**2
   assert actual**(2*n)>=S**(4*n-2*m)*T**m
   checks+=1;odd+=int(n%2==1)
# The lower l^p bound is false for signed spectra, even with positive odd trace.
assert (F(2)**3-F(1))**4 < (F(2)**4+F(1))**3
# Two real symmetric positive definite matrices need not have a symmetric product.
A=[[1,0],[0,2]];B=[[1,1],[1,2]]
AB=[[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
assert AB[0][1]!=AB[1][0]
# Source proof's small-defect purity simplification is compatible with positivity.
# (1-u)^(3/2) >= 1-3u/2 follows by convexity; squared exact check here.
for j in range(101):
 u=F(j,10000);assert (1-u)**3 >= (1-F(3,2)*u)**2
out={'status':'PASS abstract exact consistency checks','sequence_window_checks':checks,'odd_cell_base_checks':odd,'signed_spectrum_counterexample':'Y eigenvalues [2,-1], n2, M3: 7^4 < 17^3','noncommuting_selfadjoint_product_counterexample':AB,'no_physical_computation':True,'resources':{'hard_CPU_seconds':30,'hard_address_space_MiB':256,'process_CPU_seconds':time.process_time()-start,'wall_seconds':time.monotonic()-wall,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(p/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
