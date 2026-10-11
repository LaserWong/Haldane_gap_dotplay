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
using namespace std;using I=__int128_t;using V=unordered_map<uint32_t,int64_t>;struct Edge{int a,b,w;};vector<Edge> edges;int N;long long ops=0;size_t maxstates=0;
string st(I x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;string z;while(x){z+=char('0'+x%10);x/=10;}if(neg)z+='-';reverse(z.begin(),z.end());return z;}
void add(V&v,uint32_t s,I x){I y=I(v[s])+x;assert(y>=INT64_MIN&&y<=INT64_MAX);if(y)v[s]=(int64_t)y;else v.erase(s);}
V sum(V a,const V&b,long long k=1){for(auto[s,x]:b)add(a,s,I(k)*x);maxstates=max(maxstates,a.size());return a;}
V scale(V a,long long k){V b;for(auto[s,x]:a)add(b,s,I(k)*x);return b;}
int q(uint32_t s){int r=0;for(int i=0;i<N;i++)r+=((s>>(2*i))&3)!=0;return r;}
int m(int z){return z==1?1:z==3?-1:0;}int indexm(int m){return m==1?1:m==-1?3:2;}
V sector(const V&v,int n){V a;for(auto[s,x]:v)if(q(s)==n)a[s]=x;return a;}
I dot(const V&a,const V&b){I z=0;for(auto[s,x]:a){auto it=b.find(s);if(it!=b.end())z+=I(x)*it->second;}return z;}I norm(const V&a){return dot(a,a);}
V C(const V&v){V out;for(auto[s,x]:v)for(auto e:edges){int a=(s>>(2*e.a))&3,b=(s>>(2*e.b))&3;int f=(a==2&&b==2)?1:((a==1&&b==3)||(a==3&&b==1))?-1:0;if(f){uint32_t z=s&~((3u<<(2*e.a))|(3u<<(2*e.b)));add(out,z,I(x)*f*e.w);}}maxstates=max(maxstates,out.size());return out;}
V Cd(const V&v){V out;for(auto[s,x]:v)for(auto e:edges)if(!((s>>(2*e.a))&3)&&!((s>>(2*e.b))&3)){add(out,s|(2u<<(2*e.a))|(2u<<(2*e.b)),I(x)*e.w);add(out,s|(1u<<(2*e.a))|(3u<<(2*e.b)),-I(x)*e.w);add(out,s|(3u<<(2*e.a))|(1u<<(2*e.b)),-I(x)*e.w);}maxstates=max(maxstates,out.size());return out;}
V D(const V&v){V out;for(auto[s,x]:v)for(auto e:edges){int a=(s>>(2*e.a))&3,b=(s>>(2*e.b))&3;uint32_t mask=(3u<<(2*e.a))|(3u<<(2*e.b)),base=s&~mask;if(bool(a)!=bool(b))add(out,base|(uint32_t(b)<<(2*e.a))|(uint32_t(a)<<(2*e.b)),I(x)*e.w);else if(a&&b){int u=m(a),w=m(b);add(out,s,I(x)*e.w*u*w);if(u<1&&w>-1)add(out,base|(uint32_t(indexm(u+1))<<(2*e.a))|(uint32_t(indexm(w-1))<<(2*e.b)),I(x)*e.w);if(u>-1&&w<1)add(out,base|(uint32_t(indexm(u-1))<<(2*e.a))|(uint32_t(indexm(w+1))<<(2*e.b)),I(x)*e.w);}}maxstates=max(maxstates,out.size());return out;}
V K(const V&v){return sum(C(Cd(v)),Cd(C(v)),-1);}V E(const V&v){return sum(D(Cd(v)),Cd(D(v)),-1);}V Ed(const V&v){return sum(C(D(v)),D(C(v)),-1);}V CE(const V&v){return sum(C(E(v)),E(C(v)),-1);}V EE(const V&v){return sum(Ed(E(v)),E(Ed(v)),-1);}V CK(const V&v){return sum(C(K(v)),K(C(v)),-1);}V L(const V&v){return sum(CK(Cd(v)),Cd(CK(v)),-1);}
V Q(const V&v){V a;for(auto[s,x]:v)add(a,s,I(q(s))*x);return a;}V H(const V&v,int d,int h){return sum(scale(Q(v),d),scale(sum(sum(C(v),Cd(v)),D(v)),h));}
V pairadd(V v,int a,int b){V z;for(auto[s,x]:v){assert(!((s>>(2*a))&3)&&!((s>>(2*b))&3));add(z,s|(2u<<(2*a))|(2u<<(2*b)),x);add(z,s|(1u<<(2*a))|(3u<<(2*b)),-x);add(z,s|(3u<<(2*a))|(1u<<(2*b)),-x);}return z;}
void graph(int nx,int ny){N=nx*ny;map<pair<int,int>,int> es;for(int x=0;x<nx;x++)for(int y=0;y<ny;y++){int a=x*ny+y;for(int b:{((x+1)%nx)*ny+y,x*ny+(y+1)%ny})es[minmax(a,b)]++;}edges.clear();for(auto [ab,w]:es)edges.push_back({ab.first,ab.second,w});for(int a=0;a<N;a++){int deg=0;for(auto e:edges)if(e.a==a||e.b==a)deg+=e.w;assert(deg==4);}}
int main(int argc,char**argv){assert(argc==2);string dir=argv[1];auto start=chrono::steady_clock::now();for(int nx:{4,5}){graph(nx,2);maxstates=0;V vac{{0,1}};V p2=pairadd(vac,0,1),p4=pairadd(p2,2,3),m6=pairadd(p4,4,5),malt=pairadd(pairadd(pairadd(vac,0,2),1,3),4,6);V psi=sum(sum(sum(scale(vac,3),p2,-2),p4),m6,-1);psi=sum(psi,malt,2);const int d=200,h=11;V chi=H(psi,d,h),z=H(chi,d,h);I direct3=dot(chi,z),direct4=norm(z);V mm=sector(psi,6),cm=C(mm),dm=D(mm),km=K(mm),gamma=sum(Cd(cm),km);assert(gamma==C(Cd(mm)));I n8=norm(cm)+dot(mm,km);assert(n8==norm(Cd(mm)));
 I d8=2*dot(cm,C(dm))-dot(cm,D(cm))+dot(km,dm)+dot(mm,CE(mm));assert(d8==dot(Cd(mm),D(Cd(mm))));I normal3=I(d)*8*h*h*n8;I lowA=0;for(int qq:{0,2,4,6}){V cq=sector(chi,qq);normal3+=I(d)*qq*norm(cq);lowA+=dot(cq,D(cq));if(qq)lowA+=2*dot(sector(chi,qq-2),C(cq));}normal3+=I(h)*(lowA+I(h)*h*d8+2*I(h)*dot(sector(chi,6),gamma));assert(normal3==direct3);
 I normal4=0;map<int,I> sectors;for(int qq:{0,2,4,6}){V zz=scale(sector(chi,qq),d*qq);zz=sum(zz,scale(D(sector(chi,qq)),h));if(qq)zz=sum(zz,scale(Cd(sector(chi,qq-2)),h));zz=sum(zz,qq==6?scale(gamma,h*h):scale(C(sector(chi,qq+2)),h));I n=norm(zz);assert(zz==sector(z,qq));sectors[qq]=n;normal4+=n;}
 V vv=sum(sum(scale(mm,8*d*h),scale(sector(chi,6),h)),scale(dm,h*h));I vnorm=norm(C(vv))+dot(vv,K(vv));I vcross=2*I(h)*h*dot(vv,sum(E(cm),CE(mm)));I enorm=I(h)*h*h*h*(norm(Ed(mm))+dot(mm,EE(mm)));I q8=vnorm+vcross+enorm;assert(q8==norm(sector(z,8)));I q10base=norm(gamma)+2*dot(cm,C(km))-dot(cm,K(cm))+norm(km)+dot(mm,L(mm));assert(q10base==norm(Cd(Cd(mm))));I q10=I(h)*h*h*h*q10base;assert(q10==norm(sector(z,10)));sectors[8]=q8;sectors[10]=q10;normal4+=q8+q10;assert(normal4==direct4);assert(nx==4?q10==0:q10>0);
 map<string,I> terms{{"D8_2_CM_CDM",2*dot(cm,C(dm))},{"D8_minus_CM_DCM",-dot(cm,D(cm))},{"D8_KM_DM",dot(km,dm)},{"D8_nested_C_E",dot(mm,CE(mm))},{"Q8_Cv_norm",norm(C(vv))},{"Q8_v_Kv",dot(vv,K(vv))},{"Q8_cross_ECM",2*I(h)*h*dot(vv,E(cm))},{"Q8_cross_CE",2*I(h)*h*dot(vv,CE(mm))},{"Q8_EadjM_norm",I(h)*h*h*h*norm(Ed(mm))},{"Q8_Ecomm",I(h)*h*h*h*dot(mm,EE(mm))},{"Q10_gamma_norm",norm(gamma)},{"Q10_2_CM_CKM",2*dot(cm,C(km))},{"Q10_minus_CM_KCM",-dot(cm,K(cm))},{"Q10_KM_norm",norm(km)},{"Q10_L",dot(mm,L(mm))}};
 assert(terms["Q8_Ecomm"]<0);assert(terms["Q10_L"]!=0);assert(q10base-terms["Q10_L"]!=norm(Cd(Cd(mm))));assert(q8-vcross!=norm(sector(z,8)));
 ofstream tout(dir+"/terms_"+to_string(nx)+"x2.json");tout<<"{";bool firstterm=true;for(auto[k,v]:terms){if(!firstterm)tout<<",";firstterm=false;tout<<"\""<<k<<"\":\""<<st(v)<<"\"";}tout<<"}";tout.close();
 ofstream out(dir+"/fixture_"+to_string(nx)+"x2.json");out<<"{\"N\":"<<N<<",\"full_Hilbert_dimension\":"<<(1ULL<<(2*N))<<",\"integer_H\":\"200Q+11A\",\"g\":\"11/100\",\"norm\":\""<<st(norm(psi))<<"\",\"direct_m3_numerator\":\""<<st(direct3)<<"\",\"normal_m3_numerator\":\""<<st(normal3)<<"\",\"direct_m4_numerator\":\""<<st(direct4)<<"\",\"normal_m4_numerator\":\""<<st(normal4)<<"\",\"q8_D_expectation\":\""<<st(d8)<<"\",\"q8_v_norm\":\""<<st(vnorm)<<"\",\"q8_oriented_cross\":\""<<st(vcross)<<"\",\"q8_E_norm\":\""<<st(enorm)<<"\",\"EE_comm_expectation\":\""<<st(dot(mm,EE(mm)))<<"\",\"L_comm_expectation\":\""<<st(dot(mm,L(mm)))<<"\",\"q10_negative_K4_term\":\""<<st(-dot(cm,K(cm)))<<"\",\"q10_base_norm\":\""<<st(q10base)<<"\",\"sector_H2_norms\":{";bool first=true;for(auto[q,n]:sectors){if(!first)out<<",";first=false;out<<"\""<<q<<"\":\""<<st(n)<<"\"";}out<<"},\"peak_sparse_states\":"<<maxstates<<"}";out.close();cerr<<nx<<"x2 PASS sparse states "<<maxstates<<" seconds "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;}
 rusage use{};getrusage(RUSAGE_SELF,&use);ofstream o(dir+"/resources.json");o<<"{\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"peak_rss_kib\":"<<use.ru_maxrss<<"}";return 0;}
