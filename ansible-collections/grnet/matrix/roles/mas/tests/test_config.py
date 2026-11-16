"""Render MAS configuration without installing services."""

import base64
from pathlib import Path
import unittest

from ansible.plugins.filter.core import FilterModule
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml


class ConfigTests(unittest.TestCase):
    def test_disable_password_login(self):
        role = Path(__file__).resolve().parents[1]
        env = Environment(loader=FileSystemLoader(role / 'templates'), undefined=StrictUndefined)
        env.filters.update(FilterModule().filters())
        settings = yaml.safe_load((role / 'defaults/main.yml').read_text())
        settings.update(
            ansible_managed='test', mas_version='1.26.0', mas_fqdn='auth.example.org',
            synapse_server_name='example.org', mas_database_password='test',
            mas_synapse_secret='test', mas_passwords_enabled=False,
            mas_generated_config={'content': base64.b64encode(b'secrets: {}').decode()},
        )
        config = yaml.safe_load(env.get_template('config.yaml.j2').render(settings))
        self.assertEqual(config.get('passwords'), {'enabled': False})
