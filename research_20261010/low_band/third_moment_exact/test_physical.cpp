// Independent sparse physical dimer-state tests using spin-derived local matrix.
// Each scalar basis digit is orthonormal: 0=singlet,1=t-,2=t0,3=t+.
// At most six triplets: discarded q8 transitions are rejected before key creation.
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <sys/resource.h>
using namespace std;
using I=__int128_t;constexpr int D=5;
struct V{long long x[D]{};};using Map=unordered_map<uint64_t,V>;
int N,d,orb[64][64],kernel[16][16];vector<array<int,3>> edges;
int num(uint64_t s){int q=0;while(s){q+=(s&3)!=0;s>>=2;}return q;}
Map physical_apply(const Map& v,int target_q){assert(target_q<=6);Map out;for(auto& [s,c]:v){int q=num(s);for(auto [i,j,w]:edges){int a=(s>>(2*i))&3,b=(s>>(2*j))&3;for(int xy=0;xy<16;xy++){int k=kernel[xy][4*a+b]*w;if(!k)continue;int x=xy/4,y=xy%4;int tq=q-(a!=0)-(b!=0)+(x!=0)+(y!=0);if(tq>6||(target_q>=0&&tq!=target_q))continue;uint64_t t=s^((uint64_t)(a^x)<<(2*i))^((uint64_t)(b^y)<<(2*j));V& dest=out[t];for(int z=0;z<d;z++)dest.x[z]+=k*c.x[z];}}}for(auto it=out.begin();it!=out.end();){bool zero=true;for(int z=0;z<d;z++)zero&=it->second.x[z]==0;if(zero)it=out.erase(it);else ++it;}return out;}
struct Mat{I x[D][D]{};};
Mat inner(const Map& a,const Map& b){Mat o;for(auto& [s,c]:a){auto it=b.find(s);if(it!=b.end())for(int i=0;i<d;i++)for(int j=0;j<d;j++)o.x[i][j]+=(I)c.x[i]*it->second.x[j];}return o;}
Mat expect(const Map& bra,const Map& ket,int target_q){Mat out;for(auto& [s,c]:ket){int q=num(s);for(auto [i,j,w]:edges){int a=(s>>(2*i))&3,b=(s>>(2*j))&3;for(int xy=0;xy<16;xy++){int k=kernel[xy][4*a+b]*w;if(!k)continue;int x=xy/4,y=xy%4;int tq=q-(a!=0)-(b!=0)+(x!=0)+(y!=0);if(tq>6||(target_q>=0&&tq!=target_q))continue;uint64_t t=s^((uint64_t)(a^x)<<(2*i))^((uint64_t)(b^y)<<(2*j));auto it=bra.find(t);if(it!=bra.end())for(int a=0;a<d;a++)if(it->second.x[a])for(int b=0;b<d;b++)out.x[a][b]+=(I)it->second.x[a]*k*c.x[b];}}}return out;}
string str(I a){if(!a)return "0";bool neg=a<0;if(neg)a=-a;string s;while(a){s.insert(s.begin(),'0'+a%10);a/=10;}return (neg?"-":"")+s;}
void emit(ofstream& o,const char* key,const Mat& a){o<<",\n\""<<key<<"\":[";for(int i=0;i<d;i++){if(i)o<<",";o<<"[";for(int j=0;j<d;j++){if(j)o<<",";o<<str(a.x[i][j]);}o<<"]";}o<<"]";}
int main(int argc,char**argv){assert(argc==4);auto start=chrono::steady_clock::now();ifstream in(argv[1]),ki(argv[2]);in>>N>>d;assert(N<=16&&d<=D);int E;in>>E;for(int k=0;k<E;k++){array<int,3>e;in>>e[0]>>e[1]>>e[2];edges.push_back(e);}for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)in>>orb[i][j];for(int i=0;i<16;i++)for(int j=0;j<16;j++){ki>>kernel[i][j];}for(int i=0;i<16;i++)for(int j=0;j<16;j++)assert(kernel[i][j]==kernel[j][i]);
 Map B;for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)for(auto abc:vector<array<int,3>>{{1,3,-1},{2,2,1},{3,1,-1}}){uint64_t s=((uint64_t)abc[0]<<(2*i))|((uint64_t)abc[1]<<(2*j));B[s].x[orb[i][j]]=abc[2];}
 Map L=physical_apply(B,4),R=physical_apply(L,4),M=physical_apply(L,6);cerr<<"physical support B,L,R,M "<<B.size()<<","<<L.size()<<","<<R.size()<<","<<M.size()<<endl;
 auto F=inner(L,L),S=inner(L,R),Vv=inner(R,R),W=inner(M,M);auto X=expect(R,R,4),Y=expect(R,M,4),Z=expect(M,M,6);
 Map psi;psi[0].x[0]=7;for(auto& [st,v]:B)for(int i=0;i<d;i++)psi[st].x[0]+=(i%2?-i-1:i+1)*v.x[i];for(auto& [st,v]:L)for(int i=0;i<d;i++)psi[st].x[0]+=(i%2?i+2:-i-2)*v.x[i];
 Map y=physical_apply(psi,-1);for(auto& [st,v]:y)v.x[0]*=9;for(auto& [st,v]:psi)y[st].x[0]+=200*num(st)*v.x[0];
 I norm=inner(psi,psi).x[0][0],mom1=inner(psi,y).x[0][0],mom2=inner(y,y).x[0][0],mom3=9*expect(y,y,-1).x[0][0];for(auto& [st,v]:y)mom3+=(I)200*num(st)*v.x[0]*v.x[0];

 ofstream out(argv[3]);rusage u{};getrusage(RUSAGE_SELF,&u);out<<"{\n\"N\":"<<N<<",\"pair_orbits\":"<<d<<",\"support_B\":"<<B.size()<<",\"support_L\":"<<L.size()<<",\"support_R\":"<<R.size()<<",\"support_M\":"<<M.size()<<",\"max_triplet_support\":6,\"no_q8_states_created\":true,\"peak_rss_kib\":"<<u.ru_maxrss<<",\"total_seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count();out<<",\n\"fixture\":{\"b0\":7,\"b_pair_rule\":\"(-1)^i*(i+1)\",\"c_rule\":\"-(-1)^i*(i+2)\",\"coupling\":\"9/100\",\"integer_H_denominator\":200,\"norm\":"<<str(norm)<<",\"H1_numerator\":"<<str(mom1)<<",\"H2_numerator\":"<<str(mom2)<<",\"H3_numerator\":"<<str(mom3)<<",\"psi_support\":"<<psi.size()<<",\"Hpsi_support\":"<<y.size()<<"}";emit(out,"F",F);emit(out,"S",S);emit(out,"V",Vv);emit(out,"W",W);emit(out,"X",X);emit(out,"Y",Y);emit(out,"Z",Z);out<<"\n}\n";
}
