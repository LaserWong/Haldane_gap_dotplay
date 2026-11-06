import numpy as np, sys
from tm_check_lib import mc, Zed
L=int(sys.argv[1]); N=int(sys.argv[2]); beta=0.5
v=mc(L,beta,N,1000+L); z=Zed(L,beta); m=v.mean(); se=v.std()/np.sqrt(N)
# batch-means s.e. (robust to heavy tails)
bm=v.reshape(100,-1).mean(1); se_b=bm.std()/10
print(L,'N',N,'ED',z,'MC',m,'se',se,'batch-se',se_b,'z',(m-z)/se)
