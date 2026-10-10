"""Copy a saved image into the same exact packed Hamiltonian-input format."""
from pathlib import Path
import json,sys,shutil
p=Path(__file__).resolve().parent;source,target=sys.argv[1:]
r=json.loads((p/(source+'.json')).read_text())
with (p/'packed_input.txt').open() as f:header=[next(f) for _ in range(82)]
with (p/target).open('w') as out:
 out.write(f"{r['integer_denominator']} {r['image_support']}\n");out.writelines(header[1:])
 with (p/(source+'_image.txt')).open() as inp:shutil.copyfileobj(inp,out)
