from targets import *
sys.set_int_max_str_digits(100000)

def largest_width(d,b,N,keys):
 original=next(F(p['uniform_Temple_width']) for p in d['denominator_patches'] if p['N']==N)
 def valid(w):
  r,_=ratios(d,b,{f'width{N}':w},exact=True)
  return all(r[k]>=TARGET[k] for k in keys)
 assert valid(F(0)) and not valid(original)
 lo=F(0);hi=original
 for _ in range(24):
  mid=(lo+hi)/2
  if valid(mid):lo=mid
  else:hi=mid
 # A simple sufficient one-millionth energy-width ceiling.
 simple=F(lo.numerator*10**6//lo.denominator,10**6);assert valid(simple)
 return simple,{'width_cap':str(simple),'width_cap_display':float(simple),'max_sufficient_width_bracket':[str(lo),str(hi)],'current_width':str(original),'ground_lower_improvement':str(original-simple),'keys':keys}

def model32():
 path=RES/'low_band/third_moment_exact/enlarged_8x4_g9d100.json';r=json.load(open(path));gg=json.load(open(RES/'low_band/third_moment_exact/geometry_8x4_origin.json'));n=gg['pair_orbits'];d=n+1;np=P.np
 G=np.array(r['gram'],dtype=object);K0=np.zeros_like(G);K0[:d,:d]=G[:d,:d]@np.diag([0]+[2]*n)
 ff,ss,vv,ww=[np.array(gg[k],dtype=object) for k in ('F','S','V','W')]
 K0[d:d+n,d:d+n]=4*ff;K0[d:d+n,d+n:]=4*ss;K0[d+n:,d:d+n]=4*ss.T;K0[d+n:,d+n:]=4*vv+6*ww
 K=np.array([[F(x,r['integer_matrix_denominator']) for x in row] for row in r['shifted_H_numerator']],dtype=object);K1=(K-K0)/F(r['coupling']);assert np.array_equal(K0,K0.T) and np.array_equal(K1,K1.T)
 return {'geometry':[8,4],'N':32,'trial_dimension':len(G),'G':G,'first_moment_coefficients':[K0,K1]}

def temple_obstruction11(g,L):
 model=C.MODELS[0];a=C.reference(g,16,2);AA=model['first_moment_coefficients'];BB=model['full_second_moment_coefficients'];G=model['G'];n=len(G)
 A=[[sum(g**k*F(M[i,j]) for k,M in enumerate(BB))-(a+L)*sum(g**k*F(M[i,j]) for k,M in enumerate(AA))+a*L*F(G[i,j]) for j in range(n)] for i in range(n)];piv=[]
 for k in range(n):
  p=A[k][k]
  if p<=0:return {'positive_definite':False,'first_nonpositive_pivot':k}
  piv.append(str(p))
  for i in range(k+1,n):
   for j in range(i,n):A[j][i]=A[i][j]=A[i][j]-A[i][k]*A[k][j]/p
 return {'positive_definite':True,'positive_LDL_pivots':piv,'reference_cutoff':str(a),'unattainable_Temple_lower':str(L),'dimension':n,'scope':'Fixed even cutoff and entire saved11D trial space only; this target is sufficient for the reference-startup comparison, not necessary for every bootstrap.'}

if __name__=='__main__':
 start=time.time();out=[];b=F(47,5);M32=model32()
 for item in json.load(open(HERE/'reoptimized_saved.json'))['results']:
  g=F(item['g']);d=item['data'];w16,r16=largest_width(d,b,16,['J1','J2']);w32,r32=largest_width(d,b,32,['C0'])
  r,cc=ratios(d,b,{'width16':w16,'width32':w32},exact=True);assert all(r[k]>=TARGET[k] for k in TARGET)
  cond=exact_conditional_path(d,b,r);p16,p32=d['denominator_patches'];rho16=C.poly(list(map(F,p16['rayleigh_coefficients'])),g);rho32=C.poly(list(map(F,p32['rayleigh_coefficients'])),g)
  target16=rho16-w16;target32=rho32-w32
  v32=C.optimized_vector(M32,g);trial32=C.trial(M32,g,v32);newrho32=C.poly(list(map(F,trial32['rayleigh_coefficients'])),g);cut32=C.reference(g,32,2);budget32=(newrho32-target32)*(cut32-newrho32)
  row={'g':str(g),'beta':str(b),'width16':r16,'width32':r32,'target_ground16_lower':str(target16),'target_ground32_lower':str(target32),'target_current16_variance':str(w16*F(p16['even_Temple_denominator'])),'current16_variance':p16['residual_squared_max'],'current32_variance':p32['residual_squared_max'],'optimized43D_8x4_trial':trial32,'optimized43D_8x4_rayleigh':str(newrho32),'residual_squared_budget_for_optimized43D_8x4':str(budget32),'residual_budget_display':float(budget32),'budget_positive':budget32>0,'11D_Temple_target_obstruction':temple_obstruction11(g,target16),'hypothetical_only_conditional_path':cond}
  out.append(row);print(g,'w16',float(w16),'w32',float(w32),'v32budget',float(budget32),'11D obstruct',row['11D_Temple_target_obstruction']['positive_definite'],'gap',cond['gap_display'],flush=True)
  (HERE/'joint_targets_checkpoint.json').write_text(json.dumps(out,indent=2)+'\n');exp.cache_clear()
 (HERE/'joint_targets.json').write_text(json.dumps({'status':'exact_joint_conditional_targets_not_physical_gap_certificates','results':out,'seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
