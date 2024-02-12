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

    recordingService: {
        enabled: true,
        sharingEnabled: false,
    },

    liveStreaming: {
        enabled: false,
    },
};
