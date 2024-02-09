Inventory
=========

Here is an example inventory for installing on a single server::

    [jitsi_meet]
    my-jitsi-meet-server

    [jitsi_jvb]
    my-jitsi-meet-server

The ``jitsi_meet`` group must contain only one server. That server must
also be listed in the ``jitsi_jvb`` group ; that is, the Jitsi Meet
server must also be a videobridge (this is an old limitation and it
shouldn't be difficult to fix, assuming it's still there).  Additional
videobridges can be added if desired.  The playbook (see below) will
assign the ``jitsi_meet`` role to the server in the ``jitsi_meet`` group
and the ``jitsi_jvb`` role to the servers in the ``jitsi_jvb`` groupl

Although in principle nginx, jitsi-meet, prosody and jicofo could reside
in different machines, the role ``jitsi_meet`` puts them all in a single
server.

Variables example
=================

You need to make certain that some variables are available to the
roles, e.g. by putting them in ``group_vars/all``. Obviously it's a good
idea to vault the passwords/secrets. Here is an example::

    jitsi_fqdn: jitsi.example.com
    jitsi_jicofo_password: topsecret1
    jitsi_jicofo_secret: topsecret2
    jitsi_jvb_user: myvideobridgeuser
    jitsi_jvb_password: topsecret3
    jitsi_jvb_muc_nickname: myvideobridge_muc_nick
    jitsi_prosody_external_service_secret: topsecret4

Playbook
========

Use a playbook similar to this::

    ---
    - name: Jitsi server
      hosts: jitsi_meet
      roles:
        - aptiko.general.common
        - aptiko.general.nginx
        - grnet.jitsi.jitsi_meet

    - name: Jitsi videobridge
      hosts: jitsi_jvb
      roles:
        - aptiko.general.common
        - aptiko.general.nginx
        - grnet.jitsi.jitsi_jvb

Jitsi architecture
==================

The **Jitsi videobridge**, also known as **jvb**, is the component that
does the most essential work: it hosts conferences. All users connect to
the videobridge; they send their video and audio stream to it, and
receive the video and audio streams of the other users from it. Clients
talk WebRTC to the videobridge on UDP port 10000 (this does not appear
to be configurable).

The videobridge also listens on a TCP port, typically 9090, that speaks
"Colibri", a protocol on top of HTTP/WebSocket. Clients receive extra
information from that connection, such as which users connected or
disconnected from the conference. This port is actually proxied through
nginx, so clients actually connect to nginx at 443, and URL
``/colibri-ws/[videobridge-id]/`` is proxied to the videobridge.

Although the most common case is for a Jitsi installation to use a
single videobridge, you can have many videobridges for better
performance if you have many conferences, and each videobridge can host
one or more conferences. (A given conference always uses a single
videobridge.)

**Jicofo**, misleadingly meaning "Jitsi conference focus", is the
component that orchestrates conferences. Users connect to jicofo and ask
to create or join a conference. Jicofo creates the conference on the
less loaded videobridge and directs users to it. All communication
between Jicofo and other components goes through prosody (more on that
below). Jicofo also listens on TCP port 8888, but this is only an API
for diagnostic information or so.

**Jitsi-meet** is the JavaScript client the user runs on the browser. It
is loaded through nginx when the user visits the jitsi web site.

**Prosody** is a XMPP signaling server that in this case works as a
publish/subscribe queue. Videobridges publish information about
themselves on prosody, and jicofo subscribes to prosody and gets that
information from there. In addition, jitsi meet connects to prosody (via
nginx) and communicates with jicofo through it. Prosody listens on TCP
ports 5222 (XMPP client), 5269 (XMPP server), and 5280 (XMPP BOSH). Most
components, such as Jicofo and videobridges, connect to 5222. Nginx
also proxies ``/http-bind`` and ``/xmpp-websocket`` to prosody's 5280.

**Jibri** is the Jitsi recording component, that records conferences. It
works by starting a headless chrome browser that joins the conference as
an invisible user.

For additional information on Jitsi, see:

- the `Architecture section in the Jitsi documentation`_.
- a video on `how to load balance jitsi meet`_, which is useful
  even if you don't intend to load-balance.
- `a related discussion`_ in the forum, notably the `RENATER
  document`_ and the `flow chart`_.
- `another related discussion`_ in the forum.

.. _architecture section in the Jitsi documentation: https://jitsi.github.io/handbook/docs/architecture/
.. _how to load balance jitsi meet: https://www.youtube.com/watch?v=LyGV4uW8km8
.. _a related discussion: https://community.jitsi.org/t/architecture-design-of-jicofo/14906/2
.. _renater document: https://conf-ng.jres.org/2015/document_revision_1830.html?download
.. _flow chart: https://go.gliffy.com/go/publish/image/7649541/L.png
.. _another related discussion: https://community.jitsi.org/t/jicofo-and-prosody-ports/119669/1

Variables and options
=====================

- ``jitsi_fqdn``: The domain where jitsi meet is listening.
- ``jitsi_jibri_fqdn``: The domain name of the jibri server (used for
  downloading recordings).
- ``jitsi_jicofo_password``, ``jitsi_jicofo_secret``: The Jicofo
  username is set as "focus", and the password is set to the value of
  ``jitsi_jicofo_password``.  It's not actually used anywhere (but has
  to be set). Likewise with the ``jitsi_jicofo_secret``.
- ``jitsi_jvb_user``, ``jitsi_jvb_password``: Username
  and password for the videobridge. The user is registered in prosody,
  and subsequently the videobridges connect to prosody as this user. The
  user is also apparently used for SIP, but this is currently not
  supported by this role.
- ``jitsi_jvb_muc_nickname``: (Used only by the
  ``jitsi_jvb`` role.) Any unique string that is the same for
  all videobridges will work here. Other than that, we don't know
  exactly what it is for. See the `Jitsi multi-user chat documentation`_
  for more information.
- ``jitsi_jibri_password``, ``jitsi_recorder_password``: The passwords
  of the prosody ``jibri`` and ``recorder`` users, which are used by
  Jibri (see below).
- ``jitsi_ldap_*``: See :ref:`ldap`.
- ``jitsi_prosody_external_service_secret``: The secret for external
  services (e.g. for TURN).

.. _jitsi multi-user chat documentation: https://github.com/jitsi/jitsi-videobridge/blob/master/doc/muc.md

.. _ldap:

External authentication with LDAP
=================================

By default, the Jitsi server works without authentication. LDAP
authentication is supported. To enable, set the ``jitsi_ldap_*``
parameters as needed; for example::

    jitsi_ldap_servers:
      - ldap://myldapserver.example.com
    jitsi_ldap_base: dc=example,dc=com
    jitsi_ldap_filter: uid=$user
    jitsi_ldap_mode: bind

Recording conferences
=====================

There are two ways to record conferences; at the server and at the
client. Client recording works at the browser; the user's browser
records the conference and stores the recording locally at the user. At
the time of this writing, local recording is marked "Beta" and works
only on some browsers (e.g. Google Chrome; it doesn't work on Firefox).
To share the recording, the user must upload it somewhere where the
users can download it. In addition, there is no warning for the other
users that the conference is being recorded.

Recording at the server works with a Jitsi component called "Jibri". 
It runs a headless browser at the server and participates in the
conference as an invisible person. It is quite heavy, because of the
video encoding, and therefore should be run on a different server. In
fact, in this collection this is a requirement. There is also the
constraint that only a single conference can be recorded at a given time
by a single Jibri server; to record two simultaneous conferences, two
Jibri servers are needed (this is a Jibri limitation, not an Ansible
collection limitation), but currently the Ansible collection supports
only one.

To enable Jibri, you need, first, to add this to the inventory::

    [jibri]
    my-jibri-server

Second, add these variables (obviously the passwords should be vaulted)::

    jitsi_jibri_fqdn: jibri.example.com
    jitsi_jibri_password: topsecret4
    jitsi_recorder_password: topsecret5

Third, add this to the playbook::

    - name: Jibri
      hosts: jibri
      roles:
        - grnet.jitsi.jibri

Jibri doesn't have a ready-made way for users to download conferences.
We have implemented the simplest possible way for that: We install nginx
on the Jibri server, and the recordings are at ``https://{{
jitsi_jibri_fqdn }}/{{ room_name }}``. Users must know the room name to
get the recordings.  A cron job removes recordings after 24 hours. (The
fact that we have a single ``jitsi_jibri_fqdn``, a variable only used by
nginx, is the only reason the role supports only a single jibri.)
