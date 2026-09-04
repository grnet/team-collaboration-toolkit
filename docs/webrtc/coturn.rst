.. _coturn:

===================
grnet.webrtc.coturn
===================

Overview
========

Installs and configures a STUN and TURN server.

The ``grnet.webrtc.coturn`` role installs a STUN and TURN server with
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
      - aptiko.general.base
      - role: grnet.webrtc.coturn
        coturn_fqdn: coturn.example.com
        coturn_static_auth_secret: topsecret0123456789
        coturn_letsencrypt_admin: admin@example.com

Parameters
==========

.. data:: coturn_fqdn

   The FQDN of the server, such as ``coturn.example.com``.

.. data:: coturn_static_auth_secret

   A secret shared between the TURN server and its clients. Use the same
   value in the Nextcloud Talk TURN settings and/or as Jitsi's Prosody
   external service secret.

.. data:: coturn_realm

   The TURN authentication realm. It defaults to ``coturn_fqdn`` and can
   be overridden when clients require a specific realm.

.. data:: coturn_setup_firewall
   
   If this and ``base_setup_firewall`` are both true, ports 3478, 3479,
   5349, and 5350, the UDP relay port range, and, when
   ``coturn_use_http_ports`` is true, ports 80 and 443 will be allowed in
   the firewall (see aptiko.general.base_); otherwise, the firewall will
   be untouched.

.. data:: coturn_setup_letsencrypt

   If ``true`` (the default), a Let's Encrypt certificate will be
   automatically obtained and installed for the coturn server.  The
   certificate will be renewed automatically by certbot, and the coturn
   service will be restarted after each renewal. If another role has
   already obtained a certificate for ``coturn_fqdn``, coturn will reuse
   it without running certbot in standalone mode.

.. data:: coturn_letsencrypt_admin

   The email address of the administrator for Let's Encrypt
   notifications.  This is only used when ``coturn_setup_letsencrypt`` is
   ``true``, in which case it is required.

.. data:: coturn_use_http_ports

   If ``true`` (the default), coturn will also listen on the
   firewall-friendly ports 80 and 443. Set this to ``false`` when
   another service, such as a web server, must bind these ports on the
   coturn host.

.. data:: coturn_min_port

   The lower bound of the UDP relay port range. Defaults to 49152.

.. data:: coturn_max_port

   The upper bound of the UDP relay port range. Defaults to 65535.

.. _aptiko.general.base: https://aptikogeneral.readthedocs.io/en/latest/base.html
