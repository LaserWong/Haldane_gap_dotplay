from budget import *
from joint_targets import model32

def xty(d,b):
 p16,p32=d['denominator_patches'];rho32=C.poly(list(map(F,p32['rayleigh_coefficients'])),F(d['coupling_interval'][0]));rho64=C.poly(list(map(F,d['largest_base_trial']['rayleigh_coefficients'])),F(d['coupling_interval'][0]))
 r,_=ratios(d,b);u32=components(p32,b)['total'];r['J2']=math.exp(float(b*(8*rho32-4*rho64)))/u32**8;rr=raw(r)
 if rr is None:return {'status':'initial_cycle_nonpositive','ratios':r}
 can=R.S.transport(*rr,'xty',math.sqrt);states,status=R.S.sequence({'permuted_prefix':rr,'canonical':can},float(b),'xty',False,rounds=12)
 return {'status':status,'ratios':r,'minimum_defect':min(s['u'] for s in states)}
if __name__=='__main__':
 out=[]
 for item in json.load(open(HERE/'reoptimized_saved.json'))['results']:
  out.append({'g':item['g'],'tests':[{'beta':str(b),'xty':xty(item['data'],b)} for b in (F(8),F(47,5),F(11),F(13))]})
 (HERE/'order_comparison.json').write_text(json.dumps({'status':'bounded_float_order_diagnostic_only','results':out},indent=2)+'\n');print(out)
