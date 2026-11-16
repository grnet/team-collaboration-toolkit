# grnet.matrix

The `grnet.matrix.synapse` role installs an explicitly selected Synapse version
with pip in `/opt/synapse/venv`, reusing distribution Python packages through
`--system-site-packages`. It configures a local PostgreSQL database.
The `synapse_version` parameter is required and accepts an exact version or a
range such as `">=1.159,<1.160"`.  The playbook must explicitly run
`aptiko.general.postgresql` and `aptiko.general.webserver` before this role.
The role configures an Apache or nginx reverse proxy using
`aptiko.general.website`, with Let's Encrypt TLS by default.

See the [role documentation](https://team-collaboration-toolkit.readthedocs.io/en/latest/matrix/synapse.html)
for prerequisites, variables and an example playbook.

The `grnet.matrix.element` role installs an explicitly selected prebuilt Element
Web release and configures its default homeserver. It includes
`aptiko.general.website` as a dependency; the playbook must run
`aptiko.general.webserver` explicitly beforehand. Element must use a different
hostname from the homeserver, even on the same machine.

See the [Element role documentation](https://team-collaboration-toolkit.readthedocs.io/en/latest/matrix/element.html)
for parameters and a combined Synapse and Element playbook.

The `grnet.matrix.mas` role installs a selected Matrix Authentication Service
release with a separate PostgreSQL database and Apache/nginx reverse proxy.
See the [MAS role documentation](https://team-collaboration-toolkit.readthedocs.io/en/latest/matrix/mas.html)
for setup, secrets, registration and existing-server migration requirements.
