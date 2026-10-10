// Independent exact contraction engine for Appendix C of the uploaded paper.
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
 if(argc!=2){std::cerr<<"Usage: mps_exact blocks.txt\n";return 2;}
 std::ifstream in(argv[1]); if(!in){return 3;}int nb; in>>nb;
 Z u72=0,v72=0,u120=0,v120=0;
 for(int h=0;h<nb;h++){
  int delta,n;in>>delta>>n;Mat T(n),O(n);for(auto&x:T.a)in>>x;for(auto&x:O.a)in>>x;
  auto t=std::chrono::steady_clock::now();
  Mat t2=mul(T,T),t4=mul(t2,t2),t8=mul(t4,t4),t16=mul(t8,t8),t32=mul(t16,t16),t64=mul(t32,t32);
  Mat t70=mul(mul(t64,t4),t2);
  Mat t118=mul(mul(mul(mul(t64,t32),t16),t4),t2);
  u72+=trprod(t70,O);v72+=trprod(t70,t2);
  u120+=trprod(t118,O);v120+=trprod(t118,t2);
  std::cerr<<"block "<<delta<<" dimension "<<n<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count()<<"\n";
 }
 std::cout<<"U72="<<u72<<"\nV72="<<v72<<"\nU120="<<u120<<"\nV120="<<v120<<"\n";
 Z scale("1000000000000"),c72("1401482112601"),c120("1401482105174");
 bool ok72=v72>0 && -c72*v72<=scale*u72 && scale*u72<(-c72+1)*v72 && -700741*v72-500000*u72>0;
 bool ok120=v120>0 && -c120*v120<=scale*u120 && scale*u120<(-c120+1)*v120 && -700741*v120-500000*u120>0;
 std::cout<<"Appendix_C8_N72="<<ok72<<"\nAppendix_C8_N120="<<ok120<<"\n";
 return ok72&&ok120?0:1;
}
