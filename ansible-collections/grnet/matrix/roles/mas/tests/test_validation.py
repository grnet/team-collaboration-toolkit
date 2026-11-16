"""Check the guard against disabling every authentication method."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


class ValidationTests(unittest.TestCase):
    def test_passwordless_settings(self):
        role = Path(__file__).resolve().parents[1]
        for providers, registration, success in [
            ([], False, False),
            ([{'id': 'dex'}], False, True),
            ([{'id': 'dex'}], True, False),
        ]:
            with self.subTest(providers=providers, registration=registration), tempfile.TemporaryDirectory() as tmp:
                settings = yaml.safe_load((role / 'defaults/main.yml').read_text())
                settings.update(
                    mas_version='1.26.0', mas_fqdn='auth.example.org',
                    synapse_server_name='example.org', mas_database_password='test',
                    mas_synapse_secret='x' * 64, ansible_facts={'architecture': 'x86_64'},
                    mas_passwords_enabled=False, mas_registration_requires_email=False,
                    mas_enable_registration=registration, mas_upstream_oauth2_providers=providers,
                )
                playbook = Path(tmp) / 'validate.yml'
                playbook.write_text(yaml.safe_dump([{
                    'hosts': 'localhost', 'gather_facts': False, 'vars': settings,
                    'tasks': [{'ansible.builtin.import_tasks': str(role / 'tasks/validate.yml')}],
                }]))
                result = subprocess.run(
                    ['ansible-playbook', '-i', 'localhost,', '-c', 'local', str(playbook)],
                    env={**os.environ, 'ANSIBLE_LOCAL_TEMP': tmp}, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
