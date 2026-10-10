// Exact fixed-source contractions with an accumulated open-chain H insertion.
// Q_l = Q_(l-1) E_(l-1) + P_(l-2) O_(l-2,l-1), plus periodic seam separately.
#include <gmpxx.h>
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <cassert>
#include <ctime>
#include <sys/resource.h>
#include <sched.h>
using Z=mpz_class;constexpr int NG=11;int dim[NG];
struct Elt{int j;long v;};
struct Sparse{int shift=0;std::array<std::vector<std::vector<Elt>>,NG>a;};
struct Block{int nr=0,nc=0;std::vector<Z>x;Block()=default;Block(int r,int c):nr(r),nc(c),x(r*c){}};
struct Dense{int shift;std::array<Block,NG>a;explicit Dense(int s):shift(s){for(int g=0;g<NG;g++)if(g+s>=0&&g+s<NG)a[g]=Block(dim[g],dim[g+s]);}};
void addsmall(Z&z,const Z&a,long v){if(v>0)mpz_addmul_ui(z.get_mpz_t(),a.get_mpz_t(),v);else mpz_submul_ui(z.get_mpz_t(),a.get_mpz_t(),-v);}
void addprod(Dense&C,const Dense&A,const Sparse&B){assert(C.shift==A.shift+B.shift);for(int g=0;g<NG;g++){int h=g+A.shift;if(h<0||h>=NG)continue;const auto&a=A.a[g];auto&c=C.a[g];if(!a.nr||!c.nc)continue;for(int i=0;i<a.nr;i++)for(int k=0;k<a.nc;k++)if(a.x[i*a.nc+k]!=0)for(auto&e:B.a[h][k])addsmall(c.x[i*c.nc+e.j],a.x[i*a.nc+k],e.v);}}
Dense mul(const Dense&A,const Sparse&B){Dense C(A.shift+B.shift);addprod(C,A,B);return C;}
Dense identity(){Dense p(0);for(int g=0;g<NG;g++)for(int i=0;i<dim[g];i++)p.a[g].x[i*dim[g]+i]=1;return p;}
Z trace(const Dense&A){assert(A.shift==0);Z z;for(int g=0;g<NG;g++)for(int i=0;i<dim[g];i++)z+=A.a[g].x[i*dim[g]+i];return z;}
Z trprod(const Dense&A,const Sparse&B){assert(A.shift+B.shift==0);Z z;for(int g=0;g<NG;g++){int h=g+A.shift;if(h<0||h>=NG)continue;const auto&a=A.a[g];for(int k=0;k<a.nc;k++)for(auto&e:B.a[h][k])addsmall(z,a.x[e.j*a.nc+k],e.v);}return z;}
int main(int argc,char**argv){if(argc<4)return 2;rlimit mem{700ul*1024*1024,700ul*1024*1024},cpu{600,600};setrlimit(RLIMIT_AS,&mem);setrlimit(RLIMIT_CPU,&cpu);cpu_set_t cp;CPU_ZERO(&cp);sched_getaffinity(0,sizeof(cp),&cp);int last=-1;for(int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&cp))last=i;CPU_ZERO(&cp);CPU_SET(last,&cp);sched_setaffinity(0,sizeof(cp),&cp);clock_t t0=clock();std::ifstream f(argv[1]);int charge;f>>charge;std::array<int,676>group,loc;for(int i=0;i<676;i++){int q;f>>q;group[i]=(q+10)/2;loc[i]=dim[group[i]]++;}std::array<Sparse,4>E;std::array<Sparse,9>O;auto read=[&](Sparse&s,int shift){s.shift=shift;for(int g=0;g<NG;g++)s.a[g].resize(dim[g]);int nz;f>>nz;for(int k=0;k<nz;k++){int i,j;long v;f>>i>>j>>v;assert(group[j]-group[i]==shift);s.a[group[i]][loc[i]].push_back({loc[j],v});}};for(int a=0;a<2;a++)for(int b=0;b<2;b++)read(E[2*a+b],charge*(b-a));for(int a=0;a<3;a++)for(int b=0;b<3;b++)read(O[3*a+b],charge*((b!=0)-(a!=0)));assert(f.good());int n=std::stoi(argv[2]);assert(n>=2);for(int arg=3;arg<argc;arg++){int r=std::stoi(argv[arg]);assert(r>=0&&r<n);clock_t tr=clock();auto site=[&](int j)->const Sparse&{return E[2*(j==0)+(j==r)];};auto bond=[&](int j,int k)->const Sparse&{int a=j==0?1:(k==0?2:0),b=j==r?1:(k==r?2:0);return O[3*a+b];};Dense pprev=identity(),p=mul(pprev,site(0)),q(p.shift);for(int j=1;j<n;j++){Dense pn=mul(p,site(j)),qn=mul(q,site(j));addprod(qn,pprev,bond(j-1,j));pprev=std::move(p);p=std::move(pn);q=std::move(qn);}Z C=trace(p),K=trace(q);Dense middle=identity();for(int j=1;j<n-1;j++)middle=mul(middle,site(j));K+=trprod(middle,bond(n-1,0));std::cout<<"C"<<n<<"_"<<r<<"="<<C<<"\nK"<<n<<"_"<<r<<"="<<K<<"\n";std::cout.flush();rusage u;getrusage(RUSAGE_SELF,&u);std::cerr<<"n="<<n<<" r="<<r<<" CPU_seconds="<<double(clock()-tr)/CLOCKS_PER_SEC<<" peak_KiB="<<u.ru_maxrss<<"\n";}rusage u;getrusage(RUSAGE_SELF,&u);std::cerr<<"FINAL CPU_seconds="<<double(clock()-t0)/CLOCKS_PER_SEC<<" peak_KiB="<<u.ru_maxrss<<"\n";}
