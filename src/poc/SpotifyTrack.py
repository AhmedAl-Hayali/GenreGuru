class SpotifyTrack:
    artists = None
    disc_number = None
    duration_ms = None
    explicit = None
    external_urls = None
    href = None
    id = None
    is_playable = None
    name = None
    preview_url = None
    track_number = None
    type = None
    uri = None
    is_local = None
    def __init__(self,
                 artists,
                 disc_number,
                 duration_ms,
                 explicit,
                 external_urls,
                 href,
                 id,
                 is_playable,
                 name,
                 preview_url,
                 track_number,
                 type,
                 uri,
                 is_local):
        self.artists = artists
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.is_playable = is_playable
        self.name = name
        self.preview_url = preview_url
        self.track_number = track_number
        self.type = type
        self.uri = uri
        self.is_local = is_local