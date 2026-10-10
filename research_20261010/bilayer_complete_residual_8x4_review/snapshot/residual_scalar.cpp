// Exact matching contractions X=R* A44 R, Y=R* A46 M, Z=M* A66 M.
// L=A42 B, R=A44 L, M=A64 L. No states with q>=8 are ever generated.
#include <gmpxx.h>
#include <climits>
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
#include <sys/resource.h>
using namespace std;
using I=__int128_t;
using BI=mpz_class;
constexpr int D=14;
struct V {int x[D]{};};
struct R4 {V x[3];};
struct Mat {I x[D][D]{};};
int N,d,m[64][64],orb[64][64],gram[15][15],swap6[15][6][6],contract6[15][6][6];
vector<pair<int,int>> adj[64]; vector<array<int,3>> edges;
const int p4[3][4]={{0,1,2,3},{0,2,1,3},{0,3,1,2}};
vector<array<int,6>> p6; long long choose[65][7]; vector<R4> cache;
void pairs(vector<int> rest,array<int,6> a,int pos){if(pos==6){p6.push_back(a);return;}int i=rest[0];for(int j=1;j<(int)rest.size();j++){a[pos]=i;a[pos+1]=rest[j];vector<int> r;for(int k=1;k<(int)rest.size();k++)if(k!=j)r.push_back(rest[k]);pairs(r,a,pos+2);}}
int matchidx(const int* partner,int q){if(q==4){for(int p=0;p<3;p++)if(partner[0]==p4[p][1])return p;}else for(int p=0;p<15;p++){bool ok=true;for(int k=0;k<6;k+=2)ok&=partner[p6[p][k]]==p6[p][k+1];if(ok)return p;}assert(false);return -1;}
void add(V& a,const V& b,int w){for(int i=0;i<d;i++){long long z=(long long)a.x[i]+(long long)b.x[i]*w;assert(z>=INT_MIN&&z<=INT_MAX);a.x[i]=(int)z;}}
V Lpair(int a,int b,int c,int e){V z{};z.x[orb[c][e]]+=m[a][b];z.x[orb[a][b]]+=m[c][e];return z;}
void Lval(const int* st,V* out){for(int p=0;p<3;p++)out[p]=Lpair(st[p4[p][0]],st[p4[p][1]],st[p4[p][2]],st[p4[p][3]]);}
long long rank4(const int* st){return choose[st[0]][1]+choose[st[1]][2]+choose[st[2]][3]+choose[st[3]][4];}
void Rlookup(const int* st,V* out){int sorted[4];copy(st,st+4,sorted);sort(sorted,sorted+4);int perm[4];for(int i=0;i<4;i++)perm[i]=find(sorted,sorted+4,st[i])-sorted;const auto& r=cache[rank4(sorted)];for(int p=0;p<3;p++){int partner[4];for(int k=0;k<4;k+=2){int i=perm[p4[p][k]],j=perm[p4[p][k+1]];partner[i]=j;partner[j]=i;}out[p]=r.x[matchidx(partner,4)];}}
template<class Lookup> void preserve4(const int* st,V* out,Lookup lookup){V a[3];lookup(st,a);uint64_t mask=0;for(int i=0;i<4;i++)mask|=1ULL<<st[i];
 for(int i=0;i<4;i++)for(auto [j,w]:adj[st[i]])if(!(mask>>j&1)){int src[4];copy(st,st+4,src);src[i]=j;V z[3];lookup(src,z);for(int p=0;p<3;p++)add(out[p],z[p],w);}
 for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)if(m[st[i]][st[j]])for(int p=0;p<3;p++){int part[4];for(int k=0;k<4;k+=2){part[p4[p][k]]=p4[p][k+1];part[p4[p][k+1]]=p4[p][k];}int w=m[st[i]][st[j]];if(part[i]==j)add(out[p],a[p],-2*w);else{int k=part[i],l=part[j],sw[4],co[4];sw[i]=l;sw[l]=i;sw[j]=k;sw[k]=j;co[i]=j;co[j]=i;co[k]=l;co[l]=k;add(out[matchidx(sw,4)],a[p],w);add(out[matchidx(co,4)],a[p],-w);}}
}
void Mval(const int* st,V* out){for(int p=0;p<15;p++){int mul[3],id[3];for(int k=0;k<3;k++){int a=st[p6[p][2*k]],b=st[p6[p][2*k+1]];mul[k]=m[a][b];id[k]=orb[a][b];}for(int k=0;k<3;k++)if(mul[(k+1)%3]&&mul[(k+2)%3])out[p].x[id[k]]+=2*mul[(k+1)%3]*mul[(k+2)%3];}}
void preserve6(const int* st,const V* a,V* out){uint64_t mask=0;for(int i=0;i<6;i++)mask|=1ULL<<st[i];for(int i=0;i<6;i++)for(auto [j,w]:adj[st[i]])if(!(mask>>j&1)){int src[6];copy(st,st+6,src);src[i]=j;
 // Inline sparse pull, avoiding a dense temporary for the 15 matchings.
 for(int p=0;p<15;p++){int mul[3],id[3];for(int k=0;k<3;k++){int a=src[p6[p][2*k]],b=src[p6[p][2*k+1]];mul[k]=m[a][b];id[k]=orb[a][b];}for(int k=0;k<3;k++)if(mul[(k+1)%3]&&mul[(k+2)%3])out[p].x[id[k]]+=2*w*mul[(k+1)%3]*mul[(k+2)%3];}}
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(m[st[i]][st[j]])for(int p=0;p<15;p++){int w=m[st[i]][st[j]];if(swap6[p][i][j]<0)add(out[p],a[p],-2*w);else{add(out[swap6[p][i][j]],a[p],w);add(out[contract6[p][i][j]],a[p],-w);}}
}
void create6(const int* st,V* out){for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(m[st[i]][st[j]]){int rem[4],idx[4],n=0;for(int k=0;k<6;k++)if(k!=i&&k!=j){rem[n]=st[k];idx[n++]=k;}const auto& r=cache[rank4(rem)];for(int p=0;p<3;p++){int partner[6];partner[i]=j;partner[j]=i;for(int k=0;k<4;k+=2){int a=idx[p4[p][k]],b=idx[p4[p][k+1]];partner[a]=b;partner[b]=a;}add(out[matchidx(partner,6)],r.x[p],m[st[i]][st[j]]);}}}
void contract(Mat& out,const V* a,const V* b,int q){int nm=q==4?3:15;for(int p=0;p<nm;p++)for(int i=0;i<d;i++)if(a[p].x[i])for(int r=0;r<nm;r++){int w=q==4?(p==r?9:3):gram[p][r];for(int j=0;j<d;j++)if(b[r].x[j]){I term=(I)a[p].x[i]*b[r].x[j]*w;I result;assert(!__builtin_add_overflow(out.x[i][j],term,&result));out.x[i][j]=result;}}}
string str(I a){if(!a)return "0";bool neg=a<0;if(neg)a=-a;string s;while(a){s.push_back('0'+a%10);a/=10;}if(neg)s.push_back('-');reverse(s.begin(),s.end());return s;}
void emit(ofstream& o,const char* key,const Mat& a,int divisor,bool fixed){o<<",\n\""<<key<<"\":[";for(int i=0;i<d;i++){if(i)o<<",";o<<"[";for(int j=0;j<d;j++){if(j)o<<",";I z=a.x[i][j];if(fixed){assert(z*N%divisor==0);z=z*N/divisor;}o<<str(z);}o<<"]";}o<<"]";}
I cu[D]{},cl[D]{},cb[D]{},den,hh;
I dotv(const V& a,const I* c){I z=0;for(int i=0;i<d;i++){I term,zz;assert(!__builtin_mul_overflow((I)a.x[i],c[i],&term));assert(!__builtin_add_overflow(z,term,&zz));z=zz;}return z;}
long checked64(I a){assert(a>=LONG_MIN && a<=LONG_MAX);return (long)a;}
BI inner(const I* a,const I* b,int q){int nm=q==4?3:15;BI out=0;for(int p=0;p<nm;p++)if(a[p])for(int r=0;r<nm;r++)if(b[r])out+=BI(checked64(a[p]))*BI(checked64(b[r]))*(q==4?(p==r?9:3):gram[p][r]);return out;}
void annihilateM(const int* st,V* out){uint64_t mask=0;for(int k=0;k<4;k++)mask|=1ULL<<st[k];for(auto ed:edges){int i=ed[0],j=ed[1],w=ed[2];if((mask>>i&1)||(mask>>j&1))continue;int src[6];copy(st,st+4,src);src[4]=i;src[5]=j;V a[15]{};Mval(src,a);
 for(int p=0;p<15;p++){int part[6];for(int k=0;k<6;k+=2){part[p6[p][k]]=p6[p][k+1];part[p6[p][k+1]]=p6[p][k];}int f=1;if(part[4]==5)f=3;else{int x=part[4],y=part[5];part[x]=y;part[y]=x;}add(out[matchidx(part,4)],a[p],f*w);}
}}
void commM(const int* st,const V* a,V* out){uint64_t mask=0;for(int k=0;k<6;k++)mask|=1ULL<<st[k];int vac=0;for(auto ed:edges)if(!(mask>>ed[0]&1)&&!(mask>>ed[1]&1))vac+=3*ed[2]*ed[2];for(int p=0;p<15;p++)add(out[p],a[p],vac);
 // Same-edge occupied singlet projector with its required minus sign.
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(m[st[i]][st[j]])for(int p=0;p<15;p++){int w=m[st[i]][st[j]];if(swap6[p][i][j]<0)add(out[p],a[p],-3*w*w);else add(out[contract6[p][i][j]],a[p],-w*w);}
 // Ordered wedges pulled from the target's occupied endpoint k.
 for(int k=0;k<6;k++)for(auto [center,wik]:adj[st[k]]){
  int pos=-1;for(int i=0;i<6;i++)if(st[i]==center)pos=i;
  for(auto [j,wij]:adj[center])if(j!=st[k]&&!(mask>>j&1)){
   int src[6];copy(st,st+6,src);src[k]=j;V b[15]{};Mval(src,b);int w=wik*wij;
   if(pos<0){for(int p=0;p<15;p++)add(out[p],b[p],w);}
   else {int ii=min(pos,k),jj=max(pos,k);for(int p=0;p<15;p++){if(swap6[p][ii][jj]<0)add(out[p],b[p],-3*w);else add(out[contract6[p][ii][jj]],b[p],-w);}}
  }
 }
}
BI scaled(BI value,int q,bool fixed){if(fixed){value*=N;assert(value%q==0);value/=q;}return value;}
int main(int argc,char**argv){assert(argc>=4);bool fixed=argc<5||string(argv[4])!="full";size_t limit=argc>5?stoull(argv[5]):0;ifstream in(argv[1]);in>>N>>d;assert(N<=64&&d<=D);int E;in>>E;for(int k=0;k<E;k++){int a,b,w;in>>a>>b>>w;m[a][b]=m[b][a]=w;adj[a].push_back({b,w});adj[b].push_back({a,w});edges.push_back({a,b,w});}for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)in>>orb[i][j],orb[j][i]=orb[i][j];
 ifstream cf(argv[3]);long long x;cf>>x;den=x;cf>>x;hh=x;for(int i=0;i<d;i++){cf>>x;cb[i]=x;}for(int i=0;i<d;i++){cf>>x;cl[i]=x;}for(int i=0;i<d;i++){cf>>x;cu[i]=x;}assert(cf);
 for(int n=0;n<=64;n++){choose[n][0]=1;for(int k=1;k<=6;k++)choose[n][k]=n?choose[n-1][k-1]+choose[n-1][k]:0;}pairs({0,1,2,3,4,5},{},0);for(int p=0;p<15;p++)for(int r=0;r<15;r++){int parent[6];iota(parent,parent+6,0);auto root=[&](int i){while(parent[i]!=i)i=parent[i];return i;};for(auto v:{p6[p],p6[r]})for(int k=0;k<6;k+=2)parent[root(v[k])]=root(v[k+1]);int w=1;for(int i=0;i<6;i++)if(root(i)==i)w*=3;gram[p][r]=w;}
 for(int p=0;p<15;p++)for(int i=0;i<6;i++)for(int j=i+1;j<6;j++){int part[6];for(int k=0;k<6;k+=2){part[p6[p][k]]=p6[p][k+1];part[p6[p][k+1]]=p6[p][k];}if(part[i]==j){swap6[p][i][j]=-1;continue;}int k=part[i],l=part[j],sw[6],co[6];copy(part,part+6,sw);copy(part,part+6,co);sw[i]=l;sw[l]=i;sw[j]=k;sw[k]=j;co[i]=j;co[j]=i;co[k]=l;co[l]=k;swap6[p][i][j]=matchidx(sw,6);contract6[p][i][j]=matchidx(co,6);}
 auto start=chrono::steady_clock::now();auto sec=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};cache.resize(choose[N][4]);for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){int st[4]={a,b,c,e};preserve4(st,cache[rank4(st)].x,Lval);}
 double cached=sec();BI nq4=0,nq6=0,nCM=0,ncomm=0,nP=0,nT=0,nq6_Mzero=0,nT_Mzero=0;size_t q4total= fixed?choose[N-1][3]:choose[N][4],q6total=fixed?choose[N-1][5]:choose[N][6],n4=0,n6=0,active6=0,idx4=0,idx6=0;
 size_t stride4=limit?max((size_t)1,q4total/limit):1,stride6=limit?max((size_t)1,q6total/limit):1;
 for(int a=0;a<(fixed?1:N);a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){
  if((idx4++)%stride4)continue;int st[4]={a,b,c,e};V l[3]{},rr[3]{},cm[3]{};Lval(st,l);const auto&r=cache[rank4(st)];preserve4(st,rr,Rlookup);annihilateM(st,cm);I y[3],cmv[3],pv[3];I lc[D],rc[D];for(int j=0;j<d;j++){lc[j]=4*den*cl[j]+hh*cb[j];rc[j]=hh*cl[j]+4*den*cu[j];}for(int p=0;p<3;p++){cmv[p]=dotv(cm[p],cu);pv[p]=dotv(rr[p],cu)+cmv[p];y[p]=dotv(l[p],lc)+dotv(r.x[p],rc)+hh*pv[p];}nq4+=inner(y,y,4);nCM+=inner(cmv,cmv,4);nP+=inner(pv,pv,4);n4++;
 }
 double time4=sec();
 for(int a=0;a<(fixed?1:N);a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++)for(int f=e+1;f<N;f++)for(int g=f+1;g<N;g++){
  if((idx6++)%stride6)continue;int st[6]={a,b,c,e,f,g};V mv[15]{},dm[15]{},cr[15]{},km[15]{};Mval(st,mv);preserve6(st,mv,dm);create6(st,cr);I y[15],mamp[15],kamp[15],tv[15];I mc[D];for(int j=0;j<d;j++)mc[j]=hh*cl[j]+6*den*cu[j];bool active=false;
  for(int p=0;p<15;p++){mamp[p]=dotv(mv[p],cu);active|=mamp[p]!=0;tv[p]=dotv(dm[p],cu)+dotv(cr[p],cu);y[p]=dotv(mv[p],mc)+hh*tv[p];}
  bool family_active=false;for(int p=0;p<15;p++)for(int j=0;j<d;j++)family_active|=mv[p].x[j]!=0;BI ny=inner(y,y,6),nt=inner(tv,tv,6);nq6+=ny;nT+=nt;if(!family_active){nq6_Mzero+=ny;nT_Mzero+=nt;}if(active){commM(st,mv,km);for(int p=0;p<15;p++)kamp[p]=dotv(km[p],cu);ncomm+=inner(mamp,kamp,6);active6++;}n6++;
 }
 double total=sec();rusage usage{};getrusage(RUSAGE_SELF,&usage);bool partial=limit>0;
 ofstream o(argv[2]);o<<"{\n\"N\":"<<N<<",\"d\":"<<d<<",\"fixed_origin\":"<<(fixed?"true":"false")<<",\"partial\":"<<(partial?"true":"false")<<",\"q4_total\":"<<q4total<<",\"q6_total\":"<<q6total<<",\"q4_processed\":"<<n4<<",\"q6_processed\":"<<n6<<",\"M_active_processed\":"<<active6<<",\"cache_seconds\":"<<cached<<",\"q4_seconds\":"<<time4-cached<<",\"q6_seconds\":"<<total-time4<<",\"seconds\":"<<total<<",\"peak_rss_kib\":"<<usage.ru_maxrss;
 auto emit=[&](const char*key,BI value,int q){o<<",\n\""<<key<<"\":\""<<(partial?value:scaled(value,q,fixed))<<"\"";};emit("Tpsi_q4_norm",nq4,4);emit("Tpsi_q6_norm",nq6,6);emit("CM_norm",nCM,4);emit("commutator_expectation",ncomm,6);emit("P_norm",nP,4);emit("T_norm",nT,6);emit("Tpsi_q6_norm_on_M_zero_supports",nq6_Mzero,6);emit("T_norm_on_M_zero_supports",nT_Mzero,6);if(!partial){BI q8=scaled(nCM,4,fixed)+scaled(ncomm,6,fixed);assert(q8>=0);o<<",\n\"q8_creation_norm\":\""<<q8<<"\"";}o<<"\n}\n";
 cerr<<"N "<<N<<" partial "<<partial<<" seconds "<<total<<" RSS "<<usage.ru_maxrss<<" q4 "<<n4<<" q6 "<<n6<<endl;
}
