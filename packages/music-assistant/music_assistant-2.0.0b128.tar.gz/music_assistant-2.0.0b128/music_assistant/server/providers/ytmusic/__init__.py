"""Youtube Music support for MusicAssistant."""

from __future__ import annotations

import asyncio
import logging
import re
from collections.abc import AsyncGenerator
from operator import itemgetter
from time import time
from typing import TYPE_CHECKING
from urllib.parse import unquote

import pytube
from aiohttp import ClientResponseError

from music_assistant.common.models.config_entries import ConfigEntry, ConfigValueType
from music_assistant.common.models.enums import ConfigEntryType, ProviderFeature
from music_assistant.common.models.errors import (
    InvalidDataError,
    LoginFailed,
    MediaNotFoundError,
    UnplayableMediaError,
)
from music_assistant.common.models.media_items import (
    Album,
    AlbumTrack,
    AlbumType,
    Artist,
    AudioFormat,
    ContentType,
    ImageType,
    ItemMapping,
    MediaItemImage,
    MediaType,
    Playlist,
    PlaylistTrack,
    ProviderMapping,
    SearchResults,
    Track,
)
from music_assistant.common.models.streamdetails import StreamDetails
from music_assistant.server.helpers.audio import get_http_stream
from music_assistant.server.helpers.auth import AuthenticationHelper
from music_assistant.server.models.music_provider import MusicProvider

from .helpers import (
    add_remove_playlist_tracks,
    get_album,
    get_artist,
    get_library_albums,
    get_library_artists,
    get_library_playlists,
    get_library_tracks,
    get_playlist,
    get_song_radio_tracks,
    get_track,
    library_add_remove_album,
    library_add_remove_artist,
    library_add_remove_playlist,
    login_oauth,
    refresh_oauth_token,
    search,
)

if TYPE_CHECKING:
    from music_assistant.common.models.config_entries import ProviderConfig
    from music_assistant.common.models.provider import ProviderManifest
    from music_assistant.server import MusicAssistant
    from music_assistant.server.models import ProviderInstanceType


CONF_COOKIE = "cookie"
CONF_ACTION_AUTH = "auth"
CONF_AUTH_TOKEN = "auth_token"
CONF_REFRESH_TOKEN = "refresh_token"
CONF_TOKEN_TYPE = "token_type"
CONF_EXPIRY_TIME = "expiry_time"

YT_DOMAIN = "https://www.youtube.com"
YTM_DOMAIN = "https://music.youtube.com"
YTM_BASE_URL = f"{YTM_DOMAIN}/youtubei/v1/"
VARIOUS_ARTISTS_YTM_ID = "UCUTXlgdcKU5vfzFqHOWIvkA"
# Playlist ID's are not unique across instances for lists like 'Liked videos', 'SuperMix' etc.
# So we need to add a delimiter to make them unique
YT_PLAYLIST_ID_DELIMITER = "🎵"
YT_PERSONAL_PLAYLISTS = (
    "LM",  # Liked songs
    "RDTMAK5uy_kset8DisdE7LSD4TNjEVvrKRTmG7a56sY",  # SuperMix
    "RDTMAK5uy_nGQKSMIkpr4o9VI_2i56pkGliD6FQRo50",  # My Mix 1
    "RDTMAK5uy_lz2owBgwWf1mjzyn_NbxzMViQzIg8IAIg",  # My Mix 2
    "RDTMAK5uy_k5UUl0lmrrfrjMpsT0CoMpdcBz1ruAO1k",  # My Mix 3
    "RDTMAK5uy_nTsa0Irmcu2li2-qHBoZxtrpG9HuC3k_Q",  # My Mix 4
    "RDTMAK5uy_lfZhS7zmIcmUhsKtkWylKzc0EN0LW90-s",  # My Mix 5
    "RDTMAK5uy_k78ni6Y4fyyl0r2eiKkBEICh9Q5wJdfXk",  # My Mix 6
    "RDTMAK5uy_lfhhWWw9v71CPrR7MRMHgZzbH6Vku9iJc",  # My Mix 7
    "RDTMAK5uy_n_5IN6hzAOwdCnM8D8rzrs3vDl12UcZpA",  # Discover Mix
    "RDTMAK5uy_lr0LWzGrq6FU9GIxWvFHTRPQD2LHMqlFA",  # New Release Mix
    "RDTMAK5uy_nilrsVWxrKskY0ZUpVZ3zpB0u4LwWTVJ4",  # Replay Mix
    "RDTMAK5uy_mZtXeU08kxXJOUhL0ETdAuZTh1z7aAFAo",  # Archive Mix
)

SUPPORTED_FEATURES = (
    ProviderFeature.LIBRARY_ARTISTS,
    ProviderFeature.LIBRARY_ALBUMS,
    ProviderFeature.LIBRARY_TRACKS,
    ProviderFeature.LIBRARY_PLAYLISTS,
    ProviderFeature.BROWSE,
    ProviderFeature.SEARCH,
    ProviderFeature.ARTIST_ALBUMS,
    ProviderFeature.ARTIST_TOPTRACKS,
    ProviderFeature.SIMILAR_TRACKS,
)

# TODO: fix disabled tests
# ruff: noqa: PLW2901, RET504


async def setup(
    mass: MusicAssistant, manifest: ProviderManifest, config: ProviderConfig
) -> ProviderInstanceType:
    """Initialize provider(instance) with given configuration."""
    prov = YoutubeMusicProvider(mass, manifest, config)
    await prov.handle_async_init()
    return prov


async def get_config_entries(
    mass: MusicAssistant,
    instance_id: str | None = None,  # noqa: ARG001
    action: str | None = None,
    values: dict[str, ConfigValueType] | None = None,
) -> tuple[ConfigEntry, ...]:
    """
    Return Config entries to setup this provider.

    instance_id: id of an existing provider instance (None if new instance setup).
    action: [optional] action key called from config entries UI.
    values: the (intermediate) raw values for config entries sent with the action.
    """
    if action == CONF_ACTION_AUTH:
        async with AuthenticationHelper(mass, values["session_id"]) as auth_helper:
            token = await login_oauth(auth_helper)
            values[CONF_AUTH_TOKEN] = token["access_token"]
            values[CONF_REFRESH_TOKEN] = token["refresh_token"]
            values[CONF_EXPIRY_TIME] = token["expires_in"]
            values[CONF_TOKEN_TYPE] = token["token_type"]
    # return the collected config entries
    return (
        ConfigEntry(
            key=CONF_AUTH_TOKEN,
            type=ConfigEntryType.SECURE_STRING,
            label="Authentication token for Youtube Music",
            description="You need to link Music Assistant to your Youtube Music account. "
            "Please ignore the code on the page the next page and click 'Next'.",
            action=CONF_ACTION_AUTH,
            action_label="Authenticate on Youtube Music",
            value=values.get(CONF_AUTH_TOKEN) if values else None,
        ),
        ConfigEntry(
            key=CONF_REFRESH_TOKEN,
            type=ConfigEntryType.SECURE_STRING,
            label=CONF_REFRESH_TOKEN,
            hidden=True,
            value=values.get(CONF_REFRESH_TOKEN) if values else None,
        ),
        ConfigEntry(
            key=CONF_EXPIRY_TIME,
            type=ConfigEntryType.INTEGER,
            label="Expiry time of auth token for Youtube Music",
            hidden=True,
            value=values.get(CONF_EXPIRY_TIME) if values else None,
        ),
        ConfigEntry(
            key=CONF_TOKEN_TYPE,
            type=ConfigEntryType.STRING,
            label="The token type required to create headers",
            hidden=True,
            value=values.get(CONF_TOKEN_TYPE) if values else None,
        ),
    )


class YoutubeMusicProvider(MusicProvider):
    """Provider for Youtube Music."""

    _headers = None
    _context = None
    _cookies = None
    _signature_timestamp = 0
    _cipher = None

    async def handle_async_init(self) -> None:
        """Set up the YTMusic provider."""
        logging.getLogger("pytube").setLevel(self.logger.level + 10)
        if not self.config.get_value(CONF_AUTH_TOKEN):
            msg = "Invalid login credentials"
            raise LoginFailed(msg)
        await self._initialize_headers()
        await self._initialize_context()
        self._cookies = {"CONSENT": "YES+1"}
        self._signature_timestamp = await self._get_signature_timestamp()

    @property
    def supported_features(self) -> tuple[ProviderFeature, ...]:
        """Return the features supported by this Provider."""
        return SUPPORTED_FEATURES

    async def search(
        self, search_query: str, media_types=list[MediaType] | None, limit: int = 5
    ) -> SearchResults:
        """Perform search on musicprovider.

        :param search_query: Search query.
        :param media_types: A list of media_types to include. All types if None.
        :param limit: Number of items to return in the search (per type).
        """
        ytm_filter = None
        if len(media_types) == 1:
            # YTM does not support multiple searchtypes, falls back to all if no type given
            if media_types[0] == MediaType.ARTIST:
                ytm_filter = "artists"
            if media_types[0] == MediaType.ALBUM:
                ytm_filter = "albums"
            if media_types[0] == MediaType.TRACK:
                ytm_filter = "songs"
            if media_types[0] == MediaType.PLAYLIST:
                ytm_filter = "playlists"
        results = await search(query=search_query, ytm_filter=ytm_filter, limit=limit)
        parsed_results = SearchResults()
        for result in results:
            try:
                if result["resultType"] == "artist":
                    parsed_results.artists.append(await self._parse_artist(result))
                elif result["resultType"] == "album":
                    parsed_results.albums.append(await self._parse_album(result))
                elif result["resultType"] == "playlist":
                    parsed_results.playlists.append(await self._parse_playlist(result))
                elif result["resultType"] == "song" and (track := await self._parse_track(result)):
                    parsed_results.tracks.append(track)
            except InvalidDataError:
                pass  # ignore invalid item
        return parsed_results

    async def get_library_artists(self) -> AsyncGenerator[Artist, None]:
        """Retrieve all library artists from Youtube Music."""
        await self._check_oauth_token()
        artists_obj = await get_library_artists(
            headers=self._headers,
        )
        for artist in artists_obj:
            yield await self._parse_artist(artist)

    async def get_library_albums(self) -> AsyncGenerator[Album, None]:
        """Retrieve all library albums from Youtube Music."""
        await self._check_oauth_token()
        albums_obj = await get_library_albums(
            headers=self._headers,
        )
        for album in albums_obj:
            yield await self._parse_album(album, album["browseId"])

    async def get_library_playlists(self) -> AsyncGenerator[Playlist, None]:
        """Retrieve all library playlists from the provider."""
        await self._check_oauth_token()
        playlists_obj = await get_library_playlists(
            headers=self._headers,
        )
        for playlist in playlists_obj:
            yield await self._parse_playlist(playlist)

    async def get_library_tracks(self) -> AsyncGenerator[Track, None]:
        """Retrieve library tracks from Youtube Music."""
        await self._check_oauth_token()
        tracks_obj = await get_library_tracks(
            headers=self._headers,
        )
        for track in tracks_obj:
            # Library tracks sometimes do not have a valid artist id
            # In that case, call the API for track details based on track id
            try:
                yield await self._parse_track(track)
            except InvalidDataError:
                track = await self.get_track(track["videoId"])
                yield track

    async def get_album(self, prov_album_id) -> Album:
        """Get full album details by id."""
        await self._check_oauth_token()
        if album_obj := await get_album(prov_album_id=prov_album_id):
            return await self._parse_album(album_obj=album_obj, album_id=prov_album_id)
        msg = f"Item {prov_album_id} not found"
        raise MediaNotFoundError(msg)

    async def get_album_tracks(self, prov_album_id: str) -> list[AlbumTrack]:
        """Get album tracks for given album id."""
        await self._check_oauth_token()
        album_obj = await get_album(prov_album_id=prov_album_id)
        if not album_obj.get("tracks"):
            return []
        tracks = []
        for idx, track_obj in enumerate(album_obj["tracks"], 1):
            track_obj["disc_number"] = 0
            track_obj["track_number"] = track_obj.get("trackNumber", idx)
            try:
                track = await self._parse_track(track_obj=track_obj)
            except InvalidDataError:
                continue
            tracks.append(track)
        return tracks

    async def get_artist(self, prov_artist_id) -> Artist:
        """Get full artist details by id."""
        await self._check_oauth_token()
        if artist_obj := await get_artist(prov_artist_id=prov_artist_id, headers=self._headers):
            return await self._parse_artist(artist_obj=artist_obj)
        msg = f"Item {prov_artist_id} not found"
        raise MediaNotFoundError(msg)

    async def get_track(self, prov_track_id) -> Track:
        """Get full track details by id."""
        await self._check_oauth_token()
        if track_obj := await get_track(
            prov_track_id=prov_track_id,
            headers=self._headers,
            signature_timestamp=self._signature_timestamp,
        ):
            return await self._parse_track(track_obj)
        msg = f"Item {prov_track_id} not found"
        raise MediaNotFoundError(msg)

    async def get_playlist(self, prov_playlist_id) -> Playlist:
        """Get full playlist details by id."""
        await self._check_oauth_token()
        # Grab the playlist id from the full url in case of personal playlists
        if YT_PLAYLIST_ID_DELIMITER in prov_playlist_id:
            prov_playlist_id = prov_playlist_id.split(YT_PLAYLIST_ID_DELIMITER)[0]
        if playlist_obj := await get_playlist(
            prov_playlist_id=prov_playlist_id, headers=self._headers
        ):
            return await self._parse_playlist(playlist_obj)
        msg = f"Item {prov_playlist_id} not found"
        raise MediaNotFoundError(msg)

    async def get_playlist_tracks(self, prov_playlist_id) -> AsyncGenerator[PlaylistTrack, None]:
        """Get all playlist tracks for given playlist id."""
        await self._check_oauth_token()
        # Grab the playlist id from the full url in case of personal playlists
        if YT_PLAYLIST_ID_DELIMITER in prov_playlist_id:
            prov_playlist_id = prov_playlist_id.split(YT_PLAYLIST_ID_DELIMITER)[0]
        # Add a try to prevent MA from stopping syncing whenever we fail a single playlist
        try:
            playlist_obj = await get_playlist(
                prov_playlist_id=prov_playlist_id, headers=self._headers
            )
        except KeyError as ke:
            self.logger.warning("Could not load playlist: %s: %s", prov_playlist_id, ke)
            return
        if "tracks" not in playlist_obj:
            return
        for index, track_obj in enumerate(playlist_obj["tracks"]):
            if track_obj["isAvailable"]:
                # Playlist tracks sometimes do not have a valid artist id
                # In that case, call the API for track details based on track id
                try:
                    track_obj["position"] = index + 1
                    if track := await self._parse_track(track_obj):
                        yield track
                except InvalidDataError:
                    if track := await self.get_track(track_obj["videoId"]):
                        yield PlaylistTrack.from_dict({**track.to_dict(), "position": index + 1})

    async def get_artist_albums(self, prov_artist_id) -> list[Album]:
        """Get a list of albums for the given artist."""
        await self._check_oauth_token()
        artist_obj = await get_artist(prov_artist_id=prov_artist_id, headers=self._headers)
        if "albums" in artist_obj and "results" in artist_obj["albums"]:
            albums = []
            for album_obj in artist_obj["albums"]["results"]:
                if "artists" not in album_obj:
                    album_obj["artists"] = [
                        {"id": artist_obj["channelId"], "name": artist_obj["name"]}
                    ]
                albums.append(await self._parse_album(album_obj, album_obj["browseId"]))
            return albums
        return []

    async def get_artist_toptracks(self, prov_artist_id) -> list[Track]:
        """Get a list of 25 most popular tracks for the given artist."""
        await self._check_oauth_token()
        artist_obj = await get_artist(prov_artist_id=prov_artist_id, headers=self._headers)
        if artist_obj.get("songs") and artist_obj["songs"].get("browseId"):
            prov_playlist_id = artist_obj["songs"]["browseId"]
            playlist_tracks = [
                x async for x in self.get_playlist_tracks(prov_playlist_id=prov_playlist_id)
            ]
            return playlist_tracks[:25]
        return []

    async def library_add(self, prov_item_id, media_type: MediaType) -> None:
        """Add an item to the library."""
        await self._check_oauth_token()
        result = False
        if media_type == MediaType.ARTIST:
            result = await library_add_remove_artist(
                headers=self._headers, prov_artist_id=prov_item_id, add=True
            )
        elif media_type == MediaType.ALBUM:
            result = await library_add_remove_album(
                headers=self._headers, prov_item_id=prov_item_id, add=True
            )
        elif media_type == MediaType.PLAYLIST:
            result = await library_add_remove_playlist(
                headers=self._headers, prov_item_id=prov_item_id, add=True
            )
        elif media_type == MediaType.TRACK:
            raise NotImplementedError
        return result

    async def library_remove(self, prov_item_id, media_type: MediaType):
        """Remove an item from the library."""
        await self._check_oauth_token()
        result = False
        if media_type == MediaType.ARTIST:
            result = await library_add_remove_artist(
                headers=self._headers, prov_artist_id=prov_item_id, add=False
            )
        elif media_type == MediaType.ALBUM:
            result = await library_add_remove_album(
                headers=self._headers, prov_item_id=prov_item_id, add=False
            )
        elif media_type == MediaType.PLAYLIST:
            result = await library_add_remove_playlist(
                headers=self._headers, prov_item_id=prov_item_id, add=False
            )
        elif media_type == MediaType.TRACK:
            raise NotImplementedError
        return result

    async def add_playlist_tracks(self, prov_playlist_id: str, prov_track_ids: list[str]) -> None:
        """Add track(s) to playlist."""
        await self._check_oauth_token()
        # Grab the playlist id from the full url in case of personal playlists
        if YT_PLAYLIST_ID_DELIMITER in prov_playlist_id:
            prov_playlist_id = prov_playlist_id.split(YT_PLAYLIST_ID_DELIMITER)[0]
        return await add_remove_playlist_tracks(
            headers=self._headers,
            prov_playlist_id=prov_playlist_id,
            prov_track_ids=prov_track_ids,
            add=True,
        )

    async def remove_playlist_tracks(
        self, prov_playlist_id: str, positions_to_remove: tuple[int, ...]
    ) -> None:
        """Remove track(s) from playlist."""
        await self._check_oauth_token()
        # Grab the playlist id from the full url in case of personal playlists
        if YT_PLAYLIST_ID_DELIMITER in prov_playlist_id:
            prov_playlist_id = prov_playlist_id.split(YT_PLAYLIST_ID_DELIMITER)[0]
        playlist_obj = await get_playlist(prov_playlist_id=prov_playlist_id, headers=self._headers)
        if "tracks" not in playlist_obj:
            return None
        tracks_to_delete = []
        for index, track in enumerate(playlist_obj["tracks"]):
            if index in positions_to_remove:
                # YT needs both the videoId and the setVideoId in order to remove
                # the track. Thus, we need to obtain the playlist details and
                # grab the info from there.
                tracks_to_delete.append(
                    {"videoId": track["videoId"], "setVideoId": track["setVideoId"]}
                )

        return await add_remove_playlist_tracks(
            headers=self._headers,
            prov_playlist_id=prov_playlist_id,
            prov_track_ids=tracks_to_delete,
            add=False,
        )

    async def get_similar_tracks(self, prov_track_id, limit=25) -> list[Track]:
        """Retrieve a dynamic list of tracks based on the provided item."""
        await self._check_oauth_token()
        result = []
        result = await get_song_radio_tracks(
            headers=self._headers,
            prov_item_id=prov_track_id,
            limit=limit,
        )
        if "tracks" in result:
            tracks = []
            for track in result["tracks"]:
                # Playlist tracks sometimes do not have a valid artist id
                # In that case, call the API for track details based on track id
                try:
                    track = await self._parse_track(track)
                    if track:
                        tracks.append(track)
                except InvalidDataError:
                    if track := await self.get_track(track["videoId"]):
                        tracks.append(track)
            return tracks
        return []

    async def get_stream_details(self, item_id: str, retry=0) -> StreamDetails:
        """Return the content details for the given track when it will be streamed."""
        await self._check_oauth_token()
        track_obj = await get_track(
            prov_track_id=item_id,
            headers=self._headers,
            signature_timestamp=self._signature_timestamp,
        )
        if not track_obj:
            msg = f"Item {item_id} not found"
            raise MediaNotFoundError(msg)
        stream_format = await self._parse_stream_format(track_obj)
        url = await self._parse_stream_url(stream_format=stream_format, item_id=item_id)
        if not await self._is_valid_deciphered_url(url=url):
            if retry > 4:
                self.logger.warning(
                    f"Could not resolve a valid URL for item '{item_id}'. "
                    "Are you playing music on another device using the same account?"
                )
                msg = f"Could not resolve a valid URL for item '{item_id}'."
                raise UnplayableMediaError(msg)
            self.logger.debug(
                "Invalid playback URL encountered. Retrying with new signature timestamp."
            )
            self._cipher = None
            self._signature_timestamp = await self._get_signature_timestamp()
            return await self.get_stream_details(item_id=item_id, retry=retry + 1)
        stream_details = StreamDetails(
            provider=self.instance_id,
            item_id=item_id,
            audio_format=AudioFormat(
                content_type=ContentType.try_parse(stream_format["mimeType"]),
            ),
            data=url,
        )
        if (
            track_obj["streamingData"].get("expiresInSeconds")
            and track_obj["streamingData"].get("expiresInSeconds").isdigit()
        ):
            stream_details.expires = time() + int(
                track_obj["streamingData"].get("expiresInSeconds")
            )
        else:
            stream_details.expires = time() + 600
        if stream_format.get("audioChannels") and str(stream_format.get("audioChannels")).isdigit():
            stream_details.audio_format.channels = int(stream_format.get("audioChannels"))
        if stream_format.get("audioSampleRate") and stream_format.get("audioSampleRate").isdigit():
            stream_details.audio_format.sample_rate = int(stream_format.get("audioSampleRate"))
        return stream_details

    async def get_audio_stream(
        self, streamdetails: StreamDetails, seek_position: int = 0
    ) -> AsyncGenerator[bytes, None]:
        """Return the audio stream for the provider item."""
        is_retry = False
        while True:
            try:
                async for chunk in get_http_stream(
                    self.mass, streamdetails.data, streamdetails, seek_position
                ):
                    yield chunk
                return
            except ClientResponseError as err:
                if not is_retry and err.status == 403:
                    # cipher expired, get a fresh one
                    self.logger.warning("Cipher expired, trying to refresh...")
                    streamdetails = await self.get_stream_details(streamdetails.item_id)
                    continue
                # raise for all other cases or we have already retried
                raise

    async def _post_data(self, endpoint: str, data: dict[str, str], **kwargs):
        """Post data to the given endpoint."""
        await self._check_oauth_token()
        url = f"{YTM_BASE_URL}{endpoint}"
        data.update(self._context)
        async with self.mass.http_session.post(
            url,
            headers=self._headers,
            json=data,
            ssl=False,
            cookies=self._cookies,
        ) as response:
            return await response.json()

    async def _get_data(self, url: str, params: dict | None = None):
        """Get data from the given URL."""
        await self._check_oauth_token()
        async with self.mass.http_session.get(
            url, headers=self._headers, params=params, cookies=self._cookies
        ) as response:
            return await response.text()

    async def _check_oauth_token(self) -> None:
        """Verify the OAuth token is valid and refresh if needed."""
        if self.config.get_value(CONF_EXPIRY_TIME) < time():
            token = await refresh_oauth_token(
                self.mass.http_session, self.config.get_value(CONF_REFRESH_TOKEN)
            )
            self.config.update({CONF_AUTH_TOKEN: token["access_token"]})
            self.config.update({CONF_EXPIRY_TIME: time() + token["expires_in"]})
            self.config.update({CONF_TOKEN_TYPE: token["token_type"]})
            await self._initialize_headers()

    async def _initialize_headers(self) -> dict[str, str]:
        """Return headers to include in the requests."""
        auth = f"{self.config.get_value(CONF_TOKEN_TYPE)} {self.config.get_value(CONF_AUTH_TOKEN)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",  # noqa: E501
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "X-Goog-AuthUser": "0",
            "x-origin": "https://music.youtube.com",
            "X-Goog-Request-Time": str(int(time())),
            "Authorization": auth,
        }
        self._headers = headers

    async def _initialize_context(self) -> dict[str, str]:
        """Return a dict to use as a context in requests."""
        self._context = {
            "context": {
                "client": {"clientName": "WEB_REMIX", "clientVersion": "0.1"},
                "user": {},
            }
        }

    async def _parse_album(self, album_obj: dict, album_id: str | None = None) -> Album:
        """Parse a YT Album response to an Album model object."""
        album_id = album_id or album_obj.get("id") or album_obj.get("browseId")
        if "title" in album_obj:
            name = album_obj["title"]
        elif "name" in album_obj:
            name = album_obj["name"]
        album = Album(
            item_id=album_id,
            name=name,
            provider=self.domain,
            provider_mappings={
                ProviderMapping(
                    item_id=str(album_id),
                    provider_domain=self.domain,
                    provider_instance=self.instance_id,
                )
            },
        )
        if album_obj.get("year") and album_obj["year"].isdigit():
            album.year = album_obj["year"]
        if "thumbnails" in album_obj:
            album.metadata.images = await self._parse_thumbnails(album_obj["thumbnails"])
        if "description" in album_obj:
            album.metadata.description = unquote(album_obj["description"])
        if "isExplicit" in album_obj:
            album.metadata.explicit = album_obj["isExplicit"]
        if "artists" in album_obj:
            album.artists = [
                self._get_artist_item_mapping(artist)
                for artist in album_obj["artists"]
                if artist.get("id")
                or artist.get("channelId")
                or artist.get("name") == "Various Artists"
            ]
        if "type" in album_obj:
            if album_obj["type"] == "Single":
                album_type = AlbumType.SINGLE
            elif album_obj["type"] == "EP":
                album_type = AlbumType.EP
            elif album_obj["type"] == "Album":
                album_type = AlbumType.ALBUM
            else:
                album_type = AlbumType.UNKNOWN
            album.album_type = album_type
        return album

    async def _parse_artist(self, artist_obj: dict) -> Artist:
        """Parse a YT Artist response to Artist model object."""
        artist_id = None
        if "channelId" in artist_obj:
            artist_id = artist_obj["channelId"]
        elif artist_obj.get("id"):
            artist_id = artist_obj["id"]
        elif artist_obj["name"] == "Various Artists":
            artist_id = VARIOUS_ARTISTS_YTM_ID
        if not artist_id:
            msg = "Artist does not have a valid ID"
            raise InvalidDataError(msg)
        artist = Artist(
            item_id=artist_id,
            name=artist_obj["name"],
            provider=self.domain,
            provider_mappings={
                ProviderMapping(
                    item_id=str(artist_id),
                    provider_domain=self.domain,
                    provider_instance=self.instance_id,
                    url=f"https://music.youtube.com/channel/{artist_id}",
                )
            },
        )
        if "description" in artist_obj:
            artist.metadata.description = artist_obj["description"]
        if artist_obj.get("thumbnails"):
            artist.metadata.images = await self._parse_thumbnails(artist_obj["thumbnails"])
        return artist

    async def _parse_playlist(self, playlist_obj: dict) -> Playlist:
        """Parse a YT Playlist response to a Playlist object."""
        playlist_id = playlist_obj["id"]
        playlist_name = playlist_obj["title"]
        # Playlist ID's are not unique across instances for lists like 'Likes', 'Supermix', etc.
        # So suffix with the instance id to make them unique
        if playlist_id in YT_PERSONAL_PLAYLISTS:
            playlist_id = f"{playlist_id}{YT_PLAYLIST_ID_DELIMITER}{self.instance_id}"
            playlist_name = f"{playlist_name} ({self.name})"
        playlist = Playlist(
            item_id=playlist_id,
            provider=self.domain,
            name=playlist_name,
            provider_mappings={
                ProviderMapping(
                    item_id=playlist_id,
                    provider_domain=self.domain,
                    provider_instance=self.instance_id,
                )
            },
        )
        if "description" in playlist_obj:
            playlist.metadata.description = playlist_obj["description"]
        if playlist_obj.get("thumbnails"):
            playlist.metadata.images = await self._parse_thumbnails(playlist_obj["thumbnails"])
        is_editable = False
        if playlist_obj.get("privacy") and playlist_obj.get("privacy") == "PRIVATE":
            is_editable = True
        playlist.is_editable = is_editable
        if authors := playlist_obj.get("author"):
            if isinstance(authors, str):
                playlist.owner = authors
            elif isinstance(authors, list):
                playlist.owner = authors[0]["name"]
            else:
                playlist.owner = authors["name"]
        else:
            playlist.owner = self.instance_id
        playlist.metadata.checksum = playlist_obj.get("checksum")
        return playlist

    async def _parse_track(self, track_obj: dict) -> Track | AlbumTrack | PlaylistTrack:
        """Parse a YT Track response to a Track model object."""
        if not track_obj.get("videoId"):
            msg = "Track is missing videoId"
            raise InvalidDataError(msg)

        if "position" in track_obj:
            track_class = PlaylistTrack
            extra_init_kwargs = {"position": track_obj["position"]}
        elif "disc_number" in track_obj and "track_number" in track_obj:
            track_class = AlbumTrack
            extra_init_kwargs = {
                "disc_number": track_obj["disc_number"],
                "track_number": track_obj["track_number"],
            }
        else:
            track_class = Track
            extra_init_kwargs = {}
        track = track_class(
            item_id=track_obj["videoId"],
            provider=self.domain,
            name=track_obj["title"],
            provider_mappings={
                ProviderMapping(
                    item_id=str(track_obj["videoId"]),
                    provider_domain=self.domain,
                    provider_instance=self.instance_id,
                    available=track_obj.get("isAvailable", True),
                    audio_format=AudioFormat(
                        content_type=ContentType.M4A,
                    ),
                )
            },
            **extra_init_kwargs,
        )

        if track_obj.get("artists"):
            track.artists = [
                self._get_artist_item_mapping(artist)
                for artist in track_obj["artists"]
                if artist.get("id")
                or artist.get("channelId")
                or artist.get("name") == "Various Artists"
            ]
        # guard that track has valid artists
        if not track.artists:
            msg = "Track is missing artists"
            raise InvalidDataError(msg)
        if track_obj.get("thumbnails"):
            track.metadata.images = await self._parse_thumbnails(track_obj["thumbnails"])
        if (
            track_obj.get("album")
            and isinstance(track_obj.get("album"), dict)
            and track_obj["album"].get("id")
        ):
            album = track_obj["album"]
            track.album = self._get_item_mapping(MediaType.ALBUM, album["id"], album["name"])
        if "isExplicit" in track_obj:
            track.metadata.explicit = track_obj["isExplicit"]
        if "duration" in track_obj and str(track_obj["duration"]).isdigit():
            track.duration = int(track_obj["duration"])
        elif "duration_seconds" in track_obj and str(track_obj["duration_seconds"]).isdigit():
            track.duration = int(track_obj["duration_seconds"])
        return track

    async def _get_signature_timestamp(self):
        """Get a signature timestamp required to generate valid stream URLs."""
        response = await self._get_data(url=YTM_DOMAIN)
        match = re.search(r'jsUrl"\s*:\s*"([^"]+)"', response)
        if match is None:
            # retry with youtube domain
            response = await self._get_data(url=YT_DOMAIN)
            match = re.search(r'jsUrl"\s*:\s*"([^"]+)"', response)
        if match is None:
            msg = "Could not identify the URL for base.js player."
            raise Exception(msg)  # pylint: disable=broad-exception-raised
        url = YTM_DOMAIN + match.group(1)
        response = await self._get_data(url=url)
        match = re.search(r"signatureTimestamp[:=](\d+)", response)
        if match is None:
            msg = "Unable to identify the signatureTimestamp."
            raise Exception(msg)  # pylint: disable=broad-exception-raised
        return int(match.group(1))

    async def _parse_stream_url(self, stream_format: dict, item_id: str) -> str:
        """Figure out the stream URL to use based on the YT track object."""
        url = None
        if stream_format.get("signatureCipher"):
            # Secured URL
            cipher_parts = {}
            for part in stream_format["signatureCipher"].split("&"):
                key, val = part.split("=", maxsplit=1)
                cipher_parts[key] = unquote(val)
            signature = await self._decipher_signature(
                ciphered_signature=cipher_parts["s"], item_id=item_id
            )
            url = cipher_parts["url"] + "&sig=" + signature
        elif stream_format.get("url"):
            # Non secured URL
            url = stream_format.get("url")
        else:
            self.logger.debug(
                f"Something went wrong. No URL found for stream format {stream_format}"
            )
        return url

    async def _decipher_signature(self, ciphered_signature: str, item_id: str):
        """Decipher the signature, required to build the Stream URL."""

        def _decipher():
            embed_url = f"https://www.youtube.com/embed/{item_id}"
            embed_html = pytube.request.get(embed_url)
            js_url = pytube.extract.js_url(embed_html)
            ytm_js = pytube.request.get(js_url)
            cipher = pytube.cipher.Cipher(js=ytm_js)
            return cipher

        if not self._cipher:
            self.logger.debug("Creating a new cipher")
            self._cipher = await asyncio.to_thread(_decipher)
        return self._cipher.get_signature(ciphered_signature)

    async def _is_valid_deciphered_url(self, url: str) -> bool:
        """Verify whether the URL has been deciphered using a valid cipher."""
        async with self.mass.http_session.head(url) as response:
            # TODO: Remove after 403 issue has been verified as fixed
            if response.status != 200:
                self.logger.debug(f"Deciphered URL HTTP status: {response.status}")
            return response.status != 403

    def _get_item_mapping(self, media_type: MediaType, key: str, name: str) -> ItemMapping:
        return ItemMapping(
            media_type=media_type,
            item_id=key,
            provider=self.instance_id,
            name=name,
        )

    def _get_artist_item_mapping(self, artist_obj: dict) -> ItemMapping:
        artist_id = artist_obj.get("id") or artist_obj.get("channelId")
        if not artist_id and artist_obj["name"] == "Various Artists":
            artist_id = VARIOUS_ARTISTS_YTM_ID
        return self._get_item_mapping(MediaType.ARTIST, artist_id, artist_obj.get("name"))

    @classmethod
    async def _parse_thumbnails(cls, thumbnails_obj: dict) -> list[MediaItemImage]:
        """Parse and sort a list of thumbnails and return the highest quality."""
        thumb = sorted(thumbnails_obj, key=itemgetter("width"), reverse=True)[0]
        return [MediaItemImage(type=ImageType.THUMB, path=thumb["url"])]

    @classmethod
    async def _parse_stream_format(cls, track_obj: dict) -> dict:
        """Grab the highest available audio stream from available streams."""
        stream_format = {}
        quality_mapper = {
            "AUDIO_QUALITY_LOW": 1,
            "AUDIO_QUALITY_MEDIUM": 2,
            "AUDIO_QUALITY_HIGH": 3,
        }
        for adaptive_format in track_obj["streamingData"]["adaptiveFormats"]:
            if adaptive_format["mimeType"].startswith("audio") and (
                not stream_format
                or quality_mapper.get(adaptive_format["audioQuality"], 0)
                > quality_mapper.get(stream_format["audioQuality"], 0)
            ):
                stream_format = adaptive_format
        if stream_format is None:
            msg = "No stream found for this track"
            raise MediaNotFoundError(msg)
        return stream_format
