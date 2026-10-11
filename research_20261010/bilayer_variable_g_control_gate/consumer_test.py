import json,time,copy
import controller as c
import pencil24 as pen
p=c.P;t=time.process_time();count=0;mutations=0
for name in ['generic4','generic5','localized4','localized5','symmetrized4','symmetrized5']:
 sectors=c.read(p/'runs'/name/'sectors24.json');raw=c.read(p/'runs'/name/'pencils.json');out=[]
 for row in raw['tests']:
  v=pen.pencil(sectors,row['g_num'],row['g_den']);assert v['G_numerators']==raw['G'];assert v['K_numerators']==row['K_scaled_11'];assert v['J_numerators']==row['J_scaled_121'];pen.validate_export(v);out.append(v);count+=1
  for key,factor in [('K_denominator',2),('J_denominator',4)]:
   wrong=copy.deepcopy(v);wrong[key]//=factor
   try:pen.validate_export(wrong);raise RuntimeError('wrong denominator survived')
   except AssertionError:mutations+=1
 c.atomic(p/(name+'_physical_pencils_v1.json'),{'source_raw_sha256':c.digest((p/'runs'/name/'pencils.json').read_bytes()),'schema':pen.SCHEMA,'pencils':out})
c.atomic(p/'CONSUMER_TESTS.json',dict(physical_pencils_reconstructed=count,wrong_denominator_mutations_rejected=mutations,controller_cpu=time.process_time()-t));print(count,mutations)
