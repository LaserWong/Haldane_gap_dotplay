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
void add(Row& dst,const Row& src,int w){for(int c=0;c<d;c++){long long term,z;assert(!__builtin_mul_overflow((long long)w,src[c],&term));assert(!__builtin_add_overflow(dst[c],term,&z));assert(z>=-(1LL<<31)&&z<(1LL<<31));dst[c]=z;}}
Ten Runcached(const int* sites){Ten l=L(sites),out{};for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)if(E[sites[i]][sites[j]])for(int p=0;p<3;p++){int w=E[sites[i]][sites[j]];if(a4.p[p].mate[i]==j)add(out[p],l[p],-2*w);else{add(out[a4.swap[i][j][p]],l[p],w);add(out[a4.cap[i][j][p]],l[p],-w);}}
 for(int i=0;i<4;i++)for(auto [j,w]:neighbors[sites[i]]){bool occupied=false;for(int k=0;k<4;k++)occupied|=sites[k]==j;if(occupied)continue;int x[4];copy(sites,sites+4,x);x[i]=j;Ten incoming=L(x);for(int p=0;p<3;p++)add(out[p],incoming[p],w);}
 return out;}
Ten R(const int* sites){int sorted[4],where[4];copy(sites,sites+4,sorted);sort(sorted,sorted+4);for(int i=0;i<4;i++)where[i]=find(sorted,sorted+4,sites[i])-sorted;auto& v=Rcache[rank4(sorted)];Ten ans{};for(int p=0;p<3;p++){Pairing mapped{};for(int i=0;i<4;i++)mapped.mate[where[i]]=where[a4.p[p].mate[i]];ans[p]=v[index(a4,mapped)];}return ans;}
void outer(Matrix& out,const Row& l,const Row& r,int factor){if(!factor)return;for(int i=0;i<d;i++)if(l[i])for(int j=0;j<d;j++)if(r[j]){assert(l[i]>=-(1LL<<31)&&l[i]<(1LL<<31)&&r[j]>=-(1LL<<31)&&r[j]<(1LL<<31)&&factor>=-4096&&factor<=4096);Int term=(Int)l[i]*r[j]*factor,z;assert(!__builtin_add_overflow(out[i][j],term,&z));out[i][j]=z;}}
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

Ten image_preserve(const int*sites,int what,const Algebra&a){
 Ten v=what==1?R(sites):M(sites),out{};
 for(int i=0;i<a.q;i++)for(int j=i+1;j<a.q;j++)if(E[sites[i]][sites[j]])for(int p=0;p<a.k;p++){
  int w=E[sites[i]][sites[j]];
  if(a.p[p].mate[i]==j)add(out[p],v[p],-2*w);
  else{add(out[a.swap[i][j][p]],v[p],w);add(out[a.cap[i][j][p]],v[p],-w);}}
 for(int i=0;i<a.q;i++)for(auto[j,w]:neighbors[sites[i]]){bool occ=false;for(int k=0;k<a.q;k++)occ|=sites[k]==j;if(occ)continue;int source[6];copy(sites,sites+a.q,source);source[i]=j;Ten inc=what==1?R(source):M(source);for(int p=0;p<a.k;p++)add(out[p],inc[p],w);}
 return out;
}
Ten image_CM(const int*sites){Ten out{};bool occ[64]{};for(int i=0;i<4;i++)occ[sites[i]]=true;
 for(int u=0;u<N;u++)if(!occ[u])for(int v=u+1;v<N;v++)if(!occ[v]&&E[u][v]){
  int source[6];copy(sites,sites+4,source);source[4]=u;source[5]=v;Ten coeff=M(source);
  for(int r=0;r<15;r++){auto z=a6.p[r];int f=1;if(z.mate[4]==5)f=3;else{int x=z.mate[4],y=z.mate[5];z.mate[x]=y;z.mate[y]=x;}add(out[index(a4,z)],coeff[r],f*E[u][v]);}}
 return out;
}
Ten image_CR(const int*sites){Ten out{};
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]]){int src[4],pos[4],n=0;for(int k=0;k<6;k++)if(k!=i&&k!=j){src[n]=sites[k];pos[n++]=k;}Ten r=R(src);for(int p=0;p<3;p++){Pairing z{};z.mate[i]=j;z.mate[j]=i;for(int k=0;k<4;k++)z.mate[pos[k]]=pos[a4.p[p].mate[k]];add(out[index(a6,z)],r[p],E[sites[i]][sites[j]]);}}
 return out;
}
void matrix_commutator(Matrix&out,const int*sites,const Ten&left){bool occ[64]{};for(int i=0;i<6;i++)occ[sites[i]]=true;
 int vac=0;for(int u=0;u<N;u++)if(!occ[u])for(auto[v,w]:neighbors[u])if(u<v&&!occ[v])vac+=3*w*w;
 gram_contract(out,left,left,a6,vac);
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]]){Ten capped{};for(int p=0;p<15;p++)add(capped[a6.cap[i][j][p]],left[p],a6.p[p].mate[i]==j?3:1);int w=E[sites[i]][sites[j]];gram_contract(out,left,capped,a6,-w*w);}
 for(int k=0;k<6;k++)for(auto[center,w]:neighbors[sites[k]])for(auto[j,z]:neighbors[center])if(j!=sites[k]&&!occ[j]){
  int src[6];copy(sites,sites+6,src);src[k]=j;Ten incoming=M(src);
  if(!occ[center])gram_contract(out,left,incoming,a6,w*z);
  else{int i=find(sites,sites+6,center)-sites;int lo=min(i,k),hi=max(i,k);Ten capped{};for(int p=0;p<15;p++)add(capped[a6.cap[lo][hi][p]],incoming[p],a6.p[p].mate[i]==k?3:1);gram_contract(out,left,capped,a6,-w*z);}}
}
// New scalar direction audit: all local actions below are independent of producer kernels.
#include <gmpxx.h>
#include <map>
#include <functional>
#include <iomanip>
using Scalar=array<Int,15>;
int nx,ny;array<Int,D> coeffR{},coeffM{};vector<Scalar> scalar_cache;vector<unsigned char> filled;
long long choose6[65][7]{};int perms[720][15];size_t fills=0,queries=0;
Int safe_add(Int a,Int b){Int z;assert(!__builtin_add_overflow(a,b,&z));return z;}
Int safe_mul(Int a,long long b){Int z;assert(!__builtin_mul_overflow(a,(Int)b,&z));return z;}
void sadd(Scalar&to,const Scalar&from,long long w,int k){for(int p=0;p<k;p++)to[p]=safe_add(to[p],safe_mul(from[p],w));}
Scalar col(const Ten&x,int j,int k){Scalar y{};for(int p=0;p<k;p++)y[p]=x[p][j];return y;}
Scalar raw_T(const int*sites){Ten cr=image_CR(sites),dm=image_preserve(sites,2,a6);Scalar t{};for(int p=0;p<15;p++)for(int j=0;j<d;j++){t[p]=safe_add(t[p],safe_mul(coeffR[j],cr[p][j]));t[p]=safe_add(t[p],safe_mul(coeffM[j],dm[p][j]));}return t;}
int permrank(const int*w){int result=0;for(int i=0;i<6;i++){result*=6-i;for(int j=i+1;j<6;j++)result+=w[j]<w[i];}return result;}
Scalar T(const int*sites,int anchor=0){queries++;int ordered[6],sorted[6],map[6];int origin=sites[anchor];for(int i=0;i<6;i++)ordered[i]=((sites[i]/ny-origin/ny+nx)%nx)*ny+(sites[i]%ny-origin%ny+ny)%ny;copy(ordered,ordered+6,sorted);sort(sorted,sorted+6);assert(sorted[0]==0);long long r=0;for(int i=1;i<6;i++)r+=choose6[sorted[i]-1][i];assert(r>=0&&r<(long long)scalar_cache.size());if(!filled[r]){scalar_cache[r]=raw_T(sorted);filled[r]=1;fills++;}for(int i=0;i<6;i++)map[i]=find(sorted,sorted+6,ordered[i])-sorted;Scalar v{};int pi=permrank(map);for(int p=0;p<15;p++)v[p]=scalar_cache[r][perms[pi][p]];return v;}
Scalar DT(const int*sites,const Scalar&t){Scalar result{};for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]])for(int p=0;p<15;p++){int w=E[sites[i]][sites[j]];if(a6.p[p].mate[i]==j)result[p]=safe_add(result[p],safe_mul(t[p],-2*w));else{int s=a6.swap[i][j][p],c=a6.cap[i][j][p];result[s]=safe_add(result[s],safe_mul(t[p],w));result[c]=safe_add(result[c],safe_mul(t[p],-w));}}
for(int i=0;i<6;i++)for(auto[j,w]:neighbors[sites[i]]){if(find(sites,sites+6,j)!=sites+6)continue;int source[6];copy(sites,sites+6,source);source[i]=j;sadd(result,T(source),w,15);}return result;}
Scalar CT(const int*sites){bool occupied[64]{};for(int i=0;i<4;i++)occupied[sites[i]]=true;Scalar result{};for(int u=0;u<N;u++)if(!occupied[u])for(auto[v,w]:neighbors[u])if(v>u&&!occupied[v]){int source[6];copy(sites,sites+4,source);source[4]=u;source[5]=v;Scalar incoming=T(source);for(int p=0;p<15;p++){auto pairing=a6.p[p];int factor=1;if(pairing.mate[4]==5)factor=3;else{int i=pairing.mate[4],j=pairing.mate[5];pairing.mate[i]=j;pairing.mate[j]=i;}int dest=index(a4,pairing);result[dest]=safe_add(result[dest],safe_mul(incoming[p],w*factor));}}return result;}
Scalar K_action(const int*sites,const Scalar&left,const function<Scalar(const int*)>&lookup){bool occupied[64]{};for(int i=0;i<6;i++)occupied[sites[i]]=true;int vac=0;for(int u=0;u<N;u++)if(!occupied[u])for(auto[v,w]:neighbors[u])if(u<v&&!occupied[v])vac+=3*w*w;Scalar result{};sadd(result,left,vac,15);
for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]])for(int p=0;p<15;p++){int factor=(a6.p[p].mate[i]==j?3:1),w=E[sites[i]][sites[j]];int dest=a6.cap[i][j][p];result[dest]=safe_add(result[dest],safe_mul(left[p],-w*w*factor));}
for(int k=0;k<6;k++)for(auto[center,w]:neighbors[sites[k]])for(auto[j,z]:neighbors[center])if(j!=sites[k]&&!occupied[j]){int source[6];copy(sites,sites+6,source);source[k]=j;Scalar incoming=lookup(source);if(!occupied[center])sadd(result,incoming,w*z,15);else{int i=find(sites,sites+6,center)-sites,lo=min(i,k),hi=max(i,k);for(int p=0;p<15;p++){int dest=a6.cap[lo][hi][p],factor=a6.p[p].mate[i]==k?3:1;result[dest]=safe_add(result[dest],safe_mul(incoming[p],-w*z*factor));}}}return result;}
mpz_class big(Int x){return mpz_class(number(x));}
mpz_class dot(const Scalar&l,const Scalar&r,const Algebra&a){mpz_class result=0;for(int p=0;p<a.k;p++)if(l[p]){Int z=0;for(int q=0;q<a.k;q++)z=safe_add(z,safe_mul(r[q],a.gram[p][q]));if(z)result+=big(l[p])*big(z);}return result;}
struct Sums{vector<mpz_class> G,H,J;mpz_class norm,ctnorm,tkt;Sums():G(4*d+2),H(4*d+2),J(4*d+2){} }; 
void export_vector(ostream&out,const char*name,const vector<mpz_class>&a){out<<",\""<<name<<"\":[";for(size_t j=0;j<a.size();j++){if(j)out<<',';out<<'"'<<a[j]<<'"';}out<<']';}
void expand(map<unsigned long long,array<Int,4>>&out,const int*sites,const Scalar&v,int q,int column){const Algebra&a=q==4?a4:a6;int colors=q==4?9:27;for(int p=0;p<a.k;p++)for(int z=0;z<colors;z++){int n=z;unsigned long long state=0;for(int i=0;i<q;i++)if(i<a.p[p].mate[i]){int c=n%3+1;n/=3;state|=(unsigned long long)c<<(2*sites[i]);state|=(unsigned long long)c<<(2*sites[a.p[p].mate[i]]);}out[state][column]=safe_add(out[state][column],v[p]);}}
void combinations(int q,bool origin,const function<void(const int*)>&f){int sites[6]{};function<void(int,int)> rec=[&](int k,int next){if(k==q){f(sites);return;}for(int x=next;x<=N-(q-k);x++){sites[k]=x;rec(k+1,x+1);}};if(origin){sites[0]=0;rec(1,1);}else rec(0,0);}
int main(int argc,char**argv){assert(argc==9);nx=stoi(argv[3]);ny=stoi(argv[4]);string mode=argv[5];assert(mode=="fixture"||mode=="benchmark"||mode=="full_authorized");bool fixture=mode=="fixture",full=mode=="full_authorized";int limit4=stoi(argv[6]),limit6=stoi(argv[7]);assert(fixture||(full&&limit4==0&&limit6==0)||(!full&&limit4>0&&limit6>0));ifstream in(argv[1]);in>>N>>d;assert(N==nx*ny&&N<=32&&d<=14);if(fixture)assert(N==8);int ne;in>>ne;for(int k=0;k<ne;k++){int i,j,w;in>>i>>j>>w;assert(w==1||w==2);E[i][j]=E[j][i]=w;neighbors[i].push_back({j,w});neighbors[j].push_back({i,w});}for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){in>>orbit[i][j];orbit[j][i]=orbit[i][j];}
 initialize(a4,4);initialize(a6,6);for(int n=0;n<=64;n++){choose[n][0]=choose6[n][0]=1;for(int k=1;k<=6;k++){choose6[n][k]=n?choose6[n-1][k-1]+choose6[n-1][k]:0;if(k<=4)choose[n][k]=choose6[n][k];}}
 int perm[6]={0,1,2,3,4,5};do{int pi=permrank(perm);for(int p=0;p<15;p++){Pairing v{};for(int i=0;i<6;i++)v.mate[perm[i]]=perm[a6.p[p].mate[i]];perms[pi][p]=index(a6,v);}}while(next_permutation(perm,perm+6));
 ifstream cf(argv[2]);for(int j=0;j<2*d;j++){string s;cf>>s;assert(!s.empty());bool neg=s[0]=='-';Int z=0;for(char c:s)if(c!='-'){assert(c>='0'&&c<='9');z=safe_add(safe_mul(z,10),c-'0');}if(neg)z=-z;assert(z>=-((Int)1<<48)&&z<=((Int)1<<48));(j<d?coeffR[j]:coeffM[j-d])=z;}
 clock_t start=clock();Rcache.resize(choose[N][4]);combinations(4,false,[&](const int*sites){Ten r=Runcached(sites);for(int p=0;p<3;p++)Rcache[rank4(sites)][p]=r[p];});double rcpu=double(clock()-start)/CLOCKS_PER_SEC;
 scalar_cache.resize(choose6[N-1][5]);filled.resize(scalar_cache.size());Sums sum4,sum6;map<unsigned long long,array<Int,4>> physical;size_t n4=0,n6=0,nzero=0,anchors=0;long long i4=0,i6=0,stride4=(fixture||full)?1:max(1LL,choose6[N-1][3]/limit4),stride6=(fixture||full)?1:max(1LL,choose6[N-1][5]/limit6);
 auto checkpoint=[&](const char*phase){if(!full)return;string path=argv[8],tmp=path+".tmp";ofstream out(tmp);out<<"{\"partial\":true,\"phase\":\""<<phase<<"\",\"q4_processed\":"<<n4<<",\"q6_processed\":"<<n6<<",\"cpu_seconds\":"<<double(clock()-start)/CLOCKS_PER_SEC<<",\"T_norm_raw\":\""<<sum6.norm<<"\",\"CT_norm_raw\":\""<<sum4.ctnorm<<"\",\"T_K_T_raw\":\""<<sum6.tkt<<"\"";export_vector(out,"q4_G_raw",sum4.G);export_vector(out,"q4_H_raw",sum4.H);export_vector(out,"q4_J_raw",sum4.J);export_vector(out,"q6_G_raw",sum6.G);export_vector(out,"q6_H_raw",sum6.H);export_vector(out,"q6_J_raw",sum6.J);out<<"}\n";out.close();assert(rename(tmp.c_str(),path.c_str())==0);};
 clock_t begin4=clock();combinations(4,!fixture,[&](const int*sites){if(i4++%stride4)return;Scalar ct=CT(sites);Ten l=L(sites),r=R(sites),dr=image_preserve(sites,1,a4),cm=image_CM(sites);sum4.ctnorm+=dot(ct,ct,a4);for(int j=0;j<d;j++){auto lc=dot(ct,col(l,j,3),a4),rr=dot(ct,col(r,j,3),a4),dd=dot(ct,col(dr,j,3),a4),cc=dot(ct,col(cm,j,3),a4);sum4.H[1+d+j]+=11*lc;sum4.H[1+2*d+j]+=11*rr;sum4.J[1+j]+=121*lc;sum4.J[1+d+j]+=8800*lc+121*rr;sum4.J[1+2*d+j]+=8800*rr+121*dd;sum4.J[1+3*d+j]+=242*cc;}if(fixture)expand(physical,sites,ct,4,1);n4++;if(n4%1024==0)checkpoint("q4");});checkpoint("q4_complete");double q4cpu=double(clock()-begin4)/CLOCKS_PER_SEC;
 clock_t begin6=clock();combinations(6,!fixture,[&](const int*sites){if(i6++%stride6)return;Scalar t=T(sites);assert(t==raw_T(sites));for(int a=0;a<6;a++){assert(T(sites,a)==t);anchors++;}Scalar dt=DT(sites,t),kt=K_action(sites,t,[](const int*s){return T(s);}),u{};for(int p=0;p<15;p++)u[p]=safe_add(safe_mul(t[p],1200),safe_mul(dt[p],11));Ten m=M(sites),dm=image_preserve(sites,2,a6),cr=image_CR(sites);bool active=false;for(int p=0;p<15;p++)for(int j=0;j<d;j++)active|=m[p][j]!=0;if(!active&&dot(t,t,a6)!=0)nzero++;
 auto tn=dot(t,t,a6),tk=dot(t,kt,a6);sum6.norm+=tn;sum6.tkt+=tk;sum6.H.back()+=1200*tn+11*dot(t,dt,a6);sum6.J.back()+=dot(u,u,a6);for(int j=0;j<d;j++){Scalar mc=col(m,j,15),hm=col(dm,j,15);for(int p=0;p<15;p++)hm[p]=safe_add(safe_mul(mc[p],1200),safe_mul(hm[p],11));sum6.G[1+3*d+j]+=dot(t,mc,a6);sum6.H[1+3*d+j]+=dot(t,hm,a6);sum6.J[1+d+j]+=11*dot(u,mc,a6);sum6.J[1+2*d+j]+=11*dot(u,col(cr,j,15),a6);sum6.J[1+3*d+j]+=dot(u,hm,a6)+121*dot(kt,mc,a6);}if(fixture){expand(physical,sites,t,6,0);expand(physical,sites,dt,6,2);expand(physical,sites,kt,6,3);}n6++;if(n6%4096==0)checkpoint("q6");});checkpoint("q6_complete");double q6cpu=double(clock()-begin6)/CLOCKS_PER_SEC;
 sum6.G.back()=sum6.norm;sum4.J.back()=242*sum4.ctnorm;sum6.J.back()+=121*sum6.tkt;
 if(full){assert(n4==(size_t)choose6[N-1][3]&&n6==(size_t)choose6[N-1][5]);auto normalize=[&](mpz_class&x,int q){x*=N;assert(x%q==0);x/=q;};for(auto pair:{make_pair(&sum4,4),make_pair(&sum6,6)}){auto&x=*pair.first;int q=pair.second;for(auto v:{&x.G,&x.H,&x.J})for(auto&z:*v)normalize(z,q);normalize(x.norm,q);normalize(x.ctnorm,q);normalize(x.tkt,q);}}
 if(fixture){ofstream out(argv[8]);for(auto&[state,amplitudes]:physical){bool nonzero=false;for(Int x:amplitudes)nonzero|=x!=0;if(nonzero){out<<state;for(Int x:amplitudes)out<<' '<<number(x);out<<'\n';}}}
 vector<mpz_class>G=sum4.G,H=sum4.H,J=sum4.J;for(size_t j=0;j<G.size();j++){G[j]+=sum6.G[j];H[j]+=sum6.H[j];J[j]+=sum6.J[j];}
 rusage ru{};getrusage(RUSAGE_SELF,&ru);cout<<"{\"mode\":\""<<mode<<"\",\"N\":"<<N<<",\"d\":"<<d<<",\"partial\":"<<((fixture||full)?"false":"true")<<",\"q4_processed\":"<<n4<<",\"q6_processed\":"<<n6<<",\"cache_fills\":"<<fills<<",\"lookup_calls\":"<<queries<<",\"M_zero_T_nonzero\":"<<nzero<<",\"anchor_checks\":"<<anchors<<",\"r_cache_cpu_seconds\":"<<rcpu<<",\"q4_cpu_seconds\":"<<q4cpu<<",\"q6_cpu_seconds\":"<<q6cpu<<",\"cpu_seconds\":"<<double(clock()-start)/CLOCKS_PER_SEC<<",\"peak_rss_kib\":"<<ru.ru_maxrss<<",\"T_norm\":\""<<sum6.norm<<"\",\"CT_norm\":\""<<sum4.ctnorm<<"\",\"T_K_T\":\""<<sum6.tkt<<"\",\"q8_creation_norm\":\""<<sum4.ctnorm+sum6.tkt<<"\"";export_vector(cout,"G",G);export_vector(cout,"H200",H);export_vector(cout,"H200_squared",J);cout<<"}\n";
}
