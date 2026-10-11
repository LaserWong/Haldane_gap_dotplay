from budget import *
import hashlib
start=time.time();out=[]
for g in (F(21,200),F(11,100)):
 v16=P.L.optimized_auxiliary(C.MODELS[0],g);v64=C.optimized_vector(P.NUM,g);vectors=[v16,E.vectors[1],v64]
 d=P.interval_data(g,g,vectors)
 for p in d['denominator_patches']:p['odd_band']['fixed_center']='1/10'
 tests=[]
 for b in (F(8),F(47,5),F(11),F(13)):
  r,cc=ratios(d,b);tests.append({'beta':str(b),'ratios':r,'path':float_path(r,b)})
 print(g,[(x['beta'],x['path']['status']) for x in tests],flush=True)
 out.append({'g':str(g),'data':d,'tests':tests,'scope':'Reoptimized11D ground16 and43D numerator64 using saved exact matrices; ground32 vector and both odd families unchanged.'})
(HERE/'reoptimized_saved.json').write_text(json.dumps({'results':out,'seconds':time.time()-start},indent=2)+'\n')
