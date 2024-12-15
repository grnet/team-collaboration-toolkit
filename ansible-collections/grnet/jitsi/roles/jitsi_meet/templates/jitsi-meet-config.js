var config = {
    hosts: {
        domain: 'meet.jitsi',
        anonymousdomain: 'guest.meet.jitsi',
        muc: 'muc.meet.jitsi',
    },

    bosh: '/http-bind',

    testing: {
    },

    flags: {
    },

    enableNoAudioDetection: true,
    enableNoisyMicDetection: true,
    liveStreamingEnabled: true,
    channelLastN: -1,
    enableWelcomePage: true,

    p2p: {
        enabled: true,
        stunServers: [
            { urls: 'stun:meet-jit-si-turnrelay.jitsi.net:443' },
        ],
    },

    analytics: {
    },

    mouseMoveCallbackInterval: 1000,

    hiddenDomain: 'recorder.meet.jitsi',

    localRecording: {
      {{ jitsi_local_recording_config }}
    },

    recordingService: {
        enabled: true,
        sharingEnabled: false,
    },

    liveStreaming: {
        enabled: false,
    },

    {#
      Note on collabServerBaseUrl: Through experimentation I've found
      that the "https" is ignored and replaced with "wss"; however, it
      must be there, and it must be "https", not "http". In addition,
      any path after the hostname is also ignored; the request is always
      "wss://hostname/socket.io/(.*)". So the only thing jitsi-meet
      appears to be doing is extracting the hostname from the
      collabServerBaseUrl.
    #}
    whiteboard: {
      enabled: true,
      collabServerBaseUrl: 'https://{{ jitsi_fqdn }}/',
    },
};
