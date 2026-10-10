"""Independent checks of certificate builders against direct spin-basis matrices.
This script does not modify the certificate sources or their artifacts.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,math
import numpy as np
import scipy.linalg as la
import sympy as sy
from scipy.sparse.linalg import eigsh
from models import *
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/'low_energy'))
import ground_tail as gt
import dimer_subspace as ds
OUT=BASE/'results'

def check_integer(s,M,W,g,k):
    m=columnar(float(s),M,W,float(g),float(k));H=hamiltonian(m,0)
    strong,weak=gt.model_bonds(M,W,g,k);A,den=gt.integer_sector(s,m.nsites,strong+weak)
    ids,_,_=gt.states_with_sum(int(2*s+1),m.nsites,int(s*m.nsites))
    perm=np.argsort(ids);A=A[perm,:][:,perm]
    diff=H-A.astype(float)/den
    err=float(np.max(abs(diff.data),initial=0.));assert err<1e-13
    e=eigsh(H,k=2,which='SA',tol=2e-13,return_eigenvectors=False);e.sort()
    stem=f's{s}_M{M}_W{W}_g{g}_k{k}'.replace('/','d')
    cert=json.loads((BASE.parent/'low_energy'/(stem+'_ground.json')).read_text())
    assert float(cert['ground_lower_display'])-2e-12<=e[0]<=float(cert['ground_upper_display'])+2e-12
    return dict(kind='direct_integer_matrix',spin=str(s),M=M,W=W,g=str(g),k=str(k),max_entry_difference=err,independent_E0=float(e[0]),certified_E0=cert['ground_upper_display'])

def independent_local_half():
    # Unnormalised singlet and triplet Clebsch-Gordan vectors, rows (a,b).
    return np.array([[0,1,0,0],[-1,0,1,0],[1,0,1,0],[0,0,0,1]],dtype=np.int64)

def independent_local_one():
    P=np.zeros((9,9),dtype=np.int64)
    P[[2,4,6],0]=[1,-1,1]
    P[[1,3],1]=[-1,1];P[[2,6],2]=[-1,1];P[[5,7],3]=[-1,1]
    P[0,4]=1;P[[1,3],5]=1;P[[2,4,6],6]=[1,2,1];P[[5,7],7]=1;P[8,8]=1
    return P

def expand_trial(basis,vec,spin):
    N=basis.shape[1];d=int(2*spin+1);P=independent_local_half() if spin==.5 else independent_local_one();out={}
    for labels,amp in zip(basis,vec):
        if amp==0:continue
        terms={0:int(amp)}
        for r,l in enumerate(labels):
            local=[(a+d*b,int(P[d*a+b,l])) for a in range(d) for b in range(d) if P[d*a+b,l]]
            terms={idx+digits*d**(2*r):value*coeff for idx,value in terms.items() for digits,coeff in local}
        for idx,value in terms.items():out[idx]=out.get(idx,0)+value
    return out

def independent_integer_matrix(model,den):
    # Build independent float entries with exact rational-value checks, then convert.
    H=hamiltonian(model,0);A=H.copy();vals=np.rint(A.data*den)
    assert np.max(abs(A.data*den-vals),initial=0.)<1e-10
    A.data=vals.astype(np.int64)
    return A

def check_sparse_artifact(path):
    rec=json.loads(path.read_text());N=rec['N_dimers']
    s=float(F(rec['s']));assert (s==.5 and N<=8) or (s==1. and N<=4)
    art=np.load(path.parent/rec['trial_artifact']);states=art['basis'];v=art['vector']
    physical=expand_trial(states,v,s)
    weak=rec['weak_bonds'];edges=[Edge(2*i,2*i+1,1.,'rung') for i in range(N)]
    edges += [Edge(2*i+a,2*j+b,float(F(g)),'weak') for i,a,j,b,g in weak]
    model=Model(s,2*N,tuple(edges),'certificate_crosscheck',{})
    den=math.lcm(*[4*F(g).denominator for *_,g in weak],4)
    A=independent_integer_matrix(model,den);ids,_=basis(s,2*N,0)
    vv=[physical.get(int(i),0) for i in ids]
    # Full spin Sz sector, not the truncated dimer support; all residual components.
    Av=[sum(int(A.data[j])*vv[int(A.indices[j])] for j in range(A.indptr[i],A.indptr[i+1])) for i in range(A.shape[0])]
    norm=sum(x*x for x in vv);rho=F(sum(x*y for x,y in zip(vv,Av)),den*norm)
    r2=F(sum(y*y for y in Av),den*den*norm)-rho*rho
    assert rho==F(rec['exact_rayleigh']), 'Rayleigh quotient mismatch'
    assert r2==F(rec['exact_residual_squared']), 'Full residual mismatch'
    e=eigsh(A.astype(float)/den,k=2,which='SA',tol=2e-13,return_eigenvectors=False);e.sort()
    assert float(F(rec['ground_lower']))-1e-12<=e[0]<=float(F(rec['ground_upper']))+1e-12
    return dict(kind='full_spin_basis_exact_residual',artifact=path.name,physical_sites=2*N,full_sector_dimension=len(ids),expanded_nonzero_coefficients=sum(x!=0 for x in vv),rayleigh_exact_match=True,residual_squared_exact_match=True,independent_ground=float(e[0]),certificate_lower=float(F(rec['ground_lower'])),certificate_upper=float(F(rec['ground_upper'])))

def run():
    rows=[]
    for s,M,W,g,k in [(F(1,2),2,2,F(1,50),F(1,50)),(F(1,2),4,2,F(1,50),F(1,50)),(F(1),2,1,F(1,10),F(0))]:
        r=check_integer(s,M,W,g,k);rows.append(r);print(r,flush=True)
    for s in [F(1,2),F(1)]:
      labels,w,kernels=ds.dimer_local(s);P=independent_local_half() if s==F(1,2) else independent_local_one();d=int(2*s+1);dloc=d*d
      z=np.diag(np.arange(d)-float(s));p=np.diag(np.ones(d-1),-1);mi=p.T;I=np.eye(d);Pinv=np.linalg.inv(P)
      assert np.array_equal(np.diag(P.T@P),w)
      err=0.
      for a in [0,1]:
        for b in [0,1]:
          op=lambda x,side:np.kron(x,I) if side==0 else np.kron(I,x)
          factor=.5 if s==F(1,2) else 1.
          K=np.kron(Pinv@op(z,a)@P,Pinv@op(z,b)@P)+factor*(np.kron(Pinv@op(p,a)@P,Pinv@op(mi,b)@P)+np.kron(Pinv@op(mi,a)@P,Pinv@op(p,b)@P))
          B=np.zeros((dloc*dloc,dloc*dloc))
          for j,trans in enumerate(kernels[a,b]):
            for i,k,c in trans:B[dloc*i+k,j]=float(c)
          err=max(err,float(np.max(abs(K-B))))
      assert err<2e-15
      # Recheck exact rational entries; sqrt(2) ladder factors are paired.
      PP=sy.Matrix(P);PI=PP.inv();II=sy.eye(d)
      zz=sy.diag(*[sy.Rational(i)-sy.Rational(s.numerator,s.denominator) for i in range(d)])
      pp=sy.zeros(d)
      for i in range(d-1):pp[i+1,i]=1
      mm=pp.T;ff=sy.Rational(1,2) if s==F(1,2) else sy.Integer(1)
      for a in [0,1]:
        for b in [0,1]:
          op=lambda x,side:sy.kronecker_product(x,II) if side==0 else sy.kronecker_product(II,x)
          K=sy.kronecker_product(PI*op(zz,a)*PP,PI*op(zz,b)*PP)+ff*(sy.kronecker_product(PI*op(pp,a)*PP,PI*op(mm,b)*PP)+sy.kronecker_product(PI*op(mm,a)*PP,PI*op(pp,b)*PP))
          B=sy.zeros(dloc*dloc)
          for j,trans in enumerate(kernels[a,b]):
            for i,k,c in trans:B[dloc*i+k,j]=sy.Rational(c.numerator,c.denominator)
          assert K==B
      rows.append(dict(kind='independent_local_dimer_kernels',spin=str(s),all_four_kernels_match=True,all_four_kernels_exact_rational_match=True,max_float_entry_difference=err))
    for path in sorted((BASE.parent/'low_energy').glob('*_ground.json')):
        r=json.loads(path.read_text())
        if (r.get('s')=='1/2' and r.get('N_dimers',99)<=8) or (r.get('s')=='1' and r.get('N_dimers',99)<=4):
            row=check_sparse_artifact(path);rows.append(row);print(row,flush=True)
    (OUT/'certificate_crosschecks.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':run()
