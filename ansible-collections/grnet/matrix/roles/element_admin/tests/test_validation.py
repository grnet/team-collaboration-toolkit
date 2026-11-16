"""Run with python -m unittest discover -s roles/element_admin/tests from the collection."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


class ValidationTests(unittest.TestCase):
    def test_settings(self):
        cases = [
            ({}, True),
            ({"element_admin_ssl": "self-signed"}, True),
            ({"element_admin_ssl": "off"}, False),
            ({"synapse_fqdn": "ADMIN.example.org."}, False),
            ({"mas_fqdn": "admin.example.org"}, False),
            ({"element_admin_version": "../../bad"}, False),
            ({"element_admin_version": "v0.1.18"}, False),
            ({"element_admin_fqdn": "admin.example.org/extra"}, False),
            ({"element_admin_server_name": 'example.org", "x": "'}, False),
        ]
        for overrides, success in cases:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as tmp:
                settings = {
                    "element_admin_version": "0.1.18",
                    "element_admin_fqdn": "admin.example.org",
                    "element_admin_server_name": "example.org",
                    "element_admin_ssl": "letsencrypt",
                    "synapse_fqdn": "matrix.example.org",
                    "mas_fqdn": "auth.example.org",
                }
                settings.update(overrides)
                playbook = Path(tmp) / "validate.yml"
                playbook.write_text(yaml.safe_dump([{
                    "hosts": "localhost",
                    "gather_facts": False,
                    "vars": settings,
                    "tasks": [{"ansible.builtin.import_tasks": str(
                        Path(__file__).resolve().parents[1] / "tasks/validate.yml"
                    )}],
                }]))
                result = subprocess.run(
                    ["ansible-playbook", "-i", "localhost,", "-c", "local", str(playbook)],
                    env={**os.environ, "ANSIBLE_LOCAL_TEMP": tmp},
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
