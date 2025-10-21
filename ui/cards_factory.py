import asyncio
import logging

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap

from network.client import HDRezkaClient
from network.models import InlineItem
from ui.widgets.card_frame_widget import CardFrameWidget

logger = logging.getLogger(__name__)


class CardsFactory(QObject):
    new_card = Signal(CardFrameWidget)
    pixmap_ready = Signal(CardFrameWidget, QPixmap)

    def __init__(self):
        super().__init__()
        self._gw = HDRezkaClient()
        logger.debug("Создана фабрика карточек")
        self.pixmap_ready.connect(self._on_pixmap_ready)

    async def build_cards(self, metas: list[InlineItem]):
        for meta in metas:
            widget = CardFrameWidget(meta.title, meta.year, meta.url)
            self.new_card.emit(widget)
            await asyncio.sleep(0)
            asyncio.create_task(self.load_pixmap(widget, meta.img_url))

    @Slot(CardFrameWidget, QPixmap)
    def _on_pixmap_ready(self, widget: CardFrameWidget, pixmap: QPixmap):
        widget.set_pixmap(pixmap)

    async def load_pixmap(self, widget: CardFrameWidget, url: str):
        try:
            data = await self._gw.get_image(url)
            pix = QPixmap()
            pix.loadFromData(data)
            self.pixmap_ready.emit(widget, pix)
        except Exception as e:
            logger.error(
                "Не удалось добавить pixmap: (%s) %s {%s}", widget.name, url, e
            )
