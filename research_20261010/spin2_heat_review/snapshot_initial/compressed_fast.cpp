// Audited bounded benchmark: exact spin2 heat columns over Z[sqrt(6),omega].
// Fixed beta=8, P=(64-b8*L/8-H)/64, mu=256, Q=2^56.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <climits>
#include <cmath>
#include <ctime>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#include <gmpxx.h>
using i64=int64_t;using i128=__int128_t;using u128=__uint128_t;
struct Edge{int source,a,b,c,d;};
struct Rep{int index,code,mult;};
std::string dec(i128 x){bool neg=x<0;u128 z=neg?-x:x;std::string s;if(!z)return "0";while(z){s.push_back('0'+z%10);z/=10;}if(neg)s.push_back('-');std::reverse(s.begin(),s.end());return s;}
template<int Bits> i64 floorpow(i128 x){return i64(x>>Bits);}
std::vector<int> decode(int code,int n){std::vector<int>w(n);for(int k=n-1;k>=0;--k){w[k]=code%5-2;code/=5;}return w;}
int encode(const std::vector<int>&w){int c=0;for(int x:w)c=5*c+x+2;return c;}
std::set<int> orbit(const std::vector<int>&w,int m){std::set<int>o;int n=w.size();for(int f=0;f<(m==0?2:1);++f)for(int r=0;r<2;++r)for(int t=0;t<n;++t){int c=0;for(int k=0;k<n;++k)c=5*c+(f?-1:1)*w[r?(t-k+n)%n:(t+k)%n]+2;o.insert(c);}return o;}

// Compressed parity basis, exact split fixed-point matvec, and column blocking.
// C++20 signed right shift is arithmetic. These identities are also checked below.
static_assert((-1 >> 8)==-1 && (-1 & 255)==255 && (i128(-1)>>56)==-1);
template<int N>struct CEdge{int source;std::array<int16_t,2*N> c;};
template<int Bits,int N,int B>void split_apply(const std::vector<int>&off,const std::vector<CEdge<N>>&edges,const std::vector<std::array<i64,N*B>>&cur,std::vector<std::array<i64,N*B>>&next,const std::vector<std::array<i64,N*B>>&prev,const std::array<int,B>&par,bool twice){
 const i64 mask=(i64(1)<<Bits)-1;int d=off.size()-1;
 for(int i=0;i<d;++i){std::array<i64,N*B>hi{},lo{};
  for(int p=off[i];p<off[i+1];++p){const auto&e=edges[p];const auto&x=cur[e.source];
   for(int q=0;q<B;++q){i64 a=e.c[par[q]*N];i64 u=x[q*N];
    if constexpr(N==1){hi[q]+=a*(u>>Bits);lo[q]+=a*(u&mask);}
    else{i64 b=e.c[par[q]*N+1],v=x[q*N+1];
     if(b==0){hi[q*N]+=a*(u>>Bits);lo[q*N]+=a*(u&mask);hi[q*N+1]+=a*(v>>Bits);lo[q*N+1]+=a*(v&mask);continue;}
     hi[q*N]+=a*(u>>Bits)-b*(v>>Bits);lo[q*N]+=a*(u&mask)-b*(v&mask);
     hi[q*N+1]+=b*(u>>Bits)+(a-b)*(v>>Bits);lo[q*N+1]+=b*(u&mask)+(a-b)*(v&mask);}
   }
  }
  for(int q=0;q<N*B;++q)next[i][q]=hi[q]+(lo[q]>>Bits)-(twice?prev[i][q]:0);
 }
}
template<int N,int B>void compute_compressed(const std::vector<int>&off,const std::vector<Edge>&full,const std::vector<Rep>&reps,const std::vector<int>&wordpar,const std::vector<i64>&coef,int start,int count,bool dump){
 using V=std::array<i64,N*B>;int d=off.size()-1,K=coef.size()-1;while(K>0&&!coef[K])--K;
 i64 Q=i64(1)<<56,ds=std::ceil(std::sqrt(double(d)));while(ds*ds<d)++ds;
 i64 eta=(7*ds+1)/2,CB=2*(Q+eta*(i64(K)*(K+1)/2+K+2));
 if(K>640||CB>=(i64(1)<<58))throw std::runtime_error("component range failed");
 std::vector<CEdge<N>>edges(full.size());i64 maxrow=0;
 for(int i=0;i<d;++i){std::array<i64,2*N>rr{};
  for(int p=off[i];p<off[i+1];++p){auto e=full[p];edges[p].source=e.source;
   for(int seed=0;seed<2;++seed){int factor=(wordpar[i]^seed)?1:6;int a=e.a+factor*e.b,b=e.c+factor*e.d;
    if(std::abs(a)>32767||std::abs(b)>32767)throw std::runtime_error("edge range failed");
    edges[p].c[seed*N]=a;
    if constexpr(N==1){rr[seed]+=std::abs(a);}
    else{edges[p].c[seed*N+1]=b;rr[seed*N]+=std::abs(a)+std::abs(b);rr[seed*N+1]+=std::abs(b)+std::abs(a-b);}
   }
  }
  for(auto x:rr)maxrow=std::max(maxrow,x);
 }
 if(i128(maxrow)*(CB/256+2)+CB>=INT64_MAX)throw std::runtime_error("split high sum exceeds signed64");
 if(i128(maxrow)*511>=INT64_MAX)throw std::runtime_error("split low sum exceeds signed64");
 // Clear the uncompressed graph in the caller before this routine in a future
 // graph-only loader; the present bounded benchmark temporarily keeps it.
 std::vector<V>prev(d),cur(d),next(d),acc(d);
 auto begin=std::chrono::steady_clock::now();auto cpu=std::clock();int completed=0;
 for(int r=start;r<int(reps.size())&&r<start+count;r+=B){
  std::fill(prev.begin(),prev.end(),V{});std::fill(cur.begin(),cur.end(),V{});std::fill(acc.begin(),acc.end(),V{});
  int active=std::min({B,int(reps.size())-r,start+count-r});std::array<int,B>par{};
  for(int q=0;q<active;++q){par[q]=wordpar[reps[r+q].index];cur[reps[r+q].index][q*N]=Q;}
  for(int k=0;k<=K;++k){
   if(coef[k])for(int i=0;i<d;++i)for(int a=0;a<N*B;++a)acc[i][a]+=floorpow<56>(i128(coef[k])*cur[i][a]);
   if(k==K)break;
   if(k==0)split_apply<9,N,B>(off,edges,cur,next,prev,par,false);
   else split_apply<8,N,B>(off,edges,cur,next,prev,par,true);
   prev.swap(cur);cur.swap(next);
  }
  for(int q=0;q<active;++q){mpz_class norm=0;i128 partial=0;int batch=0;
   for(int i=0;i<d;++i){i128 a=acc[i][q*N],b=0;if constexpr(N==2)b=acc[i][q*N+1];int factor=(wordpar[i]^par[q])?6:1;
    partial+=factor*(a*a-a*b+b*b);if(++batch==32){norm+=mpz_class(dec(partial));partial=0;batch=0;}
    if(dump){bool rad=wordpar[i]^par[q];std::cout<<"V "<<i<<" "<<(rad?0:i64(a))<<" "<<(rad?i64(a):0);if constexpr(N==2)std::cout<<" "<<(rad?0:i64(b))<<" "<<(rad?i64(b):0);std::cout<<"\n";}
   }
   norm+=mpz_class(dec(partial));std::cout<<reps[r+q].code<<" "<<reps[r+q].mult<<" "<<norm<<" 0\n"<<std::flush;++completed;
  }
 }
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count(),cpusec=double(std::clock()-cpu)/CLOCKS_PER_SEC;
 std::cerr<<"compute_seconds="<<sec<<" compute_cpu_seconds="<<cpusec<<" dimension="<<d<<" nnz="<<edges.size()<<" block_reps="<<reps.size()<<" degree="<<K<<" components="<<N<<" block_columns="<<B<<" completed="<<completed<<" max_integer_row_l1="<<maxrow<<" component_bound="<<CB<<"\n";
}
template<int N>void dispatch(int block,const std::vector<int>&off,const std::vector<Edge>&edges,const std::vector<Rep>&reps,const std::vector<int>&wordpar,const std::vector<i64>&coef,int start,int count,bool dump){
 switch(block){
 case 1:compute_compressed<N,1>(off,edges,reps,wordpar,coef,start,count,dump);break;
 case 2:compute_compressed<N,2>(off,edges,reps,wordpar,coef,start,count,dump);break;
 case 4:compute_compressed<N,4>(off,edges,reps,wordpar,coef,start,count,dump);break;
 case 8:compute_compressed<N,8>(off,edges,reps,wordpar,coef,start,count,dump);break;
 default:throw std::runtime_error("unsupported block columns");}
}

int main(int argc,char**argv){try{
 if(argc!=8&&argc!=9)throw std::runtime_error("usage: chebyshev_columns L I|P|C M start count coefficients.txt list|compute|dump|horner|horner_dump");
 int block=argc==9?std::stoi(argv[8]):1;int n=std::stoi(argv[1]),m=std::stoi(argv[3]),start=std::stoi(argv[4]),count=std::stoi(argv[5]);std::string twist=argv[2],action=argv[7];bool horner=(action=="horner"||action=="horner_dump"),dump=(action=="dump"||action=="horner_dump");
 if(start<0||count<0||start>1000000||count>1000000)throw std::runtime_error("bad column range");
 if(n<3||n>10||m>0||m< -2*n)throw std::runtime_error("unsupported L or M");
 if(twist!="I"&&twist!="P"&&twist!="C")throw std::runtime_error("bad twist");
 std::ifstream f(argv[6]);std::vector<i64>coef;i64 c;while(f>>c)coef.push_back(c);if(coef.empty()||coef.size()>641)throw std::runtime_error("no coefficients");
 i64 Q=i64(1)<<56;mpz_class mass=0;for(i64 x:coef){if(x<0||x>Q)throw std::runtime_error("invalid coefficient");mass+=x;}if(mass>Q)throw std::runtime_error("coefficient mass >Q");
 int D=1;for(int k=0;k<n;++k)D*=5;std::vector<int>index(D,-1),codes;std::vector<std::vector<int>>words;
 for(int code=0;code<D;++code){auto w=decode(code,n);if(std::accumulate(w.begin(),w.end(),0)==m){index[code]=words.size();codes.push_back(code);words.push_back(w);}}
 int d=words.size();std::vector<int>wordpar(d);for(int i=0;i<d;++i)wordpar[i]=std::count(words[i].begin(),words[i].end(),0)%2;std::vector<Rep>reps;
 for(int j=0;j<d;++j){auto o=orbit(words[j],m);if(codes[j]==*o.begin())reps.push_back({j,codes[j],int(o.size())*(m<0?2:1)});}
 int b8=n>=8?39:40;
 std::cout<<"META "<<n<<" "<<twist<<" "<<m<<" "<<d<<" "<<reps.size()<<" "<<b8<<"\n";
 long long weights=0;for(auto r:reps)weights+=r.mult;
 if(weights!=i64(d)*(m<0?2:1))throw std::runtime_error("orbit mass mismatch");
 if(action=="list"){for(auto r:reps)std::cout<<r.code<<" "<<r.mult<<"\n";return 0;}
 if(horner)throw std::runtime_error("compressed benchmark implements Chebyshev only");
 if(action!="compute"&&!dump)throw std::runtime_error("bad action");
 std::vector<std::vector<Edge>>rows(d);
 for(int j=0;j<d;++j){const auto&w=words[j];int diag=0;for(int k=0;k<n;++k)diag+=w[k]*w[(k+1)%n];rows[j].push_back({j,512-b8*n-8*diag,0,0,0});
  for(int k=0;k<n;++k){int l=(k+1)%n;for(int step:{-1,1}){auto v=w;v[k]-=step;v[l]+=step;if(v[k]<-2||v[k]>2||v[l]<-2||v[l]>2)continue;
   int prod=(6-w[k]*(w[k]-step))*(6-w[l]*(w[l]+step));int h0=prod==16?2:prod==36?3:0,h1=prod==24?1:0;
   if(!h0&&!h1)throw std::runtime_error("bad ladder product");
   int power=l==0?w[0]-v[0]:0,pa=1,pb=0;
   if(twist=="P"&&power)pa=-1;
   if(twist=="C"&&power){pa=power==1?0:-1;pb=power==1?1:-1;}
   int target=index[encode(v)];if(target<0)throw std::runtime_error("missing target");
   rows[target].push_back({j,-8*pa*h0,-8*pa*h1,-8*pb*h0,-8*pb*h1});
  }}
 }
 std::vector<int>off(d+1);std::vector<Edge>edges;
 for(int i=0;i<d;++i){off[i]=edges.size();edges.insert(edges.end(),rows[i].begin(),rows[i].end());}off[d]=edges.size();rows.clear();rows.shrink_to_fit();words.clear();words.shrink_to_fit();index.clear();index.shrink_to_fit();
 if(twist=="C")dispatch<2>(block,off,edges,reps,wordpar,coef,start,count,dump);else dispatch<1>(block,off,edges,reps,wordpar,coef,start,count,dump);
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}}
