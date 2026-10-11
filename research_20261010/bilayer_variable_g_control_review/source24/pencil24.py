"""Exact consumer for version24 sector checkpoints; no diagonalization/bound claim."""
from fractions import Fraction as F
SCHEMA='bilayer-moment24-v1'

def pencil(sectors,g_num,g_den,origin_reduced=False):
 assert g_den>0 and set(map(int,sectors))=={0,2,4,6}
 ss={int(q):list(map(F,v)) for q,v in sectors.items()};assert all(len(v)==24 for v in ss.values())
 if origin_reduced:
  for q,w in [(4,F(8)),(6,F(16,3))]:ss[q]=[w*x for x in ss[q]]
 full=[sum(ss[q][i] for q in ss) for i in range(24)];m0,m1,m2lo,m3lo,m4lo,n8,cross,uz,wz=full[15:]
 m2=m2lo+121*n8;m3=m3lo+193600*n8+1331*sum(full[:4])+cross;m4=m4lo+sum(full[4:10])+14641*sum(full[10:15])
 weighted=lambda i,k:sum(q**k*ss[q][i] for q in ss)
 pu=weighted(15,1);uu=weighted(15,2);uc=weighted(16,1);uw=weighted(16,2);cw=weighted(17,1)+968*n8;ww=weighted(17,2)+7744*n8
 a=22*g_den-200*g_num;b=g_num
 G=[m0,m1,m2];K=[a*pu+b*m1,a*uc+b*m2,a*cw+b*m3];J=[a*a*uu+2*a*b*uc+b*b*m2,a*a*uw+a*b*(uz+cw)+b*b*m3,a*a*ww+2*a*b*wz+b*b*m4]
 assert all(x.denominator==1 for x in G+K+J),'nonintegral_complete_sector_sum'
 return {'schema':SCHEMA,'fixed_T0_Q':200,'fixed_T0_A':11,'g_num':g_num,'g_den':g_den,'G_denominator':1,'G_numerators':list(map(str,map(int,G))),'K_denominator':22*g_den,'K_numerators':list(map(str,map(int,K))),'J_denominator':(22*g_den)**2,'J_numerators':list(map(str,map(int,J)))}

def validate_export(v):
 assert v['schema']==SCHEMA and (v['fixed_T0_Q'],v['fixed_T0_A'])==(200,11)
 assert v['G_denominator']==1 and v['K_denominator']==22*v['g_den'] and v['J_denominator']==(22*v['g_den'])**2
 assert all(len(v[k])==3 for k in ['G_numerators','K_numerators','J_numerators'])
 return {k:[F(int(x),v[k+'_denominator']) for x in v[k+'_numerators']] for k in ['G','K','J']}
