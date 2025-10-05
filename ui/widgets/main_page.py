import asyncio
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget, QScrollArea, \
    QGridLayout, QVBoxLayout
from qasync import asyncSlot

from network.parser import Parser
from network.url_builder import URLBuilder
from ui.widgets.card_frame_widget import CardFrameWidget
from ui.cards_factory import CardFactory

logger = logging.getLogger(__name__)


class MainPageScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.cards_factory = CardFactory()
        self.parser = Parser()
        self._setup_ui()
        self.connect_signals()
        asyncio.create_task(self.put_cards())

    def _setup_ui(self) -> None:
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)

        self.center_widget = QWidget()

        self.content_layout = QGridLayout(self.center_widget)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.center_widget)
        self.main_layout.addStretch()

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    def connect_signals(self):
        self.cards_factory.new_card.connect(self.add_card())
        logger.debug('Добавлен слот создания карточек')

    async def put_cards(self):
        logger.debug('Начато добавление карточек')
        cards = await self.parser.fetch_listening(URLBuilder.build_url())
        self.cards_factory.build_card(cards)

    def add_card(self):
        row, col = 0, 0

        def inner(card: CardFrameWidget):
            nonlocal row, col
            card.clicked.connect(self.on_card_clicked)
            self.content_layout.addWidget(card, row, col)
            col += 1
            if col == 4:
                row += 1
                col = 0

        return inner

    # Метод нужно будет переименовать
    @asyncSlot()
    async def on_card_clicked(self):
        ...

    def remove_widget(self, widget: QWidget) -> None:
        self.content_layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()

    def clear(self) -> None:
        while (child := self.content_layout.takeAt(0)) is not None:
            w = child.widget()
            if w:
                w.setParent(None)
                w.deleteLater()


class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.settings_btn = QPushButton('Настройки')

        layout.addWidget(self.settings_btn, alignment=Qt.AlignmentFlag.AlignLeft)
