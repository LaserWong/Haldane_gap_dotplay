// Exact integer singlet-matching contractions. No physical configurations.
// Input N d, edges with multiplicities, pair orbit ids (0..d-1, vacuum excluded).
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
using ll=long long;
constexpr int D=20;
struct Mat { ll x[D][D]{}; };
struct Vec { int x[D]{}; };
int N,d,m[64][64],orb[64][64];
vector<pair<int,int>> adj[64];
vector<array<int,3>> edges;
int match4[3][4]={{0,1,2,3},{0,2,1,3},{0,3,1,2}};
vector<array<int,6>> match6;
void pairings(vector<int> rest,array<int,6> a,int pos){
 if(pos>=6){assert(pos==6 && rest.empty());match6.push_back(a);return;}
 assert(!rest.empty()); int first=rest[0];
 for(int j=1;j<(int)rest.size();j++){a[pos]=first;a[pos+1]=rest[j];vector<int> rem;
 for(int k=1;k<(int)rest.size();k++){if(k!=j)rem.push_back(rest[k]);}
 pairings(rem,a,pos+2);}
}
void outer(Mat& A,const Vec& x,const Vec& y,int scale){
 for(int i=0;i<d;i++)if(x.x[i])for(int j=0;j<d;j++)if(y.x[j])A.x[i][j]+=(ll)scale*x.x[i]*y.x[j];
}
void contract4(Mat& A,Vec* x,Vec* y){Vec sx{},sy{};for(int p=0;p<3;p++){
 outer(A,x[p],y[p],6);for(int i=0;i<d;i++){sx.x[i]+=x[p].x[i];sy.x[i]+=y[p].x[i];}}
 outer(A,sx,sy,3);
}
Vec lvec(int a,int b,int c,int e){Vec z{};z.x[orb[c][e]]+=m[a][b];z.x[orb[a][b]]+=m[c][e];return z;}
void add(Vec& x,const Vec& y,int scale){for(int i=0;i<d;i++)x.x[i]+=scale*y.x[i];}
int pairing4(int* partners){for(int p=0;p<3;p++)if(partners[match4[p][0]]==match4[p][1])return p;assert(false);return -1;}
int main(int argc,char**argv){
 assert(argc==3);ifstream in(argv[1]);in>>N>>d;assert(N<=64&&d<=D);int E;in>>E;
 for(int z=0;z<E;z++){int i,j,k;in>>i>>j>>k;m[i][j]=m[j][i]=k;adj[i].push_back({j,k});adj[j].push_back({i,k});edges.push_back({i,j,k});}
 for(int i=0;i<N;i++){int degree=0;for(auto [j,mul]:adj[i]){assert(mul>=1 && mul<=2);degree+=mul;}assert(degree==4);}
 for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){int k;in>>k;orb[i][j]=orb[j][i]=k;assert(k>=0&&k<d);}
 Mat F{},S{},V{},W{};ll count4=0,active4=0;auto t0=chrono::steady_clock::now();
 for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){
  int st[4]={a,b,c,e};uint64_t mask=(1ULL<<a)|(1ULL<<b)|(1ULL<<c)|(1ULL<<e);Vec L[3],R[3]{};bool active=false;
  for(int p=0;p<3;p++){int* f=match4[p];L[p]=lvec(st[f[0]],st[f[1]],st[f[2]],st[f[3]]);}
  // DD hopping: pull L from each source differing by one graph hop.
  for(int r=0;r<4;r++)for(auto [v,mul]:adj[st[r]])if(!(mask&(1ULL<<v))){
    int source[4]={a,b,c,e};source[r]=v;
    for(int p=0;p<3;p++){int*f=match4[p];add(R[p],lvec(source[f[0]],source[f[1]],source[f[2]],source[f[3]]),mul);}
  }
  // TT on occupied sites: swap minus contraction, with loop value 3.
  for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)if(m[st[i]][st[j]]){
    int mul=m[st[i]][st[j]];
    for(int p=0;p<3;p++){
      int partner[4];int*f=match4[p];partner[f[0]]=f[1];partner[f[1]]=f[0];partner[f[2]]=f[3];partner[f[3]]=f[2];
      if(partner[i]==j)add(R[p],L[p],-2*mul);
      else {int k=partner[i],l=partner[j],sw[4],co[4];sw[i]=l;sw[l]=i;sw[j]=k;sw[k]=j;co[i]=j;co[j]=i;co[k]=l;co[l]=k;
       add(R[pairing4(sw)],L[p],mul);add(R[pairing4(co)],L[p],-mul);}
    }
  }
  for(int p=0;p<3;p++)for(int i=0;i<d;i++)if(L[p].x[i]||R[p].x[i])active=true;
  ++count4;if(active){++active4;contract4(F,L,L);contract4(S,L,R);contract4(V,R,R);}
 }
 double sec4=chrono::duration<double>(chrono::steady_clock::now()-t0).count();cerr<<"q4 subsets "<<count4<<", active "<<active4<<", seconds "<<sec4<<endl;
 // Generate only q6 sets containing two disjoint graph edges.
 vector<uint64_t> masks;size_t upper=0;for(size_t e=0;e<edges.size();e++)for(size_t f=e+1;f<edges.size();f++){
   auto x=edges[e],y=edges[f];if(x[0]==y[0]||x[0]==y[1]||x[1]==y[0]||x[1]==y[1])continue;
   upper+=(N-4)*(N-5)/2;
 }
 masks.reserve(upper);for(size_t e=0;e<edges.size();e++)for(size_t f=e+1;f<edges.size();f++){
   auto x=edges[e],y=edges[f];if(x[0]==y[0]||x[0]==y[1]||x[1]==y[0]||x[1]==y[1])continue;
   uint64_t mask=(1ULL<<x[0])|(1ULL<<x[1])|(1ULL<<y[0])|(1ULL<<y[1]);
   for(int i=0;i<N;i++)if(!(mask&(1ULL<<i)))for(int j=i+1;j<N;j++)if(!(mask&(1ULL<<j)))masks.push_back(mask|(1ULL<<i)|(1ULL<<j));
 }
 sort(masks.begin(),masks.end());masks.erase(unique(masks.begin(),masks.end()),masks.end());
 pairings({0,1,2,3,4,5},{},0);assert(match6.size()==15);int gram6[15][15];
 for(int p=0;p<15;p++)for(int q=0;q<15;q++){
   int parent[6];iota(parent,parent+6,0);auto root=[&](int i){while(parent[i]!=i)i=parent[i];return i;};
   for(auto mat:{match6[p],match6[q]})for(int k=0;k<6;k+=2)parent[root(mat[k])]=root(mat[k+1]);
   int loops=0;for(int k=0;k<6;k++)if(root(k)==k)loops++;int weight=1;while(loops--)weight*=3;gram6[p][q]=weight;
 }
 for(uint64_t mask:masks){int st[6],idx=0;for(uint64_t mm=mask;mm;mm&=mm-1)st[idx++]=__builtin_ctzll(mm);assert(idx==6);
   Vec amps[15]{};int active[15],nactive=0;
   for(int p=0;p<15;p++){auto f=match6[p];int mul[3],id[3];for(int k=0;k<3;k++){int a=st[f[2*k]],b=st[f[2*k+1]];mul[k]=m[a][b];id[k]=orb[a][b];}
     bool nz=false;for(int k=0;k<3;k++)if(mul[(k+1)%3]&&mul[(k+2)%3]){amps[p].x[id[k]]+=2*mul[(k+1)%3]*mul[(k+2)%3];nz=true;}
     if(nz)active[nactive++]=p;
   }
   assert(nactive);for(int i=0;i<nactive;i++)for(int j=0;j<nactive;j++){int p=active[i],q=active[j];outer(W,amps[p],amps[q],gram6[p][q]);}
 }
 double total=chrono::duration<double>(chrono::steady_clock::now()-t0).count();cerr<<"q6 candidates "<<upper<<", unique "<<masks.size()<<", total seconds "<<total<<endl;
 ofstream out(argv[2]);out<<"{\n\"N\":"<<N<<",\"pair_orbits\":"<<d<<",\"four_subsets\":"<<count4<<",\"active_four_subsets\":"<<active4<<",\"six_candidates\":"<<upper<<",\"six_subsets\":"<<masks.size()<<",\"q4_seconds\":"<<sec4<<",\"total_seconds\":"<<total;
 auto emit=[&](const char* name,Mat&A){out<<",\n\""<<name<<"\":[";for(int i=0;i<d;i++){if(i)out<<",";out<<"[";for(int j=0;j<d;j++){if(j)out<<",";out<<A.x[i][j];}out<<"]";}out<<"]";};
 emit("F",F);emit("S",S);emit("V",V);emit("W",W);out<<"\n}\n";
}
