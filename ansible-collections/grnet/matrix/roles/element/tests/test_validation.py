"""Run with python -m unittest discover -s roles/element/tests from the collection."""

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
            ({"element_fqdn": "matrix.example.org"}, False),
            ({"element_fqdn": "MATRIX.example.org."}, False),
            ({"element_homeserver_url": "https://chat.example.org:8448/matrix"}, False),
            ({"synapse_fqdn": "CHAT.example.org."}, False),
            ({"element_homeserver_url": "matrix.example.org"}, False),
            ({"element_version": "../../bad"}, False),
            ({"element_fqdn": "chat.example.org/extra"}, False),
        ]
        for overrides, success in cases:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as tmp:
                settings = {
                    "element_version": "1.11.100",
                    "element_fqdn": "chat.example.org",
                    "element_homeserver_url": "https://matrix.example.org/",
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
