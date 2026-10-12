#!/usr/bin/env python3
"""Restore exact Haldane machine-generated evidence. Python standard library only.

Run from a cloned repository:
  python reproducibility/current_complete_transport/materialize.py --verify-only
  python reproducibility/current_complete_transport/materialize.py

No research calculation or external-service action is performed.
"""
from pathlib import Path, PurePosixPath
import argparse, gzip, hashlib, io, json, os, stat, tempfile, zipfile


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_name(name):
    if not isinstance(name, str) or not name or '\\' in name or '\x00' in name:
        raise ValueError('Invalid path')
    p = PurePosixPath(name)
    if p.is_absolute() or ':' in name or any(x in ('', '.', '..') for x in name.split('/')):
        raise ValueError('Unsafe path: ' + name)
    return name


def confined(root, name):
    name = safe_name(name)
    root = Path(root).resolve()
    p = root / name
    current = root
    for part in name.split('/'):
        current = current / part
        if current.is_symlink():
            raise ValueError('Symlink in path: ' + name)
    if not p.resolve().is_relative_to(root):
        raise ValueError('Path escapes repository: ' + name)
    return p


def file_digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


class Reader:
    def __init__(self, repository_root, package_root=None):
        self.root = Path(repository_root).resolve()
        self.package_root = Path(package_root).resolve() if package_root else None
        self.verified_files = {}
        self.zip_cache = {}
        self.checked_payloads = {}
        self.virtual_bootstrap_files = {}

    def source_path(self, name):
        p = confined(self.root, name)
        if not p.is_file() and self.package_root:
            p = confined(self.package_root, name)
        if not p.is_file():
            raise ValueError('Missing source: ' + name)
        return p

    def checked_file(self, name, expected, size=None):
        p = self.source_path(name)
        current = p.stat()
        signature = (current.st_size, current.st_mtime_ns, current.st_ino)
        key = (str(p), expected, size)
        if self.verified_files.get(key) != signature:
            if size is not None and current.st_size != size:
                raise ValueError('Source size mismatch: ' + name)
            if file_digest(p) != expected:
                raise ValueError('Source SHA256 mismatch: ' + name)
            self.verified_files[key] = signature
        return p

    def zip_at(self, path, expected):
        key = ('root', safe_name(path), expected)
        if key not in self.zip_cache:
            if path in self.virtual_bootstrap_files:
                raw = self.virtual_bootstrap_files[path]
                if digest(raw) != expected:
                    raise ValueError('Bootstrap archive SHA256 mismatch')
                self.zip_cache[key] = self.open_zip(io.BytesIO(raw))
            else:
                p = self.checked_file(path, expected)
                self.zip_cache[key] = self.open_zip(p)
        return self.zip_cache[key]

    @staticmethod
    def open_zip(source):
        z = zipfile.ZipFile(source)
        seen = set()
        for info in z.infolist():
            safe_name(info.filename)
            mode = info.external_attr >> 16
            if info.filename in seen or info.is_dir() or stat.S_ISLNK(mode) or info.flag_bits & 1:
                raise ValueError('Unsafe or duplicate ZIP entry')
            if stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                raise ValueError('Non-regular ZIP member')
            seen.add(info.filename)
        return z

    def payload(self, spec):
        kind = spec['kind']
        if kind == 'gzip_parts':
            compressed = bytearray()
            for part in spec['parts']:
                p = self.checked_file(part['path'], part['sha256'], part['size'])
                compressed.extend(p.read_bytes())
            if len(compressed) != spec['gzip_size'] or digest(compressed) != spec['gzip_sha256']:
                raise ValueError('Compressed stream mismatch')
            raw = gzip.decompress(compressed)
        elif kind == 'zip_member':
            z = self.zip_at(spec['archive_path'], spec['archive_sha256'])
            steps = spec['members']
            if not steps:
                raise ValueError('Empty ZIP member chain')
            for i, step in enumerate(steps):
                name = safe_name(step['path'])
                info = z.getinfo(name)
                if info.file_size != step['size']:
                    raise ValueError('ZIP declared member size mismatch')
                raw = z.read(info)
                if len(raw) != step['size'] or digest(raw) != step['sha256']:
                    raise ValueError('ZIP member hash/size mismatch')
                if i + 1 < len(steps):
                    key = ('nested', step['sha256'])
                    if key not in self.zip_cache:
                        self.zip_cache[key] = self.open_zip(io.BytesIO(raw))
                    z = self.zip_cache[key]
        else:
            raise ValueError('Unknown transport kind')
        if len(raw) != spec['raw_size'] or digest(raw) != spec['raw_sha256']:
            raise ValueError('Final raw payload hash/size mismatch')
        return raw

    def verify_payload(self, spec):
        h = spec['raw_sha256']
        if h not in self.checked_payloads:
            raw = self.payload(spec)
            self.checked_payloads[h] = len(raw)
        if self.checked_payloads[h] != spec['raw_size']:
            raise ValueError('Inconsistent raw payload size')


def bootstrap_archives(manifest, reader, write=False):
    """Acyclic first layer: bounded gzip parts -> exact archives -> ZIP members."""
    bootstrap = manifest.get('bootstrap', {'sources': {}, 'targets': []})
    sources, targets = bootstrap['sources'], bootstrap['targets']
    target_names = set()
    for t in targets:
        name = safe_name(t['path'])
        if name in target_names or t['mode'] not in ('100644', '100755'):
            raise ValueError('Duplicate bootstrap target or invalid mode')
        target_names.add(name)
        src = sources.get(t['sha256'])
        if src is None or src['raw_sha256'] != t['sha256'] or src['raw_size'] != t['size']:
            raise ValueError('Unbound bootstrap target')
    for h, src in sources.items():
        if src.get('kind') != 'gzip_parts' or src.get('raw_sha256') != h:
            raise ValueError('Bootstrap may depend only on bounded direct gzip parts')
        for part in src['parts']:
            if safe_name(part['path']) in target_names:
                raise ValueError('Bootstrap dependency cycle')
    raw_by_hash = {}
    for h, src in sources.items():
        raw_by_hash[h] = reader.payload(src)
        reader.checked_payloads[h] = len(raw_by_hash[h])
    counts = {'restored': 0, 'already_exact': 0}
    for t in targets:
        raw = raw_by_hash[t['sha256']]
        if write:
            counts[write_exact(reader.root, t, raw)] += 1
        # Virtual sources force verification to use the split transport even if
        # an original archive happens to remain in the preparation workspace.
        reader.virtual_bootstrap_files[t['path']] = raw
    return counts


def parse_rows(raw):
    return [json.loads(line) for line in raw.splitlines() if line]


def load_catalog(manifest, reader):
    sources = {}
    for source in parse_rows(reader.payload(manifest['metadata']['sources'])):
        h = source['raw_sha256']
        if h in sources:
            raise ValueError('Duplicate source identity')
        sources[h] = source
    targets = parse_rows(reader.payload(manifest['metadata']['targets']))
    names = set()
    for target in targets:
        p = safe_name(target['path'])
        if p in names or target['mode'] not in ('100644', '100755'):
            raise ValueError('Duplicate target or unsupported mode')
        names.add(p)
        source = sources.get(target['sha256'])
        if not source or target['size'] != source['raw_size']:
            raise ValueError('Unbound target or inconsistent size')
        # Destination symlinks are checked at write time; verify-only writes nothing.
    if len(targets) != manifest['logical_target_count'] or len(sources) != manifest['unique_payload_count']:
        raise ValueError('Catalog count mismatch')
    if sum(t['size'] for t in targets) != manifest['logical_target_bytes']:
        raise ValueError('Catalog target byte count mismatch')
    return sources, targets


def write_exact(root, target, raw):
    p = confined(root, target['path'])
    mode = int(target['mode'][-3:], 8)
    if p.exists():
        if not p.is_file() or p.stat().st_size != target['size'] or file_digest(p) != target['sha256']:
            raise ValueError('Refusing to overwrite differing target: ' + target['path'])
        if stat.S_IMODE(p.stat().st_mode) != mode:
            raise ValueError('Existing target has different mode: ' + target['path'])
        return 'already_exact'
    if len(raw) != target['size'] or digest(raw) != target['sha256']:
        raise ValueError('Refusing invalid raw target payload')
    p.parent.mkdir(parents=True, exist_ok=True)
    confined(root, target['path'])
    fd, tmpname = tempfile.mkstemp(prefix='.' + p.name + '.', suffix='.materializing', dir=p.parent)
    tmp = Path(tmpname)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, mode)
        # An atomic hard-link publish refuses to overwrite even if another writer races us.
        os.link(tmp, p)
    finally:
        tmp.unlink(missing_ok=True)
    return 'restored'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository-root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--package-root', type=Path, help='Optional local preparation overlay; normally omit after cloning.')
    parser.add_argument('--verify-only', action='store_true', help='Read, decompress and hash every unique payload; verify every logical target binding. Write no targets.')
    args = parser.parse_args()
    manifest_path = Path(__file__).with_name('MANIFEST.json')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('format') not in ('haldane-exact-complete-transport-v1', 'haldane-exact-complete-transport-v2'):
        raise ValueError('Unsupported manifest format')
    reader = Reader(args.repository_root, args.package_root)
    bootstrap_counts = bootstrap_archives(manifest, reader, write=not args.verify_only)
    sources, targets = load_catalog(manifest, reader)
    for source in sources.values():
        reader.verify_payload(source)
    counts = {'restored': 0, 'already_exact': 0}
    if not args.verify_only:
        for target in targets:
            p = confined(reader.root, target['path'])
            if p.exists():
                outcome = write_exact(reader.root, target, b'')
            else:
                outcome = write_exact(reader.root, target, reader.payload(sources[target['sha256']]))
            counts[outcome] += 1
    print(json.dumps({'status': 'PASS', 'verify_only': args.verify_only,
                      'logical_targets': len(targets), 'logical_bytes': manifest['logical_target_bytes'],
                      'unique_payloads_verified': len(reader.checked_payloads),
                      'bootstrap_targets': len(manifest.get('bootstrap', {}).get('targets', [])),
                      'bootstrap_restored': bootstrap_counts['restored'], **counts}, sort_keys=True))


if __name__ == '__main__':
    main()
