import asyncio
import logging

from aiohttp import ClientSession, ClientTimeout, ClientResponseError, ClientConnectionError

from network.errors import HTTPMaxRetriesError

logger = logging.getLogger(__name__)


class HTTPClient:
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self) -> None:
        self._session: ClientSession | None = None
        self.timeout = ClientTimeout(total=10)

    async def __aenter__(self):
        await self.get_session()
        return self

    async def __aexit__(self, *args) -> None:
        await self.close_session()

    async def get_session(self) -> ClientSession:
        if not self._session or self._session.closed:
            self._session = ClientSession(
                timeout=self.timeout,
                raise_for_status=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                  ' Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
                },
            )
            logger.debug('Создана новая HTTP-сессия')
        return self._session

    async def close_session(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            logger.debug('HTTP-сессия завершена')

    async def request(self, method: str, link: str, **kwargs) -> bytes | None:
        session = await self.get_session()
        for attempt in range(self.MAX_RETRIES):
            try:
                logger.debug('Начато скачивание: %s', link)
                async with session.request(method, link, **kwargs) as r:
                    content = await r.read()
                    return content
            except (ClientResponseError, ClientConnectionError, asyncio.TimeoutError) as e:
                logger.warning('[%s] Ошибка (%s): %s', link, e.__class__.__name__, e)
                if attempt == self.MAX_RETRIES - 1:
                    raise HTTPMaxRetriesError(link, e)
                delay = self.RETRY_DELAY * (2 ** attempt)
                await asyncio.sleep(delay)
            return None


    async def get(self, link: str, **kwargs) -> bytes | None:
        return await self.request('get', link, **kwargs)

    async def post(self, link: str, **kwargs) -> bytes | None:
        return await self.request('post', link, **kwargs)


http = HTTPClient()
