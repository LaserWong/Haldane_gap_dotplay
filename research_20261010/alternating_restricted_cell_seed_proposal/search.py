import json,math,ast
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog,brentq
P=Path(__file__).resolve().parent;R=P.parents[1]
C=json.loads((P.parent/'uniform_second_moment_optimization/certificate.json').read_text())
M={s:[[F(v) for v in row] for row in C['moment_intervals'][s][::2]] for s in ['J','N']}
out={'moments':{s:[[str(v) for v in row] for row in a] for s,a in M.items()},'support':{},'majorants':{}}
for s in ['J','N']:
 mid=np.array([float((l+u)/2) for l,u in M[s]]);err=np.array([float((u-l)/2) for l,u in M[s]])
 H=np.array([[mid[i+j] for j in range(3)] for i in range(3)])
 target=1.005 if s=='J' else .78
 for k in range(6):
  q=np.linalg.solve(H,np.array([target**i for i in range(3)]));q/=q[-1]
  q=np.round(q,10);conv=np.convolve(q,q);B=conv@mid+abs(conv)@err
  target=brentq(lambda x:x*x*np.polyval(q[::-1],x)**2-B,target-.05,target+.05)
 cap=math.ceil(target*10**9+1)/10**9;out['support'][s]={'coeff':q.tolist(),'cap':str(F(str(cap)))}
 print('moments',s,mid.tolist(),err.tolist(),'support',cap,'q',q.tolist(),flush=True)
 x=np.linspace(0,cap,1601);A=x[:,None]**np.arange(5)
 for n in [15,16,17,30,32,34]:
  # polynomial majorants of x^(n-2), moments2..6
  cost=np.r_[mid,err];Ab=np.c_[-A,np.zeros_like(A)];sg1=np.c_[np.eye(5),-np.eye(5)];sg2=np.c_[-np.eye(5),-np.eye(5)]
  r=linprog(cost,A_ub=np.r_[Ab,sg1,sg2],b_ub=np.r_[-x**(n-2),np.zeros(10)],bounds=[(None,None)]*5+[(0,None)]*5,method='highs',options={'threads':1})
  assert r.success
  out['majorants'][f'{s}{n}']={'coeff':r.x[:5].tolist(),'bound_display':r.fun};print(s,n,r.fun,flush=True)
(P/'candidates.json').write_text(json.dumps(out,indent=2)+'\n')
