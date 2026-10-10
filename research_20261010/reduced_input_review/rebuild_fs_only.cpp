// Independent reduced matching contraction. Enumerates four-site subsets only.
// Derived from the prior independently reviewed kernel; no H-squared contractions.
// Input graph/orbit classification is built independently by audit_large.py.
#include <array>
#include <vector>
#include <map>
#include <fstream>
#include <iostream>
#include <cassert>
#include <cstdint>
#include <numeric>
using namespace std;
using I=long long;
using V=array<I,20>;
using M=array<array<I,20>,20>;
int n,d,e[64][64]{},o[64][64]{};
vector<vector<int>> allpairs(int k) {
 vector<vector<int>> out;
 auto rec=[&](auto&& self, vector<int> rem, vector<int> p)->void {
  if(rem.empty()){out.push_back(p);return;}
  int a=rem[0];
  for(unsigned j=1;j<rem.size();++j){auto r=rem;int b=r[j];r.erase(r.begin()+j);r.erase(r.begin());auto z=p;z.push_back(a);z.push_back(b);self(self,r,z);}
 };
 vector<int> v(k);iota(v.begin(),v.end(),0);rec(rec,v,{});return out;
}
int loops(const vector<int>&p,const vector<int>&q){
 vector<int> v(p.size());iota(v.begin(),v.end(),0);
 auto root=[&](int x){while(v[x]!=x)x=v[x];return x;};
 for(auto *a:{&p,&q})for(unsigned k=0;k<a->size();k+=2)v[root((*a)[k])]=root((*a)[k+1]);
 int z=0;for(unsigned k=0;k<v.size();++k)z+=root(k)==int(k);int g=1;while(z--)g*=3;return g;
}
V first(const array<int,4>& s,const vector<int>& p){V v{};v[o[s[p[2]]][s[p[3]]]]+=e[s[p[0]]][s[p[1]]];v[o[s[p[0]]][s[p[1]]]]+=e[s[p[2]]][s[p[3]]];return v;}
void add(V&u,const V&v,I f){for(int i=0;i<d;++i)u[i]+=f*v[i];}
void outer(M& m,const V&u,const V&v,I f){for(int i=0;i<d;++i)if(u[i])for(int j=0;j<d;++j)if(v[j])m[i][j]+=f*u[i]*v[j];}
int main(int argc,char**argv){assert(argc==3);ifstream in(argv[1]);in>>n>>d;int ne;in>>ne;assert(n<=64&&d<=20);for(int z=0;z<ne;++z){int i,j,w;in>>i>>j>>w;e[i][j]=e[j][i]=w;}for(int i=0;i<n;++i)for(int j=i+1;j<n;++j){in>>o[i][j];o[j][i]=o[i][j];}
 auto p4=allpairs(4);M f{},s{};I n4=0;int g4[3][3];for(int i=0;i<3;++i)for(int j=0;j<3;++j)g4[i][j]=loops(p4[i],p4[j]);
 for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)for(int c=b+1;c<n;++c)for(int dd=c+1;dd<n;++dd){
  ++n4;array<int,4> sites={a,b,c,dd};V l[3]{},r[3]{};for(int p=0;p<3;++p)l[p]=first(sites,p4[p]);
  for(int i=0;i<4;++i)for(int h=0;h<n;++h)if(e[sites[i]][h]&&h!=a&&h!=b&&h!=c&&h!=dd){auto src=sites;src[i]=h;for(int p=0;p<3;++p)add(r[p],first(src,p4[p]),e[sites[i]][h]);}
  for(int p=0;p<3;++p){int partner[4];for(int z=0;z<4;z+=2){partner[p4[p][z]]=p4[p][z+1];partner[p4[p][z+1]]=p4[p][z];}
   for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)if(e[sites[i]][sites[j]]){
    int h=e[sites[i]][sites[j]];
    if(partner[i]==j){add(r[p],l[p],-2*h);continue;}
    int x=partner[i],y=partner[j];int pp[4]={};pp[i]=y;pp[y]=i;pp[j]=x;pp[x]=j;int cc[4]={};cc[i]=j;cc[j]=i;cc[x]=y;cc[y]=x;
    for(int z=0;z<3;++z){bool swap=true,contract=true;for(int k=0;k<4;k+=2){swap&=pp[p4[z][k]]==p4[z][k+1];contract&=cc[p4[z][k]]==p4[z][k+1];}if(swap)add(r[z],l[p],h);if(contract)add(r[z],l[p],-h);}
   }
  }
  for(int p=0;p<3;++p)for(int j=0;j<d;++j){assert(l[p][j]>=-2&&l[p][j]<=2);assert(r[p][j]>=-128&&r[p][j]<=128);}
  for(int p=0;p<3;++p)for(int q=0;q<3;++q){outer(f,l[p],l[q],g4[p][q]);outer(s,l[p],r[q],g4[p][q]);}
 }
 cerr<<"all q4 subsets "<<n4<<" checked\n";
 ofstream out(argv[2]);out<<"{\"N\":"<<n<<",\"orbits\":"<<d<<",\"all_q4\":"<<n4;
 auto emit=[&](const char*name,M&m){out<<",\""<<name<<"\":[";for(int i=0;i<d;++i){if(i)out<<",";out<<"[";for(int j=0;j<d;++j){if(j)out<<",";out<<m[i][j];}out<<"]";}out<<"]";};emit("F",f);emit("S",s);out<<"}\n";
}
