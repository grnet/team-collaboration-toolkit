.. _guide_nextcloud_talk:

=======================
Guide to Nextcloud Talk
=======================

.. contents::
   :local:
   :depth: 1

Introduction
============

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

The ``grnet.nextcloud`` collection contains two related roles:

 * :ref:`_talk_hpb`: Installs the HPB.
 * :ref:`_talk_recording`: Installs software to record conferences.

The reference for these modules includes examples that will get you
started.

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

.. _talk_hpb_architecture:

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
nginx to standard HTTPS port 443 under a path like ``/ws``. The
signaling server is mostly equivalent to Jitsi's jicofo.

The **SFU (Selective Forwarding Unit)** receives media streams from
clients and forwards selected streams to other participants. It is
equivalent to the Jitsi Video Bridge.  The SFU supported by the HPB is
called **Janus**.  Janus listens on TCP/UDP ports for RTP streams,
usually 50000-60000.  (RTP, the Realtime Transport Protocol, is used to
deliver audio and video over IP networks in real time).  At the time of
this writing the role supports only a single Janus server, although the
HPB supports more in order to distribute the load of many concurrent
conferences.

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

STUN and TURN
=============

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

