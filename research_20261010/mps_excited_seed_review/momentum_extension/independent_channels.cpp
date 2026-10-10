// Independent Heisenberg single-site channel accumulator; no two-site O file.
#include <gmpxx.h>
#include <vector>
#include <array>
#include <fstream>
#include <iostream>
#include <cassert>
#include <ctime>
#include <sys/resource.h>
#include <sched.h>
using Z=mpz_class;const int D=676;
struct Entry{int col;long v;};
struct Sparse{int shift;std::vector<std::vector<Entry>>rows;Sparse():rows(D){}};
struct Dense{int shift;std::vector<Z>x;Dense(int s=0):shift(s),x(D*D){}};
std::vector<int>charges;std::array<std::vector<int>,11>groups;
void addmul(Dense&C,const Dense&A,const Sparse&B){assert(C.shift==A.shift+B.shift);for(int i=0;i<D;i++){int target=(charges[i]+10)/2+A.shift;if(target<0||target>=11)continue;for(int k:groups[target]){const Z&z=A.x[i*D+k];if(z!=0)for(auto&e:B.rows[k]){if(e.v>0)mpz_addmul_ui(C.x[i*D+e.col].get_mpz_t(),z.get_mpz_t(),e.v);else mpz_submul_ui(C.x[i*D+e.col].get_mpz_t(),z.get_mpz_t(),-e.v);}}}}
Dense mul(const Dense&A,const Sparse&B){Dense C(A.shift+B.shift);addmul(C,A,B);return C;}
Dense dense(const Sparse&A){Dense P(A.shift);for(int i=0;i<D;i++)for(auto&e:A.rows[i])P.x[i*D+e.col]=e.v;return P;}
Z trace(const Dense&A){assert(A.shift==0);Z z;for(int i=0;i<D;i++)z+=A.x[i*D+i];return z;}
Z trprod(const Dense&A,const Sparse&B){assert(A.shift+B.shift==0);Z z;for(int i=0;i<D;i++)for(auto&e:B.rows[i])z+=A.x[e.col*D+i]*e.v;return z;}
int main(int argc,char**argv){assert(argc>=4);rlimit mem{700ul*1024*1024,700ul*1024*1024},cpu{600,600};setrlimit(RLIMIT_AS,&mem);setrlimit(RLIMIT_CPU,&cpu);cpu_set_t cp;CPU_ZERO(&cp);sched_getaffinity(0,sizeof(cp),&cp);int selected=0;while(!CPU_ISSET(selected,&cp))selected++;CPU_ZERO(&cp);CPU_SET(selected,&cp);sched_setaffinity(0,sizeof(cp),&cp);clock_t start=clock();std::ifstream f(argv[1]);charges.resize(D);for(int i=0;i<D;i++){f>>charges[i];groups[(charges[i]+10)/2].push_back(i);}std::array<std::array<Sparse,4>,4>X;for(auto&pair:X)for(auto&op:pair){int nz;f>>op.shift>>nz;while(nz--){int i,j;long value;f>>i>>j>>value;assert(charges[j]-charges[i]==2*op.shift);op.rows[i].push_back({j,value});}}assert(f.good());int n=std::stoi(argv[2]);assert(n>=2);const int partner[4]={0,1,3,2};for(int arg=3;arg<argc;arg++){int r=std::stoi(argv[arg]);assert(0<=r&&r<n);clock_t t0=clock();auto pair=[&](int j){return 2*(j==0)+(j==r);};Dense P=dense(X[pair(0)][0]),H(P.shift);std::array<Dense,3>channel={dense(X[pair(0)][1]),dense(X[pair(0)][2]),dense(X[pair(0)][3])};for(int j=1;j<n;j++){int p=pair(j);Dense N=mul(P,X[p][0]),K=mul(H,X[p][0]);for(int mu=1;mu<=3;mu++)addmul(K,channel[mu-1],X[p][partner[mu]]);if(j+1<n)for(int mu=1;mu<=3;mu++)channel[mu-1]=mul(P,X[p][mu]);P=std::move(N);H=std::move(K);}Z norm=trace(P),energy=trace(H);for(int mu=1;mu<=3;mu++){Dense seam=dense(X[pair(0)][partner[mu]]);for(int j=1;j<n-1;j++)seam=mul(seam,X[pair(j)][0]);energy+=trprod(seam,X[pair(n-1)][mu]);}std::cout<<"C"<<n<<"_"<<r<<"="<<norm<<"\nK"<<n<<"_"<<r<<"="<<energy<<"\n";std::cout.flush();rusage use;getrusage(RUSAGE_SELF,&use);std::cerr<<"n="<<n<<" r="<<r<<" CPU_seconds="<<double(clock()-t0)/CLOCKS_PER_SEC<<" peak_KiB="<<use.ru_maxrss<<"\n";}rusage use;getrusage(RUSAGE_SELF,&use);std::cerr<<"FINAL CPU_seconds="<<double(clock()-start)/CLOCKS_PER_SEC<<" peak_KiB="<<use.ru_maxrss<<"\n";}
