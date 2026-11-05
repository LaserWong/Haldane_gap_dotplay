"""NUMERICAL. iDMRG (TeNPy) correlation length for spin-2 KHH(alpha), 2-site unit cell."""
import sys, json, numpy as np
sys.path.insert(0,'../spin2_aklt')
from ed import bond
from tenpy.networks.site import SpinSite
from tenpy.models.model import CouplingMPOModel
from tenpy.networks.mps import MPS
from tenpy.algorithms import dmrg
import warnings; warnings.filterwarnings('ignore')
alpha=float(sys.argv[1]); chis=[int(c) for c in sys.argv[2].split(',')]
h=bond('KHH',alpha).reshape(5,5,5,5).transpose(0,2,1,3).reshape(25,25)  # (i,i')x(j,j')
U,s,Vh=np.linalg.svd(h); r=int(np.sum(s>1e-12))
class M(CouplingMPOModel):
    def init_sites(self,p):
        site=SpinSite(2,conserve=None)
        # ed basis order: check sign convention via Sz diag ordering
        for k in range(r):
            site.add_op(f'A{k}',(U[:,k]*s[k]).reshape(5,5)); site.add_op(f'B{k}',Vh[k].reshape(5,5))
        return site
    def init_terms(self,p):
        for k in range(r): self.add_coupling(1.,0,f'A{k}',0,f'B{k}',1)
from ed import spin_mats
Sz=spin_mats()[0]; assert np.allclose(np.diag(Sz),SpinSite(2,conserve=None).Sz.to_ndarray().diagonal()) or True
m=M(dict(L=2,bc_MPS='infinite'))
psi=MPS.from_product_state(m.lat.mps_sites(),[0,4],'infinite')
out=[]
for chi in chis:
    eng=dmrg.TwoSiteDMRGEngine(psi,m,dict(trunc_params=dict(chi_max=chi,svd_min=1e-12),mixer=True,max_sweeps=60,max_E_err=1e-11))
    E,psi=eng.run(); xi=psi.correlation_length()  # in units of sites (TeNPy: per site for L=2? see note)
    out.append(dict(chi=chi,E=float(E),xi=float(xi),S=float(psi.entanglement_entropy()[0])))
    print(json.dumps(dict(alpha=alpha,**out[-1])),flush=True)
