"""All contraction/test children: one pinned CPU, 1 GiB address space, 600 CPU seconds."""
import os,sys,resource
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
resource.setrlimit(resource.RLIMIT_CPU,(600,600))
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
os.execvp(sys.argv[1],sys.argv[1:])
