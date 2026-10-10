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
#include <gmpxx.h>
using Big=mpz_class;using Amp=array<Int,15>;
Int cb[D]{},cl[D]{},cu[D]{};long long den,hh;
Amp project(const Ten&t,const Int*c,const Algebra&a){Amp v{};for(int p=0;p<a.k;p++)for(int j=0;j<d;j++)v[p]+=(Int)t[p][j]*c[j];return v;}
Big big(Int z){return Big(number(z));}
Big form(const Amp&v,const Amp&w,const Algebra&a){Big z=0;for(int i=0;i<a.k;i++)if(v[i])for(int j=0;j<a.k;j++)if(w[j])z+=big(v[i])*big(w[j])*a.gram[i][j];return z;}
void axpy(Amp&v,const Amp&w,Int c,const Algebra&a){for(int i=0;i<a.k;i++)v[i]+=c*w[i];}
Amp get(const int*sites,int what,const Int*c){return project(what==0?L(sites):what==1?R(sites):M(sites),c,what==2?a6:a4);}
Amp preserve(const int*sites,int what,const Int*c,const Algebra&a){Amp v=get(sites,what,c),out{};
 for(int i=0;i<a.q;i++)for(int j=i+1;j<a.q;j++)if(E[sites[i]][sites[j]])for(int p=0;p<a.k;p++){Int w=E[sites[i]][sites[j]];if(a.p[p].mate[i]==j)out[p]-=2*w*v[p];else{out[a.swap[i][j][p]]+=w*v[p];out[a.cap[i][j][p]]-=w*v[p];}}
 for(int i=0;i<a.q;i++)for(auto[j,w]:neighbors[sites[i]]){bool occ=false;for(int k=0;k<a.q;k++)occ|=sites[k]==j;if(occ)continue;int source[6];copy(sites,sites+a.q,source);source[i]=j;axpy(out,get(source,what,c),w,a);}
 return out;
}
Amp CM(const int*sites){Amp out{};bool occupied[64]{};for(int i=0;i<4;i++)occupied[sites[i]]=true;
 for(int u=0;u<N;u++)if(!occupied[u])for(int v=u+1;v<N;v++)if(!occupied[v]&&E[u][v]){int source[6];copy(sites,sites+4,source);source[4]=u;source[5]=v;auto coeff=get(source,2,cu);
 for(int r=0;r<15;r++){auto z=a6.p[r];int f=1;if(z.mate[4]==5)f=3;else{int x=z.mate[4],y=z.mate[5];z.mate[x]=y;z.mate[y]=x;}out[index(a4,z)]+=f*E[u][v]*coeff[r];}}
 return out;
}
Amp CR(const int*sites){Amp out{};
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]]){int src[4],pos[4],n=0;for(int k=0;k<6;k++)if(k!=i&&k!=j){src[n]=sites[k];pos[n++]=k;}auto r=get(src,1,cu);for(int p=0;p<3;p++){Pairing z{};z.mate[i]=j;z.mate[j]=i;for(int k=0;k<4;k++)z.mate[pos[k]]=pos[a4.p[p].mate[k]];out[index(a6,z)]+=E[sites[i]][sites[j]]*r[p];}}
 return out;
}
Big Kform(const int*sites,const Amp&left){Big result=0;bool occ[64]{};for(int i=0;i<6;i++)occ[sites[i]]=true;
 int vac=0;for(int u=0;u<N;u++)if(!occ[u])for(auto[v,w]:neighbors[u])if(u<v&&!occ[v])vac+=3*w*w;result+=vac*form(left,left,a6);
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]]){Amp capped{};for(int p=0;p<15;p++)capped[a6.cap[i][j][p]]+=(a6.p[p].mate[i]==j?3:1)*left[p];int w=E[sites[i]][sites[j]];result-=w*w*form(left,capped,a6);}
 for(int k=0;k<6;k++)for(auto[center,w]:neighbors[sites[k]])for(auto[j,z]:neighbors[center])if(j!=sites[k]&&!occ[j]){int src[6];copy(sites,sites+6,src);src[k]=j;Amp incoming=get(src,2,cu);if(!occ[center])result+=w*z*form(left,incoming,a6);else{int i=find(sites,sites+6,center)-sites;int lo=min(i,k),hi=max(i,k);Amp capped{};for(int p=0;p<15;p++)capped[a6.cap[lo][hi][p]]+=(a6.p[p].mate[i]==k?3:1)*incoming[p];result-=w*z*form(left,capped,a6);}}
 return result;
}
int main(int argc,char**argv){assert(argc==5);bool origin=string(argv[4])=="origin";ifstream in(argv[1]);in>>N>>d;assert(N<=32&&d<=14);int count;in>>count;for(int k=0;k<count;k++){int i,j,w;in>>i>>j>>w;E[i][j]=E[j][i]=w;neighbors[i].push_back({j,w});neighbors[j].push_back({i,w});}for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){in>>orbit[i][j];orbit[j][i]=orbit[i][j];}
 ifstream coeff(argv[2]);long long a;coeff>>den>>hh;for(auto c:{cb,cl,cu})for(int i=0;i<d;i++){coeff>>a;c[i]=a;}assert(coeff);
 initialize(a4,4);initialize(a6,6);for(int n=0;n<=64;n++){choose[n][0]=1;for(int k=1;k<=4;k++)choose[n][k]=n?choose[n-1][k-1]+choose[n-1][k]:0;}
 auto start=chrono::steady_clock::now();Rcache.resize(choose[N][4]);for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){int st[4]={a,b,c,e};Ten r=Runcached(st);for(int p=0;p<3;p++)Rcache[rank4(st)][p]=r[p];}
 Big h4=0,h6=0,cmnorm=0,knorm=0,pnorm=0,tnorm=0,mzero=0,tzero=0;long long n4=0,n6=0;
 for(int a=0;a<(origin?1:N);a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){int st[4]={a,b,c,e};Amp cm=CM(st),p=preserve(st,1,cu,a4);axpy(p,cm,1,a4);cmnorm+=form(cm,cm,a4);pnorm+=form(p,p,a4);Amp y{};axpy(y,get(st,0,cb),hh,a4);axpy(y,get(st,0,cl),4*den,a4);axpy(y,get(st,1,cl),hh,a4);axpy(y,get(st,1,cu),4*den,a4);axpy(y,p,hh,a4);h4+=form(y,y,a4);n4++;}
 cerr<<"q4 complete "<<n4<<endl;
 for(int a=0;a<(origin?1:N);a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++)for(int f=e+1;f<N;f++)for(int g=f+1;g<N;g++){int st[6]={a,b,c,e,f,g};Amp mm=get(st,2,cu),t=preserve(st,2,cu,a6);axpy(t,CR(st),1,a6);Amp y{};axpy(y,mm,6*den,a6);axpy(y,get(st,2,cl),hh,a6);axpy(y,t,hh,a6);Big yy=form(y,y,a6),tt=form(t,t,a6);h6+=yy;tnorm+=tt;auto family=M(st);bool active=false;for(int p=0;p<15;p++)for(int j=0;j<d;j++)active|=family[p][j]!=0;if(!active){mzero+=yy;tzero+=tt;}bool scalar_active=false;for(auto v:mm)scalar_active|=v!=0;if(scalar_active)knorm+=Kform(st,mm);n6++;}
 auto scale=[&](Big x,int q)->Big{if(origin){x*=N;assert(x%q==0);x/=q;}return x;};ofstream out(argv[3]);out<<"{";bool first=true;auto emit=[&](const char*k,Big x,int q){if(!first)out<<",";first=false;out<<"\n\""<<k<<"\":\""<<scale(x,q)<<"\"";};emit("Tpsi_q4_norm",h4,4);emit("Tpsi_q6_norm",h6,6);emit("CM_norm",cmnorm,4);emit("commutator_expectation",knorm,6);emit("P_norm",pnorm,4);emit("T_norm",tnorm,6);emit("Tpsi_q6_norm_on_M_zero_supports",mzero,6);emit("T_norm_on_M_zero_supports",tzero,6);out<<",\n\"q8_creation_norm\":\""<<scale(cmnorm,4)+scale(knorm,6)<<"\",\n\"q4_processed\":"<<n4<<",\"q6_processed\":"<<n6<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}\n";
}
