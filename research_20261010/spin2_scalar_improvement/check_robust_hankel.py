"""Exact algebra about decimal candidate centers, NOT a physical moment certificate."""
import resource,json,math
from fractions import Fraction as F
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
P=Path(__file__).resolve().parent
rs=json.loads((P.parent/'spin2_heat/seed_feasibility/exploratory_moment_inputs.json').read_text())
def det(A):
 A=[r.copy()for r in A];d=F(1)
 for i in range(len(A)):
  assert A[i][i]!=0
  p=A[i][i];d*=p
  for j in range(i+1,len(A)):
   r=A[j][i]/p
   for k in range(i+1,len(A)):A[j][k]-=r*A[i][k]
 return d
out=[];epsilon=F(1,10000)
for row in rs:
 for s in ['J','N']:
  x=F(103,100)if s=='J' else F(-51 if row['beta']==6 else 51,50)
  m={int(k):F(str(v))-x**int(k)for k,v in row['moments'][s].items()}
  A=[[m[4+i+j]-(4*epsilon if i==j else 0)for j in range(4)]for i in range(4)]
  minors=[det([r[:n]for r in A[:n]])for n in range(1,5)]
  assert min(minors)>0
  R=F(math.ceil(row['caps'][s]['cap']*10**6)+1,10**6)
  e=3*epsilon*(R*R+1)
  B=[[R*R*m[4+i+j]-m[6+i+j]-(e if i==j else 0)for j in range(3)]for i in range(3)]
  bm=[det([r[:n]for r in B[:n]])for n in range(1,4)]
  assert min(bm)>0
  out.append({'beta':row['beta'],'sector':s,'atom_old_shift':str(x),'coordinatewise_moment_error_radius':str(epsilon),'hankel_minors':[str(v)for v in minors],'localizer_R_exploratory':str(R),'localizer_minors':[str(v)for v in bm],'atom_modulus_at_a4p76121_display':float(abs(x))*math.exp(-row['beta']*.00041)})
result={'status':'EXACT_DECIMAL_CENTER_ROBUST_PSD_FEASIBILITY_NOT_A_MODEL_CERTIFICATE','rows':out,'statement':'For every error vector |delta m4|,...,|delta m10| <= 1/10000, the atom-removed 4x4 Hankel remains positive definite. The displayed symmetric-support localizer remains positive definite too; its proposed support cap is exploratory.'}
(P/'robust_hankel.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(out),'robust Hankel and localizer checks')
