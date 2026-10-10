// Fresh contractions of audited archived D26 blocks. Original manuscript absent.
// Requires GMP development libraries. Input contains difference blocks of T and O.
#include <gmpxx.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <chrono>
using Z = mpz_class;
struct Mat {int n; std::vector<Z> a; explicit Mat(int n):n(n),a(n*n){};};
Mat mul(const Mat& A,const Mat& B){
 int n=A.n; Mat C(n);
 for(int i=0;i<n;i++) for(int k=0;k<n;k++) if(A.a[i*n+k]!=0)
  for(int j=0;j<n;j++) if(B.a[k*n+j]!=0)
   mpz_addmul(C.a[i*n+j].get_mpz_t(),A.a[i*n+k].get_mpz_t(),B.a[k*n+j].get_mpz_t());
 return C;
}
Z trprod(const Mat&A,const Mat&B){Z z=0; int n=A.n;for(int i=0;i<n;i++)for(int j=0;j<n;j++)mpz_addmul(z.get_mpz_t(),A.a[i*n+j].get_mpz_t(),B.a[j*n+i].get_mpz_t());return z;}

int main(int argc,char**argv){
 if(argc!=2)return 2;std::ifstream in(argv[1]);if(!in)return 3;
 int nb;in>>nb;std::vector<int> Ns={12,16,20,24};std::vector<Z> us(4),vs(4);
 for(int h=0;h<nb;h++){
  int delta,n;in>>delta>>n;Mat T(n),O(n);for(auto&x:T.a)in>>x;for(auto&x:O.a)in>>x;
  Mat t2=mul(T,T),t4=mul(t2,t2),t8=mul(t4,t4),t16=mul(t8,t8);
  std::vector<Mat> ps;ps.push_back(mul(t8,t2));ps.push_back(mul(mul(t8,t4),t2));ps.push_back(mul(t16,t2));ps.push_back(mul(mul(t16,t4),t2));
  for(int j=0;j<4;j++){us[j]+=trprod(ps[j],O);vs[j]+=trprod(ps[j],t2);}
  std::cerr<<"block "<<delta<<" dimension "<<n<<" complete\n";
 }
 for(int j=0;j<4;j++)std::cout<<"U"<<Ns[j]<<"="<<us[j]<<"\nV"<<Ns[j]<<"="<<vs[j]<<"\n";
}
