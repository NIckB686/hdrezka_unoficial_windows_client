import asyncio
import logging

from PySide6.QtWidgets import QMainWindow
from qasync import QEventLoop

from factory import CardFactory
from myInterface import *
from network_layer import MovieGateway

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')


class MainWindow(QMainWindow):
    def __init__(self, gw: MovieGateway, factory: CardFactory):
        super().__init__()
        self.ui = Ui_MainWindow(self)
        self.setCentralWidget(self.ui)
        self.resize(1000, 1000)
        self.gw = gw
        self.cards_factory = factory
        self._connect_signals()
        self.loop = loop
        self.loop.create_task(self.put_cards())

    def _connect_signals(self) -> None:
        self.cards_factory.new_card.connect(self.ui.stackedWidget.main_page.cards_container.add_widget)
        logger.debug('Сигнал присоединён к слоту')

    async def put_cards(self):
        logger.debug('Начато добавление карточек')
        cards = await self.gw.fetch_listening(self.gw.build_url())
        await self.cards_factory.build(cards)

    async def async_close(self):
        await self.gw.close_session()
        QApplication.quit()
        logger.info('Приложение завершило работу')

    def closeEvent(self, event):
        self.loop.create_task(self.async_close())
        super().closeEvent(event)


async def main() -> None:
    logger.debug('Создан и установлен ивентлуп')
    gw = MovieGateway()
    factory = CardFactory(gw)
    app.window = MainWindow(gw, factory)
    app.window.show()


if __name__ == '__main__':
    app = QApplication()
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.create_task(main())
        loop.run_forever()
