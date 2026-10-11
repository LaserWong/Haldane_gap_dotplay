#!/usr/bin/env python3
import pathlib, json, hashlib
here=pathlib.Path(__file__).resolve().parent
for name,base in [('MANIFEST_SHA256.json',here),('INPUT_SHA256.json',here.parent.parent)]:
    for path,expected in json.loads((here/name).read_text()).items():
        assert hashlib.sha256((base/path).read_bytes()).hexdigest()==expected,path
print('PASS: independent review and frozen producer hashes')
