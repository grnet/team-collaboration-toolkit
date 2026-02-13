.. _talk_recording:

==============================
grnet.nextcloud.talk_recording
==============================

Installs the Nextcloud Talk Recording service that can record
conferences.

Example
=======

::

  roles:
    - aptiko.general.common
    - aptiko.general.nginx
    - role: grnet.nextcloud.talk_recording
      nextcloud_talk_recording_fqdn: nextcloud-talk-recording.example.com
      nextcloud_talk_recording_shared_secret: topsecret12345678

Obviously the keys and secrets should be vaulted. The recording role
also needs access to variables :data:`nextcloud_fqdn` and
:data:`nextcloud_talk_hpb_internal_secret`. Variables
:data:`nextcloud_php_upload_max_filesize`,
:data:`nextcloud_php_post_max_size` and
:data:`nextcloud_php_max_execution_time` must also be set for the
``nextcloud`` role. In the Nextcloud installation, you must go to the
Nextcloud Talk settings and specify the recording FQDN and the recording
shared secret (see :data:`nextcloud_talk_recording_shared_secret`).

Parameters
==========

Except for the variables listed below, the recording role also needs
access to variables :data:`nextcloud_fqdn`,
:data:`nextcloud_talk_hpb_fqdn` and
:data:`nextcloud_talk_hpb_internal_secret`. Variables
:data:`php_upload_max_filesize`, :data:`php_post_max_size` and
:data:`php_max_execution_time` must also be set for the ``nextcloud``
role.

.. data:: nextcloud_talk_recording_fqdn

   The FQDN of the Nextcloud Talk recording server, such as
   ``nextcloud-talk-recording.example.com``.

.. data:: nextcloud_talk_recording_shared_secret

   A secret shared with Nextcloud.  In the Nextcloud installation, you
   must go to the Nextcloud Talk settings and specify this secret.
