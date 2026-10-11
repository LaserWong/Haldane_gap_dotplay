import os,time
assert os.sched_getaffinity(0)=={7}
pid=os.fork()
assert os.sched_getaffinity(0)=={7}
while True:
 x=sum(range(10000))
