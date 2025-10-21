import asyncio
import logging

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QLineEdit,
    QVBoxLayout,
)
from qasync import asyncClose

from network.client import HDRezkaClient
from ui.cards_factory import CardsFactory
from ui.details_page_factory import DetailsPageFactory
from ui.global_signals import signals
from ui.widgets.main_page import MainPageScrollArea

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gw = HDRezkaClient()
        self.cards_factory = CardsFactory()
        self._setup_ui()

    def _setup_ui(self):
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)
        self.resize(1000, 1000)

    @asyncClose
    async def closeEvent(self, event):
        try:
            logger.debug("Закрытие сессии...")
            await self.gw.close()
            logger.debug("Сессия закрыта успешно")
        except Exception as e:
            logger.exception("Ошибка при закрытии сессии: %s", e)
        finally:
            super().closeEvent(event)


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.header = HeaderWidget()
        self.body = BodyStackedWidget()

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.body)

    def _connect_signals(self):
        self.body.page_changed.connect(self.header.handle_navigation_change)
        self.header.back_button.clicked.connect(self.body.change_back)


class HeaderWidget(QWidget):
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

        self.back_button = QPushButton("Назад")
        self.back_button.hide()

        self.menu_btn = QPushButton(self)
        self.menu_btn.setText("Меню")
        self.menu_btn.clicked.connect(self.menu_clicked)

        self.searchbar = QLineEdit(self)
        self.searchbar.setPlaceholderText("Поиск")
        self.searchbar.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        self.bookmarks_btn = QPushButton(self)
        self.bookmarks_btn.setText("Закладки")

        self.continue_btn = QPushButton(self)
        self.continue_btn.setText("Досмотреть")
        self.continue_btn.clicked.connect(self.continue_clicked)

        self.profile_btn = QPushButton(self)
        self.profile_btn.setText("Профиль")
        self.profile_btn.clicked.connect(self.profile_clicked)

        self.center_box = QWidget()
        self.center_box.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.center_layout = QHBoxLayout(self.center_box)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.addStretch()
        self.center_layout.addWidget(self.searchbar)
        self.center_layout.addStretch()

        self.main_layout.addWidget(self.back_button)
        self.main_layout.addWidget(self.menu_btn)
        self.main_layout.addWidget(self.center_box, 1)
        self.main_layout.addWidget(self.bookmarks_btn)
        self.main_layout.addWidget(self.continue_btn)
        self.main_layout.addWidget(self.profile_btn)

    def layout_contains(self, widget) -> bool:
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item.widget() is widget:
                return True
        return False

    @Slot(int)
    def handle_navigation_change(self, index: int):
        if index != 0:
            self.back_button.show()
        else:
            self.back_button.hide()


class BodyStackedWidget(QStackedWidget):
    page_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.details_factory = DetailsPageFactory()
        self._setup_ui()
        self.connect_signals()

    def _setup_ui(self):
        self.main_page = MainPageScrollArea()
        asyncio.create_task(self.main_page.put_cards())
        self.addWidget(self.main_page)

        self.setCurrentIndex(0)

    def connect_signals(self):
        self.details_factory.new_page.connect(self.change_page)
        signals.card_clicked.connect(self.details_factory.build_page)

    def last_page_index(self) -> int:
        return self.count() - 1

    def get_last_page(self) -> QWidget:
        return self.widget(self.last_page_index())

    def previous_page_index(self) -> int:
        return self.count() - 2

    def is_previous_page(self) -> bool:
        if self.currentIndex() == self.count() - 2:
            return True
        return False

    @Slot()
    def change_back(self):
        if self.currentIndex() == 0:
            return
        if self.count() > 1:
            self.setCurrentIndex(self.previous_page_index())
            deleted = self.widget(self.last_page_index())
            self.removeWidget(deleted)
            deleted.setParent(None)
            deleted.deleteLater()
            logger.debug("Виджет удалён")
            self.page_changed.emit(self.currentIndex())
        else:
            logger.warning("Попытка удаления при единственной странице")

    @Slot(QWidget)
    def change_page(self, widget: QWidget) -> None:
        logger.debug("Изменение страницы")
        self.addWidget(widget)
        self.setCurrentIndex(self.last_page_index())
        self.page_changed.emit(self.currentIndex())
