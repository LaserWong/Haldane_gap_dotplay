#include <gmpxx.h>
#include <vector>
#include <array>
#include <map>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <sys/resource.h>
#include <sys/prctl.h>
#include <sched.h>
#include <signal.h>
using I=mpz_class;
void test(bool p,const char *s){if(!p)throw std::runtime_error(s);}
struct M {int n;std::vector<I>x;M(int n_=0):n(n_),x(n_*n_){} I&operator()(int i,int j){return x[i*n+j];}const I&operator()(int i,int j)const{return x[i*n+j];}};
M identity(int n){M a(n);for(int i=0;i<n;++i)a(i,i)=1;return a;}
M times(const M&a,const M&b){test(a.n==b.n,"dimension");M c(a.n);for(int i=0;i<a.n;++i)for(int k=0;k<a.n;++k)if(a(i,k)!=0)for(int j=0;j<a.n;++j)if(b(k,j)!=0)mpz_addmul(c(i,j).get_mpz_t(),a(i,k).get_mpz_t(),b(k,j).get_mpz_t());return c;}
M plus(const M&a,const M&b,int sign=1){M c(a.n);for(size_t i=0;i<a.x.size();++i)c.x[i]=a.x[i]+sign*b.x[i];return c;}
I trace(const M&a){I s;for(int i=0;i<a.n;++i)s+=a(i,i);return s;}
I dottrace(const M&a,const M&b){I s;for(int i=0;i<a.n;++i)for(int j=0;j<a.n;++j)mpz_addmul(s.get_mpz_t(),a(i,j).get_mpz_t(),b(j,i).get_mpz_t());return s;}
using Tensor=std::array<M,3>;
std::vector<int> charges;
Tensor tensor26(){
 const int ell[8]={1,1,1,1,3,3,3,5},diag[8]={-289,-84,-9,33,-22,27,71,-11};
 const int p[4][3]={{-11,-35,-28},{-23,16,-49},{-6,-25,-20},{-34,9,-32}};
 const int q[3]={1,2,-16};
 std::vector<std::pair<int,int>> labels;for(int a=0;a<8;++a)for(int m=-ell[a];m<=ell[a];m+=2)labels.push_back({a,m});
 Tensor A={M(26),M(26),M(26)};for(auto[a,m]:labels)charges.push_back(m);
 auto coeff=[&](int a,int b){if(a<4&&b>=4&&b<7)return p[a][b-4];if(a>=4&&a<7&&b==7)return q[a-4];return 0;};
 for(int s=-1;s<=1;++s)for(int i=0;i<26;++i)for(int j=0;j<26;++j){auto[a,m]=labels[i];auto[b,k]=labels[j];if(k!=m+2*s)continue;int l=ell[a],r=(l+m)/2,v=0;
  if(a==b)v=diag[a]*(s==0?m:(s==-1?2*(l-r+1):-(r+1)));
  else if(ell[b]==l+2)v=coeff(a,b)*(s==0?2*(r+1)*(l-r+1):(s==-1?2*(l-r+1)*(l-r+2):(r+1)*(r+2)));
  else if(ell[b]==l-2)v=-coeff(b,a)*(s==0?-2:(s==-1?2:1));
  A[s+1](i,j)=v;
 }
 return A;
}
M heisenberg(){M h(9);for(int a=0;a<3;++a)for(int b=0;b<3;++b){int ket=3*a+b;h(ket,ket)=(a-1)*(b-1);if(a<2&&b>0)h(ket+2,ket)=1;if(a>0&&b<2)h(ket-2,ket)=1;}return h;}
std::array<M,4> local_ops(){M h=heisenberg(),u=times(h,h),l(27),r(27);for(int a=0;a<27;++a)for(int b=0;b<27;++b){if(a%3==b%3)l(a,b)=h(a/3,b/3);if(a/9==b/9)r(a,b)=h(a%9,b%9);}M v=plus(times(l,r),times(r,l));M hplus2=h,hplus1=h,hminus1=h;for(int i=0;i<9;++i){hplus2(i,i)+=2;hplus1(i,i)+=1;hminus1(i,i)-=1;}for(auto&x:times(times(hplus2,hplus1),hminus1).x)test(x==0,"spin-one eigenvalue polynomial");
 for(auto*o:{&h,&u,&v})for(int i=0;i<o->n;++i)for(int j=0;j<o->n;++j){test((*o)(i,j)==(*o)(j,i),"Hermiticity");if((*o)(i,j)!=0){int a=i,b=j,s=0,t=0;do{s+=a%3;t+=b%3;a/=3;b/=3;}while(a||b);test(s==t,"physical charge conservation");}}
 return {identity(3),h,u,v};}
std::array<std::vector<M>,4> make_words(const Tensor&A){std::array<std::vector<M>,4>w;w[0].push_back(identity(A[0].n));for(int k=1;k<=3;++k)for(int s=0;s<3;++s)for(const auto&b:w[k-1])w[k].push_back(times(A[s],b));return w;}
M insertion(const std::vector<std::pair<int,int>>&ids,const std::vector<M>&w,const M&o){M c(ids.size());for(int s=0;s<o.n;++s)for(int t=0;t<o.n;++t)if(o(s,t)!=0)for(int row=0;row<c.n;++row){auto[i,j]=ids[row];for(int col=0;col<c.n;++col){auto[k,l]=ids[col];if(w[t](i,k)!=0&&w[s](j,l)!=0)c(row,col)+=o(s,t)*w[t](i,k)*w[s](j,l);}}return c;}
struct Values{I n,h,h2,b2,mean,same,adj,disj,omitclosing;};
I dot(const std::vector<I>&a,const std::vector<I>&b){I z;for(size_t i=0;i<a.size();++i)z+=a[i]*b[i];return z;}
Values physical(const std::array<std::vector<M>,4>&w,int L){int half=L/2,k=w[half].size(),dim=k*k;std::vector<I>psi(dim);for(int a=0;a<k;++a)for(int b=0;b<k;++b)psi[a*k+b]=dottrace(w[half][a],w[half][b]);
 std::vector<int>place(L,1);for(int j=L-2;j>=0;--j)place[j]=3*place[j+1];M h=heisenberg();std::vector<std::vector<I>>hp(L,std::vector<I>(dim));
 for(int j=0;j<L;++j)for(int x=0;x<dim;++x){int t=(j+1)%L,a=x/place[j]%3,b=x/place[t]%3,ket=3*a+b;for(int bra=0;bra<9;++bra)if(h(bra,ket)!=0){int y=x+(bra/3-a)*place[j]+(bra%3-b)*place[t];hp[j][y]+=h(bra,ket)*psi[x];}}
 std::vector<I>hv(dim),bv(dim),bc(dim);for(int j=0;j<L;++j)for(int x=0;x<dim;++x){hv[x]+=hp[j][x];bv[x]+=(j%2?-1:1)*hp[j][x];if(j<L-1)bc[x]+=(j%2?-1:1)*hp[j][x];}
 Values z;z.n=dot(psi,psi);z.h=dot(psi,hv);z.h2=dot(hv,hv);z.b2=dot(bv,bv);z.mean=dot(psi,bv);z.omitclosing=dot(bc,bc);z.same=dot(hp[0],hp[0]);z.adj=dot(hp[0],hp[1])+dot(hp[0],hp[L-1]);for(int r=2;r<=L-2;++r)z.disj+=(r%2?-1:1)*dot(hp[0],hp[r]);test(z.mean==0&&z.n>0&&z.h2*z.n>=z.h*z.h,"physical positivity or translation");test(z.b2==L*(z.same-z.adj+z.disj),"direct bond decomposition");return z;}
void read_equal(std::ifstream&f,const M&m){for(const I&v:m.x){I x;f>>x;test(bool(f)&&x==v,"saved block entry mismatch");}}
std::map<int,Values> transfer(const Tensor&A,const std::array<std::vector<M>,4>&w,const std::array<M,4>&ops,bool d26,std::ifstream*saved,std::ifstream*pinned){
 std::map<int,std::vector<std::pair<int,int>>>sectors;for(int i=0;i<A[0].n;++i)for(int j=0;j<A[0].n;++j)sectors[d26?charges[i]-charges[j]:0].push_back({i,j});
 if(d26){int n,m;*saved>>n;*pinned>>m;test(n==11&&m==11,"block count");}
 std::map<int,Values>res;for(auto&[q,ids]:sectors){M T=insertion(ids,w[1],ops[0]),O=insertion(ids,w[2],ops[1]),U=insertion(ids,w[2],ops[2]),V=insertion(ids,w[3],ops[3]);
  if(d26){int r,n,s,m;*saved>>r>>n;*pinned>>s>>m;test(q==r&&q==s&&n==int(ids.size())&&m==n,"sector labels");for(auto*x:{&T,&O,&U,&V})read_equal(*saved,*x);for(auto*x:{&T,&O})read_equal(*pinned,*x);}
  std::vector<M>pow={identity(T.n),T};for(int i=2;i<=4;++i)pow.push_back(times(pow.back(),T));
  M OO=times(O,O),OT=times(O,T);I disjplus=2*dottrace(OO,pow[2])+dottrace(OT,OT),disjminus=2*dottrace(OO,pow[2])-dottrace(OT,OT);
  for(int L:{4,6}){Values&v=res[L];v.n+=L==4?trace(pow[4]):dottrace(pow[4],pow[2]);v.h+=L*dottrace(O,pow[L-2]);I same=dottrace(U,pow[L-2]),adj=dottrace(V,pow[L-3]),dm=L==4?trace(OO):disjminus,dp=L==4?trace(OO):disjplus;v.same+=same;v.adj+=adj;v.disj+=dm;v.b2+=L*(same-adj+dm);v.h2+=L*(same+adj+dp);}
  std::cerr<<"REBUILT sector="<<q<<" dimension="<<ids.size()<<"\n";
 }
 if(d26){std::string extra;test(!(*saved>>extra)&&!(*pinned>>extra),"unexpected trailing block data");}return res;
}
void signed_power_test(){M T(2),O(2);T.x={2,1,3,-1};O.x={1,2,-1,0};for(int sign:{-1,1}){M K(4),literal=identity(4),p=identity(2),r(2);for(int i=0;i<2;++i)for(int j=0;j<2;++j){K(i,j)=T(i,j);K(i,j+2)=O(i,j);K(i+2,j+2)=sign*T(i,j);}for(int n=0;n<=12;++n){for(int i=0;i<2;++i)for(int j=0;j<2;++j)test(literal(i,j+2)==r(i,j)&&literal(i,j)==p(i,j)&&literal(i+2,j+2)==((sign==-1&&n%2)?-p(i,j):p(i,j)),"signed block power");r=plus(times(p,O),times(r,T),sign);p=times(p,T);literal=times(literal,K);}}}
void guards(){rlimit c,a;getrlimit(RLIMIT_CPU,&c);getrlimit(RLIMIT_AS,&a);test(c.rlim_cur==24&&c.rlim_max==24,"CPU limit");test(a.rlim_cur==256ul*1024*1024&&a.rlim_max==a.rlim_cur,"AS limit");cpu_set_t set;CPU_ZERO(&set);test(sched_getaffinity(0,sizeof(set),&set)==0&&CPU_COUNT(&set)==1&&CPU_ISSET(5,&set),"CPU5 affinity");struct sigaction action;sigaction(SIGXCPU,nullptr,&action);sigset_t mask;sigprocmask(SIG_BLOCK,nullptr,&mask);test(action.sa_handler==SIG_DFL&&!sigismember(&mask,SIGXCPU),"SIGXCPU disposition");int p;prctl(PR_GET_PDEATHSIG,&p);test(p==SIGKILL,"parent death guard");std::cerr<<"POSTEXEC_GUARDS_PASS CPU=24 AS=256MiB CPU5 SIGXCPU=default,unblocked PDEATHSIG=9\n";}
int main(int argc,char**argv){try{guards();test(argc==3,"arguments");signed_power_test();auto ops=local_ops();Tensor A=tensor26();std::ifstream saved(argv[1]),pinned(argv[2]);test(bool(saved)&&bool(pinned),"open inputs");std::array<bool,8>mutations{};for(int family=0;family<3;++family){if(family){A={M(2),M(2),M(2)};if(family==1){A[0].x={1,2,0,1};A[1].x={2,0,1,-1};A[2].x={0,1,-2,2};}else{A[0].x={2,-1,1,0};A[1].x={1,1,0,2};A[2].x={0,2,1,-1};}}auto w=make_words(A);auto got=transfer(A,w,ops,family==0,&saved,&pinned);for(int L:{4,6}){auto ref=physical(w,L),z=got[L];test(ref.n==z.n&&ref.h==z.h&&ref.h2==z.h2&&ref.b2==z.b2,"full physical moment mismatch");test(ref.same==z.same&&ref.adj==z.adj&&ref.disj==z.disj,"overlap groups mismatch");mutations[0]|=z.b2!=L*z.b2;mutations[1]|=z.b2!=z.b2/L;mutations[2]|=z.b2*z.n!=z.b2;mutations[3]|=z.b2+2*L*z.adj!=z.b2;mutations[4]|=z.b2+L*z.adj!=z.b2;mutations[5]|=z.b2-L*z.disj!=z.b2;mutations[6]|=ref.omitclosing!=ref.b2;mutations[7]|=L*(z.same-2*z.disj+z.disj)!=z.b2;std::cout<<"CASE "<<(family==0?"D26":family==1?"D2":"D2_extra")<<" L="<<L<<"\nN="<<z.n<<"\nH="<<z.h<<"\nH2="<<z.h2<<"\nB2="<<z.b2<<"\nSAME="<<z.same<<"\nADJ="<<z.adj<<"\nDISJ="<<z.disj<<"\nSTAGGERED_MEAN="<<ref.mean<<"\nPASS\n";}}
 for(bool m:mutations)test(m,"mutation survived");std::cout<<"ALL_SAVED_ENTRIES_REBUILT=PASS\nSIGNED_POWER_CHECKS=26\nPHYSICAL_MUTATIONS=8\nINDEPENDENT_REVIEW_PASS\n";return 0;}catch(const std::exception&e){std::cerr<<"FAIL "<<e.what()<<"\n";return 2;}}
