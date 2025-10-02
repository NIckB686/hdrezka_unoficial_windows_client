from qasync import QEventLoop

from ui.myInterface import *

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')


async def _build_window() -> None:
    gw = MovieGateway()
    factory = CardFactory(gw)
    app.window = MainWindow(gw, factory)
    app.window.show()


if __name__ == '__main__':
    logger.info('Начало работы приложения')
    app = QApplication()
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.create_task(_build_window())
        logger.debug('Создан и установлен ивентлуп')
        loop.run_forever()
