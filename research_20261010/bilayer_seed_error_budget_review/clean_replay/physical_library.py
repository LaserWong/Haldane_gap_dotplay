"""New-coupling physical-polynomial and scalar audit; no producer execution."""
from independent_point_math import F,root,down,exp,G,full,valid,advance,advance_canonical,direct,gapcheck,labels
from pathlib import Path
import ast,copy,hashlib,itertools,json,math,os,resource,time,types
HERE=Path(__file__).resolve().parent;S=HERE/'snapshot'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def poly(c,g):return sum(x*g**i for i,x in enumerate(c))
def eqseq(a,b):assert list(a)==list(map(F,b))
def sqrtdecimal(x):
 d=10**60;return F(math.isqrt(x.numerator*d*d//x.denominator),d)
def reference(N,g,k):
 assert 0<=g<F(1,4)
 c=F(3*N,8);return c*(2*g-1)+(c+k)*sqrtdecimal(1-4*g)
def extract(path,names,ns,changes=None):
 src=path.read_text();nodes=[]
 for node in ast.parse(src).body:
  if isinstance(node,ast.FunctionDef) and node.name in names:
   t=ast.get_source_segment(src,node)
   for old,new in (changes or {}).get(node.name,[]):assert old in t;t=t.replace(old,new)
   nodes+=ast.parse(t).body
 assert {x.name for x in nodes}==set(names)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
 return ns

def verify():
 for rel,h in load(HERE/'INPUT_SHA256.json').items():assert sha(S/rel)==h
 for name,p in load(HERE/'PROVENANCE.json').items():
  assert sha(S/name)==p['sha256'];mf=S/'reviews'/p['review']/'MANIFEST_SHA256.json';assert sha(mf)==p['manifest_sha256']
  m=load(mf);m=m.get('files',m);assert m[p['manifest_entry']]==p['sha256']
 assert sha(HERE/'independent_point_math.py')==sha(S/'INDEPENDENT_POINT_MATH.py')
 assert load(S/'ODD_LITERAL_IDENTITY.json')['operator_identity_for_all_real_trial_and_physical_parameters'] is True
 assert load(S/'METADATA_ERRATUM.json')['frozen_point_manifest_sha256']==sha(S/'POINT_MANIFEST_SHA256.json')

# Reuse only explicit functions from the accepted independent odd audit.
ns=dict(F=F,math=math,itertools=itertools,poly=poly,eqseq=eqseq,E=types.SimpleNamespace(reference=reference),ODD_REPORTS=[])
ns['Z']=(F(0),F(0));ns['ONE']=(F(1),F(0));ns['COS']=[(F(1),F(0)),(F(0),F(1,2)),(F(0),F(0)),(F(0),F(-1,2)),(F(-1),F(0)),(F(0),F(-1,2)),(F(0),F(0)),(F(0),F(1,2))]
extract(S/'ACCEPTED_ODD_AUDIT.py',['q','qa','qs','qm','qd','sign','bounds','qpoly','qlist','symbol','decompose','fixed_arrays','check_odd'],ns,{'check_odd':[('z=(lo+hi)/2','z=F(1,10)')]})
raw=load(S/'ODD_STRUCTURAL_POLYNOMIALS.json')['coefficients'];ns['ODD']={tuple(map(int,k.split('x'))):{key:[[[F(c) for c in cell] for cell in row] for row in v] for key,v in val.items()} for k,val in raw.items()}
fixed=load(S/'GROUND_8x4_FIXED.json');m4=load(S/'GROUND_4x4_MATRIX.json');m8=load(S/'NUMERATOR_8x8_MATRIX.json');old=load(S/'ACCEPTED_FIXED_VECTORS.json')
vectors=[x['integer_coefficients'] for x in old['denominator_patches']]+[old['largest_base_trial']['integer_coefficients']]

def contract(c,m):return sum(F(c[i])*F(m[i][j])*c[j] for i in range(len(c)) for j in range(len(c)))
def physical_trial(t,index,lo,hi):
 shape,N,dim=[([4,4],16,11),([8,4],32,43),([8,8],64,43)][index]
 assert (t['geometry'],t['N'],t['trial_dimension'])==(shape,N,dim)
 c=t['integer_coefficients'];assert c==vectors[index] and len(c)==dim and all(type(x)is int for x in c)
 assert F(t['center'])==(lo+hi)/2
 if index==0:
  norm=contract(c,m4['gram']);rho=[contract(c,m)/norm for m in m4['shifted_A_coefficients']];second=[contract(c,m)/norm for m in m4['full_shifted_B_coefficients']]
 elif index==1:
  assert c==fixed['coefficients'];norm=F(fixed['norm']);rho=list(map(F,fixed['mean']));second=list(map(F,fixed['second']))
 else:
  norm=contract(c,m8['gram']);rho=[contract(c,m)/norm for m in m8['affine_A']];second=None
 assert norm>0 and norm==F(t['integer_metric_norm']);eqseq(rho,t['rayleigh_coefficients'])
 if index==2:return rho,None
 eqseq(second,t['full_second_moment_coefficients']);var=[second[0]-rho[0]**2,second[1]-2*rho[0]*rho[1],second[2]-rho[1]**2];eqseq(var,t['full_residual_squared_coefficients'])
 assert var[0]>=0 and var[2]>=0 and 4*var[0]*var[2]>=var[1]**2
 if index==1:assert var==list(map(F,fixed['variance'])) and t['max_trial_triplet_number']==6 and t['max_full_residual_triplet_number']==8
 values=[poly(var,g) for g in (lo,hi)];eqseq(values,t['residual_endpoint_values']);vmax=max(values);assert vmax==F(t['residual_squared_max'])
 ends=[[reference(N,g,q)-poly(rho,g) for g in (lo,hi)] for q in range(1,N+1)]
 assert len(ends)==len(t['reference_minus_rayleigh_endpoint_lowers'])
 for a,b in zip(ends,t['reference_minus_rayleigh_endpoint_lowers']):eqseq(a,b)
 lower=[min(x) for x in ends];eqseq(lower,t['reference_minus_rayleigh_uniform_lowers'])
 assert lower[0]>0 and lower[0]==F(t['ground_identification_margin']);assert lower[1]>0 and lower[1]==F(t['even_Temple_denominator'])
 width=vmax/lower[1];assert width==F(t['uniform_Temple_width'])
 # Frozen point label is explicitly erroneous; require exactly the documented
 # old label, then correct only this in-memory review copy for reconstruction.
 z=F(t['odd_band']['fixed_center']);assert z==(lo if lo==hi else F(1,10))
 tt=copy.deepcopy(t);tt['odd_band']['fixed_center']='1/10'
 odd=ns['check_odd'](tt,rho,lo,hi)
 return rho,dict(N=N,width=width,lower=lower,odd=odd,ground_margin=lower[0],even_margin=lower[1],odd_margin=min(F(x['uniform_Temple_denominator']) for x in t['odd_band']['modes']))

def upper(p,beta,saved):
 N=p['N'];counts=[math.comb(3*N+q-1,q) for q in range(N+1)]
 assert counts[:2]==[1,3*N] and sum(counts)==math.comb(4*N,N)>=4**N
 terms=[exp(beta*p['width'])[1],3*sum(exp(-beta*l)[1] for l in p['odd']),sum(counts[q]*exp(-beta*p['lower'][q-1])[1] for q in range(2,N+1))]
 assert saved['retained_states']==1+3*N and saved['odd_mode_count']==N and saved['spin_multiplicity']==3 and saved['reference_q_range']==[2,N] and F(saved['beta'])==beta
 assert all(F(saved[k])>=v for k,v in zip(('normalized_ground_upper','normalized_odd_band_upper','normalized_tail_upper'),terms))
 assert F(saved['normalized_trace_upper'])==sum(F(saved[k]) for k in ('normalized_ground_upper','normalized_odd_band_upper','normalized_tail_upper'))>=sum(terms)
 return sum(terms)

def shortcheck(rows,g):
 assert [r['L'] for r in rows]==list(range(2,8));answers=[]
 for r,ss in zip(rows,(16,18,32,50,72,98)):
  L=r['L'];assert r['N']==L*L and r['edge_square_sum']==ss
  C=F(3*ss,16);lower=C*(2*g-1)+(C+1)*sqrtdecimal(1-4*g)
  assert F(r['ground_Rayleigh_upper'])==0 and F(r['lambda2_shifted_lower'])==F(r['gap_lower'])==lower>0
  answers.append(lower)
 return min(answers)

def physical(record):
 lo,hi=map(F,record['coupling_interval']);assert F(1,10)<=lo<=hi<F(1,4)
 assert F(record['fixed_vector_center'])==(lo+hi)/2
 rr=[];pp=[]
 for i,t in enumerate(record['denominator_patches']+[record['largest_base_trial']]):
  rho,p=physical_trial(t,i,lo,hi);rr.append(rho);pp.append(p)
 assert record['largest_numerator']==dict(retained_states=1,search_dimension=43,max_triplet_number=6,residual_required=False,physical_spins=128,full_dimension=4**64)
 energies={}
 for name,w in [('J1',[8,0,-2]),('J2',[16,0,-4]),('C0',[0,4,-2])]:
  s=record['correlated_energy_combinations'][name];assert s['weights']==w
  assert sum(a*(-F(3*N,4)) for a,N in zip(w,(16,32,64)))==0
  c=[sum(w[i]*rr[i][j] for i in range(3)) for j in range(2)];ends=[poly(c,g) for g in (lo,hi)];eqseq(c,s['affine_coefficients']);eqseq(ends,s['endpoint_values']);energies[name]=min(ends);assert energies[name]==F(s['uniform_lower'])
 beta=F(record['beta_initial']);assert beta>0 and len(record['trace_upper_certificates'])==3
 us=[upper(p,t,row) for p,t,row in zip((pp[0],pp[0],pp[1]),(beta,2*beta,2*beta),record['trace_upper_certificates'])]
 js=[exp(beta*energies[k])[0]/u**power for k,u,power in zip(('J1','J2','C0'),us,(8,8,2))]
 assert all(0<F(record[k])<=j<=1 for k,j in zip(('J1','J2','C0'),js))
 assert shortcheck(record['short_sizes'],hi)>0
 return dict(interval=list(map(str,(lo,hi))),ground_margins=[str(p['ground_margin']) for p in pp[:2]],even_margins=[str(p['even_margin']) for p in pp[:2]],odd_margins=[str(p['odd_margin']) for p in pp[:2]],odd_fixed_z='1/10',complete_retained_counts=[49,97],independent_initial_ratio_lowers=list(map(str,js)))

scalar_ns={k:globals()[k] for k in ['F','root','down','exp','G','full','valid','advance','advance_canonical','direct','gapcheck','labels']}
extract(S/'ACCEPTED_SCALAR_AUDIT.py',['convert','window1','canonical_window','replay'],scalar_ns,{'replay':[("assert rec['accepted'] is True","assert rec['physical_independently_verified'] is True"),('0<=lo<hi<=F(1,10)','F(1,10)<=lo<=hi<F(1,4)')]})

def domain_check(inp):
 saved=load(S/'domain.json')
 def margins(g):
  out={}
  for p in inp['denominator_patches']:
   N=p['N'];rho=poly(list(map(F,p['rayleigh_coefficients'])),g);c=F(3*N,8)
   ref=lambda q:(reference(N,g,q),reference(N,g,q)+(c+q)*F(1,10**60))
   for q,name in [(1,'ground'),(2,'even')]:out[f'{N}_{name}']=[x-rho for x in ref(q)]
   for mode in p['odd_band']['modes']:
    theta=ns['qpoly'](ns['qlist'](mode['theta_coefficients']),g);a,b=ns['bounds'](theta);u,v=ref(2)
    out[f"{N}_odd_{mode['momentum']}"]=[u-b,v-a]
  c=F(147,8);r=sqrtdecimal(1-4*g);out['short_L7']=[c*(2*g-1)+(c+1)*r,c*(2*g-1)+(c+1)*(r+F(1,10**60))]
  return out
 lo,hi=map(F,saved['legal_closed_domain']);assert lo==F(1,10) and hi<F(1,4)
 for g,key in [(F(11,100),'margin_at_11'),(hi,'all_margins_at_legal_upper_inner')]:
  m=margins(g);assert {k:list(map(str,v)) for k,v in m.items()}==saved[key]
  assert min(v[0] for v in m.values())>0
 assert min(v[0] for v in margins(lo).values())>0
 for key,bracket in saved['roots'].items():
  l,h=map(F,bracket);assert lo<=l<h<F(1,4)
  assert margins(l)[key][0]>0 and margins(h)[key][1]<0
 assert F(saved['roots']['short_L7'][0])==hi
 return dict(status='PASS',legal_closed_domain=saved['legal_closed_domain'],short_L7_zero_bracket=saved['roots']['short_L7'],all_cutoff_brackets=len(saved['roots']),positive_endpoint_margins=True,whole_domain_reason='reference minus affine means is concave; fixed-family variance is convex and PSD; short_L7 is strictly decreasing')

def main():
 start=time.monotonic();verify();points=load(S/'points.json')['results'];results=[]
 for point in points:
  inp=point['input'];assert inp['coupling_interval']==[point['g'],point['g']]
  report=physical(inp);r=copy.deepcopy(inp);r['physical_independently_verified']=True
  cert=copy.deepcopy(point['certificate']);cert['source']='points.json:g='+point['g']
  result=scalar_ns['replay'](cert,r);result['physical']=report;results.append(result)
  print('PASS point',point['g'],result['gap_display'],flush=True)
 domain=domain_check(points[0]['input'])
 bad=[];base=points[-1]['input']
 for label,change in [('wrong_fixed_vector',lambda p:p['denominator_patches'][0]['integer_coefficients'].__setitem__(0,1)),('wrong_odd_gram',lambda p:p['denominator_patches'][0]['odd_band']['modes'][0]['gram_symbol'].__setitem__(0,'1')),('wrong_odd_theta',lambda p:p['denominator_patches'][0]['odd_band']['modes'][0]['theta_coefficients'][0].__setitem__(0,'0')),('missing_odd_mode',lambda p:p['denominator_patches'][1]['odd_band']['modes'].pop()),('wrong_full_variance',lambda p:p['denominator_patches'][1]['full_residual_squared_coefficients'].__setitem__(0,'0')),('optimistic_odd_cutoff',lambda p:p['denominator_patches'][0]['odd_band']['modes'][0].update(uniform_Temple_denominator='10')),('omitted_tail',lambda p:p['trace_upper_certificates'][0].update(normalized_tail_upper='0')),('wrong_short_coupling',lambda p:p['short_sizes'][-1].update(gap_lower='1')),('optimistic_ratio',lambda p:p.update(J1='1'))]:
  r=copy.deepcopy(base);change(r)
  try:physical(r)
  except AssertionError:bad.append(label)
  else:raise AssertionError('corruption accepted '+label)
 out=dict(status='PASS_NEW_COUPLING_POINT_PHYSICAL_AND_SCALAR_CERTIFICATES',results=results,adversarial_rejections=bad,odd_mode_checks=sum(r['modes'] for r in ns['ODD_REPORTS'][:2*len(points)]),legal_domain=domain,point_count=len(points),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS all',len(points),'seconds',out['seconds'],flush=True)
if __name__=='__main__':main()
