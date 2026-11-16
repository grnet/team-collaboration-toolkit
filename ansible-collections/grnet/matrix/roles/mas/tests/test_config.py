"""Render MAS configuration without installing services."""

import base64
from pathlib import Path
import unittest

from ansible.plugins.filter.core import FilterModule
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml


class ConfigTests(unittest.TestCase):
    def render(self, **overrides):
        role = Path(__file__).resolve().parents[1]
        env = Environment(loader=FileSystemLoader(role / 'templates'), undefined=StrictUndefined)
        env.filters.update(FilterModule().filters())
        settings = yaml.safe_load((role / 'defaults/main.yml').read_text())
        settings.update(
            ansible_managed='test', mas_version='1.26.0', mas_fqdn='auth.example.org',
            synapse_server_name='example.org', mas_database_password='test',
            mas_synapse_secret='test',
            mas_generated_config={'content': base64.b64encode(b'secrets: {}').decode()},
        )
        settings.update(overrides)
        return yaml.safe_load(env.get_template('config.yaml.j2').render(settings))

    def resources(self, config):
        return [r['name'] for r in config['http']['listeners'][0]['resources']]

    def test_disable_password_login(self):
        config = self.render(mas_passwords_enabled=False)
        self.assertEqual(config.get('passwords'), {'enabled': False})

    def test_admin_api_not_exposed_by_default(self):
        self.assertNotIn('adminapi', self.resources(self.render()))

    def test_expose_admin_api(self):
        self.assertIn('adminapi', self.resources(self.render(mas_expose_admin_api=True)))
