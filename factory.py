import asyncio
from typing import Generator

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap

from card_frame_widget import CardFrameWidget
from network_layer import MovieGateway, MovieMeta

import logging

logger = logging.getLogger(__name__)


class CardFactory(QObject):
    new_card = Signal(CardFrameWidget)

    def __init__(self, gw: MovieGateway):
        super().__init__()
        self._gw = gw
        logger.debug('Создана фабрика карточек')

    # Этот метод надо будет переработать -------------------------------------------------------------------
    async def build(self, metas: Generator[MovieMeta]):
        for meta in metas:
            w = CardFrameWidget(meta.title, meta.year, meta.url)
            self.new_card.emit(w)
            asyncio.create_task(self._populate(w, meta.img_url))

    async def _populate(self, widget: CardFrameWidget, url: str):
        try:
            data = await self._gw.fetch_image(url)
            pix = QPixmap()
            pix.loadFromData(data)
            widget.set_pixmap(pix)
            logger.debug('Добавлен пиксмап')
        except Exception:
            widget.set_error()
