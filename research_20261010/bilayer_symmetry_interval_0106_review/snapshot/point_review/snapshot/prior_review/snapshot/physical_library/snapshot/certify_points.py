from explore import *
sys.path.insert(0,str(RES/'bilayer_direct_window_continuation'))
from replay_intervals import improve

def exact_initial(d,b):
 a,m=d['denominator_patches'];u0,t0=P.L.upper_exact(a,b);u1,t1=P.L.upper_exact(a,2*b);u2,t2=P.L.upper_exact(m,2*b)
 e={k:F(r['uniform_lower']) for k,r in d['correlated_energy_combinations'].items()}
 j1=C.down(C.exp_interval(b*e['J1'])[0]/u0**8,18);j2=C.down(C.exp_interval(b*e['J2'])[0]/u1**8,18);c0=C.down(C.exp_interval(b*e['C0'])[0]/u2**2,18)
 assert all(0<x<=1 for x in [j1,j2,c0]);aa=C.down(C.G(j1),18);bb=C.down(C.G(j2*aa),18);cc=C.down(C.G(c0**4*aa*aa*bb),18);assert min(aa,bb,cc)>0
 can=C.transport(aa,bb,cc,C.sqrt_down);short,rows=C.short_gap(F(d['coupling_interval'][1]))
 return dict(**d,J1=str(j1),J2=str(j2),C0=str(c0),trace_upper_certificates=[t0,t1,t2],permuted_first_purities=C.st([aa,bb,cc]),canonical_first_purities=C.st(can),beta_initial=str(b),short_sizes=rows,all_integer_L_ge2_gap='0')
if __name__=='__main__':
 out=[];start=time.time()
 points=json.load(open(HERE/'nearby.json'))['results']
 for p in points:
  if p['best_float'] is None:continue
  init=exact_initial(p['data'],F(p['best_float'][1]));new=improve(init);rec={'status':'new_coupling_exact_candidate_pending_independent_physical_and_scalar_review','g':p['g'],'input':init,'certificate':new};out.append(rec);print(p['g'],new['gap_display'],flush=True)
  (HERE/'point_checkpoint.json').write_text(json.dumps(out,indent=2)+'\n');C.exp_interval.cache_clear()
 (HERE/'points_check.json').write_text(json.dumps({'results':out,'seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
