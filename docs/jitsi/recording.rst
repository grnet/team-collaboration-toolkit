.. _jitsi_recording:

=====================
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
