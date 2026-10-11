from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'whole_original.cpp').read_text().replace('#include "brauer_snapshot.cpp"','#include "../bilayer_whole_m4_pipeline/brauer_snapshot.cpp"')
needle='o<<"},\\"moments\\":[\\""'
# Append a separate exact accumulator file beside every output.
pos='void output(string path,const Totals&t,System&sys,bool complete,string mode,double elapsed){'
rep=pos+'{ofstream a(path+".accumulators.json");auto vals=snapshot(t);a<<"[";for(int i=0;i<22;i++){if(i)a<<",";a<<"\\\""<<vals[i]<<"\\\"";}a<<"]\\n";}'
assert pos in s;s=s.replace(pos,rep)
needle='assert(mode=="sample");whole::System sys'
chunk='''if(mode=="chunk"){int nx=stoi(argv[7]),q=stoi(argv[8]);uint64_t begin=stoull(argv[9]),count=stoull(argv[10]);bool large=type=="sample";whole::System sys(nx,large?4:2,type,reference,input);for(int n=0;n<=32;n++){chooseN[n][0]=1;for(int k=1;k<=6;k++)chooseN[n][k]=n?chooseN[n-1][k-1]+chooseN[n-1][k]:0;}int shift=large&&(q==4||q==6),kk=q-shift,nn=sys.n-shift;uint64_t N=chooseN[nn][kk],stride=large?(q==6?65536:q==4?1024:q==2?127:1):(N>1?N-1:1);assert(gcd(stride,N)==1&&begin+count<=N);double setup=rule::cpu(),began=setup;ofstream targets(dir+"/targets.jsonl");for(uint64_t i=begin;i<begin+count;i++){uint64_t rank=(stride*i)%N,remaining=rank;whole::S target(q);if(shift)target[0]=0;int top=nn-1;for(int k=kk;k>=1;k--){while(chooseN[top][k]>long(remaining))top--;target[k-1+shift]=top+shift;remaining-=chooseN[top][k];top--;}assert(remaining==0);uint64_t rerank=0;for(int k=0;k<kk;k++)rerank+=chooseN[target[k+shift]-shift][k+1];assert(rerank==rank);whole::step(sys,target,totals,false);targets<<"{\\"id\\":"<<i<<",\\"rank\\":"<<rank<<"}\\n";targets.flush();}whole::output(dir+"/result.json",totals,sys,true,"chunk",rule::cpu()-began);ofstream meta(dir+"/chunk.json");meta<<"{\\"q\\":"<<q<<",\\"begin\\":"<<begin<<",\\"end\\":"<<begin+count<<",\\"N\\":"<<N<<",\\"stride\\":"<<stride<<",\\"setup_cpu\\":"<<setup<<",\\"body_cpu\\":"<<rule::cpu()-began<<"}";return 0;}assert(mode=="sample");whole::System sys'''
assert needle in s;s=s.replace(needle,chunk)
(p/'whole.cpp').write_text(s)
