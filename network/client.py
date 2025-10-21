from network.api import MovieGateway
from network.errors import NotImgUrlError
from network.models import InlineItem, PageMeta
from network.parsingservice import ParsingService
from network.aiorequests import http


class HDRezkaClient:
    def __init__(self):
        self.http = http
        self.api = MovieGateway(self.http)
        self.parser = ParsingService()

    async def __aenter__(self):
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.close(*args)

    async def close(self, *args):
        await self.http.__aexit__(*args)


    async def get_image(self, url: str) -> bytes | None:
        if not url.endswith('.jpg'):
            raise NotImgUrlError
        res = await self.http.get(url)
        return res

    async def get_cards(self, url: str) -> list[InlineItem] | None:
        html = await self.http.get(url)
        return self.parser.get_cards(html)

    async def get_page_meta(self, url: str) -> PageMeta | None:
        html = await self.http.get(url)
        return self.parser.get_movie_page(html)

    async def search(self, query: str) -> list[InlineItem] | None:
        html = await self.api.search(query)
        return self.parser.get_cards(html)