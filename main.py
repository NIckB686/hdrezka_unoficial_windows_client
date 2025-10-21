import asyncio
import logging
import queue
import sys
from logging.handlers import QueueHandler, QueueListener

from qasync import (
    QApplication,
    QEventLoop,
)

from ui.widgets.window import MainWindow


def setup_logging():
    log_queue = queue.Queue(-1)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )
    )

    queue_handler = QueueHandler(log_queue)

    listener = QueueListener(log_queue, console_handler)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(queue_handler)

    logging.getLogger("qasync").setLevel(logging.INFO)
    logging.getLogger("asyncio").setLevel(logging.INFO)

    listener.start()
    return listener


logger = logging.getLogger(__name__)


async def load_window():
    window = MainWindow()
    window.show()
    return window


def main():
    listener = setup_logging()
    logger.info("Начало работы приложения")
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    try:
        with loop:
            task = loop.create_task(load_window())
            logger.debug("Создан и установлен EventLoop")
            loop.run_forever()
    finally:
        logger.info("Приложение завершило работу")
        listener.stop()


if __name__ == "__main__":
    main()
