from urllib import parse
import re
from deprecated import deprecated
from typing import List

class SpotifyParser():

    def __init__(self):
        self.regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

    def url_lookup(self, msg: str) -> List[str]:
        link_regex = re.compile(self.regex, re.DOTALL)
        return re.findall(link_regex, msg)

    def filter_spotify_url(self, urls: List[str]) -> List[str]:
        return [u for u in urls if parse.urlparse(u).netloc.endswith('spotify.com')]

    def retrieve_songs(self, urls: List[str]) -> List[str]:
        return [parse.urlparse(u).path for u in urls if parse.urlparse(u).path.startswith('/track/')]

    def parse_songs(self, msg: str) -> List[str]:
        urls = self.url_lookup(msg)
        spotify_urls = self.filter_spotify_url(urls)
        return [self.trim_track(u) for u in self.retrieve_songs(spotify_urls)]
    
    @deprecated(reason="Esta vaina no se usa")
    def parse_message(self, msg: str) -> List[str]:
        urls = self.url_lookup(msg)
        spotify_urls = self.filter_spotify_url(urls)
        return [self.format_track_custom(u) for u in self.retrieve_songs(spotify_urls)]

    @deprecated(reason="Esta vaina no se usa")
    def format_track_custom(self, track_id: str):
        prefix = 'spotify'
        return parse.quote_plus(prefix+track_id.replace('/', ':'))

    def trim_track(self, track_id: str):
        return track_id.replace('/track/', '')
