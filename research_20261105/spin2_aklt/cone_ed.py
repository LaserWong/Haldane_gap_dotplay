"""NUMERICAL: models inside the sufficient transfer cone, h = sum_J e_J P_J with e = ray0(Heis) + mu*ray_i.
Reports E0(4),E0(8), delta4=E0(8)-2E0(4), gaps at L=4..8 (scale: e4(Heis ray)=1)."""
import numpy as np, sys, json
from jsearch import P
from ed import low
rays=[[0,0.1,0.3,0.6,1],[0,7/22,17/22,1,5/11],[0,7/11,1,9/22,15/22],[0,1,3/7,9/14,25/42]]
i=int(sys.argv[1]); mu=float(sys.argv[2])
e=np.array(rays[0])+mu*np.array(rays[i])
h=sum(e[J]*P[f'P{J}'] for J in range(5))
out={'e':e.tolist()}
for L in [4,5,6,7,8]:
    e0,_=low(L,0,h,4); e1,_=low(L,1,h,2)
    out[L]=dict(E0=e0[0],gap=min(e0[1],e1[0])-e0[0])
    print(i,mu,L,out[L],flush=True)
out['delta4']=out[8]['E0']-2*out[4]['E0']
print('RESULT',i,mu,'delta4',out['delta4'],'gap8',out[8]['gap'],'gap7',out[7]['gap'],flush=True)
json.dump(out,open(f'cone_{i}_{mu:g}.json','w'))
