from dataclasses import dataclass
from enum import Enum


@dataclass(slots=True)
class MovieMeta:
    url: str
    img_url: str
    title: str
    year: str


class Genre(str, Enum):
    FILMS = '/films'
    SERIES = '/series'
    CARTOONS = '/cartoons'
    ANIME = '/animation'
    NEW = '/new'
    ANNOUNCE = '/announce'
