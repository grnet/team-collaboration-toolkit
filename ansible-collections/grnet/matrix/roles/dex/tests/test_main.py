"""Check the build destination when chdir and the inherited PWD differ."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from jinja2 import Template
import yaml


class BuildTests(unittest.TestCase):
    def test_build_installs_in_release_directory(self):
        role = Path(__file__).resolve().parents[1]
        tasks = yaml.safe_load((role / 'tasks/main.yml').read_text())
        task = next(task for task in tasks if task['name'] == 'Build the selected Dex release')
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / 'release'
            release.mkdir()
            # Dex's Makefile derives GOBIN from PWD; simulate go install's destination.
            (release / 'Makefile').write_text(
                'export GOBIN=$(PWD)/bin\n'
                'build:\n'
                '\tmkdir -p "$(GOBIN)"\n'
                '\ttouch "$(GOBIN)/dex"\n'
            )
            argv = [
                Template(arg).render(dex_version='2.46.0').replace('/opt/dex/2.46.0', str(release))
                for arg in task['ansible.builtin.command']['argv']
            ]
            subprocess.run(
                argv, cwd=release, env={**os.environ, 'PWD': tmp},
                check=True, capture_output=True, text=True,
            )
            self.assertTrue((release / 'bin/dex').exists())
