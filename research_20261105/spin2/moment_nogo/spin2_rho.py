# ESTIMATE (floats, not rigorous); bc(b) returns beta*c(beta) per site (magnon-gas, 3 branches): ln rho_8(beta) for spin-2, rho_m := Z_m/lambda0^m - 1 >= exp(beta*(m e0 - E0(m)) - m*beta*c(beta)) - 1
import json, math
e0 = -4.761248; D = 0.08917; v = 4.41; E08 = -38.52186913540149; m = 8
gap = m*e0 - E08
def bc(b, fac=1.0): return fac*3*math.exp(-b*D)*math.sqrt(2*math.pi*D/b)/(2*math.pi*v)
for b in (10, 20, 30, 40, 56, 80):
    vals = [math.log(math.expm1(b*gap - m*bc(b, f))) for f in (2.0, 1.0, 0.5)]
    de0 = 8*b*1e-6  # e0 uncertainty ~1e-6/site (Todo-Kato quoted digits)
    print(f"beta={b:3d}  ln rho_8 ~ {vals[1]:.3f}  range(c x2, c/2) [{vals[0]:.3f},{vals[2]:.3f}]  +-{de0:.1e} from e0;  8*beta*c={8*bc(b):.2e}")
print('8e0-E0(8)=', gap)

