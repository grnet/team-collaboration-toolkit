admins = {
    "jibri@auth.meet.jitsi",
    "focus@auth.meet.jitsi",
    "jvb@auth.meet.jitsi"
}

unlimited_jids = {
    "focus@auth.meet.jitsi",
    "jvb@auth.meet.jitsi",
}

plugin_paths = { "/opt/jitsi-meet/resources/prosody-plugins" };

muc_mapper_domain_base = "meet.jitsi";
muc_mapper_domain_prefix = "muc";
http_default_host = "meet.jitsi";
external_service_secret = "{{ jitsi_prosody_external_service_secret }}";
external_services = {
     { type = "turn", host = "turn.{{ ansible_host }}", port = 3478, transport = "tcp", secret = true, ttl = 86400, algorithm = "turn" },
     { type = "turns", host = "turn.{{ ansible_host }}", port = 5349, transport = "tcp", secret = true, ttl = 86400, algorithm = "turn" }
};
consider_bosh_secure = true;
consider_websocket_secure = true;

VirtualHost "meet.jitsi"
    -- We should probably use "cyrus" instead of jitsi-anonymous, but this doesn't work
    -- with the prosody 0.12 packages.
    {% if not jitsi_ldap_servers %}
    authentication = "jitsi-anonymous"
    {% else %}
    authentication = "ldap"
    ldap_server = "{{ jitsi_ldap_servers|join(" ") }}"
    ldap_base = "{{ jitsi_ldap_base }}"
    ldap_filter = "{{ jitsi_ldap_filter }}"
    ldap_mode = "{{ jitsi_ldap_mode }}"
    {% endif %}
    allow_unencrypted_plain_auth = true
    ssl = {
        key = "/etc/prosody/certs/meet.jitsi.key";
        certificate = "/etc/prosody/certs/meet.jitsi.crt";
    }
    modules_enabled = {
        "bosh";
        "websocket";
        "smacks"; -- XEP-0198: Stream Management
        "pubsub";
        "ping";
        "speakerstats";
        "conference_duration";
        "room_metadata";
        "end_conference";
        "external_services";
        "muc_breakout_rooms";
        "av_moderation";
        --"auth_cyrus";
    }
    main_muc = "muc.meet.jitsi"
    breakout_rooms_muc = "breakout.meet.jitsi"
    speakerstats_component = "speakerstats.meet.jitsi"
    conference_duration_component = "conferenceduration.meet.jitsi"
    end_conference_component = "endconference.meet.jitsi"
    av_moderation_component = "avmoderation.meet.jitsi"
    c2s_require_encryption = false


VirtualHost "guest.meet.jitsi"
    authentication = "jitsi-anonymous"
    c2s_require_encryption = false


VirtualHost "auth.meet.jitsi"
    ssl = {
        key = "/etc/prosody/certs/auth.meet.jitsi.key";
        certificate = "/etc/prosody/certs/auth.meet.jitsi.crt";
    }
    modules_enabled = {
        "limits_exception";
    }
    authentication = "internal_hashed"

VirtualHost "recorder.meet.jitsi"
    modules_enabled = {
        "ping";
    }
    authentication = "internal_plain"

Component "internal-muc.meet.jitsi" "muc"
    storage = "memory"
    modules_enabled = {
        "ping";
        }
    restrict_room_creation = true
    muc_room_locking = false
    muc_room_default_public_jids = true
    muc_room_cache_size = 1000

Component "muc.meet.jitsi" "muc"
    restrict_room_creation = true
    storage = "memory"
    modules_enabled = {
        "muc_meeting_id";
        "polls";
        "muc_domain_mapper";
        "muc_password_whitelist";
    }
    -- The size of the cache that saves state for IP addresses
        rate_limit_cache_size = 10000;

    muc_room_cache_size = 1000
    muc_room_locking = false
    muc_room_default_public_jids = true
    muc_password_whitelist = {
        "focus@auth.meet.jitsi"
    }

Component "focus.meet.jitsi" "client_proxy"
    target_address = "focus@auth.meet.jitsi"

Component "speakerstats.meet.jitsi" "speakerstats_component"
    muc_component = "muc.meet.jitsi"

Component "conferenceduration.meet.jitsi" "conference_duration_component"
    muc_component = "muc.meet.jitsi"

Component "endconference.meet.jitsi" "end_conference"
    muc_component = "muc.meet.jitsi"

Component "avmoderation.meet.jitsi" "av_moderation_component"
    muc_component = "muc.meet.jitsi"

Component "breakout.meet.jitsi" "muc"
    storage = "memory"
    restrict_room_creation = true
    muc_room_locking = false
    muc_room_default_public_jids = true
    modules_enabled = {
        "muc_meeting_id";
        "muc_domain_mapper";
        "polls";
        }

Component "metadata.meet.jitsi" "room_metadata_component"
    muc_component = "muc.meet.jitsi"
    breakout_rooms_component = "breakout.meet.jitsi"
