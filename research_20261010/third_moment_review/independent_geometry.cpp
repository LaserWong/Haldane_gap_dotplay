// Independent direct bilinear-form audit. No producer code is included.
// Exhaustive q6 support enumeration (not the producer edge-mask construction).
// X and Z contract local bond forms directly, rather than forming second images.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
#include <sys/resource.h>
using namespace std;
using Int=__int128_t;
constexpr int D=14;
using Row=array<long long,D>;
using Ten=array<Row,15>;
using Matrix=array<array<Int,D>,D>;
using Four=array<Row,3>;
struct Pairing {array<int,6> mate;};
struct Algebra {int q,k; vector<Pairing> p; int gram[15][15]{}; int swap[6][6][15]{},cap[6][6][15]{}; int form[6][6][15][15]{};};
int N,d,E[64][64]{},orbit[64][64]{};long long choose[65][5]{};
vector<pair<int,int>> neighbors[64];vector<Four> Rcache;
Algebra a4,a6;
void enumerate(Algebra& a,Pairing x,int bits){if(!bits){a.p.push_back(x);return;}int i=__builtin_ctz(bits);bits^=1<<i;for(int j=i+1;j<a.q;j++)if(bits>>j&1){x.mate[i]=j;x.mate[j]=i;enumerate(a,x,bits^(1<<j));}}
int index(const Algebra& a,const Pairing& x){for(int p=0;p<a.k;p++){bool equal=true;for(int i=0;i<a.q;i++)equal&=x.mate[i]==a.p[p].mate[i];if(equal)return p;}assert(false);return -1;}
void initialize(Algebra& a,int q){a.q=q;enumerate(a,{},(1<<q)-1);a.k=a.p.size();
 for(int p=0;p<a.k;p++)for(int r=0;r<a.k;r++){int seen=0,loops=0;for(int i=0;i<q;i++)if(!(seen>>i&1)){loops++;int node=i;do{seen|=1<<node;node=a.p[p].mate[node];seen|=1<<node;node=a.p[r].mate[node];}while(node!=i);}int z=1;while(loops--)z*=3;a.gram[p][r]=z;}
 for(int i=0;i<q;i++)for(int j=i+1;j<q;j++)for(int r=0;r<a.k;r++){
  auto x=a.p[r];int u=x.mate[i],v=x.mate[j];
  if(u==j){a.swap[i][j][r]=a.cap[i][j][r]=r;for(int p=0;p<a.k;p++)a.form[i][j][p][r]=-2*a.gram[p][r];}
  else{auto sw=x,co=x;sw.mate[i]=v;sw.mate[v]=i;sw.mate[j]=u;sw.mate[u]=j;co.mate[i]=j;co.mate[j]=i;co.mate[u]=v;co.mate[v]=u;int s=index(a,sw),c=index(a,co);a.swap[i][j][r]=s;a.cap[i][j][r]=c;for(int p=0;p<a.k;p++)a.form[i][j][p][r]=a.gram[p][s]-a.gram[p][c];}
 }
}
long long rank4(const int* x){long long r=0;for(int i=0;i<4;i++)r+=choose[x[i]][i+1];return r;}
Ten L(const int* sites){Ten ans{};for(int p=0;p<3;p++){int a=0,b=a4.p[p].mate[a],c=1;while(c==b)c++;int e=a4.p[p].mate[c];ans[p][orbit[sites[a]][sites[b]]]+=E[sites[c]][sites[e]];ans[p][orbit[sites[c]][sites[e]]]+=E[sites[a]][sites[b]];}return ans;}
Ten M(const int* sites){Ten ans{};for(int p=0;p<15;p++){int edge[3],orb[3],z=0;for(int i=0;i<6;i++)if(i<a6.p[p].mate[i]){int j=a6.p[p].mate[i];edge[z]=E[sites[i]][sites[j]];orb[z++]=orbit[sites[i]][sites[j]];}for(int j=0;j<3;j++)ans[p][orb[j]]+=2*edge[(j+1)%3]*edge[(j+2)%3];}return ans;}
void add(Row& dst,const Row& src,int w){for(int c=0;c<d;c++)dst[c]+=w*src[c];}
Ten Runcached(const int* sites){Ten l=L(sites),out{};for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)if(E[sites[i]][sites[j]])for(int p=0;p<3;p++){int w=E[sites[i]][sites[j]];if(a4.p[p].mate[i]==j)add(out[p],l[p],-2*w);else{add(out[a4.swap[i][j][p]],l[p],w);add(out[a4.cap[i][j][p]],l[p],-w);}}
 for(int i=0;i<4;i++)for(auto [j,w]:neighbors[sites[i]]){bool occupied=false;for(int k=0;k<4;k++)occupied|=sites[k]==j;if(occupied)continue;int x[4];copy(sites,sites+4,x);x[i]=j;Ten incoming=L(x);for(int p=0;p<3;p++)add(out[p],incoming[p],w);}
 return out;}
Ten R(const int* sites){int sorted[4],where[4];copy(sites,sites+4,sorted);sort(sorted,sorted+4);for(int i=0;i<4;i++)where[i]=find(sorted,sorted+4,sites[i])-sorted;auto& v=Rcache[rank4(sorted)];Ten ans{};for(int p=0;p<3;p++){Pairing mapped{};for(int i=0;i<4;i++)mapped.mate[where[i]]=where[a4.p[p].mate[i]];ans[p]=v[index(a4,mapped)];}return ans;}
void outer(Matrix& out,const Row& l,const Row& r,int factor){if(!factor)return;for(int i=0;i<d;i++)if(l[i])for(int j=0;j<d;j++)if(r[j]){Int term=(Int)l[i]*r[j]*factor,z;assert(!__builtin_add_overflow(out[i][j],term,&z));out[i][j]=z;}}
void gram_contract(Matrix& out,const Ten& l,const Ten& r,const Algebra& a,int w=1){for(int p=0;p<a.k;p++)for(int q=0;q<a.k;q++)outer(out,l[p],r[q],w*a.gram[p][q]);}
void preserve_expect(Matrix& out,const int* sites,const Ten& left,const Algebra& a){
 // Same-support interaction contracted with an independently precomputed bond form.
 for(int i=0;i<a.q;i++)for(int j=i+1;j<a.q;j++)if(E[sites[i]][sites[j]])for(int p=0;p<a.k;p++)for(int r=0;r<a.k;r++)outer(out,left[p],left[r],E[sites[i]][sites[j]]*a.form[i][j][p][r]);
 // Distinct-support hops. Ordered labels are retained through the replacement.
 for(int i=0;i<a.q;i++)for(auto [j,w]:neighbors[sites[i]]){bool occupied=false;for(int k=0;k<a.q;k++)occupied|=sites[k]==j;if(occupied)continue;int source[6];copy(sites,sites+a.q,source);source[i]=j;Ten right=a.q==4?R(source):M(source);gram_contract(out,left,right,a,w);}
}
void cross_expect(Matrix& Y,const int* sites,const Ten& right){for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]]){int rem[4],positions[4],c=0;for(int k=0;k<6;k++)if(k!=i&&k!=j){rem[c]=sites[k];positions[c++]=k;}Ten rr=R(rem);for(int p=0;p<3;p++){Pairing combined{};combined.mate[i]=j;combined.mate[j]=i;for(int k=0;k<4;k++)combined.mate[positions[k]]=positions[a4.p[p].mate[k]];int row=index(a6,combined);for(int q=0;q<15;q++)outer(Y,rr[p],right[q],E[sites[i]][sites[j]]*a6.gram[row][q]);}}}
string number(Int x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;string s;while(x){s.push_back(char('0'+x%10));x/=10;}if(neg)s.push_back('-');reverse(s.begin(),s.end());return s;}
void emit(ostream& out,const char* name,const Matrix& m,int q,bool origin){out<<",\n\""<<name<<"\":[";for(int i=0;i<d;i++){if(i)out<<',';out<<'[';for(int j=0;j<d;j++){if(j)out<<',';Int x=m[i][j];if(origin){assert((x*N)%q==0);x=x*N/q;}out<<number(x);}out<<']';}out<<']';}
int main(int argc,char**argv){assert(argc==4);bool origin=string(argv[3])=="origin";ifstream in(argv[1]);in>>N>>d;assert(N<=64&&d<=D);int count;in>>count;for(int k=0;k<count;k++){int i,j,w;in>>i>>j>>w;E[i][j]=E[j][i]=w;neighbors[i].push_back({j,w});neighbors[j].push_back({i,w});}for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){in>>orbit[i][j];orbit[j][i]=orbit[i][j];}initialize(a4,4);initialize(a6,6);for(int n=0;n<=64;n++){choose[n][0]=1;for(int k=1;k<=4;k++)choose[n][k]=n?choose[n-1][k-1]+choose[n-1][k]:0;}
 auto start=chrono::steady_clock::now();Rcache.resize(choose[N][4]);for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){int sites[4]={a,b,c,e};Ten r=Runcached(sites);for(int p=0;p<3;p++)Rcache[rank4(sites)][p]=r[p];}
 Matrix f{},s{},v{},w{},x{},y{},z{};long long q4=0,q6=0,active=0;for(int a=0;a<(origin?1:N);a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){int sites[4]={a,b,c,e};Ten ll=L(sites),rr=R(sites);gram_contract(f,ll,ll,a4);gram_contract(s,ll,rr,a4);gram_contract(v,rr,rr,a4);preserve_expect(x,sites,rr,a4);q4++;}
 cerr<<"q4 supports "<<q4<<" complete\n";
 for(int a=0;a<(origin?1:N);a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++)for(int h=e+1;h<N;h++)for(int j=h+1;j<N;j++){q6++;int sites[6]={a,b,c,e,h,j};Ten mm=M(sites);bool nonzero=false;for(int p=0;p<15;p++)for(int k=0;k<d;k++)nonzero|=mm[p][k]!=0;if(!nonzero)continue;active++;gram_contract(w,mm,mm,a6);cross_expect(y,sites,mm);preserve_expect(z,sites,mm,a6);}
 double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();rusage usage{};getrusage(RUSAGE_SELF,&usage);ofstream out(argv[2]);out<<"{\"N\":"<<N<<",\"orbits\":"<<d<<",\"fixed_origin\":"<<(origin?"true":"false")<<",\"all_q4\":"<<q4<<",\"all_q6\":"<<q6<<",\"active_q6\":"<<active<<",\"seconds\":"<<seconds<<",\"peak_rss_kib\":"<<usage.ru_maxrss;emit(out,"F",f,4,origin);emit(out,"S",s,4,origin);emit(out,"V",v,4,origin);emit(out,"W",w,6,origin);emit(out,"X",x,4,origin);emit(out,"Y",y,6,origin);emit(out,"Z",z,6,origin);out<<"}\n";cerr<<"all q6 supports "<<q6<<", active "<<active<<", seconds "<<seconds<<'\n';}
