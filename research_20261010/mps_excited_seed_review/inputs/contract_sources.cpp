// Exact GMP two-source polynomial contractions, truncated at u^2=v^2=0.
// Each of four coefficients is represented by charge-compatible rectangular
// blocks. Local transfers/insertion entries are sparse signed 64-bit integers.
#include <gmpxx.h>
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <chrono>
#include <sys/resource.h>
#include <sched.h>
#include <cassert>
using Z=mpz_class;
constexpr int NG=11;
const int shift[4]={0,-1,1,0};
int dims[NG];
struct Mat {
 int r=0,c=0; std::vector<Z> x;
 Mat()=default; Mat(int a,int b):r(a),c(b),x(a*b){}
 Z& at(int i,int j){return x[i*c+j];}
 const Z& at(int i,int j)const{return x[i*c+j];}
};
using Poly=std::array<std::array<Mat,NG>,4>;
struct Entry{int col;long value;};
using Sparse=std::array<std::array<std::vector<std::vector<Entry>>,NG>,4>;
Poly zero(){Poly p;for(int a=0;a<4;a++)for(int g=0;g<NG;g++){int h=g+shift[a];if(h>=0&&h<NG)p[a][g]=Mat(dims[g],dims[h]);}return p;}
void addsmall(Z& out,const Z& a,long b,int sign){
 if((b>0)==(sign>0))mpz_addmul_ui(out.get_mpz_t(),a.get_mpz_t(),b>0?b:-b);
 else mpz_submul_ui(out.get_mpz_t(),a.get_mpz_t(),b>0?b:-b);
}
Poly advance(const Poly&p,const Sparse&e,int sign){
 Poly out=zero();
 for(int a=0;a<4;a++)for(int b=0;b<4;b++)if(!(a&b)){
  int s=(b==1||b==2)?sign:1;
  for(int g=0;g<NG;g++){
   int h=g+shift[a];if(h<0||h>=NG)continue;
   const Mat&A=p[a][g];Mat&C=out[a|b][g];
   if(!A.r||!C.c)continue;
   const auto&B=e[b][h];
   for(int i=0;i<A.r;i++)for(int k=0;k<A.c;k++)if(A.at(i,k)!=0)
    for(const auto& t:B[k])addsmall(C.at(i,t.col),A.at(i,k),t.value,s);
  }
 }
 return out;
}
Z trace(const Poly&p,int a){Z z=0;assert(shift[a]==0);for(int g=0;g<NG;g++)for(int i=0;i<dims[g];i++)z+=p[a][g].at(i,i);return z;}
Z insertion(const Poly&p,const Sparse&o,int degree){
 Z z=0;
 for(int a=0;a<4;a++)for(int b=0;b<4;b++)if(!(a&b)&&(a|b)==degree){
  for(int g=0;g<NG;g++){
   int h=g+shift[a];if(h<0||h>=NG)continue;
   const auto&A=p[a][g];if(!A.r)continue;
   const auto&B=o[b][h];
   for(int k=0;k<A.c;k++)for(const auto&t:B[k])addsmall(z,A.at(t.col,k),t.value,1);
  }
 }
 return z;
}
int main(int argc,char**argv){
 if(argc!=3)return 2;
 int maxn=std::stoi(argv[2]);assert(maxn>=2&&maxn%2==0);
 rlimit mem{1024ul*1024*1024,1024ul*1024*1024},cpu{600,600};setrlimit(RLIMIT_AS,&mem);setrlimit(RLIMIT_CPU,&cpu);
 cpu_set_t set;CPU_ZERO(&set);sched_getaffinity(0,sizeof(set),&set);int chosen=-1;for(int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&set))chosen=i;CPU_ZERO(&set);CPU_SET(chosen,&set);sched_setaffinity(0,sizeof(set),&set);
 auto t0=std::chrono::steady_clock::now();clock_t c0=clock();
 std::ifstream f(argv[1]);assert(f.good());
 std::array<int,676> group,local;for(int i=0;i<676;i++){int q;f>>q;int g=(q+10)/2;group[i]=g;local[i]=dims[g]++;}
 Sparse E,O;
 for(Sparse* family:{&E,&O})for(int a=0;a<4;a++){
  for(int g=0;g<NG;g++)(*family)[a][g].resize(dims[g]);
  int nz;f>>nz;
  for(int z=0;z<nz;z++){int i,j;long value;f>>i>>j>>value;assert(group[j]-group[i]==shift[a]);(*family)[a][group[i]][local[i]].push_back({local[j],value});}
 }
 assert(f.good());
 Poly p=zero();for(int g=0;g<NG;g++)for(int i=0;i<dims[g];i++)p[0][g].at(i,i)=1;
 for(int k=0;k<=maxn;k++){
  if(k%2==0){
   if(k>=2)std::cout<<"N0_"<<k<<"="<<trace(p,0)<<"\nN1_"<<k<<"="<<trace(p,3)<<"\n";
   if(k+2<=maxn)std::cout<<"H0_"<<k+2<<"="<<(k+2)*insertion(p,O,0)<<"\nH1_"<<k+2<<"="<<(k+2)*insertion(p,O,3)<<"\n";
   std::cout.flush();
   rusage r;getrusage(RUSAGE_SELF,&r);
   std::cerr<<"length="<<k<<" cpu_seconds="<<double(clock()-c0)/CLOCKS_PER_SEC<<" peak_kb="<<r.ru_maxrss<<"\n";
  }
  if(k<maxn)p=advance(p,E,k%2?-1:1);
 }
 rusage r;getrusage(RUSAGE_SELF,&r);std::cerr<<"FINAL cpu_seconds="<<double(clock()-c0)/CLOCKS_PER_SEC<<" wall_seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count()<<" peak_kb="<<r.ru_maxrss<<"\n";
}
