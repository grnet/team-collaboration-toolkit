#!/usr/bin/env python3
"""Extract Element Admin's static files from its official container image.

Usage: fetch_element_admin.py VERSION DEST

Upstream publishes no release archive; the image's /dist directory is the
built application. Only regular files and directories under dist/ are
extracted, and every downloaded blob is checked against its digest.
"""

import hashlib
import json
import shutil
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

# shortcut: anonymous pulls only, no bearer-token flow; add one if the
# registry starts requiring it.
REGISTRY = "https://oci.element.io/v2/element-admin"
INDEX_TYPES = (
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
)
MANIFEST_TYPES = (
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
)


def get(path, accept=()):
    # The registry rejects urllib's default User-Agent.
    request = urllib.request.Request(f"{REGISTRY}/{path}", headers={"User-Agent": "fetch-element-admin"})
    if accept:
        request.add_header("Accept", ", ".join(accept))
    return urllib.request.urlopen(request, timeout=60)


def get_json(path, accept, digest=None):
    with get(path, accept) as response:
        data = response.read()
    if digest:
        check_digest(hashlib.sha256(data).hexdigest(), digest)
    return json.loads(data)


def check_digest(actual, expected):
    if f"sha256:{actual}" != expected:
        raise SystemExit(f"Digest mismatch: expected {expected}, got sha256:{actual}")


def layer_digests(version):
    manifest = get_json(f"manifests/{version}", INDEX_TYPES + MANIFEST_TYPES)
    if manifest.get("manifests"):
        # The static files are the same for every architecture.
        linux = [m for m in manifest["manifests"]
                 if m.get("platform", {}).get("os") == "linux"]
        digest = linux[0]["digest"]
        manifest = get_json(f"manifests/{digest}", MANIFEST_TYPES, digest)
    return [layer["digest"] for layer in manifest["layers"]]


def download(digest, target):
    sha256 = hashlib.sha256()
    with get(f"blobs/{digest}") as response, open(target, "wb") as f:
        while chunk := response.read(1 << 20):
            sha256.update(chunk)
            f.write(chunk)
    check_digest(sha256.hexdigest(), digest)


# shortcut: ignores OCI whiteouts (.wh.*), fine while dist/ comes from a
# single layer; handle them if a release deletes files in a later layer.
def extract_dist(layer, dest):
    """Extract dist/ from a layer into dest; return the entry point if present."""
    entry_point = None
    with tarfile.open(layer) as tar:
        for member in tar:
            if not member.name.startswith("dist/") or not (member.isfile() or member.isdir()):
                continue
            member.name = member.name.removeprefix("dist/")
            member.uid = member.gid = 0
            member.uname = member.gname = "root"
            if member.name == "index.html":
                entry_point = tar.extractfile(member).read()
                continue
            tar.extract(member, dest, filter="data")
    return entry_point


def main(version, dest):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    entry_point = None
    with tempfile.TemporaryDirectory() as tmp:
        layer = Path(tmp) / "layer"
        for digest in layer_digests(version):
            download(digest, layer)
            entry_point = extract_dist(layer, dest) or entry_point
    if entry_point is None:
        raise SystemExit("The image has no dist/index.html")
    # Written last: the role uses it to tell that extraction is complete.
    with tempfile.NamedTemporaryFile(dir=dest, delete=False) as f:
        f.write(entry_point)
    Path(f.name).chmod(0o644)
    shutil.move(f.name, dest / "index.html")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
