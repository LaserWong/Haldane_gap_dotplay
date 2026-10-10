// Independent global-index sparse transfer replay, without rectangular blocks.
#include <gmpxx.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <array>
#include <cassert>
#include <ctime>
#include <sys/resource.h>
#include <sched.h>
using Z=mpz_class; const int D=676;
struct Elt{int i,j;long v;};
using State=std::array<std::vector<Z>,4>;
int main(int argc,char**argv){
 assert(argc==2);rlimit m{1024ul*1024*1024,1024ul*1024*1024},c{600,600};setrlimit(RLIMIT_AS,&m);setrlimit(RLIMIT_CPU,&c);
 cpu_set_t a;CPU_ZERO(&a);sched_getaffinity(0,sizeof(a),&a);int first=0;while(!CPU_ISSET(first,&a))first++;CPU_ZERO(&a);CPU_SET(first,&a);sched_setaffinity(0,sizeof(a),&a);
 clock_t start=clock();std::ifstream f(argv[1]);std::vector<int>q(D);for(auto&x:q)f>>x;
 std::array<std::vector<Elt>,4>E,O;for(auto*F:{&E,&O})for(int p=0;p<4;p++){int nz;f>>nz;while(nz--){Elt e;f>>e.i>>e.j>>e.v;(*F)[p].push_back(e);}}
 State P;for(auto&x:P)x.resize(D*D);for(int i=0;i<D;i++)P[0][i*D+i]=1;
 const int charge[4]={0,-2,2,0};
 for(int length=0;length<=24;length++){
  if(length%2==0){
   for(int target:{0,3}){
    if(length>=2){Z norm;for(int i=0;i<D;i++)norm+=P[target][i*D+i];std::cout<<"N"<<(target==3)<<"_"<<length<<"="<<norm<<"\n";}
    if(length+2<=24){Z energy;
     for(int bra=0;bra<=1;bra++)for(int ket=0;ket<=1;ket++)for(int ibra=0;ibra<=1;ibra++)for(int iket=0;iket<=1;iket++){
      if(bra+ibra!=(target&1)||ket+iket!=(target>>1))continue;
      for(const auto&e:O[ibra+2*iket]){const Z&z=P[bra+2*ket][e.j*D+e.i];if(z!=0)energy+=z*e.v;}
     }
     std::cout<<"H"<<(target==3)<<"_"<<length+2<<"="<<energy*(length+2)<<"\n";
    }
   }
   std::cout.flush();
  }
  if(length==24)break;
  State N;for(auto&x:N)x.resize(D*D);
  for(int bra=0;bra<=1;bra++)for(int ket=0;ket<=1;ket++)for(int ibra=0;ibra<=1-bra;ibra++)for(int iket=0;iket<=1-ket;iket++){
   int p=bra+2*ket,r=ibra+2*iket,t=p+r;int sign=(length%2&&(ibra+iket)%2)?-1:1;
   for(const auto&e:E[r])for(int i=0;i<D;i++)if(q[e.i]-q[i]==charge[p]){
    const Z&z=P[p][i*D+e.i];if(z!=0){long v=sign*e.v;if(v>0)mpz_addmul_ui(N[t][i*D+e.j].get_mpz_t(),z.get_mpz_t(),v);else mpz_submul_ui(N[t][i*D+e.j].get_mpz_t(),z.get_mpz_t(),-v);}
   }
  }
  P.swap(N);
 }
 rusage usage;getrusage(RUSAGE_SELF,&usage);std::cerr<<"CPU_seconds="<<double(clock()-start)/CLOCKS_PER_SEC<<" peak_KiB="<<usage.ru_maxrss<<"\n";
}
