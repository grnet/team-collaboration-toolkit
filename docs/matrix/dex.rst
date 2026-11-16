===
dex
===

``grnet.matrix.dex`` installs Dex as an LDAP-to-OIDC bridge for :doc:`mas`.
Dex authenticates against LDAP; MAS uses the resulting OIDC identity to
authenticate Matrix users. The roles are connected by matching client
settings in inventory.

The role builds the selected source release in ``/opt/dex/<version>`` using
the upstream ``make build`` target. It installs the distribution's Go and C
build tools. The distribution must provide Go 1.21 or later (for example,
Ubuntu 24.04 or Debian 13). Go downloads the toolchain required by the
selected release and its dependencies; outbound access to GitHub and the
Go module proxy/checksum service is required. Builds are reused on subsequent
runs. Version 2.46.0 is the tested release.

The ``dex`` systemd service runs as a dedicated unprivileged user, listening
on ``127.0.0.1:5556``. Apache or nginx exposes it at its own hostname.
Configuration is stored in ``/etc/opt/dex/config.yaml``, readable only by
root and the service group. PostgreSQL stores Dex's persistent state,
including signing keys; Dex runs database migrations on startup.
Logs go to the systemd journal.

LDAP with MAS
=============

Configure DNS for the three hostnames and allow ports 80/443 for HTTPS.
Supply database passwords, ``mas_synapse_secret``, ``dex_mas_client_secret``
and ``dex_ldap_bind_password`` through Ansible Vault. Generate independent
random secrets with ``openssl rand -hex 32``. The Dex client secret is
separate from the MAS/Synapse shared secret.

Example for a new installation using OpenLDAP::

  - hosts: matrix
    become: true
    vars:
      webserver_type: nginx
      website_letsencrypt_admin: admin@example.org
      duply_deactivate: true
      synapse_version: "1.159.0"
      synapse_server_name: example.org
      synapse_fqdn: matrix.example.org
      synapse_mas_enabled: true
      mas_version: "1.26.0"
      mas_fqdn: auth.example.org
      mas_passwords_enabled: false
      dex_version: "2.46.0"
      dex_fqdn: sso.example.org

      # Choose once and keep stable: this is the MAS provider's ULID.
      dex_mas_provider_id: 01H8PKNWKKRPCBW4YGH1RWV279
      dex_static_clients:
        - id: mas
          name: Matrix Authentication Service
          secret: "{{ dex_mas_client_secret }}"
          redirectURIs:
            - "https://{{ mas_fqdn }}/upstream/callback/{{ dex_mas_provider_id }}"

      dex_ldap:
        host: ldap.example.org:636
        bindDN: cn=reader,dc=example,dc=org
        bindPW: "{{ dex_ldap_bind_password }}"
        userSearch:
          baseDN: ou=People,dc=example,dc=org
          filter: "(objectClass=inetOrgPerson)"
          username: uid
          idAttr: entryUUID
          emailAttr: mail
          nameAttr: cn
          preferredUsernameAttr: uid

      mas_upstream_oauth2_providers:
        - id: "{{ dex_mas_provider_id }}"
          human_name: Organisation account
          issuer: "https://{{ dex_fqdn }}"
          client_id: mas
          client_secret: "{{ dex_mas_client_secret }}"
          token_endpoint_auth_method: client_secret_basic
          scope: "openid profile email"
          claims_imports:
            localpart:
              action: require
              template: !unsafe "{{ user.preferred_username }}"
            displayname:
              action: suggest
              template: !unsafe "{{ user.name }}"
            email:
              action: suggest
              template: !unsafe "{{ user.email }}"
    roles:
      - aptiko.general.postgresql
      - aptiko.general.webserver
      - grnet.matrix.dex
      - grnet.matrix.mas
      - grnet.matrix.synapse

Adapt the search base, filter and attributes to the actual directory.
``entryUUID`` is an OpenLDAP example: select an immutable, unique identity
attribute supported by your directory. The preferred username must be a
valid Matrix localpart. Do not automatically link existing accounts by an
email address or username; plan existing-account migration separately.
Keep Dex's issuer, connector ID (``ldap``), LDAP identity mapping and the MAS
provider ID stable after users start logging in.

With ``mas_passwords_enabled: false``, users authenticate through Dex's
browser login page. Keep ``mas_enable_registration: false``; it controls
local password registration, not first-time provisioning through an upstream
provider. Use the LDAP search filter to restrict which directory users can
authenticate. LDAP password changes and account removal do not by themselves
revoke existing MAS sessions.

Parameters
==========

.. data:: dex_version

   Required quoted source release number without ``v``. No automatic updates.
   Changing it builds a separate release and restarts Dex. Earlier releases
   and build caches remain on disk. Downgrading does not undo database
   migrations; back up the database and configuration before upgrading.

.. data:: dex_fqdn

   Required hostname, separate from MAS, Synapse and Element. The issuer is
   ``https://<dex_fqdn>`` with no trailing slash.

.. data:: dex_ssl

   Defaults to ``letsencrypt`` and is passed to ``aptiko.general.website``.
   ``off`` is for isolated local testing only; client callbacks still require
   HTTPS. Browser login requires access to both Dex and MAS hostnames.

.. data:: dex_database_name
            dex_database_user
            dex_database_password

   Database and user default to ``dex``; the password is required. Both must
   differ from the MAS and Synapse database names/users. Run
   ``aptiko.general.postgresql`` first, as described in :doc:`synapse`.
   Connections use TCP on localhost; PostgreSQL must allow password
   authentication for this user. Back up the Dex database with the inventory
   secrets and configuration.

.. data:: dex_ldap

   Required mapping passed to Dex's LDAP connector using its native fields.
   Verified LDAPS is the default. Set ``startTLS: true`` for StartTLS, usually
   on port 389. Unencrypted LDAP and disabled certificate verification are
   rejected. For a private CA, provide ``rootCAData`` containing the
   base64-encoded PEM CA certificate, or ``rootCA`` pointing to an existing
   CA file readable by the service. The role does not install an LDAP server.

   Provide both ``bindDN`` and ``bindPW``, or omit both for anonymous searches.
   Give the bind account only the directory read access it needs. Configuration
   environment expansion is disabled so literal dollar signs in passwords
   are preserved. See the upstream `LDAP connector reference
   <https://dexidp.io/docs/connectors/ldap/>`_ for search and attribute options.

.. data:: dex_static_clients

   Required nonempty list using Dex's native static client format. Each
   confidential client needs a unique ``id``, a random ``secret`` of at least
   32 characters and exact HTTPS ``redirectURIs`` without wildcards. For MAS,
   use ``https://<mas_fqdn>/upstream/callback/<provider-id>``. Keep the client
   ID, secret and callback provider ID consistent with the MAS configuration.

Verification
============

From the repository root, run the local validation tests::

  ANSIBLE_LOCAL_TEMP=/tmp/ansible python -m unittest discover -s ansible-collections/grnet/matrix/roles/dex/tests
  ANSIBLE_LOCAL_TEMP=/tmp/ansible python -m unittest discover -s ansible-collections/grnet/matrix/roles/mas/tests

After deployment, run ``roles/dex/tests/smoke.yml`` with the normal inventory
variables to check public OIDC discovery. Then log in with Element through
MAS and Dex using a test directory account; confirm its Matrix ID, display
name and email. Repeat with an incorrect LDAP password and confirm rejection.
