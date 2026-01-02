from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import os

from ncoreparser.data import SearchParamType, URLs
from ncoreparser.util import Size, parse_time_to_minutes


@dataclass
class Torrent:
    """
    Represents each row of torrent data as listed on the search page.
    """
    id: str
    title: str
    key: str
    size: Size
    type: SearchParamType
    date: datetime
    seed: int
    leech: int
    poster: str

    @property
    def download(self) -> str:
        return URLs.DOWNLOAD_LINK.value.format(id=self.id, key=self.key)

    @property
    def url(self) -> str:
        return URLs.DETAIL_PATTERN.value.format(id=self.id)

    def prepare_download(self, path: str) -> tuple[str, str]:
        filename = str(self.title).replace(" ", "_") + ".torrent"
        filepath = os.path.join(path, filename)
        url = str(self.download)
        return filepath, url


@dataclass
class TorrentActivity:
    """
    Represents each row of torrent data as listed on the activity page.
    """
    class Status(Enum):
        SEEDING = "Seed"
        STOPPED = "Stopped"

    torrent_id: str
    torrent_title: str
    start: str
    updated: str
    status: Status
    uploaded: Size
    downloaded: Size
    remaining: str
    ratio: float

    @property
    def remaining_minutes(self) -> int:
        return parse_time_to_minutes(self.remaining)
