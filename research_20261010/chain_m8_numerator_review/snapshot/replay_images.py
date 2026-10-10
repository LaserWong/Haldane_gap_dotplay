"""Reconstruct all three saved full images using Python integers and sealed physical kernel."""
from probe import *
START=time.process_time();checks=[]
def verify_image(name,ks,vs):
 begin=time.process_time();out,visits=full_action(ks,vs);lines=0
 with (HERE/name).open() as f:
  for line in f:
   key,val=map(int,line.split());assert out.get(key)==val,(name,key);lines+=1
 assert lines==len(out)
 checks.append(dict(file=name,support=lines,transitions=visits,cpu_seconds=time.process_time()-begin));print('IMAGE PASS',checks[-1],flush=True)
 return out
first=verify_image('full_image.txt',keys,vec)
second=verify_image('second_image.txt',list(first),list(first.values()));del second
other=verify_image('old_direction_image.txt',keys,list(map(int,vectors[0])));del other
(HERE/'image_verification.json').write_text(json.dumps(dict(status='ALL_FULL_IMAGES_REPLAYED_WITH_PYTHON_INTEGERS',checks=checks,total_cpu_seconds=time.process_time()-START,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))
