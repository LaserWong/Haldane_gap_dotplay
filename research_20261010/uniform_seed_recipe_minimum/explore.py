from pathlib import Path
import sys,math,json
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'uniform_seed_frontier_optimization'))
from explore import bounds
# The same module name on import can collide; execute imported file under a unique name below.
