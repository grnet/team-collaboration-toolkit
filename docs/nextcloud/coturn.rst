.. _coturn:

======================
grnet.nextcloud.coturn
======================

Overview
========

Installs and configures a STUN and TURN server.

The ``grnet.nextcloud.coturn`` role installs a STUN and TURN server with
the widely used coturn software.  It listens on the default TURN ports
3478 and 5349, and also on the firewall-friendly ports 80 and 443. The
server supports both ``turn:`` and ``turns:`` URLs; coturn automatically
recognizes plain and TLS traffic on its listening endpoints. A single
port could actually suffice; as the
coturn manual says, "we keep both endpoints to satisfy the RFC 5766
specs." The server should probably be dedicated but small: 512 MB of RAM
suffice, and it doesn't use much CPU either, but it needs a good network
connection.

Example
=======

.. code-block:: yaml

  - name: Coturn server
    hosts: coturn
    roles:
      - aptiko.general.common
      - role: grnet.nextcloud.coturn
        coturn_fqdn: coturn.example.com
        coturn_static_auth_secret: topsecret0123456789
        nextcloud_fqdn: nextcloud.example.com
        letsencrypt_admin: admin@example.com

Parameters
==========

.. data:: coturn_fqdn

   The FQDN of the server, such as ``coturn.example.com``.

.. data:: coturn_static_auth_secret

   A secret shared between the Nextcloud Talk server and the TURN
   server; it allows Nextcloud users to logon to the TURN server. Except
   from here, it must also be specified in the Nextcloud settings, Talk,
   TURN servers.

.. data:: coturn_use_ferm
   
   If ``true`` (the default), ports 80, 443, 3478, 3479, 5349, and 5350
   will be allowed in ferm
   (see aptiko.general.common_); otherwise, the firewall will be
   untouched.

.. data:: nextcloud_fqdn
          letsencrypt
          letsencrypt_admin
   :noindex:

   These are also used in other roles; :data:`nextcloud_fqdn` in
   ``grnet.nextcloud.nextcloud``, and the other two in, for example,
   aptiko.general.nginx_site_.

.. _aptiko.general.common: https://aptikogeneral.readthedocs.io/en/latest/common.html
.. _aptiko.general.nginx_site: https://aptikogeneral.readthedocs.io/en/latest/nginx_site.html
