import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np, json, hashlib, pathlib,struct,collections
p=pathlib.Path(__file__).parent;s=p.parent/'bilayer_connected_rule_compiler'
assert hashlib.sha256((s/'MANIFEST_SHA256.json').read_bytes()).hexdigest()=='e165f87b117e229c957e07f54151fab9c2798c31db961568bd3589ee900e2e66'
for f,h in json.loads((s/'MANIFEST_SHA256.json').read_text()).items():assert hashlib.sha256((s/f).read_bytes()).hexdigest()==h,f
for f,h in json.loads((s/'INPUT_SHA256.json').read_text()).items():assert hashlib.sha256((s.parent/f).read_bytes()).hexdigest()==h,f
I=np.eye(2);sx=np.array([[0,1],[1,0]])/2;sy=np.array([[0,-1j],[1j,0]])/2;sz=np.diag([1,-1])/2
H=np.zeros((16,16),complex)
for a,b in [(0,2),(1,3)]:
 for spin in [sx,sy,sz]:
  m=np.array([[1.]])
  for j in range(4):m=np.kron(m,spin if j in (a,b) else I)
  H+=2*m
r=np.array([[0,1,0,0],[1/np.sqrt(2),0,1/np.sqrt(2),0],[-1/np.sqrt(2),0,1/np.sqrt(2),0],[0,0,0,1]])
U=np.kron(r,r);M=U.T@H@U
assert np.max(abs(M-M.real.round()))<1e-12
M=M.real.round().astype(int)
with (p/'edge_table.txt').open('w') as f:
 for op in range(3):
  for src in range(16):
   a,b=src%4,src//4
   for dst in range(16):
    c,d=dst%4,dst//4;delta=(c!=0)+(d!=0)-(a!=0)-(b!=0)
    v=M[4*c+d,4*a+b] if delta==[-2,2,0][op] else 0
    f.write(str(v)+' ')
# Cartesian basis: x=(-t+ + t-)/sqrt2, y=i(t+ +t-)/sqrt2, z=t0.
T=np.zeros((4,4),complex);T[0,0]=1;T[1,1]=-1/np.sqrt(2);T[3,1]=1/np.sqrt(2);T[1,2]=1j/np.sqrt(2);T[3,2]=1j/np.sqrt(2);T[2,3]=1
MC=np.kron(T,T).conj().T@M@np.kron(T,T)
W=np.zeros((16,16))
for a in range(4):
 for b in range(4):
  if a==b==0:
   for c in (1,2,3):W[4*c+c,0]+=1
  elif not a or not b:W[4*b+a,4*a+b]+=1
  else:
   W[4*b+a,4*a+b]+=1
   if a==b:
    W[0,4*a+b]+=1
    for c in (1,2,3):W[4*c+c,4*a+b]-=1
assert np.max(abs(MC-W))<1e-12
print('Manifest/input hashes PASS. Independent spin-half edge derivation and exact integer Cartesian action PASS.')
