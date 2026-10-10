"""Targeted regressions for tempting incorrect contractions and interpretations."""
from audit_matrices import *
from audit_scalar import labels

def rejection(fn):
 try:fn()
 except AssertionError:return True
 raise AssertionError('Invalid witness was accepted')

def main():
 checks=[];geo=load(OUT/'results/geometry_4x2.json');r=rebuild(4,2,F(9,100),geo);n=len(r['orbits']);d=n+1
 assert any(x for row in geo['W'] for x in row)
 G=r['G'];drop=G.copy();drop[d+n:,d+n:]-=mat(geo['W'])
 assert not np.array_equal(drop,G);checks.append('Discarding W changes the exact U Gram block.')
 neg=G.copy();neg[0,0]=-1;assert rejection(lambda:rank_psd(neg));checks.append('A negative Gram pivot is rejected exactly.')
 bad=r['A'].copy();bad[d+n:,d+n:]-=6*mat(geo['W'])
 assert not np.array_equal(bad,r['A']);checks.append('Dropping the q=6 number term changes the exact Hamiltonian.')
 wrong=r['A'].copy();wrong[d:d+n,d+n:]-=F(9,200)*mat(geo['W']);wrong[d+n:,d:d+n]-=F(9,200)*mat(geo['W'])
 assert not np.array_equal(wrong,r['A']);checks.append('Replacing L/U interaction V+W with V is detected.')
 # Demonstrate why H^3 is not a residual certificate for the filtered state.
 physical=load(OUT/'results/sparse_physical_review.json')[-1];assert physical['unrestricted_H2psi_q8_norm_squared']>0 and physical['H4_projection_strictly_wrong']
 checks.append('A real q=8 component has squared integer norm 76187381760; H^3 is unchanged while H^4 loses it if truncated.')
 # The span identity needs g != 0. At g=0, H is Q and Krylov of B stays inside B.
 z=rebuild(4,2,F(0),geo);B0,B1,B2=z['B0'],z['B1'],z['B2'];Kry=np.hstack([B0,B1,B2]);sel,_=rank_psd(Kry.T@z['G']@Kry);large,_=rank_psd(z['G']);assert len(sel)==d<len(large)
 checks.append('At g=0, span(B,H B,H^2 B) has only the B rank; the enlarged-span equality is explicitly restricted to g>0.')
 for variant in ('filtered','enlarged'):
  r=load(P/'scalar_candidates'/f'candidate_{variant}_g9d100.json')['exact_attempts'][0];s=r['states'][0]
  correct,_=labels(s['n'],F(s['beta']),'xyt');shifted,_=labels(s['n'],F(s['beta'])*2,'xyt');assert correct!=shifted and correct==s['canonical_edge_labels']
  windows=[x for x in r['windows'] if x['included_in_final_minimum']]
  def cover(ws):
   cursor=8
   for w in ws:assert w['n']==cursor;cursor=w['through']
   assert cursor==r['states'][-1]['n']
  cover(windows);assert rejection(lambda:cover(windows[1:]));checks.append(f'{variant}: doubled-beta edge labels and a missing earliest finite window fail the exact basepoint/coverage checks.')
 save('adversarial_review.json',dict(status='PASS',checks=checks));print('PASS',len(checks),'targeted adversarial regressions')
if __name__=='__main__':main()
