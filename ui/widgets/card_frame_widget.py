import logging

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, Qt, QMouseEvent
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QLabel

logger = logging.getLogger(__name__)


class CardFrameWidget(QFrame):
    clicked = Signal(str)

    def __init__(self, name: str, text: str, link: str):
        super().__init__()
        self.name = name
        self.text = text
        self.url = link
        self._setup_ui()

    def mousePressEvent(self, event: QMouseEvent):
        logger.debug('Левая кнопка нажата')
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.url)
        super().mousePressEvent(event)

    def _setup_ui(self):
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        self.setFixedWidth(171)
        self.setContentsMargins(5, 5, 5, 5)
        self.layout = QVBoxLayout(self)

        self._poster = QLabel()
        self._poster.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._poster.setFixedSize(166, 250)

        self._title = QLabel(self.name)
        self._title.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        self._title.setWordWrap(True)

        self._attrs = QLabel(self.text)
        self._attrs.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layout.addWidget(self._poster, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self._title, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self._attrs, alignment=Qt.AlignmentFlag.AlignTop)

    def set_pixmap(self, pixmap: QPixmap):
        self._poster.setPixmap(pixmap)

    def set_error(self):
        self._poster.setText('❌')
