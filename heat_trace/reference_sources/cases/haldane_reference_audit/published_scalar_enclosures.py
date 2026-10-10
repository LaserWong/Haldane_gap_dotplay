"""Audit scalar inequalities from the uploaded PDF with exact rational arithmetic.
Thermal totals in this file are transcribed certificates, NOT recomputed matrices.
The separate thermal_small_exact.py rebuilds nine physical traces independently.
"""
from fractions import Fraction as F
from math import factorial,isqrt

A=[
(6,8945303,93637037510293158533967385845216),
(6,346734,3629519998654831111446492683663),
(6,939987,9839536903588146388838689926305),
(8,3741281,4947327904487991279560670127283),
(8,567167,749999795795292705866802820621),
(8,984108,1301346729026243689610427021457),
(10,2327547,388818111664728958208623998490),
(10,721090,120458568770462253326886628639),
(10,1002613,167487042402286114495695779656)]
B=[
(4,124885379,1298092848946206529211955779616040),(4,65757,683496640248050713756440676071),
(5,2925,9095379218684502088743241789),(5,2960742,9205948219074287936685289758037),
(6,12870614,11971284263768914176431179720622),(6,286599,266573596119930013833919176645),
(7,54069,15044150708248976451784593468),(7,1920414,534330762492192297990602166370),
(8,4639283,386135473475360677201628357188),(8,510140,42459883501386986922766507327),
(9,195455,4866417737994347551816846903),(9,1514846,37716485750353424806876104310),
(10,2654823,19772960374215472827775892486),(10,675419,5030484777222468978572235564),
(11,377629,841347687722481981930750335),(11,1314544,2928767918985354021900689432),
(12,1900547,1266666171463993322695232916),(12,787405,524785463625387865619045258)]
a=F(700741,500000)
for n,c,t in A:
    x=F(21,2)*n*(F(3,2)-a);Q=2**56
    L=sum((x**j/F(factorial(j)) for j in range(101)),F(0))
    U=L+2*x**101/F(factorial(101));center=F(c,10**6)
    assert center-F(2,10**6)<L*t/(Q*Q)<U*t/(Q*Q)<center+F(2,10**6)
print('Appendix A.10: all 9 scalar enclosures from printed integer certificates PASS')
for n,c,t in B:
    x=F(49,4)*n*(F(3,2)-a);Q=2**55
    s=sum((x**j/F(factorial(j)) for j in range(101)),F(0))
    tn=x**100/F(factorial(100));r=isqrt(t);dn=isqrt(3**n)+1;err=dn*(281*(dn+1)+1)
    L=s*max(0,r-err)**2/(Q*Q);U=(s+tn)*(r+1+err)**2/(Q*Q)
    assert L>F(c-30,10**6) and U<F(c+30,10**6)
    assert L-F(c-30,10**6)>F(13,10**6) and F(c+30,10**6)-U>F(13,10**6)
print('Appendix B.9: all 18 scalar enclosures and claimed margins PASS')

# Full scalar chain in Proposition 5.4 (initialization at length sixty).
data={6:[8945303,346734,939987],8:[3741281,567167,984108],10:[2327547,721090,1002613]}
I={k:F(z+3*p+8*c,12*10**6) for k,(z,p,c) in data.items()}
O={k:F(z+3*p-4*c,12*10**6) for k,(z,p,c) in data.items()}
N={k:F(z-p,4*10**6) for k,(z,p,c) in data.items()}
eps=F(1,10**5)
mI,mO,mN=F(1042655,10**6),F(40041,10**6),F(401625,10**6)
assert all(M[10]+eps<m for M,m in [(I,mI),(O,mO),(N,mN)])
U,V=F(100245,100000),F(88643,100000)
for M,c0,c1,cap,minmargin in [(I,-2,10,U,F('0.0301')),(N,-25,100,V,F('0.3463'))]:
    bound=c0*c0*M[6]+2*c0*c1*M[8]+c1*c1*M[10]+eps*(abs(c0)+abs(c1))**2
    atcap=cap**6*(c0+c1*cap**2)**2
    assert atcap-bound>minmargin and c0+c1*cap**2>0
assert U**10<mI<2*U**10 and V**10<mN<2*V**10

def Ak(k):return U**k+(mI-U**10)**(k//10)
def Bk(k):return mO**(k//10)
def Ck(k):return V**k+(mN-V**10)**(k//10)
m=Ak(30)+2*Bk(30)+3*Ck(30);p=Ak(30)+2*Bk(30);q=Ak(120)+2*Bk(120)+3*Ck(120)
D,E,tau,tau0,Rq=F('1.450'),F('1.202'),F('1.225'),F('1.264'),F('.0684')
assert D**2-m**5>F('.001068') and E**2-p**5>F('.000433')
assert q>=1 and Rq**2-(q-1)**5>F('.0000472')
assert (D+11*E)/12<=tau and (D+3*E)/4<=tau0
assert D*F('.88')**3<1 and 2*F('.88')>D

def R(t):return max(F(x)*F(x)+F(y)*F(y)/2+(D-t-x-y)**2/3 for x,y in [(0,0),(tau-t,0),(tau-t,tau0-tau),(0,tau0-t)])
assert [R(F(s)) for s in ['.88','.99','.998']]==[F('.1359'),F('.0721'),F('.068404')]
assert 1-F('.99')**4-R(F('.88'))**2==F('.02093518')
assert 1-F('.998')**4-R(F('.99'))**2==F('.002777621984')
spatial=(1+R(F('.998'))/F('.998')**2)**(-2)
temporal=(1+Rq)**(-2)
assert spatial>F(7,8) and temporal>F(7,8)
print('Proposition 5.4: all displayed filter, moment, dominant-mass, and purity comparisons PASS')
print('Purity lower bounds:',float(spatial),float(temporal))
