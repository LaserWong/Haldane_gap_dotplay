from pathlib import Path
root=Path(__file__).resolve().parent
s=(root.parents[1]/'heat_trace/spin2/chebyshev_columns.cpp').read_text()
s=s.replace('// Prototype/benchmark:', '// Audited bounded benchmark:')
s=s.replace('#include <cstdint>', '#include <cstdint>\n#include <climits>\n#include <cmath>')
s=s.replace('int start,int count){','int start,int count,bool horner,bool dump){')
s=s.replace(' std::vector<V>prev(d),cur(d),next(d),acc(d);i64 Q=i64(1)<<56;', ''' i64 Q=i64(1)<<56;
 if(K>640)throw std::runtime_error("degree outside audited range");
 // See PROOF.md: all algebraic embeddings are contractive and coordinate
 // size is <=2 times their norm. This bound also covers Horner accumulators.
 i64 ds=std::ceil(std::sqrt(double(d)));while(ds*ds<d)++ds;
 i64 eta=(7*ds+1)/2;
 i64 B=2*(Q+eta*(i64(K)*(K+1)/2+K+2));
 if(B>=(i64(1)<<58))throw std::runtime_error("coordinate invariant exceeds bound");
 i64 maxrow=0;
 for(int i=0;i<d;++i){std::array<i64,N> row{};
  for(int j=off[i];j<off[i+1];++j){auto e=edges[j];
   row[0]+=std::abs(e.a)+6*std::abs(e.b);row[1]+=std::abs(e.b)+std::abs(e.a);
   if constexpr(N==4){row[0]+=std::abs(e.c)+6*std::abs(e.d);row[1]+=std::abs(e.d)+std::abs(e.c);
    row[2]+=std::abs(e.c)+6*std::abs(e.d)+std::abs(e.a-e.c)+6*std::abs(e.b-e.d);
    row[3]+=std::abs(e.d)+std::abs(e.c)+std::abs(e.b-e.d)+std::abs(e.a-e.c);}}
  for(auto v:row)maxrow=std::max(maxrow,v);
 }
 if(i128(maxrow)*B/256+B+2>=INT64_MAX)throw std::runtime_error("int64 recurrence bound fails");
 // maxrow*B is much smaller than 2^127; a 32-row norm batch is <672*B^2<2^127.
 if(i128(maxrow)*B>=(i128(1)<<100))throw std::runtime_error("int128 matvec bound fails");
 std::cerr<<"AUDIT component_bound="<<B<<" max_integer_row_l1="<<maxrow<<" eta="<<eta<<" mode="<<(horner?"horner":"chebyshev")<<"\\n";
 std::vector<V>prev(horner?0:d),cur(d),next(d),acc(horner?0:d);''')
s=s.replace('  cur[reps[r].index][0]=Q;\n  for(int k=0;k<=K;++k){', '''  if(!horner)cur[reps[r].index][0]=Q;
  for(int step=0;step<=K;++step){
   int k=horner?K-step:step;''')
s=s.replace('   if(coef[k])for', '   if(!horner && coef[k])for')
s=s.replace('   if(k==K)break;', '   if(!horner && k==K)break;')
s=s.replace('next[i][a]=k==0?floorpow<9>(s[a]):floorpow<8>(s[a])-prev[i][a];', 'next[i][a]=horner?floorpow<9>(s[a]):(k==0?floorpow<9>(s[a]):floorpow<8>(s[a])-prev[i][a]);')
s=s.replace('   prev.swap(cur);cur.swap(next);','''   if(horner){next[reps[r].index][0]+=coef[k];cur.swap(next);}
   else{prev.swap(cur);cur.swap(next);}''')
s=s.replace('  mpz_class n0=0', '  if(horner)acc.swap(cur);\n  mpz_class n0=0')
s=s.replace('  std::cout<<reps[r].code', '''  if(dump)for(int i=0;i<d;++i){std::cout<<"V "<<i;for(int j=0;j<N;++j)std::cout<<" "<<acc[i][j];std::cout<<"\\n";}
  std::cout<<reps[r].code''')
s=s.replace('<<"\\n";\n }\n double sec=', '<<"\\n"<<std::flush;\n  if(horner){acc.swap(cur);}\n }\n double sec=')
s=s.replace(' if(argc!=8)', ' if(argc!=8)')
s=s.replace('list|compute', 'list|compute|dump|horner|horner_dump')
s=s.replace('std::string twist=argv[2];', 'std::string twist=argv[2],action=argv[7];bool horner=(action=="horner"||action=="horner_dump"),dump=(action=="dump"||action=="horner_dump");')
s=s.replace(' if(n<3', ' if(start<0||count<0||start>1000000||count>1000000)throw std::runtime_error("bad column range");\n if(n<3')
s=s.replace('if(coef.empty())', 'if(coef.empty()||coef.size()>641)')
s=s.replace('int d=words.size();std::vector<Rep>reps;', 'int d=words.size();std::vector<Rep>reps;')
s=s.replace(' if(std::string(argv[7])=="list")', ''' long long weights=0;for(auto r:reps)weights+=r.mult;
 if(weights!=i64(d)*(m<0?2:1))throw std::runtime_error("orbit mass mismatch");
 if(action=="list")''')
s=s.replace('if(std::string(argv[7])!="compute")', 'if(action!="compute"&&!horner&&!dump)')
s=s.replace('coef,start,count);', 'coef,start,count,horner,dump);')
(root/'chebyshev_columns.cpp').write_text(s)
