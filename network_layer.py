import asyncio
from dataclasses import dataclass
from enum import Enum

import aiohttp
from bs4 import BeautifulSoup


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
            print('Создана новая сессия')
        return self._s

    async def close_session(self):
        print('Сессия закрылась')
        await self._s.close()

    @staticmethod
    def url_builder(genre: Genre = '', subgenre='', best: bool = False, filter_='watching', year='') -> str:
        base_url = 'https://rezka.ag'
        return f'{base_url}{genre}{'/best' if best else ''}{subgenre}{'' if year else f'/?filter={filter_}'}{year}'

    async def response(self, url):
        session = await self.get_session()
        try:
            async with session.get(url) as r:
                r.raise_for_status()
                return r
        except aiohttp.ClientError as e:
            print(f'Ошибка сети: {e}')

    async def fetch_listening(self, link: str) -> list[MovieMeta] | None:
        session = await self.get_session()

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print('Начато скачивание страницы')
                async with session.get(link) as r:
                    r.raise_for_status()
                    html = await r.text()

                soup = BeautifulSoup(html, 'lxml')
                out: list[MovieMeta] = []

                # ---- Следующую часть надо будет доработать/переработать-----------------
                for card in soup.find(class_='b-content__inline_items').find_all(class_='b-content__inline_item'):
                    cover = card.find(class_='b-content__inline_item-cover')
                    url = cover.find('a').get('href')
                    img_url = cover.find('img').get('src')

                    bottom = card.find(class_='b-content__inline_item-link')
                    title = bottom.find('a').get_text(strip=True)
                    year = bottom.find('div').get_text(strip=True)

                    out.append(MovieMeta(url, img_url, title, year))
                    print('Создана мета карточки')
                return out
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f'Ошибка сети {e}')
                await asyncio.sleep(self.RETRY_DELAY)
        return None

    async def fetch_image(self, url: str) -> bytes:
        session = await self.get_session()
        async with session.get(url) as r:
            r.raise_for_status()
            return await r.read()
