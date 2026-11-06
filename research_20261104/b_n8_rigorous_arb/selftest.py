# Cross-check the limb/BLAS/int64-wrap exact products against pure python integers on random data.
import numpy as np, scipy.sparse as sp
from common import limbs, gram_part, LB
rng=np.random.default_rng(1); m=300
V=np.linalg.qr(rng.standard_normal((m,m)))[0]
Xi,A,B=limbs(V)
with np.errstate(over='ignore'): G=gram_part(A,B,A,B)
X=[[int(x) for x in r] for r in Xi]
for (i,j) in [(0,0),(3,7),(299,1),(150,150)]:
    ex=sum(X[t][i]*X[t][j] for t in range(m))-(2**76 if i==j else 0); assert ex==int(G[i,j]),(i,j,ex,G[i,j])
Hs=sp.random(m,m,density=0.05,random_state=2,data_rvs=lambda n:np.rint(rng.uniform(-2**33,2**33,n)))
Hd=Hs.toarray().astype(object)
Xi2=(A.astype(np.int64)<<LB)+B.astype(np.int64); C2=Xi2>>26;C1=(Xi2>>13)&8191;C0=Xi2&8191
assert (Xi2==Xi).all()
f=lambda M:(Hs@M.astype(float)).astype(np.int64)
with np.errstate(over='ignore'): R=(f(C2)<<26)+(f(C1)<<13)+f(C0)
for (i,j) in [(0,0),(5,9),(299,299)]:
    ex=sum(int(Hd[i,t])*X[t][j] for t in range(m)); assert ex%2**64==int(R[i,j])%2**64
print('selftest OK (exact products agree with python ints mod 2^64; true values small so equal)')
