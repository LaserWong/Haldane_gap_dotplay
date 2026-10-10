"""Fixed-vector exact certificates for a continuum of FF perturbations.

Everything is new output in this directory. Immutable q<=2 vectors are read from
nonperturbative_audit/epsilon_scan. Float scans only select interval/beta proposals.
Each saved success gets exact endpoint PSD, full residual polynomial, outward
heat bounds, scalar replay and all-integer finite-window interpolation.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import sys,json,math,time,hashlib,resource,argparse
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
from functools import lru_cache
import numpy as np
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
AUDIT=ROOT/'research_20261010/nonperturbative_audit'
for p in [ROOT/'low_energy',AUDIT,ROOT/'seed_size/code',ROOT/'research_20261010/root_review']:sys.path.insert(0,str(p))
from audit_ff import K,W,occupancy,multigraph,local_psd,exp192,floor_bits
import fully_frustrated as producer
from certified_core import exp_bounds,down,up,G
from correlated_seeds import replay3
from finite_window_2d import interpolate_2d,gap as finite_gap

SHAPES=[(2,2),(4,2),(4,4)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def polynomial(co,e):return sum(F(c)*e**k for k,c in enumerate(co))

@lru_cache(None)
def coefficients(eps_text,nx,ny):
    eps=F(eps_text);tag=f'ff_{nx}x{ny}_eps{eps}_q2'.replace('/','d')
    source=AUDIT/'epsilon_scan'/(tag+'_ground.json');r=json.loads(source.read_text());p=source.parent/r['trial_artifact']
    z=np.load(p,allow_pickle=False);basis=[tuple(map(int,x)) for x in z['basis']];vec=list(map(int,z['vector']));N=nx*ny;E00=-F(3*N,4)
    assert len(set(basis))==len(basis)==r['trial_subspace_dimension']
    assert all(len(st)==N and set(st)<={0,1,2,3} for st in basis)
    # Keep Hff and V in a common integer scaling, and never project outputs.
    scale=40;pair={}
    for si in range(4):
      for sj in range(4):
        hh=defaultdict(F);vv=defaultdict(F)
        for aa in range(2):
          for bb in range(2):
            for ti,tj,x in K[aa,bb][si,sj]:
              hh[ti,tj]+=F(3,10)*x
              if aa==bb:vv[ti,tj]+=x
        row=[]
        for st in hh.keys()|vv.keys():
          a=scale*hh[st];b=scale*vv[st];assert a.denominator==b.denominator==1
          if a or b:row.append((st[0],st[1],int(a),int(b)))
        pair[si,sj]=row
    h=defaultdict(int);v=defaultdict(int);reached=set(basis);edges=multigraph(nx,ny)
    for st,x in zip(basis,vec):
      h[st]+=int(scale*(E00+sum(s!=0 for s in st)))*x
      for (i,j),w in edges.items():
        for ti,tj,a,b in pair[st[i],st[j]]:
          out=list(st);out[i]=ti;out[j]=tj;out=tuple(out);reached.add(out)
          h[out]+=w*a*x;v[out]+=w*b*x
    metric=lambda st:math.prod(W[s] for s in st)
    norm=sum(metric(st)*x*x for st,x in zip(basis,vec));assert norm>0
    rho=[F(sum(metric(st)*x*y[st] for st,x in zip(basis,vec)),scale*norm) for y in [h,v]]
    moment=[F(sum(metric(st)*h[st]**2 for st in reached),scale**2*norm),F(2*sum(metric(st)*h[st]*v[st] for st in reached),scale**2*norm),F(sum(metric(st)*v[st]**2 for st in reached),scale**2*norm)]
    r2=[moment[0]-rho[0]**2,moment[1]-2*rho[0]*rho[1],moment[2]-rho[1]**2]
    assert r2[2]>=0
    assert polynomial(rho,eps)==F(r['exact_rayleigh'])
    assert polynomial(r2,eps)==F(r['exact_residual_squared'])
    hist=occupancy(nx,ny,F(3,10));assert hist==Counter({(row['q'],F(row['energy_lower'])):row['multiplicity'] for row in r['reference_certificate']['bins']})
    rec={'geometry':[nx,ny],'vector_epsilon':str(eps),'source_record':str(source.relative_to(ROOT)),'source_record_sha256':sha(source),'trial_artifact':str(p.relative_to(ROOT)),'trial_artifact_sha256':sha(p),'full_dimension':4**N,'physical_spins':2*N,'linear_trial_dimension':len(basis),'retained_vectors':1,'full_action_union_dimension':len(reached),'integer_action_scale':scale,'integer_metric_norm':str(norm),'E00':str(E00),'rayleigh_coefficients':list(map(str,rho)),'residual_squared_coefficients':list(map(str,r2)),'convex_residual_squared':True,'saved_point_Rayleigh_and_full_residual_match':True,'reference_bins':r['reference_certificate']['bins']}
    return rec

@lru_cache(None)
def reference(hi_text,nx,ny):
    hist=occupancy(nx,ny,F(3,10));bins=[dict(q=q,energy_lower=str(e),multiplicity=m) for (q,e),m in sorted(hist.items())]
    return producer.optimize_comparison(nx*ny,F(hi_text),bins)

def interval_inputs(lo,hi,center):
    lo,hi,center=map(F,[lo,hi,center]);assert 0<=lo<=hi;rows=[]
    for nx,ny in SHAPES:
      co=coefficients(str(center),nx,ny);ref=reference(str(hi),nx,ny);N=nx*ny;a=F(ref['a']);b=F(ref['b']);E00=F(co['E00'])
      rho_end=[polynomial(co['rayleigh_coefficients'],e) for e in [lo,hi]];r2_end=[polynomial(co['residual_squared_coefficients'],e) for e in [lo,hi]]
      assert min(r2_end)>=0
      rho_max=max(rho_end);alpha=E00+F(ref['second_shift_lower']);assert alpha>rho_max
      correction=max(r2_end)/(alpha-rho_max)
      rows.append({'geometry':[nx,ny],'polynomial_key':f'{center}_{nx}x{ny}','rayleigh_coefficients':co['rayleigh_coefficients'],'rayleigh_endpoint_values':list(map(str,rho_end)),'rayleigh_max':str(rho_max),'residual_squared_endpoint_values':list(map(str,r2_end)),'residual_squared_max':str(max(r2_end)),'uniform_Temple_correction':str(correction),'uniform_second_eigenvalue_lower':str(alpha),'E00':str(E00),'reference_certificate':ref})
    # Max affine combinations directly, preserving extensive-energy cancellation.
    combos={'A':[-2,1,0],'B':[0,-2,1],'J1':[-8,0,2],'J2':[0,-8,4]};correlated={}
    for key,weights in combos.items():
      co=[sum(w*F(r['rayleigh_coefficients'][j]) for w,r in zip(weights,rows)) for j in range(2)]
      vals=[polynomial(co,e) for e in [lo,hi]]
      correlated[key]={'weights':weights,'affine_coefficients':list(map(str,co)),'endpoint_values':list(map(str,vals)),'maximum':str(max(vals))}
    return {'epsilon_interval':list(map(str,[lo,hi])),'vector_epsilon':str(center),'ground_records':rows,'correlated_energy_combinations':correlated}

def trace_float(r,beta):
    ref=r['reference_certificate'];a=float(F(ref['a']));B=float(F(ref['B']));U=float(F(r['rayleigh_max']));E=float(F(r['E00']));delta=float(F(r['uniform_Temple_correction']))
    return math.exp(beta*delta)+sum(x['multiplicity']*math.exp(-beta*(E+float(F(x['energy_lower']))-4*a*x['q']-B-U)) for x in ref['bins'] if x['q'])

def float_seed(inp,beta):
    q=[trace_float(r,beta) for r in inp['ground_records']];mx={k:float(F(v['maximum'])) for k,v in inp['correlated_energy_combinations'].items()}
    gg=lambda x:1-(1-x)**2/(2*x*x) if x>0 else -1
    A=gg(math.exp(-beta*mx['J1'])/q[0]**8)
    if A<=0:return None
    B=gg(math.exp(-beta*mx['J2'])/q[1]**8*A)
    if B<=0:return None
    C=gg(q[2]**-8*A*A*B)
    if C<=0:return None
    n=4;b=2*beta
    for j in range(64):
      u=max(1-A,1-B,1-C)
      if u<=.002:return {'beta':beta,'n':n,'gap':math.log(1/(32*u))/b if u else float('inf')}
      for _ in range(3):
        new=gg(A**4*B**2*C)
        if new<=0:return None
        A,B,C=B,C,new
      n*=2;b*=2
    return None

def trace_exact(r,beta,exp=exp_bounds,round=up):
    ref=r['reference_certificate'];a=F(ref['a']);B=F(ref['B']);U=F(r['rayleigh_max']);E=F(r['E00']);delta=F(r['uniform_Temple_correction']);tail=F(0)
    for x in ref['bins']:
      if x['q']:tail=round(tail+x['multiplicity']*exp(-beta*(E+F(x['energy_lower'])-4*a*x['q']-B-U))[1])
    return round(exp(beta*delta)[1]+tail),tail

def valid_seed_bounds(inp,beta,exp=exp_bounds,round=up):
    qs=[trace_exact(r,beta,exp,round)[0] for r in inp['ground_records']];mx={k:F(v['maximum']) for k,v in inp['correlated_energy_combinations'].items()}
    vals={k:exp(-beta*mx[k])[0]/qs[i]**power for k,i,power in [('A',0,2),('B',1,2),('J1',0,8),('J2',1,8)]};vals['C']=1/qs[2]**2
    return vals,qs

def seed_exact(inp,beta):
    vals,qs=valid_seed_bounds(inp,beta);vals={k:down(v) for k,v in vals.items()};assert all(0<v<=1 for v in vals.values())
    A=down(G(vals['J1']));assert A>0;B=down(G(vals['J2']*A));assert B>0;C=down(G(vals['C']**4*A*A*B));assert C>0
    boot=replay3(A,B,C,4,4,2*beta);assert boot['accepted']
    valid,iq=valid_seed_bounds(inp,beta,exp192,lambda x:x);assert all(vals[k]<=valid[k]<=1 for k in vals)
    assert exp192(F(boot['beta'])*F(boot['gap_lower']))[1]<1/(32*F(boot['u']))
    states=[[vals[k] for k in ['A','B','C']],[A,B,C]]+[list(map(F,row)) for row in boot['updates']];windows=[]
    for j,state in enumerate(states):
      n=2*2**j
      if n>=boot['n']:break
      c,detail=interpolate_2d(*state);b=beta*2**j;g=finite_gap(c,b)
      windows.append({'n':n,'through':2*n,'beta':str(b),'purities':list(map(str,state)),'uniform_thermal_lower':str(c),'uniform_gap_lower':str(g),'details':detail})
    assert windows[0]['n']==2 and windows[-1]['through']==boot['n']
    mingap=min([F(boot['gap_lower'])]+[F(w['uniform_gap_lower']) for w in windows]);assert mingap>0
    return {'beta':str(beta),**{k+'_lower':str(v) for k,v in vals.items()},'uniform_shifted_trace_uppers':list(map(str,qs)),'bootstrap':boot,'independent_192bit_scalar_enclosures_checked':True,'all_integer_finite_windows':windows,'uniform_all_integer_L_ge2_gap':str(mingap),'gap_display':float(mingap)}

def certify(inp):
    t=time.monotonic();grid=[r for k in range(24,241) if (r:=float_seed(inp,k/2))];out={**inp,'float_scan':{'beta_grid':[12,120,.5],'successes':len(grid)}}
    if not grid:return {**out,'status':'no successful proposal on tested grid','seconds':time.monotonic()-t}
    beta=F(max(grid,key=lambda r:r['gap'])['beta']);seed=seed_exact(inp,beta)
    lo,hi=map(F,inp['epsilon_interval'])
    for r in out['ground_records']:
      ref=r['reference_certificate'];r['endpoint_local_PSD']=[{'epsilon':str(e),**local_psd(F(ref['a']),F(ref['b']),e)} for e in [lo,hi]]
    return {**out,'status':'exact uniform candidate, independent audit pending','seed':seed,'seconds':time.monotonic()-t}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--segments',nargs='*',default=['19/4000:3/500:3/500','3/500:3/400:3/400','3/400:1/125:1/125','1/125:17/2000:17/2000']);ap.add_argument('--name',default='extension');args=ap.parse_args();t=time.monotonic();res=[]
    for seg in args.segments:
      lo,hi,center=map(F,seg.split(':'));inp=interval_inputs(lo,hi,center);r=certify(inp);res.append(r)
      print(json.dumps({'interval':r['epsilon_interval'],'center':r['vector_epsilon'],'status':r['status'],'seed':{k:r.get('seed',{}).get(k) for k in ['beta','gap_display']},'seconds':r['seconds']}),flush=True)
      dump(OUT/(args.name+'_certificates.json'),res)
      polys={r['polynomial_key']:coefficients(inp['vector_epsilon'],*r['geometry']) for x in res for r in x['ground_records'] for inp in [x]}
      dump(OUT/(args.name+'_polynomials.json'),polys)
    dump(OUT/(args.name+'_cost.json'),{'seconds':time.monotonic()-t,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'cpu_threads':1,'new_eigensolves':0})
if __name__=='__main__':main()
