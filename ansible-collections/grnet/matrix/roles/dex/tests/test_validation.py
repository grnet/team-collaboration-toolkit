"""Run with python -m unittest discover -s roles/dex/tests from the collection."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


class ValidationTests(unittest.TestCase):
    def test_settings(self):
        role = Path(__file__).resolve().parents[1]
        ldap = {
            'host': 'ldap.example.org:636',
            'bindDN': 'cn=reader,dc=example,dc=org', 'bindPW': 'literal$PASSWORD',
            'userSearch': {
                'baseDN': 'ou=People,dc=example,dc=org', 'username': 'uid',
                'idAttr': 'entryUUID', 'emailAttr': 'mail', 'nameAttr': 'cn',
            },
        }
        client = {'id': 'mas', 'secret': 'x' * 64,
                  'redirectURIs': ['https://auth.example.org/upstream/callback/01H8PKNWKKRPCBW4YGH1RWV279']}
        cases = [
            ({}, True),
            ({'dex_version': '../../bad'}, False),
            ({'dex_fqdn': 'AUTH.example.org.'}, False),
            ({'dex_fqdn': 'sso.example.org/path'}, False),
            ({'dex_database_name': 'mas'}, False),
            ({'dex_database_user': 'synapse'}, False),
            ({'dex_database_password': ''}, False),
            ({'dex_ldap': {**ldap, 'insecureNoSSL': True}}, False),
            ({'dex_ldap': {**ldap, 'insecureSkipVerify': True}}, False),
            ({'dex_ldap': {**ldap, 'startTLS': True}}, True),
            ({'dex_ldap': {**ldap, 'bindPW': ''}}, False),
            ({'dex_ldap': {**ldap, 'userSearch': {}}}, False),
            ({'dex_static_clients': []}, False),
            ({'dex_static_clients': [{**client, 'secret': 'short'}]}, False),
            ({'dex_static_clients': [{**client, 'public': True}]}, False),
            ({'dex_static_clients': [{**client, 'redirectURIs': ['https://auth.example.org/*']}]}, False),
            ({'dex_static_clients': [client, client]}, False),
        ]
        for overrides, success in cases:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as tmp:
                settings = yaml.safe_load((role / 'defaults/main.yml').read_text())
                settings.update(
                    dex_version='2.46.0', dex_fqdn='sso.example.org', mas_fqdn='auth.example.org',
                    dex_database_password='test', dex_ldap=ldap, dex_static_clients=[client],
                )
                settings.update(overrides)
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
