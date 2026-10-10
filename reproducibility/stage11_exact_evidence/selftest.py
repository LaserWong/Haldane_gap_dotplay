#!/usr/bin/env python3
"""Clean-checkout, raw-seal, idempotence, and corruption tests."""
import argparse
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('materializer', HERE / 'materialize.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test(repo):
    manifest = mod.load_manifest(HERE / 'MANIFEST.json')
    checks = []
    with tempfile.TemporaryDirectory(prefix='stage11-hydration-') as temporary:
        root = Path(temporary)
        pack = root / 'reproducibility/stage11_exact_evidence'
        shutil.copytree(HERE, pack, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for obj in manifest['objects']:
            for target in obj['targets']:
                seal = target['source_seal']
                src, dst = repo / seal['path'], root / seal['path']
                assert mod.digest(src)[1] == seal['sha256']
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists(): shutil.copy2(src, dst)
                assert not (root / target['path']).exists()
        first = mod.materialize(root, pack / 'MANIFEST.json')
        assert first == {'status': 'PASS', 'verified_paths': 18, 'unique_contents': 9, 'restored_paths': 18}
        checks.append('clean restoration of all 18 original paths')
        for obj in manifest['objects']:
            for target in obj['targets']:
                seal = target['source_seal']
                value = json.loads((root / seal['path']).read_text())
                for key in seal['keys']: value = value[key]
                assert value == obj['raw_sha256'] == mod.digest(root / target['path'])[1]
                assert (root / target['path']).stat().st_mode & 0o777 == int(target['mode'], 8)
        checks.append('all 18 original producer/review seal entries and modes replayed')
        assert mod.materialize(root, pack / 'MANIFEST.json')['restored_paths'] == 0
        assert mod.materialize(root, pack / 'MANIFEST.json', True)['restored_paths'] == 0
        checks.append('idempotence and verify-only')

        def rejected(label, changed, before=None):
            out = root / ('negative-' + str(len(checks)))
            out.mkdir()
            if before: before(out)
            bad = pack / ('negative-' + str(len(checks)) + '.json')
            bad.write_text(json.dumps(changed))
            try:
                mod.materialize(out, bad)
            except (ValueError, OSError, EOFError):
                checks.append(label)
            else:
                raise AssertionError('Guard failed: ' + label)

        one = copy.deepcopy(manifest)
        one['objects'] = one['objects'][:1]
        for label, change in [
            ('reject wrong transport part hash', lambda o: o['parts'][0].update(sha256='0'*64)),
            ('reject wrong combined gzip hash', lambda o: o.update(gzip_sha256='0'*64)),
            ('reject wrong raw hash', lambda o: o.update(raw_sha256='0'*64)),
            ('reject raw byte overflow', lambda o: o.update(raw_bytes=o['raw_bytes']-1)),
            ('reject path traversal', lambda o: o['targets'][0].update(path='../escape')),
        ]:
            bad = copy.deepcopy(one); change(bad['objects'][0]); rejected(label, bad)
        def differing(out):
            dst = out / one['objects'][0]['targets'][0]['path']
            dst.parent.mkdir(parents=True); dst.write_bytes(b'differing existing content')
        rejected('refuse differing existing file', one, differing)
        def symlink(out):
            dst = out / one['objects'][0]['targets'][0]['path']
            dst.parent.mkdir(parents=True); dst.symlink_to(repo / one['objects'][0]['targets'][0]['path'])
        rejected('refuse symlink destination', one, symlink)
    return {'status': 'PASS', 'raw_paths': 18, 'unique_contents': 9, 'checks': checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=HERE.parent.parent)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = test(args.repo_root.resolve())
    text = json.dumps(result, indent=2) + '\n'
    if args.output: args.output.write_text(text)
    print(text)
