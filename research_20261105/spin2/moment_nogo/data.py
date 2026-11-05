# Load the published spin-1 Z,P enclosures (beta=49/4, shift a) exactly as uniform_second_moment_optimization/explore.py does.
import ast, math
from pathlib import Path
from fractions import Fraction as F
R = Path('/workspace/haldane_chat_bundle/audit_copy')
src = R/'upstream/extracted/cases/haldane_reference_audit/published_scalar_enclosures.py'
tree = ast.parse(src.read_text())
tab = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'B' for t in n.targets))
D = {}
for j, (n, c, W) in enumerate(tab):
    x = F(49,4)*n*(F(3,2)-F(700741,500000)); s = sum((x**k/F(math.factorial(k)) for k in range(101)), F())
    d = math.isqrt(3**n)+1; err = d*(281*(d+1)+1); r = math.isqrt(W)
    lo = s*max(0, r-err)**2/2**110; hi = (s+x**100/F(math.factorial(100)))*(r+1+err)**2/2**110
    grid = 10**18
    D[n, j % 2] = (F(lo.numerator*grid//lo.denominator, grid), F(-((-hi.numerator*grid)//hi.denominator), grid))
Z = {n: D[n,0] for n in range(4,13)}   # identity seam: full trace Z_n
P = {n: D[n,1] for n in range(4,13)}   # pi seam: twisted trace P_n
# anchors (uniform_smaller_second_initialization/certificate_w12_Z1.json): Z_L(beta0) >= exp(-beta0*R_L), R_L<0
ANCHOR_R = {60: -1.1857985499551148e-05, 64: -9.283946501609371e-06, 68: -8.322178606774621e-06}
BETA = F(49,4)
