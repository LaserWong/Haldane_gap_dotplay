#include <bits/stdc++.h>
#include <sys/resource.h>
namespace rule {
#define main compiler_main
#include "compiler.cpp"
#undef main
}
namespace physical {
#define main physical_main
#include "fixture_snapshot.cpp"
#undef main
}
using namespace std;
using V=physical::V;
struct Block {vector<int> sites; map<uint16_t,vector<pair<uint16_t,int64_t>>> columns;};
vector<Block> build(string fam){rule::Stats st;rule::canonicalize=false;auto motifs=rule::motifs(fam,st,false);vector<Block> blocks;for(auto &[sup,p]:motifs){Block b;for(int i=0;i<rule::N;i++)if(sup>>i&1)b.sites.push_back(i);auto m=rule::wordmatrix(rule::localize(p,sup),b.sites.size());auto independent=rule::productmatrix(rule::localize(rule::raw_polynomials[sup],sup),b.sites.size());assert(m==independent);for(auto [key,c]:m)b.columns[key>>10].push_back({uint16_t(key&1023),c});blocks.push_back(move(b));rule::guard();}return blocks;}
V apply_rules(const vector<Block>&blocks,const V&v){V out;for(auto &b:blocks)for(auto [s,a]:v){uint16_t x=0;uint32_t base=s;for(int i=0;i<(int)b.sites.size();i++){x|=((s>>(2*b.sites[i]))&3)<<(2*i);base&=~(3u<<(2*b.sites[i]));}auto it=b.columns.find(x);if(it!=b.columns.end())for(auto [y,c]:it->second){uint32_t t=base;for(int i=0;i<(int)b.sites.size();i++)t|=((y>>(2*i))&3)<<(2*b.sites[i]);physical::add(out,t,physical::I(a)*c);}}return out;}
int main(int argc,char**argv){assert(argc==2);string dir=argv[1];rule::outdir=dir;rule::deadline=22.;ofstream report(dir+"/validation.json");report<<"{\"fixtures\":[";bool first=true;try{for(int nx:{4,5}){physical::graph(nx,2);rule::graph(nx,2);V vac{{0,1}},p2=physical::pairadd(vac,0,1),p4=physical::pairadd(p2,2,3),m6=physical::pairadd(p4,4,5),alt=physical::pairadd(physical::pairadd(physical::pairadd(vac,0,2),1,3),4,6);V psi=physical::sum(physical::sum(physical::sum(physical::scale(vac,3),p2,-2),p4),m6,-1);psi=physical::sum(psi,alt,2);V m=physical::sector(psi,6);for(string fam:{"N","F","L"}){auto blocks=build(fam);V got=apply_rules(blocks,m);V want=fam=="N"?physical::CE(m):fam=="F"?physical::EE(m):physical::L(m);assert(got==want);if(!first)report<<",";first=false;report<<"{\"nx\":"<<nx<<",\"family\":\""<<fam<<"\",\"full_vector_equal\":true,\"output_states\":"<<got.size()<<",\"expectation\":\""<<physical::st(physical::dot(m,got))<<"\",\"cpu_seconds\":"<<rule::cpu()<<"}";report.flush();cerr<<nx<<"x2 "<<fam<<" full vector PASS CPU "<<rule::cpu()<<endl;rule::guard();}}report<<"],\"complete\":true}";physical::physical_main(argc,argv);return 0;}catch(string reason){report<<"],\"complete\":false,\"reason\":\""<<reason<<"\"}";return 2;}}
