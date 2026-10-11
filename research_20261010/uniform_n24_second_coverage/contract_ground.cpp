// Independent ordinary D26 norm and energy contractions from audited blocks.
#include <gmpxx.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <sys/resource.h>
#include <sched.h>
#include <ctime>
using Z=mpz_class;
struct Mat{int n;std::vector<Z>x;Mat(int n):n(n),x(n*n){}};
Mat mul(const Mat&a,const Mat&b){int n=a.n;Mat c(n);for(int i=0;i<n;i++)for(int k=0;k<n;k++)if(a.x[i*n+k]!=0)for(int j=0;j<n;j++)if(b.x[k*n+j]!=0)mpz_addmul(c.x[i*n+j].get_mpz_t(),a.x[i*n+k].get_mpz_t(),b.x[k*n+j].get_mpz_t());return c;}
Z trprod(const Mat&a,const Mat&b){Z z;int n=a.n;for(int i=0;i<n;i++)for(int j=0;j<n;j++)mpz_addmul(z.get_mpz_t(),a.x[i*n+j].get_mpz_t(),b.x[j*n+i].get_mpz_t());return z;}
int main(int argc,char**argv){if(argc<3)return 2;rlimit mem{100ul*1024*1024,100ul*1024*1024},cpu{60,60};setrlimit(RLIMIT_AS,&mem);setrlimit(RLIMIT_CPU,&cpu);cpu_set_t set;CPU_ZERO(&set);sched_getaffinity(0,sizeof(set),&set);int selected=-1;for(int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&set))selected=i;CPU_ZERO(&set);CPU_SET(selected,&set);sched_setaffinity(0,sizeof(set),&set);clock_t c0=clock();std::ifstream f(argv[1]);int nb;if(!(f>>nb)||nb!=11){std::cerr<<"Invalid block input\n";return 3;}std::vector<int>ns;for(int a=2;a<argc;a++)ns.push_back(std::stoi(argv[a]));std::vector<Z>U(ns.size()),V(ns.size());for(int g=0;g<nb;g++){int q,n;f>>q>>n;Mat T(n),O(n);for(auto&z:T.x)f>>z;for(auto&z:O.x)f>>z;std::vector<Mat>powers;powers.push_back(T);for(int j=1;j<=7;j++)powers.push_back(mul(powers.back(),powers.back()));for(int j=0;j<(int)ns.size();j++){Mat p(n);for(int i=0;i<n;i++)p.x[i*n+i]=1;for(int k=0;k<=7;k++)if((ns[j]-2)&(1<<k))p=mul(p,powers[k]);U[j]+=ns[j]*trprod(p,O);V[j]+=trprod(p,powers[1]);}std::cerr<<"block="<<q<<" dim="<<n<<"\n";}for(int j=0;j<(int)ns.size();j++)std::cout<<"H0_"<<ns[j]<<"="<<U[j]<<"\nN0_"<<ns[j]<<"="<<V[j]<<"\n";rusage r;getrusage(RUSAGE_SELF,&r);std::cerr<<"FINAL cpu_seconds="<<double(clock()-c0)/CLOCKS_PER_SEC<<" peak_kb="<<r.ru_maxrss<<"\n";}
