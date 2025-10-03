import asyncio
import logging
from typing import Generator

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap

from network_layer import MovieMeta, gateway
from .card_frame_widget import CardFrameWidget

logger = logging.getLogger(__name__)


class CardFactory(QObject):
    new_card = Signal(CardFrameWidget)

    def __init__(self):
        super().__init__()
        self._gw = gateway
        logger.debug('Создана фабрика карточек')

    def build_card(self, metas: Generator[MovieMeta]):
        for meta in metas:
            widget = CardFrameWidget(meta.title, meta.year, meta.url)
            self.new_card.emit(widget)
            asyncio.create_task(self._load_pixmap(widget, meta.img_url))

    async def _load_pixmap(self, widget: CardFrameWidget, url: str):
        try:
            data = await self._gw.request(url)
            pix = QPixmap()
            pix.loadFromData(data)
            widget.set_pixmap(pix)
            logger.debug('Добавлен pixmap карточки')
        except Exception:
            widget.set_error()
