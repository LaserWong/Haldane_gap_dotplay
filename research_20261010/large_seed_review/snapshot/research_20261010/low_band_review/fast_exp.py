"""Independent exact dyadic exponential enclosure with bounded denominator.
All truncation, arithmetic-rounding and range-reduction errors are enclosed.
"""
from fractions import Fraction as F
from functools import lru_cache
BITS=256;DEN=1<<BITS

def down(x):return F((x.numerator*DEN)//x.denominator,DEN)
def up(x):return -down(-x)

@lru_cache(None)
def exp_interval(x):
    x=F(x);y=abs(x);k=0
    while y>F(1,4):y/=2;k+=1
    tl=tu=sl=su=F(1)
    for j in range(1,71):
        tl=down(tl*y/j);tu=up(tu*y/j)
        sl+=tl;su+=tu
    su+=up((tu*y/71)/(1-y/72))
    for _ in range(k):sl=down(sl*sl);su=up(su*su)
    return (sl,su) if x>=0 else (down(1/su),up(1/sl))
