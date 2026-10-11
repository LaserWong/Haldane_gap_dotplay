#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <sys/resource.h>
using namespace std;
struct Edge {int a,b,w;};
using Word=vector<int>; using Poly=map<Word,int64_t>; using Matrix=map<uint32_t,int64_t>;
static int nx=8,ny=4,N=32; static vector<Edge> edges; static string outdir; static double deadline=4.5; // Final replay allowance; cumulative physical/local-algebra CPU stays below 30.
static double unused_deadline=0.; static uint64_t work=0; static bool canonicalize=true; static map<uint32_t,Poly> raw_polynomials;
double cpu(){rusage r{};getrusage(RUSAGE_SELF,&r);return r.ru_utime.tv_sec+r.ru_utime.tv_usec*1e-6+r.ru_stime.tv_sec+r.ru_stime.tv_usec*1e-6;}
void guard(){if(cpu()>deadline)throw string("CPU_CHECKPOINT_CAP");}
void graph(int x,int y){nx=x;ny=y;N=x*y;map<pair<int,int>,int> es;for(int i=0;i<N;i++){int xx=i/ny,yy=i%ny;for(int j:{((xx+1)%nx)*ny+yy,xx*ny+(yy+1)%ny})es[minmax(i,j)]++;}edges.clear();for(auto [e,w]:es)edges.push_back({e.first,e.second,w});}
uint32_t support(Edge e){return (1u<<e.a)|(1u<<e.b);}
int letter(int op,int a,int b){if(a>b)swap(a,b);return op*1024+a*32+b;}
int op(int l){return l/1024;}int aof(int l){return l/32%32;}int bof(int l){return l%32;}
uint32_t ls(int l){return (1u<<aof(l))|(1u<<bof(l));}
Word trace_normal(Word w){Word z;vector<bool> used(w.size(),false);for(size_t t=0;t<w.size();t++){int best=-1;for(size_t j=0;j<w.size();j++)if(!used[j]){bool ready=true;for(size_t k=0;k<j;k++)if(!used[k]&&(ls(w[k])&ls(w[j])))ready=false;if(ready&&(best<0||w[j]<w[best]))best=j;}assert(best>=0);used[best]=true;z.push_back(w[best]);}return z;}
void add(Poly &p,Word w,int64_t c){if(!c)return;auto &v=p[w];v+=c;if(!v)p.erase(w);}
Poly comm(const Poly&p,const Poly&q){Poly z;for(auto [u,c]:p)for(auto [v,d]:q){Word w=u;w.insert(w.end(),v.begin(),v.end());add(z,w,c*d);w=v;w.insert(w.end(),u.begin(),u.end());add(z,w,-c*d);}return z;}
Poly atom(int o,int e){auto x=edges[e];return {{{letter(o,x.a,x.b)},x.w}};}
int translate(int i,int t){return (((i/ny+t/ny)%nx)*ny+(i%ny+t%ny)%ny);}
pair<uint32_t,int> canonical(uint32_t s){uint32_t best=UINT32_MAX;int bt=0;for(int t=0;t<N;t++){uint32_t z=0;for(int i=0;i<N;i++)if(s>>i&1)z|=1u<<translate(i,t);if(z<best){best=z;bt=t;}}return {best,bt};}
struct Stats{uint64_t tuples=0,expanded=0,trace_words=0,supports=0,surviving_supports=0,transitions=0,diagonal=0,vacuum=0,zero_supports=0,entry_checks=0;int64_t maxcoef=0;};
void checkpoint(string stage,const Stats&s,bool complete=false,string reason=""){rusage r{};getrusage(RUSAGE_SELF,&r);ofstream f(outdir+"/checkpoint.json");f<<"{\"stage\":\""<<stage<<"\",\"complete\":"<<(complete?"true":"false")<<",\"reason\":\""<<reason<<"\",\"cpu_seconds\":"<<cpu()<<",\"rss_kib\":"<<r.ru_maxrss<<",\"tuples\":"<<s.tuples<<",\"expanded_signed_words\":"<<s.expanded<<",\"surviving_trace_words\":"<<s.trace_words<<",\"supports\":"<<s.supports<<",\"compiled_supports\":"<<s.surviving_supports+s.zero_supports<<",\"surviving_supports\":"<<s.surviving_supports<<",\"transitions\":"<<s.transitions<<",\"vacuum_diagonals\":"<<s.vacuum<<",\"entry_checks\":"<<s.entry_checks<<",\"max_abs_coefficient\":"<<s.maxcoef<<"}";}
using Motifs=map<uint32_t,Poly>;
void insert(Motifs&m,Poly p,Stats&s){s.tuples++;uint32_t sup=0;for(auto [w,c]:p)for(int l:w)sup|=ls(l); // Empty polynomial is a fully cancelled tuple.
 if(!sup)return;auto [cs,t]=canonicalize?canonical(sup):make_pair(sup,0);for(auto [ww,c]:p){Word w=ww;s.expanded++;for(int &l:w)l=letter(op(l),translate(aof(l),t),translate(bof(l),t));add(raw_polynomials[cs],w,c);add(m[cs],trace_normal(w),c);}if((s.tuples&127)==0)guard();}
Motifs motifs(string family,Stats&s,bool anchor=true){Motifs z;raw_polynomials.clear();vector<int> anchors;for(int e=0;e<(int)edges.size();e++)if(!anchor||((edges[e].a==0)&&(edges[e].b==1||edges[e].b==ny)))anchors.push_back(e);
 if(family=="N"||family=="L")for(int k:anchors)for(int j=0;j<(int)edges.size();j++)if(support(edges[k])&support(edges[j]))for(int i=0;i<(int)edges.size();i++)if(support(edges[i])&(support(edges[j])|support(edges[k]))){auto p=comm(atom(0,i),comm(atom(family=="N"?2:0,j),atom(1,k)));if(family=="N")insert(z,p,s);else for(int l=0;l<(int)edges.size();l++)if(support(edges[l])&(support(edges[i])|support(edges[j])|support(edges[k])))insert(z,comm(p,atom(1,l)),s);}
 if(family=="F")for(int i:anchors)for(int j=0;j<(int)edges.size();j++)if(support(edges[i])&support(edges[j]))for(int k=0;k<(int)edges.size();k++)for(int l=0;l<(int)edges.size();l++)if((support(edges[k])&support(edges[l]))&&((support(edges[i])|support(edges[j]))&(support(edges[k])|support(edges[l]))))insert(z,comm(comm(atom(0,i),atom(2,j)),comm(atom(2,k),atom(1,l))),s);
 for(auto it=z.begin();it!=z.end();)if(it->second.empty())it=z.erase(it);else{ s.trace_words+=it->second.size();++it;}s.supports=z.size();return z;}
// Independent local elementary action in the real spherical rung basis, coefficients in Z.
vector<pair<uint16_t,int>> act(uint16_t state,int l){int i=aof(l),j=bof(l),a=state>>(2*i)&3,b=state>>(2*j)&3;uint16_t base=state&~((3u<<(2*i))|(3u<<(2*j)));vector<pair<uint16_t,int>> r;auto push=[&](int x,int y,int c){if(c)r.push_back({uint16_t(base|(x<<(2*i))|(y<<(2*j))),c});};if(op(l)==0){int c=(a==2&&b==2)?1:((a==1&&b==3)||(a==3&&b==1))?-1:0;if(c)push(0,0,c);}else if(op(l)==1){if(!a&&!b){push(2,2,1);push(1,3,-1);push(3,1,-1);}}else if(bool(a)!=bool(b))push(b,a,1);else if(a&&b){int u=a==1?1:a==3?-1:0,v=b==1?1:b==3?-1:0;auto idx=[](int n){return n==1?1:n==-1?3:2;};push(a,b,u*v);if(u<1&&v>-1)push(idx(u+1),idx(v-1),1);if(u>-1&&v<1)push(idx(u-1),idx(v+1),1);}return r;}
void evalword(Matrix&r,int source,uint16_t state,const Word&w,int pos,int64_t c){if(pos<0){uint32_t key=(uint32_t(source)<<10)|state;auto &v=r[key];v+=c;if(!v)r.erase(key);return;}for(auto [z,v]:act(state,w[pos]))evalword(r,source,z,w,pos-1,c*v);}
Poly localize(const Poly&p,uint32_t sup){vector<int> sites;for(int i=0;i<N;i++)if(sup>>i&1)sites.push_back(i);Poly z;for(auto [ww,c]:p){Word w=ww;for(int&l:w){int a=lower_bound(sites.begin(),sites.end(),aof(l))-sites.begin(),b=lower_bound(sites.begin(),sites.end(),bof(l))-sites.begin();l=letter(op(l),a,b);}add(z,w,c);}return z;}
Matrix wordmatrix(const Poly&p,int n){Matrix r;for(int s=0;s<(1<<(2*n));s++)for(auto [w,c]:p)evalword(r,s,s,w,int(w.size())-1,c);return r;}
// Second multiplication order: elementary sparse matrices multiplied left-to-right by column.
Matrix productmatrix(const Poly&p,int n){Matrix r;for(auto [w,c]:p){for(int s=0;s<(1<<(2*n));s++){map<uint16_t,int64_t> v{{uint16_t(s),c}};for(auto it=w.rbegin();it!=w.rend();it++){map<uint16_t,int64_t> next;for(auto [x,a]:v)for(auto [y,b]:act(x,*it))next[y]+=a*b;v=move(next);}for(auto [y,a]:v)if(a){auto key=(uint32_t(s)<<10)|y;r[key]+=a;if(!r[key])r.erase(key);}}}return r;}
uint16_t occupancy(int s,int n){uint16_t m=0;for(int i=0;i<n;i++)if(s>>(2*i)&3)m|=1<<i;return m;}
void serialize(ofstream&f,uint32_t sup,const Matrix&r,int n,Stats&s){for(auto [key,c]:r){assert(c>=INT32_MIN&&c<=INT32_MAX);uint16_t src=key>>10,dst=key&1023;int32_t cc=c;f.write((char*)&sup,4);f.write((char*)&src,2);f.write((char*)&dst,2);f.write((char*)&cc,4);s.transitions++;s.diagonal+=src==dst;s.vacuum+=src==0&&dst==0;s.maxcoef=max<int64_t>(s.maxcoef,llabs(c));assert(occupancy(src,n)==occupancy(dst,n)||__builtin_popcount(occupancy(src,n))==__builtin_popcount(occupancy(dst,n)));}}
int main(int argc,char**argv){assert(argc==2);outdir=argv[1];Stats total;try{graph(8,4);ofstream report(outdir+"/counts.json");report<<"{\"families\":[";bool first=true;for(string family:{"N","F","L"}){Stats s;auto m=motifs(family,s);checkpoint(family+"_generated",s);ofstream bin(outdir+"/rules_"+family+".bin",ios::binary);for(auto &[sup,p]:m){int n=__builtin_popcount(sup);assert(n<=5);auto local=localize(p,sup);auto r=wordmatrix(local,n);auto independent=productmatrix(localize(raw_polynomials[sup],sup),n);assert(r==independent);s.entry_checks+=uint64_t(1)<<(4*n);if(r.empty())s.zero_supports++;else s.surviving_supports++;serialize(bin,sup,r,n,s);checkpoint(family+"_compiling",s);guard();}bin.close();if(!first)report<<",";first=false;report<<"{\"name\":\""<<family<<"\",\"anchored_tuples\":"<<s.tuples<<",\"full_tuples\":"<<32*s.tuples<<",\"expanded_signed_words\":"<<s.expanded<<",\"surviving_trace_words\":"<<s.trace_words<<",\"canonical_supports\":"<<s.supports<<",\"surviving_supports\":"<<s.surviving_supports<<",\"zero_supports\":"<<s.zero_supports<<",\"transitions\":"<<s.transitions<<",\"vacuum_diagonals\":"<<s.vacuum<<",\"entry_checks\":"<<s.entry_checks<<",\"max_abs_coefficient\":"<<s.maxcoef<<",\"serialized_bytes\":"<<12*s.transitions<<"}";report.flush();cerr<<family<<" tuples "<<s.tuples<<" supports "<<s.supports<<" rules "<<s.transitions<<" CPU "<<cpu()<<endl;total.transitions+=s.transitions;total.entry_checks+=s.entry_checks;total.tuples+=s.tuples;total.supports+=s.supports;total.surviving_supports+=s.surviving_supports;total.expanded+=s.expanded;total.trace_words+=s.trace_words;total.vacuum+=s.vacuum;total.zero_supports+=s.zero_supports;total.maxcoef=max(total.maxcoef,s.maxcoef);}report<<"],\"cpu_seconds\":"<<cpu()<<"}";checkpoint("complete",total,true);return 0;}catch(string reason){ofstream abort(outdir+"/ABORT.json");abort<<"{\"reason\":\""<<reason<<"\",\"cpu_seconds\":"<<cpu()<<"}";cerr<<reason<<endl;return 2;}}
