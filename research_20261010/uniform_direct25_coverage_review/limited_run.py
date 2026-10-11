#!/usr/bin/env python3
import os,resource,sys
from pathlib import Path
P=Path(__file__).resolve().parent
resource.setrlimit(resource.RLIMIT_AS,(100*1024**2,100*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(15,15))
aff=os.sched_getaffinity(0);os.sched_setaffinity(0,{5 if 5 in aff else min(aff)})
assert resource.getrlimit(resource.RLIMIT_AS)==(100*1024**2,100*1024**2)
assert resource.getrlimit(resource.RLIMIT_CPU)==(15,15)
# Verify the sealed executable cannot raise these external hard ceilings.
for which,higher in ((resource.RLIMIT_AS,(700*1024**2,700*1024**2)),(resource.RLIMIT_CPU,(600,600))):
 try:resource.setrlimit(which,higher)
 except (ValueError,OSError):pass
 else:raise RuntimeError('External hard ceiling could be raised; refusing execution')
assert resource.getrlimit(resource.RLIMIT_AS)==(100*1024**2,100*1024**2)
assert resource.getrlimit(resource.RLIMIT_CPU)==(15,15)
os.execv(str(P/'contract_sequential'),[str(P/'contract_sequential'),str(P/'d26_blocks.txt'),*sys.argv[1:]])
