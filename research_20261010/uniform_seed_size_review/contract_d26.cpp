// Independent sequential powers through 24, no many-body spectrum.
#include <gmpxx.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <sys/resource.h>
#include <chrono>
using Z=mpz_class;
struct Matrix {int d;std::vector<Z>x;Matrix(int d):d(d),x(d*d){};};
Matrix multiply(const Matrix&a,const Matrix&b){Matrix c(a.d);for(int i=0;i<a.d;i++)for(int k=0;k<a.d;k++)if(a.x[i*a.d+k]!=0)for(int j=0;j<a.d;j++)if(b.x[k*a.d+j]!=0)c.x[i*a.d+j]+=a.x[i*a.d+k]*b.x[k*a.d+j];return c;}
Z trace(const Matrix&a){Z s=0;for(int i=0;i<a.d;i++)s+=a.x[i*a.d+i];return s;}
Z insertion(const Matrix&a,const Matrix&b){Z s=0;for(int i=0;i<a.d;i++)for(int j=0;j<a.d;j++)s+=a.x[i*a.d+j]*b.x[j*a.d+i];return s;}
int main(int argc,char**argv){if(argc!=2)return 2;auto start=std::chrono::steady_clock::now();std::ifstream in(argv[1]);int count;in>>count;Z U[25],V[25];while(count--){int q,d;in>>q>>d;Matrix t(d),o(d),p(d);for(auto&v:t.x)in>>v;for(auto&v:o.x)in>>v;for(int i=0;i<d;i++)p.x[i*d+i]=1;for(int k=1;k<=24;k++){p=multiply(p,t);if(k==10||k==14||k==18||k==22)U[k+2]+=insertion(p,o);if(k==12||k==16||k==20||k==24)V[k]+=trace(p);}std::cerr<<"block "<<q<<" dimension "<<d<<" PASS\n";}for(int L:{12,16,20,24})std::cout<<"U"<<L<<"="<<U[L]<<"\nV"<<L<<"="<<V[L]<<"\n";rusage r;getrusage(RUSAGE_SELF,&r);std::cerr<<"seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<" peak_kb="<<r.ru_maxrss<<"\n";}
