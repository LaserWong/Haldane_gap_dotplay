// Independent adaptation of the locally reviewed streamed kernel for beta49/4.
// Source provenance and changes are recorded in PROOF.md.
// No eigensolver, dense matrix, BLAS, or floating-point acceptance arithmetic.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#include <gmpxx.h>
using cpp_int = mpz_class;
using i64 = int64_t;
using i128 = __int128_t;
using u128 = __uint128_t;
struct Edge {int source; int a,b;};
struct Rep {int index,code,multiplicity;};
static std::string decimal(u128 x) {
    if (!x) return "0";
    std::string s; while(x) {s.push_back('0'+x%10);x/=10;}
    std::reverse(s.begin(),s.end()); return s;
}
static i64 floor32(i64 x) { return x>=0 ? x/32 : -((-x+31)/32); }
static std::vector<int> decode(int code,int n) {
    std::vector<int>w(n);for(int k=n-1;k>=0;--k){w[k]=code%3-1;code/=3;}return w;
}
static int encode(const std::vector<int>&w){int c=0;for(int x:w)c=3*c+x+1;return c;}
static std::set<int> orbit(const std::vector<int>&w,const std::string&mode,int m){
    std::set<int> o;
    int n=w.size();
    if(mode=="none") {o.insert(encode(w));return o;}
    int nf=(mode=="full"&&m==0)?2:1;
    int nr=(mode=="translation")?1:2;
    for(int f=0;f<nf;++f)for(int r=0;r<nr;++r)for(int t=0;t<n;++t){
        std::vector<int>v(n);
        for(int k=0;k<n;++k)v[k]=(f?-1:1)*w[(r?(t-k+n)%n:(t+k)%n)];
        o.insert(encode(v));
    }
    return o;
}
int main(int argc,char**argv){
 try {
    if(argc!=9)throw std::runtime_error("usage: stream_horner L I|P|C none|translation|dihedral|full M start count coeff.txt list|compute");
    int n=std::stoi(argv[1]);std::string twist=argv[2],mode=argv[3];int m=std::stoi(argv[4]);
    size_t start=std::stoull(argv[5]),count=std::stoull(argv[6]);
    if(n<4||n>12)throw std::runtime_error("Appendix B lengths 4..12 supported");
    if(twist!="I"&&twist!="P")throw std::runtime_error("bad twist");
    if(mode!="none"&&mode!="translation"&&mode!="dihedral"&&mode!="full")throw std::runtime_error("bad orbit mode");
    if(mode=="full"&&m<0)throw std::runtime_error("full mode uses nonnegative M blocks only");
    std::vector<i64> coeff;std::ifstream cf(argv[7]);i64 x;while(cf>>x)coeff.push_back(x);
    if(coeff.size()!=281)throw std::runtime_error("expected 281 coefficients");
    i64 Q=i64(1)<<55;cpp_int coeff_sum=0;for(i64 c:coeff){if(c<0||c>Q)throw std::runtime_error("bad coefficient");coeff_sum+=c;}
    if(coeff_sum>Q)throw std::runtime_error("coefficient mass > Q");
    int kmax=280;while(kmax&&coeff[kmax]==0)--kmax;
    int D=1;for(int k=0;k<n;++k)D*=3;
    std::vector<int>codes,index(D,-1);std::vector<std::vector<int>>words;
    for(int c=0;c<D;++c){auto w=decode(c,n);if(std::accumulate(w.begin(),w.end(),0)==m){index[c]=words.size();codes.push_back(c);words.push_back(w);}}
    int d=words.size();if(!d)throw std::runtime_error("empty block");
    std::vector<Rep> reps;
    for(int j=0;j<d;++j){auto o=orbit(words[j],mode,m);if(codes[j]==*o.begin())reps.push_back({j,codes[j],int(o.size())*((mode=="full"&&m>0)?2:1)});}
    if(std::string(argv[8])=="list"){
        std::cout<<"META "<<n<<" "<<twist<<" "<<mode<<" "<<m<<" "<<d<<" "<<reps.size()<<" "<<kmax<<"\n";
        for(auto r:reps)std::cout<<r.code<<" "<<r.multiplicity<<"\n";
        return 0;
    }
    if(std::string(argv[8])!="compute")throw std::runtime_error("bad action");
    std::vector<std::vector<Edge>> rows(d);
    for(int j=0;j<d;++j){auto&w=words[j];int diag=0;for(int k=0;k<n;++k)diag+=w[(k+n-1)%n]*w[k];
        rows[j].push_back({j,32-3*n-2*diag,0});
        for(int k=0;k<n;++k){int l=(k+1)%n;for(int step:{-1,1}){
            auto v=w;v[k]-=step;v[l]+=step;
            if(v[k]<-1||v[k]>1||v[l]<-1||v[l]>1)continue;
            int i=index[encode(v)];if(i<0)throw std::runtime_error("missing target");
            int power=l==0?w[0]-v[0]:0,a=-2,b=0;
            if(twist=="C"&&power){if(power==1){a=0;b=-1;}else{a=2;b=1;}}
            else if(twist=="P"&&power)a=2;
            rows[i].push_back({j,a,b});
        }}
    }
    // A physical column norm is <=Q+E, E<=173 sqrt(d) (coefficient mass <=Q).
    // Each Eisenstein coordinate is <=2 times its physical modulus. This
    // simple integral overbound therefore controls all sparse partial sums.
    i64 component_bound=2*Q;
    int max_rowsum=0;
    for(auto&row:rows){int s1=0,s2=0;for(auto e:row){s1+=std::abs(e.a)+std::abs(e.b);s2+=std::abs(e.b)+std::abs(e.a-e.b);}max_rowsum=std::max({max_rowsum,s1,s2});}
    if(i128(max_rowsum)*component_bound>=i128(INT64_MAX))throw std::runtime_error("sparse partial-sum bound exceeds int64");
    std::vector<int>offset(d+1);std::vector<Edge>edges;for(int i=0;i<d;++i){offset[i]=edges.size();edges.insert(edges.end(),rows[i].begin(),rows[i].end());}offset[d]=edges.size();rows.clear();
    std::vector<i64>u(d),v(d),nu(d),nv(d);bool complex=twist=="C";
    auto t0=std::chrono::steady_clock::now();
    for(size_t r=start;r<reps.size()&&r<start+count;++r){
        std::fill(u.begin(),u.end(),0);std::fill(v.begin(),v.end(),0);
        for(int k=kmax;k>=0;--k){
            if(complex){
                for(int i=0;i<d;++i){i64 su=0,sv=0;for(int e=offset[i];e<offset[i+1];++e){auto z=edges[e];su+=z.a*u[z.source]-z.b*v[z.source];sv+=z.b*u[z.source]+(z.a-z.b)*v[z.source];}nu[i]=floor32(su);nv[i]=floor32(sv);}
                u.swap(nu);v.swap(nv);
            }else{
                for(int i=0;i<d;++i){i64 s=0;for(int e=offset[i];e<offset[i+1];++e){auto z=edges[e];s+=z.a*u[z.source];}nu[i]=floor32(s);}u.swap(nu);
            }
            u[reps[r].index]+=coeff[k];
        }
        // Products are exact signed128; chunking prevents accumulation overflow
        // even using the deliberately loose component bound rather than norms.
        cpp_int norm=0;u128 partial=0;int batch=0;
        for(int i=0;i<d;++i){i128 a=u[i],b=complex?v[i]:0;i128 term=a*a-a*b+b*b;if(term<0)throw std::runtime_error("negative norm term");partial+=u128(term);if(++batch==64){norm+=cpp_int(decimal(partial));partial=0;batch=0;}}
        norm+=cpp_int(decimal(partial));
        std::cout<<reps[r].code<<" "<<reps[r].multiplicity<<" "<<norm<<"\n";
    }
    double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
    std::cerr<<"seconds="<<sec<<" d="<<d<<" nnz="<<edges.size()<<" reps="<<reps.size()<<" rowsum="<<max_rowsum<<"\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}
}
