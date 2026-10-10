// Exact trace of a conditioned-Poisson polynomial for spin-2 H4.
#include <gmpxx.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <chrono>
using Z=mpz_class;
struct E{int i,j,a,b;};
void addmul(Z&x,const Z&y,int a){if(a>0)mpz_addmul_ui(x.get_mpz_t(),y.get_mpz_t(),a);else if(a<0)mpz_submul_ui(x.get_mpz_t(),y.get_mpz_t(),-a);}
int main(int argc,char**argv){if(argc!=2)return 2;std::ifstream in(argv[1]);if(!in)return 3;
 const int mu=144,J=640,q=36;std::vector<Z>coeff(J+1);mpz_ui_pow_ui(coeff[J].get_mpz_t(),mu,J);
 for(int j=J;j>0;j--){coeff[j-1]=coeff[j]*j*q;mpz_divexact_ui(coeff[j-1].get_mpz_t(),coeff[j-1].get_mpz_t(),mu);}
 Z w;mpz_ui_pow_ui(w.get_mpz_t(),mu,J);Z den=w;for(int j=J;j>0;j--){w*=j;mpz_divexact_ui(w.get_mpz_t(),w.get_mpz_t(),mu);den+=w;}Z qp;mpz_ui_pow_ui(qp.get_mpz_t(),q,J);den*=qp;
 int nb;in>>nb;Z total=0;auto t=std::chrono::steady_clock::now();
 for(int bl=0;bl<nb;bl++){int d,mult,nnz;in>>d>>mult>>nnz;std::vector<E>es(nnz);for(auto&e:es)in>>e.i>>e.j>>e.a>>e.b;
 std::vector<Z>u(d*d),v(d*d);for(int j=J;j>=0;j--){std::vector<Z>un(d*d),vn(d*d);for(const auto&e:es)for(int k=0;k<d;k++){
  const Z&x=u[e.j*d+k];const Z&y=v[e.j*d+k];Z&ox=un[e.i*d+k];Z&oy=vn[e.i*d+k];addmul(ox,x,e.a);addmul(ox,y,-e.b);addmul(oy,y,e.a-e.b);addmul(oy,x,e.b);
 }for(int i=0;i<d;i++)un[i*d+i]+=coeff[j];u.swap(un);v.swap(vn);}
 Z tr=0,im=0;for(int i=0;i<d;i++){tr+=u[i*d+i];im+=v[i*d+i];}if(im!=0){std::cerr<<"NONREAL TRACE\n";return 4;}total+=mult*tr;
 std::cerr<<"block="<<bl<<" dim="<<d<<" elapsed="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count()<<"\n";}
 std::cout<<"numerator="<<total<<"\ndenominator="<<den<<"\nmu="<<mu<<"\nJ="<<J<<"\nbeta=8\nq="<<q<<"\n";return 0;
}
