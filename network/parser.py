import logging
from typing import Generator, Any

from bs4 import BeautifulSoup

from models import MovieMeta
from network.aiorequests import gateway

logger = logging.getLogger(__name__)

class Parser:
    def __init__(self):
        self.gw = gateway

    async def parse_data(self, link: str) -> BeautifulSoup | None:
        try:
            html = await self.gw.request(link)
            soup = BeautifulSoup(html, 'lxml')
            return soup

        except Exception as e:
            logger.error(f'[{link}] Неизвестная ошибка: {e}')
        return None

    async def fetch_listening(self, link: str) -> Generator[MovieMeta, Any, None]:
        soup = await self.parse_data(link)
        return self.get_cards_meta(soup)

    def get_cards_meta(self, soup):
        for card in soup.find(class_='b-content__inline_items').find_all(class_='b-content__inline_item'):
            cover = card.find(class_='b-content__inline_item-cover')
            url = cover.find('a').get('href')
            img_url = cover.find('img').get('src')

            bottom = card.find(class_='b-content__inline_item-link')
            title = bottom.find('a').get_text(strip=True)
            year = bottom.find('div').get_text(strip=True)

            logger.debug('Создана мета карточки')
            yield MovieMeta(url, img_url, title, year)

    async def get_page_data(self, link: str):
        soup = await self.parse_data(link)
        table = self.get_info_table(soup)

    def get_info_table(self, soup):
        info_table = soup.find(class_='b-post__infotable clearfix')
        poster_url = info_table.find('img').get('href')
        right = info_table.find(class_='b-post__info')
        return poster_url, right