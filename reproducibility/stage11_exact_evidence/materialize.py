#!/usr/bin/env python3
"""Restore exact stage11 evidence with Python's standard library only."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
CHUNK = 1024 * 1024


def digest(path):
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as f:
        for block in iter(lambda: f.read(CHUNK), b''):
            h.update(block)
            size += len(block)
    return size, h.hexdigest()


def safe_path(root, relative):
    p = PurePosixPath(relative)
    if p.is_absolute() or not p.parts or any(x in ('..', '.', '') for x in p.parts):
        raise ValueError('Unsafe manifest path: ' + relative)
    result = root.joinpath(*p.parts)
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes repository: ' + relative)
    current = result
    while current != root:
        if current.is_symlink():
            raise ValueError('Refusing symlink: ' + str(current))
        current = current.parent
    return result


def load_manifest(path):
    manifest = json.loads(path.read_text())
    if manifest.get('format') != 'exact-evidence-gzip-parts-v1':
        raise ValueError('Unsupported evidence format')
    seen = set()
    for obj in manifest['objects']:
        for target in obj['targets']:
            if target['path'] in seen:
                raise ValueError('Duplicate target path')
            seen.add(target['path'])
    return manifest


def materialize(root, manifest_path, verify_only=False):
    root = root.resolve()
    manifest = load_manifest(manifest_path)
    # Preflight all existing destinations before restoring any missing file.
    targets = []
    for obj in manifest['objects']:
        expected = (obj['raw_bytes'], obj['raw_sha256'])
        for target in obj['targets']:
            dst = safe_path(root, target['path'])
            if dst.exists() and (not dst.is_file() or digest(dst) != expected):
                raise ValueError('Existing evidence differs; refusing overwrite: ' + target['path'])
            if verify_only and not dst.exists():
                raise ValueError('Missing evidence: ' + target['path'])
            targets.append(dst)
    restored = 0
    for obj in manifest['objects']:
        # Always check parts and gzip hash, even on an idempotent second run.
        with tempfile.TemporaryFile() as archive:
            gh = hashlib.sha256()
            gzsize = 0
            for part in obj['parts']:
                p = safe_path(manifest_path.parent, part['path'])
                if digest(p) != (part['bytes'], part['sha256']):
                    raise ValueError('Transport part hash/size mismatch: ' + part['path'])
                with p.open('rb') as source:
                    for block in iter(lambda: source.read(CHUNK), b''):
                        archive.write(block)
                        gh.update(block)
                        gzsize += len(block)
            if (gzsize, gh.hexdigest()) != (obj['gzip_bytes'], obj['gzip_sha256']):
                raise ValueError('Combined gzip hash/size mismatch')
            missing = [t for t in obj['targets'] if not safe_path(root, t['path']).exists()]
            if not missing:
                continue
            archive.seek(0)
            with tempfile.TemporaryFile() as raw:
                h = hashlib.sha256()
                size = 0
                with gzip.GzipFile(fileobj=archive, mode='rb') as stream:
                    for block in iter(lambda: stream.read(CHUNK), b''):
                        size += len(block)
                        if size > obj['raw_bytes']:
                            raise ValueError('Decompressed data exceeds sealed byte count')
                        h.update(block)
                        raw.write(block)
                if (size, h.hexdigest()) != (obj['raw_bytes'], obj['raw_sha256']):
                    raise ValueError('Decompressed evidence hash/size mismatch')
                for target in missing:
                    dst = safe_path(root, target['path'])
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    fd, tempname = tempfile.mkstemp(prefix='.' + dst.name + '.', dir=dst.parent)
                    tmp = Path(tempname)
                    try:
                        with os.fdopen(fd, 'wb') as out:
                            raw.seek(0)
                            shutil.copyfileobj(raw, out, CHUNK)
                            out.flush()
                            os.fsync(out.fileno())
                        os.chmod(tmp, int(target['mode'], 8))
                        if digest(tmp) != (obj['raw_bytes'], obj['raw_sha256']):
                            raise ValueError('Temporary output verification failed')
                        # link() atomically creates the destination without overwriting
                        # an existing or concurrently created file.
                        os.link(tmp, dst)
                        restored += 1
                    finally:
                        tmp.unlink(missing_ok=True)
    return {'status': 'PASS', 'verified_paths': len(targets),
            'unique_contents': len(manifest['objects']), 'restored_paths': restored}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=HERE.parent.parent)
    parser.add_argument('--manifest', type=Path, default=HERE / 'MANIFEST.json')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    print(json.dumps(materialize(args.repo_root, args.manifest.resolve(), args.verify_only)))


if __name__ == '__main__':
    main()
