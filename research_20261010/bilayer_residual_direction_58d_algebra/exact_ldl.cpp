#include <gmpxx.h>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <cassert>
using namespace std;int main(int argc,char**argv){assert(argc==3);ifstream in(argv[1]);ofstream out(argv[2]);int jobs;in>>jobs;out<<"[";for(int job=0;job<jobs;job++){string name;int n;in>>name>>n;vector<vector<mpq_class>>a(n,vector<mpq_class>(n));for(auto&r:a)for(auto&v:r){string x;in>>x;v=mpq_class(x);v.canonicalize();}for(int i=0;i<n;i++)for(int j=0;j<n;j++)assert(a[i][j]==a[j][i]);vector<mpq_class>piv;bool psd=true;int rank=0,bad=-1;for(int j=0;j<n;j++){mpq_class p=a[j][j];piv.push_back(p);if(p<0){psd=false;bad=j;break;}if(p==0){for(int k=j+1;k<n;k++)if(a[k][j]!=0){psd=false;bad=j;}if(!psd)break;continue;}rank++;for(int i=j+1;i<n;i++)if(a[i][j]!=0)for(int k=i;k<n;k++)if(a[k][j]!=0){a[i][k]-=a[i][j]*a[k][j]/p;a[k][i]=a[i][k];}}if(job)out<<',';out<<"{\"name\":\""<<name<<"\",\"dimension\":"<<n<<",\"PSD\":"<<(psd?"true":"false")<<",\"rank_if_PSD\":"<<rank<<",\"failure_pivot\":"<<bad<<",\"pivots\":[";for(size_t k=0;k<piv.size();k++){if(k)out<<',';out<<'"'<<piv[k]<<'"';}out<<"]}";out.flush();}out<<"]\n";}
