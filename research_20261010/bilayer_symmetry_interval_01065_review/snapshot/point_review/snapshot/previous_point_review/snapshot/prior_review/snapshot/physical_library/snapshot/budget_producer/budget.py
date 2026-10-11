import os,sys,json,math,time,resource
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;RES=HERE.parent
sys.path.insert(0,str(RES/'bilayer_frontier_above_010'))
import explore as E
C=E.C;P=E.P
sys.path.insert(0,str(RES/'bilayer_direct_window_continuation'))
from replay_intervals import R,improve
exp=C.exp_interval
source=json.load(open(RES/'bilayer_frontier_above_010/exploration.json'))
DATA={F(x['g']):x['data'] for x in source['results']}
target=json.load(open(RES/'bilayer_frontier_above_010/points.json'))['results'][-1]['input']
TARGET={k:F(target[k]) for k in ('J1','J2','C0')}

def components(p,b,scenario='current',exact=False):
 N=p['N'];w=F(p['uniform_Temple_width'])
 if scenario in ('ground_all_zero',f'ground{N}_zero'):w=F(0)
 if isinstance(scenario,dict) and f'width{N}' in scenario:w=F(scenario[f'width{N}'])
 elow=(lambda x:exp(x)[1]) if exact else (lambda x:math.exp(float(x)))
 ground=elow(b*w)
 modes=p['odd_band']['modes']
 key='theta_minus_ground_rayleigh_endpoint_lowers' if scenario in ('odd_all_ritz',f'odd{N}_ritz') else 'eigen_lower_minus_ground_rayleigh_uniform_lower'
 odds=[]
 for m in modes:
  val=min(map(F,m[key])) if isinstance(m[key],list) else F(m[key]);odds.append(3*elow(-b*val))
 odd=sum(odds)
 tail=sum(math.comb(3*N+q-1,q)*elow(-b*F(en)) for q,en in enumerate(p['reference_minus_rayleigh_uniform_lowers'],1) if q>=2)
 if scenario in ('odd_all_remove',f'odd{N}_remove'):odd=F(0)
 if scenario in ('tail_all_remove',f'tail{N}_remove'):tail=F(0)
 return dict(ground=ground,odd=odd,tail=tail,total=ground+odd+tail)

def ratios(d,b,scenario='current',epsilon=F(0),exact=False):
 a,m=d['denominator_patches'];cc=[components(a,b,scenario,exact),components(a,2*b,scenario,exact),components(m,2*b,scenario,exact)]
 e={k:F(r['uniform_lower']) for k,r in d['correlated_energy_combinations'].items()};e['J1']+=2*epsilon;e['J2']+=4*epsilon;e['C0']+=2*epsilon
 ex=(lambda x:exp(x)[0]) if exact else (lambda x:math.exp(float(x)))
 out={k:ex(b*e[k])/cc[i]['total']**power for k,i,power in [('J1',0,8),('J2',1,8),('C0',2,2)]}
 return out,cc

def raw(r):
 a=C.G(r['J1'])
 if a<=0:return None
 b=C.G(r['J2']*a)
 if b<=0:return None
 c=C.G(r['C0']**4*a*a*b)
 if c<=0:return None
 return [a,b,c]

def float_path(r,beta):
 if any(x>1 for x in r.values()):return {'status':'hypothetical_ratios_exceed_physical_upper_one'}
 rr=raw(r)
 if rr is None:return {'status':'initial_cycle_nonpositive'}
 can=C.transport(*rr,math.sqrt)
 states,status=R.S.sequence({'permuted_prefix':rr,'canonical':can},float(beta),'txy',False,rounds=12)
 return {'status':status,'min_canonical_defect':min(s['u'] for s in states),'raw':rr,'cycles':len(states)}

if __name__=='__main__':
 start=time.time();out=[]
 scenarios=['current','ground16_zero','ground32_zero','ground_all_zero','odd16_ritz','odd32_ritz','odd_all_ritz','odd16_remove','odd32_remove','odd_all_remove','tail16_remove','tail32_remove','tail_all_remove']
 for g in (F(21,200),F(11,100)):
  d=DATA[g]
  for b in (F(8),F(47,5),F(11),F(13)):
   rows=[]
   for sc in scenarios:
    r,cc=ratios(d,b,sc);row={'scenario':sc,'ratios':r,'trace_components':cc,**float_path(r,b)};rows.append(row)
   print(g,b,[(x['scenario'],x['status']) for x in rows],flush=True)
   out.append({'g':str(g),'beta':str(b),'scenarios':rows})
 (HERE/'screen.json').write_text(json.dumps({'status':'hypothetical_float_sensitivity_not_certificates','results':out,'seconds':time.time()-start},indent=2,default=str)+'\n')
