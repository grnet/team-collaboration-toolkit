.. _talk:

==============
Nextcloud Talk
==============

Overview
========

Nextcloud Talk can work by simply installing the Nextcloud Talk app
using the Nextcloud's UI.  However, in that case, a teleconference can
occur with only a few people, typically up to 5-6 for video calls and
about 20 for audio-only calls. The reason is that every client needs to
upload its data (sound and image) to all other clients, which quickly
takes up all upload bandwidth.

For conferences to scale, the High Performance Backend (HPB) is
required. This is a collection of software that is installed on one or
more servers. Each client uploads its data to the server only, and the
server mixes and distributes all data to all clients. The limiting
factor in that case is usually the server's connection speed.

The collection contains two roles for Nextcloud Talk:
``grnet.nextcloud.talk_hpb``, which installs the HPB, and
``grnet.nextcloud.talk_recording``, which installs the Nextcloud Talk
Recording service that can record conferences.

Examples
========

HPB example::

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

Recording example::

  roles:
    - aptiko.general.common
    - aptiko.general.nginx
    - role: grnet.nextcloud.talk_recording
      nextcloud_talk_recording_fqdn: nextcloud-talk-recording.example.com
      nextcloud_talk_recording_shared_secret: topsecret12345678

Obviously the keys and secrets should be vaulted. The recording role
also needs access to variables :data:`nextcloud_fqdn` and
:data:`nextcloud_talk_hpb_internal_secret`. Variables
:data:`nextcloud_php_upload_max_filesize`, :data:`nextcloud_php_post_max_size`
and :data:`nextcloud_php_max_execution_time` must also be set for the
``nextcloud`` role. In the Nextcloud installation, you must go to the Nextcloud
Talk settings and specify the recording FQDN and the recording shared secret
(see :data:`nextcloud_talk_recording_shared_secret`).

.. _talk_hpb_architecture:

Hardware requirements
=====================

Because of the high requirements, it is recommended that there be a
dedicated HPB server and a dedicated recording server.

The HPB server needs to have a good connection to the network and
moderate CPU power (4 CPU cores should suffice). The need for RAM and
disk is minimal (e.g. 1G RAM and 5G disk could be enough).

The recording server needs considerable CPU power because of the video
encoding. Two CPU cores per recording should be enough. There aren't any
important requirements beyond that. 2G RAM should suffice, and so should
20G of disk (the recordings are uploaded to the Nextcloud machine and
are not kept locally).

Nextcloud Talk HPB architecture and nomenclature
================================================

The HPB consists of three basic components: the signaling server, the
publish/subscribe queue, and the Selective Forwarding Unit (SFU).

The Nextcloud Talk **signaling server**, also called
**nextcloud-spreed-signaling**, handles the signaling layer of WebRTC
communication: users' browsers or mobile apps connect to it to negotiate
and set up audio/video sessions. This server does not handle media
streams directly, only the exchange of session control messages. It
usually listens on TCP port 8080, but deployments often proxy it through
nginx to standard HTTPS port 443 under a path like /ws. The signaling
server is mostly equivalent to Jitsi's jicofo.

The **SFU (Selective Forwarding Unit)** receives media streams from
clients and forwards selected streams to other participants. It is
equivalent to the Jitsi Video Bridge.  The SFU listens on UDP port 3478
for STUN/TURN and on TCP/UDP ports for RTP streams, usually 50000-60000.
(RTP, the Realtime Transport Protocol, is used to deliver audio and
video over IP networks in real time). The SFU supported by the HPB is
called **Janus**. At the time of this writing the role supports only a
single Janus server, although the HPB supports more in order to
distribute the load of many concurrent conferences.

**NATS**, also known as **NATS.io**, is a communications system with a
publish/subscribe queue and more. The other components communicate
through it. It plays the same role prosody plays in Jitsi.

The **Nextcloud Talk app** serves the web UI and coordinates calls. It
handles user permissions and room creation, and contacts the signaling
server when users join or leave a call. It is roughly the equivalent of
Jitsi Meet.

Note the multiple meanings of the word **backend**. From the
point-of-view of the Nextcloud Talk app, the High Performance
**Backend** is the combination of nextcloud-spreed-signaling, Janus and
the NATS server. But in the nextcloud-spreed-signaling server, the word
**backend** is used for the Nextcloud (and Nextcloud Talk app)
installation. A single instance of nextcloud-spreed-signaling can serve
many Nextcloud installations, that is, many "backends". This is the
meaning with which "backend" is used in nextcloud-spreed-signaling's
``server.conf``.

Role grnet.nextcloud.talk_hpb parameters
========================================

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

Role grnet.nextcloud.talk_recording parameters
==============================================

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
