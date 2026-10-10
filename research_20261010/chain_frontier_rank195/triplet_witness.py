"""Three exact orthogonal spin-one trial vectors give a small-trace lower bound."""
exec(open(__file__.replace('triplet_witness.py','common.py')).read())
import numpy as np
from scipy.linalg import eigh
C=p.C
m=json.loads((HERE/'expanded_moments.json').read_text());states=list(map(tuple,m['basis']));n=len(states);index=dict(zip(states,range(n)));weights=list(map(F,m['Gram_diagonal']));K=[list(map(F,row)) for row in m['unit_K']];mags=[sum(C.MAG[x] for x in s) for s in states]
ids=[i for i,z in enumerate(mags) if z==1];targets=[i for i,z in enumerate(mags) if z==2];tindex=dict(zip(targets,range(len(targets))))
def action(vec,op):
 out=[F(0)]*n
 for j,x in enumerate(vec):
  if not x:continue
  s=states[j]
  for site in range(4):
   for dest in range(9):
    c=C.OPS[0,op][dest][s[site]]+C.OPS[1,op][dest][s[site]]
    if c:
     ss=list(s);ss[site]=dest;ss=tuple(ss);assert ss in index;out[index[ss]]+=x*c
 return out
raising=[]
for j in ids:
 vv=[F(0)]*n;vv[j]=F(1);av=action(vv,'+');assert all(x==0 for i,x in enumerate(av) if i not in targets);raising.append([av[i] for i in targets])
mat=[list(x) for x in zip(*raising)];rr=[x[:] for x in mat];piv=[];row=0
for col in range(len(ids)):
 found=next((i for i in range(row,len(rr)) if rr[i][col]),None)
 if found is None:continue
 rr[row],rr[found]=rr[found],rr[row];v=rr[row][col];rr[row]=[x/v for x in rr[row]]
 for i in range(len(rr)):
  if i!=row and rr[i][col]:
   v=rr[i][col];rr[i]=[x-v*y for x,y in zip(rr[i],rr[row])]
 piv.append(col);row+=1
 if row==len(rr):break
free=[j for j in range(len(ids)) if j not in piv];basis=[]
for j in free:
 v=[F(0)]*len(ids);v[j]=F(1)
 for i,col in enumerate(piv):v[col]=-rr[i][j]
 assert all(sum(x*y for x,y in zip(r,v))==0 for r in mat);basis.append(v)
dim=len(basis);g=F(1,4);Em=[sum(C.EX[x] for x in states[i]) for i in ids]
smallH=[[(F(Em[ii])*weights[i] if i==j else F(0))+g*K[i][j] for jj,j in enumerate(ids)] for ii,i in enumerate(ids)]
GG=[[sum(weights[i]*u[k]*v[k] for k,i in enumerate(ids)) for v in basis] for u in basis]
HH=[[sum(u[i]*smallH[i][j]*v[j] for i in range(len(ids)) for j in range(len(ids))) for v in basis] for u in basis]
eigs,vecs=eigh(np.array(HH,dtype=float),np.array(GG,dtype=float));coeff=[int(round(x*10**12)) for x in vecs[:,0]]
high=[F(0)]*n
for i,idx in enumerate(ids):high[idx]=sum(F(c)*v[i] for c,v in zip(coeff,basis))
assert all(x==0 for x in action(high,'+'));mid=action(high,'-');low=action(mid,'-');assert all(x==0 for x in action(low,'-'))
assert action(mid,'+')==high and action(low,'+')==mid
vectors=[high,mid,low];norms=[];energies=[]
for vec in vectors:
 norm=sum(w*x*x for w,x in zip(weights,vec));assert norm>0
 energy=(sum(weights[i]*vec[i]*vec[i]*sum(C.EX[x] for x in states[i]) for i in range(n))+g*sum(vec[i]*K[i][j]*vec[j] for i in range(n) for j in range(n)))/norm
 norms.append(norm);energies.append(energy)
assert len(set(norms))==len(set(energies))==1
rec=json.loads((HERE/'expanded_inputs.json').read_text())[0];rho=F(rec['small']['exact_rayleigh']);exc=energies[0]-8-rho
out=dict(status='EXACT_SPIN_ONE_TRIPLET_RAYLEIGH_WITNESS',g=str(g),reference_dimension=n,highest_weight_magnetization_dimension=len(ids),highest_weight_nullspace_dimension=dim,raising_matrix=[[str(x) for x in r] for r in mat],highest_weight_ids=ids,target_magnetization_two_ids=targets,nullspace_basis=[[str(x) for x in v] for v in basis],combination_integers=list(map(str,coeff)),vectors=[[str(x) for x in v] for v in vectors],metric_norm=str(norms[0]),shifted_rayleigh=str(energies[0]),unshifted_rayleigh=str(energies[0]-8),excitation_relative_to_ground_rayleigh=str(exc),excitation_display=float(exc),contract='Exact highest weight M=1, killed by raising; lowering gives M=0,-1 with equal norms and equal energy. These spin-one vectors are orthogonal to the unique singlet ground. Peierls/Jensen gives exp(beta*rho4) Z4(beta)>=1+3 exp(-beta*d_upper).')
(HERE/'triplet_witness.json').write_text(json.dumps(out,indent=2));print('TRIPLET',float(exc),'subspace',dim,flush=True)
