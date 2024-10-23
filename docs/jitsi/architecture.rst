==================
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
