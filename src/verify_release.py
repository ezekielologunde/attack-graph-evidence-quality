"""Check the manuscript release's exact-byte manifest, offline."""
import hashlib,json
from pathlib import Path

def main():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'paper/release-manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest['files'].items():
        path=(root/name).resolve()
        assert root==path or root in path.parents, name
        assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,name
    print('Verified',len(manifest['files']),'release files; hashes match.')

if __name__=='__main__':main()
