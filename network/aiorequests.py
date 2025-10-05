import asyncio
import logging

import aiohttp

from models import Genre

logger = logging.getLogger(__name__)

class MovieGateway:
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self):
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


gateway = MovieGateway()