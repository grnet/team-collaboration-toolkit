===
mas
===

``grnet.matrix.mas`` installs an explicitly selected Matrix Authentication
Service (MAS) release from the upstream Linux binaries.  It runs alongside
Synapse on the same server, with a separate PostgreSQL database and its
own hostname. Run ``aptiko.general.postgresql`` and
``aptiko.general.webserver`` first, as described in :doc:`synapse`.

MAS listens on ``127.0.0.1:8080`` behind Apache or nginx. The role manages
``/etc/opt/mas/config.yaml`` and the ``matrix-authentication-service`` systemd
service. Releases, including frontend assets and policies, are installed in
``/opt/mas/<version>``. Logs go to the systemd journal. MAS applies its database
migrations and synchronizes configured providers when it starts.

New installation
================

Define ``postgres_password``, ``synapse_database_password``,
``mas_database_password`` and ``mas_synapse_secret`` in vaulted inventory
variables. Generate the shared secret with ``openssl rand -hex 32``.
Use Synapse 1.136.0 or later. For example::

  - hosts: matrix
    become: true
    vars:
      synapse_version: "1.159.0"
      synapse_server_name: example.org
      synapse_fqdn: matrix.example.org
      synapse_mas_enabled: true
      mas_version: "1.26.0"
      mas_fqdn: auth.example.org
      webserver_type: nginx
      website_letsencrypt_admin: admin@example.org
      duply_deactivate: true
    roles:
      - aptiko.general.postgresql
      - aptiko.general.webserver
      - grnet.matrix.mas
      - grnet.matrix.synapse

DNS for both hostnames must point to this server. Ports 80 and 443 must be
reachable for Let's Encrypt. Client and federation discovery on the
server-name domain remain the administrator's responsibility; see
:doc:`synapse`.

``synapse_mas_enabled`` enables delegation and routes login, logout and
refresh requests on the Synapse hostname to MAS. The same
``mas_synapse_secret`` is used by both services. Keep Synapse's
registration options disabled; MAS owns authentication and registration.
Synapse's email settings may still be used for message notifications.

Registration is closed by default. To enable password registration, set
``mas_enable_registration: true`` and configure delivery of verification
emails, for example::

  mas_email:
    from: '"Matrix" <auth@example.org>'
    transport: smtp
    mode: starttls
    hostname: smtp.example.org
    port: 587
    username: auth@example.org
    password: "{{ vault_smtp_password }}"

For a closed server, create accounts using ``mas-cli manage register-user``;
run ``/opt/mas/<version>/mas-cli manage register-user --help`` for that
release's options and pass ``--config /etc/opt/mas/config.yaml``.

Parameters
==========

.. data:: mas_version

   Required quoted release number without ``v``, for example ``"1.26.0"``.
   No default or automatic upgrades. Changing it installs and starts that
   release; older release directories are retained. Back up before upgrading:
   selecting an older binary does not reverse database migrations.

.. data:: mas_fqdn

   Required hostname, different from ``synapse_fqdn``.

.. data:: mas_ssl

   Website SSL setting, default ``letsencrypt``. ``off`` uses HTTP and is
   intended only for local testing.

.. data:: mas_database_name
          mas_database_user
          mas_database_password

   Database and user default to ``mas``; the password is required. Both the
   database and user must differ from Synapse's. PostgreSQL is local.

.. data:: mas_synapse_secret

   Required high-entropy secret shared with Synapse, at least 32 characters.
   Keep it in Ansible Vault. It authorizes administrative operations.

.. data:: mas_enable_registration
          mas_registration_requires_email

   Defaults: ``false`` and ``true``. Email-required registration needs a
   working ``mas_email`` transport. Set ``mas_registration_requires_email``
   to ``false`` only if registrations without email verification are intended.

.. data:: mas_email

   MAS email configuration mapping, default ``{}`` (no delivery).
   This is separate from ``synapse_email``. See the upstream
   `configuration reference
   <https://element-hq.github.io/matrix-authentication-service/reference/configuration.html#email>`_.

.. data:: mas_upstream_oauth2_providers

   List of upstream OIDC provider configurations, default ``[]``. Passed to
   MAS's ``upstream_oauth2.providers``; see the upstream
   `provider configuration
   <https://element-hq.github.io/matrix-authentication-service/reference/configuration.html#upstream_oauth2providers>`_.
   LDAP requires an OIDC bridge such as Dex, installed separately.
   Use Ansible's ``!unsafe`` tag on provider claim
   templates containing literal ``{{ ... }}`` so Ansible leaves them for MAS.
   Removing a provider from inventory does not delete its database entry;
   review MAS's ``config sync --prune`` procedure when removing providers.

Secrets and backups
===================

On first installation, MAS generates keys into
``/var/opt/mas/generated.yaml`` in a private service-owned directory. The
role reuses only the secrets from this file on subsequent runs, including
upgrades. The rendered configuration is root-owned and readable only by the
service group; secret-bearing tasks suppress Ansible output.

Back up the MAS database, ``/var/opt/mas/generated.yaml`` and the vaulted
inventory secrets together, as well as the Synapse data. Never delete or
regenerate the MAS encryption secret for an existing database: encrypted
information would become unreadable.

Existing installations
======================

Do not simply enable ``synapse_mas_enabled`` on an existing homeserver.
User and session migration requires downtime and the upstream
`migration procedure
<https://element-hq.github.io/matrix-authentication-service/setup/migration.html>`_.
This role does not run ``syn2mas``. It starts MAS automatically, so perform
and complete the migration separately before using this role to manage the
migrated service. Preserve the migrated configuration's ``secrets`` mapping
in ``/var/opt/mas/generated.yaml`` before the first role run.

Migrated password hashes and upstream identity mappings may need additional
MAS configuration beyond this role's fresh-install defaults. Review those
requirements before adopting the role for a migrated installation.
