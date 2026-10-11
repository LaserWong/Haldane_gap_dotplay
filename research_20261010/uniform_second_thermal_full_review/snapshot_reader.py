"""Verify immutable archive before exposing a disposable local replay tree."""
from pathlib import Path
import hashlib,json,zipfile

def campaign(p):
 archive=p/'campaign_snapshot.zip';want=(p/'SNAPSHOT_ARCHIVE_SHA256.txt').read_text().split()[0]
 assert hashlib.sha256(archive.read_bytes()).hexdigest()==want
 pins=json.loads((p/'SNAPSHOT_SHA256.json').read_text());out=p/'.replay_snapshot'
 with zipfile.ZipFile(archive) as z:
  assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(pins)
  for name,h in pins.items():
   rel=Path(name);assert not rel.is_absolute() and '..' not in rel.parts
   b=z.read(name);assert hashlib.sha256(b).hexdigest()==h
   f=out/rel;f.parent.mkdir(parents=True,exist_ok=True)
   if f.exists():assert f.read_bytes()==b
   else:f.write_bytes(b)
 return out
