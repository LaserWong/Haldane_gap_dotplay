// Authorized length64-only positive-convolution H² wrapper.
#define main frozen_fixture_main
#include "../uniform_alternating_b2_fixture/fixture.cpp"
#undef main
#include <filesystem>
constexpr int LENGTH=64;
constexpr int CONVOLUTION_POWER=LENGTH-3;
constexpr int CONVOLUTION_SIGN=1;
constexpr int CHILD_CPU_CAP=39;
constexpr int H_NORM=2*LENGTH;
const std::array<int,11> BLOCK_SIDES={1,8,32,80,136,162,136,80,32,8,1};
void wrapper_guard(){
 rlimit c,m;getrlimit(RLIMIT_CPU,&c);getrlimit(RLIMIT_AS,&m);
 require(c.rlim_cur==CHILD_CPU_CAP&&c.rlim_max==CHILD_CPU_CAP,"H2 CPU cap");
 require(m.rlim_cur==256ul*1024*1024&&m.rlim_max==m.rlim_cur,"H2 memory cap");
 cpu_set_t s;CPU_ZERO(&s);require(sched_getaffinity(0,sizeof(s),&s)==0&&CPU_COUNT(&s)==1&&CPU_ISSET(4,&s),"H2 CPU4 affinity");
 struct sigaction a;sigaction(SIGXCPU,nullptr,&a);sigset_t b;sigprocmask(SIG_BLOCK,nullptr,&b);
 require(a.sa_handler==SIG_DFL&&!sigismember(&b,SIGXCPU),"H2 SIGXCPU");
 int pd;prctl(PR_GET_PDEATHSIG,&pd);require(pd==SIGKILL,"H2 parent death");
 require(LENGTH==64&&CONVOLUTION_SIGN==1,"authorized length/sign scope");
 std::cerr<<"GUARDS CPU="<<CHILD_CPU_CAP<<" AS=256MiB AFFINITY=4 LENGTH="<<LENGTH<<" CONV="<<CONVOLUTION_POWER<<" SIGN="<<CONVOLUTION_SIGN<<"\n";
}
size_t maxbits(const Mat&A){size_t n=0;for(auto&z:A.a)n=std::max(n,mpz_sizeinbase(z.get_mpz_t(),2));return n;}
int main(int argc,char**argv){try{
 wrapper_guard();require(argc==5,"arguments blocks anchors expected-checkpoints output-directory");
 const std::string nk="N0_"+std::to_string(LENGTH)+"=",hk="H0_"+std::to_string(LENGTH)+"=";
 std::ifstream anc(argv[2]);require((bool)anc,"accepted anchor input");Z wantN,wantH;bool hn=false,hh=false;std::string line;
 while(std::getline(anc,line)){
  if(line.rfind(nk,0)==0){wantN=Z(line.substr(nk.size()));hn=true;}
  if(line.rfind(hk,0)==0){wantH=Z(line.substr(hk.size()));hh=true;}
 }
 require(hn&&hh&&wantN>0,"accepted length64 keys");
 std::ifstream in(argv[1]),expected(argv[3]);int nb,ne;in>>nb;expected>>ne;
 require((bool)in&&(bool)expected&&nb==11&&ne==nb,"complete local and expected blocks");Z N,H,H2;
 for(int k=0;k<nb;k++){
  int q,d;in>>q>>d;require(q==-10+2*k&&d==BLOCK_SIDES.at(k),"ordered block identity");
  int ek,eq,ed;Z en,eh,esame,eadj;expected>>ek>>eq>>ed>>en>>eh>>esame>>eadj;
  require((bool)expected&&ek==k&&eq==q&&ed==d,"expected checkpoint identity");
  Mat T(d),O(d),U(d),V(d);for(auto&A:{&T,&O,&U,&V})for(auto&z:A->a)in>>z;
  require((bool)in,"complete local block");double before=double(clock())/CLOCKS_PER_SEC;
  auto K=bpower(T,O,CONVOLUTION_POWER,CONVOLUTION_SIGN);require(K.sg==1,"positive final block sign");
  Mat Pnext=mul(K.p,T),T2=mul(T,T);
  Z dn=trprod(Pnext,T2),dh=LENGTH*trprod(Pnext,O);
  Z same=trprod(Pnext,U),adj=trprod(K.p,V),disj=trprod(K.r,O);
  require(dn==en&&dh==eh&&same==esame&&adj==eadj,"mandatory per-block N/H/same/adjacent match");
  Z dH2=LENGTH*(same+adj+disj);N+=dn;H+=dh;H2+=dH2;
  auto cp=std::filesystem::path(argv[4])/("checkpoint_"+std::to_string(k)+".json");
  require(!std::filesystem::exists(cp),"existing checkpoint");std::ofstream out(cp);
  out<<"{\n  \"physical_length\": "<<LENGTH<<",\n  \"block_index\": "<<k<<",\n  \"charge\": "<<q<<",\n  \"side\": "<<d<<",\n  \"norm_contribution\": \""<<dn<<"\",\n  \"H_contribution\": \""<<dh<<"\",\n  \"H2_contribution\": \""<<dH2<<"\",\n  \"same_bond\": \""<<same<<"\",\n  \"adjacent_symmetric\": \""<<adj<<"\",\n  \"positive_disjoint\": \""<<disj<<"\",\n  \"positive_convolution_sign\": "<<CONVOLUTION_SIGN<<",\n  \"all_four_old_checkpoint_fields_match\": true,\n  \"power_max_bits\": "<<maxbits(K.p)<<",\n  \"convolution_max_bits\": "<<maxbits(K.r)<<",\n  \"cpu_seconds_cumulative\": "<<double(clock())/CLOCKS_PER_SEC<<"\n}\n";
  out.close();require((bool)out,"checkpoint write");
  std::cerr<<"block="<<q<<" side="<<d<<" cpu_delta="<<double(clock())/CLOCKS_PER_SEC-before<<" cpu_total="<<double(clock())/CLOCKS_PER_SEC<<"\n";
 }
 std::string extra;require(!(in>>extra)&&!(expected>>extra),"trailing input");
 require(N==wantN&&H==wantH,"mandatory exact N0_64/H0_64 agreement");
 Z varianceNumerator=H2*N-H*H;
 require(H2>=0&&H2<=N*H_NORM*H_NORM&&varianceNumerator>=0,"physical H2 norm/variance bound");
 std::cout<<nk<<N<<"\n"<<hk<<H<<"\nH2_"<<LENGTH<<"="<<H2<<"\nVARIANCE_NUMERATOR="<<varianceNumerator<<"\nVARIANCE_DENOMINATOR="<<N*N<<"\nEXACT_N0_H0_AGREEMENT=PASS\nALL_SAME_ADJACENT_CHECKPOINTS=PASS\nL64_H2_ONLY_PASS\n";
 rusage u;getrusage(RUSAGE_SELF,&u);std::cerr<<"FINAL cpu="<<double(clock())/CLOCKS_PER_SEC<<" rss_kib="<<u.ru_maxrss<<" matrix_multiplications="<<muls<<"\n";return 0;
}catch(const std::exception&e){std::cerr<<"FAILED "<<e.what()<<" cpu="<<double(clock())/CLOCKS_PER_SEC<<"\n";return 2;}}
