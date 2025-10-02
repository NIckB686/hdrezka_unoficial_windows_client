from qasync import QEventLoop

from ui.myInterface import *

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logging.getLogger('qasync').setLevel(logging.WARNING)


async def _build_window() -> None:
    factory = CardFactory()
    app.window = MainWindow()
    app.window.show()


if __name__ == '__main__':
    logger.info('Начало работы приложения')
    app = QApplication()
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.create_task(_build_window())
        logger.debug('Создан и установлен EventLoop')
        loop.run_forever()
    logger.info('Приложение завершило работу')
