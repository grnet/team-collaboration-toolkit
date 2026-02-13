.. _talk_hpb:

========================
grnet.nextcloud.talk_hpb
========================

Installs the Nextcloud Talk High Performance Backend.

Example
=======

::

  roles:
    - aptiko.general.common
    - aptiko.general.nginx
    - role: grnet.nextcloud.talk_hpb
      nextcloud_talk_hpb_fqdn: nextcloud-talk-hpb.example.com
      nextcloud_talk_hpb_user_password: topsecret0000000
      nextcloud_talk_hpb_secret_key: topsecret0000001
      nextcloud_talk_hpb_encryption_key: topsecret00000020000000000000000
      nextcloud_talk_hpb_internal_secret: topsecret0000003
      nextcloud_talk_hpb_shared_secret: topsecret0000004
      nextcloud_talk_hpb_turn_api_key: topsecret0000005
      nextcloud_talk_hpb_turn_secret: topsecret0000006

(Obviously the keys and secrets should be vaulted.)

Then, in your Nextcloud installation, install Nextcloud Talk and
specify, as High-performance backend URL,
``wss://nextcloud-talk-hpb.example.com/standalone-signaling/``.

Parameters
==========

.. data:: nextcloud_talk_hpb_fqdn

   The FQDN of the Nextcloud Talk signaling server, such as
   ``hpb.example.com``.

.. data:: nextcloud_talk_hpb_nextcloud_instance_url

   The URL of the Nextcloud instance, such as
   ``https://nextcloud.example.com``. (This is sometimes misleadingly
   referred to as the "backend"; see the discussion about the meaning of
   "backend" at :ref:`talk_hpb_architecture`.) Currently only a single
   Nextcloud instance is supported.

.. data:: nextcloud_talk_hpb_secret_key
   nextcloud_talk_hpb_encryption_key
   nextcloud_talk_hpb_internal_secret
   nextcloud_talk_hpb_shared_secret
   nextcloud_talk_hpb_turn_api_key
   nextcloud_talk_hpb_turn_secret

   Various secrets and keys. All must be specified. The encryption key
   must be exactly 32 characters long. The rest are recommended to be
   long, but it is not a requirement.

   An easy way to produce six such secrets is ``pwgen -Bs 32 6|cat``.
