import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generator

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


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


class MovieGateway:
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self, ):
        self._s: aiohttp.ClientSession | None = None
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def get_session(self) -> aiohttp.ClientSession:
        if self._s is None or self._s.closed:
            self._s = aiohttp.ClientSession(timeout=self.timeout)
            logger.debug('Создана интернет-сессия')
        return self._s

    @staticmethod
    def build_url(genre: Genre = '', subgenre='', best: bool = False, filter_='watching', year='') -> str:
        base_url = 'https://rezka.ag'
        return f'{base_url}{genre}{'/best' if best else ''}{subgenre}{'' if year else f'/?filter={filter_}'}{year}'

    @staticmethod
    def get_cards_meta(soup):
        for card in soup.find(class_='b-content__inline_items').find_all(class_='b-content__inline_item'):
            cover = card.find(class_='b-content__inline_item-cover')
            url = cover.find('a').get('href')
            img_url = cover.find('img').get('src')

            bottom = card.find(class_='b-content__inline_item-link')
            title = bottom.find('a').get_text(strip=True)
            year = bottom.find('div').get_text(strip=True)

            logger.debug('Создана мета карточки')
            yield MovieMeta(url, img_url, title, year)

    async def close_session(self):
        logger.debug('Сессия завершена')
        await self._s.close()

    async def request(self, link):
        session = await self.get_session()

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                logger.debug('Начато скачивание страницы')
                async with session.get(link) as r:
                    r.raise_for_status()
                    html = await r.text()
                    return html

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.error(f'Ошибка сети: {e}')
                await asyncio.sleep(self.RETRY_DELAY)
        return None

    async def fetch_listening(self, link: str) -> Generator[MovieMeta, Any, None]:
        html = await self.request(link)
        soup = BeautifulSoup(html, 'lxml')

        return self.get_cards_meta(soup)

    async def fetch_image(self, url: str) -> bytes:
        session = await self.get_session()
        async with session.get(url) as r:
            r.raise_for_status()
            logger.debug('Получена картинка')
            return await r.read()
