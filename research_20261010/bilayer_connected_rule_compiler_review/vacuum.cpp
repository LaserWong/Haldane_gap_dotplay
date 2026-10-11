#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>
#include <sys/resource.h>
using namespace std;using I=__int128_t;using V=unordered_map<uint64_t,int64_t>;struct Edge{int a,b,w;};vector<Edge> edges;int N;long long ops=0;size_t maxstates=0;
string st(I x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;string z;while(x){z+=char('0'+x%10);x/=10;}if(neg)z+='-';reverse(z.begin(),z.end());return z;}
void add(V&v,uint64_t s,I x){I y=I(v[s])+x;assert(y>=INT64_MIN&&y<=INT64_MAX);if(y)v[s]=(int64_t)y;else v.erase(s);}
V sum(V a,const V&b,long long k=1){for(auto[s,x]:b)add(a,s,I(k)*x);maxstates=max(maxstates,a.size());return a;}
V scale(V a,long long k){V b;for(auto[s,x]:a)add(b,s,I(k)*x);return b;}
int q(uint64_t s){int r=0;for(int i=0;i<N;i++)r+=((s>>(2*i))&3)!=0;return r;}
int m(int z){return z==1?1:z==3?-1:0;}int indexm(int m){return m==1?1:m==-1?3:2;}
V sector(const V&v,int n){V a;for(auto[s,x]:v)if(q(s)==n)a[s]=x;return a;}
I dot(const V&a,const V&b){I z=0;for(auto[s,x]:a){auto it=b.find(s);if(it!=b.end())z+=I(x)*it->second;}return z;}I norm(const V&a){return dot(a,a);}
// Independent Cartesian local actions: delta creation/annihilation; swap minus delta contraction.
V cart(const V&v,int op){V out;for(auto [s,x]:v)for(auto e:edges){int a=s>>(2*e.a)&3,b=s>>(2*e.b)&3;uint64_t base=s&~((3ULL<<(2*e.a))|(3ULL<<(2*e.b)));auto put=[&](int c,int d,int f){add(out,base|(uint64_t(c)<<(2*e.a))|(uint64_t(d)<<(2*e.b)),I(x)*e.w*f);};if(op==0){if(a&&a==b)put(0,0,1);}else if(op==1){if(!a&&!b)for(int c=1;c<4;c++)put(c,c,1);}else if(bool(a)!=bool(b))put(b,a,1);else if(a&&b){put(b,a,1);if(a==b)for(int c=1;c<4;c++)put(c,c,-1);}}maxstates=max(maxstates,out.size());return out;}
V C(const V&v){return cart(v,0);}V Cd(const V&v){return cart(v,1);}V D(const V&v){return cart(v,2);}
V K(const V&v){return sum(C(Cd(v)),Cd(C(v)),-1);}V E(const V&v){return sum(D(Cd(v)),Cd(D(v)),-1);}V Ed(const V&v){return sum(C(D(v)),D(C(v)),-1);}V CE(const V&v){return sum(C(E(v)),E(C(v)),-1);}V EE(const V&v){return sum(Ed(E(v)),E(Ed(v)),-1);}V CK(const V&v){return sum(C(K(v)),K(C(v)),-1);}V L(const V&v){return sum(CK(Cd(v)),Cd(CK(v)),-1);}
V Q(const V&v){V a;for(auto[s,x]:v)add(a,s,I(q(s))*x);return a;}V H(const V&v,int d,int h){return sum(scale(Q(v),d),scale(sum(sum(C(v),Cd(v)),D(v)),h));}
V pairadd(V v,int a,int b){V z;for(auto[s,x]:v){assert(!((s>>(2*a))&3)&&!((s>>(2*b))&3));for(int c=1;c<4;c++)add(z,s|(uint64_t(c)<<(2*a))|(uint64_t(c)<<(2*b)),x);}return z;}
void graph(int nx,int ny){N=nx*ny;map<pair<int,int>,int> es;for(int x=0;x<nx;x++)for(int y=0;y<ny;y++){int a=x*ny+y;for(int b:{((x+1)%nx)*ny+y,x*ny+(y+1)%ny})es[minmax(a,b)]++;}edges.clear();for(auto [ab,w]:es)edges.push_back({ab.first,ab.second,w});for(int a=0;a<N;a++){int deg=0;for(auto e:edges)if(e.a==a||e.b==a)deg+=e.w;assert(deg==4);}}
int main(){graph(8,4);V vac{{0,1}};for(string f:{"N","F","L"}){V v=f=="N"?CE(vac):f=="F"?EE(vac):L(vac);assert(v.size()==1&&v.count(0));cout<<f<<" "<<v.at(0)<<endl;}rusage r{};getrusage(RUSAGE_SELF,&r);cerr<<"CPU="<<r.ru_utime.tv_sec+r.ru_utime.tv_usec/1e6+r.ru_stime.tv_sec+r.ru_stime.tv_usec/1e6<<" RSS="<<r.ru_maxrss<<endl;}