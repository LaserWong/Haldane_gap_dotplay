// Independent global-index cell contraction. No prefix cache; seam is three
// separate complete operator chains, not the producer's carried head channels.
#include <gmpxx.h>
#include <vector>
#include <array>
#include <fstream>
#include <iostream>
#include <cassert>
#include <ctime>
#include <sys/resource.h>
#include <sched.h>
#include <algorithm>
using Z=mpz_class;const int D=676;
struct Entry{int col;long value;};
struct Sparse{int shift;std::vector<std::vector<Entry>> rows;Sparse():rows(D){}};
struct Dense{int shift;std::vector<Z>x;explicit Dense(int s=0):shift(s),x(D*D){}};
struct Cell{int length;std::array<Sparse,8>ops;};
std::vector<int>charges;std::array<std::vector<int>,11>groups;
void add(Dense&C,const Dense&A,const Sparse&B){assert(C.shift==A.shift+B.shift);for(int i=0;i<D;i++){int g=(charges[i]+10)/2+A.shift;if(g<0||g>=11)continue;for(int k:groups[g]){const Z&z=A.x[i*D+k];if(z==0)continue;for(auto&e:B.rows[k]){if(e.value>0)mpz_addmul_ui(C.x[i*D+e.col].get_mpz_t(),z.get_mpz_t(),e.value);else mpz_submul_ui(C.x[i*D+e.col].get_mpz_t(),z.get_mpz_t(),-e.value);}}}}
Dense multiply(const Dense&A,const Sparse&B){Dense C(A.shift+B.shift);add(C,A,B);return C;}
Dense from(const Sparse&A){Dense B(A.shift);for(int i=0;i<D;i++)for(auto&e:A.rows[i])B.x[i*D+e.col]=e.value;return B;}
Z trace(const Dense&A){assert(A.shift==0);Z z;for(int i=0;i<D;i++)z+=A.x[i*D+i];return z;}
Z trprod(const Dense&A,const Sparse&B){assert(A.shift+B.shift==0);Z z;for(int i=0;i<D;i++)for(auto&e:B.rows[i])z+=A.x[e.col*D+i]*e.value;return z;}
// Independently partition physical source intervals after moving a wrapping
// current to the beginning of the cyclic word.
std::vector<int> partition(int n,bool mixed,int r){
 int cut=(r==n-1)?r:0,bra=(n-cut)%n,ket=(r-cut+n)%n;
 int blen=mixed?1:2;assert(bra+blen<=n&&ket+2<=n);
 std::vector<int>seq;int pos=0;
 while(pos<n){
  if(pos!=bra&&pos!=ket){seq.push_back(0);pos++;continue;}
  bool overlap=std::max(bra,ket)<std::min(bra+blen,ket+2);
  if(overlap){
   int start=std::min(bra,ket),end=std::max(bra+blen,ket+2);assert(pos==start);
   int id;
   if(mixed){assert(end-start==2);id=bra==start?5:6;}
   else{id=bra==ket?4:(bra<ket?7:8);}
   seq.push_back(id);pos=end;
  }else if(pos==bra){seq.push_back(mixed?1:2);pos+=blen;}
  else{seq.push_back(3);pos+=2;}
 }
 return seq;
}
int main(int argc,char**argv){assert(argc>=4&&sizeof(long)>=8);rlimit mem{700ul*1024*1024,700ul*1024*1024},cpu{2400,2400};setrlimit(RLIMIT_AS,&mem);setrlimit(RLIMIT_CPU,&cpu);cpu_set_t a;CPU_ZERO(&a);sched_getaffinity(0,sizeof(a),&a);int c=0;while(!CPU_ISSET(c,&a))c++;CPU_ZERO(&a);CPU_SET(c,&a);sched_setaffinity(0,sizeof(a),&a);clock_t start=clock();std::ifstream f(argv[1]);charges.resize(D);for(int i=0;i<D;i++){f>>charges[i];groups[(charges[i]+10)/2].push_back(i);}int count;f>>count;assert(count==9);std::vector<Cell>cells(count);for(int k=0;k<count;k++){int id;f>>id>>cells[k].length;assert(id==k);for(auto&op:cells[k].ops){int nz;f>>op.shift>>nz;while(nz--){int i,j;long value;f>>i>>j>>value;assert(f.good()&&charges[j]-charges[i]==2*op.shift);op.rows[i].push_back({j,value});}}}int n=std::stoi(argv[2]);assert(n>=4);const int last[3]={5,6,7},first_partner[3]={2,4,3};
 for(int arg=3;arg<argc;arg++){
  std::string token=argv[arg];auto split=token.find(':');assert(split!=std::string::npos);std::string kind=token.substr(0,split);assert(kind=="mix"||kind=="jj");int r=std::stoi(token.substr(split+1));assert(r>=0&&r<n);clock_t t=clock();auto seq=partition(n,kind=="mix",r);int len=0;for(int x:seq)len+=cells[x].length;assert(len==n&&seq.size()>=2);
  const auto&first=cells[seq[0]];Dense P=from(first.ops[0]),H=from(first.ops[1]);std::array<Dense,3>tail={from(first.ops[5]),from(first.ops[6]),from(first.ops[7])};
  for(size_t j=1;j<seq.size();j++){
   const auto&next=cells[seq[j]];Dense N=multiply(P,next.ops[0]),Q=multiply(H,next.ops[0]);add(Q,P,next.ops[1]);for(int mu=0;mu<3;mu++)add(Q,tail[mu],next.ops[first_partner[mu]]);if(j+1<seq.size())for(int mu=0;mu<3;mu++)tail[mu]=multiply(P,next.ops[last[mu]]);P=std::move(N);H=std::move(Q);
  }
  Z norm=trace(P),energy=trace(H);
  for(int mu=0;mu<3;mu++){
   Dense seam=from(first.ops[first_partner[mu]]);for(size_t j=1;j+1<seq.size();j++)seam=multiply(seam,cells[seq[j]].ops[0]);energy+=trprod(seam,cells[seq.back()].ops[last[mu]]);
  }
  std::cout<<"C_"<<kind<<"_"<<n<<"_"<<r<<"="<<norm<<"\nK_"<<kind<<"_"<<n<<"_"<<r<<"="<<energy<<"\n";std::cout.flush();rusage use;getrusage(RUSAGE_SELF,&use);std::cerr<<"n="<<n<<" case="<<token<<" CPU_seconds="<<double(clock()-t)/CLOCKS_PER_SEC<<" peak_KiB="<<use.ru_maxrss<<"\n";
 }
 rusage use;getrusage(RUSAGE_SELF,&use);std::cerr<<"FINAL CPU_seconds="<<double(clock()-start)/CLOCKS_PER_SEC<<" peak_KiB="<<use.ru_maxrss<<"\n";
}
