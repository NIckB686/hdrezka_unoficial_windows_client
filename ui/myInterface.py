import asyncio
import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QStackedWidget, QApplication, QMainWindow, QPushButton, QHBoxLayout, QSizePolicy, \
    QLineEdit, QFrame, QVBoxLayout

from network_layer import gateway
from ui.cards_factory import CardFactory
from ui.main_page import MainPage

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gw = gateway
        self.cards_factory = CardFactory()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.header = HeaderWidget()
        self.central_widget = BodyWidget()
        self.setCentralWidget(self.central_widget)
        self.resize(1000, 1000)

        asyncio.create_task(self.put_cards())

    def _connect_signals(self) -> None:
        self.cards_factory.new_card.connect(self.central_widget.body.main_page.cards_container.add_card)
        logger.debug('Сигнал присоединён к слоту')

    async def put_cards(self):
        logger.debug('Начато добавление карточек')
        cards = await self.gw.fetch_listening(self.gw.build_url())
        self.cards_factory.build_card(cards)

    async def async_close(self):
        await self.gw.close_session()
        QApplication.quit()

    def closeEvent(self, event):
        asyncio.create_task(self.async_close())
        super().closeEvent(event)


class BodyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.header = HeaderWidget()
        self.body = BodyStackedWidget()
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.body)


class HeaderWidget(QFrame):
    menu_clicked = Signal()
    continue_clicked = Signal()
    profile_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(6)

        self.menu_btn = QPushButton(self)
        self.menu_btn.setText('Меню')
        self.menu_btn.clicked.connect(self.menu_clicked)

        self.searchbar = QLineEdit(self)
        self.searchbar.setPlaceholderText('Поиск')
        self.searchbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.bookmarks_btn = QPushButton(self)
        self.bookmarks_btn.setText('Закладки')

        self.continue_btn = QPushButton(self)
        self.continue_btn.setText('Досмотреть')
        self.continue_btn.clicked.connect(self.continue_clicked)

        self.profile_btn = QPushButton(self)
        self.profile_btn.setText('Профиль')
        self.profile_btn.clicked.connect(self.profile_clicked)

        self.center_box = QWidget()
        self.center_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.center_layout = QHBoxLayout(self.center_box)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.addStretch()
        self.center_layout.addWidget(self.searchbar)
        self.center_layout.addStretch()

        self.main_layout.addWidget(self.menu_btn)
        self.main_layout.addWidget(self.center_box, 1)
        self.main_layout.addWidget(self.bookmarks_btn)
        self.main_layout.addWidget(self.continue_btn)
        self.main_layout.addWidget(self.profile_btn)


class BodyStackedWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.main_page = MainPage()
        self.addWidget(self.main_page)

        self.setCurrentIndex(0)

    def change_page(self, widget: QWidget) -> None:
        self.setCurrentWidget(widget)
