// Exact matching contractions X=R* A44 R, Y=R* A46 M, Z=M* A66 M.
// L=A42 B, R=A44 L, M=A64 L. No states with q>=8 are ever generated.
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
void add(V& a,const V& b,int w){for(int i=0;i<d;i++)a.x[i]+=b.x[i]*w;}
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
int main(int argc,char**argv){assert(argc>=3);bool fixed=argc<4||string(argv[3])!="full";size_t limit=argc>4?stoull(argv[4]):0;ifstream in(argv[1]);in>>N>>d;assert(N<=64&&d<=D);int E;in>>E;for(int k=0;k<E;k++){int a,b,w;in>>a>>b>>w;m[a][b]=m[b][a]=w;adj[a].push_back({b,w});adj[b].push_back({a,w});edges.push_back({a,b,w});}for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)in>>orb[i][j],orb[j][i]=orb[i][j];
 for(int n=0;n<=64;n++){choose[n][0]=1;for(int k=1;k<=6;k++)choose[n][k]=n?choose[n-1][k-1]+choose[n-1][k]:0;}pairs({0,1,2,3,4,5},{},0);for(int p=0;p<15;p++)for(int r=0;r<15;r++){int parent[6];iota(parent,parent+6,0);auto root=[&](int i){while(parent[i]!=i)i=parent[i];return i;};for(auto v:{p6[p],p6[r]})for(int k=0;k<6;k+=2)parent[root(v[k])]=root(v[k+1]);int w=1;for(int i=0;i<6;i++)if(root(i)==i)w*=3;gram[p][r]=w;}
 for(int p=0;p<15;p++)for(int i=0;i<6;i++)for(int j=i+1;j<6;j++){int part[6];for(int k=0;k<6;k+=2){part[p6[p][k]]=p6[p][k+1];part[p6[p][k+1]]=p6[p][k];}if(part[i]==j){swap6[p][i][j]=-1;continue;}int k=part[i],l=part[j],sw[6],co[6];copy(part,part+6,sw);copy(part,part+6,co);sw[i]=l;sw[l]=i;sw[j]=k;sw[k]=j;co[i]=j;co[j]=i;co[k]=l;co[l]=k;swap6[p][i][j]=matchidx(sw,6);contract6[p][i][j]=matchidx(co,6);}
 auto start=chrono::steady_clock::now();auto sec=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};cache.resize(choose[N][4]);Mat F{},S{},Vv{},W{},X{},Y{},Z{};long long q4=0;
 for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){int st[4]={a,b,c,e};auto& r=cache[rank4(st)];preserve4(st,r.x,Lval);}
 double cached=sec();cerr<<"cached q4 "<<cache.size()<<" seconds "<<cached<<endl;
 for(int a=0;a<(fixed?1:N);a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){int st[4]={a,b,c,e};V l[3],rr[3]{};Lval(st,l);auto& r=cache[rank4(st)];preserve4(st,rr,Rlookup);contract(F,l,l,4);contract(S,l,r.x,4);contract(Vv,r.x,r.x,4);contract(X,r.x,rr,4);q4++;}
 double sec4=sec();cerr<<"q4 contraction "<<q4<<" seconds "<<sec4-cached<<endl;
 vector<uint64_t> masks;for(size_t a=0;a<edges.size();a++)for(size_t b=a+1;b<edges.size();b++){auto e=edges[a],f=edges[b];uint64_t mask=(1ULL<<e[0])|(1ULL<<e[1])|(1ULL<<f[0])|(1ULL<<f[1]);if(__builtin_popcountll(mask)!=4)continue;if(fixed&&!(mask&1)){for(int j=1;j<N;j++)if(!(mask>>j&1))masks.push_back(mask|1|(1ULL<<j));}else for(int i=0;i<N;i++)if(!(mask>>i&1))for(int j=i+1;j<N;j++)if(!(mask>>j&1))masks.push_back(mask|(1ULL<<i)|(1ULL<<j));}
 size_t candidates=masks.size();sort(masks.begin(),masks.end());masks.erase(unique(masks.begin(),masks.end()),masks.end());double prepared=sec();size_t count=limit?min(limit,masks.size()):masks.size();cerr<<"q6 unique "<<masks.size()<<" processing "<<count<<" preparation seconds "<<prepared-sec4<<endl;
 for(size_t n=0;n<count;n++){uint64_t mask=masks[limit?n*masks.size()/count:n];int st[6],idx=0;for(uint64_t mm=mask;mm;mm&=mm-1)st[idx++]=__builtin_ctzll(mm);assert(idx==6);V a[15]{},b[15]{},c[15]{};Mval(st,a);preserve6(st,a,b);create6(st,c);contract(W,a,a,6);contract(Y,c,a,6);contract(Z,a,b,6);}
 double total=sec();rusage usage{};getrusage(RUSAGE_SELF,&usage);cerr<<"DONE seconds "<<total<<" peak RSS KiB "<<usage.ru_maxrss<<endl;
 ofstream out(argv[2]);out<<"{\n\"N\":"<<N<<",\"pair_orbits\":"<<d<<",\"fixed_origin\":"<<(fixed?"true":"false")<<",\"partial_benchmark\":"<<(count<masks.size()?"true":"false")<<",\"q4_subsets\":"<<q4<<",\"q6_candidates\":"<<candidates<<",\"q6_subsets\":"<<masks.size()<<",\"q6_processed\":"<<count<<",\"cache_bytes\":"<<cache.size()*sizeof(R4)<<",\"cache_seconds\":"<<cached<<",\"q4_seconds\":"<<sec4-cached<<",\"q6_prepare_seconds\":"<<prepared-sec4<<",\"q6_contract_seconds\":"<<total-prepared<<",\"total_seconds\":"<<total<<",\"peak_rss_kib\":"<<usage.ru_maxrss;
 if(count==masks.size()){emit(out,"F",F,4,fixed);emit(out,"S",S,4,fixed);emit(out,"V",Vv,4,fixed);emit(out,"W",W,6,fixed);emit(out,"X",X,4,fixed);emit(out,"Y",Y,6,fixed);emit(out,"Z",Z,6,fixed);}out<<"\n}\n";
}
