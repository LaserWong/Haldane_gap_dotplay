// Prototype/benchmark: exact spin2 heat columns over Z[sqrt(6),omega].
// Fixed beta=8, P=(64-b8*L/8-H)/64, mu=256, Q=2^56.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
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
template<int Bits> i64 floorpow(i128 x){if(x>=0)return i64(x>>Bits);return -i64(((-x)+(i128(1)<<Bits)-1)>>Bits);}
std::vector<int> decode(int code,int n){std::vector<int>w(n);for(int k=n-1;k>=0;--k){w[k]=code%5-2;code/=5;}return w;}
int encode(const std::vector<int>&w){int c=0;for(int x:w)c=5*c+x+2;return c;}
std::set<int> orbit(const std::vector<int>&w,int m){std::set<int>o;int n=w.size();for(int f=0;f<(m==0?2:1);++f)for(int r=0;r<2;++r)for(int t=0;t<n;++t){int c=0;for(int k=0;k<n;++k)c=5*c+(f?-1:1)*w[r?(t-k+n)%n:(t+k)%n]+2;o.insert(c);}return o;}
template<int N>void compute(const std::vector<int>&off,const std::vector<Edge>&edges,const std::vector<Rep>&reps,const std::vector<i64>&coef,int start,int count){
 using V=std::array<i64,N>;int d=off.size()-1,K=coef.size()-1;while(K>0&&!coef[K])--K;
 std::vector<V>prev(d),cur(d),next(d),acc(d);i64 Q=i64(1)<<56;
 auto begin=std::chrono::steady_clock::now();
 for(int r=start;r<int(reps.size())&&r<start+count;++r){
  std::fill(prev.begin(),prev.end(),V{});std::fill(cur.begin(),cur.end(),V{});std::fill(acc.begin(),acc.end(),V{});
  cur[reps[r].index][0]=Q;
  for(int k=0;k<=K;++k){
   if(coef[k])for(int i=0;i<d;++i)for(int a=0;a<N;++a)acc[i][a]+=floorpow<56>(i128(coef[k])*cur[i][a]);
   if(k==K)break;
   for(int i=0;i<d;++i){std::array<i128,N>s{};
    for(int p=off[i];p<off[i+1];++p){auto e=edges[p];const auto&x=cur[e.source];
     s[0]+=i128(e.a)*x[0]+i128(6*e.b)*x[1];s[1]+=i128(e.b)*x[0]+i128(e.a)*x[1];
     if constexpr(N==4){
      s[0]-=i128(e.c)*x[2]+i128(6*e.d)*x[3];s[1]-=i128(e.d)*x[2]+i128(e.c)*x[3];
      s[2]+=i128(e.c)*x[0]+i128(6*e.d)*x[1]+i128(e.a-e.c)*x[2]+i128(6*(e.b-e.d))*x[3];
      s[3]+=i128(e.d)*x[0]+i128(e.c)*x[1]+i128(e.b-e.d)*x[2]+i128(e.a-e.c)*x[3];
     }
    }
    for(int a=0;a<N;++a)next[i][a]=k==0?floorpow<9>(s[a]):floorpow<8>(s[a])-prev[i][a];
   }
   prev.swap(cur);cur.swap(next);
  }
  mpz_class n0=0,n1=0;i128 p0=0,p1=0;int batch=0;
  for(const auto&v:acc){i128 a=v[0],b=v[1],c=0,d=0;if constexpr(N==4){c=v[2];d=v[3];}
   p0+=a*a+6*b*b-a*c-6*b*d+c*c+6*d*d;
   p1+=2*a*b-a*d-b*c+2*c*d;
   if(++batch==32){n0+=mpz_class(dec(p0));n1+=mpz_class(dec(p1));p0=p1=0;batch=0;}
  }
  n0+=mpz_class(dec(p0));n1+=mpz_class(dec(p1));
  std::cout<<reps[r].code<<" "<<reps[r].mult<<" "<<n0<<" "<<n1<<"\n";
 }
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
 std::cerr<<"compute_seconds="<<sec<<" dimension="<<d<<" nnz="<<edges.size()<<" block_reps="<<reps.size()<<" degree="<<K<<" components="<<N<<"\n";
}
int main(int argc,char**argv){try{
 if(argc!=8)throw std::runtime_error("usage: chebyshev_columns L I|P|C M start count coefficients.txt list|compute");
 int n=std::stoi(argv[1]),m=std::stoi(argv[3]),start=std::stoi(argv[4]),count=std::stoi(argv[5]);std::string twist=argv[2];
 if(n<3||n>10||m>0||m< -2*n)throw std::runtime_error("unsupported L or M");
 if(twist!="I"&&twist!="P"&&twist!="C")throw std::runtime_error("bad twist");
 std::ifstream f(argv[6]);std::vector<i64>coef;i64 c;while(f>>c)coef.push_back(c);if(coef.empty())throw std::runtime_error("no coefficients");
 i64 Q=i64(1)<<56;mpz_class mass=0;for(i64 x:coef){if(x<0||x>Q)throw std::runtime_error("invalid coefficient");mass+=x;}if(mass>Q)throw std::runtime_error("coefficient mass >Q");
 int D=1;for(int k=0;k<n;++k)D*=5;std::vector<int>index(D,-1),codes;std::vector<std::vector<int>>words;
 for(int code=0;code<D;++code){auto w=decode(code,n);if(std::accumulate(w.begin(),w.end(),0)==m){index[code]=words.size();codes.push_back(code);words.push_back(w);}}
 int d=words.size();std::vector<Rep>reps;
 for(int j=0;j<d;++j){auto o=orbit(words[j],m);if(codes[j]==*o.begin())reps.push_back({j,codes[j],int(o.size())*(m<0?2:1)});}
 int b8=n>=8?39:40;
 std::cout<<"META "<<n<<" "<<twist<<" "<<m<<" "<<d<<" "<<reps.size()<<" "<<b8<<"\n";
 if(std::string(argv[7])=="list"){for(auto r:reps)std::cout<<r.code<<" "<<r.mult<<"\n";return 0;}
 if(std::string(argv[7])!="compute")throw std::runtime_error("bad action");
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
 if(twist=="C")compute<4>(off,edges,reps,coef,start,count);else compute<2>(off,edges,reps,coef,start,count);
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}}
