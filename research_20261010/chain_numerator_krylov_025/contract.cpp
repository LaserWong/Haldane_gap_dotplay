#include <gmpxx.h>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <chrono>
#include <ctime>
#include <sys/resource.h>
#include <stdexcept>
using I=mpz_class;
using S=mpz_class;
struct Tr{unsigned a,b;int c;};
struct Val{I x=0;int w=0;};
using Map=std::unordered_map<uint32_t,Val>;
int W[9]={3,2,2,2,1,2,6,2,1},EX[9]={0,1,1,1,3,3,3,3,3};
std::vector<Tr> ker[9][9];int den;
int weight(uint32_t k){int w=1;for(int i=0;i<8;i++)w*=W[(k>>(4*i))&15];return w;}
int energy(uint32_t k){int e=-16;for(int i=0;i<8;i++)e+=EX[(k>>(4*i))&15];return e;}
double cpu(){return double(clock())/CLOCKS_PER_SEC;}
void budget(){if(cpu()>580)throw std::runtime_error("stop before 600 CPU second cap");}
Map action(const std::vector<uint32_t>& keys,const std::vector<I>& vec,int count,unsigned long long& visits){
 Map out;out.reserve(count<2000?80000:300000);
 for(int k=0;k<count;k++){
  int z=count<(int)keys.size()?((long long)k*keys.size()/count):k;uint32_t key=keys[z];const I& x=vec[z];if(x==0)continue;
  out[key].x+=I(x*den*energy(key));
  for(int r=0;r<8;r++){
   int l=(r+7)%8,ls=4*l,rs=4*r;uint32_t mask=~((15u<<ls)|(15u<<rs));
   for(const auto&t:ker[(key>>ls)&15][(key>>rs)&15]){uint32_t target=(key&mask)|(t.a<<ls)|(t.b<<rs);out[target].x+=I(x*t.c);visits++;}
  }
  if(k%2000==0)budget();
 }
 for(auto it=out.begin();it!=out.end();){if(it->second.x==0)it=out.erase(it);else{it->second.w=weight(it->first);++it;}}
 return out;
}
S contraction(const Map& phi,int count,bool force,unsigned long long& visits){
 S total=0;int n=0;
 for(const auto& entry:phi){
  if(n++>=count)break;uint32_t key=entry.first;const auto& v=entry.second;total+=S(v.x)*S(v.x)*v.w*den*energy(key);
  for(int r=0;r<8;r++){
   int l=(r+7)%8,ls=4*l,rs=4*r;uint32_t mask=~((15u<<ls)|(15u<<rs));
   for(const auto&t:ker[(key>>ls)&15][(key>>rs)&15]){
    uint32_t target=(key&mask)|(t.a<<ls)|(t.b<<rs);auto it=phi.find(target);visits++;
    if(it!=phi.end())total+=S(v.x)*S(it->second.x)*it->second.w*t.c;
    else if(force)total+=S(v.x)*S(v.x)*v.w*t.c;
   }
  }
  if(n%2000==0)budget();
 }
 return total;
}
int main(int argc,char**argv){
 try{
  struct rlimit as{700ull*1024*1024,700ull*1024*1024};setrlimit(RLIMIT_AS,&as);struct rlimit cp{590,600};setrlimit(RLIMIT_CPU,&cp);
  if(argc<4)throw std::runtime_error("usage: contract input output_prefix probe|full");
  std::ifstream in(argv[1]);int n;in>>den>>n;if(!in)throw std::runtime_error("input missing");
  for(int a=0;a<9;a++)for(int b=0;b<9;b++){int len;in>>len;for(int j=0;j<len;j++){Tr t;in>>t.a>>t.b>>t.c;ker[a][b].push_back(t);}}
  std::vector<uint32_t> keys(n);std::vector<I> vec(n);for(int i=0;i<n;i++)in>>keys[i]>>vec[i];if(!in)throw std::runtime_error("truncated input");
  if(std::string(argv[3])=="support"){
   double t=cpu();std::unordered_set<uint32_t> reached;reached.reserve(1500000);unsigned long long visits=0;
   for(int j=0;j<n;j++){uint32_t key=keys[j];reached.insert(key);for(int r=0;r<8;r++){int l=(r+7)%8,ls=4*l,rs=4*r;uint32_t mask=~((15u<<ls)|(15u<<rs));for(const auto& tr:ker[(key>>ls)&15][(key>>rs)&15]){reached.insert((key&mask)|(tr.a<<ls)|(tr.b<<rs));visits++;}}if(j%2000==0)budget();}
   struct rusage ru;getrusage(RUSAGE_SELF,&ru);std::ofstream out(std::string(argv[2])+".json");out<<"{\n\"status\":\"EXACT_GRAPH_SUPPORT_UPPER\",\n\"input_support\":"<<n<<",\n\"next_image_support_upper\":"<<reached.size()<<",\n\"transitions\":"<<visits<<",\n\"cpu_seconds\":"<<cpu()-t<<",\n\"peak_rss_kib\":"<<ru.ru_maxrss<<"\n}\n";std::cout<<"SUPPORT "<<reached.size()<<" cpu="<<cpu()-t<<" rss="<<ru.ru_maxrss<<"\n";return 0;
  }
  if(std::string(argv[3])=="energy"){
   double start=cpu();Map v;v.reserve(n*12/10);for(int i=0;i<n;i++){v[keys[i]].x=vec[i];v[keys[i]].w=weight(keys[i]);}S value=0;unsigned long long pairs=0;
   for(int j=0;j<n;j++){uint32_t key=keys[j];const auto& x=v.at(key);value+=S(x.x)*S(x.x)*x.w*den*energy(key);
    for(int r=0;r<8;r++){int l=(r+7)%8,ls=4*l,rs=4*r;uint32_t mask=~((15u<<ls)|(15u<<rs));for(const auto& t:ker[(key>>ls)&15][(key>>rs)&15]){uint32_t target=(key&mask)|(t.a<<ls)|(t.b<<rs);if(target<key)continue;auto it=v.find(target);if(it==v.end())continue;value+=S(x.x)*S(it->second.x)*it->second.w*t.c*(target==key?1:2);pairs++;}}
    if(j%2000==0)budget();
   }
   struct rusage ru;getrusage(RUSAGE_SELF,&ru);std::ofstream out(std::string(argv[2])+".json");out<<"{\n\"status\":\"EXACT_TRIANGULAR_ENERGY_REPLAY\",\n\"value\":\""<<value<<"\",\n\"support\":"<<n<<",\n\"counted_pairs\":"<<pairs<<",\n\"cpu_seconds\":"<<cpu()-start<<",\n\"peak_rss_kib\":"<<ru.ru_maxrss<<"\n}\n";std::cout<<"ENERGY REPLAY cpu="<<cpu()-start<<" rss="<<ru.ru_maxrss<<"\n";return 0;
  }
  bool probe=std::string(argv[3])=="probe";double start=cpu();unsigned long long visits=0;Map phi=action(keys,vec,probe?1000:n,visits);double atime=cpu()-start;
  unsigned long long cvisits=0;start=cpu();S m3=contraction(phi,probe?std::min(1000,(int)phi.size()):(int)phi.size(),probe,cvisits);double ctime=cpu()-start;
  struct rusage ru;getrusage(RUSAGE_SELF,&ru);
  std::ofstream out(std::string(argv[2])+".json");
  out<<"{\n\"status\":\""<<(probe?"COST_PROBE_ONLY":"EXACT_MOMENTS_PENDING_REPLAY")<<"\",\n\"input_support\":"<<n<<",\n\"image_support\":"<<phi.size()<<",\n\"action_cpu_seconds\":"<<atime<<",\n\"contraction_cpu_seconds\":"<<ctime<<",\n\"action_transitions\":"<<visits<<",\n\"contraction_transitions\":"<<cvisits<<",\n\"peak_rss_kib\":"<<ru.ru_maxrss<<",\n\"integer_denominator\":"<<den;
  if(!probe){
   S m0=0,m1=0,m2=0;for(int i=0;i<n;i++){int w=weight(keys[i]);m0+=S(vec[i])*S(vec[i])*w;auto it=phi.find(keys[i]);if(it!=phi.end())m1+=S(vec[i])*S(it->second.x)*w;}
   std::vector<uint32_t> pkeys;pkeys.reserve(phi.size());unsigned maxbits=0;for(auto &z:phi){m2+=S(z.second.x)*S(z.second.x)*z.second.w;pkeys.push_back(z.first);I ax=z.second.x;if(ax<0)ax=-ax;maxbits=std::max(maxbits,(unsigned)mpz_sizeinbase(ax.get_mpz_t(),2));}std::sort(pkeys.begin(),pkeys.end());
   std::ofstream vf(std::string(argv[2])+"_image.txt");for(auto k:pkeys)vf<<k<<" "<<phi.at(k).x<<"\n";
   out<<",\n\"norm\":\""<<m0<<"\",\n\"moment1_scaled\":\""<<m1<<"\",\n\"moment2_scaled\":\""<<m2<<"\",\n\"moment3_scaled\":\""<<m3<<"\",\n\"image_coefficient_max_bits\":"<<maxbits;
  }else out<<",\n\"probe_accumulator\":\""<<m3<<"\"";
  out<<"\n}\n";std::cout<<"DONE "<<(probe?"probe":"full")<<" action_cpu="<<atime<<" contraction_cpu="<<ctime<<" image_support="<<phi.size()<<" rss="<<ru.ru_maxrss<<"\n";
 }catch(std::exception&e){std::cerr<<e.what()<<"\n";return 1;}
}
