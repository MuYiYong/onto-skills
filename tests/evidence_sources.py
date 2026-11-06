"""Read immutable historical source bytes without Git, network or extraction."""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile

BASE = Path(__file__).resolve().parent / 'compatibility/source-baselines'


def packages(baseline=BASE):
    manifest = json.loads((baseline / 'manifest.json').read_text())
    data = (baseline / manifest['archive']).read_bytes()
    if hashlib.sha256(data).hexdigest() != manifest['sha256']:
        raise ValueError('historical source archive digest mismatch')
    result = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        for member in archive.getmembers():
            path = PurePosixPath(member.name)
            if path.is_absolute() or '..' in path.parts or member.issym() or member.islnk():
                raise ValueError('unsafe historical source member')
            if member.isdir():
                continue
            if not member.isfile() or len(path.parts) < 4 or path.parts[0] != 'skills':
                raise ValueError('unexpected historical source member')
            files = result.setdefault(path.parts[2], {})
            relative = '/'.join(path.parts[3:])
            if relative in files:
                raise ValueError('duplicate historical source member')
            files[relative] = archive.extractfile(member).read()
    if (len(result) != manifest['package_count']
            or sum(map(len, result.values())) != manifest['file_count']):
        raise ValueError('historical source inventory mismatch')
    return result


def package_files(name):
    return {p: hashlib.sha256(data).hexdigest() for p, data in packages()[name].items()}


def package_digest(files):
    digest = hashlib.sha256()
    for relative, data in sorted(files.items()):
        digest.update(relative.encode())
        digest.update(b'\0')
        digest.update(data)
    return digest.hexdigest()
