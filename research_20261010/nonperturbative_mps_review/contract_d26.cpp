#include <gmpxx.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <sys/resource.h>
#include <chrono>
using Z=mpz_class;
using M=std::vector<std::vector<Z>>;
M mul(const M&a,const M&b){size_t n=a.size();M c(n,std::vector<Z>(n));for(size_t i=0;i<n;++i)for(size_t j=0;j<n;++j)for(size_t k=0;k<n;++k)if(a[i][k]!=0&&b[k][j]!=0)c[i][j]+=a[i][k]*b[k][j];return c;}
Z tr(const M&a){Z r=0;for(size_t i=0;i<a.size();++i)r+=a[i][i];return r;}
Z inserted(const M&a,const M&o){Z r=0;for(size_t i=0;i<a.size();++i)for(size_t j=0;j<a.size();++j)r+=a[i][j]*o[j][i];return r;}
int main(int argc,char**argv){auto start=std::chrono::steady_clock::now();if(argc!=2)return 1;std::ifstream f(argv[1]);int nb;f>>nb;Z U[21],V[21];for(int b=0;b<nb;++b){int diff,n;f>>diff>>n;M t(n,std::vector<Z>(n)),o=t,p=t;for(auto&r:t)for(auto&v:r)f>>v;for(auto&r:o)for(auto&v:r)f>>v;for(int i=0;i<n;++i)p[i][i]=1;for(int k=1;k<=20;++k){p=mul(p,t);if(k==10||k==14||k==18)U[k+2]+=inserted(p,o);if(k==12||k==16||k==20)V[k]+=tr(p);}std::cerr<<"contracted block "<<diff<<" dimension "<<n<<"\n";}for(int L:{12,16,20})std::cout<<"U"<<L<<"="<<U[L]<<"\nV"<<L<<"="<<V[L]<<"\n";struct rusage usage;getrusage(RUSAGE_SELF,&usage);std::cerr<<"peak_kb="<<usage.ru_maxrss<<" elapsed_seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";}
