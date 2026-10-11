// Authorized corrected L32-only wrapper. Matrix/convolution kernel is unchanged.
#define main frozen_fixture_main
#include "../uniform_alternating_b2_fixture/fixture.cpp"
#undef main
#include <filesystem>
constexpr int LENGTH=32;
constexpr int CONVOLUTION_POWER=LENGTH-3;
constexpr int CHILD_CPU_CAP=25;
constexpr int B_NORM=3*LENGTH/2;
const std::array<int,11> BLOCK_SIDES={1,8,32,80,136,162,136,80,32,8,1};
void wrapper_guard(){
 rlimit c,m; getrlimit(RLIMIT_CPU,&c); getrlimit(RLIMIT_AS,&m);
 require(c.rlim_cur==CHILD_CPU_CAP&&c.rlim_max==CHILD_CPU_CAP,"corrected32 CPU cap");
 require(m.rlim_cur==256ul*1024*1024&&m.rlim_max==m.rlim_cur,"corrected32 memory cap");
 cpu_set_t s;CPU_ZERO(&s);require(sched_getaffinity(0,sizeof(s),&s)==0&&CPU_COUNT(&s)==1&&CPU_ISSET(4,&s),"corrected32 CPU4 affinity");
 struct sigaction a;sigaction(SIGXCPU,nullptr,&a);sigset_t b;sigprocmask(SIG_BLOCK,nullptr,&b);
 require(a.sa_handler==SIG_DFL&&!sigismember(&b,SIGXCPU),"corrected32 SIGXCPU");
 int pd;prctl(PR_GET_PDEATHSIG,&pd);require(pd==SIGKILL,"corrected32 parent death");
 std::cerr<<"GUARDS CPU="<<CHILD_CPU_CAP<<" AS=256MiB AFFINITY=4 LENGTH="<<LENGTH<<" CONV="<<CONVOLUTION_POWER<<"\n";
}
size_t maxbits(const Mat&A){size_t n=0;for(auto&z:A.a)n=std::max(n,mpz_sizeinbase(z.get_mpz_t(),2));return n;}
int main(int argc,char**argv){try{
 wrapper_guard();require(argc==4,"arguments blocks anchors output-directory");
 const std::string nk="N0_"+std::to_string(LENGTH)+"=", hk="H0_"+std::to_string(LENGTH)+"=";
 std::ifstream anc(argv[2]);require((bool)anc,"accepted anchor input");Z wantN,wantH;bool hn=false,hh=false;std::string line;
 while(std::getline(anc,line)){
  if(line.rfind(nk,0)==0){wantN=Z(line.substr(nk.size()));hn=true;}
  if(line.rfind(hk,0)==0){wantH=Z(line.substr(hk.size()));hh=true;}
 }
 require(hn&&hh&&wantN>0,"accepted32 keys");
 std::ifstream in(argv[1]);int nb;in>>nb;require((bool)in&&nb==11,"all local blocks");Z N,H,B2;
 for(int k=0;k<nb;k++){
  int q,d;in>>q>>d;require(q==-10+2*k&&d==BLOCK_SIDES.at(k),"ordered block identity");
  Mat T(d),O(d),U(d),V(d);for(auto&A:{&T,&O,&U,&V})for(auto&z:A->a)in>>z;require((bool)in,"complete block");
  double before=double(clock())/CLOCKS_PER_SEC;
  // This is exactly the shared, fixture-tested signed block power.
  auto K=bpower(T,O,CONVOLUTION_POWER,-1);require(K.sg==-1,"odd final convolution power");
  Mat Pnext=mul(K.p,T),T2=mul(T,T);
  Z dn=trprod(Pnext,T2),dh=LENGTH*trprod(Pnext,O);
  Z same=trprod(Pnext,U),adj=trprod(K.p,V),disj=trprod(K.r,O);
  Z db=LENGTH*(same-adj+disj);N+=dn;H+=dh;B2+=db;
  auto cp=std::filesystem::path(argv[3])/("checkpoint_"+std::to_string(k)+".json");require(!std::filesystem::exists(cp),"existing checkpoint");
  std::ofstream out(cp);
  out<<"{\n  \"block_index\": "<<k<<",\n  \"charge\": "<<q<<",\n  \"side\": "<<d<<",\n  \"norm_contribution\": \""<<dn<<"\",\n  \"H_contribution\": \""<<dh<<"\",\n  \"B2_contribution\": \""<<db<<"\",\n  \"same_bond\": \""<<same<<"\",\n  \"adjacent_symmetric\": \""<<adj<<"\",\n  \"alternating_disjoint\": \""<<disj<<"\",\n  \"power_max_bits\": "<<maxbits(K.p)<<",\n  \"convolution_max_bits\": "<<maxbits(K.r)<<",\n  \"cpu_seconds_cumulative\": "<<double(clock())/CLOCKS_PER_SEC<<"\n}\n";
  out.close();require((bool)out,"checkpoint write");
  std::cerr<<"block="<<q<<" side="<<d<<" cpu_delta="<<double(clock())/CLOCKS_PER_SEC-before<<" cpu_total="<<double(clock())/CLOCKS_PER_SEC<<"\n";
 }
 std::string extra;require(!(in>>extra),"trailing input");
 require(N==wantN&&H==wantH,"mandatory exact N0_32/H0_32 agreement");
 require(B2>=0&&B2<=N*B_NORM*B_NORM,"physical B2 norm bound");
 std::cout<<nk<<N<<"\n"<<hk<<H<<"\nB2_"<<LENGTH<<"="<<B2<<"\nB2_NORMALIZING_B_SQUARED="<<B_NORM*B_NORM<<"\nEXACT_N0_H0_AGREEMENT=PASS\nL32_B2_ONLY_PASS\n";
 rusage u;getrusage(RUSAGE_SELF,&u);std::cerr<<"FINAL cpu="<<double(clock())/CLOCKS_PER_SEC<<" rss_kib="<<u.ru_maxrss<<" matrix_multiplications="<<muls<<"\n";return 0;
}catch(const std::exception&e){std::cerr<<"FAILED "<<e.what()<<" cpu="<<double(clock())/CLOCKS_PER_SEC<<"\n";return 2;}}
