import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QLabel

from ui.global_signals import signals

logger = logging.getLogger(__name__)


class CardFrameWidget(QFrame):

    def __init__(self, name: str, text: str, link: str):
        super().__init__()

        self.name = name
        self.text = text
        self.url = link
        self._setup_ui()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        logger.debug("Левая кнопка нажата")
        if event.button() == Qt.MouseButton.LeftButton:
            signals.card_clicked.emit(self.url)
        super().mousePressEvent(event)

    def _setup_ui(self) -> None:
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setContentsMargins(5, 5, 5, 5)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self._poster = QLabel()
        self._poster.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._poster.setFixedSize(174, 262)

        self._title = QLabel(self.name)
        self._title.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred
        )
        self._title.setWordWrap(True)

        self._attrs = QLabel(self.text)
        self._attrs.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.layout.addWidget(self._poster, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self._title, alignment=Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self._attrs, alignment=Qt.AlignmentFlag.AlignBottom)
        self.layout.addStretch()

    def set_pixmap(self, pixmap: QPixmap) -> None:
        scaled = pixmap.scaled(
            self._poster.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._poster.setPixmap(scaled)
        self._poster.setText("")
        logger.debug('Установлен постер для карточки "%s"', self.name)

    def set_error(self) -> None:
        self._poster.clear()
        self._poster.setText("❌")
        self._poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logger.warning("Не удалось загрузить постер для %s", self.name)
