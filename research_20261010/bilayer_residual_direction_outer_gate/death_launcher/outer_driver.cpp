// Sole campaign entry point: fixed plan, durable precharges, no retries or resume.
#include <sys/resource.h>
#include <sys/prctl.h>
#include <sys/file.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <cassert>
#include <cerrno>
#include <cstring>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
void logline(int fd,const string&s){string x=s+"\n";size_t n=0;while(n<x.size()){ssize_t z=write(fd,x.data()+n,x.size()-n);assert(z>0);n+=z;}assert(fsync(fd)==0);}
int main(int argc,char**argv){assert(argc==6);string mode=argv[1],home=argv[2],out=argv[3],geo=argv[4],coef=argv[5];bool fixture=mode=="fixture";assert(fixture||mode=="production_authorized");int N,d;ifstream gf(geo);gf>>N>>d;assert((fixture&&N==8&&d==5)||(!fixture&&N==32&&d==14));int nx=fixture?4:8,ny=fixture?2:4;
 // Effective limits are the terminating soft limits. Children may raise their
 // own soft limits only within the unchanged100MiB/360CPU hard campaign envelope.
 assert(signal(SIGXCPU,SIG_DFL)!=SIG_ERR);rlimit as{8*1024*1024,100*1024*1024},cpu{10,360};assert(setrlimit(RLIMIT_AS,&as)==0);assert(setrlimit(RLIMIT_CPU,&cpu)==0);cpu_set_t cpus;CPU_ZERO(&cpus);CPU_SET(3,&cpus);assert(sched_setaffinity(0,sizeof(cpus),&cpus)==0);
 assert(mkdir(out.c_str(),0700)==0&&"campaign directory exists: no restart/resume is allowed");int lock=open((out+"/outer.lock").c_str(),O_CREAT|O_RDWR,0600);assert(lock>=0&&flock(lock,LOCK_EX|LOCK_NB)==0);int ledger=open((out+"/outer_ledger.jsonl").c_str(),O_CREAT|O_EXCL|O_WRONLY,0600);assert(ledger>=0);
 int reserved=10,call=0;logline(ledger,"{\"event\":\"start\",\"driver_cpu_reservation\":10,\"total_cpu_cap\":360,\"memory_split_MiB\":[8,32,60],\"automatic_restart\":false}");
 auto invoke=[&](vector<string> args,int cap){assert(reserved+cap<=360);reserved+=cap;int id=call++;logline(ledger,"{\"event\":\"reserve_invocation\",\"index\":"+to_string(id)+",\"cpu_cap_including_supervisor\":"+to_string(cap)+",\"cumulative_reserved\":"+to_string(reserved)+"}");pid_t parent=getpid(),pid=fork();assert(pid>=0);if(pid==0){assert(prctl(PR_SET_PDEATHSIG,SIGKILL)==0);if(getppid()!=parent)kill(getpid(),SIGKILL);rlimit child_as{32*1024*1024,100*1024*1024},child_cpu{1,360};if(setrlimit(RLIMIT_AS,&child_as)||setrlimit(RLIMIT_CPU,&child_cpu))_exit(120);string logfile=out+"/invocation_"+to_string(id)+".log";int fd=open(logfile.c_str(),O_CREAT|O_EXCL|O_WRONLY,0600);if(fd<0)_exit(121);dup2(fd,STDOUT_FILENO);dup2(fd,STDERR_FILENO);close(fd);setenv("RESIDUAL_OUTER_LOCK_FD",to_string(lock).c_str(),1);vector<string> cmd={"/usr/bin/python3",home+"/checkpoint.py"};cmd.insert(cmd.end(),args.begin(),args.end());vector<char*> av;for(auto&s:cmd)av.push_back(s.data());av.push_back(nullptr);execv(av[0],av.data());_exit(127);}
  int status=0;rusage ru{};assert(wait4(pid,&status,0,&ru)==pid);double used=ru.ru_utime.tv_sec+ru.ru_utime.tv_usec/1e6+ru.ru_stime.tv_sec+ru.ru_stime.tv_usec/1e6;bool ok=WIFEXITED(status)&&WEXITSTATUS(status)==0;logline(ledger,"{\"event\":\"invocation_return\",\"index\":"+to_string(id)+",\"success\":"+(ok?"true":"false")+",\"wait_status\":"+to_string(status)+",\"observed_wait4_cpu_seconds\":"+to_string(used)+"}");if(!ok){logline(ledger,"{\"event\":\"STOPPED_ON_FIRST_FAILURE\",\"cumulative_reserved\":"+to_string(reserved)+"}");exit(2);}};
 string state=out+"/checkpoint";invoke({"init",state,"--geometry",geo,"--coefficients",coef,"--nx",to_string(nx),"--ny",to_string(ny),"--budget",fixture?"10":"350"},1);
 if(fixture){for(auto phase:{"q4","q6"})for(int k=0;k<2;k++)invoke({"chunk",state,"--phase",phase,"--count",phase==string("q4")?(k?"18":"17"):(k?"11":"10"),"--cap","2"},2);}else{for(int k=0;k<2;k++)invoke({"chunk",state,"--phase","q4","--count","4096","--cap","6"},6);for(int k=0;k<42;k++)invoke({"chunk",state,"--phase","q6","--count","4096","--cap","8"},8);}
 invoke({"assemble",state},1);assert(call==(fixture?6:46));assert(reserved==(fixture?20:360));logline(ledger,"{\"event\":\"COMPLETE_SOLE_PATH\",\"invocations\":"+to_string(call)+",\"cumulative_reserved\":"+to_string(reserved)+"}");close(ledger);close(lock);return 0;}
