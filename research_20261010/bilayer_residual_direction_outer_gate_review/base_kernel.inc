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
