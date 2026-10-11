// Independent ordinary D26 norm and energy contractions from audited blocks.
#include <gmpxx.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <sys/resource.h>
#include <sched.h>
#include <ctime>
#include <signal.h>
#include <sys/prctl.h>
#include <unistd.h>
using Z=mpz_class;
struct Mat{int n;std::vector<Z>x;Mat(int n):n(n),x(n*n){}};
Mat mul(const Mat&a,const Mat&b){int n=a.n;Mat c(n);for(int i=0;i<n;i++)for(int k=0;k<n;k++)if(a.x[i*n+k]!=0)for(int j=0;j<n;j++)if(b.x[k*n+j]!=0)mpz_addmul(c.x[i*n+j].get_mpz_t(),a.x[i*n+k].get_mpz_t(),b.x[k*n+j].get_mpz_t());return c;}
Z trprod(const Mat&a,const Mat&b){Z z;int n=a.n;for(int i=0;i<n;i++)for(int j=0;j<n;j++)mpz_addmul(z.get_mpz_t(),a.x[i*n+j].get_mpz_t(),b.x[j*n+i].get_mpz_t());return z;}
int main(int argc,char**argv){if(argc<3)return 2;rlimit mem{100ul*1024*1024,100ul*1024*1024},cpu{30,30};if(setrlimit(RLIMIT_AS,&mem)!=0 || setrlimit(RLIMIT_CPU,&cpu)!=0)return 10;rlimit am,ac;if(getrlimit(RLIMIT_AS,&am)!=0 || getrlimit(RLIMIT_CPU,&ac)!=0)return 11;if(am.rlim_cur!=100ul*1024*1024 || am.rlim_max!=100ul*1024*1024 || ac.rlim_cur!=30 || ac.rlim_max!=30)return 12;std::cerr<<"LIMITS cpu_soft="<<ac.rlim_cur<<" cpu_hard="<<ac.rlim_max<<" as_soft="<<am.rlim_cur<<" as_hard="<<am.rlim_max<<"\n";cpu_set_t set;CPU_ZERO(&set);sched_getaffinity(0,sizeof(set),&set);int selected=-1;for(int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&set))selected=i;CPU_ZERO(&set);CPU_SET(selected,&set);if(sched_setaffinity(0,sizeof(set),&set)!=0)return 13;cpu_set_t verify;CPU_ZERO(&verify);if(sched_getaffinity(0,sizeof(verify),&verify)!=0 || CPU_COUNT(&verify)!=1 || !CPU_ISSET(4,&verify))return 14;struct sigaction act;if(sigaction(SIGXCPU,nullptr,&act)!=0 || act.sa_handler!=SIG_DFL)return 15;sigset_t blocked;if(sigprocmask(SIG_BLOCK,nullptr,&blocked)!=0 || sigismember(&blocked,SIGXCPU))return 16;int pd=0;if(prctl(PR_GET_PDEATHSIG,&pd)!=0 || pd!=SIGKILL)return 17;std::cerr<<"POSTEXEC affinity=4 threads=1 SIGXCPU=default_unblocked PDEATHSIG=9\n";clock_t c0=clock();std::ifstream f(argv[1]);int nb;if(!(f>>nb)||nb!=11){std::cerr<<"Invalid block input\n";return 3;}std::vector<int>ns;for(int a=2;a<argc;a++)ns.push_back(std::stoi(argv[a]));for(int n:ns)if(n<26 || n>33)return 4;std::vector<Z>U(ns.size()),V(ns.size());for(int g=0;g<nb;g++){int q,n;f>>q>>n;Mat T(n),O(n);for(auto&z:T.x)f>>z;for(auto&z:O.x)f>>z;std::vector<Mat>powers;powers.push_back(T);for(int j=1;j<=4;j++)powers.push_back(mul(powers.back(),powers.back()));for(int j=0;j<(int)ns.size();j++){Mat p(n);for(int i=0;i<n;i++)p.x[i*n+i]=1;for(int k=0;k<=4;k++)if((ns[j]-2)&(1<<k))p=mul(p,powers[k]);U[j]+=ns[j]*trprod(p,O);V[j]+=trprod(p,powers[1]);}std::cerr<<"block="<<q<<" dim="<<n<<"\n";}for(int j=0;j<(int)ns.size();j++)std::cout<<"H0_"<<ns[j]<<"="<<U[j]<<"\nN0_"<<ns[j]<<"="<<V[j]<<"\n";rusage r;getrusage(RUSAGE_SELF,&r);std::cerr<<"FINAL cpu_seconds="<<double(clock()-c0)/CLOCKS_PER_SEC<<" peak_kb="<<r.ru_maxrss<<"\n";}
