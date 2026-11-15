=======
synapse
=======

``grnet.matrix.synapse`` installs a selected version of ``matrix-synapse[postgres]``
from PyPI in ``/opt/synapse/venv`` and configures a local PostgreSQL database.
The selected Synapse version must support the distribution's Python and
PostgreSQL versions.

The venv is created with ``--system-site-packages``. Dependencies including
Twisted, cryptography, Pillow and psycopg2 are installed from the distribution
repositories (Ubuntu requires Universe). Pip reuses them when their versions
satisfy Synapse's requirements and installs missing or newer dependencies
inside the venv otherwise. System packages are not modified by pip. Platforms
without compatible PyPI wheels may need additional compiler/build dependencies.

The playbook must explicitly run ``aptiko.general.postgresql`` before this role.
That role also installs PostGIS and requires the
``en_US.UTF-8`` locale to exist. It expects ``postgres_password`` and a
configured ``aptiko.general.duply`` installation; set
``duply_deactivate: true`` if backups are managed separately.

The playbook must explicitly run ``aptiko.general.webserver`` before this role
to install the shared Apache or nginx web server.

Synapse listens on localhost port 8008 with registration disabled by default. The role
configures a reverse proxy through ``aptiko.general.website``,
forwarding ``/_matrix`` and ``/_synapse/client``
with the required headers and preserving encoded request paths. The admin API
is not proxied. HTTPS uses Let's Encrypt by default; DNS must point to the
server and ports 80 and 443 must be reachable for certificate issuance.

Federation discovery must direct other servers to ``synapse_fqdn:443`` (for
example, through ``https://<synapse_server_name>/.well-known/matrix/server``).
The role does not listen on the default federation port 8448 or configure
discovery on the server-name domain. Client discovery on that domain must
also be configured separately when needed.

The role manages ``/etc/opt/synapse/homeserver.yaml`` and the ``matrix-synapse``
systemd service, which runs as the ``matrix-synapse`` user. Logs go to the
systemd journal. The signing key is generated on first start and preserved
in ``/var/opt/synapse/homeserver.signing.key``; media is stored in
``/var/opt/synapse/media_store``.

Example
=======

With the passwords defined in vaulted inventory variables::

  - hosts: matrix
    become: true
    vars:
      synapse_version: "1.159.0"
      synapse_server_name: example.org
      synapse_fqdn: matrix.example.org
      webserver_type: nginx
      website_letsencrypt_admin: admin@example.org
      duply_deactivate: true
    roles:
      - aptiko.general.postgresql
      - aptiko.general.webserver
      - grnet.matrix.synapse

Parameters
==========

.. data:: synapse_version

   Required, with no default. A quoted PyPI version or version specifier, for
   example ``"1.159.0"``, ``"==1.159.0"`` or ``">=1.159,<1.160"``. Pip validates
   the specifier and selects a matching release. An already installed version
   satisfying the constraint is kept; rerunning the role does not automatically
   upgrade to the newest matching release. Change the constraint to require
   another version and rerun the role to install it and restart Synapse.
   Normal APT upgrades do not upgrade Synapse,
   but can update its system-provided Python dependencies. Pip dependencies
   are not locked. Review Synapse's upgrade notes and back up before upgrading;
   selecting an older version does not undo database migrations.

.. data:: synapse_server_name

   Required. The domain in Matrix user IDs (``@user:example.org``). Choose
   before first installation; changing it on an existing server is unsupported.

.. data:: synapse_database_password

   Required. Password for the Synapse database user. Store in Ansible Vault.

.. data:: postgres_password

   Required by ``aptiko.general.postgresql``. Password for the PostgreSQL
   administrator; store in Ansible Vault.

.. data:: synapse_public_baseurl

   Public URL. Defaults to ``https://{{ synapse_fqdn }}/`` (HTTP when
   ``synapse_ssl`` is ``"off"``).

.. data:: synapse_fqdn

   Public reverse proxy hostname. Defaults to ``synapse_server_name``.

.. data:: synapse_ssl

   TLS mode passed to ``aptiko.general.website``. Default ``"letsencrypt"``;
   also accepts ``"self-signed"``, ``"custom"`` and ``"off"``. Custom TLS
   requires ``website_cert`` and ``website_private_key`` as defined by that role.

.. data:: webserver_type

   Required. Set to ``"nginx"`` or ``"apache"``. This selects the shared
   web server for the host, as in ``aptiko.general.webserver``.

.. data:: website_letsencrypt_admin

   Required for the default Let's Encrypt mode. Email address used for
   certificate registration.

.. data:: synapse_report_stats

   Whether to report usage statistics to Synapse developers. Default ``false``.

.. data:: synapse_enable_registration

   Whether to allow public account registration. Default ``false``. Set
   ``synapse_enable_registration: true`` in inventory and rerun the role to
   enable sign-ups. Unless ``synapse_registration_requires_email`` is enabled,
   registration requires no verification, increasing the risk of spam and abuse.
   Set it back to ``false`` to disable new sign-ups; existing accounts are
   unaffected.

.. data:: synapse_registration_requires_email

   Require new users to verify ownership of an email address during registration.
   Default ``false``. Requires ``synapse_email`` to be configured. Public
   registration still requires ``synapse_enable_registration: true``. Existing
   accounts are not required to verify an email address retroactively.

.. data:: synapse_email

   Mapping passed to Synapse's ``email`` configuration. Default ``{}`` (email
   sending is not configured). Set ``notif_from`` to the sender address and
   configure an SMTP server. SMTP defaults to localhost port 25 without
   authentication; the role does not install a mail server. See the
   `Synapse email settings <https://element-hq.github.io/synapse/latest/usage/configuration/config_documentation.html#email>`_
   for all supported keys.

   For example, to enable registration with email verification through an
   authenticated SMTP server using STARTTLS::

      synapse_enable_registration: true
      synapse_registration_requires_email: true
      synapse_email:
        smtp_host: smtp.example.org
        smtp_port: 587
        smtp_user: matrix@example.org
        smtp_pass: "{{ vault_synapse_smtp_password }}"
        require_transport_security: true
        notif_from: "Matrix <matrix@example.org>"

   Store the SMTP password in Ansible Vault. For implicit TLS (usually port
   465), set ``force_tls: true`` instead of ``require_transport_security``.

.. data:: synapse_database_name
   synapse_database_user

   Both default to ``synapse``. The database uses UTF-8 encoding and ``C``
   collation, as required by Synapse.
