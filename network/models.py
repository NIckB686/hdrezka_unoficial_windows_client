from dataclasses import dataclass
from enum import Enum


@dataclass(slots=True)
class InlineItem:
    url: str
    img_url: str
    title: str
    year: str


@dataclass(slots=True)
class PageMeta:
    title: str
    orig_title: str
    poster_url: str
    table: str
    description: str
    cards: list[InlineItem]


class Genre(str, Enum):
    FILMS = "/films"
    SERIES = "/series"
    CARTOONS = "/cartoons"
    ANIME = "/animation"
    NEW = "/new"
    ANNOUNCE = "/announce"
