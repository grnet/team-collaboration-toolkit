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

.. _jitsi_recording:

Recording conferences
=====================

There are two ways to record conferences; at the server and at the
client. Client recording works at the browser; the user's browser
records the conference and stores the recording locally at the user. At
the time of this writing, local recording is marked "Beta" and works
only on some browsers (e.g. Google Chrome; it doesn't work on Firefox).
To share the recording, the user must upload it somewhere where the
users can download it.

To enable client recording, specify this::

    jitsi_local_recording_config: "disable: false"

See localRecording_ in the Jitsi documentation for more options. For
example, you can specify this::

    jitsi_local_recording_config: "disable: false, notifyAllParticipants: true"

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

.. _localRecording: https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-configuration/#localrecording

.. _jitsi_statistics:

Getting statistics about Jitsi usage
====================================

Company administrators often want to see some statistics about what
conferences happened and what the attendance was. We have a Prometheus
exporter that can provide this information to a Prometheus server. The
exporter is installed if prometheus_server_ips_ has a value.

To enable the exporter, follow these steps:

 * Ensure prometheus_server_ips_ has a valid value.
 * Optionally set :ref:`jitsi_prometheus_exporter_port
   <jitsi_reference>`; the default is 9102.
 * Add an appropriate item to prometheus_scrape_configs_; for example::

    prometheus_scrape_configs:
      - job_name: jitsi
        static_configs:
          - targets:
              - jitsi.example.com:{{ jitsi_prometheus_exporter_port }}

To create a graph of the data in a Grafana dashboard:

 * Go to the dashboard and select Add, Visualization.
 * In the right panel, visualization, select "Time series", and in the
   Panel options below it, specify a title such as "Jitsi conference
   participants".
 * In the bottom panel, in the query builder, select Code (instead of
   "Builder) and type the PromQL query ``label_replace(jitsi_room_participants, "room", "$1", "room", "(.*)@.*")``.
 * Switch to Builder Label filters select ``room !=
   __active_rooms_exist__``.
 * In the query builder, under Options, select Legend = ``{{room}}``.

.. _prometheus_server_ips: https://aptikogeneral.readthedocs.io/en/latest/prometheus.html#parameters
.. _prometheus_scrape_configs: https://aptikogeneral.readthedocs.io/en/latest/prometheus.html#parameters

.. _jitsi_whiteboard:

Whiteboard
==========

The ``grnet.jitsi.jitsi_meet`` role automatically enables the
whiteboard. It installs the necessary excalidraw backend on the Jitsi
meet server and makes nginx proxy related requests to it. The port on
which the backend is listening can be configured with the
``jitsi_excalidraw_backend_port`` variable. The backend is also
providing data for prometheus on the port specified by
``jitsi_excalidraw_backend_prometheus_port``, but this is currently not
used anywhere. You normally don't need to specify these two variables,
their default values will work.
