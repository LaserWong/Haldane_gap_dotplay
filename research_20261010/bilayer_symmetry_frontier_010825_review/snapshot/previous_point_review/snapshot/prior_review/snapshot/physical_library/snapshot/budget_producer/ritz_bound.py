from budget import *
sys.set_int_max_str_digits(100000)
def pivots_at(g,energy):
 G=P.NUM['G'];AA=P.NUM['first_moment_coefficients'];n=len(G)
 A=[[sum(g**k*F(M[i,j]) for k,M in enumerate(AA))-energy*F(G[i,j]) for j in range(n)] for i in range(n)]
 pivots=[]
 for k in range(n):
  p=A[k][k];assert p>0,('not_positive',k);pivots.append(str(p))
  for i in range(k+1,n):
   for j in range(i,n):A[j][i]=A[i][j]=A[i][j]-A[i][k]*A[k][j]/p
 return pivots
if __name__=='__main__':
 start=time.time();out=[]
 for row in json.load(open(HERE/'targets.json'))['results']:
  g=F(row['g']);upper=F(row['existing43D_reoptimized_rayleigh']);lower=upper-F(1,10**8);pp=pivots_at(g,lower);maximum_gain=F(row['current_numerator_rayleigh'])-lower
  assert maximum_gain<F(row['sufficient_numerator']['epsilon'])
  out.append({'g':str(g),'dimension':43,'ritz_lower':str(lower),'ritz_upper':str(upper),'enclosure_width':'1/100000000','max_improvement_from_saved_rayleigh':str(maximum_gain),'max_improvement_display':float(maximum_gain),'positive_LDL_pivots':pp,'scope':'Entire saved43D numerator subspace only. Failure to meet this sufficient target is not an impossibility proof for all scalar paths.'});print(g,float(maximum_gain),flush=True)
 (HERE/'ritz_bounds.json').write_text(json.dumps({'status':'exact_compressed_space_lower_bound','results':out,'seconds':time.time()-start},indent=2)+'\n')
