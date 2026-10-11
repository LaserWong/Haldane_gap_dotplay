// Test-only single-process pre-exec delay; never used as production scientific kernel.
#include <cstdlib>
#include <fstream>
#include <string>
#include <unistd.h>
#include <sys/resource.h>
int main(int argc,char**argv){std::string dir=getenv("RESIDUAL_TEST_DIR");{std::ofstream f(dir+"/child.pid");f<<getpid()<<"\n";}
 if(access((dir+"/allow_go").c_str(),F_OK)!=0)sleep(20);
 execv(getenv("RESIDUAL_REAL_KERNEL"),argv);return 127;}
