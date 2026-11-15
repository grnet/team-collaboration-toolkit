=======
element
=======

``grnet.matrix.element`` installs a selected prebuilt Element Web release from
GitHub. It serves static files through ``aptiko.general.website`` and needs no
database or application service. Run ``aptiko.general.webserver`` explicitly
before this role.

Element must have a different hostname from its homeserver, even when both
share a machine and IP address.  See `Element's security guidance
<https://web-docs.element.dev/readme-element-web.html#separate-domains>`_.

Example
=======

With Synapse and PostgreSQL passwords defined in vaulted inventory variables::

  - hosts: matrix
    become: true
    vars:
      webserver_type: nginx
      website_letsencrypt_admin: admin@example.org
      synapse_version: "1.159.0"
      synapse_server_name: example.org
      synapse_fqdn: matrix.example.org
      duply_deactivate: true
      element_version: "1.11.100"
      element_fqdn: chat.example.org
      element_homeserver_url: "{{ synapse_public_baseurl }}"
    roles:
      - aptiko.general.postgresql
      - aptiko.general.webserver
      - grnet.matrix.synapse
      - grnet.matrix.element

Version numbers above are examples, not recommendations. Element can also run
without the Synapse role: supply the public URL of an existing homeserver.
Homeserver discovery and calling infrastructure are configured separately.

Parameters
==========

.. data:: element_version

   Required. Exact Element Web release version as a quoted string, without
   the ``v`` prefix. No default; normal APT upgrades do not upgrade Element.

.. data:: element_fqdn

   Required. Element's public hostname, for example ``chat.example.org``.

.. data:: element_homeserver_url

   Required. Public homeserver URL reachable by users' browsers, for example
   ``https://matrix.example.org/``. Must have a different hostname from Element.

.. data:: element_ssl

   TLS mode passed to ``aptiko.general.website``. Default ``"letsencrypt"``;
   also accepts ``"self-signed"``, ``"custom"`` and ``"off"``. Use HTTPS in
   production; browser encryption and calling features require a secure context.
   Custom TLS requires ``website_cert`` and ``website_private_key``.
