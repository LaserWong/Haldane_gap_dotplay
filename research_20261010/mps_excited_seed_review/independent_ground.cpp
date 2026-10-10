// Sequential sparse ground contraction through length 48, no power squaring.
#include <gmpxx.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <sys/resource.h>
#include <sched.h>
#include <ctime>
#include <cassert>
using Z=mpz_class;struct Entry{int i,j;long v;};
int main(int argc,char**argv){assert(argc==2);rlimit m{1024ul*1024*1024,1024ul*1024*1024},c{300,300};setrlimit(RLIMIT_AS,&m);setrlimit(RLIMIT_CPU,&c);cpu_set_t s;CPU_ZERO(&s);sched_getaffinity(0,sizeof(s),&s);int cpu=0;while(!CPU_ISSET(cpu,&s))cpu++;CPU_ZERO(&s);CPU_SET(cpu,&s);sched_setaffinity(0,sizeof(s),&s);clock_t start=clock();std::ifstream f(argv[1]);int count;f>>count;Z norms[49],energies[49];while(count--){int charge,d;f>>charge>>d;std::vector<Entry>T,O;for(auto*V:{&T,&O})for(int i=0;i<d;i++)for(int j=0;j<d;j++){long x;f>>x;if(x)V->push_back({i,j,x});}std::vector<Z>P(d*d);for(int i=0;i<d;i++)P[i*d+i]=1;for(int n=0;n<=48;n++){if(n%2==0){if(n>=2)for(int i=0;i<d;i++)norms[n]+=P[i*d+i];if(n+2<=48)for(auto&e:O)energies[n+2]+=(n+2)*P[e.j*d+e.i]*e.v;}if(n==48)break;std::vector<Z>next(d*d);for(auto&e:T)for(int i=0;i<d;i++)if(P[i*d+e.i]!=0){if(e.v>0)mpz_addmul_ui(next[i*d+e.j].get_mpz_t(),P[i*d+e.i].get_mpz_t(),e.v);else mpz_submul_ui(next[i*d+e.j].get_mpz_t(),P[i*d+e.i].get_mpz_t(),-e.v);}P.swap(next);}}for(int n=2;n<=48;n+=2)std::cout<<"N0_"<<n<<"="<<norms[n]<<"\nH0_"<<n<<"="<<energies[n]<<"\n";rusage r;getrusage(RUSAGE_SELF,&r);std::cerr<<"CPU_seconds="<<double(clock()-start)/CLOCKS_PER_SEC<<" peak_KiB="<<r.ru_maxrss<<"\n";}
