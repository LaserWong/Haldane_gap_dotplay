// Independent sequential powers, avoiding producer binary-power contraction.
#include <gmpxx.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <set>
#include <algorithm>
#include <sys/resource.h>
#include <sched.h>
#include <ctime>
using Z=mpz_class;
struct M{int n;std::vector<Z>a;M(int d):n(d),a(d*d){}};
M step(const M&p,const M&t){M out(p.n);for(int i=0;i<p.n;i++)for(int k=0;k<p.n;k++)if(p.a[i*p.n+k]!=0)for(int j=0;j<p.n;j++)if(t.a[k*p.n+j]!=0)out.a[i*p.n+j]+=p.a[i*p.n+k]*t.a[k*p.n+j];return out;}
Z trace(const M&p){Z out;for(int i=0;i<p.n;i++)out+=p.a[i*p.n+i];return out;}
Z ins(const M&p,const M&o){Z out;for(int i=0;i<p.n;i++)for(int j=0;j<p.n;j++)out+=p.a[i*p.n+j]*o.a[j*p.n+i];return out;}
int main(int argc,char**argv){if(argc<3)return 2;rlimit mem{700ul*1024*1024,700ul*1024*1024},time{600,600};setrlimit(RLIMIT_AS,&mem);setrlimit(RLIMIT_CPU,&time);cpu_set_t set;CPU_ZERO(&set);sched_getaffinity(0,sizeof(set),&set);int cpu=-1;for(int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&set)){cpu=i;break;}if(CPU_ISSET(5,&set))cpu=5;CPU_ZERO(&set);CPU_SET(cpu,&set);sched_setaffinity(0,sizeof(set),&set);clock_t start=clock();std::set<int>want;for(int i=2;i<argc;i++)want.insert(std::stoi(argv[i]));int max=*want.rbegin();if(*want.begin()<4||max>120)return 3;std::vector<Z>U(max+1),V(max+1);std::ifstream f(argv[1]);int blocks;f>>blocks;if(!f||blocks!=11)return 4;for(int b=0;b<blocks;b++){int q,d;f>>q>>d;if(!f||d<1||d>162)return 5;M t(d),o(d),p(d);for(auto&x:t.a)f>>x;for(auto&x:o.a)f>>x;if(!f)return 6;for(int i=0;i<d;i++)p.a[i*d+i]=1;for(int k=1;k<=max;k++){p=step(p,t);if(want.count(k+2))U[k+2]+=(k+2)*ins(p,o);if(want.count(k))V[k]+=trace(p);}std::cerr<<"block="<<q<<" dim="<<d<<"\n";}for(int n:want)std::cout<<"H0_"<<n<<"="<<U[n]<<"\nN0_"<<n<<"="<<V[n]<<"\n";rusage r;getrusage(RUSAGE_SELF,&r);std::cerr<<"cpu="<<cpu<<" cpu_seconds="<<double(clock()-start)/CLOCKS_PER_SEC<<" peak_kib="<<r.ru_maxrss<<"\n";}
