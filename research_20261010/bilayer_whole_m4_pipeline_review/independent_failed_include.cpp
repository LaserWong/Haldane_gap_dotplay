#define main pipeline_main
#include "source/whole.cpp"
#undef main
namespace independent {
using V=vector<int64_t>; using Row=vector<pair<int,int>>;
int N,NX;size_t dim;vector<array<int,3>> edges;array<array<Row,16>,3> A;vector<unsigned char> sectors;
void put(int64_t&out,I value){value+=out;assert(value>=INT64_MIN&&value<=INT64_MAX);out=(int64_t)value;}
V sum(V a,const V&b,int64_t k=1){for(size_t i=0;i<dim;i++)put(a[i],I(k)*b[i]);return a;}
V scale(const V&a,int64_t k){V b(dim);for(size_t i=0;i<dim;i++)put(b[i],I(k)*a[i]);return b;}
V sector(const V&a,int q){V b(dim);for(size_t i=0;i<dim;i++)if(sectors[i]==q)b[i]=a[i];return b;}
void setup(int nx){NX=nx;N=2*nx;dim=size_t(1)<<(2*N);sectors.resize(dim);for(size_t s=0;s<dim;s++){int q=0;for(int k=0;k<N;k++)q+=bool((s>>(2*k))&3);sectors[s]=q;}
 edges.clear();map<pair<int,int>,int> e;for(int x=0;x<nx;x++)for(int y=0;y<2;y++){int a=2*x+y;for(int b:{2*((x+1)%nx)+y,2*x+(y+1)%2})e[minmax(a,b)]++;}for(auto[p,w]:e)edges.push_back({p.first,p.second,w});
 // Integer rung columns, each has norm sqrt(2): singlet, Cartesian x,y,z triplets.
 using Z=complex<int>;array<array<Z,4>,4> U{};U[0]={0,1,-1,0};U[1]={-1,0,0,1};U[2]={Z(0,1),0,0,Z(0,1)};U[3]={0,1,1,0};
 for(auto&kind:A)for(auto&row:kind)row.clear();
 for(int src=0;src<16;src++)for(int dst=0;dst<16;dst++){
  Z value=0;for(int bits=0;bits<16;bits++){
   auto perm=[&](int a,int b){return bits^((((bits>>a)^(bits>>b))&1)*((1<<a)|(1<<b)));};
   Z ket=U[src&3][bits&3]*U[src>>2][bits>>2];
   for(auto[nb,c]:vector<pair<int,int>>{{perm(0,2),1},{perm(1,3),1},{bits,-1}})value+=conj(U[dst&3][nb&3]*U[dst>>2][nb>>2])*ket*c;
  }
  assert(value.imag()==0&&value.real()%4==0);int v=value.real()/4;if(!v)continue;
  int delta=int(bool(dst&3))+int(bool(dst>>2))-int(bool(src&3))-int(bool(src>>2));assert(delta==-2||delta==0||delta==2);int k=delta==-2?0:delta==2?1:2;A[k][src].push_back({dst,v});
 }
 // Rung shift Q=(1+P_12)/2: exactly zero on singlet, one on every triplet.
 for(int a=0;a<4;a++)for(int b=0;b<4;b++){Z z=0;for(int s=0;s<4;s++){int sw=(s>>1)|((s&1)<<1);z+=conj(U[a][s])*(U[b][s]+U[b][sw]);}assert(z==Z(a==b&&a?4:0,0));}
}
V act(const V&v,int kind){V out(dim);for(size_t s=0;s<dim;s++)if(v[s])for(auto e:edges){int a=e[0],b=e[1],w=e[2],loc=((s>>(2*a))&3)|(((s>>(2*b))&3)<<2);size_t base=s&~((size_t(3)<<(2*a))|(size_t(3)<<(2*b)));for(auto[t,c]:A[kind][loc])put(out[base|(size_t(t&3)<<(2*a))|(size_t(t>>2)<<(2*b))],I(v[s])*c*w);}return out;}
V C(const V&v){return act(v,0);}V Cd(const V&v){return act(v,1);}V D(const V&v){return act(v,2);}V K(const V&v){return sum(C(Cd(v)),Cd(C(v)),-1);}V E(const V&v){return sum(D(Cd(v)),Cd(D(v)),-1);}V Ed(const V&v){return sum(C(D(v)),D(C(v)),-1);}V Nop(const V&v){return sum(C(E(v)),E(C(v)),-1);}V F(const V&v){return sum(Ed(E(v)),E(Ed(v)),-1);}V CK(const V&v){return sum(C(K(v)),K(C(v)),-1);}V L(const V&v){return sum(CK(Cd(v)),Cd(CK(v)),-1);}
V H(const V&v){V out=sum(sum(C(v),Cd(v)),D(v));for(size_t s=0;s<dim;s++){I r=I(out[s])*11+I(v[s])*200*sectors[s];out[s]=0;put(out[s],r);}return out;}
I dot(const V&a,const V&b){I r=0;for(size_t i=0;i<dim;i++){I term=I(a[i])*b[i];assert(!__builtin_add_overflow(r,term,&r));}return r;}I norm(const V&a){return dot(a,a);}
whole::Big big0(I v){return whole::Big(physical::st(v));}
V paired(initializer_list<pair<int,int>> pairs){V v(dim);v[0]=1;for(auto[a,b]:pairs){V out(dim);for(size_t s=0;s<dim;s++)if(v[s])for(int c=1;c<=3;c++)put(out[s|(size_t(c)<<(2*a))|(size_t(c)<<(2*b))],v[s]);v=move(out);}return v;}
V source(string type){if(type!="generic"){V v(dim);v[0]=3;v=sum(v,paired({{0,1}}),-2);v=sum(v,paired({{0,1},{2,3}}));v=sum(v,paired({{0,1},{2,3},{4,5}}),-1);v=sum(v,paired({{0,2},{1,3},{4,6}}),2);if(type=="localized")return v;V out(dim);for(size_t s=0;s<dim;s++)if(v[s])for(int x=0;x<NX;x++)for(int y=0;y<2;y++){size_t t=0;for(int k=0;k<N;k++){int j=((k/2+x)%NX)*2+(k%2+y)%2;t|=((s>>(2*k))&3)<<(2*j);}put(out[t],v[s]);}return out;}
 map<pair<int,int>,int> orbit;for(int dx=0;dx<=NX/2;dx++)for(int dy=0;dy<=1;dy++)if(dx||dy)orbit[{dx,dy}]=orbit.size();
 auto B=[&](int kind){V v(dim);for(int a=0;a<N;a++)for(int b=a+1;b<N;b++){int dx=abs(a/2-b/2),dy=abs(a%2-b%2),j=orbit.at({min(dx,NX-dx),dy});int c=kind==0?(j%2?-1:1)*(j+1):kind==1?j+2:kind==2?-j-3:(j%2?1:-1)*(j+4);for(int color=1;color<=3;color++)v[(size_t(color)<<(2*a))|(size_t(color)<<(2*b))]+=c;}return v;};V v=B(0);v[0]=3;v=sum(v,Cd(B(1)));v=sum(v,D(Cd(B(2))));v=sum(v,Cd(Cd(B(3))));return v;
}
void compare(const physical::V&a,const V&b,int maxq=10){size_t count=0;for(size_t s=0;s<dim;s++)if(sectors[s]<=maxq&&b[s]){count++;auto it=a.find(s);assert(it!=a.end()&&it->second==b[s]);}assert(a.size()==count);}
array<I,15> terms(const V&psi,const V&chi){auto m=sector(psi,6),cm=C(m),dm=D(m),km=K(m),x=Cd(cm),gamma=sum(x,km),v=sum(sum(scale(m,17600),scale(sector(chi,6),11)),scale(dm,121));array<I,15> t{};t[0]=2*dot(cm,C(dm));t[1]=-dot(cm,D(cm));t[2]=dot(km,dm);t[3]=dot(m,Nop(m));t[4]=norm(C(v));t[5]=dot(v,K(v));t[6]=242*dot(v,E(cm));t[7]=242*dot(v,Nop(m));t[8]=14641*norm(Ed(m));t[9]=14641*dot(m,F(m));t[10]=norm(gamma);t[11]=2*dot(cm,C(km));t[12]=-dot(cm,K(cm));t[13]=norm(km);t[14]=dot(m,L(m));return t;}
}
int main(int argc,char**argv){assert(argc==3);string path=argv[1],reference=argv[2];rule::deadline=38;rule::outdir=path;whole::setup_match();ofstream report(path+"/independent.jsonl");for(int nx:{4,5})for(string type:{"localized","symmetrized","generic"}){double start=rule::cpu();independent::setup(nx);auto psi=independent::source(type),chi=independent::H(psi),z=independent::H(chi);whole::System sys(nx,2,type,reference,"unused");whole::Totals t;for(int q:{0,2,4,6})whole::enumerate(sys.n,q,[&](const whole::S&s){whole::step(sys,s,t,true);});independent::compare(sys.psi,psi);independent::compare(t.expanded_psi,psi);independent::compare(t.expanded_chi,chi,6);independent::compare(t.expanded_z,z,6);auto terms=independent::terms(psi,chi);for(int i=0;i<15;i++)assert(t.term[i]==independent::big0(terms[i]));whole::Big d8=0,q8=0,q10=0;for(int i=0;i<4;i++)d8+=t.term[i];for(int i=4;i<10;i++)q8+=t.term[i];for(int i=10;i<15;i++)q10+=t.term[i];array<whole::Big,5> moments={t.m0,t.m1,t.m2low+121*t.n8,t.m3low+193600*t.n8+1331*d8+t.cross6,t.m4low+q8+14641*q10};array<I,5> direct={independent::norm(psi),independent::dot(psi,chi),independent::norm(chi),independent::dot(chi,z),independent::norm(z)};for(int i=0;i<5;i++)assert(moments[i]==independent::big0(direct[i]));for(int q:{0,2,4,6})assert(t.znorm[q]==independent::big0(independent::norm(independent::sector(z,q))));assert(q8==independent::big0(independent::norm(independent::sector(z,8))));assert(14641*q10==independent::big0(independent::norm(independent::sector(z,10))));assert(t.term[12]!=0&&t.term[6]!=0&&t.term[7]!=0&&t.orientation_detected>0);if(type=="localized")assert(t.mzero_z_nonzero>0&&t.mzero_kv_nonzero>0);if(type=="generic")assert(t.crcm_detected>0);report<<"{\"nx\":"<<nx<<",\"type\":\""<<type<<"\",\"independent_dense_spin_derived_vectors_and_15_terms\":true,\"moments\":[";for(int i=0;i<5;i++){if(i)report<<",";report<<"\""<<moments[i]<<"\"";}report<<"],\"q8\":\""<<q8<<"\",\"q10\":\""<<14641*q10<<"\",\"seconds\":"<<rule::cpu()-start<<"}\n";report.flush();cerr<<"PASS "<<nx<<" "<<type<<" CPU "<<rule::cpu()<<endl;rule::guard();}return 0;}
