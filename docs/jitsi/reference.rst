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
- ``jitsi_excalidraw_backend_port``: The port on which the excalidraw
  backend is listening; the default is 1080. See
  :ref:`jitsi_whiteboard`.
- ``jitsi_excalidraw_backend_prometheus_port``: The port on which
  excalidraw is providing data for prometheus; the default is 9091. See
  :ref:`jitsi_whiteboard`.
- ``jitsi_welcome_background_image``: The filename of the background
  image that will be used on the Jitsi Meet front page, on top. If
  unspecified, Jitsi's default image will be used. If specified, a file
  with that name must exist in the ``files`` subdirectory of the
  playbook (or `any directory where Ansible will search`_). The file
  must be a ``.png`` with a resolution of 1280x437.
- ``jitsi_favicon``: The filename of the favicon. If unspecified,
  Jitsi's default favicon will be used. If specified, a file
  with that name must exist in the ``files`` subdirectory of the
  playbook (or `any directory where Ansible will search`_).

.. _any directory where Ansible will search: https://docs.ansible.com/ansible/latest/playbook_guide/playbook_pathing.html#resolving-local-relative-paths
