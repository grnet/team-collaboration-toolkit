.. _jitsi_reference:

=======================
Jitsi modules reference
=======================

Variables and options
=====================

- ``jitsi_fqdn``: The domain where jitsi meet is listening.
- ``jitsi_jibri_fqdn``: The domain name of the jibri server (used for
  downloading recordings).
- ``jitsi_local_recording_config``: A JS snippet with the Jitsi Meet
  configuration for ``localRecording``. The default is ``disable: true``.
  See :ref:`jitsi_recording` for more information.
- ``jitsi_jicofo_password``, ``jitsi_jicofo_secret``: The Jicofo
  username is set as "focus", and the password is set to the value of
  ``jitsi_jicofo_password``.  It's not actually used anywhere (but has
  to be set). Likewise with the ``jitsi_jicofo_secret``.
- ``jitsi_jvb_user``, ``jitsi_jvb_password``, ``jitsi_jvb_secret``:
  Username, password and secret for the videobridge. The user is
  registered in prosody, and subsequently the videobridges connect to
  prosody as this user. The user is also apparently used for SIP, but
  this is currently not supported by this role.
- ``jitsi_jibri_password``, ``jitsi_recorder_password``: The passwords
  of the prosody ``jibri`` and ``recorder`` users, which are used by
  Jibri (see :ref:`jitsi_recording`).
- ``jitsi_ldap_*``: See :ref:`ldap`.
- ``jitsi_prosody_external_service_secret``: The secret for external
  services (e.g. for TURN).
- ``jitsi_prometheus_exporter_port``: The port on which the prometheus
  exporter is listening; the default is 9102. See
  :ref:`jitsi_statistics`.
