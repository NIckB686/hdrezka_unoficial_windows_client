import asyncio
import logging
import sys

from PySide6.QtWidgets import QWidget, QStackedWidget, QApplication, QMainWindow

from network_layer import MovieGateway
from ui.cards_factory import CardFactory
from ui.main_page import MainPage

logger = logging.getLogger()


class MainWindow(QMainWindow):
    def __init__(self, gw: MovieGateway, factory: CardFactory):
        super().__init__()
        self.gw = gw
        self.cards_factory = factory
        self._setup_ui()

    def _setup_ui(self):
        self.stacked_widget = StackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.resize(1000, 1000)

        self._connect_signals()

        asyncio.create_task(self.put_cards())

    def _connect_signals(self) -> None:
        self.cards_factory.new_card.connect(self.stacked_widget.main_page.cards_container.add_card)
        logger.debug('Сигнал присоединён к слоту')

    async def put_cards(self):
        logger.debug('Начато добавление карточек')
        cards = await self.gw.fetch_listening(self.gw.build_url())
        self.cards_factory.build_card(cards)

    async def async_close(self):
        await self.gw.close_session()
        QApplication.quit()
        logger.info('Приложение завершило работу')

    def closeEvent(self, event):
        asyncio.create_task(self.async_close())
        super().closeEvent(event)


class StackedWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.main_page = MainPage(self)
        self.addWidget(self.main_page)

        self.setCurrentIndex(0)

    def change_page(self, widget: QWidget) -> None:
        self.setCurrentWidget(widget)


def main():
    app = QApplication([])
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
