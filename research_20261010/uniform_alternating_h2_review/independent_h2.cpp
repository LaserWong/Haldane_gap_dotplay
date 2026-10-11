// Independent positive insertion convolution; no producer helper imported.
#define main previous_small_fixture_main
#include "../uniform_alternating_b2_fixture_review/independent.cpp"
#undef main
void h2_guards(int L){const unsigned cap=L==64?13:10;rlimit c,a;getrlimit(RLIMIT_CPU,&c);getrlimit(RLIMIT_AS,&a);test(c.rlim_cur==cap&&c.rlim_max==cap,"H2 CPU cap");test(a.rlim_cur==256ul*1024*1024&&a.rlim_max==a.rlim_cur,"H2 AS cap");cpu_set_t set;CPU_ZERO(&set);test(sched_getaffinity(0,sizeof(set),&set)==0&&CPU_COUNT(&set)==1&&CPU_ISSET(5,&set),"H2 CPU5");struct sigaction action;sigaction(SIGXCPU,nullptr,&action);sigset_t mask;sigprocmask(SIG_BLOCK,nullptr,&mask);test(action.sa_handler==SIG_DFL&&!sigismember(&mask,SIGXCPU),"H2 SIGXCPU");int death;prctl(PR_GET_PDEATHSIG,&death);test(death==SIGKILL,"H2 PDEATHSIG");std::cerr<<"POSTEXEC_GUARDS_PASS CPU="<<cap<<" AS=256MiB CPU5 SIGXCPU=default_unblocked PDEATHSIG9 L="<<L<<"\n";}
int main(int argc,char**argv){try{
 test(argc==4,"arguments: length blocks expected");const int L=std::stoi(argv[1]);test(L==32||L==64,"authorized length");h2_guards(L);const int Nexp=L-3;
 std::ifstream data(argv[2]),expected(argv[3]);int n;data>>n;test(n==11,"block count");I N,H,H2;const int sizes[11]={1,8,32,80,136,162,136,80,32,8,1};
 for(int block=0;block<11;++block){int charge,d;data>>charge>>d;test(charge==2*block-10&&d==sizes[block],"sector identity");M T(d),O(d),U(d),V(d);for(auto*m:{&T,&O,&U,&V})for(auto&x:m->x)data>>x;test(bool(data),"complete blocks");
  M P=T,R=O;int exponent=1,leading=0;while((1<<(leading+1))<=Nexp)++leading;
  for(int bit=leading-1;bit>=0;--bit){M square=times(P,P),doubled=plus(times(P,R),times(R,P));P=std::move(square);R=std::move(doubled);exponent*=2;if((Nexp>>bit)&1){M next=plus(times(P,O),times(R,T));P=times(P,T);R=std::move(next);++exponent;}}
  test(exponent==Nexp,"positive convolution exponent");M Pend=times(P,T),T2=times(T,T);I norm=dottrace(Pend,T2),h=L*dottrace(Pend,O),same=dottrace(Pend,U),adj=dottrace(P,V),disj=dottrace(R,O),h2=L*(same+adj+disj);
  int q;expected>>q;test(q==charge,"checkpoint charge");std::array<I,6>computed={norm,h,h2,same,adj,disj};for(const I&v:computed){I want;expected>>want;test(bool(expected)&&want==v,"independent H2 checkpoint mismatch");}
  N+=norm;H+=h;H2+=h2;std::cout<<"BLOCK_MATCH charge="<<charge<<" side="<<d<<" sign=+1\n";std::cout.flush();
 }
 std::string extra;test(!(data>>extra)&&!(expected>>extra),"trailing data");I var=H2*N-H*H;test(N>0&&H2>=0&&H2<=4*L*L*N&&var>=0,"physical variance and norm bounds");
 std::cout<<"N0_"<<L<<"="<<N<<"\nH0_"<<L<<"="<<H<<"\nH2_"<<L<<"="<<H2<<"\nVARIANCE_NUMERATOR="<<var<<"\nVARIANCE_DENOMINATOR="<<N*N<<"\nINDEPENDENT_H2_ALL_BLOCKS_AND_TOTALS_PASS\n";return 0;
 }catch(const std::exception&e){std::cerr<<"FAIL "<<e.what()<<"\n";return 2;}}
