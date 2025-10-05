import asyncio
import logging
import sys

from qasync import (QEventLoop,
                    QApplication,
                    )

from ui.widgets.myInterface import MainWindow

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logging.getLogger('qasync').setLevel(logging.WARNING)


async def _build_window() -> None:
    app.window = MainWindow()
    app.window.show()


if __name__ == '__main__':
    logger.info('Начало работы приложения')
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.create_task(_build_window())
        logger.debug('Создан и установлен EventLoop')
        loop.run_forever()
    logger.info('Приложение завершило работу')
