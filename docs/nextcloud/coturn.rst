.. _coturn:

======
coturn
======

Overview
========

Installs and configures a STUN and TURN server.

**What is STUN:** A computer that is behind a NAT does not know the IP
address with which it is known to the world. For some communication
stuff to work (such as video conferencing), the client needs to know
this information. A STUN server can help it learn it. Essentially you
communicate with a STUN server and ask "what is my IP address?", and it
replies. This is pretty much all. It commonly works with UDP in server
port 3478. It can also be used with TCP, but this is rarely done and
might not be standard.

**What is TURN:** Video conferencing works with UDP. A client exchanges
UDP packets with the video conferencing server on various ports (it can
also exchange packets directly with peers, especially when conferencing
with only two clients). But sometimes firewalls (on the client's side)
restrict this traffic. (On the server side there should be no firewall
problem—if an organization wants to install a video conferencing server
accessible from the Internet, presumably they can configure their
firewall for that.) A TURN server helps work around the problem by
listening on UDP and TCP port 443, which is, especially the TCP, very
unlikely to be blocked.  The client talks UDP, or, failing that, TCP to
the TURN server at port 443, and sends/receives all its data there, and
the TURN server relays this data to the video conferencing server.
Obviously this solution sucks (especially the TCP version) but it works
as a last resort when everything else fails.

The ``grnet.nextcloud.coturn`` role installs a STUN and TURN server with
the widely used coturn software, with should be deployed alongside
:ref:`talk`. It is listening on ports 3478 and 443.  Both ports can be
used for both unencrypted and encrypted communication, both UDP and TCP,
and both STUN and TURN. A single port could actually suffice; as the
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
   
   If ``true`` (the default), ports 3478 and 443 will be allowed in ferm
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
