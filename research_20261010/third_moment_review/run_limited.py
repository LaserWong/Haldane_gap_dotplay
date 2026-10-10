import os,resource,sys
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
os.execvp(sys.argv[1],sys.argv[1:])
