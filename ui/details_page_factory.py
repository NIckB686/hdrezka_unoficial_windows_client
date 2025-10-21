import asyncio
import logging

from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QPixmap

from network.client import HDRezkaClient
from ui.cards_factory import CardsFactory
from ui.widgets.details_page import DetailsPage

logger = logging.getLogger(__name__)


class DetailsPageFactory(QObject):
    new_page = Signal(DetailsPage)

    def __init__(self):
        super().__init__()
        self.api = HDRezkaClient()
        self.cards_factory = CardsFactory()
        logger.debug("Создана фабрика страниц подробностей")

    def build_page(self, url):
        page = DetailsPage()
        self.new_page.emit(page)
        asyncio.create_task(self._load_page(page, url))

    async def _load_page(self, page: DetailsPage, url: str):
        meta = await self.api.get_page_meta(url)
        self._load_title(page, meta.title)
        self._load_orig_title(page, meta.orig_title)
        asyncio.create_task(self._load_pixmap(page, meta.poster_url))
        self._load_meta(page, meta.table)
        self._load_description(page, meta.description)
        asyncio.create_task(self._load_watch_also(page, meta.cards))

    @staticmethod
    def _load_title(page: DetailsPage, text: str):
        logger.debug('title loaded: %s', text)
        page.set_title(f'<h1>{text}<\h1>')

    @staticmethod
    def _load_orig_title(page: DetailsPage, text: str):
        logger.debug('orig title loaded: %s', text)
        page.set_orig_title(text)

    @staticmethod
    def _load_meta(page: DetailsPage, text: str):
        page.set_table_text(text)

    @staticmethod
    def _load_description(page: DetailsPage, text: str):
        page.set_description_text(text)

    async def _load_pixmap(self, widget: DetailsPage, url: str):
        try:
            data = await self.api.get_image(url)
            pix = QPixmap()
            pix.loadFromData(data)
            pix = pix.scaledToWidth(350, Qt.TransformationMode.SmoothTransformation)
            widget.set_poster(pix)
            logger.debug("Добавлен pixmap постера")
        except Exception as e:
            logger.error("Не удалось добавить pixmap: %s, {%s}", url, e)

    async def _load_watch_also(self, widget: DetailsPage, cards):
        self.cards_factory.new_card.connect(widget.watch_also.add_card())
        asyncio.create_task(self.cards_factory.build_cards(cards))
