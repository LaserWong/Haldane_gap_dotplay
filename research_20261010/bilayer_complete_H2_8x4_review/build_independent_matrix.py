from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'independent_residual.cpp').read_text().split('#include <gmpxx.h>')[0]
s=s.replace('for(int c=0;c<d;c++)dst[c]+=w*src[c];','for(int c=0;c<d;c++){long long term,z;assert(!__builtin_mul_overflow((long long)w,src[c],&term));assert(!__builtin_add_overflow(dst[c],term,&z));assert(z>=-(1LL<<31)&&z<(1LL<<31));dst[c]=z;}')
s=s.replace('Int term=(Int)l[i]*r[j]*factor,z;', 'assert(l[i]>=-(1LL<<31)&&l[i]<(1LL<<31)&&r[j]>=-(1LL<<31)&&r[j]<(1LL<<31)&&factor>=-4096&&factor<=4096);Int term=(Int)l[i]*r[j]*factor,z;')
s+='''
Ten image_preserve(const int*sites,int what,const Algebra&a){
 Ten v=what==1?R(sites):M(sites),out{};
 for(int i=0;i<a.q;i++)for(int j=i+1;j<a.q;j++)if(E[sites[i]][sites[j]])for(int p=0;p<a.k;p++){
  int w=E[sites[i]][sites[j]];
  if(a.p[p].mate[i]==j)add(out[p],v[p],-2*w);
  else{add(out[a.swap[i][j][p]],v[p],w);add(out[a.cap[i][j][p]],v[p],-w);}}
 for(int i=0;i<a.q;i++)for(auto[j,w]:neighbors[sites[i]]){bool occ=false;for(int k=0;k<a.q;k++)occ|=sites[k]==j;if(occ)continue;int source[6];copy(sites,sites+a.q,source);source[i]=j;Ten inc=what==1?R(source):M(source);for(int p=0;p<a.k;p++)add(out[p],inc[p],w);}
 return out;
}
Ten image_CM(const int*sites){Ten out{};bool occ[64]{};for(int i=0;i<4;i++)occ[sites[i]]=true;
 for(int u=0;u<N;u++)if(!occ[u])for(int v=u+1;v<N;v++)if(!occ[v]&&E[u][v]){
  int source[6];copy(sites,sites+4,source);source[4]=u;source[5]=v;Ten coeff=M(source);
  for(int r=0;r<15;r++){auto z=a6.p[r];int f=1;if(z.mate[4]==5)f=3;else{int x=z.mate[4],y=z.mate[5];z.mate[x]=y;z.mate[y]=x;}add(out[index(a4,z)],coeff[r],f*E[u][v]);}}
 return out;
}
Ten image_CR(const int*sites){Ten out{};
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]]){int src[4],pos[4],n=0;for(int k=0;k<6;k++)if(k!=i&&k!=j){src[n]=sites[k];pos[n++]=k;}Ten r=R(src);for(int p=0;p<3;p++){Pairing z{};z.mate[i]=j;z.mate[j]=i;for(int k=0;k<4;k++)z.mate[pos[k]]=pos[a4.p[p].mate[k]];add(out[index(a6,z)],r[p],E[sites[i]][sites[j]]);}}
 return out;
}
void matrix_commutator(Matrix&out,const int*sites,const Ten&left){bool occ[64]{};for(int i=0;i<6;i++)occ[sites[i]]=true;
 int vac=0;for(int u=0;u<N;u++)if(!occ[u])for(auto[v,w]:neighbors[u])if(u<v&&!occ[v])vac+=3*w*w;
 gram_contract(out,left,left,a6,vac);
 for(int i=0;i<6;i++)for(int j=i+1;j<6;j++)if(E[sites[i]][sites[j]]){Ten capped{};for(int p=0;p<15;p++)add(capped[a6.cap[i][j][p]],left[p],a6.p[p].mate[i]==j?3:1);int w=E[sites[i]][sites[j]];gram_contract(out,left,capped,a6,-w*w);}
 for(int k=0;k<6;k++)for(auto[center,w]:neighbors[sites[k]])for(auto[j,z]:neighbors[center])if(j!=sites[k]&&!occ[j]){
  int src[6];copy(sites,sites+6,src);src[k]=j;Ten incoming=M(src);
  if(!occ[center])gram_contract(out,left,incoming,a6,w*z);
  else{int i=find(sites,sites+6,center)-sites;int lo=min(i,k),hi=max(i,k);Ten capped{};for(int p=0;p<15;p++)add(capped[a6.cap[lo][hi][p]],incoming[p],a6.p[p].mate[i]==k?3:1);gram_contract(out,left,capped,a6,-w*z);}}
}
int main(int argc,char**argv){assert(argc==4);long long limit=stoll(argv[3]);ifstream in(argv[1]);in>>N>>d;assert(N<=32&&d<=14);int ne;in>>ne;for(int k=0;k<ne;k++){int i,j,w;in>>i>>j>>w;assert(w==1||w==2);E[i][j]=E[j][i]=w;neighbors[i].push_back({j,w});neighbors[j].push_back({i,w});}for(int i=0;i<N;i++)for(int j=i+1;j<N;j++){in>>orbit[i][j];orbit[j][i]=orbit[i][j];}
 initialize(a4,4);initialize(a6,6);for(int n=0;n<=64;n++){choose[n][0]=1;for(int k=1;k<=4;k++)choose[n][k]=n?choose[n-1][k-1]+choose[n-1][k]:0;}
 auto start=chrono::steady_clock::now();auto seconds=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};
 Rcache.resize(choose[N][4]);for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){int st[4]={a,b,c,e};Ten r=Runcached(st);for(int p=0;p<3;p++)Rcache[rank4(st)][p]=r[p];}
 double cached=seconds();long long total4=choose[N-1][3],total6=1;for(int k=1;k<=5;k++)total6=total6*(N-k)/k;
 long long stride4=limit?max(1LL,total4/limit):1,stride6=limit?max(1LL,total6/limit):1,i4=0,i6=0,n4=0,n6=0,nzero=0;
 Matrix pp{},tt{},cmcm{},comm{},ttzero{};
 for(int b=1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++){if(i4++%stride4)continue;int st[4]={0,b,c,e};Ten cm=image_CM(st),p=image_preserve(st,1,a4);for(int k=0;k<3;k++)add(p[k],cm[k],1);gram_contract(pp,p,p,a4);gram_contract(cmcm,cm,cm,a4);n4++;}
 double phase4=seconds();
 for(int b=1;b<N;b++)for(int c=b+1;c<N;c++)for(int e=c+1;e<N;e++)for(int f=e+1;f<N;f++)for(int g=f+1;g<N;g++){if(i6++%stride6)continue;int st[6]={0,b,c,e,f,g};Ten m=M(st),t=image_preserve(st,2,a6),cr=image_CR(st);bool active=false;for(int p=0;p<15;p++){add(t[p],cr[p],1);for(int j=0;j<d;j++)active|=m[p][j]!=0;}gram_contract(tt,t,t,a6);if(active)matrix_commutator(comm,st,m);else{gram_contract(ttzero,t,t,a6);nzero++;}n6++;}
 double elapsed=seconds();rusage u{};getrusage(RUSAGE_SELF,&u);ofstream out(argv[2]);out<<"{\\n\\"N\\":"<<N<<",\\"d\\":"<<d<<",\\"partial\\":"<<(limit?"true":"false")<<",\\"q4_processed\\":"<<n4<<",\\"q6_processed\\":"<<n6<<",\\"M_zero_supports\\":"<<nzero<<",\\"cache_seconds\\":"<<cached<<",\\"q4_seconds\\":"<<phase4-cached<<",\\"q6_seconds\\":"<<elapsed-phase4<<",\\"seconds\\":"<<elapsed<<",\\"peak_rss_kib\\":"<<u.ru_maxrss;
 emit(out,"PP",pp,4,!limit);emit(out,"TT",tt,6,!limit);emit(out,"CMCM",cmcm,4,!limit);emit(out,"COMM",comm,6,!limit);emit(out,"TT_on_M_zero",ttzero,6,!limit);out<<"\\n}\\n";
}
'''
(p/'independent_matrix.cpp').write_text(s)
