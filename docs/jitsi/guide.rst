===========
Jitsi guide
===========

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
and the ``jitsi_jvb`` role to the servers in the ``jitsi_jvb`` group.

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
    jitsi_jvb_secret: topsecret4
    jitsi_prosody_external_service_secret: topsecret5

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
