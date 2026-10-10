from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'chebyshev_columns.cpp').read_text()
start=s.index('template<int N>void compute(');end=s.index('\nint main(',start)
func=r'''
// Compressed parity basis, exact split fixed-point matvec, and column blocking.
// C++20 signed right shift is arithmetic. These identities are also checked below.
static_assert((-1 >> 8)==-1 && (-1 & 255)==255);
template<int N>struct CEdge{int source;std::array<int16_t,2*N> c;};
template<int Bits,int N,int B>void split_apply(const std::vector<int>&off,const std::vector<CEdge<N>>&edges,const std::vector<std::array<i64,N*B>>&cur,std::vector<std::array<i64,N*B>>&next,const std::vector<std::array<i64,N*B>>&prev,const std::array<int,B>&par,bool twice){
 const i64 mask=(i64(1)<<Bits)-1;int d=off.size()-1;
 for(int i=0;i<d;++i){std::array<i64,N*B>hi{},lo{};
  for(int p=off[i];p<off[i+1];++p){const auto&e=edges[p];const auto&x=cur[e.source];
   for(int q=0;q<B;++q){i64 a=e.c[par[q]*N];i64 u=x[q*N];
    if constexpr(N==1){hi[q]+=a*(u>>Bits);lo[q]+=a*(u&mask);}
    else{i64 b=e.c[par[q]*N+1],v=x[q*N+1];
     hi[q*N]+=a*(u>>Bits)-b*(v>>Bits);lo[q*N]+=a*(u&mask)-b*(v&mask);
     hi[q*N+1]+=b*(u>>Bits)+(a-b)*(v>>Bits);lo[q*N+1]+=b*(u&mask)+(a-b)*(v&mask);}
   }
  }
  for(int q=0;q<N*B;++q)next[i][q]=hi[q]+(lo[q]>>Bits)-(twice?prev[i][q]:0);
 }
}
template<int N,int B>void compute_compressed(const std::vector<int>&off,const std::vector<Edge>&full,const std::vector<Rep>&reps,const std::vector<int>&wordpar,const std::vector<i64>&coef,int start,int count,bool dump){
 using V=std::array<i64,N*B>;int d=off.size()-1,K=coef.size()-1;while(K>0&&!coef[K])--K;
 i64 Q=i64(1)<<56,ds=std::ceil(std::sqrt(double(d)));while(ds*ds<d)++ds;
 i64 eta=(7*ds+1)/2,CB=2*(Q+eta*(i64(K)*(K+1)/2+K+2));
 if(K>640||CB>=(i64(1)<<58))throw std::runtime_error("component range failed");
 std::vector<CEdge<N>>edges(full.size());i64 maxrow=0;
 for(int i=0;i<d;++i){std::array<i64,2*N>rr{};
  for(int p=off[i];p<off[i+1];++p){auto e=full[p];edges[p].source=e.source;
   for(int seed=0;seed<2;++seed){int factor=(wordpar[i]^seed)?1:6;int a=e.a+factor*e.b,b=e.c+factor*e.d;
    if(std::abs(a)>32767||std::abs(b)>32767)throw std::runtime_error("edge range failed");
    edges[p].c[seed*N]=a;
    if constexpr(N==1){rr[seed]+=std::abs(a);}
    else{edges[p].c[seed*N+1]=b;rr[seed*N]+=std::abs(a)+std::abs(b);rr[seed*N+1]+=std::abs(b)+std::abs(a-b);}
   }
  }
  for(auto x:rr)maxrow=std::max(maxrow,x);
 }
 if(i128(maxrow)*(CB/256+2)+CB>=INT64_MAX)throw std::runtime_error("split high sum exceeds signed64");
 if(i128(maxrow)*511>=INT64_MAX)throw std::runtime_error("split low sum exceeds signed64");
 // Clear the uncompressed graph in the caller before this routine in a future
 // graph-only loader; the present bounded benchmark temporarily keeps it.
 std::vector<V>prev(d),cur(d),next(d),acc(d);
 auto begin=std::chrono::steady_clock::now();auto cpu=std::clock();int completed=0;
 for(int r=start;r<int(reps.size())&&r<start+count;r+=B){
  std::fill(prev.begin(),prev.end(),V{});std::fill(cur.begin(),cur.end(),V{});std::fill(acc.begin(),acc.end(),V{});
  int active=std::min({B,int(reps.size())-r,start+count-r});std::array<int,B>par{};
  for(int q=0;q<active;++q){par[q]=wordpar[reps[r+q].index];cur[reps[r+q].index][q*N]=Q;}
  for(int k=0;k<=K;++k){
   if(coef[k])for(int i=0;i<d;++i)for(int a=0;a<N*B;++a)acc[i][a]+=floorpow<56>(i128(coef[k])*cur[i][a]);
   if(k==K)break;
   if(k==0)split_apply<9,N,B>(off,edges,cur,next,prev,par,false);
   else split_apply<8,N,B>(off,edges,cur,next,prev,par,true);
   prev.swap(cur);cur.swap(next);
  }
  for(int q=0;q<active;++q){mpz_class norm=0;i128 partial=0;int batch=0;
   for(int i=0;i<d;++i){i128 a=acc[i][q*N],b=0;if constexpr(N==2)b=acc[i][q*N+1];int factor=(wordpar[i]^par[q])?6:1;
    partial+=factor*(a*a-a*b+b*b);if(++batch==32){norm+=mpz_class(dec(partial));partial=0;batch=0;}
    if(dump){bool rad=wordpar[i]^par[q];std::cout<<"V "<<i<<" "<<(rad?0:i64(a))<<" "<<(rad?i64(a):0);if constexpr(N==2)std::cout<<" "<<(rad?0:i64(b))<<" "<<(rad?i64(b):0);std::cout<<"\n";}
   }
   norm+=mpz_class(dec(partial));std::cout<<reps[r+q].code<<" "<<reps[r+q].mult<<" "<<norm<<" 0\n"<<std::flush;++completed;
  }
 }
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count(),cpusec=double(std::clock()-cpu)/CLOCKS_PER_SEC;
 std::cerr<<"compute_seconds="<<sec<<" compute_cpu_seconds="<<cpusec<<" dimension="<<d<<" nnz="<<edges.size()<<" block_reps="<<reps.size()<<" degree="<<K<<" components="<<N<<" block_columns="<<B<<" completed="<<completed<<" max_integer_row_l1="<<maxrow<<" component_bound="<<CB<<"\n";
}
template<int N>void dispatch(int block,const std::vector<int>&off,const std::vector<Edge>&edges,const std::vector<Rep>&reps,const std::vector<int>&wordpar,const std::vector<i64>&coef,int start,int count,bool dump){
 switch(block){
 case 1:compute_compressed<N,1>(off,edges,reps,wordpar,coef,start,count,dump);break;
 case 2:compute_compressed<N,2>(off,edges,reps,wordpar,coef,start,count,dump);break;
 case 4:compute_compressed<N,4>(off,edges,reps,wordpar,coef,start,count,dump);break;
 case 8:compute_compressed<N,8>(off,edges,reps,wordpar,coef,start,count,dump);break;
 default:throw std::runtime_error("unsupported block columns");}
}
'''
s=s[:start]+func+s[end:]
s=s.replace('#include <cmath>','#include <cmath>\n#include <ctime>')
s=s.replace('if(argc!=8)','if(argc!=8&&argc!=9)')
s=s.replace('int n=std::stoi(argv[1]),','int block=argc==9?std::stoi(argv[8]):1;int n=std::stoi(argv[1]),')
s=s.replace(' int d=words.size();std::vector<Rep>reps;', ' int d=words.size();std::vector<int>wordpar(d);for(int i=0;i<d;++i)wordpar[i]=std::count(words[i].begin(),words[i].end(),0)%2;std::vector<Rep>reps;')
s=s.replace(' if(action!="compute"&&!horner&&!dump)', ' if(horner)throw std::runtime_error("compressed benchmark implements Chebyshev only");\n if(action!="compute"&&!dump)')
s=s.replace('if(twist=="C")compute<4>(off,edges,reps,coef,start,count,horner,dump);else compute<2>(off,edges,reps,coef,start,count,horner,dump);', 'if(twist=="C")dispatch<2>(block,off,edges,reps,wordpar,coef,start,count,dump);else dispatch<1>(block,off,edges,reps,wordpar,coef,start,count,dump);')
(R/'compressed_columns.cpp').write_text(s)
