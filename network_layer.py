import asyncio
import logging
from typing import Any, Generator

import aiohttp
from bs4 import BeautifulSoup

from models import Genre, MovieMeta

logger = logging.getLogger(__name__)


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


class MovieGateway:
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self, ):
        self._s: aiohttp.ClientSession | None = None
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def get_session(self) -> aiohttp.ClientSession:
        if self._s is None or self._s.closed:
            self._s = aiohttp.ClientSession(
                timeout=self.timeout,
                raise_for_status=True
            )
            logger.debug('Создана интернет-сессия')
        return self._s

    @staticmethod
    def build_url(genre: Genre = '', subgenre='', best: bool = False, filter_='watching', year='') -> str:
        base_url = 'https://rezka.ag'
        return f'{base_url}{genre}{'/best' if best else ''}{subgenre}{'' if year else f'/?filter={filter_}'}{year}'

    async def close_session(self):
        logger.debug('Сессия завершена')
        await self._s.close()

    async def request(self, link) -> bytes | None:
        session = await self.get_session()

        for attempt in range(self.MAX_RETRIES):
            try:
                logger.debug('Начато скачивание страницы')
                async with session.get(link) as r:
                    content = await r.content.read()
                    return content
            except aiohttp.ClientResponseError as e:
                logger.error(f'[{link}] Сервер вернул {e.status} {e.message}')
            except aiohttp.ClientConnectionError as e:
                logger.error(f'[{link}] Ошибка соединения: {e}')
            except asyncio.TimeoutError:
                logger.error(f'[{link}] Таймаут запроса')
            except Exception as e:
                logger.error(f'[{link}] Неизвестная ошибка: {e}')
            finally:
                await asyncio.sleep(self.RETRY_DELAY)
        return b''

    async def parse_data(self, link: str) -> BeautifulSoup | None:
        try:
            html = await self.request(link)
            soup = BeautifulSoup(html, 'lxml')
            return soup
        except Exception as e:
            logger.error(f'[{link}] Неизвестная ошибка: {e}')
        return None

    async def fetch_listening(self, link: str) -> Generator[MovieMeta, Any, None]:
        soup = await self.parse_data(link)
        return get_cards_meta(soup)


gateway = MovieGateway()
