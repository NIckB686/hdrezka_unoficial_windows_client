import asyncio
import logging
from typing import Callable
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QLayout,
)

from ui.widgets.card_frame_widget import CardFrameWidget
from ui.widgets.models import AbstractScrollArea

logger = logging.getLogger(__name__)


class MainPageScrollArea(AbstractScrollArea):
    def __init__(self):
        super().__init__()
        logger.debug("Создана страница главной")

    def get_layout(self) -> QLayout:
        return QGridLayout()

    async def put_cards(self):
        cards = await self.api.get_cards(self.url)
        asyncio.create_task(self.cards_factory.build_cards(cards))

    def add_card(self) -> Callable:
        row, col = 0, 0

        @Slot(CardFrameWidget)
        def inner(card: CardFrameWidget):
            logger.debug('Добавляю карточку "%s"', card.name)
            nonlocal row, col
            self.content_layout.addWidget(card, row, col)
            col += 1
            if col == 4:
                row += 1
                col = 0

        return inner


class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.settings_btn = QPushButton("Настройки")

        layout.addWidget(self.settings_btn, alignment=Qt.AlignmentFlag.AlignLeft)
