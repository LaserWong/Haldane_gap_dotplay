"""Independent 66-interval scalar continuation; no producer code is imported."""
from independent_point_math import F,root,down,exp,G,full,valid,advance,advance_canonical,direct,gapcheck,labels
import json,time,hashlib,copy,resource,os
from pathlib import Path
HERE=Path(__file__).resolve().parent;S=HERE/'snapshot'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def convert(v):
 a,b,c=v
 return [a*root(b),a*a*b*root(c),full(v)]
def window1(s,t,k=F(0)):
 assert 0<s<=1 and 0<t<=1 and 0<=k<=1
 p=max(s*s*t,k);assert p>F(1,2)
 w=(1+root(2*p-1))/2;r=(1-w)/w;d=t/(1+r*r)
 return down((1-r)*min(s*root(d),d))
def canonical_window(v,k):
 a,b,c=v;assert b>F(1,2)
 r=root(2*b-1);sx=max(a*a*r,root(k)*r/b);ty=window1(b,c,k)
 return window1(sx,ty)
def replay(row,rec):
 assert rec['accepted'] is True
 assert row['coupling_interval']==rec['coupling_interval']
 lo,hi=map(F,row['coupling_interval']);assert 0<=lo<hi<=F(1,10)
 beta=F(rec['beta_initial']);raw=list(map(F,rec['permuted_first_purities']));can=list(map(F,rec['canonical_first_purities']));valid(raw);valid(can)
 limits=[G(F(rec['J1'])),G(F(rec['J2'])*raw[0]),G(F(rec['C0'])**4*raw[0]**2*raw[1])]
 assert all(x<=y for x,y in zip(raw,limits))
 joint=max(full(raw),full(can),F(rec.get('initial_joint_product','0')))
 shorts=rec['short_sizes'];assert [s['L'] for s in shorts]==list(range(2,8))
 assert [s['N'] for s in shorts]==[L*L for L in range(2,8)]
 assert [s['edge_square_sum'] for s in shorts]==[16,18,32,50,72,98]
 short=min(F(s['gap_lower']) for s in shorts);assert short==F(row['short_gap'])>0
 assert F(row['previous_gap'])==F(rec['all_integer_L_ge2_gap'])
 assert len(row['states'])==row['terminal_cycle']+1 and len(row['windows'])==row['terminal_cycle']
 final=F(row['gap']);assert 0<final<=short and final>=F(row['previous_gap'])
 gaps=[];methods={'direct_txy':0,'inherited_canonical':0}
 for i,state in enumerate(row['states']):
  n=8*2**i;tau=2*beta*2**i
  assert state['n']==n and F(state['beta'])==tau and state['physical_base']==[n,n,str(tau)]
  assert state['raw_edge_labels']==labels(n,tau,'txy') and state['canonical_edge_labels']==labels(n,tau,'xyt')
  can=list(map(max,can,convert(raw)));joint=max(joint,full(can),full(raw));u=max(1-x for x in can)
  assert all(0<F(x)<=y for x,y in zip(state['raw'],raw))
  assert all(0<F(x)<=y for x,y in zip(state['canonical'],can))
  assert 0<F(state['joint'])<=joint and u<=F(state['defect'])
  if i==row['terminal_cycle']:
   assert row['terminal_n']==n and F(row['terminal_beta'])==tau
   su=F(state['defect']);assert 0<u<=su<=F(1,500)
   g=F(row['asymptotic_gap']);assert exp(tau*g)[1]*32*su<1;gaps.append(g)
  else:
   w=row['windows'][i];assert w['n']==n and w['through']==2*n and F(w['beta'])==tau
   saved_raw=list(map(F,state['raw']));saved_can=list(map(F,state['canonical']));saved_joint=F(state['joint'])
   try:dp,d,s=direct(*saved_raw,n,n)
   except AssertionError:dp=F(0)
   cp=canonical_window(saved_can,saved_joint)
   assert 0<=F(w['direct_purity'])<=dp and 0<F(w['canonical_purity'])<=cp
   pp=max(F(w['direct_purity']),F(w['canonical_purity']));assert F(w['purity'])==pp
   assert w['method']==('direct_txy' if F(w['direct_purity'])>=F(w['canonical_purity']) else 'inherited_canonical')
   if dp:
    assert F(w['details']['transverse_spatial_lower'])<=d and F(w['details']['interpolated_spatial_lower'])<=s
   gapcheck(pp,tau,F(w['gap']));gaps.append(F(w['gap']));methods[w['method']]+=1
   can=advance_canonical(can,joint);raw=advance(raw);joint=full(can)
 assert final==min([short]+gaps)
 return dict(source=row['source'],coupling_interval=row['coupling_interval'],gap=str(final),gap_display=float(final),terminal_n=row['terminal_n'],terminal_beta=row['terminal_beta'],finite_windows=len(row['windows']),methods=methods)
def main():
 start=time.monotonic()
 ub=F(1,500)
 assert 49/(2*(1-7*ub)**2)<32 and 32*ub<1 and 20/(1-20*ub)<32 and 5*ub<=F(1,100)
 for rel,h in load(HERE/'INPUT_SHA256.json').items():assert sha(S/rel)==h
 prov=load(HERE/'PROVENANCE.json')
 for source,p in prov.items():
  assert sha(S/source)==p['source_sha256']
  review=S/p['accepted_review'];assert sha(review/'MANIFEST_SHA256.json')==p['accepted_manifest_sha256']
  manifest=load(review/'MANIFEST_SHA256.json');manifest=manifest.get('files',manifest)
  assert manifest[p['matched_record']]==p['source_sha256']
  # Pass statuses differ across historical reviews; each status contains PASS.
  assert 'PASS' in load(review/'REVIEW_STATUS.json')['status']
 lemma=load(S/'DIRECT_LEMMA_MANIFEST.json');assert sha(HERE/'independent_point_math.py')==lemma['audit.py']
 assert load(S/'DIRECT_LEMMA_ACCEPTANCE.json')['status']=='PASS'
 saved=load(S/'interval_results.json');assert saved['count']==66==len(saved['results'])==len(prov)
 ans=[];cursor=F(0)
 for row in saved['results']:
  assert saved['source_sha256'][row['source']]==prov[row['source']]['source_sha256']
  assert F(row['coupling_interval'][0])==cursor
  ans.append(replay(row,load(S/row['source'])));cursor=F(row['coupling_interval'][1])
 assert cursor==F(1,10)
 uniform=min(F(r['gap']) for r in ans);assert uniform==F(saved['uniform_gap'])
 assert sum(r['finite_windows'] for r in ans)==517
 bad=[];original=saved['results'][0];rec=load(S/original['source'])
 mutations=[('wrong_interval',lambda p:p['coupling_interval'].__setitem__(0,'1/1000')),('wrong_beta',lambda p:p['states'][1].update(beta='1')),('wrong_common_base',lambda p:p['states'][1].update(n=24)),('wrong_label',lambda p:p['states'][0]['raw_edge_labels'][1]['base'].__setitem__(2,'1')),('missing_window',lambda p:p['windows'].pop(1)),('inflated_direct_endpoint',lambda p:p['windows'][0].update(direct_purity='1')),('inflated_canonical_endpoint',lambda p:p['windows'][0].update(canonical_purity='1')),('wrong_terminal',lambda p:p.update(terminal_n=128)),('oversized_gap',lambda p:p.update(gap='1')),('changed_short_bound',lambda p:p.update(short_gap='1'))]
 for label,change in mutations:
  row=copy.deepcopy(original);change(row)
  try:replay(row,rec)
  except AssertionError:bad.append(label)
  else:raise AssertionError('corruption accepted '+label)
 out=dict(status='PASS_ALL_66_CLOSED_INTERVAL_PATHS',interval=['0','1/10'],uniform_gap=str(uniform),uniform_gap_display=float(uniform),limiting=[r for r in ans if F(r['gap'])==uniform],results=ans,finite_windows=sum(r['finite_windows'] for r in ans),closed_interval_cover=True,adversarial_rejections=bad,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_affinity=sorted(os.sched_getaffinity(0)))
 (HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
if __name__=='__main__':main()
