=============
element_admin
=============

``grnet.matrix.element_admin`` installs a selected release of `Element Admin
<https://github.com/element-hq/element-admin>`_, Element's web
administration console for Synapse with :doc:`mas`. It manages users and
sessions through MAS's admin API, and rooms, media and the server through
Synapse's admin API.

Upstream publishes Element Admin only as a container image. The role does
not need Docker: it downloads the image layers from ``oci.element.io``,
verifies their digests and extracts only the static application files into
``/var/www/<element_admin_fqdn>/element-admin-<version>``, served by Apache
or nginx through ``aptiko.general.website``. Run
``aptiko.general.webserver`` explicitly before this role.

The role could instead build Element Admin from source, but that needs
recent Node.js and pnpm versions that Debian does not package, downloads
many npm packages for every new version, and runs a slow, memory-hungry
build on the server. The image already contains exactly the files Element
built and released, and a registry is only HTTPS and tarballs, so
extracting them is simpler and has fewer dependencies. The digests are
checked against the image manifest that the registry serves; the release
is not pinned to a fixed checksum.

Element Admin must be served over HTTPS from its own hostname, different
from those of Synapse, MAS and Element Web, even on the same server.

Requirements
============

* Element Admin runs in the administrator's browser, which calls both admin
  APIs directly. Set ``synapse_expose_admin_api: true`` (:doc:`synapse`) and
  ``mas_expose_admin_api: true`` (:doc:`mas`). Both default to ``false``.
* The browser finds the homeserver through client discovery,
  ``https://<server name>/.well-known/matrix/client``. The synapse role
  serves it when the server name is the Synapse hostname; otherwise see
  :doc:`synapse`.
* Element Admin registers itself as a MAS client on first login. Log in with
  a MAS account that is allowed to request administrator access::

    /opt/mas/<version>/mas-cli manage promote-admin --config /etc/opt/mas/config.yaml <username>

  Only such accounts can obtain tokens for the admin APIs; exposing the
  APIs does not grant access to anyone else.

Example
=======

Together with the settings of :doc:`synapse` and :doc:`mas`::

  - hosts: matrix
    become: true
    vars:
      synapse_server_name: example.org
      synapse_fqdn: matrix.example.org
      synapse_expose_admin_api: true
      mas_fqdn: auth.example.org
      mas_expose_admin_api: true
      element_admin_version: "0.1.18"
      element_admin_fqdn: admin.example.org
      element_admin_server_name: "{{ synapse_server_name }}"
      # ... other Synapse and MAS settings
    roles:
      - aptiko.general.postgresql
      - aptiko.general.webserver
      - grnet.matrix.mas
      - grnet.matrix.synapse
      - grnet.matrix.element_admin

Version numbers above are examples, not recommendations.

Parameters
==========

.. data:: element_admin_version

   Required. Quoted release version without ``v``, for example ``"0.1.18"``;
   it must exist as an image tag on ``oci.element.io/element-admin``. Change it
   and rerun the role to switch releases; old release directories are retained.

.. data:: element_admin_fqdn

   Required. Hostname for the console, for example ``admin.example.org``.

.. data:: element_admin_server_name

   Required. The Matrix server name, normally ``synapse_server_name``. The
   console uses it to discover the homeserver.

.. data:: element_admin_ssl

   TLS mode passed to ``aptiko.general.website``. Default ``"letsencrypt"``;
   also accepts ``"self-signed"`` and ``"custom"``. ``"off"`` is rejected
   because Element Admin needs a secure context. Custom TLS requires
   ``website_cert`` and ``website_private_key``.
