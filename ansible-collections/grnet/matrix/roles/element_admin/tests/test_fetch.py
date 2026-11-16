"""Check which image layer entries fetch_element_admin.py extracts."""

import io
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "files"))
import fetch_element_admin  # noqa: E402


def add(tar, name, data=b"", **attrs):
    info = tarfile.TarInfo(name)
    info.size = len(data)
    for key, value in attrs.items():
        setattr(info, key, value)
    tar.addfile(info, io.BytesIO(data))


class ExtractTests(unittest.TestCase):
    def extract(self, *entries):
        tmp = Path(self.enterContext(tempfile.TemporaryDirectory()))
        layer, dest = tmp / "layer.tar.gz", tmp / "dest"
        with tarfile.open(layer, "w:gz") as tar:
            for name, data, attrs in entries:
                add(tar, name, data, **attrs)
        return fetch_element_admin.extract_dist(layer, dest), dest

    def test_extracts_only_regular_files_under_dist(self):
        entry_point, dest = self.extract(
            ("dist/assets/app.js", b"js", {"uid": 101}),
            ("dist/index.html", b"entry", {}),
            ("dist/index.runtime.html", b"",
             {"type": tarfile.SYMTYPE, "linkname": "/tmp/index.runtime.html"}),
            ("etc/nginx/nginx.conf", b"conf", {}),
        )
        self.assertEqual(entry_point, b"entry")
        self.assertEqual((dest / "assets/app.js").read_bytes(), b"js")
        # main() writes the entry point only after all layers are extracted.
        self.assertEqual([p.name for p in dest.iterdir()], ["assets"])

    def test_rejects_paths_outside_dest(self):
        with self.assertRaises(tarfile.OutsideDestinationError):
            self.extract(("dist/../escape", b"bad", {}))
